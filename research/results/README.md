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
