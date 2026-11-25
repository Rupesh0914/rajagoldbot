"""Lesson 8 in code: when not to trade.

Everything here answers one question before a trade is placed: is this a moment to stay out?

  * hours: only the New York session, Monday to Friday;
  * spread: not when the spread is unusually wide;
  * news: not around scheduled news;
  * sideways: not when the market is going nowhere (built, switched off until tested);
  * rejection wick: not straight into a 4-hour candle that was pushed back (built, switched off);
  * daily safety limits: stop for the day after too many trades, too much lost, or a losing run.

`Gate.check` runs them in a fixed order and gives the first reason to stay out, or None.

This module only says yes or no. It places no order.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import Sequence

from .candles import NEW_YORK, Candle, server_seconds
from .direction import BUY, SELL

OUTSIDE_SESSION = "outside_session"
SPREAD_TOO_WIDE = "spread_too_wide"
NEWS = "news"
SIDEWAYS = "sideways"
REJECTION_WICK = "rejection_wick"
MAX_TRADES = "max_trades_per_day"
DAILY_LOSS = "daily_loss_limit"
LOSING_STREAK = "losing_streak"

SESSION_HOURS = (7, 16)             # New York time: 07:00 to 16:00, both ends included
DEFAULT_MAX_SPREAD = 0.50           # dollars. The usual spread on gold here is about 0.13
DEFAULT_NEWS_MINUTES = 30           # stay out this long before and after scheduled news
SIDEWAYS_CANDLES = 12               # 30-minute candles: the last six hours
SIDEWAYS_BELOW = 0.2                # progress under a fifth of the distance travelled is sideways
REJECTION_RATIO = 2.0               # a wick at least twice the body


# ---------------------------------------------------------------------- hours
def in_session(utc_seconds: int, hours: tuple[int, int] = SESSION_HOURS) -> bool:
    """Monday to Friday, 07:00 to 16:00 New York time by default (both ends included)."""
    local = datetime.fromtimestamp(utc_seconds, timezone.utc).astimezone(NEW_YORK)
    minutes = local.hour * 60 + local.minute
    return local.weekday() < 5 and hours[0] * 60 <= minutes <= hours[1] * 60


def trading_day(utc_seconds: int) -> date:
    """The trading day a moment belongs to: it runs from 17:00 to 17:00 New York time and is
    named by the date it ends on, which is the date on the broker's clock."""
    return datetime.fromtimestamp(server_seconds(utc_seconds), timezone.utc).date()


# ----------------------------------------------------------------------- news
@dataclass
class NewsCalendar:
    """Scheduled news, and the minutes around each item to stay out."""
    events: list[tuple[int, str]] = field(default_factory=list)      # (UTC seconds, name)
    before_minutes: int = DEFAULT_NEWS_MINUTES
    after_minutes: int = DEFAULT_NEWS_MINUTES

    def add(self, utc_seconds: int, name: str) -> None:
        self.events.append((int(utc_seconds), name))
        self.events.sort()

    def blocked(self, utc_seconds: int) -> str | None:
        """The name of the news item that blocks this moment, or None."""
        for when, name in self.events:
            if when - self.before_minutes * 60 <= utc_seconds <= when + self.after_minutes * 60:
                return name
        return None

    @classmethod
    def from_csv(cls, path, before_minutes: int = DEFAULT_NEWS_MINUTES,
                 after_minutes: int = DEFAULT_NEWS_MINUTES) -> "NewsCalendar":
        """Read a file with one item a line: `2026-12-04 08:30,US jobs report`, in New York time.

        A first line starting with `when` is taken as a heading. Blank lines and lines starting
        with # are ignored.
        """
        calendar = cls([], before_minutes, after_minutes)
        with open(path, "r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.reader(handle):
                if not row or not row[0].strip() or row[0].lstrip().startswith("#") or row[0].strip().lower().startswith("when"):
                    continue
                local = datetime.strptime(row[0].strip(), "%Y-%m-%d %H:%M").replace(tzinfo=NEW_YORK)
                calendar.add(int(local.timestamp()), row[1].strip() if len(row) > 1 and row[1].strip() else "news")
        return calendar


def jobs_report_time(year: int, month: int) -> int:
    """The usual time of the US jobs report (NFP): the first Friday of the month, 08:30 New York.

    This is the usual pattern, not a guarantee: around holidays the date moves. A real calendar
    (lesson 10 reads MetaTrader's) is the authority.
    """
    day = date(year, month, 1)
    day += timedelta(days=(4 - day.weekday()) % 7)
    return int(datetime(day.year, day.month, day.day, 8, 30, tzinfo=NEW_YORK).timestamp())


# ------------------------------------------------------------------- sideways
def progress(candles: Sequence[Candle], lookback: int = SIDEWAYS_CANDLES) -> float | None:
    """How much of the distance price travelled was real progress, from 0 to 1.

    Over the last `lookback` closed candles: the net move from first close to last close, divided
    by the sum of every close-to-close move in between. Straight up or down is 1. Up and down and
    back to where it started is 0. None until there are enough candles, or if price did not move.
    """
    if lookback < 2:
        raise ValueError("lookback must be at least 2 candles")
    if len(candles) < lookback + 1:
        return None
    closes = [candle.close for candle in candles[-(lookback + 1):]]
    travelled = sum(abs(b - a) for a, b in zip(closes, closes[1:]))
    if travelled <= 0:
        return None
    return abs(closes[-1] - closes[0]) / travelled


def is_sideways(candles: Sequence[Candle], lookback: int = SIDEWAYS_CANDLES, below: float = SIDEWAYS_BELOW) -> bool:
    """True when recent progress is under `below`. False when it cannot be measured yet."""
    value = progress(candles, lookback)
    return value is not None and value < below


# ------------------------------------------------------------- rejection wick
def rejection_wick(candle: Candle, ratio: float = REJECTION_RATIO) -> str | None:
    """"upper" when the candle was pushed back from higher prices, "lower" from lower prices.

    A wick counts when it is at least `ratio` times the body and it is the longer of the two
    wicks. The body is taken as at least one cent, so a candle that closed where it opened still
    gives an answer. None for a candle with no height or no such wick.
    """
    if ratio <= 0:
        raise ValueError("ratio must be positive")
    if candle.range <= 0:
        return None
    body = max(candle.body, 0.01)
    upper, lower = candle.upper_wick, candle.lower_wick
    if upper > lower and upper >= ratio * body:
        return "upper"
    if lower > upper and lower >= ratio * body:
        return "lower"
    return None


def wick_against(side: str, candle: Candle | None, ratio: float = REJECTION_RATIO) -> bool:
    """Was the last closed 4-hour candle pushed back from the side this trade wants to go?"""
    if side not in (BUY, SELL):
        raise ValueError("side must be 'buy' or 'sell'")
    if candle is None:
        return False
    return rejection_wick(candle, ratio) == ("upper" if side == BUY else "lower")


# --------------------------------------------------------- daily safety limits
@dataclass
class DayGuard:
    """Stops new trades for the rest of the trading day once a limit is reached.

    The day runs from 17:00 to 17:00 New York time. Everything resets when a new one starts.
    """
    max_trades: int = 5
    max_loss_r: float = 3.0             # stop after losing this many R in the day
    max_losing_streak: int = 3          # stop after this many losses in a row in the day
    day: date | None = None
    trades: int = 0
    total_r: float = 0.0
    streak: int = 0

    def __post_init__(self) -> None:
        if self.max_trades < 1 or self.max_loss_r <= 0 or self.max_losing_streak < 1:
            raise ValueError("limits must be positive")

    def _roll(self, utc_seconds: int) -> None:
        today = trading_day(utc_seconds)
        if today != self.day:
            self.day, self.trades, self.total_r, self.streak = today, 0, 0.0, 0

    def opened(self, utc_seconds: int) -> None:
        """Call when a trade is opened."""
        self._roll(utc_seconds)
        self.trades += 1

    def closed(self, utc_seconds: int, result_r: float) -> None:
        """Call when a trade is fully closed, with its result in R. Counted on the day it closed."""
        self._roll(utc_seconds)
        self.total_r += result_r
        self.streak = self.streak + 1 if result_r < 0 else 0

    def blocked(self, utc_seconds: int) -> str | None:
        """The limit that stops a new trade now, or None."""
        self._roll(utc_seconds)
        if self.trades >= self.max_trades:
            return MAX_TRADES
        if self.total_r <= -self.max_loss_r:
            return DAILY_LOSS
        if self.streak >= self.max_losing_streak:
            return LOSING_STREAK
        return None


# ----------------------------------------------------------------------- gate
@dataclass
class Gate:
    """Every when-not-to-trade rule, checked in one fixed order.

    Hours, spread, news, sideways, rejection wick, then the daily limits. The first one that says
    no is the reason given. A rule set to None (or False) is switched off.
    """
    session_hours: tuple[int, int] | None = SESSION_HOURS
    max_spread: float | None = DEFAULT_MAX_SPREAD
    news: NewsCalendar | None = None
    avoid_sideways: bool = False                # built, switched off until tested
    avoid_rejection_wick: bool = False          # built, switched off until tested
    guard: DayGuard | None = None

    def check(self, utc_seconds: int, side: str, spread: float, recent_candles: Sequence[Candle] = (),
              last_four_hour: Candle | None = None) -> str | None:
        """The first reason to stay out, or None when a trade may be placed.

        `utc_seconds` is the moment of the signal. `recent_candles` are closed 30-minute candles
        and `last_four_hour` the last closed 4-hour candle, both as known at that moment.
        """
        if self.session_hours is not None and not in_session(utc_seconds, self.session_hours):
            return OUTSIDE_SESSION
        if self.max_spread is not None and spread > self.max_spread:
            return SPREAD_TOO_WIDE
        if self.news is not None and self.news.blocked(utc_seconds):
            return NEWS
        if self.avoid_sideways and is_sideways(recent_candles):
            return SIDEWAYS
        if self.avoid_rejection_wick and wick_against(side, last_four_hour):
            return REJECTION_WICK
        if self.guard is not None:
            return self.guard.blocked(utc_seconds)
        return None
