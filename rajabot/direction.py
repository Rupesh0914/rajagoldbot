"""Lesson 3 in code: direction, read from closed 4-hour candles.

The rule: compare the close of the last closed 4-hour candle with the close `lookback` candles
earlier. Higher means up, lower means down. With the default of 6 candles that asks one plain
question: is gold higher or lower than it was 24 trading hours ago?

  * up:   the bot may look for buys only
  * down: the bot may look for sells only
  * flat or unknown: no trades

This is our exact stand-in for something Raja Banks does by eye. He gives no formula. Whether
this filter helps at all is settled by the honest test in lesson 9.

This module answers "which way?". It places no order.
"""
from __future__ import annotations

from typing import Sequence

from .candles import Candle

UP, DOWN, FLAT, UNKNOWN = "up", "down", "flat", "unknown"
BUY, SELL = "buy", "sell"
DEFAULT_LOOKBACK = 6        # 4-hour candles: 24 hours of trading


def direction_of_closes(closes: Sequence[float], lookback: int = DEFAULT_LOOKBACK) -> str:
    """Direction from closing prices in time order, oldest first. All must be CLOSED candles."""
    if not isinstance(lookback, int) or lookback < 1:
        raise ValueError("lookback must be a whole number of candles, 1 or more")
    if len(closes) < lookback + 1:
        return UNKNOWN
    last, earlier = closes[-1], closes[-1 - lookback]
    if last > earlier:
        return UP
    if last < earlier:
        return DOWN
    return FLAT


def direction(four_hour_candles: Sequence[Candle], lookback: int = DEFAULT_LOOKBACK) -> str:
    """Direction from closed 4-hour candles, oldest first.

    Pass only candles that have closed: build them with `build_four_hour_candles(bars, as_of=now)`.
    """
    return direction_of_closes([candle.close for candle in four_hour_candles], lookback)


def allows(current: str, side: str) -> bool:
    """May the bot take this side? Buys need an up direction, sells a down direction."""
    if side not in (BUY, SELL):
        raise ValueError("side must be 'buy' or 'sell'")
    return (current == UP and side == BUY) or (current == DOWN and side == SELL)


def explain(closes: Sequence[float], lookback: int = DEFAULT_LOOKBACK) -> str:
    """One plain sentence about the direction, used in the lesson's examples."""
    current = direction_of_closes(closes, lookback)
    if current == UNKNOWN:
        return "unknown: need %d closed candles, have %d. No trades." % (lookback + 1, len(closes))
    last, earlier = closes[-1], closes[-1 - lookback]
    if current == FLAT:
        return "flat: the last close %.2f equals the close %d candles earlier. No trades." % (last, lookback)
    word, side = ("above", "buys") if current == UP else ("below", "sells")
    return "%s: the last close %.2f is %s %.2f, the close %d candles earlier. Look for %s only." % (
        current, last, word, earlier, lookback, side)
