"""The whole bot loop (rajabot/engine.py)."""
import unittest
from dataclasses import replace
from datetime import datetime, timezone

from rajabot.candles import NEW_YORK, Bar, build_candles
from rajabot.engine import CANDLE, LEVEL, Bot, Settings, run
from rajabot.filters import trading_day
from research.signal_check import Readings
from research.trade_test import BENCHMARK, LEVEL_TRIGGER, NO_TARGET_R, run_setup
from tests.test_signal_check import random_walk

BIG = 1_000_000.0
OPEN = dict(max_spread=None, daily_limits=False)        # the lesson-8 rules off, as in the earlier research runs


class AgreesWithTheResearchCode(unittest.TestCase):
    """Two separately written versions of the rules must take exactly the same trades."""

    @classmethod
    def setUpClass(cls):
        cls.bars = random_walk(150, seed=7)
        cls.times = [bar.time for bar in cls.bars]
        cls.candles = build_candles(cls.bars, 30, as_of=cls.bars[-1].time + 3600)
        cls.readings = Readings(cls.bars)

    def compare(self, settings, setup):
        bot = run(self.bars, settings, BIG, compound=False)
        research = run_setup(self.bars, self.times, self.candles, self.readings, setup)["trades"]
        self.assertGreater(len(research), 40)
        self.assertEqual(len(bot.trades), len(research))
        for mine, theirs in zip(bot.trades, research):
            self.assertEqual((mine.opened_at, mine.side, mine.reason), (theirs["time"], theirs["side"], theirs["reason"]))
            self.assertAlmostEqual(mine.r, theirs["r"], places=9)

    def test_any_convincing_candle_target_two_r(self):
        self.compare(Settings("c1", **OPEN), BENCHMARK)

    def test_any_convincing_candle_no_target(self):
        self.compare(Settings("c2", target_r=None, **OPEN), replace(BENCHMARK, open_space_r=NO_TARGET_R))

    def test_morning_only_no_target(self):
        self.compare(Settings("c3", target_r=None, session_hours=(7, 13), **OPEN),
                     replace(BENCHMARK, open_space_r=NO_TARGET_R, session_hours=(7, 13)))

    def test_level_breaks_only_no_target(self):
        self.compare(Settings("c4", entry=LEVEL, target_r=None, **OPEN), replace(LEVEL_TRIGGER, open_space_r=NO_TARGET_R))

    def test_no_direction_filter_and_no_session(self):
        self.compare(Settings("raw", use_direction=False, session_hours=None, **OPEN),
                     replace(BENCHMARK, readings=(), session=False))


class NoHindsight(unittest.TestCase):
    def test_trades_already_closed_never_change_when_more_bars_arrive(self):
        bars = random_walk(60, seed=11)
        full = run(bars, Settings("c2", target_r=None), BIG, compound=False).trades
        self.assertGreater(len(full), 20)
        for cut in (len(bars) // 3, len(bars) // 2, len(bars) - 500):
            part = run(bars[:cut], Settings("c2", target_r=None), BIG, compound=False).trades
            self.assertEqual(part, full[:len(part)])
            self.assertTrue(all(trade.closed_at <= bars[cut - 1].time for trade in part))

    def test_bars_out_of_order_are_refused(self):
        bars = random_walk(3, seed=1)
        bot = Bot(Settings("x"), BIG)
        bot.on_bar(bars[1])
        with self.assertRaises(ValueError):
            bot.on_bar(bars[0])


class TheRulesInForce(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bars = random_walk(120, seed=5)

    def test_every_trade_is_inside_the_session_and_flat_by_ten_to_five(self):
        for trade in run(self.bars, Settings("c1"), BIG, compound=False).trades:
            opened = datetime.fromtimestamp(trade.opened_at, timezone.utc).astimezone(NEW_YORK)
            closed = datetime.fromtimestamp(trade.closed_at, timezone.utc).astimezone(NEW_YORK)
            self.assertLess(opened.weekday(), 5)
            self.assertTrue(7 * 60 <= opened.hour * 60 + opened.minute <= 16 * 60 + 5, opened)
            self.assertEqual(opened.date(), closed.date())
            self.assertLessEqual(closed.hour * 60 + closed.minute, 16 * 60 + 50)

    def test_one_trade_at_a_time(self):
        trades = run(self.bars, Settings("c1"), BIG, compound=False).trades
        for earlier, later in zip(trades, trades[1:]):
            self.assertGreater(later.opened_at, earlier.closed_at - 1)

    def test_the_daily_limits_bind(self):
        limited = run(self.bars, Settings("c1"), BIG, compound=False)
        free = run(self.bars, Settings("c1", daily_limits=False), BIG, compound=False)
        self.assertLess(len(limited.trades), len(free.trades))
        blocked = sum(limited.skips[reason] for reason in ("max_trades_per_day", "daily_loss_limit", "losing_streak"))
        self.assertGreater(blocked, 0)
        per_day = {}
        for trade in limited.trades:
            per_day.setdefault(trading_day(trade.opened_at), []).append(trade.r)
        for results in per_day.values():
            self.assertLessEqual(len(results), 5)
            for index in range(len(results)):                   # no trade was opened after three straight losses
                self.assertFalse(index >= 3 and all(r < 0 for r in results[index - 3:index]), results)

    def test_a_wide_spread_keeps_it_out(self):
        wide = [bar._replace(spread=0.9) for bar in self.bars]
        bot = run(wide, Settings("c1"), BIG, compound=False)
        self.assertEqual(bot.trades, [])
        self.assertGreater(bot.skips["spread_too_wide"], 0)

    def test_nothing_is_traded_before_trade_from(self):
        cut = self.bars[len(self.bars) // 2].time
        bot = run(self.bars, Settings("c1"), BIG, trade_from=cut, compound=False)
        self.assertTrue(bot.trades)
        self.assertTrue(all(trade.opened_at >= cut for trade in bot.trades))
        self.assertGreater(bot.skips["warm_up"], 0)

    def test_risk_is_half_a_percent_and_the_balance_compounds(self):
        bot = run(self.bars, Settings("c1"), 10_000.0)
        self.assertTrue(bot.trades)
        self.assertAlmostEqual(bot.balance, 10_000.0 + sum(trade.money for trade in bot.trades))
        first = bot.trades[0]
        self.assertLessEqual(abs(first.entry - first.stop) * 100 * first.lots, 10_000.0 * 0.005 + 1e-6)

    def test_settings_must_make_sense(self):
        with self.assertRaises(ValueError):
            Settings("bad", entry="guess")
        with self.assertRaises(ValueError):
            Settings("bad", target_r=0)


if __name__ == "__main__":
    unittest.main()
