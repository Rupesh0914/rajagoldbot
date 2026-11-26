# Review of the Raja Banks material: what we know, what we do not, and how to close the gap

Written 2026-11-26, after the final test. The aim is the owner's: understand why he enters each
trade, how he reads structure, what confirms an entry, and how he manages stop and profit, and
then fix our bot from that evidence, not from guesses and not by chasing a better backtest.

## 1. What this review is built on, and its limit

**What we have:** the owner's research notes. They are summaries of 13 video transcripts (11
unique, since two pairs are duplicates). They are careful notes: they mark what is explicit, what
is inferred and what is unknown.

**What we do not have:**

- The videos themselves, or their links. The notes number them 1 to 13 and do not name them.
- The transcripts the notes were made from, or the per-video files the notes refer to.
- **Any chart.** The notes say so themselves: "Transcript-only: chart geometry, candle sizes and
  precise order placement need video-frame verification."

So nobody working on this bot, human or AI, has yet looked at one of his charts. Everything in
lessons 1 to 9 was built from descriptions of what he said, not from what he drew or where he
clicked. That is the single biggest gap, and no amount of backtesting closes it.

## 2. The casebook: every trade and example the notes record

"Pips" are left as the notes give them. What a pip is on gold in these videos is not established
(section 4, question 1).

### Actual trades (all from Video 12, a gold simulation)

| # | Where | What he did | Why, as recorded | Stop and risk | Management and outcome | What the notes cannot tell us |
|---|---|---|---|---|---|---|
| T1 | 33:27-36:59 | **Bought** gold | A 30-minute bullish close from support, with a wick fill as the possible aim | About 15 pips, intended 1% | **Lost.** Afterwards he says not waiting for a 15-minute bullish close may have been the mistake | Where the support was and how he drew it. What the 4-hour chart showed. Where the target was |
| T2 | 35:53-46:31 | **Sold** gold | After a fall, price bounced up into fresh resistance. Bearish 30-minute or 1-hour candle. Aim: a lower wick or the next support | About 25 pips, intended 1% | Took 50%, later 90% of the rest, stop moved to break-even. Sized at 2 lots by accident | What "fresh resistance" looked like on the chart. The exact entry candle. Where each partial was taken and why there |
| T3 | 1:14:59-1:18:35 | Stopped out, then re-entered, near the ADP report | Not recorded | Not recorded | Moving the stop was criticised afterwards | Almost everything. Which way, why re-enter, which way the stop moved |
| T4 | 1:19:19-1:24:09 | Jobs report (NFP): a buy order above and a sell order below a 30-minute candle | An event tactic, separate from his normal trading | 5% stated | Cancel the other order when one fills. Outcome not generalisable | Which candle. How far the orders were placed. The fills |

### A trade he turned down (Video 12)

| # | Where | What | Why |
|---|---|---|---|
| N1 | 21:40-22:25 | Skipped a trade | The stop would have been about 27 pips: too wide for the opportunity |
| N2 | 24:00-26:04 | Lists when he skips | Price consolidating, a nearby zone blocking the move, confirmation missing, stop too wide |

### Analysis and teaching, without a completed trade

| # | Where | What it shows |
|---|---|---|
| A1 | Video 12, 12:00-12:41 | Most trade ideas come from the 4-hour chart. Execution on 1-hour or 30-minute |
| A2 | Video 12, 15:02-19:18 | Drawing the nearby zones, looking at candles to the left, measuring the clean distance to the next obstacle (17:25-18:06), then waiting for the break or close (18:53-19:18) |
| A3 | Video 12, 23:38-23:46 | Risk of 1.5% discussed |
| A4 | Video 12, 29:50-31:07 | After a strong move, wait for the retracement and fresh structure before entering |
| A5 | Video 9, 21:40-24:54 | An entry on the break of a previous candle, before the slower candle closes. 2% risk. About 90% closed early |
| A6 | Video 2, 00:36-08:19 | Wick fills: a wick on a higher timeframe as the destination, a lower timeframe for the entry. Candles that are mostly body preferred |
| A7 | Video 2, 05:19-05:44 and 10:51-11:56 | Support is a down candle then an up candle. Resistance the reverse. To sell a continuation, wait for the bounce into resistance |
| A8 | Video 2, 08:19-09:49 | A long wick against the body as a sign of exhaustion. Trading against the trend from it is called advanced and risky |
| A9 | Video 2, 12:53-13:51 | He says he rarely uses the 15-minute chart |
| A10 | Video 8, 00:00-19:21 | A whole video on entering earlier, on the 15-minute chart: catching more of the move against weaker confirmation |
| A11 | Videos 1, 3, 4 | The basic teaching: break and close beyond a level, with clean space ahead |
| A12 | Videos 5, 10 | Gold simulations. The notes record only that partial closes, break-even and a runner recur |

### What the casebook shows

- **There are four real trades in the notes, all from one video.** One lost. One was sized
  wrongly. One involved a stop move that was criticised. One is a news tactic at 5% risk.
- **Not one of them has a date, a price, or a chart.** So none can be replayed against real
  prices as it stands.
- The one trade where the notes record profit being taken, T2, is a **retest entry**: sell the bounce into fresh
  resistance. **Our bot has never tested that kind of entry.** Everything in lessons 4 to 9
  tested the other kind, the break and close.

That last point matters most. Our final test said the level **break** did not hold up. It said
nothing about the kind of entry in the one trade where he is recorded taking profit.

## 3. His approach against our bot, piece by piece

| Piece | What he does, per the notes | What our bot does | What our tests said | The gap |
|---|---|---|---|---|
| Big picture | Weekly, daily, 4-hour. Ideas from the 4-hour | 4-hour closes rule only | Helps. One of the things that carried the result | Small. His reading is richer, ours is a single comparison |
| Hours | Before and around the New York open | 07:00-16:00 New York | Helps most of all | Small |
| Where the levels are | Recent support and resistance, wicks, candles to the left, drawn by eye | Swing highs and lows by a counting rule | As an entry trigger, failed on unseen data | **Large.** We do not know that our levels are his levels. Nobody has compared them on a chart |
| How he enters | Four different ways: break and close; **retest of fresh structure**; wick fill; early entry on a smaller timeframe | Break and close only | Break and close: no edge of its own | **Large.** Three of his four entry types are untested, including the one in his best-recorded trade |
| What confirms | A 30-minute or 1-hour close. Sometimes a 15-minute close first. He regrets skipping it in T1 | A 30-minute close with at least half body | Fuller candles did worse | Medium. The 15-minute confirmation is untested |
| Stop | Beyond the previous candle or the structure. About 15 to 25 pips in the examples. Refuses about 27 | Beyond the signal candle. Refuses over 3 average candles | Not isolated | **Unknown size.** Depending on what a pip is, his stops are either several times tighter than ours or wider. This changes everything downstream |
| Room | Measures clean space to the next obstacle before entering | Room against risk, to our own swing levels | Did not help | Medium. May be the levels, not the idea |
| Taking profit | Partial closes (50%, 90%), stop to break-even, sometimes a runner. Targets: the previous low, next support, a wick | Tested partials, a ladder, fixed targets and no target | **Holding to the stop or the end of the day did best. Partials did worst** | **A real contradiction.** Either his partials work because of *when* he takes them, which we have not captured, or they cost him money too. The charts would show which |
| When he skips | Consolidation, a blocking zone, no confirmation, a wide stop | Hours, spread, daily limits. Sideways rule built, untested | Not tested | Medium |
| Risk | 1% to 2% | 0.5% | Not relevant to edge | A choice, not a gap |

## 4. The questions only the charts can answer

Each is tied to a place in a video. These are what to look at, in order of how much they would
change the bot.

1. **What is a pip on gold here?** Read the price scale on any gold chart in Video 12 against a
   stated stop. If "15 pips" is 1.50 dollars, his stops are about a fifth of ours and his whole
   method is tighter and faster than what we built. If it is 15 dollars, they are about twice
   ours. Everything about size, room and targets depends on this.
2. **T2, the retest sell (Video 12, 35:53-46:31).** The chart at the moment of entry. Where is
   the "fresh resistance" relative to the fall before it? Which candle is the entry? Where is the
   stop, exactly? Where were the 50% and the 90% taken, and what was the chart doing at each?
3. **T1, the losing buy (Video 12, 33:27-36:59).** The chart at entry. What made that a
   "support"? What did the 4-hour chart look like? Would our rules have taken it?
4. **How he draws a zone (Video 12, 15:02-18:06).** One frame with his zones on it. Are they at
   swing highs and lows, at candle bodies, at wicks? How many does he draw, how far back?
5. **N1, the trade he refused (Video 12, 21:40-22:25).** What a "too wide" stop looks like next
   to the room available.
6. **The date of each gold session.** Simulation software shows the date being replayed. With a
   date and a time, each trade can be put on real prices and our bot run over the same hours.
7. **The early entry (Video 9, 21:40-22:29, and Video 8).** Which candle's break he enters on.

## 5. The method from here

The owner's condition is the right one: change the bot from evidence, not from a better
backtest. That needs a different yardstick from the one used in lessons 4 to 9.

**Step 1. Get the source.** The 13 videos, identified. Their transcripts. Frames at the places
listed in section 4.

**Step 2. Write each of his trades as a record.** Date, time, direction, entry, stop, each exit,
and his stated reason, taken from the frame and the transcript together.

**Step 3. Replay our bot over those same hours on real prices.** For each of his trades: did our
bot see a level where he drew one? Did it signal? Earlier or later than him? Where would its stop
and exit have been? For each trade he refused: did our bot refuse it too?

**Step 4. Fix the differences that the records show,** one at a time, each traced to a specific
trade of his. The measure of success is **agreement with what he did**, not profit.

**Step 5. Only then test for profit, once, on data that none of this touched.** All 25 months of
our Eightcap history are now used up (lesson 9). So a new test needs new data: gold prices from
before October 2024, which exist from other sources, or the bot's own demo record going forward.
The same discipline as lesson 9 applies: rules frozen first, one run.

**What does not change meanwhile.** The version that came out PROVISIONAL stays exactly as
tested. It is not adjusted on the strength of this review. Anything built from the steps above is
a new version with its own test.

## 6. An honest caution about the whole exercise

Four trades from one video, one of them a loss and one a sizing mistake, are teaching examples.
They are not a track record, and the notes say the videos do not show verified profitability. So
even a bot that copied him perfectly would still have to earn its result in a test. Matching him
is how we find out what his method actually is. It is not, by itself, evidence that the method
makes money.
