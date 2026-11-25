"""Small hand-made price examples used by the lessons. Not market data."""
from __future__ import annotations

from datetime import datetime, timezone

from .candles import Candle

HALF_HOUR = 1800


def _half_hours(first_open_utc: datetime, rows: list[tuple[float, float, float, float]]) -> list[Candle]:
    start = int(first_open_utc.timestamp())
    return [Candle(start + i * HALF_HOUR, o, h, l, c, HALF_HOUR) for i, (o, h, l, c) in enumerate(rows)]


# Lesson 2: ten 30-minute candles from 08:00 to 13:00 New York time (13:00 UTC in winter).
# Gold climbs to 3761, falls back to 3742, then pushes up through 3761.
LESSON_2 = _half_hours(datetime(2026, 11, 10, 13, 0, tzinfo=timezone.utc), [
    # open, high, low, close
    (3747.0, 3752.0, 3746.0, 3751.0),      # 08:00
    (3751.0, 3756.0, 3750.0, 3755.0),      # 08:30
    (3755.0, 3761.0, 3754.0, 3757.0),      # 09:00  the high of the morning
    (3757.0, 3758.0, 3751.0, 3752.0),      # 09:30
    (3752.0, 3755.0, 3747.0, 3748.0),      # 10:00
    (3748.0, 3750.0, 3742.0, 3746.0),      # 10:30  the low of the morning
    (3746.0, 3753.0, 3745.0, 3752.0),      # 11:00
    (3752.0, 3757.0, 3749.0, 3756.0),      # 11:30
    (3756.0, 3763.0, 3755.0, 3762.0),      # 12:00  closes above 3761
    (3762.0, 3766.0, 3759.0, 3765.0),      # 12:30
])
