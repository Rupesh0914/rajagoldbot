"""Lesson 8: when not to trade."""
import os
import tempfile
import unittest
from datetime import date, datetime

from rajabot.candles import NEW_YORK, Candle
from rajabot.direction import BUY, SELL
from rajabot.filters import (DAILY_LOSS, LOSING_STREAK, MAX_TRADES, NEWS, OUTSIDE_SESSION, REJECTION_WICK, SIDEWAYS,
                             SPREAD_TOO_WIDE, DayGuard, Gate, NewsCalendar, in_session, is_sideways, jobs_report_time,
                             progress, rejection_wick, trading_day, wick_against)

HALF_HOUR = 1800


def ny(year, month, day, hour=0, minute=0) -> int:
    return int(datetime(year, month, day, hour, minute, tzinfo=NEW_YORK).timestamp())


def closes_to_candles(closes):
    return [Candle(i * HALF_HOUR, c, c + 0.5, c - 0.5, c, HALF_HOUR) for i, c in enumerate(closes)]


class Hours(unittest.TestCase):
    def test_seven_to_four_new_york_on_weekdays_summer_and_winter(self):
        for month in (1, 7):                                    # winter and summer clocks
            tuesday = 13 if month == 1 else 14
            self.assertFalse(in_session(ny(2026, month, tuesday, 6, 59)))
            self.assertTrue(in_session(ny(2026, month, tuesday, 7, 0)))
            self.assertTrue(in_session(ny(2026, month, tuesday, 16, 0)))
            self.assertFalse(in_session(ny(2026, month, tuesday, 16, 1)))
        self.assertFalse(in_session(ny(2026, 12, 5, 10, 0)))    # Saturday
        self.assertFalse(in_session(ny(2026, 12, 6, 10, 0)))    # Sunday

    def test_other_hours_can_be_chosen(self):
        self.assertFalse(in_session(ny(2026, 12, 1, 14, 0), (7, 13)))
        self.assertTrue(in_session(ny(2026, 12, 1, 13, 0), (7, 13)))

    def test_the_trading_day_turns_over_at_five_pm_new_york(self):
        self.assertEqual(trading_day(ny(2026, 12, 1, 16, 59)), date(2026, 12, 1))
        self.assertEqual(trading_day(ny(2026, 12, 1, 17, 0)), date(2026, 12, 2))
        self.assertEqual(trading_day(ny(2026, 7, 14, 17, 0)), date(2026, 7, 15))     # same in summer


class News(unittest.TestCase):
    def test_half_an_hour_either_side(self):
        calendar = NewsCalendar()
        calendar.add(ny(2026, 12, 4, 8, 30), "US jobs report")
        self.assertIsNone(calendar.blocked(ny(2026, 12, 4, 7, 59)))
        self.assertEqual(calendar.blocked(ny(2026, 12, 4, 8, 0)), "US jobs report")
        self.assertEqual(calendar.blocked(ny(2026, 12, 4, 9, 0)), "US jobs report")
        self.assertIsNone(calendar.blocked(ny(2026, 12, 4, 9, 1)))

    def test_the_window_can_be_changed(self):
        calendar = NewsCalendar(before_minutes=5, after_minutes=60)
        calendar.add(ny(2026, 12, 4, 8, 30), "jobs")
        self.assertIsNone(calendar.blocked(ny(2026, 12, 4, 8, 24)))
        self.assertEqual(calendar.blocked(ny(2026, 12, 4, 9, 30)), "jobs")

    def test_the_jobs_report_is_the_first_friday_at_half_past_eight(self):
        self.assertEqual(jobs_report_time(2026, 12), ny(2026, 12, 4, 8, 30))
        self.assertEqual(jobs_report_time(2026, 5), ny(2026, 5, 1, 8, 30))        # the 1st is a Friday
        self.assertEqual(jobs_report_time(2026, 8), ny(2026, 8, 7, 8, 30))        # the 1st is a Saturday

    def test_a_calendar_file_in_new_york_time(self):
        handle = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        handle.write("when,what\n# a comment\n2026-12-04 08:30,US jobs report\n\n2026-12-16 14:00,Fed decision\n2026-07-02 08:30\n")
        handle.close()
        self.addCleanup(os.unlink, handle.name)
        calendar = NewsCalendar.from_csv(handle.name)
        self.assertEqual(calendar.events, [(ny(2026, 7, 2, 8, 30), "news"), (ny(2026, 12, 4, 8, 30), "US jobs report"),
                                           (ny(2026, 12, 16, 14, 0), "Fed decision")])


class Sideways(unittest.TestCase):
    def test_straight_moves_score_one_and_round_trips_score_zero(self):
        self.assertAlmostEqual(progress(closes_to_candles([3750 + 2 * i for i in range(13)])), 1.0)
        self.assertAlmostEqual(progress(closes_to_candles([3750 - 2 * i for i in range(13)])), 1.0)
        zigzag = [3750, 3756] * 6 + [3750]
        self.assertAlmostEqual(progress(closes_to_candles(zigzag)), 0.0)

    def test_the_lesson_example(self):
        candles = closes_to_candles([3750, 3756, 3751, 3757, 3750, 3755, 3751])
        self.assertAlmostEqual(progress(candles, 6), 1 / 33)
        self.assertTrue(is_sideways(candles, 6))
        self.assertFalse(is_sideways(closes_to_candles([3750, 3754, 3758, 3762, 3766]), 4))

    def test_only_the_last_candles_count_and_too_few_is_not_sideways(self):
        chop_then_run = [3750, 3756] * 6 + [3750 + 3 * i for i in range(13)]
        self.assertAlmostEqual(progress(closes_to_candles(chop_then_run)), 1.0)
        self.assertIsNone(progress(closes_to_candles([3750, 3751, 3752])))
        self.assertFalse(is_sideways(closes_to_candles([3750, 3751, 3752])))
        self.assertIsNone(progress(closes_to_candles([3750] * 13)))                 # no movement at all
        with self.assertRaises(ValueError):
            progress([], 1)

    def test_the_answer_does_not_change_when_later_candles_arrive(self):
        closes = [3750 + ((i * 7) % 11) - (i % 5) * 1.3 for i in range(60)]
        candles = closes_to_candles(closes)
        for cut in (13, 20, 41):
            self.assertEqual(progress(candles[:cut]), progress(closes_to_candles(closes[:cut])))


class RejectionWick(unittest.TestCase):
    def test_a_long_wick_on_one_side(self):
        pushed_back_from_above = Candle(0, 3750.0, 3762.0, 3749.0, 3752.0, 14400)     # body 2, upper wick 10
        pushed_back_from_below = Candle(0, 3752.0, 3753.0, 3740.0, 3750.0, 14400)     # body 2, lower wick 10
        ordinary = Candle(0, 3750.0, 3759.0, 3749.0, 3758.0, 14400)                   # body 8, wicks 1
        self.assertEqual(rejection_wick(pushed_back_from_above), "upper")
        self.assertEqual(rejection_wick(pushed_back_from_below), "lower")
        self.assertIsNone(rejection_wick(ordinary))
        self.assertIsNone(rejection_wick(Candle(0, 3750.0, 3750.0, 3750.0, 3750.0, 14400)))

    def test_it_must_be_twice_the_body_and_the_longer_wick(self):
        self.assertIsNone(rejection_wick(Candle(0, 3750.0, 3757.9, 3749.0, 3754.0, 14400)))      # upper 3.9, body 4
        self.assertEqual(rejection_wick(Candle(0, 3750.0, 3762.0, 3749.0, 3754.0, 14400)), "upper")   # upper 8, body 4
        self.assertEqual(rejection_wick(Candle(0, 3750.0, 3760.0, 3740.0, 3750.5, 14400)), "lower")   # lower 10 beats upper 9.5
        self.assertIsNone(rejection_wick(Candle(0, 3750.0, 3760.0, 3740.0, 3750.0, 14400)))       # two equal wicks: neither side
        self.assertEqual(rejection_wick(Candle(0, 3750.0, 3760.0, 3741.0, 3750.0, 14400)), "upper")   # closed where it opened

    def test_which_trades_it_warns_against(self):
        above = Candle(0, 3750.0, 3762.0, 3749.0, 3752.0, 14400)
        self.assertTrue(wick_against(BUY, above))                # buying into prices that were refused
        self.assertFalse(wick_against(SELL, above))
        self.assertFalse(wick_against(BUY, None))
        with self.assertRaises(ValueError):
            wick_against("hold", above)


class DailyLimits(unittest.TestCase):
    def test_three_losses_in_a_row_stop_the_day(self):
        guard = DayGuard(max_loss_r=10.0)
        for hour in (8, 9, 10):
            self.assertIsNone(guard.blocked(ny(2026, 12, 2, hour)))
            guard.opened(ny(2026, 12, 2, hour))
            guard.closed(ny(2026, 12, 2, hour, 30), -0.5)
        self.assertEqual(guard.blocked(ny(2026, 12, 2, 11)), LOSING_STREAK)

    def test_a_winner_breaks_the_run(self):
        guard = DayGuard(max_loss_r=10.0)
        for result in (-1.0, -1.0, 0.4, -1.0):
            guard.opened(ny(2026, 12, 2, 9))
            guard.closed(ny(2026, 12, 2, 9, 30), result)
        self.assertIsNone(guard.blocked(ny(2026, 12, 2, 11)))

    def test_losing_three_r_stops_the_day(self):
        guard = DayGuard(max_losing_streak=99)
        for result in (-1.0, 0.5, -1.0, -1.5):
            guard.opened(ny(2026, 12, 2, 9))
            guard.closed(ny(2026, 12, 2, 9, 30), result)
        self.assertAlmostEqual(guard.total_r, -3.0)
        self.assertEqual(guard.blocked(ny(2026, 12, 2, 11)), DAILY_LOSS)

    def test_five_trades_is_the_most_in_a_day(self):
        guard = DayGuard()
        for index in range(5):
            self.assertIsNone(guard.blocked(ny(2026, 12, 2, 8 + index)))
            guard.opened(ny(2026, 12, 2, 8 + index))
            guard.closed(ny(2026, 12, 2, 8 + index, 30), 1.0)
        self.assertEqual(guard.blocked(ny(2026, 12, 2, 14)), MAX_TRADES)

    def test_everything_resets_at_the_new_trading_day(self):
        guard = DayGuard()
        for hour in (8, 9, 10):
            guard.opened(ny(2026, 12, 2, hour))
            guard.closed(ny(2026, 12, 2, hour, 30), -1.0)
        self.assertIsNotNone(guard.blocked(ny(2026, 12, 2, 16, 59)))
        self.assertIsNone(guard.blocked(ny(2026, 12, 2, 17, 0)))          # the next trading day has begun
        self.assertEqual((guard.trades, guard.total_r, guard.streak), (0, 0.0, 0))

    def test_limits_must_be_positive(self):
        for bad in (dict(max_trades=0), dict(max_loss_r=0), dict(max_losing_streak=0)):
            with self.assertRaises(ValueError):
                DayGuard(**bad)


class TheGate(unittest.TestCase):
    GOOD = ny(2026, 12, 1, 9, 30)                                # a Tuesday morning

    def test_a_clean_moment_passes(self):
        self.assertIsNone(Gate().check(self.GOOD, BUY, 0.15))

    def test_each_rule_on_its_own(self):
        self.assertEqual(Gate().check(ny(2026, 12, 1, 5, 0), BUY, 0.15), OUTSIDE_SESSION)
        self.assertEqual(Gate().check(self.GOOD, BUY, 0.51), SPREAD_TOO_WIDE)
        self.assertIsNone(Gate().check(self.GOOD, BUY, 0.50))
        news = NewsCalendar([(self.GOOD + 600, "CPI")])
        self.assertEqual(Gate(news=news).check(self.GOOD, BUY, 0.15), NEWS)
        chop = closes_to_candles([3750, 3756] * 6 + [3750])
        self.assertEqual(Gate(avoid_sideways=True).check(self.GOOD, BUY, 0.15, chop), SIDEWAYS)
        wick = Candle(0, 3750.0, 3762.0, 3749.0, 3752.0, 14400)
        self.assertEqual(Gate(avoid_rejection_wick=True).check(self.GOOD, BUY, 0.15, last_four_hour=wick), REJECTION_WICK)
        self.assertIsNone(Gate(avoid_rejection_wick=True).check(self.GOOD, SELL, 0.15, last_four_hour=wick))

    def test_sideways_and_wick_rules_are_off_unless_switched_on(self):
        chop = closes_to_candles([3750, 3756] * 6 + [3750])
        wick = Candle(0, 3750.0, 3762.0, 3749.0, 3752.0, 14400)
        self.assertIsNone(Gate().check(self.GOOD, BUY, 0.15, chop, wick))

    def test_rules_can_be_switched_off(self):
        gate = Gate(session_hours=None, max_spread=None)
        self.assertIsNone(gate.check(ny(2026, 12, 5, 3, 0), BUY, 5.0))

    def test_the_first_rule_that_says_no_is_the_reason(self):
        guard = DayGuard()
        for hour in (8, 9, 10):
            guard.opened(ny(2026, 12, 1, hour))
            guard.closed(ny(2026, 12, 1, hour, 30), -1.0)
        news = NewsCalendar([(ny(2026, 12, 1, 11, 0), "CPI")])
        gate = Gate(news=news, guard=guard)
        self.assertEqual(gate.check(ny(2026, 12, 1, 16, 30), BUY, 0.9), OUTSIDE_SESSION)
        self.assertEqual(gate.check(ny(2026, 12, 1, 11, 0), BUY, 0.9), SPREAD_TOO_WIDE)
        self.assertEqual(gate.check(ny(2026, 12, 1, 11, 0), BUY, 0.15), NEWS)
        self.assertEqual(gate.check(ny(2026, 12, 1, 12, 0), BUY, 0.15), DAILY_LOSS)


if __name__ == "__main__":
    unittest.main()
