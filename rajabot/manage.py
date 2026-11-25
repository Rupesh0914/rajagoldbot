"""Lesson 7 in code: managing the trade from entry to exit.

Once a trade is open there are only four ways it ends:

  * target: price reaches where the profit is taken;
  * stop: price reaches the stop;
  * time stop: nothing has been banked after a set number of hours, so it is closed;
  * flat: the end of the trading day, when everything is closed.

How the profit is taken is the exit style. Three are built here:

  * SINGLE: the whole position at the target. The stop never moves.
  * HALVES: half at the halfway point, the stop moves to the entry price (break-even), the rest
    at the target.
  * QUARTERS: the ladder of the earlier Sugarwood bot. A quarter each at 25%, 50%, 75% and 100%
    of the way to the target. After the first quarter the stop moves to break-even, then it
    follows one step behind. Closed if no step is banked within 4 hours.

The same `Position` object is stepped one-minute bar by one-minute bar in a test and, later, on
the live demo account, so both follow the same rules. This module places no order itself.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta, timezone

from .candles import NEW_YORK, Bar
from .direction import BUY, SELL
from .levels import Level
from .risk import Plan

TARGET, STOP, TIME_STOP, FLAT = "target", "stop", "time_stop", "flat"
DEFAULT_OPEN_SPACE_R = 2.0          # with no level to aim at, the target is this many times the risk
FLAT_TIME = time(16, 50)            # New York time: everything is closed
_EPS = 1e-9                         # prices are sums of cents; this absorbs rounding in those sums


@dataclass(frozen=True)
class ExitStyle:
    name: str
    fractions: tuple[float, ...]            # where each part is closed, as a share of the way to the target
    move_stop: bool                         # move the stop up behind banked parts
    time_stop_hours: float | None = None    # close if nothing is banked within this many hours

    def __post_init__(self) -> None:
        steps = self.fractions
        if not steps or any(not 0 < f <= 1 for f in steps) or list(steps) != sorted(set(steps)) or steps[-1] != 1.0:
            raise ValueError("fractions must rise, each above 0, and end at 1.0")
        if self.time_stop_hours is not None and self.time_stop_hours <= 0:
            raise ValueError("time_stop_hours must be positive")


SINGLE = ExitStyle("single", (1.0,), move_stop=False)
HALVES = ExitStyle("halves", (0.5, 1.0), move_stop=True)
QUARTERS = ExitStyle("quarters", (0.25, 0.5, 0.75, 1.0), move_stop=True, time_stop_hours=4.0)
STYLES = {style.name: style for style in (SINGLE, HALVES, QUARTERS)}

# With too little size for every step, fewer steps are used, as the Sugarwood bot did:
# three parts take steps 1, 2 and 4; two parts take steps 1 and 3; one part takes step 2.
_FEWER_OF_FOUR = {3: (0, 1, 3), 2: (0, 2), 1: (1,)}


@dataclass(frozen=True)
class Leg:
    lots: float
    step: int               # which step of the style this part is closed at (0 = the first)
    price: float            # the price at which it is closed


@dataclass(frozen=True)
class Fill:
    time: int
    lots: float
    price: float
    reason: str
    step: int | None = None


def target_price(plan: Plan, wall: Level | None, spread: float, open_space_r: float = DEFAULT_OPEN_SPACE_R) -> float:
    """Where the profit is taken.

    With a level ahead: a touch in front of it, by one spread. For a sell one more spread is
    added, because a sell is closed at the ask. With no level ahead: `open_space_r` times the
    risk away from the entry.
    """
    if wall is None:
        if open_space_r <= 0:
            raise ValueError("open_space_r must be positive")
        away = open_space_r * plan.distance
        return plan.entry + away if plan.side == BUY else plan.entry - away
    return wall.price - spread if plan.side == BUY else wall.price + 2 * spread


def build_legs(plan: Plan, target: float, style: ExitStyle) -> list[Leg]:
    """Split the position into the parts the style closes, on the broker's lot steps.

    Parts are equal where the size allows; any odd steps of size go to the earliest parts. With
    too little size for every step, fewer steps are used.
    """
    reward = target - plan.entry if plan.side == BUY else plan.entry - target
    if reward <= 0:
        raise ValueError("the target is not on the profit side of the entry")
    step_size = plan.contract.volume_step
    units = int(round(plan.lots / step_size))
    wanted = len(style.fractions)
    if units <= 0:
        raise ValueError("the plan has no size")
    if units >= wanted:
        steps = list(range(wanted))
        each, extra = divmod(units, wanted)
        sizes = [each + (1 if index < extra else 0) for index in range(wanted)]
    else:
        steps = list(_FEWER_OF_FOUR[units]) if wanted == 4 else list(range(wanted - units, wanted))
        sizes = [1] * units
    return [Leg(round(size * step_size, 8), step, _step_price(plan, target, style.fractions[step]))
            for step, size in zip(steps, sizes)]


def _step_price(plan: Plan, target: float, fraction: float) -> float:
    return plan.entry + fraction * (target - plan.entry)


def flat_time_after(opened_at: int) -> int:
    """The next 16:50 New York time at or after the entry, as UTC seconds."""
    local = datetime.fromtimestamp(opened_at, timezone.utc).astimezone(NEW_YORK)
    flat = datetime.combine(local.date(), FLAT_TIME, tzinfo=NEW_YORK)
    if flat < local:
        flat = datetime.combine(local.date() + timedelta(days=1), FLAT_TIME, tzinfo=NEW_YORK)
    return int(flat.timestamp())


@dataclass
class Position:
    """One open trade, stepped one-minute bar by one-minute bar.

    Each bar, in this order: the end of the day and the time stop (at the bar's open), then the
    stop, then the targets. The stop is checked before the targets, so a bar that touches both
    counts as stopped: the cautious reading. A stop moved up by a target applies from the next
    bar. A stop that price jumps past is filled at the worse price. A target is filled exactly
    at its price, never better.
    """
    plan: Plan
    target: float
    style: ExitStyle
    opened_at: int
    stop_buffer: float = 0.0                    # how far behind a banked step the stop sits
    legs: list[Leg] = field(default_factory=list)
    stop: float = 0.0
    fills: list[Fill] = field(default_factory=list)
    flat_at: int = 0
    time_stop_at: int | None = None

    def __post_init__(self) -> None:
        self.legs = build_legs(self.plan, self.target, self.style)
        self.stop = self.plan.stop
        self.flat_at = flat_time_after(self.opened_at)
        if self.style.time_stop_hours is not None:
            self.time_stop_at = self.opened_at + int(self.style.time_stop_hours * 3600)

    # ------------------------------------------------------------------ state
    @property
    def open(self) -> bool:
        return bool(self.legs)

    @property
    def lots_open(self) -> float:
        return round(sum(leg.lots for leg in self.legs), 8)

    @property
    def banked(self) -> int:
        """How many parts have been closed at their target."""
        return sum(1 for fill in self.fills if fill.reason == TARGET)

    @property
    def money(self) -> float:
        """Result so far, in the account's currency, commission included."""
        sign = 1.0 if self.plan.side == BUY else -1.0
        gross = sum(sign * (fill.price - self.plan.entry) * self.plan.contract.money_per_dollar(fill.lots)
                    for fill in self.fills)
        closed = sum(fill.lots for fill in self.fills)
        return gross - self.plan.commission_money * (closed / self.plan.lots)

    @property
    def result_r(self) -> float:
        """Result so far in R: multiples of the money this trade put at risk."""
        return self.money / self.plan.risk_money

    @property
    def last_reason(self) -> str | None:
        return self.fills[-1].reason if self.fills else None

    # ------------------------------------------------------------------- step
    def on_bar(self, bar: Bar) -> list[Fill]:
        """Apply one one-minute bar. Returns what was closed on it."""
        if not self.open:
            return []
        buy = self.plan.side == BUY
        spread = bar.spread
        open_exit = bar.open if buy else bar.open + spread          # the price a close gets at the bar's open
        before = len(self.fills)

        if bar.time >= self.flat_at:
            self._close_all(bar.time, open_exit, FLAT)
        elif self.time_stop_at is not None and bar.time >= self.time_stop_at and self.banked == 0:
            self._close_all(bar.time, open_exit, TIME_STOP)
        elif buy and bar.low <= self.stop + _EPS:
            self._close_all(bar.time, min(self.stop, bar.open), STOP)
        elif not buy and bar.high + spread >= self.stop - _EPS:
            self._close_all(bar.time, max(self.stop, bar.open + spread), STOP)
        else:
            for leg in list(self.legs):
                reached = bar.high >= leg.price - _EPS if buy else bar.low + spread <= leg.price + _EPS
                if not reached:
                    break
                self.legs.remove(leg)
                self.fills.append(Fill(bar.time, leg.lots, leg.price, TARGET, leg.step))
                self._move_stop_behind(leg.step)
        return self.fills[before:]

    def _close_all(self, when: int, price: float, reason: str) -> None:
        for leg in self.legs:
            self.fills.append(Fill(when, leg.lots, price, reason))
        self.legs = []

    def _move_stop_behind(self, step: int) -> None:
        """After a part is banked: break-even after the first step, then one step behind."""
        if not self.style.move_stop:
            return
        buy = self.plan.side == BUY
        if step == 0:
            new = self.plan.entry
        else:
            behind = _step_price(self.plan, self.target, self.style.fractions[step - 1])
            new = behind - self.stop_buffer if buy else behind + self.stop_buffer
        self.stop = max(self.stop, new) if buy else min(self.stop, new)       # never against the trade
