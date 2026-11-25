"""Lesson 3: direction from the 4-hour chart."""
import unittest
from datetime import datetime, timezone

from rajabot.candles import Bar, Candle, build_four_hour_candles
from rajabot.direction import (BUY, DOWN, FLAT, SELL, UNKNOWN, UP, allows, direction, direction_of_closes,
                               explain)

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


if __name__ == "__main__":
    unittest.main()
