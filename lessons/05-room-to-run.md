# Lesson 5: Room to run

Lesson 4 ended with a signal: price closed through a level. This lesson asks the next question
before any money is risked: **is there anywhere for the trade to go?**

## 1. Why room matters

A ceiling breaks at 3761. Good. But there is another ceiling at 3766.

The trade has 4 dollars of space before it meets the next place where sellers are waiting. If
the idea is wrong, it loses 8. Risking 8 to make 4, with a wall in the way, is a bad trade even
when the break is real.

Raja checks this on every trade: before entering, he looks for clean space to the next obstacle.
If a nearby zone blocks the move, he skips it.

## 2. The three measurements

**The wall.** The next standing level in the way.

- For a buy: the nearest ceiling above the entry.
- For a sell: the nearest floor below the entry.

**The room.** The distance from the entry to the wall.

**The risk.** How far price has to go against you before the idea is proven wrong. For a break,
that is the far end of the signal candle: if price falls back below the low of the candle that
broke the ceiling, the break has failed. Lesson 6 puts the real stop there. For now it is the
yardstick.

```
   3775 ---------------  the wall (next ceiling)
                 ^
                 |  room = 13
                 v
   3762  [ ]  <- entry (the signal candle's close)
         [ ]     ^
         [ ]     |  risk = 8
         [ ]     v
   3754   |   <- the signal candle's low: below here the break has failed
```

## 3. The rule

> **Room divided by risk must be at least 1.**

In the picture: 13 divided by 8 is 1.62. There is more room than risk, so the trade passes.

Asking for at least as much room as risk is the loosest sensible rule. The candidates are 1.0,
1.5 and 2.0, from your research notes. A stricter number means fewer trades, each with more
space. Lesson 9 decides which one the bot uses.

## 4. Three examples

All three have the same signal: a candle closing at 3762 through the ceiling at 3761.

| | Next ceiling | Room | Risk | Room ÷ risk | Verdict |
|---|---|---|---|---|---|
| Room | 3775 | 13 | 8 | 1.62 | Passes |
| Tight | 3766 | 4 | 8 | 0.50 | Skipped: not enough room |
| Open | none | | 7 | | Passes: open space |

```
python -m rajabot room
python -m rajabot room --example tight
python -m rajabot room --example open
```

In the tight example (hand-made, like all the lesson examples), the candle after the signal
climbs to 3765 and stalls under the 3766 ceiling. That is what a wall looks like.

Try the stricter rule on the first example and watch it fail:

```
python -m rajabot room --min-ratio 2
```

## 5. Open space

Sometimes there is no level ahead at all. This is common when gold is at a price it has not
visited for a week or more, or at an all-time high. Nothing is in the way.

That sounds ideal, and it has a catch: with no wall, there is also no obvious place to take
profit. The bot treats open space as "enough room", and Lesson 7 deals with where to take profit
when there is no level to aim at.

The other view is that a trade with no target is not a plan, and should be skipped. The bot has
a switch for that view too:

```
python -m rajabot room --example open --no-open-space
```

Which is better is a question for Lesson 9.

## 6. Why the same level can be good for one trade and bad for another

Room is measured against risk, not in dollars. A wall 10 dollars away is plenty of room after a
small signal candle (risk 4), and not enough after a big one (risk 14).

A big signal candle means a far stop, and a far stop needs a lot of room to be worth taking.
The room rule handles that case by case, without banning big candles outright.

## 7. What this lesson is for, honestly

The checks in `research/results` found that breaking a level, by itself, did not predict where
gold went next. This lesson is the first place where levels do a second job: they mark where
the trade is likely to stall. If levels are worth anything to this bot, it is probably here and
in Lesson 6, where they place the stop and the target.

That is a claim to test, not a fact. Once Lesson 6 is built, the data check becomes a real trade
test and this rule is switched on and off like the others.

## 8. What Raja does differently

- **He measures by eye.** He talks about distances in pips for a particular chart on a
  particular day. He gives no fixed minimum. The ratio against risk is our way of writing down
  "enough for this trade".
- **He counts more things as walls.** A long wick, a round number, a level from the daily chart:
  all can be obstacles to him. The bot counts only its own swing levels on the 30-minute chart.
  Walls from the 4-hour and daily charts are a candidate to add later.

## What the bot piece does

`rajabot/space.py` takes a signal and the levels standing at that moment, and measures the wall,
the room and the risk. Then it answers: enough room, or not, with the reason.

Its tests check that the wall is always a level that was already known when the signal
happened, never one found later.

## Practice on a real chart

Take the three breaks you found in Lesson 4's exercise. For each one, mark the next level in the
way and measure the room. Then measure from the close of the breakout candle back to its far
end. Divide. Which of the three had room? What did price do when it reached the wall?

## Check yourself

1. A buy signal closes at 3800. The signal candle's low is 3794. The next ceiling is at 3810.
   What are the room, the risk and the ratio? Does it pass at 1.0? At 2.0?
2. A sell signal closes at 3740. The signal candle's high is 3750. The next floor below is at
   3734. Does it pass?
3. There is a floor at 3790, below a buy entry at 3800. Does it count as a wall for the buy?
4. Why is room measured against risk instead of as a fixed number of dollars?
5. Gold breaks a ceiling at an all-time high. There is no level above. What does the bot do?

<details>
<summary>Answers</summary>

1. Room 10 (3800 to 3810). Risk 6 (3800 back to 3794). Ratio 1.67. Passes at 1.0, fails at 2.0.
2. No. Room is 6 (3740 down to 3734), risk is 10 (3740 up to 3750), ratio 0.6.
3. No. For a buy the wall is the next ceiling **above** the entry. A floor below is behind the
   trade, not in its way.
4. Because what matters is whether the possible gain is worth the possible loss. Ten dollars of
   room is a lot for a trade risking 4 and too little for a trade risking 14.
5. It treats it as open space and counts that as enough room. Where to take profit is decided in
   Lesson 7. (With the "no open space" switch on, it would skip the trade.)

</details>

## Next

Lesson 6: the stop loss, costs, and how much to risk. Where exactly the stop goes, how many lots
to trade so a loss is a small fixed share of the account, and what the spread costs.
