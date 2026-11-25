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
