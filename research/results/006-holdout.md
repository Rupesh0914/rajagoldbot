# Run 006: final test, stage 2 (holdout)

Run once on the owner's PC on 2026-11-25. Code version `eafc04f`, rules fingerprint
`01ec33dd426d62bc` (unchanged since stage 1), exit code 0, 12 seconds. The report below is
exactly as the tool wrote it. The reading is in [README.md](README.md).

---

# Final test, stage 2: holdout

Rules: `research/PROTOCOL.md`, fingerprint `01ec33dd426d62bc`. Code version `eafc04f`.

**Holdout part: 2026-05-24 to 2026-11-23.** One-minute bars in it: 178439. Median spread: 0.16.

**The primary, chosen on validation:** candidate 2: any convincing candle, 07:00-16:00, no target.

# Outcome: PROVISIONAL

Gates compare unrounded figures.

| Gate | Requirement | Measured | |
|---|---|---|---|
| Sample | at least 100 closed trades | 239 | met |
| Economic | profit factor >= 1.20 and average > 0 R | profit factor 1.2120, average +0.1321 R | met |
| Risk | largest fall <= 15% | 11.76% (cautious bound); 11.32% on closed trades | met |
| Robustness | profit factor >= 1.05 with spreads doubled | profit factor 1.1635 | met |
| Uncertainty | lower end of the 95% range > 0 R | -0.1238 to +0.4158 R | NOT met |

## The run

| | Trades | Winners | Average R | 95% range | Profit factor | Total R | Largest fall | Profit factor, spread doubled |
|---|---|---|---|---|---|---|---|---|
| Holdout | 239 | 30.1% | +0.132 | -0.124 to +0.416 | 1.21 | +31.6 | 11.8% | 1.16 |
| Holdout, spreads doubled | 238 | 29.4% | +0.102 | -0.150 to +0.377 | 1.16 | +24.2 | 12.1% |  |

- Buys: 112 trades, -0.264 R each. Sells: 127 trades, +0.482 R each.
- How they ended: flat 98, stop 141.
- Median time in a trade: 112 minutes.

| Month | Total R |
|---|---|
| 2026-05 | -3.2 |
| 2026-06 | -5.4 |
| 2026-07 | +0.1 |
| 2026-08 | +0.0 |
| 2026-09 | +2.6 |
| 2026-10 | +2.3 |
| 2026-11 | +35.1 |

Months with a profit: 5 of 7.

Signals not traded: daily_loss_limit 7, no_entry_minute 1, outside_session 861, position_open 316, stop_too_wide 13, warm_up 37.

## For information: a 10,000 account with real lot steps

Decides nothing. Sizes are rounded down to 0.01 lots and the balance compounds.

- Trades: 239. Final balance: 11569.34 from 10000.00.
- Smallest and largest trade: 0.01 to 0.14 lots.

## What this cannot say

- It describes six months of the past. It is not a forecast, and the label is not a promise.
- News was not excluded. Fills are simulated from one-minute bars; real stops slip more.
- Whatever the label, nothing here is a reason to trade real money.
