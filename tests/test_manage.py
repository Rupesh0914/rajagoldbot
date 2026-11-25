"""Lesson 7: managing the trade."""
import unittest
from datetime import datetime, timezone

from rajabot.candles import Bar, Candle
from rajabot.direction import BUY, SELL
from rajabot.levels import HIGH, LOW, Level
from rajabot.manage import (FLAT, HALVES, QUARTERS, SINGLE, STOP, TARGET, TIME_STOP, ExitStyle, Position, build_legs,
                            flat_time_after, target_price)
from rajabot.risk import Contract, Plan

T0 = int(datetime(2026, 11, 10, 16, 30, tzinfo=timezone.utc).timestamp())       # 11:30 New York


def buy_plan(lots=0.60, entry=3762.2, stop=3753.8):
    contract = Contract()
    risk = (entry - stop) * contract.money_per_dollar(lots)
    return Plan(BUY, entry, stop, lots, risk, 0.2 * contract.money_per_dollar(lots), 0.0, contract)


def sell_plan(lots=0.60, entry=3740.0, stop=3750.4):
    contract = Contract()
    risk = (stop - entry) * contract.money_per_dollar(lots)
    return Plan(SELL, entry, stop, lots, risk, 0.2 * contract.money_per_dollar(lots), 0.0, contract)


def bar(minute, open_, high, low, close, spread=0.2):
    return Bar(T0 + minute * 60, open_, high, low, close, spread)


def run(position, bars):
    for one in bars:
        position.on_bar(one)
    return position


TARGET_PRICE = 3774.8          # 12.60 above the entry: 1.5R


class Targets(unittest.TestCase):
    def test_a_touch_in_front_of_the_wall(self):
        self.assertAlmostEqual(target_price(buy_plan(), Level(3775.0, HIGH, 0, 0), 0.2), 3774.8)
        # a sell is closed at the ask: one spread in front of the floor, plus the spread itself
        self.assertAlmostEqual(target_price(sell_plan(), Level(3730.0, LOW, 0, 0), 0.2), 3730.4)

    def test_open_space_aims_at_a_multiple_of_the_risk(self):
        self.assertAlmostEqual(target_price(buy_plan(), None, 0.2), 3762.2 + 2 * 8.4)
        self.assertAlmostEqual(target_price(sell_plan(), None, 0.2, open_space_r=3.0), 3740.0 - 3 * 10.4)
        with self.assertRaises(ValueError):
            target_price(buy_plan(), None, 0.2, open_space_r=0)


class Legs(unittest.TestCase):
    def test_quarters_split_evenly_at_the_four_steps(self):
        legs = build_legs(buy_plan(lots=0.60), TARGET_PRICE, QUARTERS)
        self.assertEqual([leg.lots for leg in legs], [0.15, 0.15, 0.15, 0.15])
        for leg, expected in zip(legs, (3765.35, 3768.5, 3771.65, 3774.8)):
            self.assertAlmostEqual(leg.price, expected)

    def test_odd_size_goes_to_the_earliest_parts(self):
        self.assertEqual([leg.lots for leg in build_legs(buy_plan(lots=0.05), TARGET_PRICE, QUARTERS)],
                         [0.02, 0.01, 0.01, 0.01])
        self.assertEqual([leg.lots for leg in build_legs(buy_plan(lots=0.05), TARGET_PRICE, HALVES)], [0.03, 0.02])

    def test_too_little_size_uses_fewer_steps_as_the_sugarwood_bot_did(self):
        steps = lambda lots, style: [leg.step for leg in build_legs(buy_plan(lots=lots), TARGET_PRICE, style)]
        self.assertEqual(steps(0.03, QUARTERS), [0, 1, 3])
        self.assertEqual(steps(0.02, QUARTERS), [0, 2])
        self.assertEqual(steps(0.01, QUARTERS), [1])
        self.assertEqual(steps(0.01, HALVES), [1])
        self.assertEqual(steps(0.01, SINGLE), [0])

    def test_the_parts_always_add_up_to_the_whole(self):
        for lots in (0.01, 0.02, 0.03, 0.05, 0.07, 0.13, 0.60, 2.37):
            for style in (SINGLE, HALVES, QUARTERS):
                legs = build_legs(buy_plan(lots=lots), TARGET_PRICE, style)
                self.assertAlmostEqual(sum(leg.lots for leg in legs), lots)

    def test_a_target_on_the_wrong_side_is_refused(self):
        with self.assertRaises(ValueError):
            build_legs(buy_plan(), 3760.0, SINGLE)
        with self.assertRaises(ValueError):
            ExitStyle("bad", (0.5, 0.25, 1.0), True)
        with self.assertRaises(ValueError):
            ExitStyle("bad", (0.5,), True)


class SingleTarget(unittest.TestCase):
    def position(self):
        return Position(buy_plan(), TARGET_PRICE, SINGLE, T0)

    def test_reaching_the_target_makes_the_reward(self):
        position = run(self.position(), [bar(0, 3762, 3766, 3761, 3765), bar(1, 3765, 3775, 3764, 3774)])
        self.assertFalse(position.open)
        self.assertEqual(position.last_reason, TARGET)
        self.assertAlmostEqual(position.result_r, 1.5)

    def test_reaching_the_stop_loses_exactly_one_r(self):
        position = run(self.position(), [bar(0, 3762, 3763, 3753.8, 3754)])
        self.assertEqual(position.last_reason, STOP)
        self.assertAlmostEqual(position.result_r, -1.0)

    def test_a_bar_touching_both_counts_as_stopped(self):
        position = run(self.position(), [bar(0, 3762, 3776, 3753, 3770)])
        self.assertEqual(position.last_reason, STOP)

    def test_a_jump_past_the_stop_is_filled_at_the_worse_price(self):
        position = run(self.position(), [bar(0, 3750, 3751, 3749, 3750)])        # opens 3.80 below the stop
        self.assertAlmostEqual(position.fills[0].price, 3750.0)
        self.assertLess(position.result_r, -1.0)

    def test_the_stop_never_moves(self):
        position = run(self.position(), [bar(0, 3762, 3774, 3761, 3773)])
        self.assertEqual(position.stop, 3753.8)
        self.assertTrue(position.open)


class Halves(unittest.TestCase):
    def test_half_banked_then_stopped_at_break_even(self):
        position = Position(buy_plan(), TARGET_PRICE, HALVES, T0)
        position.on_bar(bar(0, 3762, 3769, 3761, 3768))                           # halfway is 3768.50
        self.assertEqual(position.banked, 1)
        self.assertAlmostEqual(position.stop, 3762.2)                             # break-even
        self.assertAlmostEqual(position.lots_open, 0.30)
        position.on_bar(bar(1, 3768, 3768.4, 3762, 3762.5))
        self.assertFalse(position.open)
        self.assertEqual(position.last_reason, STOP)
        self.assertAlmostEqual(position.result_r, 0.375)                          # half of 0.75R, the rest at zero

    def test_all_the_way(self):
        position = run(Position(buy_plan(), TARGET_PRICE, HALVES, T0), [bar(0, 3762, 3775, 3761, 3774)])
        self.assertAlmostEqual(position.result_r, 0.5 * 0.75 + 0.5 * 1.5)

    def test_a_stop_moved_up_applies_from_the_next_bar(self):
        position = Position(buy_plan(), TARGET_PRICE, HALVES, T0)
        position.on_bar(bar(0, 3762.5, 3769, 3762.1, 3768))        # low under the entry, but the old stop was far below
        self.assertTrue(position.open)


class Quarters(unittest.TestCase):
    def position(self, plan=None):
        return Position(plan or buy_plan(), TARGET_PRICE, QUARTERS, T0, stop_buffer=0.2)

    def test_the_stop_follows_one_step_behind(self):
        position = self.position()
        position.on_bar(bar(0, 3762, 3766, 3761, 3765.5))                         # step 1 at 3765.35
        self.assertAlmostEqual(position.stop, 3762.2)                             # break-even
        position.on_bar(bar(1, 3765.5, 3769, 3765, 3768.6))                       # step 2 at 3768.50
        self.assertAlmostEqual(position.stop, 3765.15)                            # just behind step 1
        position.on_bar(bar(2, 3768.6, 3772, 3768, 3771.7))                       # step 3 at 3771.65
        self.assertAlmostEqual(position.stop, 3768.3)                             # just behind step 2
        self.assertEqual(position.banked, 3)

    def test_two_steps_then_back_to_the_trailed_stop(self):
        position = run(self.position(), [bar(0, 3762, 3769.8, 3761, 3769.5), bar(1, 3769.5, 3769.6, 3765, 3765.1)])
        self.assertFalse(position.open)
        expected = 0.25 * (3.15 / 8.4) + 0.25 * (6.3 / 8.4) + 0.5 * (2.95 / 8.4)
        self.assertAlmostEqual(position.result_r, expected)
        self.assertEqual([fill.reason for fill in position.fills], [TARGET, TARGET, STOP, STOP])

    def test_all_four_steps(self):
        position = run(self.position(), [bar(0, 3762, 3775, 3761, 3774.9)])
        self.assertAlmostEqual(position.result_r, 1.5 * (0.25 + 0.5 + 0.75 + 1.0) / 4)
        self.assertEqual([fill.step for fill in position.fills], [0, 1, 2, 3])

    def test_closed_after_four_hours_with_nothing_banked(self):
        position = self.position()
        position.on_bar(bar(0, 3762, 3764, 3761, 3763))
        position.on_bar(bar(239, 3763, 3764, 3762, 3763.5))
        self.assertTrue(position.open)
        position.on_bar(bar(240, 3763.5, 3764, 3763, 3763.6))
        self.assertEqual(position.last_reason, TIME_STOP)
        self.assertAlmostEqual(position.fills[0].price, 3763.5)

    def test_no_time_stop_once_a_step_is_banked(self):
        position = self.position()
        position.on_bar(bar(0, 3762, 3766, 3761, 3765.5))
        position.on_bar(bar(240, 3765.5, 3766, 3765, 3765.6))
        self.assertTrue(position.open)

    def test_the_stop_never_moves_against_the_trade(self):
        position = self.position()
        position.stop = 3770.0                                    # already higher than any rule would put it
        position._move_stop_behind(0)
        self.assertEqual(position.stop, 3770.0)


class EndOfDay(unittest.TestCase):
    def test_everything_is_closed_at_ten_to_five_new_york(self):
        self.assertEqual(flat_time_after(T0), int(datetime(2026, 11, 10, 21, 50, tzinfo=timezone.utc).timestamp()))
        late = int(datetime(2026, 11, 10, 23, 0, tzinfo=timezone.utc).timestamp())            # 18:00 New York
        self.assertEqual(flat_time_after(late), int(datetime(2026, 11, 11, 21, 50, tzinfo=timezone.utc).timestamp()))
        summer = int(datetime(2026, 7, 14, 15, 0, tzinfo=timezone.utc).timestamp())
        self.assertEqual(flat_time_after(summer), int(datetime(2026, 7, 14, 20, 50, tzinfo=timezone.utc).timestamp()))

    def test_a_trade_still_open_is_closed_at_the_price_then(self):
        position = Position(buy_plan(), TARGET_PRICE, SINGLE, T0)
        position.on_bar(bar(0, 3762, 3764, 3761, 3763))
        minutes_to_flat = (position.flat_at - T0) // 60
        position.on_bar(bar(minutes_to_flat - 1, 3766, 3767, 3765, 3766))
        self.assertTrue(position.open)
        position.on_bar(bar(minutes_to_flat, 3766.4, 3767, 3766, 3766.5))
        self.assertEqual(position.last_reason, FLAT)
        self.assertAlmostEqual(position.result_r, (3766.4 - 3762.2) / 8.4)


class SellSide(unittest.TestCase):
    TARGET = 3730.4

    def test_a_sell_is_closed_at_the_ask(self):
        # the target is an ask price: the chart (bid) must reach 3730.20 with a 0.20 spread
        position = Position(sell_plan(), self.TARGET, SINGLE, T0)
        position.on_bar(bar(0, 3740, 3741, 3730.3, 3731))
        self.assertTrue(position.open)
        position.on_bar(bar(1, 3731, 3731.5, 3730.2, 3730.5))
        self.assertEqual(position.last_reason, TARGET)
        self.assertAlmostEqual(position.result_r, (3740.0 - 3730.4) / 10.4)

    def test_a_sell_is_stopped_when_the_ask_reaches_the_stop(self):
        position = Position(sell_plan(), self.TARGET, SINGLE, T0)
        position.on_bar(bar(0, 3740, 3750.1, 3739, 3749))                # ask high 3750.30: not yet
        self.assertTrue(position.open)
        position.on_bar(bar(1, 3749, 3750.2, 3748, 3750))                # ask high 3750.40: stopped
        self.assertEqual(position.last_reason, STOP)
        self.assertAlmostEqual(position.result_r, -1.0)

    def test_quarters_on_a_sell_trail_the_stop_downwards(self):
        position = Position(sell_plan(), self.TARGET, QUARTERS, T0, stop_buffer=0.2)
        position.on_bar(bar(0, 3740, 3740.5, 3737.3, 3737.5))            # step 1 at 3737.60 (ask)
        self.assertEqual(position.stop, 3740.0)
        position.on_bar(bar(1, 3737.5, 3738, 3734.9, 3735))              # step 2 at 3735.20
        self.assertAlmostEqual(position.stop, 3737.8)


class Money(unittest.TestCase):
    def test_commission_comes_off_the_result(self):
        contract = Contract(commission_per_lot_per_side=3.5)
        lots, distance = 0.60, 8.4
        commission = 2 * 3.5 * lots
        plan = Plan(BUY, 3762.2, 3753.8, lots, distance * 100 * lots + commission, 12.0, commission, contract)
        position = run(Position(plan, TARGET_PRICE, SINGLE, T0), [bar(0, 3762, 3763, 3753.8, 3754)])
        self.assertAlmostEqual(position.result_r, -1.0)
        self.assertAlmostEqual(position.money, -(distance * 100 * lots + commission))

    def test_a_closed_position_ignores_further_bars(self):
        position = run(Position(buy_plan(), TARGET_PRICE, SINGLE, T0), [bar(0, 3762, 3763, 3753.8, 3754)])
        self.assertEqual(position.on_bar(bar(1, 3754, 3800, 3700, 3760)), [])
        self.assertAlmostEqual(position.result_r, -1.0)


if __name__ == "__main__":
    unittest.main()
