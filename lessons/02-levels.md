# Lesson 2: Levels

Lesson 1 was about reading one candle. This lesson is about the map: the prices that matter.
Every trade in this strategy starts at a level.

## 1. What a level is

A level is a price where gold turned around before.

- Price climbed, hit a price, and fell away. That price is a **ceiling** (traders call it
  resistance).
- Price fell, hit a price, and bounced. That price is a **floor** (traders call it support).

Why it matters: many traders watch the same turning points. Orders pile up around them. So when
price comes back, something tends to happen there. Either it turns again, or it pushes through
with force. This strategy trades the second case: the push through. That is Lesson 4.

## 2. Swing highs and swing lows

"Where price turned" needs an exact definition, or two people will draw two different charts.

- A **swing high** is a candle whose high is above the highs of the candles on both sides of it.
  A peak.
- A **swing low** is a candle whose low is below the lows of the candles on both sides. A dip.

```
            high 3761
               |
           |   |   |
       |   |   |   |   |
       |   |       |   |
       |               |
     two candles     two candles
     before, lower   after, lower     ->  swing high at 3761 = a ceiling
```

How many candles on each side? That number is the **strength**.

| Strength | Meaning | Result |
|---|---|---|
| 2 | Higher than 2 candles each side | Many levels, including minor ones |
| 4 | Higher than 4 candles each side | Fewer, more obvious levels |
| 8 | Higher than 8 candles each side | Only the major turning points |

The bot's candidates are 2, 4 and 8. Which one it uses is not chosen by feel and not chosen by
what looks good on a chart. It is settled by the honest test in Lesson 9.

The level is the tip of the wick: the swing high's **high**, the swing low's **low**.

## 3. The trap: you only know a swing afterwards

This is the most important idea in this lesson.

Look at any finished chart and the swing highs are obvious. But at the moment a high is made,
nobody knows it is a swing high. The next candle might go higher. You only know once the candles
**after** it have closed lower.

So with strength 2 on 30-minute candles, a swing high is confirmed one hour after the candle
that made it closed. With strength 8, four hours after.

A level drawn on a finished chart looks like it was always there. It was not. Anyone who tests a
strategy using levels before they could have been known is cheating without realising it, and
the results will look far better than real trading ever will.

The bot stamps every level with the time it became usable, and never uses it before then.

## 4. When a level stops being a level

Two ways:

1. **It is broken.** A 30-minute candle **closes** beyond it: above a ceiling, or below a floor.
   A wick poking through does not count (Lesson 1: only the close counts). Once broken, the bot
   removes it for good.
2. **It is too old.** A level is dropped 7 days after it became usable, whether or not price
   came back to it. Old turning points matter less as the market moves on.

## 5. A line or a zone?

On a chart, traders often shade a level as a zone: a band a few dollars thick. That is honest,
because price rarely turns at the exact same cent twice.

The bot needs one exact number, so it uses the wick tip. Because only a candle **close** beyond
that price counts as a break, small pokes around the line are ignored anyway. The close rule
does the job the shaded zone does by eye.

## 6. How Raja describes it, and how that matches

Raja's own description of fresh support is simple: a down candle followed by an up candle. Price
was falling, then it turned. The low between those two candles is the support. Resistance is the
reverse: an up candle followed by a down candle, and the high between them.

That is the same idea as a swing low and a swing high. The swing rule in section 2 only adds an
exact test, so that the bot and you would mark the same price every time. A strength of 1 is
closest to his words. Higher strengths keep only the turns that held for longer.

He also says to look at the candles to the left: has price turned at this same area before? A
price that turned gold more than once deserves more respect than one that did it once.

## 7. Worked example

Ten 30-minute candles on a morning in New York. Strength 2.

| Candle | High | Low | Close | What happens |
|---|---|---|---|---|
| 08:00 | 3752 | 3746 | 3751 | |
| 08:30 | 3756 | 3750 | 3755 | |
| 09:00 | **3761** | 3754 | 3757 | Highest so far. Nobody knows yet that it is a swing high. |
| 09:30 | 3758 | 3751 | 3752 | Lower high. One candle after. |
| 10:00 | 3755 | 3747 | 3748 | Lower high again. At its close (10:30): **ceiling 3761 confirmed.** |
| 10:30 | 3750 | **3742** | 3746 | Lowest so far. |
| 11:00 | 3753 | 3745 | 3752 | Higher low. |
| 11:30 | 3757 | 3749 | 3756 | Higher low again. At its close (12:00): **floor 3742 confirmed.** |
| 12:00 | 3763 | 3755 | 3762 | **Closes above 3761. The ceiling is broken.** |
| 12:30 | 3766 | 3759 | 3765 | |

Things to notice:

- The 3761 high was made at 09:00 but was not a usable level until 10:30.
- The 12:00 candle broke the ceiling by closing at 3762. That break is exactly the kind of event
  Lesson 4 turns into an entry.
- At the end, one level is standing: the floor at 3742.

Watch the bot do the same thing:

```
python -m rajabot levels
```

Then try `python -m rajabot levels --strength 4` and see that the stricter setting keeps only
the floor.

## What the bot piece does

`rajabot/levels.py` keeps the list of levels, updated each time a 30-minute candle closes:

1. Drops levels older than 7 days.
2. Removes levels the candle closed through, and reports them as broken.
3. Adds any swing the candle just confirmed, stamped with the time it became usable.

It decides nothing. It only keeps the map current.

Its tests check that a level is never usable before the candles after it have closed, and that
what the bot knew at any moment never changes when later prices arrive.

## Check yourself

1. Strength is 2. A candle makes a high of 3800. The next two candles have highs of 3797 and
   3801. Is 3800 a swing high?
2. Strength is 4, on 30-minute candles. A swing high is made by the candle that opens at 10:00.
   What is the earliest time the bot can use it as a level?
3. There is a ceiling at 3761. A candle spikes to 3764 and closes at 3760. Is the ceiling
   broken?
4. Why is it cheating to test a strategy with levels marked on a finished chart?
5. A ceiling is broken at 12:30. An hour later price drops back below it. Does the bot treat it
   as a ceiling again?

<details>
<summary>Answers</summary>

1. No. The second candle after it went higher (3801), so 3800 was not a peak.
2. 12:30. The candle closes at 10:30, then four more candles must close: 11:00, 11:30, 12:00,
   12:30.
3. No. The wick went through, but the close (3760) is below 3761. Only a close beyond counts.
4. Because the levels were only known after later candles closed. Using them earlier gives the
   test information a real trader did not have at the time.
5. No. A broken level is removed for good.

</details>

## Next

Lesson 3: direction. How to read the 4-hour chart to decide whether the bot should be looking
for buys or for sells.
