# Corrections to the lessons

On 2026-11-25 lessons 1 to 7 were checked line by line by an independent reviewer: every sum,
every command, every statement about what the bot does, every statement about what Raja does,
and every claim that our own test results now contradict. This page records what was wrong and
what was changed, so nothing is corrected silently.

## What was checked and found right

- **Every "check yourself" answer** in all seven lessons.
- **Every command** shown in a lesson runs and prints what the lesson says.
- **The worked sums:** lot sizes, rounding down, the Canadian-dollar example, the ladder splits.
- **The clocks:** 4-hour candle times, daily candles running 17:00 to 17:00 New York, the 16:50
  close moving correctly with daylight saving.
- **What the bot does with levels:** when a level becomes usable, the order of updates, a broken
  level never coming back.
- **The trigger:** the order of the checks, the furthest level being the signal level.
- **Buy and sell handled as mirror images,** with the spread on the correct side each time.
- **Most statements about Raja:** ideas from the 4-hour chart, his varying risk, the 2-lot
  mistake, turning down a wide stop, his partial closes.

## What was wrong

### Wrong numbers

| Where | What was wrong | Fix |
|---|---|---|
| Lesson 7, section 4 | The "same trade, three endings" table was presented as the 10,000-account trade from lesson 6, but its numbers came from a 100,000 account | The table now says which account it uses, and gives the 10,000 numbers beside it |
| Lesson 3, section 4 | "Six 4-hour candles are 24 hours of trading." One of the six holds only 3 hours because of the daily break | Now "one trading day" |
| Lesson 5, sections 3 and 4 | 13 divided by 8 was written as 1.62. It is 1.625 | Now "about 1.6" |
| Lesson 5, section 4 | "All three have the same signal." The third example is a different candle | Now says so |

### Statements our own tests contradict

These read as true when they were written. The data checks in `research/results` then said
otherwise. Each lesson now has a "What our tests have said so far" section.

| Where | What it said | What the tests found |
|---|---|---|
| Lessons 1 and 4 | A fuller-bodied breakout candle shows conviction and is better | Candles over 80% body did worse afterwards than candles of 50% to 65% |
| Lesson 4 | A level break is a bet that price keeps going | On its own it was a coin flip: 50.0% over 784 signals |
| Lessons 2 and 4 | A level that held more than once means more | It added nothing once the hours and direction filters were on |
| Lesson 3 | More direction readings give cleaner trades | The daily background added nothing, and all three together were no better than one |
| Lesson 5 | Levels mark where a trade will stall | The room rule and level targets did worse than a plain target of twice the risk |
| Lesson 7 | Which exit style is best was left open | A single target beat the quarters ladder clearly on the large sample |

### Trading lore stated as fact

| Where | What it said | Fix |
|---|---|---|
| Lesson 2 | "Orders pile up around them", "the one everybody is watching" | Now given as the usual explanation traders offer, not as something measured |
| Lesson 3 | "Breaks that go with the bigger move tend to have more behind them" | Now given as Raja's approach, with what our tests made of it |
| Lessons 1 and 4 | Waiting for the close "avoids most of those traps", is "the most common way" to be caught | Softened. We have not measured it |

### Statements about Raja that went beyond the notes

| Where | What it said | Fix |
|---|---|---|
| Lesson 7 | Raja himself says moving the stop was the mistake | The notes only record that a stop move was criticised afterwards. "Never loosen a stop" is now given as our rule |
| Lesson 7 | Halves "is close to what Raja does" | His partial closes vary. Halves is now called our simple fixed version |
| Lesson 5 | He checks room "on every trade"; a round number is one of his walls | "On every trade" and "a round number" removed. Neither is in the notes |
| Lesson 2 | Support is "the low between those two candles"; a strength of 1 is "closest to his words" | The notes give only "a down candle then an up candle". The lesson now says the rest is our reading, and that his test and ours are not the same |

### Things that would mislead

| Where | What it said | Fix |
|---|---|---|
| Lesson 1 | The broker's clock is 7 hours ahead of New York, as a fact | Now stated as what we have seen and assumed, to be checked against MetaTrader in lesson 10 |
| Lesson 1 | "Two timeframes", "only a closed candle counts" as absolute | Notes added: lesson 3 adds the daily chart, and Raja sometimes enters before the close |
| Lesson 2 | The close rule "does the job" of a zone | "Part of the job" |
| Lesson 4 | The list of checks looked complete | A note on the one extra safety guard in the code |
| Lesson 6 | One spread as the stop buffer, as if settled | Now says it is our choice and the notes proposed smaller ones |
| Lesson 6 | "Every losing trade costs the same"; stopped out is "always exactly -1R" | Now: about the same and never more than chosen, except when price jumps past the stop |
| Lesson 7 | "Never holds overnight"; the time stop as a general ending | Now: never through the daily break; the time stop belongs to the quarters style only |
| Lesson 7 | The ladder "from your first bot" | "Based on": the first bot's version differs in two small details |
| Lessons 6 and 7 | Two figures with no source given (152 trades; 695, 356 and 62) | The source and date are now stated |
