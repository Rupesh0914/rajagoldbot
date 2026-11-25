# Run 002: signal check with combinations

Run on the owner's PC on 2026-11-25, code version `3dbf158`, point 0.01, 17 seconds. Same data
as run 001 (development part, 2024-10-23 to 2025-11-21; 382,953 one-minute bars; median spread
0.13; median unit 5.94; no-edge win share about 48.9%).

Every table that run 001 already had came out identical, as it must, and is not repeated here:
see [001-signal-check.md](001-signal-check.md). Below are the tables that are new in this run,
exactly as the tool wrote them. The reading is in [README.md](README.md).

---

## Combinations

Each piece was written down before any price was seen (session hours and the closes rule in the research notes, level quality in lesson 2). Compare each line with its no-level twin in the next table.

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| New York session only (07:00-16:00) | 339 | 51.5% | +0.031 | -0.076 to +0.139 | +0.018 |
| Session + closes rule | 217 | 54.2% | +0.076 | -0.056 to +0.209 | +0.056 |
| Session + level held at least twice | 220 | 51.7% | +0.038 | -0.096 to +0.171 | +0.026 |
| Session + closes rule + level held at least twice | 133 | 53.1% | +0.054 | -0.115 to +0.223 | +0.037 |

## Suggested by the first run (hindsight)

These were picked after seeing the first run's tables. A setting chosen because it looked good will look good again on the same data. Watch, do not trust.

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| Level held at least three times | 307 | 53.3% | +0.074 | -0.039 to +0.186 | +0.053 |
| Session + closes rule + level held at least three times | 66 | 51.6% | +0.016 | -0.224 to +0.256 | +0.012 |

## What the levels must beat

The same test on every convincing candle, whether or not it broke a level. If these lines do as well as the ones above, the levels are adding nothing.

| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |
|---|---|---|---|---|---|
| No level at all: every convincing candle (body 50%) | 5562 | 49.5% | -0.011 | -0.038 to +0.015 | -0.035 |
| No level, with the closes rule | 2861 | 51.6% | +0.033 | -0.003 to +0.070 | +0.009 |
| No level, New York session only | 2325 | 49.3% | -0.017 | -0.058 to +0.025 | -0.035 |
| No level, New York session + closes rule | 1242 | 53.2% | +0.063 | +0.008 to +0.119 | +0.046 |
