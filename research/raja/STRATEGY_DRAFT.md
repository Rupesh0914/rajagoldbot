# Strategy draft: the consolidation breakout, corrected

A corrected version of the owner's draft of 2026-11-26. Each line says where it comes from:
**Raja** (in the research notes), **Tested** (supported by our own tests on Eightcap gold), or
**Open** (not yet confirmed either way). Nothing here changes the PROVISIONAL bot. This is the
design for the next version, to be checked against his real trades before it is built.

## The timeframes

| Chart | Job | Source |
|---|---|---|
| 4-hour | Decide whether this is a BUY or a SELL environment | Raja, Tested |
| 30-minute | Find the consolidation and its support and resistance. The 30-minute close is the trigger | Raja (he acts on 30-minute or 1-hour) |
| 15-minute | Not used for now. Later: an optional earlier trigger, tested separately | Raja uses it sometimes and calls it riskier. Open |
| 5-minute | Not used | No basis in the notes |

## The trade, step by step

1. **Direction first.** The 4-hour chart says buy or sell. Only trades in that direction are
   taken. *(Raja, Tested)*
2. **Right hours only.** 07:00 to 16:00 New York time, Monday to Friday. *(Raja, Tested)*
3. **Find the consolidation.** Price moving sideways between a support and a resistance on the
   30-minute chart. No trade while price is inside it. *(Raja. How to recognise it is Open: this
   is the hard part and the part still to be built)*
4. **Wait for a 30-minute candle to close outside.** A wick through does not count.
   - Closes above the resistance: BUY setup.
   - Closes below the support: SELL setup.
   - Wicks through and closes back inside: nothing. *(Raja, and how our bot already works)*
5. **Enter at the open of the next candle.** Never during the breakout candle. *(How our bot
   already works)*
6. **Stop loss** just beyond the far end of the breakout candle: below its low for a buy, above
   its high for a sell. *(Raja, roughly. Exact placement Open until his charts are read)*
7. **Size** so that being stopped out costs 0.5% of the account. *(Our choice. Raja uses 1% to
   2%)*
8. **Exit:** hold until the stop is hit or 16:50 New York time, whichever comes first.
   *(Tested: this did best. See the note below)*

## Worked example

```
10:00-10:30   breakout candle
10:30         it closes above resistance, with the 4-hour chart pointing up
10:30         next candle opens: BUY
              stop just below the low of the 10:00-10:30 candle
10:30 on      hold
              EXIT when the stop is hit, or at 16:50
```

## What was changed from the draft, and why

| In the draft | Now | Why |
|---|---|---|
| 15-minute chart for the setup and the trigger | 30-minute | The notes say he acts on the 30-minute or 1-hour chart and rarely uses the 15-minute. The draft also mixed a 15-minute trigger with a 30-minute breakout candle |
| 5-minute chart to manage the trade by counting candles | Removed | Nothing in the notes supports it |
| Exit after exactly one 15-minute candle | Hold to the stop or 16:50 | In our tests, every step of holding longer did better: +0.045 R with a near target, +0.175 R with none. A 15-minute exit cuts every winner short and the spread takes a large share of so small a move |
| Target at the next opposing support or resistance | Kept as the alternative, not the default | This is what Raja does, with partial closes. In our tests it did worse than holding. His charts may show why |

## What is still open

1. **How to recognise a consolidation.** Not built, not tested. The owner's four marked
   screenshots and Raja's own charts are the reference for this.
2. **Whether a breakout from a consolidation beats any strong candle.** In our tests a break of
   a swing level added nothing. A consolidation is a different thing from a swing level, so that
   result does not settle this.
3. **His exact stop and target placement,** and what a pip means on gold in his videos.
4. **Any new version needs its own test on prices not yet used.** All 25 months of our Eightcap
   history are used up.
