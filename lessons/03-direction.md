# Lesson 3: Direction

Lesson 2 gave us the map: the levels. This lesson answers the first question to ask of any
chart: which way is gold going? The answer decides whether the bot looks for buys or for sells.

## 1. Why direction comes first

A level can break upward or downward. Breaks that go with the bigger move tend to have more
behind them than breaks against it. So before looking at any level, decide the direction, and
then only take trades that agree with it.

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
to run into a wall has less space. That is Lesson 5.

## 4. The bot's exact version

"Stepping up" is a judgement. The bot needs a rule with no judgement in it. This is the one it
starts with:

> Take the close of the last **closed** 4-hour candle. Compare it with the close six 4-hour
> candles earlier.
> Higher: direction is **up**. Lower: direction is **down**. Equal, or not enough candles yet:
> **no trades**.

Six 4-hour candles are 24 hours of trading. So the rule asks one plain question: **is gold
higher or lower than it was a day ago?**

Example. The last seven 4-hour closes, oldest first:

```
3700   3710   3705   3720   3730   3725   3740
 ^                                          ^
 six candles earlier                        last close
```

3740 is above 3700, so the direction is up and the bot looks for buys only. The dips in the
middle (3705, 3725) do not matter. Only the two ends are compared.

## 5. Be honest about this rule

- **Raja gives no formula.** He reads direction by eye. The rule above is our stand-in, and the
  number six is our choice, not his.
- **It is late at turns.** After a long climb, gold can fall for hours before the rule flips to
  down. Every direction rule has this cost.
- **It flip-flops when gold goes sideways.** Up one candle, down the next. Sideways markets are
  where this strategy loses, and Lesson 8 adds rules for staying out of them.
- **It may not help.** Lesson 9 tests the bot with this filter on and with it off. If it does not
  earn its place, it goes.

## 6. Still closed candles only

The 4-hour candle that is forming right now is not counted. Halfway through it, price can be far
above yesterday and still finish below. The bot waits for the 4-hour candle to close, the same
rule as Lesson 1.

The 4-hour candles are the ones on your broker's chart: they close at 21:00, 01:00, 05:00,
09:00, 13:00 and 17:00 New York time.

## What the bot piece does

`rajabot/direction.py` takes the closed 4-hour candles and answers `up`, `down`, `flat` or
`unknown`. It also answers the question the later lessons will ask: "is a buy allowed right
now?" (only when up) and "is a sell allowed?" (only when down).

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

<details>
<summary>Answers</summary>

1. Down (3812 is below 3835). Sells only.
2. No. A buy needs the direction to be up. It skips the trade.
3. No. That candle has not closed. Only closed candles count.
4. Nothing. With fewer than seven closed candles the direction is unknown, so no trades.
5. Ideas from the 4-hour chart. Action on the 1-hour or 30-minute chart.

</details>

## Next

Lesson 4: the trigger. The exact moment the bot acts: a 30-minute candle closing through a
level, in the direction from this lesson.
