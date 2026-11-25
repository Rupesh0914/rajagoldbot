# Lesson 8: When not to trade

Every lesson so far has been about finding a trade. This one is about refusing them. It matters
more than it sounds: in our tests so far, most of what worked came from **when the bot stays
out**, not from how it gets in.

## 1. "No trade" is a decision

A signal is not an order to trade. It is a question: "is this one worth taking?" Most of the
time the right answer is no.

The bot asks a fixed list of questions before every trade. If any one says no, it stays out and
writes down which one.

| # | Question | Switched on? |
|---|---|---|
| 1 | Is it the right time of day? | Yes |
| 2 | Is the spread normal? | Yes |
| 3 | Is scheduled news about to hit? | Yes, once it has a calendar |
| 4 | Is the market going sideways? | Built, switched off |
| 5 | Was the last 4-hour candle pushed back against this trade? | Built, switched off |
| 6 | Has today already gone badly enough? | Yes |

```
python -m rajabot gate
```

## 2. The time of day

Gold trades almost around the clock, but it does not behave the same all day. Raja concentrates
on the hours before and around the New York open, and your notes record that.

**The rule:** the signal candle must close between **07:00 and 16:00 New York time, Monday to
Friday.**

This is the rule our tests support most strongly (13 months of your Eightcap history; clues, not
proof):

- With no hours or direction filter, the bot **lost** money: -0.037 R a trade over 398 trades.
- With both filters on, the comparable setups came out positive.
- Inside the session, the morning carried it:

| Entered | Trades | Average R |
|---|---|---|
| 07:00 to 10:00 | 290 | +0.195 |
| 10:00 to 13:00 | 203 | +0.069 |
| 13:00 to 17:00 | 153 | -0.016 |

The afternoon added nothing. A shorter session, 07:00 to 13:00, is one of the candidates Lesson 9
will judge. It is not adopted yet, because it was noticed in the same data it would be tested
on, and a rule found that way always looks better than it is.

## 3. The spread

The spread is the broker's fee (Lesson 6). Usually it is about 13 cents on gold. At certain
moments it jumps: around the daily break at 17:00, in the first minutes of the week, and around
news. It can reach a dollar or more.

A wide spread costs you twice. You pay more to get in, and your stop is effectively closer,
because price has less distance to travel to hit it.

**The rule:** no new trade when the spread is above **0.50 dollars**. That number is our choice:
roughly four times normal.

## 4. Scheduled news

Some economic reports move gold violently, at a time known in advance. The main ones:

| Report | Usually when (New York time) |
|---|---|
| US jobs report (NFP) | First Friday of the month, 08:30 |
| US inflation (CPI) | Mid-month, 08:30 |
| Federal Reserve rate decision (FOMC) | Eight times a year, 14:00 |

In the minutes around these, the spread widens, price jumps past stops, and a candle can travel
further in one minute than it normally does in an hour. A stop loss does not protect you from a
jump: it fills wherever price lands (Lesson 6).

**The rule:** no new trade from **30 minutes before to 30 minutes after** a listed news item.
Thirty minutes is our choice.

Three honest points:

- **The bot needs a calendar.** It reads a simple file of dates and times. Lesson 10 fills it
  from MetaTrader's own economic calendar. Until then the rule has nothing to work from.
- **Our tests did not exclude news.** We had no calendar for the past, so every result so far
  includes trades taken around news. The rule is here for safety, not because we measured it.
- **Raja does trade some news.** His jobs-report tactic is Lesson 16. It is taught, and it is not
  something this bot will do.

## 5. Sideways markets

Raja is clear about this one: do not force trades when price is going nowhere. In a sideways
market, candles overlap, levels break and immediately fail, and a breakout strategy gets chopped
up.

**By eye:** the last several candles overlap each other. Highs and lows are not stepping in
either direction. Price ends the morning about where it began.

**The bot's measure: progress.** Over the last 12 thirty-minute candles (six hours):

> progress = how far price actually got ÷ how far it travelled to get there

```
3750 -> 3754 -> 3758 -> 3762 -> 3766      got 16, travelled 16:  progress 1.00
3750 -> 3756 -> 3751 -> 3757 -> 3750 -> 3755 -> 3751
                                          got 1, travelled 33:   progress 0.03
```

Under 0.20 counts as sideways.

```
python -m rajabot progress 3750 3754 3758 3762 3766
python -m rajabot progress 3750 3756 3751 3757 3750 3755 3751
```

**This rule is built and switched off.** It has not been tested, deliberately. We have already
looked at the same 13 months four times, and each extra look makes the results less trustworthy
(see `research/results`). Twelve candles and 0.20 are our guesses. It will be judged later, on
the bot's own demo record, which is data none of these rules were shaped on.

Lesson 3's "mixed" structure reading is a second, slower sign of the same thing.

## 6. A rejection wick against the trade

From Lesson 1: a long wick shows where price went and was pushed back. If the last closed 4-hour
candle has a long **upper** wick, higher prices were just refused, and buying straight into them
is questionable. The mirror applies to sells.

**The bot's measure:** the wick is at least twice the body, and is the longer of the two wicks.

**Also built and switched off,** for the same reason as section 5. The "twice" comes from the
candidates in your research notes (1.5, 2 or 3).

## 7. The daily safety limits

These are different from everything above. They are not about finding better trades. They exist
so that one bad day cannot do serious damage, whatever the cause: a market the rules do not suit,
a broker problem, or a mistake in the bot itself.

| Limit | Value | What it stops |
|---|---|---|
| Most trades in a day | 5 | Overtrading in a choppy market |
| Most lost in a day | 3R (1.5% of the account at 0.5% risk) | A bad day becoming a terrible one |
| Losses in a row | 3 | Carrying on when today's market clearly is not working |

When any limit is reached, the bot takes no new trades until the next trading day. A trading day
runs from 17:00 to 17:00 New York time, the same as the broker's daily candle.

A trade that is already open is left alone. The limits stop new entries, they do not close
anything.

Do the limits cost profit? The test of your first bot (run on your PC on 25 November 2026)
suggests not: with its limits switched off it took 287 extra trades, and all of them together
made about 27 dollars, against 2,432 from the 408 trades inside the limits. Trading on after a
bad start added risk and nothing else.

The three values are our choices, taken from your first bot.

## 8. Why the order matters, and why every "no" is written down

The questions are asked in the order of the table in section 1. The first "no" is the reason
recorded.

The record matters for two reasons:

- You can ask the bot afterwards: "why didn't you take the 14:30 signal?" and get an answer.
- If one reason is blocking nearly everything, something is wrong and it shows up at once. Your
  first bot once looked broken when it was only outside its trading hours.

## 9. What Raja does differently

- **He judges sideways by eye.** He gives no measure. "Progress" is ours.
- **He prepares for the day's news** and decides case by case. The bot has one blunt rule.
- **He prefers the active hours** before and around the New York open. The notes do not give his
  exact hours. 07:00 to 16:00 is ours.
- **Daily limits are not from Raja at all.** They are standard risk practice, and they were in
  your first bot.

## What the bot piece does

`rajabot/filters.py` holds each rule and one "gate" that asks them all in order. It is given the
moment of the signal, the side, the current spread and the recent candles, and answers either
"go ahead" or the first reason to stay out. It also keeps the day's tally of trades and results
for the safety limits.

## Check yourself

1. A clean buy signal closes at 06:30 New York time on a Wednesday. Does the bot trade?
2. It is 10:15 on a Tuesday, everything looks fine, and the spread is 0.70. What happens?
3. The US jobs report is at 08:30. Signals arrive at 07:55, 08:10 and 09:05. Which can be
   traded?
4. Over six hours price went from 3800 to 3803, moving 60 dollars in total along the way. What is
   the progress, and what does it mean?
5. Today the bot has lost three trades in a row, each -1R. It is 11:00 and a strong signal
   appears. What does it do, and when can it trade again?
6. The bot is in a trade when the daily loss limit is reached by an earlier trade's result. Is
   the open trade closed?
7. Why is the sideways rule switched off, when Raja says so clearly to avoid sideways markets?

<details>
<summary>Answers</summary>

1. No. It is before 07:00: "outside session".
2. No trade: "spread too wide". The limit is 0.50.
3. 07:55 and 09:05. The blocked window runs from 08:00 to 09:00, so 08:10 falls inside it. 07:55
   is five minutes before it starts and 09:05 is five minutes after it ends.
4. 3 divided by 60 is 0.05. Price travelled a long way and got almost nowhere: sideways.
5. Nothing. Three losses in a row stops the day (and so does being down 3R). It can trade again
   when the next trading day starts, at 17:00 New York time, though in practice at 07:00 the next
   morning when the session opens.
6. No. The limits only stop new trades. An open trade runs to its stop or to 16:50.
7. Because our version of it (12 candles, under 0.20) is a guess that has not been tested, and we
   have stopped testing on the 13 months we already looked at four times. The idea is Raja's. The
   numbers are ours, and they have to earn their place on new data.

</details>

## Next

Lesson 9: honest testing. The four candidates are run on the twelve months of prices none of
these rules have seen, with the pass marks fixed in advance.
