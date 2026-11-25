# Research

Tools that run the bot's rules over saved price history. Nothing here places an order.

Read [DATA_SPLIT.md](DATA_SPLIT.md) first. These tools load only the development part of the
history. The rest stays unseen until Lesson 9.

## Signal check

The bot has no stop, target or position size yet (Lessons 5 to 7), so there is no profit backtest
yet. The signal check asks the one question that can be asked of the trigger alone:

> Enter on the minute after a signal. Which comes first: one unit our way, or one unit against?

One unit is the average height of the last 20 thirty-minute candles. A win is +1, a loss is -1.
The spread is paid on the way in and out. A signal still undecided after 24 hours is closed at
the price then. If one minute touches both sides, it counts as a loss.

```
python -m research.signal_check --bars PATH_TO\bars_m1.csv --out data\signal_check
```

It prints a report and saves `report.md` and `report.json` in the `--out` folder.

What it compares, one change at a time from a base setting: the swing strength, how much of the
candle must be body, level quality, and each direction reading. It also runs the same test on
**every convincing candle with no level at all**. If that does as well as the level breaks, the
levels are adding nothing.

### Zero point: what "no edge" looks like here

Measured on random-walk prices before any market price was loaded (260 days, spread 0.16, unit
about 2.96, so the spread is about 0.054 units):

| | Signals | Win share | Average (units) |
|---|---|---|---|
| Every convincing candle, no level | 4,389 | 46.8% | -0.064 |
| Base level breaks | 624 | 46.8% | -0.064 |
| Smaller groups (80 to 400 signals) | | 44% to 51% | -0.12 to +0.02 |

So with nothing to find, the check shows a win share of about 47% and a loss about the size of
the spread. Groups of a few hundred signals swing by several points either way from luck alone.
A real edge has to stand clear of that.

### How to read a result

- A win share above 50% with an average above zero, on a large group, is a clue worth following.
- Compare every line with the no-level line. Beating a coin flip is not enough if every strong
  candle does the same.
- Ten settings are compared. By luck alone, one of ten will often look good. A setting that
  looks best here still has to prove itself on the unseen parts in Lesson 9.
- This is the development part. Fixing a weakness found here and checking again is allowed, and
  is the point. It is not proof.

## Trade test

From Lesson 7 the bot can run a whole trade, so this test gives results in R. For every signal it
enters on the next minute, places the stop, sizes the trade, checks the room, picks the target
and manages the position minute by minute. One trade at a time. The spread is paid.

```
python -m research.trade_test --bars PATH_TO\bars_m1.csv --out data\trade_test
```

It compares, one change at a time from a base setup: the three exit styles (single target,
halves, and the quarters ladder from the Sugarwood bot), the room rule at 1.0, 1.5 and 2.0,
skipping open space, and dropping the hours and direction filters. Two benchmark lines trade
**every convincing candle with no level**, under the same hours, direction and stop. A
level-based setup that cannot beat them is not earning its complexity.

### Zero point: what "no edge" looks like here

Measured on six sets of random-walk prices (300 days each, spread 0.16) before the test was run
on any market price:

| | Trades (six runs) | Average R, pooled | Single runs, average R | Single runs, profit factor |
|---|---|---|---|---|
| Base setup, single target | 591 | -0.039 | -0.19 to +0.07 | 0.69 to 1.15 |
| Halves | 592 | -0.044 | -0.22 to +0.06 | 0.60 to 1.14 |
| Quarters ladder | 600 | -0.061 | -0.27 to +0.04 | 0.44 to 1.12 |
| Room at least 2.0 | 431 | +0.025 | -0.14 to +0.18 | 0.75 to 1.34 |
| Benchmark, target 2R | 3,080 | -0.072 | -0.16 to +0.03 | 0.75 to 1.06 |
| Benchmark, quarters | 3,947 | -0.061 | -0.13 to -0.01 | 0.68 to 0.97 |

What follows:

- **With nothing to find, it loses about the spread:** -0.04 to -0.07 R a trade on the large
  samples.
- **A hundred trades can show almost anything.** Single runs of about 100 trades ranged from
  -0.27 R to +0.18 R, and profit factors from 0.44 to 1.34, from luck alone. One run cleared the
  1.20 pass mark on pure noise.
- **The quarters ladder won about 60% of its trades on random prices.** A high win rate is what
  a ladder produces, not evidence of an edge.
