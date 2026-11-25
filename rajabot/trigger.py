"""Lesson 4 in code: the trigger, the moment the bot says "this is a signal".

A signal needs all of these, checked when a 30-minute candle closes:

  1. the candle closed through a standing level: above a ceiling (a buy) or below a floor (a sell);
  2. the candle is convincing: it closed in that direction and enough of it is body, not wick;
  3. the direction from lesson 3 agrees (when that filter is switched on);
  4. the level is good enough (when the level-quality option from lesson 2 is switched on).

A break that fails a check is a skip, recorded with its reason. The level is used up either way:
it was broken, so it is no longer a level.

A signal is not yet a trade. Room to run (lesson 5), the stop and size (lesson 6) and the
when-not-to-trade rules (lesson 8) still have to pass. This module places no order.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .candles import Candle
from .direction import BUY, SELL, allows
from .levels import HIGH, LOW, Level, LevelBook, Update

BOTH_WAYS = "both_ways"                     # broke a ceiling and a floor at once: no clear side
WEAK_CANDLE = "weak_candle"                 # too much wick, or closed against the break
AGAINST_DIRECTION = "against_direction"     # the direction from lesson 3 does not agree
WEAK_LEVEL = "weak_level"                   # price has not turned here often enough

DEFAULT_MIN_BODY = 0.5                      # at least half the candle must be body


@dataclass(frozen=True)
class Signal:
    side: str               # "buy" or "sell"
    level: Level            # the level that was broken (the furthest one, if several)
    candle: Candle          # the candle that broke it
    body_share: float       # how much of that candle is body, 0 to 1
    turns: int              # how many times price had turned at this area

    @property
    def time(self) -> int:
        """When the signal exists: the close of the signal candle, never earlier."""
        return self.candle.close_time


@dataclass(frozen=True)
class Skip:
    reason: str
    candle: Candle
    side: str | None = None
    level: Level | None = None

    @property
    def time(self) -> int:
        return self.candle.close_time


def decide(candle: Candle, update: Update, *, turns: Callable[[float], int], direction: str | None = None,
           min_body: float = DEFAULT_MIN_BODY, min_turns: int = 1) -> Signal | Skip | None:
    """Turn what a closed candle did to the levels into a signal, a skip, or nothing.

    `update` is what `LevelBook.add(candle)` returned. `turns` answers "how many times has price
    turned near this price" (`LevelBook.turns_at`). `direction` is the reading from lesson 3, or
    None when that filter is switched off.
    """
    if not 0 < min_body <= 1:
        raise ValueError("min_body is a share of the candle: above 0, at most 1")
    if not isinstance(min_turns, int) or min_turns < 1:
        raise ValueError("min_turns must be a whole number, 1 or more")

    ceilings = [level for level in update.broken if level.kind == HIGH]
    floors = [level for level in update.broken if level.kind == LOW]
    if not ceilings and not floors:
        return None
    if ceilings and floors:
        return Skip(BOTH_WAYS, candle)

    if ceilings:
        side, level = BUY, max(ceilings, key=lambda l: l.price)
        with_the_break = candle.bullish
    else:
        side, level = SELL, min(floors, key=lambda l: l.price)
        with_the_break = candle.bearish

    if not with_the_break or candle.body_share < min_body:
        return Skip(WEAK_CANDLE, candle, side, level)
    if direction is not None and not allows(direction, side):
        return Skip(AGAINST_DIRECTION, candle, side, level)
    count = turns(level.price)
    if count < min_turns:
        return Skip(WEAK_LEVEL, candle, side, level)
    return Signal(side, level, candle, candle.body_share, count)


class Trigger:
    """Keeps the levels up to date and reports a signal or a skip for each closed candle."""

    def __init__(self, book: LevelBook, min_body: float = DEFAULT_MIN_BODY, min_turns: int = 1) -> None:
        self.book = book
        self.min_body = min_body
        self.min_turns = min_turns

    def on_candle(self, candle: Candle, direction: str | None = None) -> Signal | Skip | None:
        """Feed the next CLOSED 30-minute candle, with the direction as known at its close."""
        update = self.book.add(candle)
        return decide(candle, update, turns=self.book.turns_at, direction=direction,
                      min_body=self.min_body, min_turns=self.min_turns)
