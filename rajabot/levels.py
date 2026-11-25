"""Lesson 2 in code: levels, the prices where gold turned before.

A level here is a swing high (a ceiling) or a swing low (a floor) on closed candles:

  * swing high: a candle whose high is above the highs of the `strength` candles before it and
    the `strength` candles after it;
  * swing low: the same with lows, below.

The catch this file is built around: a swing can only be recognised once the candles AFTER it
have closed. So every level carries the time it became usable, and nothing may use it earlier.

A level stops being a level when a candle closes through it (it is broken) or when it is too old.

Level quality: a person sees at a glance that price has turned at the same area more than once.
`LevelBook.turns_at` counts that: how many confirmed swings sit within a small reach of a price.

This module finds and tracks levels. It decides nothing and places no order.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .candles import Candle

DAY = 86400
HIGH, LOW = "high", "low"
ZONE_CANDLES = 20           # the reach of a zone is measured from this many recent candles
ZONE_SHARE = 0.5            # ...as this share of their average height


@dataclass(frozen=True)
class Level:
    price: float
    kind: str              # "high": a ceiling (resistance). "low": a floor (support).
    made_at: int           # UTC seconds when the candle that made the swing opened
    usable_from: int       # UTC seconds when it was confirmed: the close of the last candle needed

    @property
    def name(self) -> str:
        return "ceiling" if self.kind == HIGH else "floor"


@dataclass(frozen=True)
class Update:
    """What one newly closed candle did to the levels."""
    expired: tuple[Level, ...] = ()     # dropped for age
    broken: tuple[Level, ...] = ()      # the candle closed through them
    new: tuple[Level, ...] = ()         # swings this candle confirmed


def _check_strength(strength: int) -> None:
    if not isinstance(strength, int) or strength < 1:
        raise ValueError("strength must be a whole number of candles, 1 or more")


def _swings_confirmed_by_last(window: list[Candle], strength: int) -> list[Level]:
    """Swings confirmed by the newest candle in `window` (the last 2*strength+1 closed candles).

    The candidate is the middle candle. Highs and lows must be strictly beyond every neighbour:
    two equal highs side by side make no swing high.
    """
    if len(window) < 2 * strength + 1:
        return []
    middle = window[-strength - 1]
    others = window[-2 * strength - 1:-strength - 1] + window[-strength:]
    usable = window[-1].close_time
    found = []
    if all(middle.high > other.high for other in others):
        found.append(Level(middle.high, HIGH, middle.time, usable))
    if all(middle.low < other.low for other in others):
        found.append(Level(middle.low, LOW, middle.time, usable))
    return found


def find_swings(candles: Iterable[Candle], strength: int) -> list[Level]:
    """Every swing high and swing low in closed candles, in the order they became usable.

    This is the plain list, with nothing removed for being broken or old. Use `LevelBook` for the
    levels still standing at a given moment.
    """
    _check_strength(strength)
    window: list[Candle] = []
    swings: list[Level] = []
    for candle in candles:
        window.append(candle)
        del window[:-(2 * strength + 1)]
        swings.extend(_swings_confirmed_by_last(window, strength))
    return swings


@dataclass
class LevelBook:
    """The levels still standing, kept up to date one closed candle at a time.

    For each closed candle, in this order:
      1. levels older than `max_age_days` (counted from when they became usable) are dropped;
      2. levels the candle closed through are broken and dropped: a close above a ceiling, or a
         close below a floor. A wick through a level does not break it;
      3. swings this candle confirms are added.
    A broken level never comes back.

    The book also remembers every swing it confirmed within the age limit, broken or not, so it
    can say how many times price has turned near a price (`turns_at`).
    """
    strength: int
    max_age_days: float = 7.0
    levels: list[Level] = field(default_factory=list)
    _window: list[Candle] = field(default_factory=list, repr=False)
    _heights: list[float] = field(default_factory=list, repr=False)      # last ZONE_CANDLES candle heights
    _turns: list[Level] = field(default_factory=list, repr=False)        # confirmed swings within the age limit

    def __post_init__(self) -> None:
        _check_strength(self.strength)
        if self.max_age_days <= 0:
            raise ValueError("max_age_days must be positive")

    def add(self, candle: Candle) -> Update:
        """Feed the next CLOSED candle. Returns what it changed."""
        if self._window and candle.time <= self._window[-1].time:
            raise ValueError("candles must be in time order with no repeats (at %d)" % candle.time)
        now = candle.close_time
        limit = self.max_age_days * DAY

        expired = tuple(level for level in self.levels if level.usable_from + limit <= now)
        standing = [level for level in self.levels if level.usable_from + limit > now]

        broken = tuple(level for level in standing if _closed_through(candle, level))
        standing = [level for level in standing if not _closed_through(candle, level)]

        self._window.append(candle)
        del self._window[:-(2 * self.strength + 1)]
        new = tuple(_swings_confirmed_by_last(self._window, self.strength))

        self._heights.append(candle.range)
        del self._heights[:-ZONE_CANDLES]
        self._turns = [turn for turn in self._turns if turn.usable_from + limit > now] + list(new)

        self.levels = standing + list(new)
        return Update(expired, broken, new)

    @property
    def reach(self) -> float:
        """How close two turns must be to count as the same area: half the average height of the
        last 20 closed candles. It widens when gold is moving a lot and narrows when it is quiet."""
        if not self._heights:
            return 0.0
        return ZONE_SHARE * sum(self._heights) / len(self._heights)

    def turns_at(self, price: float) -> int:
        """How many confirmed swings, highs or lows, sit within `reach` of this price.

        Counts swings confirmed within the age limit, including ones since broken: a broken
        ceiling that price later bounces off is the same area seen twice. A lone level scores 1.
        """
        reach = self.reach
        return sum(1 for turn in self._turns if abs(turn.price - price) <= reach)

    def ceilings_above(self, price: float) -> list[Level]:
        """Standing ceilings above a price, nearest first."""
        return sorted((l for l in self.levels if l.kind == HIGH and l.price > price), key=lambda l: l.price)

    def floors_below(self, price: float) -> list[Level]:
        """Standing floors below a price, nearest first."""
        return sorted((l for l in self.levels if l.kind == LOW and l.price < price), key=lambda l: -l.price)


def _closed_through(candle: Candle, level: Level) -> bool:
    return candle.close > level.price if level.kind == HIGH else candle.close < level.price


def standing_levels(candles: Iterable[Candle], strength: int, max_age_days: float = 7.0) -> list[Level]:
    """The levels still standing after the last candle given."""
    book = LevelBook(strength, max_age_days)
    for candle in candles:
        book.add(candle)
    return list(book.levels)
