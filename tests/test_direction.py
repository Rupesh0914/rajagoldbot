"""Lesson 3: direction from the 4-hour chart."""
import unittest
from datetime import datetime, timezone

from rajabot.candles import Bar, Candle, build_daily_candles, build_four_hour_candles
from rajabot.direction import (BUY, DOWN, FLAT, MIXED, SELL, UNKNOWN, UP, allows, combine, daily_direction,
                               direction, direction_of_closes, explain, structure)
from rajabot.examples import LESSON_3

FOUR_HOURS = 4 * 3600


def four_hour(closes):
    return [Candle(i * FOUR_HOURS, close, close + 1, close - 1, close, FOUR_HOURS) for i, close in enumerate(closes)]


class TheRule(unittest.TestCase):
    def test_up_down_and_flat(self):
        self.assertEqual(direction_of_closes([3700, 3710, 3705, 3720, 3730, 3725, 3740]), UP)
        self.assertEqual(direction_of_closes([3740, 3730, 3735, 3720, 3710, 3715, 3700]), DOWN)
        self.assertEqual(direction_of_closes([3700, 3710, 3705, 3720, 3730, 3725, 3700]), FLAT)

    def test_only_the_two_ends_matter(self):
        # a wild middle does not change the answer: last close against the close six candles earlier
        self.assertEqual(direction_of_closes([3700, 3900, 3500, 3900, 3500, 3900, 3701]), UP)

    def test_older_candles_are_ignored(self):
        self.assertEqual(direction_of_closes([9999, 9999, 3700, 3710, 3705, 3720, 3730, 3725, 3740]), UP)

    def test_too_few_candles_is_unknown(self):
        self.assertEqual(direction_of_closes([]), UNKNOWN)
        self.assertEqual(direction_of_closes([3700, 3710, 3705, 3720, 3730, 3725]), UNKNOWN)     # six: one short

    def test_lookback_can_be_changed_and_must_be_sensible(self):
        self.assertEqual(direction_of_closes([3700, 3690], lookback=1), DOWN)
        for bad in (0, -2, 1.5):
            with self.assertRaises(ValueError):
                direction_of_closes([3700, 3710], lookback=bad)

    def test_from_candles(self):
        self.assertEqual(direction(four_hour([3700, 3710, 3705, 3720, 3730, 3725, 3740])), UP)
        self.assertEqual(direction(four_hour([3700])), UNKNOWN)


class WhatItAllows(unittest.TestCase):
    def test_buys_need_up_and_sells_need_down(self):
        self.assertTrue(allows(UP, BUY))
        self.assertTrue(allows(DOWN, SELL))
        for current, side in ((UP, SELL), (DOWN, BUY), (FLAT, BUY), (FLAT, SELL), (UNKNOWN, BUY), (UNKNOWN, SELL)):
            self.assertFalse(allows(current, side), (current, side))
        with self.assertRaises(ValueError):
            allows(UP, "hold")


class Explanation(unittest.TestCase):
    def test_sentences(self):
        self.assertEqual(explain([3700, 3710, 3705, 3720, 3730, 3725, 3740]),
                         "up: the last close 3740.00 is above 3700.00, the close 6 candles earlier. Look for buys only.")
        self.assertIn("Look for sells only", explain([3740, 3730, 3735, 3720, 3710, 3715, 3700]))
        self.assertIn("No trades", explain([3700, 3710]))
        self.assertIn("flat", explain([3700, 1, 1, 1, 1, 1, 3700]))


class NoHindsight(unittest.TestCase):
    """The 4-hour candle still forming must not move the answer."""

    def bars(self, start, closes_per_block):
        out, time = [], start
        for close in closes_per_block:
            for minute in range(240):
                out.append(Bar(time, close, close + 0.5, close - 0.5, close))
                time += 60
        return out

    def test_a_forming_candle_is_not_counted_until_its_block_is_over(self):
        start = int(datetime(2026, 1, 12, 22, 0, tzinfo=timezone.utc).timestamp())     # broker midnight
        closes = [3740, 3730, 3735, 3720, 3710, 3715, 3700]                            # seven blocks, falling
        bars = self.bars(start, closes)
        end_of_seventh = start + 7 * FOUR_HOURS

        # halfway through the seventh block only six candles have closed: not enough yet
        mid = end_of_seventh - 2 * 3600
        seen = [bar for bar in bars if bar.time < mid]
        self.assertEqual(direction(build_four_hour_candles(seen, as_of=mid)), UNKNOWN)

        # the moment the seventh block ends, it counts
        self.assertEqual(direction(build_four_hour_candles(bars, as_of=end_of_seventh)), DOWN)

        # a spike inside the next, still-forming block changes nothing
        spike = [Bar(end_of_seventh + i * 60, 3900, 3901, 3899, 3900) for i in range(30)]
        now = end_of_seventh + 30 * 60
        self.assertEqual(direction(build_four_hour_candles(bars + spike, as_of=now)), DOWN)


def zigzag(points):
    """4-hour candles from (high, low) pairs; closes sit mid-candle."""
    return [Candle(i * FOUR_HOURS, (h + l) / 2, h, l, (h + l) / 2, FOUR_HOURS) for i, (h, l) in enumerate(points)]


class Structure(unittest.TestCase):
    STEPPING_UP = [(3700, 3690), (3706, 3696), (3715, 3703), (3711, 3700), (3708, 3697), (3714, 3699),
                   (3722, 3709), (3731, 3718), (3727, 3715), (3724, 3712), (3730, 3714), (3738, 3725)]

    def test_the_lesson_example_steps_up(self):
        self.assertEqual(structure(LESSON_3), UP)
        self.assertEqual(structure(zigzag(self.STEPPING_UP)), UP)

    def test_the_mirror_image_steps_down(self):
        mirrored = [(7500 - low, 7500 - high) for high, low in self.STEPPING_UP]
        self.assertEqual(structure(zigzag(mirrored)), DOWN)

    def test_a_higher_peak_with_a_lower_dip_is_mixed(self):
        points = list(self.STEPPING_UP)
        points[9] = (3724, 3695)            # second dip undercuts the first (3697)
        points[10] = (3730, 3696)
        self.assertEqual(structure(zigzag(points)), MIXED)

    def test_it_is_unknown_until_two_peaks_and_two_dips_are_confirmed(self):
        candles = zigzag(self.STEPPING_UP)
        self.assertEqual(structure(candles[:11]), UNKNOWN)      # the second dip needs one more closed candle
        self.assertEqual(structure(candles[:12]), UP)
        self.assertEqual(structure([]), UNKNOWN)

    def test_only_peaks_and_dips_already_confirmed_are_used(self):
        import random
        from rajabot.levels import HIGH, LOW, find_swings
        rng, price, points = random.Random(5), 3750.0, []
        for _ in range(300):
            price += rng.uniform(-8, 8)
            points.append((price + rng.uniform(1, 6), price - rng.uniform(1, 6)))
        candles = zigzag(points)
        every_swing = find_swings(candles, 2)                  # found with the whole future in view
        seen = set()
        for cut in range(1, 301):
            now = candles[cut - 1].close_time
            known = [s for s in every_swing if s.usable_from <= now]      # what could be known by then
            peaks = [s.price for s in known if s.kind == HIGH][-2:]
            dips = [s.price for s in known if s.kind == LOW][-2:]
            if len(peaks) < 2 or len(dips) < 2:
                expected = UNKNOWN
            elif peaks[1] > peaks[0] and dips[1] > dips[0]:
                expected = UP
            elif peaks[1] < peaks[0] and dips[1] < dips[0]:
                expected = DOWN
            else:
                expected = MIXED
            self.assertEqual(structure(candles[:cut]), expected, cut)
            seen.add(expected)
        self.assertEqual(seen, {UNKNOWN, UP, DOWN, MIXED})


class DailyBackground(unittest.TestCase):
    def daily(self, closes):
        return [Candle(i * 86400, c, c + 5, c - 5, c, 86400) for i, c in enumerate(closes)]

    def test_higher_or_lower_than_a_trading_week_ago(self):
        self.assertEqual(daily_direction(self.daily([3700, 3720, 3690, 3710, 3730, 3745])), UP)
        self.assertEqual(daily_direction(self.daily([3745, 3720, 3690, 3710, 3730, 3700])), DOWN)
        self.assertEqual(daily_direction(self.daily([3700, 3720, 3690, 3710, 3730])), UNKNOWN)     # five: one short

    def test_daily_candles_run_from_five_pm_to_five_pm_new_york(self):
        start = int(datetime(2026, 1, 12, 22, 0, tzinfo=timezone.utc).timestamp())     # Monday 17:00 New York
        bars = [Bar(start + 3600 + i * 60, 3750.0, 3751.0, 3749.0, 3750.0) for i in range(23 * 60)]   # after the break
        self.assertEqual(build_daily_candles(bars), [])                                # not proven closed
        candles = build_daily_candles(bars, as_of=start + 86400)
        self.assertEqual([(c.time, c.close_time) for c in candles], [(start, start + 86400)])
        with self.assertRaises(ValueError):
            from rajabot.candles import build_broker_candles
            build_broker_candles(bars, 5)


class Combining(unittest.TestCase):
    def test_all_must_agree(self):
        self.assertEqual(combine(UP, UP, UP), UP)
        self.assertEqual(combine(DOWN, DOWN), DOWN)
        for readings in ((UP, DOWN), (UP, UP, MIXED), (DOWN, UNKNOWN), (UP, FLAT), (FLAT, FLAT)):
            self.assertEqual(combine(*readings), MIXED, readings)
            self.assertFalse(allows(combine(*readings), BUY))
            self.assertFalse(allows(combine(*readings), SELL))

    def test_one_reading_passes_through(self):
        for reading in (UP, DOWN, FLAT, UNKNOWN, MIXED):
            self.assertEqual(combine(reading), reading)
        with self.assertRaises(ValueError):
            combine()


if __name__ == "__main__":
    unittest.main()
