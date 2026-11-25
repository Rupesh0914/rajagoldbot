"""Lesson 1 in code: candles and timeframes.

A candle sums up what price did in one stretch of time: where it opened, the highest and lowest
it went, and where it closed. The bot is fed one-minute bars and builds the bigger candles it
decides on (30-minute) and reads direction from (4-hour).

Two rules run through this whole file, and through the whole bot:

  * A candle is used only after it has CLOSED. A candle still forming can change completely.
  * Nothing here looks ahead. Each candle is built only from bars at or before it.

This module decides nothing and places no order. It only turns small bars into bigger ones.
"""
from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, NamedTuple
from zoneinfo import ZoneInfo

NEW_YORK = ZoneInfo("America/New_York")
SERVER_AHEAD_OF_NEW_YORK = 7 * 3600     # most gold brokers run their clock 7 hours ahead of New York
FOUR_HOURS = 4 * 3600


class Bar(NamedTuple):
    """One minute of price, as the broker reports it. Prices are bid prices."""
    time: int          # UTC seconds when the minute opened (a multiple of 60)
    open: float
    high: float
    low: float
    close: float
    spread: float = 0.0    # ask minus bid during that minute, in price


@dataclass(frozen=True)
class Candle:
    time: int          # UTC seconds when the candle opened
    open: float
    high: float
    low: float
    close: float
    seconds: int       # how long the candle lasts (1800 for 30 minutes)

    @property
    def close_time(self) -> int:
        return self.time + self.seconds

    @property
    def range(self) -> float:
        """Whole height of the candle, wick tip to wick tip."""
        return self.high - self.low

    @property
    def body(self) -> float:
        """Distance between open and close: the thick part of the candle."""
        return abs(self.close - self.open)

    @property
    def upper_wick(self) -> float:
        return self.high - max(self.open, self.close)

    @property
    def lower_wick(self) -> float:
        return min(self.open, self.close) - self.low

    @property
    def bullish(self) -> bool:
        """Closed higher than it opened (buyers won the candle)."""
        return self.close > self.open

    @property
    def bearish(self) -> bool:
        return self.close < self.open

    @property
    def body_share(self) -> float:
        """How much of the candle is body, from 0 (all wick) to 1 (all body). 0 for a flat candle."""
        return self.body / self.range if self.range > 0 else 0.0


def build_candles(bars: Iterable[Bar], minutes: int, as_of: int | None = None) -> list[Candle]:
    """Turn one-minute bars into CLOSED candles of `minutes` length, oldest first.

    Bars are grouped by clock time (a 30-minute candle runs from :00 to :30 or :30 to :00). A
    stretch with no bars has no candle. The last group is left out unless it is known to have
    closed, because a candle that is still forming must never be used. It is known to have closed
    when a later bar exists, or when `as_of` (the current time, UTC seconds) is at or past its end.
    """
    if minutes <= 0:
        raise ValueError("minutes must be positive")
    seconds = minutes * 60
    candles: list[Candle] = []
    forming: list | None = None                      # [start, open, high, low, close]
    previous = None
    for bar in bars:
        if previous is not None and bar.time <= previous:
            raise ValueError("bars must be in time order with no repeats (at %d)" % bar.time)
        previous = bar.time
        start = bar.time - bar.time % seconds
        if forming is not None and forming[0] != start:
            candles.append(Candle(forming[0], forming[1], forming[2], forming[3], forming[4], seconds))
            forming = None
        if forming is None:
            forming = [start, bar.open, bar.high, bar.low, bar.close]
        else:
            forming[2] = max(forming[2], bar.high)
            forming[3] = min(forming[3], bar.low)
            forming[4] = bar.close
    if forming is not None and as_of is not None and forming[0] + seconds <= as_of:
        candles.append(Candle(forming[0], forming[1], forming[2], forming[3], forming[4], seconds))
    return candles


def server_seconds(utc_seconds: int) -> int:
    """The broker's clock for a moment in time, as seconds.

    The broker's clock is New York time plus 7 hours, all year. That puts the daily break at the
    broker's midnight, which is why a 4-hour candle on the broker's chart starts at 17:00, 21:00,
    01:00, 05:00, 09:00 or 13:00 New York time.
    """
    local = datetime.fromtimestamp(utc_seconds, timezone.utc).astimezone(NEW_YORK)
    return calendar.timegm(local.replace(tzinfo=None).timetuple()) + SERVER_AHEAD_OF_NEW_YORK


def build_four_hour_candles(bars: Iterable[Bar], as_of: int | None = None) -> list[Candle]:
    """CLOSED 4-hour candles as the broker's own chart draws them (blocks of the broker's clock).

    A candle's `time` is the start of its 4-hour block, even when the block's first minutes had no
    bars (the block after the daily break starts an hour late). The last block is left out unless
    it is known to have closed: a later bar exists, or `as_of` (the current time, UTC seconds) is
    in a later block.
    """
    candles: list[Candle] = []
    forming: list | None = None                      # [block, block start, open, high, low, close]
    previous = None
    for bar in bars:
        if previous is not None and bar.time <= previous:
            raise ValueError("bars must be in time order with no repeats (at %d)" % bar.time)
        previous = bar.time
        on_server = server_seconds(bar.time)
        block = on_server // FOUR_HOURS
        if forming is not None and forming[0] != block:
            candles.append(Candle(forming[1], forming[2], forming[3], forming[4], forming[5], FOUR_HOURS))
            forming = None
        if forming is None:
            forming = [block, bar.time - on_server % FOUR_HOURS, bar.open, bar.high, bar.low, bar.close]
        else:
            forming[3] = max(forming[3], bar.high)
            forming[4] = min(forming[4], bar.low)
            forming[5] = bar.close
    if forming is not None and as_of is not None and server_seconds(as_of) // FOUR_HOURS > forming[0]:
        candles.append(Candle(forming[1], forming[2], forming[3], forming[4], forming[5], FOUR_HOURS))
    return candles


def describe(candle: Candle) -> str:
    """One plain line about a candle, used in the lesson's examples."""
    kind = "bullish" if candle.bullish else "bearish" if candle.bearish else "flat"
    return "%s candle: body %.2f, upper wick %.2f, lower wick %.2f, body is %d%% of the candle" % (
        kind, candle.body, candle.upper_wick, candle.lower_wick, round(100 * candle.body_share))
