# Run 001: signal check on the development part

Run on the owner's PC on 2026-11-25, code version `6b833ac`, point 0.01, 17 seconds. The report
below is exactly as the tool wrote it. The reading of it is in
[README.md](README.md).

---

# Signal check on the development part

**Not a profit backtest.** The bot has no stop, target or size yet. This asks one question of the trigger alone: after a signal, which comes first, one unit our way or one unit against us? One unit is the average height of the last 20 thirty-minute candles. A coin flip gives a 50% win share and an average a little below zero, because the spread is paid.

**Development part only** (2024-10-23 to 2025-11-21). Nothing after 2025-11-23 was loaded. A result here is a clue, not a verdict.

- One-minute bars: 382953. Thirty-minute candles: 12785. Median spread: 0.13.
- Median unit: 5.94. So the spread costs about 0.022 units per signal.
- Code version: `6b833ac`.
- "Likely range" is a rough 95% range for the average. Signals overlap in time, so the true range is wider than shown.

## One change at a time

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| Base: strength 4, body 50%, any level, no direction filter | 784 | 50.0% | +0.000 | -0.070 to +0.070 | -0.021 |
| Strength 2 (more, minor levels) | 1337 | 50.0% | +0.010 | -0.044 to +0.065 | -0.016 |
| Strength 8 (fewer, major levels) | 459 | 51.3% | +0.024 | -0.067 to +0.116 | -0.007 |
| Body at least 65% | 584 | 49.2% | -0.018 | -0.099 to +0.064 | -0.039 |
| Body at least 80% | 282 | 47.7% | -0.052 | -0.169 to +0.064 | -0.074 |
| Level held at least twice | 529 | 51.6% | +0.033 | -0.052 to +0.119 | +0.017 |
| Direction: closes rule | 486 | 51.0% | +0.016 | -0.072 to +0.105 | -0.013 |
| Direction: structure | 240 | 51.5% | +0.029 | -0.097 to +0.155 | +0.020 |
| Direction: daily background | 379 | 49.7% | -0.013 | -0.113 to +0.087 | -0.036 |
| Direction: all three agree | 121 | 48.8% | -0.025 | -0.204 to +0.154 | -0.025 |

## What the levels must beat

The same test on every convincing candle, whether or not it broke a level. If these lines do as well as the ones above, the levels are adding nothing.

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| No level at all: every convincing candle (body 50%) | 5562 | 49.5% | -0.011 | -0.038 to +0.015 | -0.035 |
| No level, with the closes rule | 2861 | 51.6% | +0.033 | -0.003 to +0.070 | +0.009 |

## Inside the base signals

The base signals cut different ways. This is where to look for weaknesses. Small groups swing widely by luck: read the signal count before the average.

### Buy and sell

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| buy | 441 | 48.8% | -0.015 | -0.109 to +0.079 | -0.052 |
| sell | 343 | 51.5% | +0.020 | -0.086 to +0.125 | +0.018 |

### Time of day

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| 00-03 New York (Asia) | 111 | 50.5% | +0.009 | -0.178 to +0.196 | -0.009 |
| 03-07 New York (London) | 121 | 43.3% | -0.138 | -0.314 to +0.039 | -0.171 |
| 07-12 New York (NY morning) | 235 | 55.4% | +0.119 | -0.011 to +0.248 | +0.101 |
| 12-17 New York (NY afternoon) | 110 | 43.4% | -0.138 | -0.319 to +0.044 | -0.145 |
| 17-24 New York (evening) | 207 | 50.7% | +0.014 | -0.122 to +0.151 | -0.014 |

### Closes rule at the signal

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| agrees | 486 | 51.0% | +0.016 | -0.072 to +0.105 | -0.013 |
| disagrees | 297 | 48.1% | -0.030 | -0.145 to +0.085 | -0.038 |
| no clear reading | 1 | 100.0% | +1.000 | +nan to +nan | +1.000 |

### Structure at the signal

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| agrees | 240 | 51.5% | +0.029 | -0.097 to +0.155 | +0.020 |
| disagrees | 217 | 47.2% | -0.040 | -0.176 to +0.096 | -0.050 |
| no clear reading | 327 | 50.8% | +0.006 | -0.102 to +0.114 | -0.033 |

### Daily background at the signal

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| agrees | 379 | 49.7% | -0.013 | -0.113 to +0.087 | -0.036 |
| disagrees | 391 | 49.9% | +0.009 | -0.091 to +0.109 | -0.012 |
| no clear reading | 14 | 61.5% | +0.107 | -0.457 to +0.672 | +0.105 |

### Share of the signal candle that is body

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| 50-65% | 200 | 52.3% | +0.051 | -0.086 to +0.189 | +0.030 |
| 65-80% | 302 | 50.7% | +0.015 | -0.099 to +0.129 | -0.006 |
| 80%+ | 282 | 47.7% | -0.052 | -0.169 to +0.064 | -0.074 |

### Times price had turned at the level

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| 1 | 255 | 46.6% | -0.069 | -0.192 to +0.054 | -0.101 |
| 2 | 222 | 49.3% | -0.022 | -0.153 to +0.108 | -0.034 |
| 3 or more | 307 | 53.3% | +0.074 | -0.039 to +0.186 | +0.053 |

### Half-year

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| 2024 second half | 136 | 50.8% | -0.012 | -0.179 to +0.155 | -0.032 |
| 2025 first half | 355 | 50.1% | +0.013 | -0.092 to +0.118 | +0.001 |
| 2025 second half | 293 | 49.5% | -0.009 | -0.124 to +0.105 | -0.044 |

## Breaks the base skipped

| Reason | Count |
|---|---|
| weak_candle | 239 |

Signals with no outcome (no entry minute, or the history ended first): 9.
