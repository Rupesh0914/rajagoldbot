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

# Lesson 2, level quality: the same morning, but instead of breaking 3761 gold turns just under
# it a second time, at 3760.
LESSON_2_TWICE = _half_hours(datetime(2026, 11, 10, 13, 0, tzinfo=timezone.utc), [
    (3747.0, 3752.0, 3746.0, 3751.0),      # 08:00
    (3751.0, 3756.0, 3750.0, 3755.0),      # 08:30
    (3755.0, 3761.0, 3754.0, 3757.0),      # 09:00  first turn, at 3761
    (3757.0, 3758.0, 3751.0, 3752.0),      # 09:30
    (3752.0, 3755.0, 3747.0, 3748.0),      # 10:00
    (3748.0, 3750.0, 3742.0, 3746.0),      # 10:30  the low of the morning
    (3746.0, 3753.0, 3745.0, 3752.0),      # 11:00
    (3752.0, 3757.0, 3749.0, 3756.0),      # 11:30
    (3756.0, 3760.0, 3754.0, 3758.0),      # 12:00  second turn, at 3760
    (3758.0, 3759.0, 3752.0, 3753.0),      # 12:30
    (3753.0, 3754.0, 3748.0, 3749.0),      # 13:00
])

FOUR_HOURS = 4 * 3600


def _four_hours(first_open_utc: datetime, rows: list[tuple[float, float, float, float]]) -> list[Candle]:
    start = int(first_open_utc.timestamp())
    return [Candle(start + i * FOUR_HOURS, o, h, l, c, FOUR_HOURS) for i, (o, h, l, c) in enumerate(rows)]


# Lesson 3, structure: twelve 4-hour candles (two trading days) stepping up. Two peaks, the second
# higher than the first; two dips, the second higher than the first.
LESSON_3 = _four_hours(datetime(2026, 11, 9, 22, 0, tzinfo=timezone.utc), [
    (3692.0, 3700.0, 3690.0, 3698.0),
    (3698.0, 3706.0, 3696.0, 3704.0),
    (3704.0, 3715.0, 3703.0, 3710.0),      # first peak, 3715
    (3710.0, 3711.0, 3700.0, 3702.0),
    (3702.0, 3708.0, 3697.0, 3700.0),      # first dip, 3697
    (3700.0, 3714.0, 3699.0, 3712.0),
    (3712.0, 3722.0, 3709.0, 3720.0),
    (3720.0, 3731.0, 3718.0, 3726.0),      # second peak, 3731: higher
    (3726.0, 3727.0, 3715.0, 3717.0),
    (3717.0, 3724.0, 3712.0, 3715.0),      # second dip, 3712: higher
    (3715.0, 3730.0, 3714.0, 3728.0),
    (3728.0, 3738.0, 3725.0, 3736.0),
])
