"""Lesson 6: stop, costs and size."""
import unittest

from rajabot.candles import Candle
from rajabot.direction import BUY, SELL
from rajabot.examples import LESSON_5_ROOM
from rajabot.levels import HIGH, LOW, ZONE_SHARE, Level, LevelBook
from rajabot.risk import (SIZE_BELOW_MIN, STOP_TOO_TIGHT, STOP_TOO_WIDE, Contract, NoTrade, Plan, describe_plan,
                          entry_price, plan_trade, position_size, stop_price)
from rajabot.space import measure_room
from rajabot.trigger import Signal, Trigger

HALF_HOUR = 1800


def lesson_signal():
    trigger = Trigger(LevelBook(2))
    for candle in LESSON_5_ROOM:
        result = trigger.on_candle(candle)
        if isinstance(result, Signal):
            return result, trigger.book
    raise AssertionError("no signal")


def sell_signal(open_=3749.0, high=3750.0, low=3739.0, close=3740.0):
    candle = Candle(0, open_, high, low, close, HALF_HOUR)
    return Signal(SELL, Level(3742.0, LOW, 0, 0), candle, candle.body_share, 1)


class EntryAndStop(unittest.TestCase):
    def test_a_buy_pays_the_spread_on_the_way_in_and_a_sell_does_not(self):
        self.assertAlmostEqual(entry_price(BUY, 3762.0, 0.2), 3762.2)
        self.assertEqual(entry_price(SELL, 3762.0, 0.2), 3762.0)

    def test_a_buy_stop_sits_one_spread_below_the_candles_low(self):
        candle = Candle(0, 3755.0, 3763.0, 3754.0, 3762.0, HALF_HOUR)
        self.assertAlmostEqual(stop_price(BUY, candle, 0.2), 3753.8)
        self.assertAlmostEqual(stop_price(BUY, candle, 0.2, buffer_spreads=0), 3754.0)

    def test_a_sell_stop_sits_two_spreads_above_the_candles_high(self):
        # one spread of buffer, and one more because a sell is closed at the ask
        candle = Candle(0, 3749.0, 3750.0, 3739.0, 3740.0, HALF_HOUR)
        self.assertAlmostEqual(stop_price(SELL, candle, 0.2), 3750.4)

    def test_an_unknown_side_is_refused(self):
        with self.assertRaises(ValueError):
            entry_price("hold", 1.0, 0.1)


class Size(unittest.TestCase):
    def test_the_lesson_arithmetic(self):
        # 50 of risk, 8.40 away, 100 ounces a lot: 0.0595 lots, rounded DOWN to 0.05
        self.assertEqual(position_size(50.0, 8.4), 0.05)
        self.assertEqual(position_size(84.0, 8.4), 0.10)          # exactly a round number of lots

    def test_it_never_rounds_up(self):
        for risk in (10.0, 33.3, 77.7, 250.0, 999.0):
            for distance in (2.5, 8.4, 13.37):
                lots = position_size(risk, distance)
                self.assertLessEqual(lots * distance * 100, risk + 1e-9)
                self.assertGreater((lots + 0.01) * distance * 100, risk - 1e-9)

    def test_too_little_money_for_the_smallest_lot_is_zero(self):
        self.assertEqual(position_size(5.0, 8.4), 0.0)            # 0.01 lots would lose 8.40
        self.assertEqual(position_size(8.4, 8.4), 0.01)
        self.assertEqual(position_size(50.0, 0.0), 0.0)
        self.assertEqual(position_size(0.0, 8.4), 0.0)

    def test_an_account_in_another_currency_trades_smaller(self):
        cad = Contract(usd_to_account=1.40)                       # one US dollar is 1.40 Canadian
        self.assertEqual(position_size(50.0, 8.4, cad), 0.04)     # not 0.05: each dollar of gold costs more
        self.assertAlmostEqual(cad.money_per_dollar(0.04), 5.6)

    def test_commission_counts_as_part_of_the_risk(self):
        paid = Contract(commission_per_lot_per_side=3.5)          # 7 a lot, in and out
        self.assertEqual(position_size(50.0, 8.4, paid), 0.05)    # 0.05 * (840 + 7) = 42.35
        self.assertEqual(position_size(42.0, 8.4, paid), 0.04)    # 0.05 lots would now cost 42.35

    def test_the_brokers_largest_trade_is_respected(self):
        self.assertEqual(position_size(10_000_000.0, 1.0, Contract(volume_max=50.0)), 50.0)


class ThePlan(unittest.TestCase):
    def setUp(self):
        self.signal, self.book = lesson_signal()
        self.average = self.book.reach / ZONE_SHARE

    def plan(self, **changes):
        settings = dict(bid=3762.0, spread=0.2, balance=10000.0, average_candle=self.average)
        settings.update(changes)
        return plan_trade(self.signal, **settings)

    def test_the_lesson_example(self):
        plan = self.plan()
        self.assertIsInstance(plan, Plan)
        self.assertEqual((plan.side, plan.lots), (BUY, 0.05))
        self.assertAlmostEqual(plan.entry, 3762.2)
        self.assertAlmostEqual(plan.stop, 3753.8)
        self.assertAlmostEqual(plan.distance, 8.4)
        self.assertAlmostEqual(plan.risk_money, 42.0)             # under the 50 allowed, never over
        self.assertAlmostEqual(plan.spread_money, 1.0)
        self.assertEqual(plan.commission_money, 0.0)

    def test_results_in_r(self):
        plan = self.plan()
        self.assertAlmostEqual(plan.r_multiple(plan.stop), -1.0)                  # stopped out
        self.assertAlmostEqual(plan.r_multiple(plan.entry), 0.0)
        self.assertAlmostEqual(plan.r_multiple(plan.entry + 2 * plan.distance), 2.0)
        self.assertAlmostEqual(plan.r_multiple(3762.0), -0.2 / 8.4)               # closed at once: lost the spread

    def test_the_risk_never_exceeds_the_share_chosen(self):
        for balance in (800.0, 2500.0, 10000.0, 73000.0):
            for share in (0.0025, 0.005, 0.01, 0.02):
                plan = self.plan(balance=balance, risk_share=share)
                if isinstance(plan, Plan):
                    self.assertLessEqual(plan.risk_money, balance * share + 1e-9)

    def test_a_canadian_dollar_account(self):
        plan = self.plan(contract=Contract(usd_to_account=1.40))
        self.assertEqual(plan.lots, 0.04)
        self.assertAlmostEqual(plan.risk_money, 47.04)

    def test_commission_is_inside_the_risk_and_the_r(self):
        plan = self.plan(contract=Contract(commission_per_lot_per_side=3.5))
        self.assertEqual(plan.lots, 0.05)
        self.assertAlmostEqual(plan.commission_money, 0.35)
        self.assertAlmostEqual(plan.risk_money, 42.35)
        self.assertAlmostEqual(plan.r_multiple(plan.stop), -1.0)

    def test_a_small_account_cannot_take_the_trade(self):
        result = self.plan(balance=500.0)
        self.assertIsInstance(result, NoTrade)
        self.assertEqual(result.reason, SIZE_BELOW_MIN)

    def test_a_stop_too_far_for_the_market_is_refused(self):
        result = self.plan(average_candle=2.0)                    # 8.40 is more than 3 candles of 2.00
        self.assertEqual(result.reason, STOP_TOO_WIDE)
        self.assertIsInstance(self.plan(average_candle=2.8), Plan)       # exactly 3 candles: allowed

    def test_a_stop_so_close_the_spread_eats_it_is_refused(self):
        result = self.plan(spread=2.0)                            # distance 12.0 exactly 6 spreads: allowed
        self.assertIsInstance(result, Plan)
        self.assertEqual(self.plan(spread=2.5).reason, STOP_TOO_TIGHT)   # 13.0 away, under 15.0

    def test_a_sell_is_the_mirror(self):
        plan = plan_trade(sell_signal(), bid=3740.0, spread=0.2, balance=10000.0, average_candle=7.0)
        self.assertEqual(plan.side, SELL)
        self.assertEqual(plan.entry, 3740.0)
        self.assertAlmostEqual(plan.stop, 3750.4)
        self.assertAlmostEqual(plan.distance, 10.4)
        self.assertEqual(plan.lots, 0.04)                         # 50 / 1040 = 0.048
        self.assertAlmostEqual(plan.r_multiple(plan.stop), -1.0)
        self.assertAlmostEqual(plan.r_multiple(3729.6), 1.0)

    def test_bad_inputs_are_refused(self):
        for changes in (dict(risk_share=0), dict(risk_share=0.06), dict(spread=-0.1), dict(balance=0),
                        dict(average_candle=0)):
            with self.assertRaises(ValueError):
                self.plan(**changes)

    def test_room_can_be_measured_with_the_real_entry_and_stop(self):
        plan = self.plan()
        room = measure_room(self.signal, self.book, plan.entry, plan.distance)
        self.assertAlmostEqual(room.distance, 12.8)               # 3775 - 3762.20
        self.assertAlmostEqual(room.ratio, 12.8 / 8.4)

    def test_the_description(self):
        text = describe_plan(self.plan(), 10000.0)
        self.assertIn("BUY 0.05 lots.", text)
        self.assertIn("If stopped out: -42.00, which is 0.42% of the account. That is 1R.", text)
        self.assertTrue(describe_plan(self.plan(balance=500.0), 500.0).startswith("NO TRADE: size below min"))


if __name__ == "__main__":
    unittest.main()
