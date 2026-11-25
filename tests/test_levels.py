"""Lesson 2: levels."""
import random
import unittest

from rajabot.candles import Candle
from rajabot.examples import LESSON_2, LESSON_2_TWICE
from rajabot.levels import HIGH, LOW, Level, LevelBook, find_swings, standing_levels

HALF_HOUR = 1800


def candles_from(rows, start=0):
    """rows of (high, low, close); open is the previous close."""
    out, last = [], rows[0][2]
    for i, (high, low, close) in enumerate(rows):
        out.append(Candle(start + i * HALF_HOUR, min(max(last, low), high), high, low, close, HALF_HOUR))
        last = close
    return out


def random_candles(count, seed):
    rng = random.Random(seed)
    price, rows = 3750.0, []
    for _ in range(count):
        close = price + rng.uniform(-6, 6)
        rows.append((max(price, close) + rng.uniform(0, 3), min(price, close) - rng.uniform(0, 3), close))
        price = close
    return candles_from(rows)


class TheLessonExample(unittest.TestCase):
    def test_the_swings_and_when_each_became_usable(self):
        swings = find_swings(LESSON_2, strength=2)
        self.assertEqual([(s.kind, s.price) for s in swings], [(HIGH, 3761.0), (LOW, 3742.0)])
        ceiling, floor = swings
        # the 09:00 candle (third) made the high; it is confirmed when the fifth candle closes
        self.assertEqual(ceiling.made_at, LESSON_2[2].time)
        self.assertEqual(ceiling.usable_from, LESSON_2[4].close_time)
        self.assertEqual(floor.made_at, LESSON_2[5].time)
        self.assertEqual(floor.usable_from, LESSON_2[7].close_time)

    def test_the_story_candle_by_candle(self):
        book = LevelBook(strength=2)
        updates = [book.add(candle) for candle in LESSON_2]
        self.assertEqual([len(u.new) for u in updates], [0, 0, 0, 0, 1, 0, 0, 1, 0, 0])
        self.assertEqual([len(u.broken) for u in updates], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
        self.assertEqual(updates[8].broken[0].price, 3761.0)          # the 12:00 candle closed at 3762
        self.assertEqual([(l.kind, l.price) for l in book.levels], [(LOW, 3742.0)])
        self.assertEqual(standing_levels(LESSON_2, 2), book.levels)

    def test_a_bigger_strength_is_stricter(self):
        # With 4 candles needed on each side, the 09:00 high has only 2 candles before it, so it is
        # no swing. The 10:30 low has 4 on each side and is confirmed when the 12:30 candle closes.
        swings = find_swings(LESSON_2, strength=4)
        self.assertEqual([(s.kind, s.price) for s in swings], [(LOW, 3742.0)])
        self.assertEqual(swings[0].usable_from, LESSON_2[9].close_time)


class SwingRules(unittest.TestCase):
    def test_a_swing_needs_candles_on_both_sides(self):
        rows = [(10, 5, 8), (12, 7, 11), (15, 9, 12), (13, 8, 9), (11, 6, 7)]
        self.assertEqual(find_swings(candles_from(rows[:4]), 2), [])          # one candle short
        swings = find_swings(candles_from(rows), 2)
        self.assertEqual([(s.kind, s.price) for s in swings], [(HIGH, 15)])

    def test_equal_highs_make_no_swing(self):
        rows = [(10, 5, 8), (12, 7, 11), (15, 9, 12), (15, 8, 9), (11, 6, 7), (10, 5.5, 6)]
        self.assertEqual([s for s in find_swings(candles_from(rows), 2) if s.kind == HIGH], [])

    def test_one_candle_can_be_both_a_swing_high_and_a_swing_low(self):
        rows = [(10, 8, 9), (10.5, 8.5, 9), (14, 4, 9), (10.5, 8.5, 9), (10, 8, 9)]
        swings = find_swings(candles_from(rows), 2)
        self.assertEqual({(s.kind, s.price) for s in swings}, {(HIGH, 14), (LOW, 4)})

    def test_strength_must_be_a_whole_number_of_one_or_more(self):
        for bad in (0, -1, 1.5):
            with self.assertRaises(ValueError):
                find_swings([], bad)
            with self.assertRaises(ValueError):
                LevelBook(bad)
        with self.assertRaises(ValueError):
            LevelBook(2, max_age_days=0)


class NoHindsight(unittest.TestCase):
    def test_a_level_is_never_usable_before_the_candles_after_it_closed(self):
        for seed in range(5):
            candles = random_candles(300, seed)
            for strength in (1, 2, 4, 8):
                swings = find_swings(candles, strength)
                self.assertTrue(swings)
                for swing in swings:
                    self.assertEqual(swing.usable_from, swing.made_at + (strength + 1) * HALF_HOUR)

    def test_what_was_known_at_any_moment_never_changes_later(self):
        candles = random_candles(400, seed=11)
        full_book, snapshots = LevelBook(4), []
        for candle in candles:
            full_book.add(candle)
            snapshots.append(list(full_book.levels))
        for cut in (9, 50, 123, 300, 400):
            self.assertEqual(standing_levels(candles[:cut], 4), snapshots[cut - 1])
            known = [s for s in find_swings(candles, 4) if s.usable_from <= candles[cut - 1].close_time]
            self.assertEqual(find_swings(candles[:cut], 4), known)


class BrokenAndExpired(unittest.TestCase):
    def setUp(self):
        self.book = LevelBook(strength=1, max_age_days=1.0)
        for candle in candles_from([(10, 8, 9), (14, 9, 10), (11, 7, 9)]):
            self.update = self.book.add(candle)
        self.next_time = 3 * HALF_HOUR

    def add(self, high, low, close, at=None):
        time = self.next_time if at is None else at
        self.next_time = time + HALF_HOUR
        return self.book.add(Candle(time, close, high, low, close, HALF_HOUR))

    def test_setup_has_one_ceiling(self):
        self.assertEqual([(l.kind, l.price) for l in self.book.levels], [(HIGH, 14)])

    def test_a_wick_through_a_level_does_not_break_it(self):
        update = self.add(high=16, low=9, close=13.5)
        self.assertEqual(update.broken, ())
        self.assertIn(14, [l.price for l in self.book.levels])

    def test_a_close_exactly_on_the_level_does_not_break_it(self):
        self.assertEqual(self.add(high=14.5, low=9, close=14).broken, ())

    def test_a_close_through_breaks_it_for_good(self):
        update = self.add(high=15, low=9, close=14.5)
        self.assertEqual([l.price for l in update.broken], [14])
        self.add(high=13, low=9, close=10)                 # price comes back under: still gone
        self.assertNotIn(14, [l.price for l in self.book.levels if l.kind == HIGH])

    def test_a_floor_breaks_on_a_close_below(self):
        book = LevelBook(strength=1)
        for candle in candles_from([(10, 8, 9), (9, 5, 8), (10, 7, 9)]):
            book.add(candle)
        self.assertEqual([(l.kind, l.price) for l in book.levels], [(LOW, 5)])
        update = book.add(Candle(3 * HALF_HOUR, 9, 9.5, 4, 4.5, HALF_HOUR))
        self.assertEqual([l.price for l in update.broken], [5])

    def test_an_old_level_expires(self):
        level = self.book.levels[0]
        day_later = level.usable_from + 86400 - HALF_HOUR       # closes exactly one day after it became usable
        update = self.add(high=12, low=9, close=10, at=day_later)
        self.assertEqual([l.price for l in update.expired], [14])
        self.assertNotIn(14, [l.price for l in self.book.levels])

    def test_a_level_one_candle_short_of_the_age_limit_still_stands(self):
        level = self.book.levels[0]
        update = self.add(high=12, low=9, close=10, at=level.usable_from + 86400 - 2 * HALF_HOUR)
        self.assertEqual(update.expired, ())

    def test_candles_out_of_order_are_refused(self):
        with self.assertRaises(ValueError):
            self.add(high=12, low=9, close=10, at=0)


class Lookups(unittest.TestCase):
    def test_nearest_first_on_each_side(self):
        book = LevelBook(strength=1)
        book.levels = [Level(3770.0, HIGH, 0, 0), Level(3760.0, HIGH, 0, 0), Level(3740.0, LOW, 0, 0),
                       Level(3745.0, LOW, 0, 0), Level(3750.0, HIGH, 0, 0)]
        self.assertEqual([l.price for l in book.ceilings_above(3755.0)], [3760.0, 3770.0])
        self.assertEqual([l.price for l in book.floors_below(3755.0)], [3745.0, 3740.0])
        self.assertEqual(book.ceilings_above(3770.0), [])


class LevelQuality(unittest.TestCase):
    def book_after(self, candles, strength=2, **options):
        book = LevelBook(strength, **options)
        for candle in candles:
            book.add(candle)
        return book

    def test_reach_is_half_the_average_candle_height(self):
        book = LevelBook(2)
        self.assertEqual(book.reach, 0.0)
        self.assertEqual(book.turns_at(3750.0), 0)
        for candle in LESSON_2_TWICE:
            book.add(candle)
        heights = [candle.range for candle in LESSON_2_TWICE]
        self.assertAlmostEqual(book.reach, 0.5 * sum(heights) / len(heights))
        self.assertAlmostEqual(book.reach, 3.5)

    def test_reach_uses_only_the_last_twenty_candles(self):
        tall = candles_from([(3760, 3740, 3750)] * 5)                       # 20 high
        short = candles_from([(3751, 3749, 3750)] * 20, start=5 * HALF_HOUR)   # 2 high
        self.assertAlmostEqual(self.book_after(tall + short, strength=1).reach, 1.0)

    def test_two_turns_at_the_same_area_count_as_two(self):
        book = self.book_after(LESSON_2_TWICE)
        self.assertEqual(sorted((l.kind, l.price) for l in book.levels),
                         [(HIGH, 3760.0), (HIGH, 3761.0), (LOW, 3742.0)])
        self.assertEqual(book.turns_at(3761.0), 2)
        self.assertEqual(book.turns_at(3760.0), 2)
        self.assertEqual(book.turns_at(3742.0), 1)
        self.assertEqual(book.turns_at(3700.0), 0)

    def test_a_broken_level_still_counts_as_a_turn_at_that_area(self):
        # In the first example the 3761 ceiling is broken, but price did turn there once.
        book = self.book_after(LESSON_2)
        self.assertEqual([(l.kind, l.price) for l in book.levels], [(LOW, 3742.0)])
        self.assertEqual(book.turns_at(3761.0), 1)

    def test_old_turns_stop_counting(self):
        book = self.book_after(LESSON_2_TWICE, max_age_days=1.0)
        late = LESSON_2_TWICE[-1].time + 2 * 86400
        book.add(Candle(late, 3750.0, 3751.0, 3749.0, 3750.0, HALF_HOUR))
        self.assertEqual(book.levels, [])
        self.assertEqual(book.turns_at(3761.0), 0)

    def test_quality_known_at_any_moment_never_changes_later(self):
        candles = random_candles(400, seed=3)
        full, seen = LevelBook(2), []
        for candle in candles:
            full.add(candle)
            seen.append((full.reach, [full.turns_at(level.price) for level in full.levels]))
        for cut in (30, 111, 250, 400):
            part = self.book_after(candles[:cut])
            self.assertEqual((part.reach, [part.turns_at(level.price) for level in part.levels]), seen[cut - 1])


if __name__ == "__main__":
    unittest.main()
