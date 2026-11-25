# The final test: rules fixed in advance

**Frozen on 2026-11-25, before any price in the validation or holdout parts was loaded by this
bot.** The git commit that adds this file is the proof of when. The test tool records a
fingerprint of this file and refuses to run the second stage if the file has changed since the
first.

## 1. What is being tested

Four versions of the bot, carried forward from the development work (`results/README.md`, run
004). Nothing about them may change now.

| # | Entry | Hours (New York) | Profit target |
|---|---|---|---|
| 1 | Any convincing candle | 07:00-16:00 | 2R |
| 2 | Any convincing candle | 07:00-16:00 | None |
| 3 | Any convincing candle | 07:00-13:00 | None |
| 4 | A level break only | 07:00-16:00 | None |

Common to all four, exactly as built in lessons 1 to 8:

- **Convincing candle:** a closed 30-minute candle that closed in its own direction with at
  least 50% body. A bullish one is a buy, a bearish one a sell.
- **Level break (candidate 4):** such a candle that also closed through a swing level, strength 4.
- **Direction:** the 4-hour closes rule must agree (last closed 4-hour close against the close
  six candles earlier).
- **Hours:** the signal candle closes inside the hours shown, Monday to Friday.
- **Entry:** the open of the next minute, within five minutes. A buy pays the spread.
- **Stop:** one spread beyond the far end of the signal candle (a sell adds one more spread).
  No trade if the stop is more than 3 average candles away or less than 6 spreads away.
- **Size:** 0.5% of the account at risk.
- **Exit:** the target if there is one, the stop, or 16:50 New York. "None" means no target.
- **One trade at a time.**
- **Lesson 8 rules on:** no entry when the spread is above 0.50; no new trade after 5 trades,
  3R lost, or 3 losses in a row in a trading day.
- **Lesson 8 rules off:** news (there is no calendar for the past), sideways, rejection wick.

## 2. The data

Eightcap XAUUSD one-minute bars from the owner's MetaTrader, split as fixed in `DATA_SPLIT.md`.

| Part | From (UTC) | To (UTC) | Use here |
|---|---|---|---|
| Development | start | 2025-11-23 | Already used. Run again only as a check that the tool reproduces run 004 |
| Validation | 2025-11-23 | 2026-05-24 | **Stage 1.** All four candidates, once. Chooses the primary |
| Holdout | 2026-05-24 | end | **Stage 2.** The primary only, once. Gives the verdict |

Each stage also reads the 14 days before its part, so that candles, levels and the direction
exist on the first day. No trade is opened in those 14 days.

## 3. Stage 1: validation

1. **Check the tool first.** With the lesson 8 rules switched off, the tool must reproduce run
   004 on the development part exactly: candidate 1, 646 trades and +68.1 R; candidate 2, 499
   trades and +87.5 R; candidate 4, 152 trades and +22.6 R. If it does not, it stops and the
   validation part is not loaded.
2. Run all four candidates on the validation part.
3. **Choose the primary:** among candidates with **at least 100 trades** and an **average above
   0 R** on validation, the one with the highest average R. A tie goes to the lower number.
4. **If no candidate qualifies, the test stops here.** The outcome is "stopped at validation",
   the holdout is not opened, and it stays unseen for whatever is built next.

A candidate with fewer than 100 validation trades is reported and cannot be the primary.

## 4. Stage 2: holdout

The primary is run once on the holdout part. The same run is repeated with every spread doubled
(and the spread limit doubled with it, so the same trades are attempted).

Results are measured in R, with every trade sized on the same notional balance so that the order
of wins and losses does not change the sizes. A second replay on a 10,000 account with real lot
steps is shown for information and decides nothing.

## 5. Pass marks

These are the marks proposed in the owner's research notes, unchanged.

| Gate | Requirement |
|---|---|
| Sample | At least 100 closed trades on the holdout. Fewer: INCONCLUSIVE |
| Economic | Profit factor at least 1.20 **and** average above 0 R, after costs |
| Risk | Largest fall from a peak at most 15% of the account, at 0.5% risk a trade |
| Robustness | Profit factor at least 1.05 with spreads doubled |
| Uncertainty | The lower end of the 95% range for the average R is above 0 |

- The risk gate uses a cautious bound: before each trade it assumes that trade's whole risk is
  lost, and measures the fall from the highest balance so far.
- The 95% range is a bootstrap: 10,000 resamples of the trades, seed 1.
- Gates compare unrounded figures.

| Label | Meaning |
|---|---|
| STOPPED AT VALIDATION | No candidate qualified in stage 1. The holdout was not opened |
| INCONCLUSIVE | Fewer than 100 holdout trades. No verdict either way |
| FAIL | The economic, risk or robustness gate was not met |
| PROVISIONAL | Economic, risk and robustness met. The uncertainty gate was not |
| ROBUST PASS | Every gate met |

## 6. What each outcome leads to

- **ROBUST PASS or PROVISIONAL:** the primary goes onto the demo account in lesson 10, to be
  watched trade by trade against this test.
- **FAIL, INCONCLUSIVE or STOPPED:** the bot is not presented as a working strategy. Lessons 10
  and 11 can still connect it to the demo account, to learn the plumbing, labelled plainly as a
  strategy that did not pass.
- **In no case does anything go on a real-money account.** That is the owner's decision and the
  owner's action, by hand.

## 7. What may not happen

1. No setting changes after this file is committed.
2. Each stage runs once. The tool writes a lock file and refuses a second run. A rerun forced by
   a bug is reported with the bug and both results.
3. The holdout is not looked at, plotted or summarised in any other way, before or after.
4. The result is published as it comes out, whatever it says.

## 8. What had already been seen

- **Development part:** used four times to arrive at these candidates (runs 001 to 004). Its
  results are not evidence. They are why this test exists.
- **Holdout part, last three months (from 2026-08-21):** used in November 2026 to test a
  different strategy, the first bot's option-based levels. None of this bot's rules was run on
  it, and no result from that test shaped these candidates.
- **Validation part:** never loaded.

## 9. What a result can and cannot say

- It describes the past. It is not a forecast, and no label here is a promise.
- Six months is short. A pass means "not ruled out, worth watching on demo". It does not mean
  "proven".
- News was not excluded, because there is no calendar for the past. Live, the bot will stand
  aside around news, so it will take somewhat fewer trades than the test.
- Fills are simulated from one-minute bars. A stop fills at its price unless price jumped past
  it. Real stops slip more. The doubled-spread run is the allowance for that.
- The broker's clock is taken to be New York plus 7 hours all year. If Eightcap's differs for a
  few weeks a year, the 4-hour candles in those weeks are an hour out.
- Gold rose strongly over most of this history. The development runs showed buys and sells doing
  about equally well, which argues that the result is not only the trend. It does not prove it.
