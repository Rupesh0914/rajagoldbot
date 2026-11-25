# Lesson 7: Managing the trade

The trade is open. The entry, the stop and the size are fixed (Lesson 6). This lesson is about
everything from that moment to the exit: where the profit is taken, whether to take some of it
early, what happens to the stop, and when to simply close and go home.

## 1. The four ways a trade ends

| Ending | What happened |
|---|---|
| **Target** | Price reached the place where the profit is taken |
| **Stop** | Price reached the stop |
| **Time stop** | Hours have passed and nothing has happened, so the trade is closed (used by the quarters style only) |
| **End of day** | It is 16:50 in New York. Everything is closed |

There is no fifth way. The bot never holds a trade through the daily market break, and never
decides mid-trade that "this one is different".

## 2. The target

The target is the wall from Lesson 5: the next level in the way. The bot takes profit **a touch
in front of it**, by one spread, because price often turns just before a level without quite
touching it.

When there is no level ahead (open space), there is nothing to aim at. The bot then aims at
**twice the risk**. That number is our choice, and Lesson 9 tests it.

Example, continuing the trade from Lessons 5 and 6:

```
Entry   3762.20
Stop    3753.80    risk 8.40
Ceiling 3775.00
Target  3774.80    12.60 away, which is 1.5R
```

## 3. Three ways to take the profit

**Single.** The whole position is closed at the target. The stop never moves. Simple, and
all-or-nothing.

**Halves.** Half is closed at the halfway point. The stop on the rest moves to the entry price,
so the remainder should not lose (unless price jumps past the stop). The rest is closed at the
target. This is our simple fixed version of Raja's partial closes, which vary from video to
video.

**Quarters.** This is based on the take-profit ladder from your first bot, Sugarwood Gold. A quarter of
the position is closed at 25%, 50%, 75% and 100% of the way to the target. After each step the
stop moves up behind it:

| After this step is banked | The stop on what is left moves to |
|---|---|
| 25% | The entry price (break-even) |
| 50% | Just behind the 25% step |
| 75% | Just behind the 50% step |

If no step is banked within 4 hours, the trade is closed.

## 4. The same trade, three endings

Here is that trade under each style, for three things price might do. To keep the sums clean
this table uses a 100,000 account, where the position (0.59 lots) splits into even parts:

| What price did | Single | Halves | Quarters |
|---|---|---|---|
| Straight to the target | +1.50R | +1.12R | +0.93R |
| 60% of the way, then all the way back | -1.00R | +0.38R | +0.46R |
| Straight to the stop | -1.00R | -1.00R | -1.00R |

```
python -m rajabot exits
```

On the 10,000 account from Lesson 6 the trade is 0.05 lots, which cannot be split evenly (see
section 8). The numbers shift: straight to the target gives +1.05R for halves and +0.83R for
quarters, and "60% then back" gives +0.45R and +0.44R. The pattern is the same.

```
python -m rajabot exits --balance 10000
```

This table is the whole lesson. Read it twice.

- When the trade **works**, the ladder makes much less: 0.93R instead of 1.50R. Three quarters
  of the position were sold before the target.
- When the trade **half works and fails**, the ladder rescues it: a small win instead of a full
  loss.
- When it **fails outright**, nothing helps. A loss is a loss.

So a ladder does not create profit. It moves it. It gives up part of the big wins to buy
protection against the trades that turn back.

## 5. Why a high win rate proves nothing

A ladder makes far more trades end as "winners", because any trade that reaches the first step
and then falls back to break-even counts as a small win. Win rates of 60% and more are normal
with a ladder, even on random prices where nothing can have an edge.

What matters is the **average R per trade**: wins and losses added together, divided by the
number of trades. A style that wins 62% of the time with tiny winners can lose money. One that
wins 40% of the time with big winners can make it.

In the test of your first bot (run on your PC on 25 November 2026, under its live settings), 695
trades reached the first step 356 times and the final target only 62 times. Most of its "wins"
were quarter-sized.

## 6. Moving the stop to break-even

It feels safe: "now I cannot lose". And it has a real cost. Price rarely moves in a straight
line. It often comes back to the entry area before continuing. A break-even stop takes you out
right there, for nothing, on a trade that would have won.

Whether the protection is worth the cost is not something to argue about. It is something to
measure, and that is the next test.

**One rule that is not up for testing:** the stop never moves **away** from the trade. The bot
can only tighten a stop, never loosen it. That is our rule. The notes record one of Raja's
losing trades where moving the stop was criticised afterwards, without saying more.

## 7. Closing at the end of the day

At 16:50 New York time every open trade is closed at whatever the price is. The gold market
shuts for its daily break ten minutes later. Holding through the break means a gap risk the stop
cannot protect against, and an overnight charge.

## 8. Small accounts cannot ladder

The broker's smallest step is 0.01 lots. A position of 0.05 lots cannot be cut into four equal
parts. The bot does what it can and says so:

| Position | Quarters becomes |
|---|---|
| 0.59 lots | 0.15, 0.15, 0.15, 0.14 |
| 0.05 lots | 0.02, 0.01, 0.01, 0.01 |
| 0.03 lots | Three parts, at steps 1, 2 and 4 |
| 0.02 lots | Two parts, at steps 1 and 3 |
| 0.01 lots | One part, at the 50% step |

```
python -m rajabot exits --balance 10000
python -m rajabot exits --balance 3000
```

At 0.5% risk, an account needs roughly 5,000 to 10,000 before a four-step ladder is really four
steps. Below that, "quarters" quietly becomes something else. This is one of the things your
first bot's notes warned about too.

## 9. What Raja does differently

- **His partial closes vary.** In one video he closes about 90% early. In another he closes 50%,
  then 90% of what is left. The notes found no fixed schedule. Halves is our nearest fixed
  version.
- **He sometimes lets a small "runner" go on** with the stop at break-even, hoping for a much
  bigger move. The bot's styles all end at the target. A runner is a candidate for later.
- **He exits early by judgement** when the chart stops looking right. The bot has no judgement.
  Its only early exits are the time stop and the end of the day.

## 10. Which style is best? What our tests have said so far

The first whole-trade test on 13 months of your Eightcap history compared the styles with every
other rule the same. Clues, not proof; details in `research/results`.

On the large sample (every strong candle in New York hours, with the 4-hour direction):

| Exit | Trades | Winners | Average R |
|---|---|---|---|
| Single target at twice the risk | 646 | 44% | +0.105 |
| Quarters ladder | 838 | 64% | +0.019 |

- **The ladder won far more often and made far less.** Winners went from 44% to 64%, and the
  average fell by about four fifths. With the spread doubled the ladder went below zero.
- Of 838 ladder trades, 332 banked nothing and only 74 reached the last step.
- On the smaller level-break sample (115 trades) the three styles could not be told apart.
  Halves was the weakest there.

This is section 5 in real numbers: a high win rate, bought with the size of the winners.

A second test then moved the single target nearer and further:

| Target | Winners | Average R |
|---|---|---|
| 1R | 52% | +0.045 |
| 1.5R | 47% | +0.091 |
| 2R | 44% | +0.105 |
| 3R | 41% | +0.133 |
| None: hold to the stop or 16:50 | 37% | +0.175 |

Every step further out did better, all the way to having no target at all. Fewer winners each
time, and more made overall. The trades still open at 16:50 turned out to be the good ones:
closed there, they averaged +0.38 R.

So the working exit is **no target**: the trade ends at its stop or at 16:50. The ladder stays in
the code and in this lesson, because it is the best way to see the trade-off, and because the
question is not closed: this is one period of one market, and the final choice is made in
Lesson 9 on prices the bot has not seen.

A warning that comes with this exit: it wins only about 37% of the time. Most trades lose, and a
few long runs pay for them. That is hard to sit through, and it is the price of the result.

## What the bot piece does

`rajabot/manage.py` holds one open trade and is fed each new minute of prices. Each minute it
checks, in this order: is it the end of the day, has the time stop run out, was the stop
reached, was a target reached. It closes what needs closing and moves the stop up when a step is
banked.

When one minute touches both the stop and a target, it assumes the stop came first. That is the
cautious reading, and it keeps the tests from flattering the bot.

The same code runs in the tests and, from Lesson 10, on the demo account, so both follow
identical rules.

## Check yourself

1. Entry 3800, stop 3790, next ceiling 3820, spread 0.20. Where is the target, and how many R is
   it?
2. With the quarters ladder on that trade, price reaches the 50% step and then falls all the way
   back. Roughly where is the remaining half closed, and is the trade a winner or a loser?
3. A style wins 65% of its trades. Is it profitable?
4. Price has moved in your favour and you move the stop to break-even. Name one benefit and one
   cost.
5. It is 16:50 in New York and a trade is slightly in profit, well short of its target. What
   does the bot do?
6. Why can a 3,000 account not really use the quarters ladder?

<details>
<summary>Answers</summary>

1. Target 3819.80 (one spread in front of the ceiling). That is 19.80 away, and the risk is 10,
   so 1.98R.
2. After the 50% step the stop sits just behind the 25% step. The 25% step is at about 3804.95,
   so the rest is closed just under that. A quarter was banked at about 3804.95, a quarter at
   about 3809.90, and the remaining half just under 3804.95: a winner, of roughly +0.6R.
3. Cannot tell. It depends on the size of the winners against the losers. Many small wins and a
   few full losses can add up to a loss.
4. Benefit: the trade can no longer lose money. Cost: an ordinary pullback to the entry takes you
   out of a trade that might have gone on to the target.
5. Closes it at the current price. Nothing is held past 16:50.
6. At 0.5% risk its positions are about 0.01 to 0.02 lots, and 0.01 is the smallest step. There
   is nothing to split into four.

</details>

## Next

Lesson 8: when not to trade. Sideways markets, the hours to stay out, scheduled news, and the
daily safety limits that stop a bad day from becoming a disaster.
