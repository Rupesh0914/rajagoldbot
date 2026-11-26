# Run 005: final test, stage 1 (validation)

Run once on the owner's PC on 2026-11-25. Code version `eafc04f`, rules fingerprint
`01ec33dd426d62bc`, exit code 0, 89 seconds. The report below is exactly as the tool wrote it.
The reading is in [README.md](README.md).

---

# Final test, stage 1: validation

Rules: `research/PROTOCOL.md`, fingerprint `01ec33dd426d62bc`. Code version `eafc04f`.

**Validation part: 2025-11-23 to 2026-05-22.** One-minute bars in it: 174026. Median spread: 0.16. Nothing from the holdout part was loaded.

The tool check passed: it reproduces run 004 on the development part exactly.

## The four candidates on the validation part

| | Trades | Winners | Average R | 95% range | Profit factor | Total R | Largest fall | Profit factor, spread doubled |
|---|---|---|---|---|---|---|---|---|
| 1: any convincing candle, 07:00-16:00, target 2R | 329 | 39.8% | +0.058 | -0.082 to +0.200 | 1.11 | +19.0 | 15.2% | 1.09 |
| 2: any convincing candle, 07:00-16:00, no target | 251 | 32.3% | +0.071 | -0.147 to +0.308 | 1.11 | +17.9 | 14.4% | 1.08 |
| 3: any convincing candle, 07:00-13:00, no target | 222 | 30.6% | +0.054 | -0.187 to +0.314 | 1.08 | +12.0 | 13.3% | 1.05 |
| 4: level break only, 07:00-16:00, no target | 80 | 31.2% | -0.137 | -0.427 to +0.191 | 0.78 | -11.0 | 9.5% | 0.76 |

Largest fall is the cautious bound, at 0.5% risk a trade.

## The primary: candidate 2: any convincing candle, 07:00-16:00, no target

Chosen by the rule fixed in advance: at least 100 trades and an average above 0 R, then the highest average R. This is the only version that will be run on the holdout part.

### Candidate 1: any convincing candle, 07:00-16:00, target 2R

- Buys: 185 trades, -0.015 R each. Sells: 144 trades, +0.152 R each.
- How they ended: flat 82, stop 168, target 79.
- Median time in a trade: 69 minutes.

| Month | Total R |
|---|---|
| 2025-11 | -1.1 |
| 2025-12 | +6.3 |
| 2026-01 | +9.9 |
| 2026-02 | +7.9 |
| 2026-03 | +21.0 |
| 2026-04 | -13.3 |
| 2026-05 | -11.8 |

Months with a profit: 4 of 7.

Signals not traded: daily_loss_limit 13, losing_streak 2, outside_session 819, position_open 225, spread_too_wide 1, stop_too_wide 1, warm_up 28.

### Candidate 2: any convincing candle, 07:00-16:00, no target

- Buys: 149 trades, +0.028 R each. Sells: 102 trades, +0.135 R each.
- How they ended: flat 100, stop 151.
- Median time in a trade: 110 minutes.

| Month | Total R |
|---|---|
| 2025-11 | +2.0 |
| 2025-12 | +16.2 |
| 2026-01 | +9.0 |
| 2026-02 | -0.0 |
| 2026-03 | +16.1 |
| 2026-04 | -13.3 |
| 2026-05 | -12.1 |

Months with a profit: 4 of 7.

Signals not traded: daily_loss_limit 14, outside_session 819, position_open 305, stop_too_wide 1, warm_up 28.

### Candidate 3: any convincing candle, 07:00-13:00, no target

- Buys: 129 trades, -0.010 R each. Sells: 93 trades, +0.144 R each.
- How they ended: flat 79, stop 143.
- Median time in a trade: 108 minutes.

| Month | Total R |
|---|---|
| 2025-11 | +1.2 |
| 2025-12 | +15.9 |
| 2026-01 | +6.3 |
| 2026-02 | -0.8 |
| 2026-03 | +13.5 |
| 2026-04 | -11.1 |
| 2026-05 | -13.0 |

Months with a profit: 4 of 7.

Signals not traded: daily_loss_limit 2, outside_session 994, position_open 182, stop_too_wide 1, warm_up 17.

### Candidate 4: level break only, 07:00-16:00, no target

- Buys: 51 trades, -0.337 R each. Sells: 29 trades, +0.215 R each.
- How they ended: flat 33, stop 47.
- Median time in a trade: 105 minutes.

| Month | Total R |
|---|---|
| 2025-11 | +1.6 |
| 2025-12 | -4.4 |
| 2026-01 | -6.2 |
| 2026-02 | -5.5 |
| 2026-03 | +10.8 |
| 2026-04 | -4.8 |
| 2026-05 | -2.6 |

Months with a profit: 2 of 7.

Signals not traded: against_direction 150, outside_session 133, position_open 22, stop_too_wide 1, warm_up 7, weak_candle 107.

## For reference: the same four on the development part, as the bot will run

With the lesson 8 rules on (spread limit, daily limits). The development part was already used to choose these candidates, so this is not evidence.

| | Trades | Winners | Average R | 95% range | Profit factor | Total R | Largest fall | Profit factor, spread doubled |
|---|---|---|---|---|---|---|---|---|
| 1: any convincing candle, 07:00-16:00, target 2R | 634 | 45.0% | +0.116 | +0.021 to +0.213 | 1.23 | +73.5 | 5.8% | 1.19 |
| 2: any convincing candle, 07:00-16:00, no target | 487 | 37.8% | +0.190 | +0.025 to +0.363 | 1.33 | +92.5 | 8.2% | 1.26 |
| 3: any convincing candle, 07:00-13:00, no target | 425 | 36.5% | +0.203 | +0.020 to +0.399 | 1.34 | +86.2 | 7.6% | 1.26 |
| 4: level break only, 07:00-16:00, no target | 152 | 43.4% | +0.149 | -0.084 to +0.402 | 1.29 | +22.6 | 7.6% | 1.24 |
