"""The final test: validation, then holdout, once each. The rules are in research/PROTOCOL.md.

    python -m research.final_test --bars PATH_TO/bars_m1.csv --stage validation --out data/final
    python -m research.final_test --bars PATH_TO/bars_m1.csv --stage holdout --out data/final

Stage "validation" first checks that this tool reproduces run 004 on the development part, then
runs the four candidates on the validation part and chooses the primary. Stage "holdout" runs the
primary once on the holdout part and gives the verdict. Each stage writes a lock file and refuses
to run twice.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

from rajabot.candles import NEW_YORK, Bar
from rajabot.data import read_mt5_bars
from rajabot.engine import LEVEL, Settings, run

from .signal_check import DEVELOPMENT_ENDS, _commit

VALIDATION_ENDS = int(datetime(2026, 5, 24, tzinfo=timezone.utc).timestamp())      # research/DATA_SPLIT.md
WARM_UP = 14 * 86400
NOTIONAL = 1_000_000.0          # every trade sized on this, so results in R do not depend on their order
RISK = 0.005
PROTOCOL = Path(__file__).resolve().parent / "PROTOCOL.md"

CANDIDATES = [
    Settings("1: any convincing candle, 07:00-16:00, target 2R", target_r=2.0),
    Settings("2: any convincing candle, 07:00-16:00, no target", target_r=None),
    Settings("3: any convincing candle, 07:00-13:00, no target", target_r=None, session_hours=(7, 13)),
    Settings("4: level break only, 07:00-16:00, no target", entry=LEVEL, target_r=None),
]
# Run 004 on the development part, lesson 8 rules off: (candidate index, trades, total R).
RUN_004 = [(0, 646, 68.1), (1, 499, 87.5), (3, 152, 22.6)]

MIN_TRADES = 100
PASS_PROFIT_FACTOR = 1.20
PASS_DRAWDOWN = 0.15
PASS_STRESS_PROFIT_FACTOR = 1.05
RESAMPLES = 10_000


def fingerprint() -> str:
    """A fingerprint of the protocol and the candidates. If either changes, this changes."""
    digest = hashlib.sha256(PROTOCOL.read_bytes().replace(b"\r\n", b"\n"))
    digest.update(repr(CANDIDATES).encode())
    return digest.hexdigest()


# -------------------------------------------------------------------- numbers
def profit_factor(results: list[float]) -> float:
    gains = sum(x for x in results if x > 0)
    losses = -sum(x for x in results if x < 0)
    return gains / losses if losses else float("inf")


def drawdown(results: list[float], risk: float = RISK) -> tuple[float, float]:
    """(fall from a peak on closed trades, cautious bound) as shares of the account.

    The balance grows by risk x R each trade. The bound assumes, before every trade, that the
    trade's whole risk is lost, and measures the fall from the highest balance so far.
    """
    balance = peak = 1.0
    closed = bound = 0.0
    for r in results:
        bound = max(bound, 1 - balance * (1 - risk) / peak)
        balance *= 1 + risk * r
        peak = max(peak, balance)
        closed = max(closed, 1 - balance / peak)
    return closed, bound


def likely_range(results: list[float], resamples: int = RESAMPLES, seed: int = 1) -> tuple[float, float]:
    """A 95% range for the average R, by resampling the trades."""
    if len(results) < 2:
        return float("nan"), float("nan")
    rng, n = random.Random(seed), len(results)
    means = sorted(sum(rng.choices(results, k=n)) / n for _ in range(resamples))
    return means[int(0.025 * resamples)], means[int(0.975 * resamples) - 1]


def summarise(trades) -> dict:
    results = [t.r for t in trades]
    n = len(results)
    if not n:
        return {"trades": 0, "average": 0.0, "profit_factor": 0.0, "total": 0.0, "winners": 0.0}
    closed, bound = drawdown(results)
    low, high = likely_range(results)
    months = defaultdict(float)
    for trade in trades:
        months[datetime.fromtimestamp(trade.opened_at, timezone.utc).astimezone(NEW_YORK).strftime("%Y-%m")] += trade.r
    return {"trades": n, "winners": sum(1 for x in results if x > 0) / n, "average": sum(results) / n,
            "profit_factor": profit_factor(results), "total": sum(results), "drawdown_closed": closed,
            "drawdown_bound": bound, "low": low, "high": high, "months": dict(sorted(months.items())),
            "ends": dict(Counter(t.reason for t in trades)),
            "buys": sum(1 for t in trades if t.side == "buy"),
            "buy_average": _mean([t.r for t in trades if t.side == "buy"]),
            "sell_average": _mean([t.r for t in trades if t.side == "sell"]),
            "median_minutes": median((t.closed_at - t.opened_at) // 60 for t in trades)}


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def choose_primary(summaries: list[dict]) -> int | None:
    """Protocol section 3: at least 100 trades and an average above 0 R; then the highest average.
    A tie goes to the lower number. None when no candidate qualifies."""
    eligible = [index for index, s in enumerate(summaries) if s["trades"] >= MIN_TRADES and s["average"] > 0]
    if not eligible:
        return None
    return max(eligible, key=lambda index: (summaries[index]["average"], -index))


def verdict(real: dict, stressed: dict) -> tuple[str, list[tuple[str, str, str, bool]]]:
    """Protocol section 5: the label, and each gate as (name, requirement, measured, met)."""
    sample = real["trades"] >= MIN_TRADES
    economic = real["trades"] > 0 and real["profit_factor"] >= PASS_PROFIT_FACTOR and real["average"] > 0
    risk = real["trades"] > 0 and real["drawdown_bound"] <= PASS_DRAWDOWN
    robust = stressed["trades"] > 0 and stressed["profit_factor"] >= PASS_STRESS_PROFIT_FACTOR
    certain = real["trades"] > 1 and real["low"] > 0
    gates = [
        ("Sample", "at least %d closed trades" % MIN_TRADES, "%d" % real["trades"], sample),
        ("Economic", "profit factor >= %.2f and average > 0 R" % PASS_PROFIT_FACTOR,
         "profit factor %.4f, average %+.4f R" % (real["profit_factor"], real["average"]), economic),
        ("Risk", "largest fall <= %d%%" % round(100 * PASS_DRAWDOWN),
         "%.2f%% (cautious bound); %.2f%% on closed trades" % (
             100 * real.get("drawdown_bound", 0), 100 * real.get("drawdown_closed", 0)), risk),
        ("Robustness", "profit factor >= %.2f with spreads doubled" % PASS_STRESS_PROFIT_FACTOR,
         "profit factor %.4f" % stressed["profit_factor"], robust),
        ("Uncertainty", "lower end of the 95% range > 0 R",
         "%+.4f to %+.4f R" % (real.get("low", float("nan")), real.get("high", float("nan"))), certain),
    ]
    if not sample:
        label = "INCONCLUSIVE"
    elif not (economic and risk and robust):
        label = "FAIL"
    elif not certain:
        label = "PROVISIONAL"
    else:
        label = "ROBUST PASS"
    return label, gates


# ----------------------------------------------------------------------- runs
def run_candidate(bars: list[Bar], settings: Settings, trade_from: int | None):
    return run(bars, settings, NOTIONAL, trade_from=trade_from, compound=False)


def stressed(bars: list[Bar], settings: Settings, trade_from: int | None):
    """The same run with every spread doubled, and the spread limit doubled with it."""
    from dataclasses import replace
    doubled = [bar._replace(spread=bar.spread * 2) for bar in bars]
    wider = replace(settings, max_spread=None if settings.max_spread is None else settings.max_spread * 2)
    return run(doubled, wider, NOTIONAL, trade_from=trade_from, compound=False)


def check_against_run_004(development: list[Bar]) -> list[str]:
    """Protocol section 3.1. Returns the mismatches; an empty list means the tool reproduces run 004."""
    from dataclasses import replace
    problems = []
    for index, trades, total in RUN_004:
        open_rules = replace(CANDIDATES[index], max_spread=None, daily_limits=False)
        bot = run_candidate(development, open_rules, None)
        got_total = sum(t.r for t in bot.trades)
        if len(bot.trades) != trades or abs(got_total - total) > 0.05:
            problems.append("candidate %d: expected %d trades and %+.1f R, got %d trades and %+.2f R" % (
                index + 1, trades, total, len(bot.trades), got_total))
    return problems


def _row(name: str, s: dict, stress: dict | None = None) -> str:
    if not s["trades"]:
        return "| %s | 0 | | | | | | |" % name
    return "| %s | %d | %.1f%% | %+.3f | %+.3f to %+.3f | %.2f | %+.1f | %.1f%% | %s |" % (
        name, s["trades"], 100 * s["winners"], s["average"], s["low"], s["high"], s["profit_factor"], s["total"],
        100 * s["drawdown_bound"], ("%.2f" % stress["profit_factor"]) if stress and stress["trades"] else "")


HEAD = ("| | Trades | Winners | Average R | 95% range | Profit factor | Total R | Largest fall | Profit factor, spread doubled |\n"
        "|---|---|---|---|---|---|---|---|---|")


def _detail(s: dict) -> list[str]:
    if not s["trades"]:
        return []
    out = ["- Buys: %d trades, %+.3f R each. Sells: %d trades, %+.3f R each." % (
               s["buys"], s["buy_average"], s["trades"] - s["buys"], s["sell_average"]),
           "- How they ended: " + ", ".join("%s %d" % item for item in sorted(s["ends"].items())) + ".",
           "- Median time in a trade: %d minutes." % s["median_minutes"],
           "", "| Month | Total R |", "|---|---|"]
    out += ["| %s | %+.1f |" % item for item in s["months"].items()]
    positive = sum(1 for value in s["months"].values() if value > 0)
    out += ["", "Months with a profit: %d of %d." % (positive, len(s["months"]))]
    return out


def validation(path, point: float, out: Path, check_run_004: bool = True) -> tuple[str, dict]:
    lock = out / "validation.json"
    if lock.exists():
        raise SystemExit("Validation was already run. Its result is in %s. It runs once (PROTOCOL.md, section 7)." % lock)
    development = read_mt5_bars(path, point, before=DEVELOPMENT_ENDS)
    if check_run_004:
        problems = check_against_run_004(development)
        if problems:
            raise SystemExit("The tool does not reproduce run 004, so the validation part was NOT loaded:\n  "
                             + "\n  ".join(problems))
    as_built = [(c, summarise(run_candidate(development, c, None).trades), summarise(stressed(development, c, None).trades))
                for c in CANDIDATES]
    del development

    bars = read_mt5_bars(path, point, before=VALIDATION_ENDS, not_before=DEVELOPMENT_ENDS - WARM_UP)
    if not bars or bars[-1].time < DEVELOPMENT_ENDS:
        raise SystemExit("The price file has no bars in the validation part.")
    rows = []
    for candidate in CANDIDATES:
        bot = run_candidate(bars, candidate, DEVELOPMENT_ENDS)
        rows.append((candidate, summarise(bot.trades), summarise(stressed(bars, candidate, DEVELOPMENT_ENDS).trades),
                     dict(bot.skips)))
    primary = choose_primary([row[1] for row in rows])
    iso = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")
    first_traded = next(bar.time for bar in bars if bar.time >= DEVELOPMENT_ENDS)

    text = ["# Final test, stage 1: validation", "",
            "Rules: `research/PROTOCOL.md`, fingerprint `%s`. Code version `%s`." % (fingerprint()[:16], _commit()),
            "", "**Validation part: %s to %s.** One-minute bars in it: %d. Median spread: %.2f. Nothing from the "
            "holdout part was loaded." % (iso(first_traded), iso(bars[-1].time),
                                          sum(1 for bar in bars if bar.time >= DEVELOPMENT_ENDS),
                                          median(bar.spread for bar in bars if bar.time >= DEVELOPMENT_ENDS)),
            "", "The tool check passed: it reproduces run 004 on the development part exactly." if check_run_004
            else "The tool check against run 004 was skipped.",
            "", "## The four candidates on the validation part", "", HEAD]
    text += [_row(candidate.name, real, stress) for candidate, real, stress, _ in rows]
    text += ["", "Largest fall is the cautious bound, at 0.5% risk a trade.", ""]
    if primary is None:
        text += ["## Outcome: STOPPED AT VALIDATION", "",
                 "No candidate had at least %d trades and an average above 0 R. By the rules fixed in advance, "
                 "the holdout part is not opened." % MIN_TRADES]
    else:
        text += ["## The primary: candidate %s" % rows[primary][0].name, "",
                 "Chosen by the rule fixed in advance: at least %d trades and an average above 0 R, then the "
                 "highest average R. This is the only version that will be run on the holdout part." % MIN_TRADES]
    for candidate, real, _, skips in rows:
        text += ["", "### Candidate %s" % candidate.name, ""] + _detail(real)
        text += ["", "Signals not traded: " + (", ".join("%s %d" % item for item in sorted(skips.items())) or "none") + "."]
    text += ["", "## For reference: the same four on the development part, as the bot will run", "",
             "With the lesson 8 rules on (spread limit, daily limits). The development part was already used to "
             "choose these candidates, so this is not evidence.", "", HEAD]
    text += [_row(candidate.name, real, stress) for candidate, real, stress in as_built]
    text = "\n".join(text) + "\n"

    data = {"stage": "validation", "fingerprint": fingerprint(), "commit": _commit(),
            "primary": primary, "primary_name": None if primary is None else rows[primary][0].name,
            "candidates": {candidate.name: {k: v for k, v in real.items()} for candidate, real, _, _ in rows}}
    out.mkdir(parents=True, exist_ok=True)
    lock.write_text(json.dumps(data, indent=1), encoding="utf-8")
    (out / "validation.md").write_text(text, encoding="utf-8")
    return text, data


def holdout(path, point: float, out: Path) -> tuple[str, dict]:
    first = out / "validation.json"
    lock = out / "holdout.json"
    if not first.exists():
        raise SystemExit("Run the validation stage first (PROTOCOL.md, section 3).")
    if lock.exists():
        raise SystemExit("The holdout was already run. Its result is in %s. It runs once (PROTOCOL.md, section 7)." % lock)
    chosen = json.loads(first.read_text(encoding="utf-8"))
    if chosen["fingerprint"] != fingerprint():
        raise SystemExit("The protocol or the candidates changed after validation. The holdout will not be run.")
    if chosen["primary"] is None:
        raise SystemExit("Validation stopped with no primary. By the rules, the holdout is not opened.")
    primary = CANDIDATES[chosen["primary"]]

    bars = read_mt5_bars(path, point, not_before=VALIDATION_ENDS - WARM_UP)
    if not bars or bars[-1].time < VALIDATION_ENDS:
        raise SystemExit("The price file has no bars in the holdout part.")
    bot = run_candidate(bars, primary, VALIDATION_ENDS)
    real = summarise(bot.trades)
    stress = summarise(stressed(bars, primary, VALIDATION_ENDS).trades)
    small = run(bars, primary, 10_000.0, trade_from=VALIDATION_ENDS)          # a real 10,000 account, real lot steps
    label, gates = verdict(real, stress)
    iso = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")
    in_part = [bar for bar in bars if bar.time >= VALIDATION_ENDS]

    text = ["# Final test, stage 2: holdout", "",
            "Rules: `research/PROTOCOL.md`, fingerprint `%s`. Code version `%s`." % (fingerprint()[:16], _commit()),
            "", "**Holdout part: %s to %s.** One-minute bars in it: %d. Median spread: %.2f." % (
                iso(in_part[0].time), iso(in_part[-1].time), len(in_part), median(bar.spread for bar in in_part)),
            "", "**The primary, chosen on validation:** candidate %s." % primary.name,
            "", "# Outcome: %s" % label, "",
            "Gates compare unrounded figures.", "",
            "| Gate | Requirement | Measured | |", "|---|---|---|---|"]
    text += ["| %s | %s | %s | %s |" % (name, need, got, "met" if met else "NOT met") for name, need, got, met in gates]
    text += ["", "## The run", "", HEAD, _row("Holdout", real, stress), _row("Holdout, spreads doubled", stress),
             ""] + _detail(real)
    text += ["", "Signals not traded: " + (", ".join("%s %d" % item for item in sorted(bot.skips.items())) or "none") + ".",
             "", "## For information: a 10,000 account with real lot steps", "",
             "Decides nothing. Sizes are rounded down to 0.01 lots and the balance compounds.", "",
             "- Trades: %d. Final balance: %.2f from 10000.00." % (len(small.trades), small.balance),
             "- Smallest and largest trade: %s lots." % (
                 "%.2f to %.2f" % (min(t.lots for t in small.trades), max(t.lots for t in small.trades))
                 if small.trades else "none"),
             "", "## What this cannot say", "",
             "- It describes six months of the past. It is not a forecast, and the label is not a promise.",
             "- News was not excluded. Fills are simulated from one-minute bars; real stops slip more.",
             "- Whatever the label, nothing here is a reason to trade real money."]
    text = "\n".join(text) + "\n"

    data = {"stage": "holdout", "fingerprint": fingerprint(), "commit": _commit(), "primary": primary.name,
            "label": label, "real": real, "stressed": stress,
            "gates": [{"gate": name, "requirement": need, "measured": got, "met": met} for name, need, got, met in gates]}
    lock.write_text(json.dumps(data, indent=1), encoding="utf-8")
    (out / "holdout.md").write_text(text, encoding="utf-8")
    return text, data


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--bars", required=True, help="the MT5 export CSV of one-minute bars")
    parser.add_argument("--point", type=float, default=0.01, help="size of one point as a price (0.01 for gold)")
    parser.add_argument("--stage", required=True, choices=("validation", "holdout"))
    parser.add_argument("--out", default="data/final", help="folder for the reports and the lock files")
    args = parser.parse_args(argv)
    text, _ = (validation if args.stage == "validation" else holdout)(args.bars, args.point, Path(args.out))
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
