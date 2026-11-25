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
