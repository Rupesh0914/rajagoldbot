# Lesson 1: Candles and timeframes

Everything else in this strategy is read off candles. Ten minutes here saves confusion in every
later lesson.

## 1. What a candle is

A candle is a summary of what price did during one stretch of time. It records four prices:

| Price | Meaning |
|---|---|
| **Open** | Where price was when the stretch began |
| **High** | The highest it reached |
| **Low** | The lowest it reached |
| **Close** | Where price was when the stretch ended |

```
        |      <- high (tip of the upper wick)
        |
      +---+    <- close  (on a rising candle)
      |   |
      |   |    <- the body: the distance between open and close
      |   |
      +---+    <- open
        |
        |      <- low (tip of the lower wick)
```

- **Body:** the thick part, between open and close. It shows who won.
- **Wicks:** the thin lines. They show where price went and was pushed back.
- **Bullish candle:** closed higher than it opened. Buyers won. Usually drawn green.
- **Bearish candle:** closed lower than it opened. Sellers won. Usually drawn red.

## 2. Reading one candle

Two candles can cover the same distance and mean opposite things.

**Mostly body.** Open 3750, high 3758, low 3748, close 3756. The candle is 10 dollars tall and
6 of that is body. Buyers pushed up and held most of it. Traders call this a conviction candle.

**Mostly wick.** Open 3756, high 3760, low 3740, close 3755. The candle is 20 dollars tall but
the body is only 1. Sellers drove price down 16 dollars and lost nearly all of it by the close.
This is rejection: the low was tested and refused.

This strategy asks for a candle that is at least half body when price breaks a level. A candle
that pokes through a level and closes as mostly wick has not broken anything. Lesson 4 turns this
into an exact rule.

A caution from our own tests: "more body is better" turned out not to be true. On 13 months of
gold, breakout candles that were almost all body did slightly worse afterwards than ordinary
ones. So the body rule is a minimum that screens out wick-heavy candles, and nothing more.

## 3. Timeframes

The timeframe is how long each candle lasts. The same price movement can be drawn as 1-minute,
30-minute or 4-hour candles. One 30-minute candle is thirty 1-minute candles squeezed into one.

This strategy starts with two timeframes, each for one job (Lesson 3 adds the daily chart as an
optional third):

| Timeframe | Job |
|---|---|
| **4-hour** | The big picture: is gold heading up or down? (Lesson 3) |
| **30-minute** | The decision: did a candle close through a level? (Lesson 4) |

Small timeframes are noisy. A move that looks dramatic on a 1-minute chart is often a single
wick on the 30-minute chart. Deciding on the 30-minute is meant to keep the bot out of that noise.

## 4. The rule that matters most: wait for the close

A candle that is still forming can look like a strong breakout at minute 20 and finish as a wick
at minute 30. Until it closes, it has told you nothing final.

So the rule, for you and for the bot: **only a closed candle counts.** Acting on a forming candle
is a common way to get caught in a fake breakout.

Raja does not always wait. In some videos he enters before the candle closes, and treats that as
the riskier choice. The bot always waits. The early entry is Lesson 14.

## 5. The broker's clock

MetaTrader shows candles in the broker's time, not yours. Many brokers, and Eightcap as far as
we have seen, run their clock 7 hours ahead of New York all year. Your first bot used the same
assumption and its replay matched its real trades. Lesson 10 checks it again against your
MetaTrader, because a broker that changes its clocks on European dates would be an hour off for
about three weeks a year. That makes the broker's midnight fall at 17:00 New
York time, which is when the gold market takes its daily one-hour break.

It matters for the 4-hour chart: the broker's 4-hour candles start at 17:00, 21:00, 01:00, 05:00,
09:00 and 13:00 New York time. The bot builds its 4-hour candles on that same clock, so it sees
the same candles you see on the chart.

## What the bot piece does

`rajabot/candles.py` does three things and decides nothing:

1. Takes 1-minute price bars and builds 30-minute candles and 4-hour candles from them.
2. Hands over **only closed candles**. The one still forming is held back.
3. Measures each candle: body, wicks, bullish or bearish, and what share of it is body.

Its tests check, among other things, that a finished candle never changes when later prices
arrive. That is the "no looking ahead" rule in its simplest form.

Try it with the two candles from section 2:

```
python -m rajabot candle 3750 3758 3748 3756
python -m rajabot candle 3756 3760 3740 3755
```

## Check yourself

1. A 30-minute candle opens at 3800, goes as high as 3812, as low as 3798, and closes at 3810.
   Bullish or bearish? How big is the body? How big is each wick?
2. Price is 5 dollars above a level with 10 minutes left in the 30-minute candle. Has the level
   been broken?
3. A candle is 20 dollars tall with a 2-dollar body and a long upper wick. Who won the candle,
   and what does the wick tell you?
4. Why does the bot decide on 30-minute candles instead of 1-minute candles?

<details>
<summary>Answers</summary>

1. Bullish. Body 10 (3800 to 3810). Upper wick 2 (3810 to 3812). Lower wick 2 (3798 to 3800).
2. Not yet. Only the close counts, and the candle has not closed.
3. Nobody clearly. Buyers pushed price up and sellers pushed it nearly all the way back. The
   long upper wick is rejection of the higher prices.
4. One-minute candles are mostly noise. A 30-minute close shows that price held beyond the level
   for a meaningful stretch.

</details>

## Next

Lesson 2: levels. How to mark the prices where gold has turned before, and how the bot finds
them without hindsight.
