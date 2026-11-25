# Lesson 3: Direction

Lesson 2 gave us the map: the levels. This lesson answers the first question to ask of any
chart: which way is gold going? The answer decides whether the bot looks for buys or for sells.

## 1. Why direction comes first

A level can break upward or downward. Raja trades with the bigger direction: he decides which
way gold is going first, and then only takes trades that agree with it. The idea is that a move
going with the bigger picture has more behind it. Section 10 says what our tests made of that.

- Direction up: look for **buys** only (a ceiling breaking).
- Direction down: look for **sells** only (a floor breaking).
- Not clear: do nothing. No trade is a position too.

## 2. Top-down: big charts first

Raja Banks works from the big picture down to the small one. He says most of his trade
ideas come from the 4-hour chart, and he acts on the 1-hour or 30-minute chart.

| Chart | What it is for |
|---|---|
| Weekly, daily | The background. Is gold in a long climb, a long fall, or going sideways? Where are the major ceilings and floors? |
| **4-hour** | The trade idea. Which way are the recent candles heading? |
| 30-minute | The action. Did a candle close through a level? (Lesson 4) |

The mistake this prevents: a 30-minute chart can look like a strong rally while the 4-hour chart
shows it is only a small bounce inside a fall.

## 3. Reading direction by eye

On the 4-hour chart, look at the last several candles and ask three things:

1. **Are the candles stepping up or stepping down?** Each high and low higher than the last is
   up. Each high and low lower than the last is down. Overlapping candles going nowhere is
   sideways.
2. **Where are the candles closing?** Lesson 1: the close shows who won. Closes marching higher
   mean buyers are in control.
3. **Are there rejection wicks?** A long upper wick at a ceiling says higher prices were refused.
   A long lower wick at a floor says lower prices were refused. A wick against the move is an
   early warning that it may be tiring.

Then check the room: is a major daily or weekly level sitting just ahead? A move that is about
to run into a wall has less space. Lesson 5 is about room, though the bot only measures it
against its own 30-minute levels. Daily and weekly walls are for your eye for now.

## 4. The bot's exact version

"Stepping up" is a judgement. The bot needs a rule with no judgement in it. This is the one it
starts with:

> Take the close of the last **closed** 4-hour candle. Compare it with the close six 4-hour
> candles earlier.
> Higher: direction is **up**. Lower: direction is **down**. Equal, or not enough candles yet:
> **no trades**.

Six 4-hour candles are one trading day. So the rule asks one plain question: **is gold higher
or lower than it was a trading day ago?** (On a Monday that reaches back to Friday.)

Example. The last seven 4-hour closes, oldest first:

```
3700   3710   3705   3720   3730   3725   3740
 ^                                          ^
 six candles earlier                        last close
```

3740 is above 3700, so the direction is up and the bot looks for buys only. The dips in the
middle (3705, 3725) do not matter. Only the two ends are compared.

## 5. A second reading: structure

The rule above compares two prices and ignores everything between them. Your eye does more: it
sees the peaks and dips and whether they are stepping up or down. The bot can do that too, using
the swings from Lesson 2 on the 4-hour chart.

> Take the last two peaks (swing highs) and the last two dips (swing lows).
> Newer peak higher **and** newer dip higher: structure is **up**.
> Newer peak lower **and** newer dip lower: structure is **down**.
> Anything else: **mixed**. No trades.

```
                             peak 3731
       peak 3715                /\
          /\                   /  \
         /  \                 /    \
        /    \               /      dip 3712
       /      \             /
      /        \___________/
                dip 3697
```

Both peaks and both dips are stepping up, so structure is up. See it with:

```
python -m rajabot structure
```

A peak or dip counts only after the candles following it have closed, exactly as in Lesson 2. So
this reading is slower than the closes rule, but one big candle sways it less.

"Mixed" is useful. A higher peak with a lower dip is a market widening out with no clear
direction, which is the kind of market this strategy should leave alone.

## 6. A third reading: the daily background

The 4-hour chart can point up inside a week that is falling. To see the background, the bot asks
the same question one size bigger:

> Is the last closed **daily** candle higher or lower than the daily close five candles earlier?

Five daily candles are one trading week. So: **is gold higher or lower than a week ago?**

The daily candles are the broker's: each runs from 17:00 to 17:00 New York time, five a week.

## 7. Three readings, one decision

| Reading | Question it asks |
|---|---|
| Closes | Higher or lower than a day ago? |
| Structure | Are the peaks and dips stepping up or down? |
| Daily | Higher or lower than a week ago? |

When several readings are switched on, the bot trades only when **all of them agree**. Any
disagreement means no trade. More readings switched on means fewer trades. Whether it means
better ones is a question for the data, answered in section 10.

Which readings to switch on is not chosen by feel. Lesson 9 tests the combinations and keeps the
one that earns its place.

## 8. Be honest about these rules

- **Raja gives no formula.** He reads direction by eye. These rules are our stand-ins, and the
  numbers in them (six candles, five days, the last two peaks and dips, found with two candles
  each side) are our choices, not his.
- **They are late at turns.** After a long climb, gold can fall for hours before a rule flips to
  down. Every direction rule has this cost.
- **The closes rule flip-flops when gold goes sideways.** Up one candle, down the next. Sideways markets are
  where this strategy loses, and Lesson 8 adds rules for staying out of them.
- **They may not help.** Lesson 9 tests the bot with each reading on and off. One that does not
  earn its place goes.
- **They are still not an eye.** They catch the stepping pattern and the background. They do not
  see rejection wicks or a market going sideways yet. Those come in Lesson 8.

## 9. Still closed candles only

The 4-hour candle that is forming right now is not counted. Halfway through it, price can be far
above yesterday and still finish below. The bot waits for the 4-hour candle to close, the same
rule as Lesson 1.

The 4-hour candles are the ones on your broker's chart: they close at 21:00, 01:00, 05:00,
09:00, 13:00 and 17:00 New York time.

## 10. What our tests have said so far

Results on the first 13 months of your Eightcap history. Clues, not proof. Details are in
`research/results`.

- **The closes rule helped, a little.** Signals that agreed with it won 51.0%, signals against
  it 48.1%. With the New York hours added, the lift was clearer, and trades taken without the
  hours and direction filters lost money.
- **Structure pointed the same way**, about as weakly (51.5% agreeing, 47.2% against).
- **The daily background added nothing** (49.7% agreeing, 49.9% against).
- **All three together was no better** than the closes rule alone (48.8%, on few signals).

So the working setup uses the closes rule only. Structure and the daily background are built and
switched off.

One caution, and what came of it. Gold rose strongly through this whole period, so "trade with
the direction" might have been no more than "buy a rising market". That was checked: in the
working setup, buys made +0.111 R a trade and sells +0.098 R. Both sides worked about equally,
and the result was positive in each half-year. So it does not look like a buying bias alone.

## What the bot piece does

`rajabot/direction.py` gives three readings: the closes rule and the structure of the 4-hour
chart, and the daily background. It combines the ones that are switched on into a single answer,
and then answers the question the later lessons will ask: "is a buy allowed right now?" (only
when up) and "is a sell allowed?" (only when down).

Its tests check that a candle still forming never changes the answer, even if price spikes
inside it.

Try it with 4-hour closing prices, oldest first:

```
python -m rajabot direction 3700 3710 3705 3720 3730 3725 3740
python -m rajabot direction 3755 3760 3748 3752 3741 3738 3744
```

## Practice on a real chart

Open XAUUSD in MetaTrader on the 4-hour timeframe (H4). Find the last closed candle and count
six candles back. Compare the two closes and say the direction out loud. Then look at the chart
as a whole: do your eyes agree with the rule? Do this a few days in a row. The days your eyes
and the rule disagree are the ones to study.

## Check yourself

1. The last closed 4-hour candle closed at 3812. The 4-hour candle six earlier closed at 3835.
   What is the direction, and which trades may the bot look for?
2. The direction is down. A 30-minute candle closes strongly above a ceiling. Does the bot buy?
3. The current 4-hour candle is two hours old and far above every recent close. Does that change
   the direction?
4. Only five 4-hour candles of history are available. What does the bot do?
5. On which chart does Raja say most of his trade ideas come from, and on which does he act?
6. The last two 4-hour peaks were 3790 then 3805. The last two dips were 3770 then 3762. What is
   the structure?
7. The closes rule says up, structure says up, the daily background says down, and all three are
   switched on. Does the bot buy?

<details>
<summary>Answers</summary>

1. Down (3812 is below 3835). Sells only.
2. No. A buy needs the direction to be up. It skips the trade.
3. No. That candle has not closed. Only closed candles count.
4. Nothing. With fewer than seven closed candles the direction is unknown, so no trades.
5. Ideas from the 4-hour chart. Action on the 1-hour or 30-minute chart.
6. Mixed. The peak is higher but the dip is lower. No trades.
7. No. All the readings that are switched on must agree.

</details>

## Next

Lesson 4: the trigger. The exact moment the bot acts: a 30-minute candle closing through a
level, in the direction from this lesson.
