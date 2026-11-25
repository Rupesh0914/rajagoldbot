"""Reading saved price history into one-minute bars.

Reads the CSV that the MetaTrader 5 export writes: one row per minute, stamped with the broker's
clock, with the spread in points. Rows come out as `Bar`s in UTC with the spread as a price.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from .candles import NEW_YORK, SERVER_AHEAD_OF_NEW_YORK, Bar

EPOCH = datetime(1970, 1, 1)


def server_to_utc(server_seconds: int) -> int:
    """UTC seconds for a time on the broker's clock (New York + 7 hours)."""
    new_york = (EPOCH + timedelta(seconds=server_seconds - SERVER_AHEAD_OF_NEW_YORK)).replace(tzinfo=NEW_YORK)
    return int(new_york.timestamp())


def read_mt5_bars(path: str | Path, point: float = 0.01, before: int | None = None) -> list[Bar]:
    """One-minute bars from an MT5 export CSV, oldest first.

    Columns: server_time (seconds on the broker's clock), open, high, low, close, tick_volume,
    spread (in points). `point` is the size of one point as a price (0.01 for gold at most
    brokers). Rows out of time order or repeated are dropped. With `before` (UTC seconds), bars at
    or after that moment are never loaded at all.
    """
    if point <= 0:
        raise ValueError("point must be positive")
    bars: list[Bar] = []
    last = None
    with open(path, "r", encoding="utf-8-sig", newline="") as handle:
        header = handle.readline().strip()
        if not header.startswith("server_time,"):
            raise ValueError("not an MT5 export this reader knows: the first line should start with server_time,")
        for line in handle:
            parts = line.strip().split(",")
            if len(parts) < 7:
                continue
            try:
                time = server_to_utc(int(parts[0]))
                row = Bar(time, float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]),
                          int(parts[6]) * point)
            except ValueError:
                continue
            if last is not None and time <= last:
                continue
            if before is not None and time >= before:
                break
            last = time
            bars.append(row)
    return bars
