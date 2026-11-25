# Run 003: the first trade test

Run on the owner's PC on 2026-11-25, code version `785fd71`, point 0.01, 22 seconds. The report
below is as the tool wrote it, except that the empty last column of the breakdown tables is left
out. The reading of it is in [README.md](README.md).

---

# Trade test on the development part

Whole trades, entry to exit: stop beyond the signal candle, one trade at a time, every trade risking the same. Results are in R (multiples of the risk). The spread is paid.

**Development part only** (2024-10-23 to 2025-11-21). Nothing after 2025-11-23 was loaded. A result here is a clue, not a verdict.

- One-minute bars: 382953. Thirty-minute candles: 12785. Median spread: 0.13.
- Code version: `785fd71`.
- "Likely range" is a rough 95% range for the average R. "Worst drop" is the largest fall from a peak in the running total, in R.
- For scale: the pass marks lesson 9 will use on unseen data are a profit factor of at least 1.20 and an average above 0 R.

## The setups

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) | Average R, spread doubled |
|---|---|---|---|---|---|---|---|---|
| Base: level break, New York hours, 4-hour direction, room 1.0, one target at the next level | 115 | 46.1% | +0.083 | -0.133 to +0.299 | 1.17 | +9.5 | 7.7 | +0.023 |
| Exit: halves (half at halfway, stop to break-even) | 115 | 53.9% | +0.025 | -0.152 to +0.201 | 1.06 | +2.8 | 11.5 | -0.007 |
| Exit: quarters ladder with 4-hour time stop (the Sugarwood exit) | 115 | 65.2% | +0.058 | -0.091 to +0.207 | 1.19 | +6.6 | 7.8 | +0.024 |
| Exit: quarters ladder, no time stop | 115 | 66.1% | +0.067 | -0.081 to +0.216 | 1.22 | +7.7 | 7.2 | +0.035 |
| Room at least 1.5 | 95 | 44.2% | +0.054 | -0.190 to +0.297 | 1.11 | +5.1 | 8.6 | -0.010 |
| Room at least 2.0 | 86 | 44.2% | +0.057 | -0.200 to +0.313 | 1.11 | +4.9 | 10.1 | +0.008 |
| Open space skipped | 55 | 45.5% | +0.099 | -0.216 to +0.413 | 1.21 | +5.4 | 9.1 | +0.100 |
| Level as trigger only: no room rule, target always 2R | 163 | 47.9% | +0.140 | -0.047 to +0.327 | 1.30 | +22.8 | 11.7 | +0.096 |
| No hours or direction filter | 398 | 34.9% | -0.037 | -0.175 to +0.101 | 0.94 | -14.7 | 38.9 | -0.050 |
| Benchmark: any convincing candle, same hours and direction, target 2R | 646 | 44.4% | +0.105 | +0.010 to +0.201 | 1.21 | +68.1 | 12.5 | +0.083 |
| Benchmark with the quarters ladder | 838 | 63.7% | +0.019 | -0.034 to +0.072 | 1.06 | +16.0 | 11.6 | -0.008 |

## How the trades ended

By the last part closed. "Stop" includes stops that had been moved up behind banked parts, so a ladder trade can end at its stop and still be a winner.

| | Target | Stop | Time stop | End of day |
|---|---|---|---|---|
| Base: level break, New York hours, 4-hour direction, room 1.0, one target at the next level | 26 | 50 | 0 | 39 |
| Exit: halves (half at halfway, stop to break-even) | 19 | 63 | 0 | 33 |
| Exit: quarters ladder with 4-hour time stop (the Sugarwood exit) | 11 | 79 | 5 | 20 |
| Exit: quarters ladder, no time stop | 11 | 80 | 0 | 24 |
| Room at least 1.5 | 17 | 43 | 0 | 35 |
| Room at least 2.0 | 14 | 38 | 0 | 34 |
| Open space skipped | 14 | 25 | 0 | 16 |
| Level as trigger only: no room rule, target always 2R | 36 | 70 | 0 | 57 |
| No hours or direction filter | 94 | 235 | 0 | 69 |
| Benchmark: any convincing candle, same hours and direction, target 2R | 146 | 300 | 0 | 200 |
| Benchmark with the quarters ladder | 74 | 638 | 29 | 97 |

## How far the ladders got

How many parts of the position were closed at a target before the trade ended.

| | 0 parts | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Exit: halves (half at halfway, stop to break-even) | 68 | 28 | 19 | 0 | 0 |
| Exit: quarters ladder with 4-hour time stop (the Sugarwood exit) | 47 | 29 | 19 | 9 | 11 |
| Exit: quarters ladder, no time stop | 47 | 29 | 19 | 9 | 11 |
| Benchmark with the quarters ladder | 332 | 242 | 118 | 72 | 74 |

## Inside the base setup

Small groups swing widely by luck: read the trade count before the average.

### Buy and sell

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| buy | 76 | 44.7% | +0.048 | -0.216 to +0.313 | 1.10 | +3.7 | 6.3 |
| sell | 39 | 48.7% | +0.151 | -0.228 to +0.529 | 1.34 | +5.9 | 8.0 |

### Time of day at entry

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| 07-10 New York | 46 | 43.5% | +0.162 | -0.234 to +0.558 | 1.30 | +7.5 | 7.7 |
| 10-13 New York | 37 | 54.1% | +0.239 | -0.145 to +0.622 | 1.56 | +8.8 | 4.0 |
| 13-17 New York | 32 | 40.6% | -0.211 | -0.488 to +0.066 | 0.53 | -6.7 | 9.9 |

### Aiming at a level, or open space

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| a level | 55 | 45.5% | +0.099 | -0.216 to +0.413 | 1.21 | +5.4 | 9.1 |
| open space | 60 | 46.7% | +0.068 | -0.231 to +0.368 | 1.14 | +4.1 | 5.5 |

### Reward planned at entry

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| 1.5R to 3R | 80 | 43.8% | +0.062 | -0.209 to +0.333 | 1.12 | +4.9 | 8.1 |
| 3R or more | 13 | 38.5% | -0.141 | -0.725 to +0.442 | 0.73 | -1.8 | 4.9 |
| under 1.5R | 22 | 59.1% | +0.292 | -0.143 to +0.728 | 1.83 | +6.4 | 2.0 |

### How it ended

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| flat | 39 | 69.2% | +0.370 | +0.134 to +0.606 | 3.72 | +14.4 | 1.1 |
| stop | 50 | 0.0% | -1.000 | -1.000 to -1.000 | 0.00 | -50.0 | 50.0 |
| target | 26 | 100.0% | +1.735 | +1.566 to +1.904 | inf | +45.1 | 0.0 |

### Half-year

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| 2024 second half | 20 | 60.0% | +0.516 | -0.061 to +1.093 | 2.53 | +10.3 | 3.7 |
| 2025 first half | 46 | 43.5% | +0.060 | -0.281 to +0.400 | 1.12 | +2.7 | 7.7 |
| 2025 second half | 49 | 42.9% | -0.072 | -0.382 to +0.238 | 0.86 | -3.5 | 7.2 |

Median time in a trade: 80 minutes. Median reward planned: 2.00R.

## Signals the base setup did not trade

| Reason | Count |
|---|---|
| against_direction | 299 |
| not_enough_room | 76 |
| outside_session | 277 |
| position_open | 3 |
| stop_too_wide | 23 |
| weak_candle | 239 |

## What this cannot say

- It describes 13 months of the past. It is not a forecast.
- Fills are simulated from one-minute bars. A stop fills at its price unless price jumped past it. Real stops slip more. The doubled-spread column is the allowance for that.
- When one minute touches both the stop and a target, the stop is assumed first. When a target moves the stop up, the new stop applies from the next minute.
- Several setups are compared on the same data. The best of several looks better than it is.
