"""Lesson 5: room to run."""
import random
import unittest

from rajabot.candles import Candle
from rajabot.direction import BUY, SELL
from rajabot.examples import LESSON_2, LESSON_2_TWICE, LESSON_5_ROOM, LESSON_5_TIGHT
from rajabot.levels import HIGH, LOW, Level, LevelBook
from rajabot.space import NO_RISK, NOT_ENOUGH_ROOM, OPEN_SPACE, Room, check_room, describe_room, measure_room
from rajabot.trigger import Signal, Trigger

HALF_HOUR = 1800


def first_signal(candles, strength=2):
    trigger = Trigger(LevelBook(strength))
    for candle in candles:
        result = trigger.on_candle(candle)
        if isinstance(result, Signal):
            return result, trigger.book
    raise AssertionError("no signal in these candles")


class TheLessonExamples(unittest.TestCase):
    def test_a_ceiling_well_above_leaves_room(self):
        signal, book = first_signal(LESSON_5_ROOM)
        room = measure_room(signal, book)
        self.assertEqual((room.side, room.entry, room.risk), (BUY, 3762.0, 8.0))
        self.assertEqual((room.wall.kind, room.wall.price, room.distance), (HIGH, 3775.0, 13.0))
        self.assertAlmostEqual(room.ratio, 1.625)
        self.assertIsNone(check_room(room))                       # needs 1.0
        self.assertIsNone(check_room(room, min_ratio=1.5))
        self.assertEqual(check_room(room, min_ratio=2.0), NOT_ENOUGH_ROOM)

    def test_a_ceiling_just_above_leaves_none(self):
        signal, book = first_signal(LESSON_5_TIGHT)
        room = measure_room(signal, book)
        self.assertEqual((room.wall.price, room.distance, room.ratio), (3766.0, 4.0, 0.5))
        self.assertEqual(check_room(room), NOT_ENOUGH_ROOM)

    def test_nothing_in_the_way_is_open_space(self):
        signal, book = first_signal(LESSON_2)
        room = measure_room(signal, book)
        self.assertIsNone(room.wall)
        self.assertIsNone(room.distance)
        self.assertIsNone(room.ratio)
        self.assertEqual(room.risk, 7.0)
        self.assertIsNone(check_room(room))
        self.assertEqual(check_room(room, allow_open_space=False), OPEN_SPACE)

    def test_exactly_the_ratio_needed_is_enough(self):
        room = Room(BUY, 3762.0, 8.0, Level(3770.0, HIGH, 0, 0))
        self.assertEqual(room.ratio, 1.0)
        self.assertIsNone(check_room(room, min_ratio=1.0))
        self.assertEqual(check_room(room, min_ratio=1.01), NOT_ENOUGH_ROOM)


class Sells(unittest.TestCase):
    def test_the_wall_for_a_sell_is_the_nearest_floor_below(self):
        # LESSON_2_TWICE leaves a floor at 3742. Two lower floors are planted by hand, then a strong
        # candle closes below 3742.
        trigger = Trigger(LevelBook(2))
        for candle in LESSON_2_TWICE:
            trigger.on_candle(candle)
        trigger.book.levels.append(Level(3725.0, LOW, 0, LESSON_2_TWICE[-1].close_time))
        trigger.book.levels.append(Level(3731.0, LOW, 0, LESSON_2_TWICE[-1].close_time))
        candle = Candle(LESSON_2_TWICE[-1].close_time, 3749.0, 3749.5, 3739.0, 3740.0, HALF_HOUR)
        signal = trigger.on_candle(candle)
        self.assertEqual((signal.side, signal.level.price), (SELL, 3742.0))
        room = measure_room(signal, trigger.book)
        self.assertEqual(room.risk, 9.5)                          # entry 3740 back up to the candle high 3749.5
        self.assertEqual((room.wall.price, room.distance), (3731.0, 9.0))     # the nearer floor, not 3725
        self.assertEqual(check_room(room), NOT_ENOUGH_ROOM)       # 9.0 / 9.5 is under 1
        self.assertIsNone(check_room(room, min_ratio=0.9))


class Details(unittest.TestCase):
    def test_a_different_entry_price_changes_both_room_and_risk(self):
        signal, book = first_signal(LESSON_5_ROOM)
        room = measure_room(signal, book, entry=3763.0)           # a point worse than the close
        self.assertEqual((room.risk, room.distance), (9.0, 12.0))

    def test_an_entry_beyond_the_wall_looks_to_the_next_one(self):
        signal, book = first_signal(LESSON_5_TIGHT)
        self.assertIsNone(measure_room(signal, book, entry=3766.5).wall)      # past 3766: nothing above

    def test_no_risk_distance_is_refused(self):
        self.assertEqual(check_room(Room(BUY, 3762.0, 0.0, None)), NO_RISK)
        self.assertIsNone(Room(BUY, 3762.0, 0.0, Level(3770.0, HIGH, 0, 0)).ratio)

    def test_bad_settings_are_refused(self):
        with self.assertRaises(ValueError):
            check_room(Room(BUY, 3762.0, 8.0, None), min_ratio=0)

    def test_the_description_says_what_was_measured(self):
        signal, book = first_signal(LESSON_5_TIGHT)
        text = describe_room(measure_room(signal, book))
        self.assertIn("Next ceiling in the way: 3766.00. Room: 4.00.", text)
        self.assertTrue(text.endswith("NOT ENOUGH ROOM: skipped."))


class NoHindsight(unittest.TestCase):
    def test_the_wall_is_always_a_level_already_known_at_the_signal(self):
        rng = random.Random(8)
        price, candles = 3750.0, []
        for i in range(4000):
            close = price + rng.uniform(-6, 6)
            candles.append(Candle(i * HALF_HOUR, price, max(price, close) + rng.uniform(0, 3),
                                  min(price, close) - rng.uniform(0, 3), close, HALF_HOUR))
            price = close
        trigger, walls, open_space = Trigger(LevelBook(2)), 0, 0
        for candle in candles:
            result = trigger.on_candle(candle)
            if not isinstance(result, Signal):
                continue
            room = measure_room(result, trigger.book)
            self.assertGreater(room.risk, 0)
            if room.wall is None:
                open_space += 1
                continue
            walls += 1
            self.assertLessEqual(room.wall.usable_from, result.time)
            self.assertGreater(room.distance, 0)
            self.assertEqual(room.wall.kind, HIGH if result.side == BUY else LOW)
        self.assertGreater(walls, 50)
        self.assertGreater(open_space, 5)


if __name__ == "__main__":
    unittest.main()
