# Lesson 6: The stop, the costs, and how much to risk

This is the lesson that keeps the account alive. A trader with average entries and good risk
control survives. A trader with brilliant entries and no risk control does not.

It answers three questions for every trade: where is the stop, how big is the trade, and what
does it cost.

## 1. The stop loss

A stop loss is an order that closes the trade automatically if price reaches a level you chose
in advance. It is decided **before** entering, and it is not moved further away afterwards.

**Where it goes.** At the price that proves the idea wrong. The idea was "this candle broke the
level and price will keep going". If price comes all the way back through that candle, the break
has failed. So:

- **Buy:** the stop goes just **below the low** of the signal candle.
- **Sell:** the stop goes just **above the high** of the signal candle.

"Just beyond" means a small buffer, so that price touching the exact low by a cent does not take
you out. The bot uses one spread as the buffer.

The mistake to avoid: choosing the stop by how much you want to lose ("I'll put it 3 dollars
away because that's all I can afford"). The market does not know what you can afford. The stop
goes where the idea is wrong, and the **size** of the trade is what you adjust to make the loss
affordable. That is section 3.

## 2. Two prices: bid and ask

Gold always has two prices at once.

| Price | What it is |
|---|---|
| **Bid** | What you get when you **sell**. This is the price the chart shows |
| **Ask** | What you pay when you **buy**. Always a little higher |

The gap between them is the **spread**. On your account it is usually about 13 to 20 cents on
gold. It is the broker's fee, and you pay it on every trade.

What this means in practice:

- A **buy** is filled at the ask. The moment you buy, you are down by the spread.
- A **sell** is filled at the bid, and later closed at the ask. So a sell's stop has to sit one
  extra spread higher, or it gets hit while the chart still shows price below it.

Example. The signal candle closed at 3762, its low is 3754, and the spread is 0.20.

```
Buy entry = 3762.00 + 0.20 = 3762.20   (the ask)
Stop      = 3754.00 - 0.20 = 3753.80   (one spread below the low)
Distance  = 3762.20 - 3753.80 = 8.40
```

If the stop is hit, the trade loses 8.40 dollars for every ounce traded.

## 3. Position size: the most important sum in trading

Decide what share of the account you are willing to lose on one trade. Then work backwards to
the size.

**The facts about gold:** one lot is 100 ounces. So when gold moves 1 dollar:

| Size | Money |
|---|---|
| 1.00 lot | 100 dollars |
| 0.10 lot | 10 dollars |
| 0.01 lot (the smallest) | 1 dollar |

**The sum:**

```
money to risk = account x risk share
lots          = money to risk / (stop distance x 100)
```

With a 10,000 account risking 0.5%:

```
money to risk = 10,000 x 0.005 = 50
lots          = 50 / (8.40 x 100) = 0.0595
```

The broker only takes lots in steps of 0.01, so that becomes **0.05 lots**. The bot always
rounds **down**, never up, so the real risk is never more than you chose. Here the real risk is
0.05 x 8.40 x 100 = 42 dollars, which is 0.42% of the account.

```
python -m rajabot plan
python -m rajabot size 50 8.4
```

Notice what this does. A far stop gives a small trade. A near stop gives a bigger trade. Either
way the loss is about the same amount of money. Every losing trade costs the same, so no single
trade can do real damage.

## 4. Your account is not in US dollars

Gold is priced in US dollars. Your demo account is held in Canadian dollars. So a 1-dollar move
in gold on one lot is 100 **US** dollars, which is about 140 Canadian.

If the bot ignores this, it trades too big. At a rate of 1.40 it would risk 0.7% when it meant
to risk 0.5%. The old bot had exactly this fault.

This bot converts:

```
python -m rajabot plan --usd-rate 1.40 --currency CAD
```

The same trade becomes 0.04 lots instead of 0.05, risking 47.04 CAD. In Lesson 10 the bot reads
the live rate from MetaTrader instead of being told it.

## 5. Thinking in R

Because every trade risks about the same, traders measure results in **R**: multiples of the
amount risked.

| Result | Meaning |
|---|---|
| -1R | Stopped out. Lost what was risked |
| 0R | Closed where it was entered |
| +1R | Made as much as was risked |
| +2R | Made twice what was risked |

R lets you compare trades of different sizes, and it shows the arithmetic of a strategy plainly.
A strategy that wins half the time needs its winners to be bigger than 1R to make money after
costs. One that wins 40% of the time needs winners averaging above 1.5R.

Lesson 5's room rule, in these words: there must be at least 1R of space before the next wall.

## 6. When the bot refuses the trade

| Reason | Meaning |
|---|---|
| **Stop too wide** | The stop would be more than 3 average candles away. The signal candle was huge, and the trade would need an enormous move to pay |
| **Stop too tight** | The stop would be less than 6 spreads away. The spread alone would be a big part of the risk, and normal jitter would hit the stop |
| **Size below minimum** | Even the smallest trade, 0.01 lots, would lose more than the share allowed. The account is too small for this stop |

Try the last one:

```
python -m rajabot plan --balance 500
```

## 7. The costs

| Cost | What it is | On your account |
|---|---|---|
| **Spread** | Ask minus bid, paid on every trade | About 0.13, median over the 13 months tested. Wider at night and around news |
| **Commission** | A fee per lot, on some account types | None. Measured from 152 of your own demo trades |
| **Swap** | A charge for holding a trade overnight | Not paid: the bot will close everything before the daily break (Lesson 7) |
| **Slippage** | Getting a worse price than asked, mostly on stops in fast markets | Real and unpredictable. Tests allow for it by also running with the spread doubled |

Costs look small and are not. In the first data check the average candle was about 6 dollars
tall, and the spread took about 2% of that on every signal. An edge of a few percent can be
eaten whole by costs, which is why every test in this project pays them.

## 8. What Raja does differently

- **His risk varies.** The notes record 1%, 1.5% and 2% on ordinary trades, and 5% on the
  jobs-report tactic. The bot uses one fixed share. It starts at 0.5%, which is deliberately
  small while the strategy is unproven.
- **He places stops by eye,** beyond the previous candle or the nearest structure, and he walks
  away when the stop would be too wide. In one video he turns down a trade for that reason. "3
  average candles" is our way of writing that down.
- **He once traded the wrong size by accident.** In one of the videos he meant to risk 1% and
  placed 2 lots by mistake. That is a normal human error. The bot works the size out fresh for
  every trade, so it cannot make it.
- **He talks in pips.** The notes could not settle what a pip means on gold in his videos, so
  this bot uses dollars throughout.

## What the bot piece does

`rajabot/risk.py` takes a signal, the price and spread on the next minute, the account balance
and the broker's facts about gold. It returns a plan (entry, stop, lots, and the money at risk)
or the reason there is no trade.

Its tests check that the risk never exceeds the share chosen, for any balance or stop distance,
and that being stopped out is always exactly -1R.

## Check yourself

1. The signal candle for a buy has a low of 3800. The spread is 0.20. Where is the stop?
2. Your account is 5,000 US dollars and you risk 0.5%. The stop is 5 dollars from the entry. How
   many lots? What is the real risk?
3. Same trade, but the stop is 12.50 away. How many lots now? What do you notice about the money
   at risk?
4. You buy at 3762.20 with a stop at 3753.80. Price reaches 3779.00 and you close. What is the
   result in R?
5. Why does a sell's stop sit one spread higher than you would expect from the chart?
6. A friend says: "I always trade 0.10 lots, it's simpler." What is wrong with that?

<details>
<summary>Answers</summary>

1. 3799.80. One spread below the low.
2. Money to risk: 25. Lots: 25 / (5 x 100) = 0.05. Real risk: 0.05 x 5 x 100 = 25, exactly 0.5%.
3. 25 / (12.50 x 100) = 0.02 lots. Real risk: 0.02 x 12.50 x 100 = 25. The same money: a wider
   stop means a smaller trade, not a bigger loss.
4. Risk is 8.40. Gain is 3779.00 - 3762.20 = 16.80. That is +2R.
5. A sell is closed by buying, at the ask, and the ask is a spread above the price on the chart.
   Without the extra spread the stop would be hit before the chart price got there.
6. With a fixed size, the loss depends on how far the stop is. A trade with a 12-dollar stop
   loses four times as much as one with a 3-dollar stop. One wide-stop loser can wipe out
   several winners. Sizing each trade to the stop keeps every loss the same.

</details>

## Next

Lesson 7: managing the trade. Where to take profit, whether to close part of it early, when to
move the stop to break-even, and closing everything before the end of the day.
