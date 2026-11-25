"""The whole bot in one loop: every lesson's piece, joined up.

`Bot.on_bar` is fed one-minute bars, one at a time, in order. It builds the candles, reads the
direction, spots a signal, asks the when-not-to-trade questions, plans the trade, and manages it
to its exit. It only ever sees the bars it has been given, so it cannot look ahead.

The same loop runs in the tests (lesson 9) and on the demo account (lesson 10).

For each one-minute bar, in this order:
  1. if a 30-minute candle has just closed, judge it: is it a signal?
  2. if it is, and nothing says stay out, open a trade on this bar;
  3. manage the open trade against this bar (including the bar it was opened on);
  4. add the bar to the candles being built.

This module decides. It still places no order: lesson 10 connects its decisions to MetaTrader.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .candles import FOUR_HOURS, Bar, Candle, server_seconds
from .direction import BUY, DEFAULT_LOOKBACK, SELL, allows, direction_of_closes
from .filters import DEFAULT_MAX_SPREAD, SESSION_HOURS, DayGuard, NewsCalendar, in_session
from .levels import ZONE_SHARE, LevelBook
from .manage import SINGLE, ExitStyle, Position, target_price
from .risk import DEFAULT_RISK_SHARE, Contract, NoTrade, plan_trade
from .trigger import Signal, Skip, Trigger

ENTRY_WINDOW = 300              # the entry minute must start within 5 minutes of the signal candle's close
NO_TARGET_R = 100.0             # "no target": so far away that the trade ends at its stop or the end of the day
AVERAGE_OVER = 20               # candles in the "average candle" used to judge a stop too wide

CANDLE, LEVEL = "candle", "level"


@dataclass(frozen=True)
class Settings:
    """Everything that defines one version of the bot."""
    name: str
    entry: str = CANDLE                     # "candle": any convincing candle. "level": only a level break
    min_body: float = 0.5                   # share of the signal candle that must be body
    strength: int = 4                       # candles each side of a swing, for level entries
    use_direction: bool = True              # the 4-hour closes rule must agree
    session_hours: tuple | None = SESSION_HOURS
    target_r: float | None = 2.0            # profit target in R. None: no target
    style: ExitStyle = SINGLE
    risk_share: float = DEFAULT_RISK_SHARE
    max_spread: float | None = DEFAULT_MAX_SPREAD
    daily_limits: bool = True               # 5 trades, 3R lost, 3 losses in a row

    def __post_init__(self) -> None:
        if self.entry not in (CANDLE, LEVEL):
            raise ValueError("entry must be 'candle' or 'level'")
        if self.target_r is not None and self.target_r <= 0:
            raise ValueError("target_r must be positive, or None for no target")


@dataclass(frozen=True)
class Trade:
    opened_at: int
    closed_at: int
    side: str
    entry: float
    stop: float
    lots: float
    reason: str             # how the last part was closed: target, stop, time_stop or flat
    r: float                # result in R
    money: float            # result in the account's currency


@dataclass
class Bot:
    settings: Settings
    balance: float
    contract: Contract = field(default_factory=Contract)
    trade_from: int | None = None           # no trade is opened before this moment (warm-up before it)
    news: NewsCalendar | None = None
    trades: list[Trade] = field(default_factory=list)
    skips: Counter = field(default_factory=Counter)
    position: Position | None = None

    def __post_init__(self) -> None:
        cfg = self.settings
        self._trigger = Trigger(LevelBook(cfg.strength), cfg.min_body) if cfg.entry == LEVEL else None
        self._guard = DayGuard() if cfg.daily_limits else None
        self._forming: list | None = None           # the 30-minute candle being built: [start, o, h, l, c]
        self._heights: list[float] = []             # heights of the last closed 30-minute candles
        self._four_closes: list[float] = []         # closes of completed 4-hour candles
        self._four_block: int | None = None         # the 4-hour block being built
        self._four_close = 0.0
        self._last_time: int | None = None

    # ------------------------------------------------------------------ loop
    def on_bar(self, bar: Bar) -> None:
        if self._last_time is not None and bar.time <= self._last_time:
            raise ValueError("bars must be in time order with no repeats (at %d)" % bar.time)
        self._last_time = bar.time

        signal = None
        if self._forming is not None and bar.time >= self._forming[0] + 1800:
            start, open_, high, low, close = self._forming
            self._forming = None
            signal = self._judge(Candle(start, open_, high, low, close, 1800))
        if signal is not None:
            self._enter(signal[0], signal[1], bar)
        if self.position is not None:
            self.position.on_bar(bar)
            if not self.position.open:
                self._book_result()
        self._absorb(bar)

    def _absorb(self, bar: Bar) -> None:
        """Add the bar to the 30-minute candle and the 4-hour candle being built."""
        start = bar.time - bar.time % 1800
        if self._forming is None:
            self._forming = [start, bar.open, bar.high, bar.low, bar.close]
        else:
            self._forming[2] = max(self._forming[2], bar.high)
            self._forming[3] = min(self._forming[3], bar.low)
            self._forming[4] = bar.close
        block = server_seconds(bar.time) // FOUR_HOURS
        if self._four_block is not None and block != self._four_block:
            self._four_closes.append(self._four_close)
            del self._four_closes[:-(DEFAULT_LOOKBACK + 1)]
        self._four_block, self._four_close = block, bar.close

    # -------------------------------------------------------------- deciding
    def _direction(self, now: int) -> str:
        """The closes rule from 4-hour candles that had closed by `now`."""
        closes = list(self._four_closes)
        if self._four_block is not None and server_seconds(now) // FOUR_HOURS > self._four_block:
            closes.append(self._four_close)             # the block being built ended before `now`
        return direction_of_closes(closes[-(DEFAULT_LOOKBACK + 1):], DEFAULT_LOOKBACK)

    def _judge(self, candle: Candle):
        """Is this closed candle a signal? Returns (Signal, average candle height) or None."""
        cfg = self.settings
        self._heights.append(candle.range)
        del self._heights[:-AVERAGE_OVER]
        now = candle.close_time
        reading = self._direction(now) if cfg.use_direction else None

        if self._trigger is not None:
            result = self._trigger.on_candle(candle, reading)
            if isinstance(result, Skip):
                self.skips[result.reason] += 1
                return None
            if not isinstance(result, Signal):
                return None
            signal, average = result, self._trigger.book.reach / ZONE_SHARE
        else:
            if candle.body_share < cfg.min_body or not (candle.bullish or candle.bearish):
                return None
            side = BUY if candle.bullish else SELL
            if reading is not None and not allows(reading, side):
                return None
            signal, average = Signal(side, None, candle, candle.body_share, 0), sum(self._heights) / len(self._heights)

        if cfg.session_hours is not None and not in_session(now, cfg.session_hours):
            self.skips["outside_session"] += 1
            return None
        return signal, average

    def _enter(self, signal: Signal, average: float, bar: Bar) -> None:
        cfg = self.settings
        now = signal.time
        if self.position is not None:
            self.skips["position_open"] += 1
            return
        if bar.time - now > ENTRY_WINDOW:
            self.skips["no_entry_minute"] += 1
            return
        if self.trade_from is not None and bar.time < self.trade_from:
            self.skips["warm_up"] += 1
            return
        if cfg.max_spread is not None and bar.spread > cfg.max_spread:
            self.skips["spread_too_wide"] += 1
            return
        if self.news is not None and self.news.blocked(bar.time):
            self.skips["news"] += 1
            return
        if self._guard is not None:
            limit = self._guard.blocked(bar.time)
            if limit:
                self.skips[limit] += 1
                return
        plan = plan_trade(signal, bar.open, bar.spread, self.balance, average, self.contract, cfg.risk_share)
        if isinstance(plan, NoTrade):
            self.skips[plan.reason] += 1
            return
        target = target_price(plan, None, bar.spread, cfg.target_r if cfg.target_r is not None else NO_TARGET_R)
        self.position = Position(plan, target, cfg.style, bar.time, stop_buffer=bar.spread)
        if self._guard is not None:
            self._guard.opened(bar.time)

    def _book_result(self) -> None:
        position = self.position
        closed_at = position.fills[-1].time
        self.trades.append(Trade(position.opened_at, closed_at, position.plan.side, position.plan.entry,
                                 position.plan.stop, position.plan.lots, position.last_reason,
                                 position.result_r, position.money))
        self.balance += position.money
        if self._guard is not None:
            self._guard.closed(closed_at, position.result_r)
        self.position = None


def run(bars, settings: Settings, balance: float, trade_from: int | None = None, contract: Contract | None = None,
        compound: bool = True) -> Bot:
    """Feed bars to a fresh bot and return it. With `compound` off, every trade is sized on the
    starting balance, so results in R are not affected by the order of wins and losses."""
    bot = Bot(settings, balance, contract or Contract(), trade_from)
    for bar in bars:
        bot.on_bar(bar)
        if not compound:
            bot.balance = balance
    return bot
