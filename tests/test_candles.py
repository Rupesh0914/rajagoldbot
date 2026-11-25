"""Lesson 1: candles and timeframes."""
import unittest
from datetime import datetime, timezone

from rajabot.candles import Bar, Candle, build_candles, build_four_hour_candles, describe, server_seconds


def utc(*parts) -> int:
    return int(datetime(*parts, tzinfo=timezone.utc).timestamp())


def minute_bars(start: int, closes: list[float], spread: float = 0.2) -> list[Bar]:
    """One bar a minute; each opens at the previous close and wiggles 0.10 either side."""
    bars, last = [], closes[0]
    for index, close in enumerate(closes):
        bars.append(Bar(start + index * 60, last, max(last, close) + 0.10, min(last, close) - 0.10, close, spread))
        last = close
    return bars


class CandleShape(unittest.TestCase):
    def test_parts_of_a_bullish_candle(self):
        candle = Candle(0, open=3750.0, high=3758.0, low=3748.0, close=3756.0, seconds=1800)
        self.assertTrue(candle.bullish)
        self.assertFalse(candle.bearish)
        self.assertEqual((candle.range, candle.body, candle.upper_wick, candle.lower_wick), (10.0, 6.0, 2.0, 2.0))
        self.assertAlmostEqual(candle.body_share, 0.6)
        self.assertEqual(candle.close_time, 1800)
        self.assertIn("bullish", describe(candle))
        self.assertIn("60%", describe(candle))

    def test_parts_of_a_bearish_candle_that_is_mostly_wick(self):
        candle = Candle(0, open=3756.0, high=3760.0, low=3740.0, close=3755.0, seconds=1800)
        self.assertTrue(candle.bearish)
        self.assertEqual((candle.body, candle.upper_wick, candle.lower_wick), (1.0, 4.0, 15.0))
        self.assertAlmostEqual(candle.body_share, 0.05)

    def test_a_flat_candle_is_neither_and_has_no_body_share(self):
        candle = Candle(0, 3750.0, 3750.0, 3750.0, 3750.0, 1800)
        self.assertFalse(candle.bullish or candle.bearish)
        self.assertEqual(candle.body_share, 0.0)


class ThirtyMinuteCandles(unittest.TestCase):
    def test_sixty_minutes_make_one_closed_candle_and_the_forming_one_is_left_out(self):
        start = utc(2026, 11, 10, 14, 0)
        closes = [3750.0 + i * 0.5 for i in range(60)]             # rises 0.50 a minute for an hour
        candles = build_candles(minute_bars(start, closes), 30)
        self.assertEqual(len(candles), 1)                          # 14:00-14:30 closed; 14:30-15:00 not proven closed
        first = candles[0]
        self.assertEqual((first.time, first.close_time), (start, start + 1800))
        self.assertEqual((first.open, first.close), (3750.0, 3764.5))
        self.assertAlmostEqual(first.high, 3764.6)
        self.assertAlmostEqual(first.low, 3749.9)
        # one more minute, from the next half hour, proves the second candle closed
        more = minute_bars(start, closes + [3780.0])
        self.assertEqual(len(build_candles(more, 30)), 2)

    def test_a_candle_never_changes_when_later_bars_arrive(self):
        start = utc(2026, 11, 10, 14, 0)
        bars = minute_bars(start, [3750.0 + (i % 7) - (i % 5) * 0.7 for i in range(200)])
        full = build_candles(bars, 30)
        for cut in (31, 61, 95, 150):
            part = build_candles(bars[:cut], 30)
            self.assertEqual(part, full[:len(part)])               # the past is never rewritten

    def test_gaps_make_no_candle_and_candles_sit_on_the_clock(self):
        start = utc(2026, 11, 10, 14, 10)                          # first bar arrives at 14:10
        bars = minute_bars(start, [3750.0] * 5) + minute_bars(utc(2026, 11, 10, 16, 0), [3760.0] * 2)
        candles = build_candles(bars, 30)
        self.assertEqual(len(candles), 1)
        self.assertEqual(candles[0].time, utc(2026, 11, 10, 14, 0))    # sits on :00, not on the first bar
        self.assertEqual(candles[0].close, 3750.0)

    def test_the_last_candle_counts_once_the_clock_says_it_has_closed(self):
        start = utc(2026, 11, 10, 14, 0)
        bars = minute_bars(start, [3750.0] * 30)                   # exactly one half hour, nothing after
        self.assertEqual(build_candles(bars, 30), [])
        self.assertEqual(build_candles(bars, 30, as_of=start + 1799), [])
        self.assertEqual(len(build_candles(bars, 30, as_of=start + 1800)), 1)

    def test_bars_out_of_order_are_refused(self):
        bars = minute_bars(utc(2026, 11, 10, 14, 0), [3750.0, 3751.0])
        with self.assertRaises(ValueError):
            build_candles([bars[1], bars[0]], 30)
        with self.assertRaises(ValueError):
            build_candles(bars, 0)


class FourHourCandles(unittest.TestCase):
    def test_broker_clock_is_new_york_plus_seven_hours_in_winter_and_summer(self):
        # 17:00 New York is the broker's midnight, whatever the season.
        winter = utc(2026, 1, 12, 22, 0)          # 17:00 New York in January (UTC-5)
        summer = utc(2026, 7, 13, 21, 0)          # 17:00 New York in July (UTC-4)
        self.assertEqual(server_seconds(winter) % 86400, 0)
        self.assertEqual(server_seconds(summer) % 86400, 0)

    def test_four_hour_candles_start_where_the_brokers_chart_starts_them(self):
        start = utc(2026, 1, 12, 22, 0)            # broker midnight: a 4-hour candle starts here
        bars = minute_bars(start, [3750.0 + i * 0.01 for i in range(9 * 60)])     # nine hours
        candles = build_four_hour_candles(bars)
        self.assertEqual(len(candles), 2)          # two closed blocks; the third is still forming
        self.assertEqual([c.time for c in candles], [start, start + 4 * 3600])
        self.assertEqual(candles[0].open, 3750.0)
        self.assertAlmostEqual(candles[0].close, 3750.0 + 239 * 0.01)
        # in summer the same candle starts an hour earlier in UTC, because New York's clock moved
        summer = build_four_hour_candles(minute_bars(utc(2026, 7, 13, 21, 0), [3750.0] * (5 * 60)))
        self.assertEqual(summer[0].time, utc(2026, 7, 13, 21, 0))

    def test_a_block_whose_first_minutes_are_missing_still_sits_on_the_brokers_clock(self):
        # The daily break ends an hour into the broker's first block of the day.
        block_start = utc(2026, 1, 12, 22, 0)                      # broker midnight
        bars = minute_bars(block_start + 3600, [3750.0] * (4 * 60))    # first bar an hour late, runs 4 hours
        candles = build_four_hour_candles(bars)
        self.assertEqual(len(candles), 1)
        self.assertEqual(candles[0].time, block_start)
        self.assertEqual(candles[0].close_time, block_start + 4 * 3600)

    def test_the_last_four_hour_candle_counts_once_the_clock_is_in_the_next_block(self):
        start = utc(2026, 1, 12, 22, 0)
        bars = minute_bars(start, [3750.0] * (4 * 60))             # exactly one block, nothing after
        self.assertEqual(build_four_hour_candles(bars), [])
        self.assertEqual(build_four_hour_candles(bars, as_of=start + 4 * 3600 - 1), [])
        self.assertEqual(len(build_four_hour_candles(bars, as_of=start + 4 * 3600)), 1)

    def test_four_hour_candles_never_change_when_later_bars_arrive(self):
        bars = minute_bars(utc(2026, 1, 12, 22, 0), [3750.0 + (i % 11) * 0.3 for i in range(14 * 60)])
        full = build_four_hour_candles(bars)
        for cut in (241, 500, 721):
            part = build_four_hour_candles(bars[:cut])
            self.assertEqual(part, full[:len(part)])


if __name__ == "__main__":
    unittest.main()
