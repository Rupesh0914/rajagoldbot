# rajagoldbot

A gold (XAUUSD) trading bot built from scratch, one lesson at a time. Each lesson teaches one idea
from the Raja Banks style of trading in plain English, and adds the piece of the bot that does
that one thing, with tests.

By the end, the owner understands every rule the bot follows, because each rule was learned
before it was coded.

This project is not affiliated with Raja Banks. It is built from the owner's own notes on
publicly taught ideas.

## The strategy in one paragraph

Mark the prices where gold has turned before (levels). Read the big-picture direction from the
4-hour chart. Wait for a 30-minute candle to **close** through a level in that direction, with
open space ahead of it. Enter, put the stop where the idea is proven wrong, risk a small fixed
share of the account, and be out by the end of the New York day.

## Roadmap

| # | Lesson | Bot piece | Status |
|---|---|---|---|
| 1 | [Candles and timeframes](lessons/01-candles-and-timeframes.md) | `rajabot/candles.py` | Done |
| 2 | [Levels: where price turned before](lessons/02-levels.md) | `rajabot/levels.py` | Done |
| 3 | Direction: reading the 4-hour chart | `rajabot/direction.py` | Next |
| 4 | The trigger: a 30-minute close through a level | `rajabot/trigger.py` | |
| 5 | Room to run: is there open space ahead? | `rajabot/space.py` | |
| 6 | Stop loss and how much to risk | `rajabot/risk.py` | |
| 7 | Managing the trade and going flat | `rajabot/manage.py` | |
| 8 | When not to trade: hours, news, wide spreads | `rajabot/filters.py` | |
| 9 | Honest testing: a backtest that cannot fool us | `rajabot/backtest/` | |
| 10 | Connecting to MetaTrader 5 on a demo account | `mt5/` | |
| 11 | Watching it: journal and daily report | `rajabot/journal.py` | |

## Ground rules

1. **Demo account only.** Switching to a real-money account is the owner's decision and the
   owner's action, by hand, in MetaTrader. No code or assistant in this project does it.
2. **Closed candles only.** The bot never acts on a candle that is still forming.
3. **No looking ahead.** Every decision uses only what was known at that moment. Tests enforce it.
4. **Honest testing before trust.** Nobody knows yet whether these rules make money. Lesson 9
   builds a test with its pass marks fixed before the data is seen, and its result is published
   whatever it says.
5. **No secrets in the repo.** Passwords, API keys and account numbers stay out of git.

## Running it

Needs Python 3.10 or newer.

```
python -m pip install -r requirements.txt
python -m unittest discover -s tests -t .
```

Try the pieces built so far:

```
python -m rajabot candle 3750 3758 3748 3756     # lesson 1: read one candle
python -m rajabot levels                         # lesson 2: watch levels appear and break
```
