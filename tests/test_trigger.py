"""Lesson 4: the trigger."""
import random
import unittest

from rajabot.candles import Candle
from rajabot.direction import BUY, DOWN, FLAT, MIXED, SELL, UNKNOWN, UP
from rajabot.examples import LESSON_2, LESSON_2_TWICE, LESSON_4_WEAK, LESSON_4_WICK
from rajabot.levels import HIGH, LOW, Level, LevelBook, Update
from rajabot.trigger import (AGAINST_DIRECTION, BOTH_WAYS, WEAK_CANDLE, WEAK_LEVEL, Signal, Skip, Trigger, decide)

HALF_HOUR = 1800


def run(candles, direction=None, strength=2, **settings):
    trigger = Trigger(LevelBook(strength), **settings)
    results = [trigger.on_candle(candle, direction) for candle in candles]
    return trigger, results


def after(candles, open_, high, low, close):
    """One more candle straight after the last of `candles`."""
    return Candle(candles[-1].close_time, open_, high, low, close, HALF_HOUR)


class TheLessonExamples(unittest.TestCase):
    def test_a_clean_close_through_the_ceiling_is_a_buy_signal(self):
        trigger, results = run(LESSON_2, direction=UP)
        signals = [r for r in results if r is not None]
        self.assertEqual(len(signals), 1)
        signal = signals[0]
        self.assertIsInstance(signal, Signal)
        self.assertEqual((signal.side, signal.level.kind, signal.level.price), (BUY, HIGH, 3761.0))
        self.assertIs(signal.candle, LESSON_2[8])
        self.assertEqual(signal.time, LESSON_2[8].close_time)        # exists at the close, not before
        self.assertAlmostEqual(signal.body_share, 0.75)
        self.assertEqual(signal.turns, 1)

    def test_a_wick_through_the_ceiling_is_nothing_and_the_level_stands(self):
        trigger, results = run(LESSON_4_WICK, direction=UP)
        self.assertEqual([r for r in results if r is not None], [])
        self.assertIn(3761.0, [l.price for l in trigger.book.levels])

    def test_a_close_through_on_a_poor_candle_is_skipped_and_the_level_is_used_up(self):
        trigger, results = run(LESSON_4_WEAK, direction=UP)
        skips = [r for r in results if r is not None]
        self.assertEqual(len(skips), 1)
        self.assertIsInstance(skips[0], Skip)
        self.assertEqual((skips[0].reason, skips[0].side, skips[0].level.price), (WEAK_CANDLE, BUY, 3761.0))
        self.assertEqual(skips[0].time, LESSON_4_WEAK[8].close_time)
        self.assertNotIn(3761.0, [l.price for l in trigger.book.levels])

    def test_a_stricter_body_rule_turns_the_clean_break_into_a_skip(self):
        _, results = run(LESSON_2, direction=UP, min_body=0.8)           # the candle is 75% body
        self.assertEqual([r.reason for r in results if r is not None], [WEAK_CANDLE])


class CandleQuality(unittest.TestCase):
    def test_a_candle_that_closes_above_the_ceiling_but_fell_during_the_candle_is_weak(self):
        # opens far above after a jump, sells off, still closes above 3761: bearish, so not convincing
        candles = LESSON_2[:8] + [after(LESSON_2[:8], 3766.0, 3767.0, 3762.0, 3762.5)]
        _, results = run(candles)
        self.assertEqual(results[-1].reason, WEAK_CANDLE)

    def test_exactly_half_body_passes_the_default(self):
        candles = LESSON_2[:8] + [after(LESSON_2[:8], 3757.0, 3765.0, 3755.0, 3762.0)]     # body 5 of 10
        _, results = run(candles)
        self.assertIsInstance(results[-1], Signal)


class Sells(unittest.TestCase):
    def setUp(self):
        # LESSON_2_TWICE leaves a floor at 3742 and ceilings at 3760 and 3761
        self.base = LESSON_2_TWICE

    def test_a_strong_close_below_the_floor_is_a_sell_signal(self):
        candles = self.base + [after(self.base, 3749.0, 3749.5, 3739.0, 3740.0)]
        _, results = run(candles, direction=DOWN)
        signal = results[-1]
        self.assertIsInstance(signal, Signal)
        self.assertEqual((signal.side, signal.level.kind, signal.level.price), (SELL, LOW, 3742.0))

    def test_a_bullish_candle_closing_below_the_floor_is_weak(self):
        candles = self.base + [after(self.base, 3739.0, 3741.5, 3736.0, 3741.0)]
        _, results = run(candles, direction=DOWN)
        self.assertEqual((results[-1].reason, results[-1].side), (WEAK_CANDLE, SELL))


class DirectionFilter(unittest.TestCase):
    def test_only_an_up_reading_lets_a_buy_through(self):
        for reading in (DOWN, FLAT, MIXED, UNKNOWN):
            _, results = run(LESSON_2, direction=reading)
            self.assertEqual([r.reason for r in results if r is not None], [AGAINST_DIRECTION], reading)
        _, results = run(LESSON_2, direction=UP)
        self.assertIsInstance(results[8], Signal)

    def test_with_the_filter_off_the_break_is_enough(self):
        _, results = run(LESSON_2, direction=None)
        self.assertIsInstance(results[8], Signal)

    def test_a_sell_needs_a_down_reading(self):
        candles = LESSON_2_TWICE + [after(LESSON_2_TWICE, 3749.0, 3749.5, 3739.0, 3740.0)]
        self.assertEqual(run(candles, direction=UP)[1][-1].reason, AGAINST_DIRECTION)


class SeveralLevelsAtOnce(unittest.TestCase):
    def setUp(self):
        # one strong candle closes above both ceilings, 3760 and 3761
        self.candles = LESSON_2_TWICE + [after(LESSON_2_TWICE, 3749.0, 3764.0, 3748.5, 3763.0)]

    def test_the_furthest_level_broken_is_the_signal_level(self):
        trigger, results = run(self.candles)
        signal = results[-1]
        self.assertIsInstance(signal, Signal)
        self.assertEqual(signal.level.price, 3761.0)
        self.assertEqual(signal.turns, 2)                               # price had turned here twice
        self.assertEqual([l.price for l in trigger.book.levels if l.kind == HIGH], [])     # both used up

    def test_level_quality_can_be_required(self):
        self.assertIsInstance(run(self.candles, min_turns=2)[1][-1], Signal)
        self.assertEqual(run(self.candles, min_turns=3)[1][-1].reason, WEAK_LEVEL)
        self.assertEqual(run(LESSON_2, min_turns=2)[1][8].reason, WEAK_LEVEL)       # a lone ceiling

    def test_a_ceiling_and_a_floor_broken_together_give_no_side(self):
        candle = Candle(0, 3750.0, 3756.0, 3749.0, 3755.0, HALF_HOUR)
        update = Update(broken=(Level(3752.0, HIGH, 0, 0), Level(3758.0, LOW, 0, 0)))
        result = decide(candle, update, turns=lambda price: 1)
        self.assertEqual((result.reason, result.side, result.level), (BOTH_WAYS, None, None))


class OrderOfChecks(unittest.TestCase):
    def test_the_first_failed_check_is_the_reason(self):
        # weak candle AND wrong direction AND weak level: the candle is checked first
        _, results = run(LESSON_4_WEAK, direction=DOWN, min_turns=2)
        self.assertEqual(results[8].reason, WEAK_CANDLE)
        # good candle, wrong direction AND weak level: direction comes next
        _, results = run(LESSON_2, direction=DOWN, min_turns=2)
        self.assertEqual(results[8].reason, AGAINST_DIRECTION)

    def test_nothing_broken_is_nothing(self):
        candle = Candle(0, 3750.0, 3756.0, 3749.0, 3755.0, HALF_HOUR)
        self.assertIsNone(decide(candle, Update(), turns=lambda price: 9))

    def test_settings_must_be_sensible(self):
        candle, update = Candle(0, 1, 2, 0, 1.5, HALF_HOUR), Update()
        for bad in (0, -0.1, 1.01):
            with self.assertRaises(ValueError):
                decide(candle, update, turns=lambda price: 1, min_body=bad)
        for bad in (0, 1.5):
            with self.assertRaises(ValueError):
                decide(candle, update, turns=lambda price: 1, min_turns=bad)


class NoHindsight(unittest.TestCase):
    def test_every_signal_uses_a_level_known_before_its_candle_opened(self):
        rng = random.Random(21)
        price, candles = 3750.0, []
        for i in range(3000):
            close = price + rng.uniform(-6, 6)
            high, low = max(price, close) + rng.uniform(0, 3), min(price, close) - rng.uniform(0, 3)
            candles.append(Candle(i * HALF_HOUR, price, high, low, close, HALF_HOUR))
            price = close
        _, results = run(candles)
        signals = [r for r in results if isinstance(r, Signal)]
        skips = [r for r in results if isinstance(r, Skip)]
        self.assertGreater(len(signals), 20)
        self.assertGreater(len(skips), 20)
        for signal in signals:
            self.assertLessEqual(signal.level.usable_from, signal.candle.time)
            self.assertEqual(signal.time, signal.candle.close_time)
            self.assertGreaterEqual(signal.body_share, 0.5)
            if signal.side == BUY:
                self.assertTrue(signal.candle.close > signal.level.price and signal.candle.bullish)
            else:
                self.assertTrue(signal.candle.close < signal.level.price and signal.candle.bearish)

    def test_what_was_signalled_never_changes_when_later_candles_arrive(self):
        rng = random.Random(4)
        price, candles = 3750.0, []
        for i in range(600):
            close = price + rng.uniform(-6, 6)
            candles.append(Candle(i * HALF_HOUR, price, max(price, close) + 2, min(price, close) - 2, close, HALF_HOUR))
            price = close
        _, full = run(candles, direction=UP)
        for cut in (100, 333, 599):
            self.assertEqual(run(candles[:cut], direction=UP)[1], full[:cut])


if __name__ == "__main__":
    unittest.main()
