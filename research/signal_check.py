"""Signal check: after a signal, does gold keep going more often than a coin flip?

The bot has no stop, target or position size yet (lessons 5 to 7), so this is not a profit
backtest. It asks the one question that can be asked of the trigger on its own:

    Enter on the minute after the signal. Which comes first: one "unit" in our favour, or one
    unit against us?

One unit is the average height of the last 20 closed 30-minute candles at the signal. A win is
+1, a loss is -1, and a signal still undecided after 24 hours is closed at the price then. The
spread is paid: buys enter at the ask and exit at the bid, sells the reverse. If one minute
touches both sides, it is counted as a loss.

With no edge at all the win share is 50% and the average is a little below zero (the spread).

It loads ONLY the development part of the history (research/DATA_SPLIT.md).

    python -m research.signal_check --bars PATH_TO/bars_m1.csv --out data/signal_check
"""
from __future__ import annotations

import argparse
import bisect
import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

from rajabot.candles import NEW_YORK, Bar, build_broker_candles, build_candles
from rajabot.data import read_mt5_bars
from rajabot.filters import SESSION_HOURS, in_session
from rajabot.direction import (BUY, DAILY_LOOKBACK, DEFAULT_LOOKBACK, DOWN, FLAT, MIXED, SELL, STRUCTURE_STRENGTH,
                               UNKNOWN, UP, allows, combine, direction_of_closes)
from rajabot.levels import HIGH, ZONE_SHARE, LevelBook, find_swings
from rajabot.trigger import Signal, Skip, Trigger

DEVELOPMENT_ENDS = int(datetime(2025, 11, 23, tzinfo=timezone.utc).timestamp())      # research/DATA_SPLIT.md
ENTRY_WINDOW = 300          # the entry minute must start within 5 minutes of the signal
TIME_LIMIT = 86400          # undecided after 24 hours: closed at the price then

# One change at a time from the base, so each line answers one question. Fixed before any data.
BASE = dict(strength=4, min_body=0.5, min_turns=1, readings=())
VARIANTS = [
    ("Base: strength 4, body 50%, any level, no direction filter", {}),
    ("Strength 2 (more, minor levels)", dict(strength=2)),
    ("Strength 8 (fewer, major levels)", dict(strength=8)),
    ("Body at least 65%", dict(min_body=0.65)),
    ("Body at least 80%", dict(min_body=0.8)),
    ("Level held at least twice", dict(min_turns=2)),
    ("Direction: closes rule", dict(readings=("closes",))),
    ("Direction: structure", dict(readings=("structure",))),
    ("Direction: daily background", dict(readings=("daily",))),
    ("Direction: all three agree", dict(readings=("closes", "structure", "daily"))),
]
NO_LEVEL = [
    ("No level at all: every convincing candle (body 50%)", dict(readings=())),
    ("No level, with the closes rule", dict(readings=("closes",))),
    ("No level, New York session only", dict(session=True)),
    ("No level, New York session + closes rule", dict(session=True, readings=("closes",))),
]

# Added for the second run. Every piece of these was written down before any price was seen: the
# session hours and the closes rule in the owner's research notes (the earlier study's D5 and D6),
# level quality in lesson 2. Only the act of combining them came after the first run.
COMBINED = [
    ("New York session only (07:00-16:00)", dict(session=True)),
    ("Session + closes rule", dict(session=True, readings=("closes",))),
    ("Session + level held at least twice", dict(session=True, min_turns=2)),
    ("Session + closes rule + level held at least twice", dict(session=True, readings=("closes",), min_turns=2)),
]
# These two come from looking at the first run's tables. That is hindsight: they are here to be
# watched with suspicion, not trusted.
HINDSIGHT = [
    ("Level held at least three times", dict(min_turns=3)),
    ("Session + closes rule + level held at least three times", dict(session=True, readings=("closes",), min_turns=3)),
]


# ------------------------------------------------------------------- readings
class Readings:
    """The three direction readings of lesson 3 at any moment, from closed candles only."""

    def __init__(self, bars: list[Bar]) -> None:
        end = bars[-1].time + 7 * 86400
        self.four = build_broker_candles(bars, 4, as_of=end)
        self.four_closed = [c.close_time for c in self.four]
        self.four_closes = [c.close for c in self.four]
        self.daily = build_broker_candles(bars, 24, as_of=end)
        self.daily_closed = [c.close_time for c in self.daily]
        self.daily_closes = [c.close for c in self.daily]
        # structure: the last two peaks and dips known after each swing was confirmed
        self.swing_times, self.swing_state = [], []
        peaks, dips = [], []
        for swing in find_swings(self.four, STRUCTURE_STRENGTH):
            (peaks if swing.kind == HIGH else dips).append(swing.price)
            self.swing_times.append(swing.usable_from)
            self.swing_state.append((tuple(peaks[-2:]), tuple(dips[-2:])))

    def at(self, now: int) -> dict:
        n = bisect.bisect_right(self.four_closed, now)
        closes = direction_of_closes(self.four_closes[max(0, n - DEFAULT_LOOKBACK - 1):n], DEFAULT_LOOKBACK)
        d = bisect.bisect_right(self.daily_closed, now)
        daily = direction_of_closes(self.daily_closes[max(0, d - DAILY_LOOKBACK - 1):d], DAILY_LOOKBACK)
        k = bisect.bisect_right(self.swing_times, now)
        structure = UNKNOWN
        if k:
            peaks, dips = self.swing_state[k - 1]
            if len(peaks) == 2 and len(dips) == 2:
                if peaks[1] > peaks[0] and dips[1] > dips[0]:
                    structure = UP
                elif peaks[1] < peaks[0] and dips[1] < dips[0]:
                    structure = DOWN
                else:
                    structure = MIXED
        return {"closes": closes, "structure": structure, "daily": daily}


# -------------------------------------------------------------------- outcome
def follow(bars: list[Bar], times: list[int], signal_time: int, side: str, unit: float,
           spread_mult: float = 1.0) -> tuple[float, str] | None:
    """What happened after a signal: (result in units, "win" / "loss" / "timeout").

    None when there is no entry minute within 5 minutes, the unit is not positive, or the history
    ends before the signal is decided.
    """
    if unit <= 0:
        return None
    start = bisect.bisect_left(times, signal_time)
    if start >= len(bars) or bars[start].time - signal_time > ENTRY_WINDOW:
        return None
    first = bars[start]
    entry = first.open + first.spread * spread_mult if side == BUY else first.open
    deadline = first.time + TIME_LIMIT
    for index in range(start, len(bars)):
        bar = bars[index]
        spread = bar.spread * spread_mult
        if bar.time >= deadline:
            exit_price = bar.open if side == BUY else bar.open + spread
            moved = exit_price - entry if side == BUY else entry - exit_price
            return moved / unit, "timeout"
        if side == BUY:                                   # a buy is closed at the bid
            if bar.low <= entry - unit:
                return -1.0, "loss"
            if bar.high >= entry + unit:
                return 1.0, "win"
        else:                                             # a sell is closed at the ask
            if bar.high + spread >= entry + unit:
                return -1.0, "loss"
            if bar.low + spread <= entry - unit:
                return 1.0, "win"
    return None


# ----------------------------------------------------------------------- runs
def session_of(utc_seconds: int) -> str:
    hour = datetime.fromtimestamp(utc_seconds, timezone.utc).astimezone(NEW_YORK).hour
    if hour < 3:
        return "00-03 New York (Asia)"
    if hour < 7:
        return "03-07 New York (London)"
    if hour < 12:
        return "07-12 New York (NY morning)"
    if hour < 17:
        return "12-17 New York (NY afternoon)"
    return "17-24 New York (evening)"


def run_variant(bars, times, candles, readings: Readings, settings: dict) -> dict:
    cfg = {**BASE, "session": False, **settings}
    trigger = Trigger(LevelBook(cfg["strength"]), cfg["min_body"], cfg["min_turns"])
    rows, skips = [], Counter()
    for candle in candles:
        seen = readings.at(candle.close_time)
        reading = combine(*[seen[name] for name in cfg["readings"]]) if cfg["readings"] else None
        result = trigger.on_candle(candle, reading)
        if isinstance(result, Skip):
            skips[result.reason] += 1
        elif isinstance(result, Signal):
            if cfg["session"] and not in_session(result.time):
                skips["outside_session"] += 1
                continue
            unit = trigger.book.reach / ZONE_SHARE
            rows.append(_row(bars, times, result.time, result.side, unit, seen,
                             body=result.body_share, turns=result.turns))
    return {"rows": [r for r in rows if r], "skips": dict(skips), "no_outcome": sum(1 for r in rows if r is None)}


def run_no_level(bars, times, candles, readings: Readings, settings: dict) -> dict:
    """Every convincing candle is a 'signal', level or no level: what the levels must beat."""
    cfg = {**BASE, "session": False, **settings}
    heights, rows = [], []
    for candle in candles:
        heights.append(candle.range)
        del heights[:-20]
        if candle.body_share < cfg["min_body"] or not (candle.bullish or candle.bearish):
            continue
        side = BUY if candle.bullish else SELL
        if cfg["session"] and not in_session(candle.close_time):
            continue
        seen = readings.at(candle.close_time)
        if cfg["readings"] and not allows(combine(*[seen[name] for name in cfg["readings"]]), side):
            continue
        rows.append(_row(bars, times, candle.close_time, side, sum(heights) / len(heights), seen,
                         body=candle.body_share, turns=0))
    return {"rows": [r for r in rows if r], "skips": {}, "no_outcome": sum(1 for r in rows if r is None)}


def _row(bars, times, when, side, unit, seen, body, turns):
    once = follow(bars, times, when, side, unit)
    twice = follow(bars, times, when, side, unit, spread_mult=2.0)
    if once is None or twice is None:
        return None
    agrees = {name: ("agrees" if allows(value, side) else "no clear reading" if value in (UNKNOWN, MIXED, FLAT)
                     else "disagrees") for name, value in seen.items()}
    return {"time": when, "side": side, "unit": unit, "result": once[0], "kind": once[1], "result_2x": twice[0],
            "body": body, "turns": turns, "session": session_of(when), **{"dir_" + k: v for k, v in agrees.items()}}


# -------------------------------------------------------------------- summary
def summarise(rows: list[dict]) -> dict:
    n = len(rows)
    if not n:
        return {"signals": 0}
    results = [r["result"] for r in rows]
    mean = sum(results) / n
    spread = math.sqrt(sum((x - mean) ** 2 for x in results) / (n - 1)) / math.sqrt(n) if n > 1 else float("nan")
    wins = sum(1 for r in rows if r["kind"] == "win")
    losses = sum(1 for r in rows if r["kind"] == "loss")
    return {"signals": n, "wins": wins, "losses": losses, "timeouts": n - wins - losses,
            "win_share": wins / (wins + losses) if wins + losses else float("nan"),
            "average": mean, "low": mean - 1.96 * spread, "high": mean + 1.96 * spread,
            "average_2x": sum(r["result_2x"] for r in rows) / n}


def breakdown(rows: list[dict], key) -> list[tuple[str, dict]]:
    groups = defaultdict(list)
    for row in rows:
        groups[key(row)].append(row)
    return [(name, summarise(groups[name])) for name in sorted(groups)]


def _half_year(utc_seconds: int) -> str:
    when = datetime.fromtimestamp(utc_seconds, timezone.utc)
    return "%d %s half" % (when.year, "first" if when.month <= 6 else "second")


def _line(name: str, s: dict) -> str:
    if not s.get("signals"):
        return "| %s | 0 | | | | |" % name
    return "| %s | %d | %.1f%% | %+.3f | %+.3f to %+.3f | %+.3f |" % (
        name, s["signals"], 100 * s["win_share"], s["average"], s["low"], s["high"], s["average_2x"])


HEAD = "| | Signals | Win share | Average (units) | Likely range | Average, spread doubled |\n|---|---|---|---|---|---|"


def report(facts: dict, variants: list, no_level: list, combined: list = (), hindsight: list = ()) -> str:
    out = ["# Signal check on the development part", "",
           "**Not a profit backtest.** The bot has no stop, target or size yet. This asks one question of the "
           "trigger alone: after a signal, which comes first, one unit our way or one unit against us? One unit "
           "is the average height of the last 20 thirty-minute candles. A coin flip gives a 50% win share and an "
           "average a little below zero, because the spread is paid.", "",
           "**Development part only** (%s to %s). Nothing after 2025-11-23 was loaded. A result here is a clue, "
           "not a verdict." % (facts["first"], facts["last"]), "",
           "- One-minute bars: %d. Thirty-minute candles: %d. Median spread: %.2f." % (
               facts["bars"], facts["candles"], facts["median_spread"]),
           "- Median unit: %.2f. So the spread costs about %.3f units per signal, and with no edge at all "
           "the win share would be about %.1f%%." % (
               facts["median_unit"], facts["median_spread"] / facts["median_unit"] if facts["median_unit"] else 0,
               100 * (0.5 - facts["median_spread"] / (2 * facts["median_unit"])) if facts["median_unit"] else 50),
           "- Code version: `%s`." % facts["commit"],
           "- \"Likely range\" is a rough 95% range for the average. Signals overlap in time, so the true "
           "range is wider than shown.", "",
           "## One change at a time", "", HEAD]
    for name, result in variants:
        out.append(_line(name, summarise(result["rows"])))
    if combined:
        out += ["", "## Combinations", "",
                "Each piece was written down before any price was seen (session hours and the closes rule in "
                "the research notes, level quality in lesson 2). Compare each line with its no-level twin "
                "in the next table.", "", HEAD]
        out += [_line(name, summarise(result["rows"])) for name, result in combined]
    if hindsight:
        out += ["", "## Suggested by the first run (hindsight)", "",
                "These were picked after seeing the first run's tables. A setting chosen because it looked "
                "good will look good again on the same data. Watch, do not trust.", "", HEAD]
        out += [_line(name, summarise(result["rows"])) for name, result in hindsight]
    out += ["", "## What the levels must beat", "",
            "The same test on every convincing candle, whether or not it broke a level. If these lines do as "
            "well as the ones above, the levels are adding nothing.", "", HEAD]
    for name, result in no_level:
        out.append(_line(name, summarise(result["rows"])))

    base = variants[0][1]["rows"]
    cuts = [("Buy and sell", lambda r: r["side"]),
            ("Time of day", lambda r: r["session"]),
            ("Closes rule at the signal", lambda r: r["dir_closes"]),
            ("Structure at the signal", lambda r: r["dir_structure"]),
            ("Daily background at the signal", lambda r: r["dir_daily"]),
            ("Share of the signal candle that is body", lambda r: "50-65%" if r["body"] < 0.65 else "65-80%" if r["body"] < 0.8 else "80%+"),
            ("Times price had turned at the level", lambda r: "1" if r["turns"] <= 1 else "2" if r["turns"] == 2 else "3 or more"),
            ("Half-year", lambda r: _half_year(r["time"]))]
    out += ["", "## Inside the base signals", "",
            "The base signals cut different ways. This is where to look for weaknesses. Small groups swing "
            "widely by luck: read the signal count before the average."]
    for title, key in cuts:
        out += ["", "### " + title, "", HEAD]
        out += [_line(name, s) for name, s in breakdown(base, key)]
    out += ["", "## Breaks the base skipped", "", "| Reason | Count |", "|---|---|"]
    out += ["| %s | %d |" % item for item in sorted(variants[0][1]["skips"].items())] or ["| none | 0 |"]
    out += ["", "Signals with no outcome (no entry minute, or the history ended first): %d." % variants[0][1]["no_outcome"], ""]
    return "\n".join(out)


def _commit() -> str:
    try:
        root = Path(__file__).resolve().parent.parent
        text = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, timeout=10).stdout.strip()
        return text or "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def check(bars: list[Bar]) -> tuple[str, dict]:
    """Run every variant on bars already limited to the development part."""
    if bars and bars[-1].time >= DEVELOPMENT_ENDS:
        raise ValueError("these bars go past the development part: refusing to run (research/DATA_SPLIT.md)")
    if len(bars) < 5000:
        raise ValueError("too little history to check anything: %d one-minute bars" % len(bars))
    times = [bar.time for bar in bars]
    candles = build_candles(bars, 30, as_of=bars[-1].time + 3600)
    readings = Readings(bars)
    variants = [(name, run_variant(bars, times, candles, readings, settings)) for name, settings in VARIANTS]
    no_level = [(name, run_no_level(bars, times, candles, readings, settings)) for name, settings in NO_LEVEL]
    combined = [(name, run_variant(bars, times, candles, readings, settings)) for name, settings in COMBINED]
    hindsight = [(name, run_variant(bars, times, candles, readings, settings)) for name, settings in HINDSIGHT]
    units = [row["unit"] for row in variants[0][1]["rows"]]
    iso = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")
    facts = {"first": iso(bars[0].time), "last": iso(bars[-1].time), "bars": len(bars), "candles": len(candles),
             "median_spread": median(bar.spread for bar in bars), "median_unit": median(units) if units else 0.0,
             "commit": _commit()}
    data = {"facts": facts,
            "variants": {name: dict(summarise(r["rows"]), skips=r["skips"])
                         for name, r in variants + no_level + combined + hindsight}}
    return report(facts, variants, no_level, combined, hindsight), data


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--bars", required=True, help="the MT5 export CSV of one-minute bars")
    parser.add_argument("--point", type=float, default=0.01, help="size of one point as a price (0.01 for gold)")
    parser.add_argument("--out", default="data/signal_check", help="folder for report.md and report.json")
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
