# Run 004: investigating the weaknesses of run 003

Run on the owner's PC on 2026-11-25, code version `9277b60`, point 0.01, 29 seconds. Same data as
run 003 (development part, 2024-10-23 to 2025-11-21).

Every table that run 003 already had came out identical and is not repeated: see
[003-trade-test.md](003-trade-test.md). Below are the tables that are new in this run, as the
tool wrote them (the empty last column of the breakdown tables is left out). The reading is in
[README.md](README.md).

---

## Where to take profit

The same entries with the profit taken at different distances. "No target" holds until the stop or 16:50 New York.

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) | Average R, spread doubled |
|---|---|---|---|---|---|---|---|---|
| Benchmark, target 1R | 855 | 51.9% | +0.045 | -0.017 to +0.107 | 1.11 | +38.8 | 16.3 | +0.030 |
| Benchmark, target 1.5R | 713 | 46.8% | +0.091 | +0.009 to +0.172 | 1.19 | +64.7 | 12.7 | +0.062 |
| Benchmark, target 2R (from run 003) | 646 | 44.4% | +0.105 | +0.010 to +0.201 | 1.21 | +68.1 | 12.5 | +0.083 |
| Benchmark, target 3R | 582 | 40.5% | +0.133 | +0.016 to +0.251 | 1.25 | +77.6 | 11.7 | +0.101 |
| Benchmark, no target: stop or end of day | 499 | 37.3% | +0.175 | +0.007 to +0.344 | 1.30 | +87.5 | 15.9 | +0.134 |
| Benchmark, halves at 2R | 687 | 53.0% | +0.058 | -0.015 to +0.132 | 1.14 | +40.1 | 15.2 | +0.034 |
| Level as trigger only, no target: stop or end of day | 152 | 43.4% | +0.149 | -0.095 to +0.393 | 1.29 | +22.6 | 14.8 | +0.121 |

## Suggested by earlier runs (hindsight)

Picked after seeing that the afternoon did worst in runs 001 and 003. A setting chosen because it looked good will look good again on the same data. Watch, do not trust.

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) | Average R, spread doubled |
|---|---|---|---|---|---|---|---|---|
| Benchmark, entries 07:00 to 13:00 only | 522 | 45.0% | +0.141 | +0.030 to +0.252 | 1.27 | +73.5 | 12.2 | +0.124 |
| Level as trigger only, entries 07:00 to 13:00 only | 128 | 48.4% | +0.207 | -0.018 to +0.432 | 1.42 | +26.5 | 11.2 | +0.152 |

## How the trades ended (new setups)

| | Target | Stop | Time stop | End of day |
|---|---|---|---|---|
| Benchmark, target 1R | 369 | 327 | 0 | 159 |
| Benchmark, target 1.5R | 226 | 310 | 0 | 177 |
| Benchmark, target 3R | 77 | 290 | 0 | 215 |
| Benchmark, no target: stop or end of day | 0 | 272 | 0 | 227 |
| Benchmark, halves at 2R | 123 | 383 | 0 | 181 |
| Level as trigger only, no target: stop or end of day | 0 | 72 | 0 | 80 |
| Benchmark, entries 07:00 to 13:00 only | 134 | 260 | 0 | 128 |
| Level as trigger only, entries 07:00 to 13:00 only | 34 | 59 | 0 | 35 |

Benchmark, halves at 2R: 386 trades banked nothing, 178 banked the first half, 123 banked both.

## Inside: Benchmark: any convincing candle, same hours and direction, target 2R

### Did the signal candle also break a level?

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| no level broken | 547 | 43.0% | +0.069 | -0.034 to +0.172 | 1.13 | +37.7 | 12.7 |
| yes, broke a level | 99 | 52.5% | +0.307 | +0.057 to +0.556 | 1.72 | +30.4 | 8.2 |

### Buy and sell

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| buy | 359 | 44.8% | +0.111 | -0.016 to +0.239 | 1.22 | +39.9 | 10.9 |
| sell | 287 | 43.9% | +0.098 | -0.046 to +0.242 | 1.19 | +28.2 | 12.9 |

### Time of day at entry

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| 07-10 New York | 290 | 43.1% | +0.195 | +0.033 to +0.357 | 1.35 | +56.5 | 12.4 |
| 10-13 New York | 203 | 47.8% | +0.069 | -0.085 to +0.223 | 1.15 | +14.0 | 15.0 |
| 13-17 New York | 153 | 42.5% | -0.016 | -0.177 to +0.145 | 0.96 | -2.4 | 14.1 |

### Half-year

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| 2024 second half | 103 | 46.6% | +0.199 | -0.040 to +0.438 | 1.44 | +20.5 | 12.5 |
| 2025 first half | 298 | 44.3% | +0.075 | -0.065 to +0.215 | 1.15 | +22.4 | 10.6 |
| 2025 second half | 245 | 43.7% | +0.103 | -0.053 to +0.259 | 1.20 | +25.2 | 11.5 |

### How it ended

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| flat | 200 | 70.5% | +0.380 | +0.292 to +0.469 | 4.44 | +76.1 | 1.8 |
| stop | 300 | 0.0% | -1.000 | -1.000 to -1.000 | 0.00 | -300.0 | 300.0 |
| target | 146 | 100.0% | +2.000 | +2.000 to +2.000 | inf | +292.0 | 0.0 |

Median time in a trade: 84 minutes. Median reward planned: 2.00R.

## Inside: Level as trigger only: no room rule, target always 2R

### Buy and sell

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| buy | 97 | 44.3% | +0.068 | -0.173 to +0.309 | 1.14 | +6.6 | 9.0 |
| sell | 66 | 53.0% | +0.245 | -0.051 to +0.542 | 1.58 | +16.2 | 7.5 |

### Time of day at entry

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| 07-10 New York | 74 | 47.3% | +0.282 | -0.036 to +0.600 | 1.55 | +20.9 | 7.4 |
| 10-13 New York | 47 | 53.2% | +0.206 | -0.131 to +0.542 | 1.49 | +9.7 | 4.0 |
| 13-17 New York | 42 | 42.9% | -0.184 | -0.436 to +0.068 | 0.58 | -7.7 | 10.5 |

### Half-year

| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) |
|---|---|---|---|---|---|---|---|
| 2024 second half | 29 | 55.2% | +0.391 | -0.061 to +0.844 | 2.10 | +11.3 | 5.7 |
| 2025 first half | 67 | 43.3% | +0.022 | -0.261 to +0.306 | 1.04 | +1.5 | 11.7 |
| 2025 second half | 67 | 49.3% | +0.149 | -0.149 to +0.447 | 1.31 | +10.0 | 7.6 |

Median time in a trade: 90 minutes.
