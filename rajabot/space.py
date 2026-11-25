"""Lesson 5 in code: room to run.

A signal says price got through a level. This asks the next question: is there open space ahead,
or is another level sitting so close that the trade has nowhere to go?

  * the wall: the next standing level in the way. For a buy, the nearest ceiling above the entry.
    For a sell, the nearest floor below it.
  * the room: the distance from the entry to the wall.
  * the risk: the distance from the entry back to the far end of the signal candle, where the
    idea is proven wrong (lesson 6 places the real stop there).

The trade has enough room when room / risk is at least a chosen ratio. No wall at all is open
space.

This module measures and judges. It places no order.
"""
from __future__ import annotations

from dataclasses import dataclass

from .direction import BUY, SELL
from .levels import Level, LevelBook
from .trigger import Signal

NOT_ENOUGH_ROOM = "not_enough_room"         # the wall is too close for the risk taken
OPEN_SPACE = "open_space"                   # no wall ahead, and open space is switched off
NO_RISK = "no_risk_distance"                # the entry is not on the right side of the candle's far end

DEFAULT_MIN_RATIO = 1.0                     # at least as much room as risk


@dataclass(frozen=True)
class Room:
    side: str
    entry: float
    risk: float                 # entry to the far end of the signal candle
    wall: Level | None          # the next level in the way; None means open space

    @property
    def distance(self) -> float | None:
        """Entry to the wall. None in open space."""
        if self.wall is None:
            return None
        return self.wall.price - self.entry if self.side == BUY else self.entry - self.wall.price

    @property
    def ratio(self) -> float | None:
        """Room divided by risk. None in open space or when there is no risk distance."""
        if self.wall is None or self.risk <= 0:
            return None
        return self.distance / self.risk


def measure_room(signal: Signal, book: LevelBook, entry: float | None = None, risk: float | None = None) -> Room:
    """Measure the room ahead of a signal, using only levels standing at that moment.

    Call it right after the signal candle was fed to the book, so the level just broken is gone
    and anything that candle confirmed is in. `entry` defaults to the signal candle's close and
    `risk` to the distance back to the candle's far end. Once lesson 6 has worked out the real
    entry and stop, pass those: `entry=plan.entry, risk=plan.distance`.
    """
    candle = signal.candle
    price = candle.close if entry is None else entry
    if signal.side == BUY:
        ahead = book.ceilings_above(price)
        estimate = price - candle.low
    elif signal.side == SELL:
        ahead = book.floors_below(price)
        estimate = candle.high - price
    else:
        raise ValueError("side must be 'buy' or 'sell'")
    return Room(signal.side, price, estimate if risk is None else risk, ahead[0] if ahead else None)


def check_room(room: Room, min_ratio: float = DEFAULT_MIN_RATIO, allow_open_space: bool = True) -> str | None:
    """None when there is enough room; otherwise the reason there is not."""
    if min_ratio <= 0:
        raise ValueError("min_ratio must be positive")
    if room.risk <= 0:
        return NO_RISK
    if room.wall is None:
        return None if allow_open_space else OPEN_SPACE
    return None if room.ratio >= min_ratio else NOT_ENOUGH_ROOM


def describe_room(room: Room, min_ratio: float = DEFAULT_MIN_RATIO, allow_open_space: bool = True) -> str:
    """Plain lines about the room, used in the lesson's examples."""
    verdict = check_room(room, min_ratio, allow_open_space)
    lines = ["Entry about %.2f. Risk: %.2f (back to the far end of the signal candle)." % (room.entry, room.risk)]
    if room.wall is None:
        lines.append("No level in the way: open space.")
    else:
        lines.append("Next %s in the way: %.2f. Room: %.2f." % (room.wall.name, room.wall.price, room.distance))
        if room.ratio is not None:
            lines.append("Room is %.2f times the risk. Needed: %.2f." % (room.ratio, min_ratio))
    lines.append("ENOUGH ROOM." if verdict is None else {
        NOT_ENOUGH_ROOM: "NOT ENOUGH ROOM: skipped.",
        OPEN_SPACE: "OPEN SPACE with no target level: skipped (open space is switched off).",
        NO_RISK: "No risk distance could be measured: skipped.",
    }[verdict])
    return "\n".join(lines)
