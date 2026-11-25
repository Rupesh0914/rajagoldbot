# How the price history is split

**Fixed on 2026-11-25, before any price in this history was looked at for this bot.** The git
commit that adds this file is the proof of when.

The history is Eightcap XAUUSD one-minute bars, 2024-10-23 to 2026-11-23 (about 25 months),
pulled from the owner's MetaTrader 5.

| Part | From (UTC) | To (UTC) | Length | Use |
|---|---|---|---|---|
| **Development** | start of data | 2025-11-23 00:00 | 13 months | Open. Look, test ideas, find weaknesses, fix, test again |
| **Validation** | 2025-11-23 00:00 | 2026-05-24 00:00 | 6 months | Closed until Lesson 9. Used once, to choose between the few final candidates |
| **Holdout** | 2026-05-24 00:00 | end of data | 6 months | Closed until Lesson 9. Used once, for the final verdict |

Both boundaries fall on a Sunday, when the gold market is shut.

## Why

Trying an idea, looking at the result, fixing and trying again is the right way to build. It is
also the easiest way to fool yourself: change enough things and something will look good on the
data you kept looking at, by luck alone.

The split keeps both. Everything may be tried on the development part, as often as wanted. The
other two parts stay unseen, so that in Lesson 9 the bot is judged on prices that none of its
rules were shaped on.

## Rules

1. The research tools load **only** the development part. They do not read a single bar past the
   boundary. Opening another part takes a deliberate code change in Lesson 9.
2. A result on the development part is a clue, not a verdict. Nothing here is called proven.
3. Every check is saved with the code version that produced it, including the ones that came out
   badly.

## What had been seen before this was fixed

- The last three months of this history (2026-08-21 onward, inside the holdout) were used in
  November 2026 to test a **different** strategy, the old bot's option-based levels. No rule of
  this bot was run on them, and no result from that test is used here.
- No rule of this bot had been run on any market price. Its examples so far are hand-made.
