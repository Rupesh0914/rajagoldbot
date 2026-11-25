"""Lesson 6 in code: the stop loss, costs, and how much to risk.

For a signal this works out the three numbers every trade needs before it is placed:

  * the entry: a buy is filled at the ask (the chart price plus the spread), a sell at the bid;
  * the stop: just beyond the far end of the signal candle, where the break has failed;
  * the size: how many lots, so that being stopped out costs a small fixed share of the account.

It refuses a trade whose stop is too far (too wide for the market), too close (the spread would
eat it), or whose size would be below the smallest the broker allows.

Prices are gold prices in US dollars. Money is in the account's own currency. This module does
arithmetic only. It places no order.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from .candles import Candle
from .direction import BUY, SELL
from .trigger import Signal

STOP_TOO_WIDE = "stop_too_wide"             # further than the market's recent candles justify
STOP_TOO_TIGHT = "stop_too_tight"           # so close that the spread is a big part of the risk
SIZE_BELOW_MIN = "size_below_min"           # even the smallest lot would risk more than allowed

DEFAULT_RISK_SHARE = 0.005                  # risk 0.5% of the account on one trade
DEFAULT_BUFFER_SPREADS = 1.0                # the stop sits one spread beyond the candle's far end
DEFAULT_MAX_STOP_CANDLES = 3.0              # a stop further than 3 average candles is too wide
DEFAULT_MIN_STOP_SPREADS = 6.0              # a stop closer than 6 spreads is too tight


@dataclass(frozen=True)
class Contract:
    """What the broker says about the symbol and the account. Lesson 10 reads these from MT5."""
    contract_size: float = 100.0            # ounces of gold in one lot
    volume_min: float = 0.01                # smallest trade, in lots
    volume_step: float = 0.01               # lots go up in steps of this
    volume_max: float = 100.0
    commission_per_lot_per_side: float = 0.0    # in the account's currency
    usd_to_account: float = 1.0             # what one US dollar is worth in the account's currency

    def money_per_dollar(self, lots: float) -> float:
        """Account money gained or lost when gold moves one dollar, for this many lots."""
        return lots * self.contract_size * self.usd_to_account


@dataclass(frozen=True)
class Plan:
    side: str
    entry: float            # the price paid (buy: ask) or received (sell: bid)
    stop: float             # the price at which the trade is closed for a loss
    lots: float
    risk_money: float       # what being stopped out costs, commission included: this is "1R"
    spread_money: float     # the part of that which is the spread paid on the way in
    commission_money: float  # both sides
    contract: Contract

    @property
    def distance(self) -> float:
        """Entry to stop, in dollars of gold price."""
        return abs(self.entry - self.stop)

    def r_multiple(self, exit_price: float) -> float:
        """The result of closing at `exit_price`, in units of the risk taken (R).

        `exit_price` is the price actually received (buy) or paid (sell). Stopped out exactly at
        the stop is -1R.
        """
        moved = exit_price - self.entry if self.side == BUY else self.entry - exit_price
        money = moved * self.contract.money_per_dollar(self.lots) - self.commission_money
        return money / self.risk_money


@dataclass(frozen=True)
class NoTrade:
    reason: str
    detail: str = ""


def entry_price(side: str, bid: float, spread: float) -> float:
    """A buy pays the ask, which is the chart (bid) price plus the spread. A sell gets the bid."""
    _check_side(side)
    return bid + spread if side == BUY else bid


def stop_price(side: str, candle: Candle, spread: float, buffer_spreads: float = DEFAULT_BUFFER_SPREADS) -> float:
    """Where the stop goes: just beyond the far end of the signal candle.

    Buy: below the candle's low by the buffer. A buy is closed by selling at the bid, which is
    the price the chart shows.
    Sell: above the candle's high by the buffer, plus one more spread: a sell is closed by buying
    at the ask, which sits a spread above the chart. The stop is given as that ask price.
    """
    _check_side(side)
    buffer = buffer_spreads * spread
    return candle.low - buffer if side == BUY else candle.high + buffer + spread


def position_size(risk_money: float, distance: float, contract: Contract = Contract()) -> float:
    """Lots to trade so that losing `distance` dollars of gold price costs about `risk_money`.

    Always rounded DOWN to the broker's step, so the real risk is never above the target. 0 when
    even the smallest allowed trade would risk more.
    """
    if distance <= 0 or risk_money <= 0:
        return 0.0
    per_lot = distance * contract.contract_size * contract.usd_to_account + 2 * contract.commission_per_lot_per_side
    steps = math.floor(risk_money / per_lot / contract.volume_step + 1e-9)
    lots = min(steps * contract.volume_step, contract.volume_max)
    return round(lots, 8) if lots >= contract.volume_min - 1e-12 else 0.0


def plan_trade(signal: Signal, bid: float, spread: float, balance: float, average_candle: float,
               contract: Contract = Contract(), risk_share: float = DEFAULT_RISK_SHARE,
               buffer_spreads: float = DEFAULT_BUFFER_SPREADS,
               max_stop_candles: float = DEFAULT_MAX_STOP_CANDLES,
               min_stop_spreads: float = DEFAULT_MIN_STOP_SPREADS) -> Plan | NoTrade:
    """Entry, stop and size for a signal, or the reason there is no trade.

    `bid` and `spread` are those of the first minute after the signal candle closed.
    `average_candle` is the average height of recent 30-minute candles (what a normal move is).
    """
    if not 0 < risk_share <= 0.05:
        raise ValueError("risk_share is a share of the account: above 0, at most 0.05 (5%)")
    if spread < 0 or balance <= 0 or average_candle <= 0:
        raise ValueError("spread cannot be negative; balance and average_candle must be positive")
    side = signal.side
    entry = entry_price(side, bid, spread)
    stop = stop_price(side, signal.candle, spread, buffer_spreads)
    distance = entry - stop if side == BUY else stop - entry

    if distance > max_stop_candles * average_candle:
        return NoTrade(STOP_TOO_WIDE, "stop is %.2f away, more than %.1f average candles (%.2f)" % (
            distance, max_stop_candles, max_stop_candles * average_candle))
    if distance <= 0 or distance < min_stop_spreads * spread:
        return NoTrade(STOP_TOO_TIGHT, "stop is %.2f away, under %.0f spreads (%.2f)" % (
            distance, min_stop_spreads, min_stop_spreads * spread))

    target_risk = balance * risk_share
    lots = position_size(target_risk, distance, contract)
    if lots <= 0:
        smallest = distance * contract.money_per_dollar(contract.volume_min) + 2 * contract.commission_per_lot_per_side * contract.volume_min
        return NoTrade(SIZE_BELOW_MIN, "the smallest trade (%.2f lots) would risk %.2f, above the %.2f allowed" % (
            contract.volume_min, smallest, target_risk))
    commission = 2 * contract.commission_per_lot_per_side * lots
    risk_money = distance * contract.money_per_dollar(lots) + commission
    return Plan(side, entry, stop, lots, risk_money, spread * contract.money_per_dollar(lots), commission, contract)


def describe_plan(plan: Plan | NoTrade, balance: float, currency: str = "") -> str:
    """Plain lines about a plan, used in the lesson's examples."""
    if isinstance(plan, NoTrade):
        return "NO TRADE: %s (%s)." % (plan.reason.replace("_", " "), plan.detail)
    unit = (" " + currency) if currency else ""
    return "\n".join([
        "%s %.2f lots." % (plan.side.upper(), plan.lots),
        "Entry %.2f. Stop %.2f. Distance %.2f." % (plan.entry, plan.stop, plan.distance),
        "If stopped out: -%.2f%s, which is %.2f%% of the account. That is 1R." % (
            plan.risk_money, unit, 100 * plan.risk_money / balance),
        "Of that, the spread is %.2f%s and commission %.2f%s." % (plan.spread_money, unit, plan.commission_money, unit),
        "Each dollar gold moves is worth %.2f%s." % (plan.contract.money_per_dollar(plan.lots), unit),
    ])


def _check_side(side: str) -> None:
    if side not in (BUY, SELL):
        raise ValueError("side must be 'buy' or 'sell'")
