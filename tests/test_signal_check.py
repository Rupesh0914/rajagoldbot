"""The signal check (research/signal_check.py) and the history reader."""
import os
import random
import tempfile
import unittest
from datetime import datetime, timezone

from rajabot.candles import Bar
from rajabot.data import read_mt5_bars, server_to_utc
from rajabot.direction import BUY, SELL
from research.signal_check import DEVELOPMENT_ENDS, check, follow, in_session


def utc(*parts) -> int:
    return int(datetime(*parts, tzinfo=timezone.utc).timestamp())


def flat_then(start, rows, spread=0.2):
    """Bars one minute apart from (open, high, low, close) rows."""
    return [Bar(start + i * 60, o, h, l, c, spread) for i, (o, h, l, c) in enumerate(rows)]


class Follow(unittest.TestCase):
    T = utc(2025, 3, 3, 14, 0)

    def outcome(self, rows, side, unit=5.0, spread=0.2, mult=1.0, signal=None):
        bars = flat_then(self.T, rows, spread)
        return follow(bars, [b.time for b in bars], self.T if signal is None else signal, side, unit, mult)

    def test_a_buy_wins_when_the_bid_gains_one_unit_over_the_ask_paid(self):
        # entry = 3000 + 0.2 spread = 3000.2; needs a bid of 3005.2
        self.assertIsNone(self.outcome([(3000, 3005.1, 2999, 3005)], BUY))          # not there yet, then history ends
        self.assertEqual(self.outcome([(3000, 3001, 2999, 3001), (3001, 3005.2, 3000, 3005)], BUY), (1.0, "win"))

    def test_a_buy_loses_one_unit_below_the_ask_paid(self):
        self.assertEqual(self.outcome([(3000, 3001, 2995.2, 2996)], BUY), (-1.0, "loss"))

    def test_one_minute_touching_both_sides_counts_as_a_loss(self):
        self.assertEqual(self.outcome([(3000, 3006, 2995, 3000)], BUY), (-1.0, "loss"))
        self.assertEqual(self.outcome([(3000, 3006, 2994, 3000)], SELL), (-1.0, "loss"))

    def test_a_sell_enters_at_the_bid_and_pays_the_spread_to_close(self):
        # entry 3000; closes at the ask = bid + 0.2. Win needs bid low <= 2994.8; loss at bid high >= 3004.8
        self.assertIsNone(self.outcome([(3000, 3001, 2994.9, 2995)], SELL))
        self.assertEqual(self.outcome([(3000, 3001, 2994.8, 2995)], SELL), (1.0, "win"))
        self.assertEqual(self.outcome([(3000, 3004.8, 2999, 3004)], SELL), (-1.0, "loss"))

    def test_a_doubled_spread_makes_it_harder(self):
        rows = [(3000, 3005.2, 2999, 3005)]
        self.assertEqual(self.outcome(rows, BUY), (1.0, "win"))
        self.assertIsNone(self.outcome(rows, BUY, mult=2.0))                        # now needs 3005.4

    def test_undecided_after_a_day_is_closed_at_the_price_then(self):
        bars = flat_then(self.T, [(3000, 3001, 2999, 3000)] * 10)
        bars.append(Bar(self.T + 86400, 3002.2, 3003, 3002, 3002.5, 0.2))
        result, kind = follow(bars, [b.time for b in bars], self.T, BUY, 5.0)
        self.assertEqual(kind, "timeout")
        self.assertAlmostEqual(result, (3002.2 - 3000.2) / 5.0)
        result, kind = follow(bars, [b.time for b in bars], self.T, SELL, 5.0)
        self.assertAlmostEqual(result, (3000 - 3002.4) / 5.0)

    def test_no_entry_minute_soon_enough_is_no_outcome(self):
        self.assertIsNone(self.outcome([(3000, 3010, 2990, 3000)], BUY, signal=self.T - 301))
        self.assertIsNotNone(self.outcome([(3000, 3010, 2990, 3000)], BUY, signal=self.T - 300))
        self.assertIsNone(self.outcome([(3000, 3010, 2990, 3000)], BUY, unit=0.0))


class Session(unittest.TestCase):
    def test_seven_to_four_new_york_on_weekdays(self):
        # Tuesday 2025-03-04, New York is UTC-5
        self.assertFalse(in_session(utc(2025, 3, 4, 11, 59)))       # 06:59
        self.assertTrue(in_session(utc(2025, 3, 4, 12, 0)))         # 07:00
        self.assertTrue(in_session(utc(2025, 3, 4, 21, 0)))         # 16:00
        self.assertFalse(in_session(utc(2025, 3, 4, 21, 1)))        # 16:01
        self.assertFalse(in_session(utc(2025, 3, 8, 15, 0)))        # Saturday
        self.assertTrue(in_session(utc(2025, 7, 1, 11, 0)))         # summer: 07:00 New York is 11:00 UTC


class Reader(unittest.TestCase):
    def write(self, text):
        handle = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        handle.write(text)
        handle.close()
        self.addCleanup(os.unlink, handle.name)
        return handle.name

    def test_broker_midnight_is_five_pm_new_york_winter_and_summer(self):
        self.assertEqual(server_to_utc(utc(2026, 1, 13, 0, 0)), utc(2026, 1, 12, 22, 0))
        self.assertEqual(server_to_utc(utc(2026, 7, 14, 0, 0)), utc(2026, 7, 13, 21, 0))

    def test_rows_become_utc_bars_with_the_spread_as_a_price(self):
        first = utc(2026, 1, 13, 1, 0)                        # 01:00 on the broker's clock
        path = self.write("server_time,open,high,low,close,tick_volume,spread\n"
                          "%d,3750.10,3751.00,3749.90,3750.50,120,16\n"
                          "%d,3750.50,3752.00,3750.40,3751.80,95,18\n"
                          "%d,1,1,1,1,1,1\n"                  # repeated minute: dropped
                          "not,a,row\n"
                          "%d,3751.80,3752.20,3751.00,3751.10,80,17\n" % (first, first + 60, first + 60, first + 120))
        bars = read_mt5_bars(path)
        self.assertEqual([b.time for b in bars], [utc(2026, 1, 12, 23, 0) + i * 60 for i in range(3)])
        self.assertEqual(bars[0], Bar(utc(2026, 1, 12, 23, 0), 3750.10, 3751.00, 3749.90, 3750.50, 0.16))
        self.assertEqual(len(read_mt5_bars(path, before=utc(2026, 1, 12, 23, 1))), 1)     # the cut-off is never crossed

    def test_an_unknown_file_is_refused(self):
        with self.assertRaises(ValueError):
            read_mt5_bars(self.write("time,price\n1,2\n"))
        with self.assertRaises(ValueError):
            read_mt5_bars(self.write("server_time,open\n"), point=0)


def random_walk(days, seed, start=utc(2025, 1, 6)):
    rng, price, bars = random.Random(seed), 2700.0, []
    for minute in range(days * 1440):
        time = start + minute * 60
        if datetime.fromtimestamp(time, timezone.utc).weekday() >= 5:
            continue
        open_ = high = low = price
        for _ in range(4):
            price += rng.gauss(0, 0.18)
            high, low = max(high, price), min(low, price)
        bars.append(Bar(time, round(open_, 2), round(high, 2), round(low, 2), round(price, 2), 0.16))
    return bars


class TheCheck(unittest.TestCase):
    def test_random_prices_show_no_edge(self):
        text, data = check(random_walk(90, seed=2))
        self.assertIn("Not a profit backtest", text)
        self.assertIn("## What the levels must beat", text)
        every_candle = data["variants"]["No level at all: every convincing candle (body 50%)"]
        self.assertGreater(every_candle["signals"], 1000)
        self.assertTrue(0.42 < every_candle["win_share"] < 0.52, every_candle["win_share"])
        self.assertTrue(-0.15 < every_candle["average"] < 0.03, every_candle["average"])
        self.assertLess(every_candle["average_2x"], every_candle["average"])       # more spread, worse result
        self.assertIn("## Combinations", text)
        self.assertIn("## Suggested by the first run (hindsight)", text)
        in_hours = data["variants"]["New York session only (07:00-16:00)"]
        base = data["variants"]["Base: strength 4, body 50%, any level, no direction filter"]
        self.assertTrue(0 < in_hours["signals"] < base["signals"])
        self.assertGreater(in_hours["skips"]["outside_session"], 0)

    def test_it_refuses_history_past_the_development_part(self):
        bars = random_walk(10, seed=1, start=DEVELOPMENT_ENDS - 5 * 86400)
        self.assertGreaterEqual(bars[-1].time, DEVELOPMENT_ENDS)
        with self.assertRaises(ValueError):
            check(bars)

    def test_it_refuses_too_little_history(self):
        with self.assertRaises(ValueError):
            check(random_walk(2, seed=1))


if __name__ == "__main__":
    unittest.main()
