"""Trade test: whole trades, entry to exit, on the development part of the history.

This is the first test that can produce a result in R. For every signal it does what the bot
would do: enter on the next minute, put the stop beyond the signal candle, size the trade, check
the room, pick the target, and manage the position minute by minute to its exit.

One trade at a time: a signal that arrives while a trade is open is skipped. Every trade risks
the same, so results are in R (multiples of the risk). The spread is paid. Sizing uses a large
notional balance so that the broker's 0.01-lot steps do not distort the comparison of exit
styles.

It loads ONLY the development part of the history (research/DATA_SPLIT.md).

    python -m research.trade_test --bars PATH_TO/bars_m1.csv --out data/trade_test
"""
from __future__ import annotations

import argparse
import bisect
import json
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

from rajabot.candles import NEW_YORK, Bar, build_candles
from rajabot.data import read_mt5_bars
from rajabot.direction import BUY, SELL, allows, combine
from rajabot.levels import HIGH, ZONE_SHARE, LevelBook
from rajabot.manage import HALVES, QUARTERS, SINGLE, TARGET, ExitStyle, Position, target_price
from rajabot.risk import Contract, NoTrade, plan_trade
from rajabot.space import check_room, measure_room
from rajabot.trigger import Signal, Skip, Trigger

from .signal_check import DEVELOPMENT_ENDS, ENTRY_WINDOW, Readings, _commit, _half_year, in_session

BALANCE = 1_000_000.0       # notional: large, so lot steps do not matter. Results are in R
QUARTERS_NO_CLOCK = ExitStyle("quarters, no time stop", QUARTERS.fractions, move_stop=True)


@dataclass(frozen=True)
class Setup:
    name: str
    use_levels: bool = True
    strength: int = 4
    min_body: float = 0.5
    readings: tuple = ("closes",)
    session: bool = True
    min_room: float | None = 1.0        # None: no room rule
    open_space: bool = True             # take trades with no level ahead
    aim_at_level: bool = True           # False: the target is always open_space_r times the risk
    open_space_r: float = 2.0
    style: ExitStyle = SINGLE
    session_hours: tuple = (7, 16)      # New York time, signal candle's close


# Fixed before the first trade test was run. One change at a time from the base.
BASE = Setup("Base: level break, New York hours, 4-hour direction, room 1.0, one target at the next level")
SETUPS = [
    BASE,
    replace(BASE, name="Exit: halves (half at halfway, stop to break-even)", style=HALVES),
    replace(BASE, name="Exit: quarters ladder with 4-hour time stop (the Sugarwood exit)", style=QUARTERS),
    replace(BASE, name="Exit: quarters ladder, no time stop", style=QUARTERS_NO_CLOCK),
    replace(BASE, name="Room at least 1.5", min_room=1.5),
    replace(BASE, name="Room at least 2.0", min_room=2.0),
    replace(BASE, name="Open space skipped", open_space=False),
    replace(BASE, name="Level as trigger only: no room rule, target always 2R", min_room=None, aim_at_level=False),
    replace(BASE, name="No hours or direction filter", readings=(), session=False),
]
BENCHMARK = Setup("Benchmark: any convincing candle, same hours and direction, target 2R", use_levels=False,
                  min_room=None, aim_at_level=False)
BENCHMARKS = [
    BENCHMARK,
    replace(BENCHMARK, name="Benchmark with the quarters ladder", style=QUARTERS),
]
LEVEL_TRIGGER = SETUPS[7]

# Added for run 004, fixed before it was run. Where to take profit, on the large sample.
NO_TARGET_R = 100.0                 # so far away that the trade runs to its stop or the end of the day
TARGETS = [
    replace(BENCHMARK, name="Benchmark, target 1R", open_space_r=1.0),
    replace(BENCHMARK, name="Benchmark, target 1.5R", open_space_r=1.5),
    replace(BENCHMARK, name="Benchmark, target 3R", open_space_r=3.0),
    replace(BENCHMARK, name="Benchmark, no target: stop or end of day", open_space_r=NO_TARGET_R),
    replace(BENCHMARK, name="Benchmark, halves at 2R", style=HALVES),
    replace(LEVEL_TRIGGER, name="Level as trigger only, no target: stop or end of day", open_space_r=NO_TARGET_R),
]
# Picked by looking at runs 001 and 003, where the afternoon did worst. Hindsight: watch, do not trust.
HINDSIGHT = [
    replace(BENCHMARK, name="Benchmark, entries 07:00 to 13:00 only", session_hours=(7, 13)),
    replace(LEVEL_TRIGGER, name="Level as trigger only, entries 07:00 to 13:00 only", session_hours=(7, 13)),
]


def run_setup(bars: list[Bar], times: list[int], candles, readings: Readings, setup: Setup) -> dict:
    """Run one setup over the history. Returns its trades and why signals were skipped."""
    trigger = Trigger(LevelBook(setup.strength), setup.min_body) if setup.use_levels else None
    shadow = None if setup.use_levels else LevelBook(setup.strength)      # only to note whether a level broke
    contract = Contract()
    heights: list[float] = []
    trades, skips = [], Counter()
    busy_until = -1                                    # time the open trade closed; signals before it are skipped

    for candle in candles:
        heights.append(candle.range)
        del heights[:-20]
        now = candle.close_time
        seen = readings.at(now)
        reading = combine(*[seen[name] for name in setup.readings]) if setup.readings else None

        broke_level = True
        if shadow is not None:
            update = shadow.add(candle)
            broke_level = any((level.kind == HIGH) == candle.bullish for level in update.broken)
        if trigger is not None:
            result = trigger.on_candle(candle, reading)
            if isinstance(result, Skip):
                skips[result.reason] += 1
                continue
            if not isinstance(result, Signal):
                continue
            signal, average = result, trigger.book.reach / ZONE_SHARE
        else:
            if candle.body_share < setup.min_body or not (candle.bullish or candle.bearish):
                continue
            side = BUY if candle.bullish else SELL
            if reading is not None and not allows(reading, side):
                continue
            signal, average = Signal(side, None, candle, candle.body_share, 0), sum(heights) / len(heights)

        if setup.session and not in_session(now, setup.session_hours):
            skips["outside_session"] += 1
            continue
        if now < busy_until:
            skips["position_open"] += 1
            continue
        start = bisect.bisect_left(times, now)
        if start >= len(bars) or bars[start].time - now > ENTRY_WINDOW:
            skips["no_entry_minute"] += 1
            continue
        first = bars[start]
        plan = plan_trade(signal, first.open, first.spread, BALANCE, average, contract)
        if isinstance(plan, NoTrade):
            skips[plan.reason] += 1
            continue

        wall = None
        if trigger is not None and setup.aim_at_level:
            room = measure_room(signal, trigger.book, plan.entry, plan.distance)
            if setup.min_room is not None:
                problem = check_room(room, setup.min_room, setup.open_space)
                if problem:
                    skips[problem] += 1
                    continue
            wall = room.wall
        target = target_price(plan, wall, first.spread, setup.open_space_r)
        reward = target - plan.entry if plan.side == BUY else plan.entry - target
        if reward <= 0:
            skips["no_reward"] += 1
            continue

        position = Position(plan, target, setup.style, first.time, stop_buffer=first.spread)
        index = start
        while position.open and index < len(bars):
            position.on_bar(bars[index])
            index += 1
        if position.open:
            skips["history_ended"] += 1
            break                                      # still in a trade when the history ends: nothing after it can be taken
        closed_at = position.fills[-1].time
        busy_until = closed_at + 60
        trades.append({"time": first.time, "side": plan.side, "r": position.result_r, "reason": position.last_reason,
                       "banked": position.banked, "minutes": (closed_at - first.time) // 60,
                       "planned_r": reward / plan.distance, "aim": "a level" if wall is not None else "open space",
                       "broke_level": broke_level})
    return {"trades": trades, "skips": dict(skips)}


# -------------------------------------------------------------------- summary
def summarise(trades: list[dict]) -> dict:
    n = len(trades)
    if not n:
        return {"trades": 0}
    results = [t["r"] for t in trades]
    mean = sum(results) / n
    error = math.sqrt(sum((x - mean) ** 2 for x in results) / (n - 1)) / math.sqrt(n) if n > 1 else float("nan")
    gains = sum(x for x in results if x > 0)
    losses = -sum(x for x in results if x < 0)
    peak = total = worst = 0.0
    for x in results:
        total += x
        peak = max(peak, total)
        worst = max(worst, peak - total)
    return {"trades": n, "win_share": sum(1 for x in results if x > 0) / n, "average": mean,
            "low": mean - 1.96 * error, "high": mean + 1.96 * error,
            "profit_factor": gains / losses if losses else float("inf"), "total": total, "drawdown": worst}


def _line(name: str, s: dict, doubled: dict | None = None) -> str:
    if not s.get("trades"):
        return "| %s | 0 | | | | | | | |" % name
    tail = "%+.3f" % doubled["average"] if doubled and doubled.get("trades") else ""
    return "| %s | %d | %.1f%% | %+.3f | %+.3f to %+.3f | %.2f | %+.1f | %.1f | %s |" % (
        name, s["trades"], 100 * s["win_share"], s["average"], s["low"], s["high"], s["profit_factor"],
        s["total"], s["drawdown"], tail)


HEAD = ("| | Trades | Winners | Average R | Likely range | Profit factor | Total R | Worst drop (R) | Average R, spread doubled |\n"
        "|---|---|---|---|---|---|---|---|---|")


def _time_of_day(utc_seconds: int) -> str:
    hour = datetime.fromtimestamp(utc_seconds, timezone.utc).astimezone(NEW_YORK).hour
    if hour < 7:
        return "before 07:00 New York"
    if hour < 10:
        return "07-10 New York"
    if hour < 13:
        return "10-13 New York"
    if hour < 17:
        return "13-17 New York"
    return "after 17:00 New York"


GROUPS = [("One change at a time", SETUPS),
          ("The benchmarks", BENCHMARKS),
          ("Where to take profit", TARGETS),
          ("Suggested by earlier runs (hindsight)", HINDSIGHT)]
NOTES = {"The benchmarks": "Every convincing candle, level or no level, under the same hours, direction and stop. A "
                           "level-based setup that cannot beat these is not earning its complexity.",
         "Where to take profit": "The same entries with the profit taken at different distances. \"No target\" "
                                 "holds until the stop or 16:50 New York.",
         "Suggested by earlier runs (hindsight)": "Picked after seeing that the afternoon did worst in runs 001 and "
                                                  "003. A setting chosen because it looked good will look good "
                                                  "again on the same data. Watch, do not trust."}


def _cuts(title: str, trades: list[dict], with_level_flag: bool) -> list[str]:
    cuts = [("Buy and sell", lambda t: t["side"]),
            ("Time of day at entry", lambda t: _time_of_day(t["time"])),
            ("Half-year", lambda t: _half_year(t["time"])),
            ("How it ended", lambda t: t["reason"])]
    if with_level_flag:
        cuts.insert(0, ("Did the signal candle also break a level?", lambda t: "yes, broke a level" if t["broke_level"] else "no level broken"))
    else:
        cuts += [("Aiming at a level, or open space", lambda t: t["aim"]),
                 ("Reward planned at entry", lambda t: "under 1.5R" if t["planned_r"] < 1.5 else "1.5R to 3R" if t["planned_r"] < 3 else "3R or more")]
    out = ["", "## Inside: " + title, "", "Small groups swing widely by luck: read the trade count before the average."]
    for name, key in cuts:
        groups = defaultdict(list)
        for trade in trades:
            groups[key(trade)].append(trade)
        out += ["", "### " + name, "", HEAD] + [_line(group, summarise(groups[group])) for group in sorted(groups)]
    if trades:
        out += ["", "Median time in a trade: %d minutes. Median reward planned: %.2fR." % (
            median(t["minutes"] for t in trades), median(t["planned_r"] for t in trades))]
    return out


def report(facts: dict, rows: list[tuple[Setup, dict, dict]]) -> str:
    by_name = {setup.name: (setup, once, twice) for setup, once, twice in rows}
    out = ["# Trade test on the development part", "",
           "Whole trades, entry to exit: stop beyond the signal candle, one trade at a time, every trade risking "
           "the same. Results are in R (multiples of the risk). The spread is paid.", "",
           "**Development part only** (%s to %s). Nothing after 2025-11-23 was loaded. A result here is a clue, "
           "not a verdict." % (facts["first"], facts["last"]), "",
           "- One-minute bars: %d. Thirty-minute candles: %d. Median spread: %.2f." % (
               facts["bars"], facts["candles"], facts["median_spread"]),
           "- Code version: `%s`." % facts["commit"],
           "- \"Likely range\" is a rough 95% range for the average R. \"Worst drop\" is the largest fall from a "
           "peak in the running total, in R.",
           "- For scale: the pass marks lesson 9 will use on unseen data are a profit factor of at least 1.20 "
           "and an average above 0 R."]
    for title, setups in GROUPS:
        present = [by_name[setup.name] for setup in setups if setup.name in by_name]
        if not present:
            continue
        out += ["", "## " + title, ""]
        if title in NOTES:
            out += [NOTES[title], ""]
        out.append(HEAD)
        out += [_line(setup.name, summarise(once["trades"]), summarise(twice["trades"])) for setup, once, twice in present]

    out += ["", "## How the trades ended", "",
            "By the last part closed. \"Stop\" includes stops that had been moved up behind banked parts, so a "
            "ladder trade can end at its stop and still be a winner.", "",
            "| | Target | Stop | Time stop | End of day |", "|---|---|---|---|---|"]
    for setup, once, _ in rows:
        ends = Counter(t["reason"] for t in once["trades"])
        out.append("| %s | %d | %d | %d | %d |" % (setup.name, ends["target"], ends["stop"], ends["time_stop"], ends["flat"]))

    ladders = [(s, o) for s, o, _ in rows if len(s.style.fractions) > 1]
    if ladders:
        out += ["", "## How far the ladders got", "",
                "How many parts of the position were closed at a target before the trade ended.", "",
                "| | 0 parts | 1 | 2 | 3 | 4 |", "|---|---|---|---|---|---|"]
        for setup, once in ladders:
            banked = Counter(t["banked"] for t in once["trades"])
            out.append("| %s | %d | %d | %d | %d | %d |" % (setup.name, banked[0], banked[1], banked[2], banked[3], banked[4]))

    for setup in (BENCHMARK, LEVEL_TRIGGER, BASE):
        if setup.name in by_name:
            out += _cuts(setup.name, by_name[setup.name][1]["trades"], with_level_flag=not setup.use_levels)

    out += ["", "## Signals the base setup did not trade", "", "| Reason | Count |", "|---|---|"]
    out += ["| %s | %d |" % item for item in sorted(by_name[BASE.name][1]["skips"].items())] or ["| none | 0 |"]
    out += ["", "## What this cannot say", "",
            "- It describes 13 months of the past. It is not a forecast.",
            "- Fills are simulated from one-minute bars. A stop fills at its price unless price jumped past it. "
            "Real stops slip more. The doubled-spread column is the allowance for that.",
            "- When one minute touches both the stop and a target, the stop is assumed first. When a target moves "
            "the stop up, the new stop applies from the next minute.",
            "- Many setups are compared on the same data. The best of many looks better than it is.", ""]
    return "\n".join(out)


def check(bars: list[Bar]) -> tuple[str, dict]:
    """Run every setup on bars already limited to the development part."""
    if bars and bars[-1].time >= DEVELOPMENT_ENDS:
        raise ValueError("these bars go past the development part: refusing to run (research/DATA_SPLIT.md)")
    if len(bars) < 5000:
        raise ValueError("too little history to test anything: %d one-minute bars" % len(bars))
    times = [bar.time for bar in bars]
    doubled = [bar._replace(spread=bar.spread * 2) for bar in bars]
    candles = build_candles(bars, 30, as_of=bars[-1].time + 3600)
    readings = Readings(bars)
    rows = [(setup, run_setup(bars, times, candles, readings, setup), run_setup(doubled, times, candles, readings, setup))
            for setup in SETUPS + BENCHMARKS + TARGETS + HINDSIGHT]
    iso = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")
    facts = {"first": iso(bars[0].time), "last": iso(bars[-1].time), "bars": len(bars), "candles": len(candles),
             "median_spread": median(bar.spread for bar in bars), "commit": _commit()}
    data = {"facts": facts, "setups": {setup.name: dict(summarise(once["trades"]), skips=once["skips"],
                                                        average_2x=summarise(twice["trades"]).get("average"))
                                       for setup, once, twice in rows}}
    return report(facts, rows), data


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--bars", required=True, help="the MT5 export CSV of one-minute bars")
    parser.add_argument("--point", type=float, default=0.01, help="size of one point as a price (0.01 for gold)")
    parser.add_argument("--out", default="data/trade_test", help="folder for report.md and report.json")
    args = parser.parse_args(argv)
    bars = read_mt5_bars(args.bars, args.point, before=DEVELOPMENT_ENDS)       # nothing later is ever read
    text, data = check(bars)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text(text, encoding="utf-8")
    (out / "report.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
