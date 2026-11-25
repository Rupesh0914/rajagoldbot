# Coverage: is anything missing?

This page checks the lesson plan against the owner's research notes on Raja Banks (13 video
transcripts, 11 unique). Every rule and every setup in those notes is listed here with the lesson
that covers it. Nothing is dropped silently: if something is taught but not automated, this page
says so and says why.

It is updated with every lesson.

## The 16 rules in the notes

| Rule | What the notes say | Where it is covered |
|---|---|---|
| R01 | Read weekly, daily and 4-hour charts before acting on 1-hour or 30-minute | Lesson 3. The bot reads the 4-hour chart two ways and the daily chart one way. The weekly chart is taught for the eye only |
| R02 | Mark nearby support and resistance; look at the candles to the left | Lesson 2. "Candles to the left" is the level-quality count in section 8 |
| R03 | Check for clean space to the next obstacle before entering | Lesson 5 |
| R04 | A break or close beyond a level, for continuation | Lesson 4 (close version). The break-before-close version is Lesson 14 |
| R05 | Support is a down candle followed by an up candle; resistance the reverse | Lesson 2 (section 6), used fully in Lesson 12 |
| R06 | Trade wick fills with the trend, after structure forms on a lower timeframe | Lesson 13 |
| R07 | A large wick relative to the body can signal exhaustion | Lesson 1 (reading wicks), Lesson 15 |
| R08 | Prefer the active hours, including before the New York open | Lesson 8 |
| R09 | A 15-minute confirmation can come before the 30-minute close | Lesson 14 |
| R10 | Do not force trades in consolidation or when the stop would be too wide | Lesson 8 (consolidation), Lesson 6 (wide stops) |
| R11 | Stops go beyond the prior candle or structure | Lesson 6 |
| R12 | Risk of 1%, 1.5%, 2% and 5% appears in different examples | Lesson 6. The bot uses one small fixed share, not a mix |
| R13 | Close part of the position and move the stop to break-even | Lesson 7 |
| R14 | To sell a continuation, wait for a bounce up into resistance | Lesson 12 |
| R15 | The jobs-report (NFP) tactic: an order above and below, cancel the other when one fills | Lesson 16, taught only, not automated |
| R16 | A losing buy that might have been avoided by waiting for a 15-minute close | Lessons 12 and 14, as a case study |

## The 9 setups in the notes

| Setup | What it is | Plan |
|---|---|---|
| S01 | Break of a level, with the bigger direction | **The core bot.** Lessons 1 to 8 |
| S02 | Wick fill with the trend | Lesson 13. Joins the bot only if its own honest test passes |
| S03 | Bounce off support with a bullish candle | Lesson 12. Same condition |
| S04 | Bounce into resistance, then sell the continuation | Lesson 12. Same condition |
| S05 | Earlier entry on a 15-minute close or a break of the previous candle | Lesson 14. The notes call it riskier; the version that enters inside a candle needs tick data to test |
| S06 | Escape from a sideways range | Lessons 5 and 8: staying out of the middle of a range is part of the core bot |
| S07 | Exhaustion wick reversal | Lesson 15, **taught only.** The notes say Raja himself calls it advanced and risky |
| S08 | Jobs-report straddle at 5% risk | Lesson 16, **taught only, not automated.** One example, extreme spread and slippage risk, and 5% risk is far above anything this bot will use |
| S09 | Partial closes, break-even stop, a runner | Lesson 7: partial closes and break-even are built. A runner is not yet |

## Things a working bot needs that the notes do not contain

| Need | Where |
|---|---|
| Exact position size for gold on the broker's contract | Lesson 6 |
| Costs: spread, commission, overnight charges | Lessons 6 and 9 |
| Daily safety limits: most trades a day, a daily loss stop, a losing-streak stop | Lesson 8 |
| Scheduled news: when to stand aside | Lesson 8 |
| An honest test with pass marks fixed before the data is seen | Lesson 9 |
| The link to MetaTrader 5 on a demo account, and what happens if the PC sleeps or restarts | Lesson 10 |
| A journal of every trade and every skipped signal, and a daily report | Lesson 11 |

## What an eye sees, and what the bot measures

The bot does not look at a chart the way a person does. Each thing an eye picks up has to be
turned into something measured. This table tracks how far that has got.

| What an eye sees | What the bot measures | Lesson | Status |
|---|---|---|---|
| A level is an area, and some areas have held many times | Turns at a level, within half an average candle | 2 | Built, as an option |
| Candles stepping up or down | Last two peaks and last two dips on the 4-hour chart | 3 | Built, as an option |
| The weekly and daily background | Daily close against a week earlier | 3 | Built, as an option |
| A strong, convincing breakout candle | Share of the candle that is body, and closing in the direction of the break | 4 | Built |
| Open space ahead, or a wall close by | Distance to the next level, against the distance to the far end of the signal candle | 5 | Built. Walls from the 4-hour and daily charts not yet counted |
| A market going sideways | Overlapping candles, mixed structure | 8 | Structure built; the rest planned |
| A rejection wick warning that a move is tiring | Wick against the move, measured against the body | 8 | Planned |
| "This one just looks wrong" | Nothing. Some judgement cannot be written as a rule | | See below |

Every option is tried on the first 13 months of history (`research/results`) and then judged in
Lesson 9 on the 12 months held back, not by opinion. Once the bot can produce trades, the owner reviews about 50 chart pictures drawn at
random from that history in one sitting, as a check that the bot's trades look like trades a
person would take.

## Numbers we had to choose

Raja trades by eye. The notes record no exact number for most of what he does, so a bot has to
choose one. Each choice is listed here so none is hidden. None of these is a Raja Banks rule. None
may be tuned on test results: Lesson 9 fixes them before the data is seen.

| Lesson | Choice | Value | Status |
|---|---|---|---|
| 1 | Decision timeframe | 30-minute candles | From the notes (30-minute or 1-hour) |
| 1 | Context timeframe | 4-hour candles on the broker's clock | From the notes |
| 2 | What counts as a level | Swing high or low, wick tip, one exact price | Our choice |
| 2 | Swing strength | 2, 4 or 8 candles each side | Candidates; one is fixed in Lesson 9 |
| 2 | Level age limit | 7 days | Our choice |
| 2 | What breaks a level | A 30-minute close beyond it | From the notes (one of two versions) |
| 2 | How close two turns must be to count as one area | Half the average height of the last 20 candles | Our choice |
| 2 | Minimum turns at a level before trading it | 1 (off) or 2 | Decided in Lesson 9 |
| 3 | Closes rule | Last 4-hour close against the close 6 candles earlier | Our choice |
| 3 | Structure rule | Last two peaks and dips on the 4-hour chart, strength 2 | Our choice |
| 3 | Daily background | Last daily close against the close 5 candles earlier | Our choice |
| 3 | Which direction readings are switched on | Combinations tested | Decided in Lesson 9 |
| 4 | How much of the signal candle must be body | 50%, 65% or 80% | Candidates from the notes; one is fixed in Lesson 9 |
| 4 | Signal level when one candle breaks several | The furthest one broken | Our choice |
| 4 | A level broken by a candle that fails a check | Used up, no second chance | Our choice |
| 5 | What counts as a wall | The nearest standing 30-minute ceiling above a buy, floor below a sell | Our choice |
| 5 | Room needed | 1.0, 1.5 or 2.0 times the risk | Candidates from the notes; one is fixed in Lesson 9 |
| 5 | Open space, with no level ahead | Allowed, or skipped | Decided in Lesson 9 |
| 6 | Where the stop goes | Beyond the far end of the signal candle | From the notes (prior candle or structure) |
| 6 | Stop buffer | One spread (a sell adds one more, because it closes at the ask) | Our choice; the notes list 0, 2 or 5 ticks as candidates |
| 6 | Risk per trade | 0.5% of the account | Our choice, deliberately below the 1% to 2% in the notes |
| 6 | Stop too wide | More than 3 average candles | Our choice |
| 6 | Stop too tight | Less than 6 spreads | Our choice |
| 6 | Lot rounding | Always down | Our choice |
| 7 | Target | One spread in front of the next level | Our choice |
| 7 | Target in open space | 2 times the risk | Our choice |
| 7 | Exit style | Single target, halves, or the quarters ladder from the Sugarwood bot | Decided in Lesson 9; compared first in the trade test |
| 7 | Stop after a banked part | Break-even after the first, then one step behind | From the Sugarwood bot |
| 7 | Time stop | 4 hours with nothing banked (quarters only) | From the Sugarwood bot |
| 7 | End of day | Everything closed at 16:50 New York | From the Sugarwood bot |

## Where the notes disagree with themselves

The notes record these conflicts and say not to smooth them over. The plan keeps them apart.

| Topic | The two sides | How the plan handles it |
|---|---|---|
| Wait for the candle close, or enter on the break | Both appear | The core bot waits for the close (Lesson 4). The early version is a separate lesson and a separate test (Lesson 14) |
| Is the 15-minute chart reliable | Rarely used in one video, relied on in another | Lesson 14 |
| Risk per trade | 1%, 1.5%, 2%, 5% | One small fixed share (Lesson 6) |
| How wide a stop is too wide | No fixed limit | A rule tied to the room available (Lessons 5 and 6) |
| How much to close early | 50% in one example, 90% in another | Lesson 7 picks one schedule and tests it |

## Limits of the source

- The notes come from transcripts, not from the charts on screen. Where Raja pointed at
  something, the notes can only guess what it was.
- The examples in the videos include losing trades and one sizing mistake. They are teaching
  examples, not a track record.
- Nothing in the notes shows that the strategy makes money. That is what Lesson 9 is for.
