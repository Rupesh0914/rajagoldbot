# Results log

Every check that is run is kept here, with the reading of it, including the ones that came out
badly. All of it is on the development part of the history only
([DATA_SPLIT.md](../DATA_SPLIT.md)). A result here is a clue, never proof.

## Run 001, 2026-11-25: the trigger on its own

Report: [001-signal-check.md](001-signal-check.md). Code `6b833ac`.

**The finding: the trigger on its own is a coin flip.**

- Base trigger: 784 signals, 50.0% wins, average +0.000 units. With no edge at all the win share
  would be about 48.9% (the spread), so this is one point above nothing, well inside the noise.
- **The levels are not adding anything yet.** Every convincing candle, with no level at all, did
  49.5%. With the closes rule and no level it did 51.6% on 2,861 signals, as well as any level
  setting.
- No line in the report is clear of zero. Every "likely range" includes it.

**Clues, each small and inside the noise:**

| Clue | Numbers | Reading |
|---|---|---|
| Level quality | 1 turn 46.6%, 2 turns 49.3%, 3 or more 53.3% | The only cut that steps the same way all through. On random prices the same cut was flat (46.6, 47.1, 46.7), so it is not built in by the method |
| Time of day | New York morning 55.4% (235 signals). London 43.3%, New York afternoon 43.4% | Fits the notes, which prefer the hours before and around the New York open. Groups are small |
| Direction | Closes rule agrees 51.0%, disagrees 48.1%. Structure agrees 51.5%, disagrees 47.2% | Points the right way, weakly |
| Daily background | Agrees 49.7%, disagrees 49.9% | Nothing |
| All three readings | 48.8% on 121 signals | Nothing, and few signals |
| Candle body | 50-65% body 52.3%, 65-80% 50.7%, over 80% 47.7% | **Against** what lesson 4 assumed. The fuller the breakout candle, the worse the follow-through. A very full candle may mean the move is already spent by the close |
| Buy and sell, half-years | All near 50% | No one side or period carrying it |

**What this does not say.** It does not say the strategy cannot work. The test is symmetric: one
unit up against one unit down. The strategy in the notes is not symmetric: the stop goes behind
the signal candle and the target is the next level, taken only when there is room (lessons 5 and
6). Its edge, if it has one, may come from choosing where there is room, not from calling
direction. That cannot be measured until those pieces exist.

**What it does say.** Breaking a swing level, by itself, does not predict follow-through on gold
in this period. The pieces that select *which* breaks to take have to carry the edge, or there
is none.

**Decisions taken from this run**

1. The body rule stays at "at least 50%" and is not tightened. The 65% and 80% candidates look
   worse, not better. The final choice is still made in lesson 9.
2. Run 002 adds combinations of pieces that were all written down before any price was seen:
   session hours (07:00 to 16:00 New York, from the notes), the closes rule, and level quality.
3. "Held at least three times" is added as a watched line only. It was picked by looking at this
   run, which is hindsight.
4. Lesson 5 (room to run) and lesson 6 (stop and target) are the next real test of the idea, and
   the check will be extended to use them.

## Run 002, 2026-11-25: combinations

Report: [002-signal-check.md](002-signal-check.md). Code `3dbf158`.

**The finding: when and which way matter. The level break still does not.**

| | Signals | Wins | Average (units) |
|---|---|---|---|
| Base trigger (run 001) | 784 | 50.0% | +0.000 |
| Trigger, New York session + closes rule | 217 | 54.2% | +0.076 |
| **No level**, New York session + closes rule | 1,242 | 53.2% | +0.063 |

- Adding session hours and the 4-hour direction lifted the trigger from 50.0% to 54.2%.
- **The same two filters with no level at all did 53.2%, on six times as many signals.** That
  no-level line is the only one in either report whose likely range clears zero (+0.008 to
  +0.119), and only just.
- So the lift comes from *when* (New York hours) and *which way* (with the 4-hour direction).
  One point of it, at most, comes from the level, and one point on 217 signals is noise.
- Level quality added nothing on top: session + closes + held twice did 53.1%.

**The hindsight pick fell apart, as hindsight picks do.** "Held at least three times" looked
best in run 001 (53.3%). Combined with the session and the closes rule it dropped to 51.6% on 66
signals. Nothing was built on it.

**How big is this, if it is real?** +0.063 units on a 1-to-1 bet is a profit factor of about
1.14. That is thin, and under the 1.20 pass mark that lesson 9 will use. It is a clue worth
following, not a result.

**A caution on the direction result.** Gold rose strongly through this whole period. "Trade
with the 4-hour direction" may partly be "gold kept going up". The base signals show buys at
48.8% and sells at 51.5%, so it is not simply a buying bias, but the session + direction line
has not been split by side yet. The next check does that.

**What the bot must now beat.** "Any convincing candle, in New York hours, with the 4-hour
direction" becomes the standing benchmark. A level-based rule that cannot beat it is not earning
its complexity.

**Decisions taken from this run**

1. Session hours (07:00 to 16:00 New York) and the closes rule go into the bot's working
   candidate. Both were in the notes before any data, and both moved the result the right way.
2. Level quality stays an option, switched off. It did not add to the combination.
3. The level break is kept, unproven. In the notes its job is not only to predict direction: it
   gives the stop (behind the signal candle) and the target (the next level), and a trade is
   taken only when there is room between them. Lessons 5 and 6 build that, and the check then
   becomes a real trade test in R, with the benchmark above run the same way.
4. The body result from run 001 (fuller candles do worse) points at entering late. The notes have
   an answer to that: wait for price to come back to the broken level and enter there (the
   retest, lesson 12). It will be tested beside the immediate entry once stops and targets exist.

## Run 003, 2026-11-25: the first trade test

Report: [003-trade-test.md](003-trade-test.md). Code `785fd71`. Whole trades, results in R.

**The finding: the simplest version did best, and the parts built on levels did not earn their
place.**

| | Trades | Winners | Average R | Profit factor | Total R |
|---|---|---|---|---|---|
| Base: level break, room rule, target at the next level | 115 | 46.1% | +0.083 | 1.17 | +9.5 |
| Level as trigger only, target always 2R | 163 | 47.9% | +0.140 | 1.30 | +22.8 |
| **Benchmark: any convincing candle, no level, target 2R** | 646 | 44.4% | +0.105 | 1.21 | +68.1 |
| Benchmark with the quarters ladder | 838 | 63.7% | +0.019 | 1.06 | +16.0 |
| Base with no hours or direction filter | 398 | 34.9% | -0.037 | 0.94 | -14.7 |

**1. The benchmark is the only line clear of zero.** Any convincing candle, in New York hours,
with the 4-hour direction, stop behind the candle, target 2R: +0.105 R a trade over 646 trades,
likely range +0.010 to +0.201, and still +0.083 with the spread doubled. On random prices the
same setup lost 0.07 R a trade and never did better than +0.03 in six runs, so this is outside
what luck alone produced there.

**2. Levels still do not earn their place.** The level-break setups made a similar amount per
trade (+0.083 to +0.140) on a quarter of the trades or fewer, and none is clear of zero. In
total R the no-level benchmark made three to seven times as much.

**3. Using the next level as the target, and the room rule, made things worse, not better.**
Aiming at the next level with a room rule: +0.083. Ignoring levels ahead and always aiming at
2R: +0.140. Tightening the room rule to 1.5 or 2.0 lowered the result further. Lesson 5's idea
that levels mark where a trade will stall is not supported here.

**4. The quarters ladder costs most of the edge.** On the large sample it raised the share of
winners from 44% to 64% and cut the average from +0.105 R to +0.019 R, and to below zero with
the spread doubled. Of 838 ladder trades, 332 banked nothing and only 74 reached the last step.
On the 115-trade base the three styles cannot be told apart, which is why the large sample
matters. Halves was the weakest of the three there (+0.025).

**5. The filters are doing the work.** With no hours or direction filter the base setup lost
(-0.037 R, profit factor 0.94). This matches runs 001 and 002.

**Weaknesses this run shows**

| Weakness | Evidence | Status |
|---|---|---|
| The afternoon loses | Base trades entered 13:00 to 17:00 New York: -0.211 R on 32 trades. Run 001 saw the same hours do worst | Same data both times, so not independent. A lead |
| It fades through the period | Base: +0.516 R in late 2024, +0.060 in early 2025, -0.072 in late 2025 | Small groups. Needs the same cut on the large benchmark sample |
| Many trades run out of day | 39 of 115 base trades were closed at 16:50, averaging +0.370 R. The targets may be further than a day's move allows | To be tested: nearer and further targets, and no target |
| Most of the result may be the trend | Gold rose strongly all period. "With the 4-hour direction" may largely be "long gold" | Base sells did +0.151 on 39 trades, which argues against, weakly. Needs the benchmark split by side |
| Still thin | Profit factor 1.21 on the data it was chosen on, against a 1.20 pass mark on unseen data | The best of eleven setups always looks better than it is |

**Decisions taken from this run**

1. **The benchmark becomes the working candidate.** It is simpler, has six times the trades and
   is the only setup clear of zero. The level break stays in the code as an option under test.
2. **The quarters ladder is not adopted.** A single target is the working exit. The ladder stays
   in the code, and lesson 7 keeps it as a taught comparison.
3. **The room rule and level targets stay switched off** in the working candidate. Lesson 5 is
   corrected to say what the data showed.
4. **Run 004 investigates the weaknesses** on the large sample: the benchmark split by side,
   half-year and time of day, whether a level break adds anything to a benchmark trade, and
   targets at 1R, 1.5R, 2R, 3R and none.

## Run 004, 2026-11-25: investigating the weaknesses

Report: [004-trade-test.md](004-trade-test.md). Code `9277b60`. Each weakness from run 003,
tested on the large benchmark sample (646 trades).

| Weakness from run 003 | What run 004 found | Verdict |
|---|---|---|
| Most of it may be the trend | Buys +0.111 R on 359 trades. Sells +0.098 R on 287 | **Not supported.** Both sides made about the same, in a market that rose all period |
| It fades through the period | +0.199 R in late 2024, +0.075 in early 2025, +0.103 in late 2025 | **Not supported on the large sample.** Positive in all three. The fade in run 003 was a small-group effect |
| Many trades run out of day | See the next table | **Confirmed, and it points the other way from what was feared:** the trades still open at 16:50 are the good ones |
| The afternoon loses | 07:00-10:00 +0.195 R. 10:00-13:00 +0.069. 13:00-17:00 -0.016 | **Partly.** The afternoon adds nothing. It does not lose much either |
| Levels do not earn their place | See below | **Reopened.** One cut says they may |

**Where to take profit: the further away, the better, all the way.**

| Target | Trades | Winners | Average R | Profit factor | Spread doubled |
|---|---|---|---|---|---|
| 1R | 855 | 51.9% | +0.045 | 1.11 | +0.030 |
| 1.5R | 713 | 46.8% | +0.091 | 1.19 | +0.062 |
| 2R | 646 | 44.4% | +0.105 | 1.21 | +0.083 |
| 3R | 582 | 40.5% | +0.133 | 1.25 | +0.101 |
| None: stop or end of day | 499 | 37.3% | +0.175 | 1.30 | +0.134 |
| Halves at 2R | 687 | 53.0% | +0.058 | 1.14 | +0.034 |

Five steps, and each one further out did better than the last. That is harder to put down to
luck than one good number would be. It also fits everything before it: the quarters ladder and
halves, which take profit early, were the two worst exits. The cost is fewer winners (37%) and a
larger worst drop (15.9 R against 12.5).

**Do levels add anything? One cut says yes.** Inside the benchmark's own trades:

| | Trades | Winners | Average R | Profit factor |
|---|---|---|---|---|
| Signal candle also broke a level | 99 | 52.5% | +0.307 | 1.72 |
| No level broken | 547 | 43.0% | +0.069 | 1.13 |

This question was written down before the run. The gap is large, and the level group is clear of
zero on its own. It is also 99 trades, and the gap between the two groups is about 1.7 times its
own uncertainty: suggestive, not settled.

It does not square neatly with the "level as trigger only" setup, which trades level breaks alone
and made +0.140 R on 163 trades. The difference is which breaks are taken. The benchmark takes
one trade at a time, so its 99 are level breaks that came while it had no trade open. The other
64 or so came while an earlier trade was still running, and work out at about -0.12 R. So it may
be that a level break is worth taking when it starts a move, and not when it comes late in one.
That reading was made after seeing the numbers. It is a lead to test, not a result.

**The hindsight lines did what hindsight lines do.** Entries 07:00 to 13:00 only: +0.141 R
against +0.105. Better, and chosen because it would be. It goes forward as a candidate to be
judged on unseen data, not as a finding.

**Decisions taken from this run**

1. **The working exit becomes "no target": hold to the stop or 16:50.** Supported by a steady
   trend across five target distances and by every earlier exit comparison.
2. **The working setup stays the benchmark**, 07:00 to 16:00, with the 4-hour direction.
3. **Levels are back in question, in a good way.** Swing levels stay in the bot. "Take level
   breaks only when no trade is open" becomes a candidate.
4. **Exploring on this data stops here.** Four runs have now looked at the same 13 months. Every
   further look makes the next result less trustworthy. The candidates below go to lesson 9,
   where the 6 unseen validation months choose between them and the 6 holdout months judge the
   winner once.

**Candidates carried forward to lesson 9**

| # | Entry | Hours | Exit |
|---|---|---|---|
| 1 | Any convincing candle, with the 4-hour direction | 07:00-16:00 | Target 2R |
| 2 | Same | 07:00-16:00 | No target |
| 3 | Same | 07:00-13:00 | No target |
| 4 | Level break only, with the 4-hour direction | 07:00-16:00 | No target |

All use the stop beyond the signal candle, 0.5% risk, one trade at a time, flat at 16:50.
