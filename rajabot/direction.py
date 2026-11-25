"""Lesson 3 in code: direction, read from closed 4-hour candles.

The rule: compare the close of the last closed 4-hour candle with the close `lookback` candles
earlier. Higher means up, lower means down. With the default of 6 candles that asks one plain
question: is gold higher or lower than it was one trading day ago?

  * up:   the bot may look for buys only
  * down: the bot may look for sells only
  * flat or unknown: no trades

This is our exact stand-in for something Raja Banks does by eye. He gives no formula. Whether
this filter helps at all is settled by the honest test in lesson 9.

Two more readings bring the bot closer to what an eye sees:

  * structure: are the peaks and dips of the 4-hour chart stepping up, or stepping down?
  * the daily background: is gold higher or lower than a trading week ago?

`combine` turns several readings into one decision: trade only when they all agree.

This module answers "which way?". It places no order.
"""
from __future__ import annotations

from typing import Sequence

from .candles import Candle
from .levels import HIGH, LOW, find_swings

UP, DOWN, FLAT, MIXED, UNKNOWN = "up", "down", "flat", "mixed", "unknown"
BUY, SELL = "buy", "sell"
DEFAULT_LOOKBACK = 6        # 4-hour candles: one trading day
DAILY_LOOKBACK = 5          # daily candles: one trading week
STRUCTURE_STRENGTH = 2      # candles each side for a peak or dip on the 4-hour chart


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


def daily_direction(daily_candles: Sequence[Candle], lookback: int = DAILY_LOOKBACK) -> str:
    """The background: the last closed daily close against the close a trading week earlier."""
    return direction_of_closes([candle.close for candle in daily_candles], lookback)


def structure(candles: Sequence[Candle], strength: int = STRUCTURE_STRENGTH) -> str:
    """Are the peaks and dips stepping up or down? Pass closed candles, oldest first.

    Takes the last two confirmed swing highs (peaks) and the last two confirmed swing lows (dips):
      * up:    the newer peak is higher AND the newer dip is higher
      * down:  the newer peak is lower AND the newer dip is lower
      * mixed: anything else (one stepping up, the other down, or level)
      * unknown: fewer than two peaks or two dips so far
    A peak or dip counts only once the candles after it have closed, as in lesson 2.
    """
    swings = find_swings(candles, strength)
    peaks = [swing.price for swing in swings if swing.kind == HIGH][-2:]
    dips = [swing.price for swing in swings if swing.kind == LOW][-2:]
    if len(peaks) < 2 or len(dips) < 2:
        return UNKNOWN
    if peaks[1] > peaks[0] and dips[1] > dips[0]:
        return UP
    if peaks[1] < peaks[0] and dips[1] < dips[0]:
        return DOWN
    return MIXED


def combine(*readings: str) -> str:
    """One decision from several readings: up if all say up, down if all say down, otherwise
    mixed, which means no trades. With one reading it is that reading."""
    if not readings:
        raise ValueError("give at least one reading")
    if all(reading == UP for reading in readings):
        return UP
    if all(reading == DOWN for reading in readings):
        return DOWN
    return readings[0] if len(readings) == 1 else MIXED


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
