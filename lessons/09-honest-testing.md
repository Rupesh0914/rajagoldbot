# Lesson 9: Honest testing

This is the lesson that decides whether the bot is worth anything. Everything before it built
the bot. This one judges it, on prices it has never seen, by rules written down before looking.

## 1. Why most backtests lie

A backtest runs trading rules over old prices to see how they would have done. It is the most
useful tool a trader has, and the easiest to fool yourself with. There are four ways it lies.

**1. Hindsight.** The test uses something that was not known at the time. A level drawn after the
fact. A candle that had not closed yet. The result looks brilliant and cannot be repeated.

**2. Tuning to the past.** You try a setting, look at the result, change it, look again. Do that
enough and you find settings that fit the old prices perfectly, because you shaped them to. They
describe the past. They predict nothing.

**3. Ignoring costs.** The spread is small on any one trade and enormous over hundreds. A
strategy that makes a little before costs loses after them.

**4. Trying many things and keeping the best.** Test twenty ideas that are all worthless and one
of them will look good, by luck alone. If you only report that one, you are reporting luck.

## 2. How this bot was guarded against each

| The lie | The guard |
|---|---|
| Hindsight | The bot only acts on closed candles, and every piece has a test that its past answers never change when later prices arrive |
| Tuning | The price history was split in three **before** anyone looked at it. Ideas were tried on the first part only |
| Costs | Every test pays the spread, and is repeated with the spread doubled |
| Keeping the best | Every run is kept in `research/results`, including the bad ones. And the final judgement is made on data none of the runs touched |

There is one more guard, and it is the cleverest. Before each test was run on real prices, it
was run on **random** prices, where no rule can possibly work. That shows what "nothing" looks
like through that test. On random prices our trade test lost about the spread, and single runs
of a hundred trades swung from -0.27 R to +0.18 R by luck. A real result has to stand clear of
that.

## 3. The three parts of the history

We have about 25 months of your Eightcap gold prices.

```
|------ Development: 13 months ------|-- Validation: 6 --|--- Holdout: 6 ---|
  Oct 2024              Nov 2025                  May 2026          Nov 2026

  Open. Try, fix, try again.          Used once,           Used once,
                                      to choose.           for the verdict.
```

- **Development** is where the building happened. We ran four tests on it and learned a lot.
- **Validation** has never been loaded. It will be used once, to choose between four versions.
- **Holdout** will be used once, on the one version chosen. It gives the verdict.

Why two unseen parts and not one? Because choosing between versions is itself a look at the
data. If the same six months both picked the winner and judged it, the winner would be flattered.
So one part chooses and a separate part judges.

## 4. What the development runs taught us, and why they are not evidence

Four runs on the first 13 months (details in `research/results`):

- A level break on its own was a coin flip.
- Trading only in New York hours, and only with the 4-hour direction, is what made the
  difference.
- Taking profit early (the ladder, halves, near targets) cost most of the result. Holding to the
  stop or the end of the day did best.
- Level quality, the room rule, the daily background and stricter candles did not help.

These are real lessons, and none of them is proof. Every choice we made was made **on that
data**. Of course the chosen versions look good there: they were picked because they did. The
question is whether they still work on prices that had no say in choosing them.

## 5. The final test

The rules are in `research/PROTOCOL.md`. They were written and saved before any unseen price was
loaded, and the tool refuses to continue if that file is changed afterwards.

**The four versions:**

| # | Entry | Hours (New York) | Profit target |
|---|---|---|---|
| 1 | Any convincing candle | 07:00-16:00 | 2R |
| 2 | Any convincing candle | 07:00-16:00 | None |
| 3 | Any convincing candle | 07:00-13:00 | None |
| 4 | A level break only | 07:00-16:00 | None |

All four trade with the 4-hour direction, put the stop beyond the signal candle, risk 0.5%, take
one trade at a time, close at 16:50, and obey the spread limit and daily safety limits from
Lesson 8.

**Stage 1, validation.** The tool first proves it reproduces our earlier results exactly. Then
it runs all four versions on the validation months. The winner is the one with the highest
average R, among those with at least 100 trades and an average above zero. If none qualifies,
**the test stops and the holdout is never opened.**

**Stage 2, holdout.** The winner alone is run once on the holdout months.

## 6. The pass marks

These come from your own research notes, unchanged.

| Gate | It must show | In plain words |
|---|---|---|
| Sample | At least 100 trades | Enough trades to mean something |
| Economic | Profit factor at least 1.20, and average above 0 R | It makes clearly more than it loses, after costs |
| Risk | Largest fall at most 15% | The worst losing stretch was survivable |
| Robustness | Profit factor at least 1.05 with spreads doubled | It still works if costs are worse than expected |
| Uncertainty | The low end of the likely range is above 0 R | Luck alone is an unlikely explanation |

The terms:

- **R:** one unit of risk. Losing a trade at its stop is -1R (Lesson 6).
- **Average R:** all results added up, divided by the number of trades.
- **Profit factor:** everything won, divided by everything lost. 1.00 breaks even. 1.20 means 120
  won for every 100 lost.
- **Largest fall:** the biggest drop of the account from a high point, at 0.5% risk a trade.
- **Likely range:** if these trades are a fair sample, the true average probably lies in this
  range. If the range reaches below zero, "it was luck" has not been ruled out.

## 7. The five possible verdicts

| Verdict | Meaning | What happens next |
|---|---|---|
| **ROBUST PASS** | Every gate met | Onto the demo account, watched trade by trade |
| **PROVISIONAL** | It made money, survivably, even with doubled costs. But luck is not ruled out | Onto the demo account, with that warning attached |
| **FAIL** | It did not make enough, or fell too far, or broke under doubled costs | Not presented as a working strategy |
| **INCONCLUSIVE** | Fewer than 100 trades. No verdict either way | More data needed |
| **STOPPED AT VALIDATION** | Nothing qualified in stage 1 | The holdout stays unopened, for whatever is built next |

**In no case does anything go on a real-money account.** That is your decision and your action.

## 8. What a pass would and would not mean

A pass means: on six months of prices that had no part in shaping it, this bot made money after
costs. That is much stronger than anything we had before, and it is still modest.

- Six months is short. Markets change character.
- Gold rose through most of this history.
- Simulated fills are kinder than real ones.
- News was not excluded, because we have no calendar for the past.

So a pass means "not ruled out, worth watching on demo". A fail means "this version, in this
period, did not work". Neither is the end of the story, but only one of them earns the bot a
place on the demo account as a strategy.

## 9. The results

The test ran on 25 November 2026, each stage once. Full reports are in `research/results`, runs
005 and 006.

### Verdict: PROVISIONAL

**Stage 1, six unseen months, all four versions:**

| Version | Trades | Average R | Profit factor |
|---|---|---|---|
| 1: any convincing candle, target 2R | 329 | +0.058 | 1.11 |
| **2: any convincing candle, no target** | 251 | +0.071 | 1.11 |
| 3: the same, mornings only | 222 | +0.054 | 1.08 |
| 4: level break only | 80 | -0.137 | 0.78 |

Version 2 won by the rule.

**Stage 2, the last six months, version 2 only:**

| Gate | Needed | Got | |
|---|---|---|---|
| Sample | 100 trades | 239 | Met |
| Economic | Profit factor 1.20, average above 0 | 1.21, +0.132 R | Met |
| Risk | Largest fall at most 15% | 11.8% | Met |
| Robustness | 1.05 with spreads doubled | 1.16 | Met |
| Uncertainty | Low end of the range above 0 | -0.124 to +0.416 R | **Not met** |

Four gates of five. By the rules fixed in advance, that is PROVISIONAL: it made money on prices
it had never seen, survivably, even with doubled costs, and luck has not been ruled out.

### What to take from it

**The good part is real.** Across both unseen halves, 490 trades made +0.10 R each. Most trading
ideas, tested this strictly, lose. This one did not.

**The weak parts are just as real.**

- **One month made the whole second-half result.** November 2026 made +35 R. The other six months
  together lost 3.5 R.
- **The economic gate was passed by a hair:** 1.212 against a pass mark of 1.20.
- **It shrank from development,** exactly as section 4 warned: profit factor 1.33 where it was
  chosen, then 1.11 and 1.21 where it was not.
- **It loses about seven trades in ten.** A few long runs pay for many small losses. April and May
  2026 lost 13 R and 12 R back to back.
- **Buys and sells did not behave the same** from one period to the next.

**The version built on levels failed.** Version 4, the level break, lost money on unseen prices.
What survived is plainer than the strategy this project set out to build: a strong candle, in New
York hours, with the 4-hour direction, held to the stop or the end of the day. Three of Raja's
ideas carried it (the hours, the direction, letting a trade run). The level work did not, in the
mechanical form we gave it. That says something about our rules. It does not prove anything about
his trading, which leans on judgement we could not write down.

### What happens now

By the rules, a PROVISIONAL result goes onto the **demo** account, to be watched. A sensible bar:
at least three months and 100 trades before believing anything, with every month compared against
this test.

All 25 months of history are now used. There is nothing unseen left to test on. From here, the
only honest new evidence is what the bot does on the demo account.

One correction, recorded openly: the frozen rules say an earlier test of your first bot had used
this history from 21 August 2026. It was from about 19 July. It does not change this result, and
the rules file is left as it was frozen. The correction is in `research/results/README.md`.

## What the bot piece does

Two pieces.

`rajabot/engine.py` is the whole bot in one loop: every lesson's piece joined together. It is fed
prices one minute at a time and can only see what it has been given, so it cannot look ahead. It
was checked against the earlier research code, which was written separately: the two take
exactly the same trades. From Lesson 10, this same loop runs on the demo account.

`research/final_test.py` runs the two stages. It writes a lock after each one and refuses to run
it again. It will not open the holdout unless validation has chosen a winner, and not at all if
the rules file has changed.

## Check yourself

1. You test thirty ideas on the same year of prices. One makes 40%. Why is that not good news
   yet?
2. Why was the history split before anyone looked at it, and not after?
3. Our best version made +0.175 R a trade on the development part. Why is that not evidence that
   it works?
4. A strategy has a profit factor of 1.35 and an average of +0.2 R over 60 holdout trades. What
   is the verdict?
5. A strategy passes every gate except that its likely range runs from -0.03 R to +0.31 R. What
   is the verdict, and what does it mean?
6. In stage 1, no version reaches 100 trades with an average above zero. What happens to the
   holdout?
7. What is the point of running a test on random prices first?

<details>
<summary>Answers</summary>

1. With thirty tries, one looking that good by luck is likely. Until it is tested on prices it has
   not seen, you cannot tell skill from luck.
2. Because once you have looked, you cannot un-look. A split chosen afterwards could be placed,
   even without meaning to, where the results come out well.
3. Because it was chosen for doing well on that part. The winner of any contest looks good on the
   contest it won. It has to be judged on something else.
4. INCONCLUSIVE. Under 100 trades there is no verdict, however good the numbers look.
5. PROVISIONAL. It made money, survivably, even with doubled costs, but the range reaches below
   zero, so luck has not been ruled out.
6. Nothing. It is not opened. It stays unseen for whatever is built next.
7. To see what "no edge at all" looks like through that particular test, so a real result can be
   compared against it. It also proves the test gives away no free profit.

</details>

## Next

Lesson 10: connecting to MetaTrader 5 on the demo account.
