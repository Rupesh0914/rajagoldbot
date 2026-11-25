"""The final test (research/final_test.py): stages, locks and pass marks."""
import json
import os
import random
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from rajabot.candles import Bar, server_seconds
from research import final_test
from research.final_test import (VALIDATION_ENDS, choose_primary, drawdown, fingerprint, likely_range, profit_factor,
                                 verdict)
from research.signal_check import DEVELOPMENT_ENDS


def utc(*parts) -> int:
    return int(datetime(*parts, tzinfo=timezone.utc).timestamp())


def walk(start: int, end: int, seed: int) -> list[Bar]:
    rng, price, bars = random.Random(seed), 4000.0, []
    for time in range(start, end, 60):
        if datetime.fromtimestamp(time, timezone.utc).weekday() >= 5:
            continue
        open_ = high = low = price
        for _ in range(4):
            price += rng.gauss(0, 0.25)
            high, low = max(high, price), min(low, price)
        bars.append(Bar(time, round(open_, 2), round(high, 2), round(low, 2), round(price, 2), 0.16))
    return bars


def write_export(path, bars):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write("server_time,open,high,low,close,tick_volume,spread\n")
        for bar in bars:
            handle.write("%d,%.2f,%.2f,%.2f,%.2f,100,%d\n" % (
                server_seconds(bar.time), bar.open, bar.high, bar.low, bar.close, round(bar.spread * 100)))


class Numbers(unittest.TestCase):
    def test_profit_factor(self):
        self.assertAlmostEqual(profit_factor([1.5, -1, -1, 2]), 3.5 / 2)
        self.assertEqual(profit_factor([1.0, 2.0]), float("inf"))

    def test_drawdown_closed_and_cautious_bound(self):
        closed, bound = drawdown([1, -1, -1, -1, 2])
        self.assertAlmostEqual(closed, 1 - 0.995 ** 3)                # three full losses in a row from the peak
        self.assertAlmostEqual(bound, 1 - 0.995 ** 4)                 # before the fifth trade, its risk is assumed lost too
        closed, bound = drawdown([1, 1, 1])
        self.assertEqual(closed, 0.0)
        self.assertAlmostEqual(bound, 0.005)                          # even a winning run puts 0.5% at risk each time
        self.assertGreater(drawdown([-1] * 40)[1], 0.15)

    def test_the_range_brackets_the_average_and_is_repeatable(self):
        results = [1.5, -1, -1, 2, -1, 0.4] * 40
        low, high = likely_range(results)
        mean = sum(results) / len(results)
        self.assertTrue(low < mean < high)
        self.assertEqual(likely_range(results), (low, high))


class ChoosingThePrimary(unittest.TestCase):
    def s(self, trades, average):
        return {"trades": trades, "average": average}

    def test_highest_average_among_those_that_qualify(self):
        self.assertEqual(choose_primary([self.s(300, 0.05), self.s(220, 0.12), self.s(180, 0.09), self.s(70, 0.40)]), 1)

    def test_a_candidate_with_too_few_trades_cannot_win_however_good(self):
        self.assertEqual(choose_primary([self.s(300, 0.01), self.s(99, 0.90), self.s(99, 0.80), self.s(70, 0.40)]), 0)

    def test_a_tie_goes_to_the_lower_number(self):
        self.assertEqual(choose_primary([self.s(300, 0.10), self.s(220, 0.10), self.s(180, 0.02), self.s(150, 0.10)]), 0)

    def test_nothing_qualifies(self):
        self.assertIsNone(choose_primary([self.s(300, -0.01), self.s(220, 0.0), self.s(99, 0.5), self.s(0, 0.0)]))


class TheVerdict(unittest.TestCase):
    def real(self, **changes):
        base = {"trades": 250, "profit_factor": 1.30, "average": 0.15, "drawdown_bound": 0.08, "drawdown_closed": 0.07,
                "low": 0.02, "high": 0.28}
        base.update(changes)
        return base

    def label(self, real=None, stress_pf=1.15):
        return verdict(real or self.real(), {"trades": 240, "profit_factor": stress_pf})[0]

    def test_every_label(self):
        self.assertEqual(self.label(), "ROBUST PASS")
        self.assertEqual(self.label(self.real(low=-0.01)), "PROVISIONAL")
        self.assertEqual(self.label(self.real(trades=99)), "INCONCLUSIVE")
        self.assertEqual(self.label(self.real(profit_factor=1.1999)), "FAIL")          # shown as 1.20, still a fail
        self.assertEqual(self.label(self.real(average=0.0)), "FAIL")
        self.assertEqual(self.label(self.real(drawdown_bound=0.1501)), "FAIL")
        self.assertEqual(self.label(stress_pf=1.0499), "FAIL")
        self.assertEqual(self.label(self.real(trades=99, profit_factor=0.5)), "INCONCLUSIVE")     # sample comes first

    def test_exactly_on_the_marks_passes(self):
        self.assertEqual(self.label(self.real(profit_factor=1.20, drawdown_bound=0.15), stress_pf=1.05), "ROBUST PASS")

    def test_the_gates_are_listed(self):
        _, gates = verdict(self.real(), {"trades": 240, "profit_factor": 1.15})
        self.assertEqual([gate[0] for gate in gates], ["Sample", "Economic", "Risk", "Robustness", "Uncertainty"])
        self.assertTrue(all(gate[3] for gate in gates))


class TheStages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = Path(tempfile.mkdtemp())
        cls.export = cls.folder / "bars_m1.csv"
        bars = (walk(DEVELOPMENT_ENDS - 30 * 86400, DEVELOPMENT_ENDS + 45 * 86400, seed=1)
                + walk(VALIDATION_ENDS - 20 * 86400, VALIDATION_ENDS + 40 * 86400, seed=2))
        write_export(cls.export, bars)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.folder, ignore_errors=True)

    def setUp(self):
        self.out = Path(tempfile.mkdtemp(dir=self.folder))
        self.loaded = []
        real_reader = final_test.read_mt5_bars

        def spy(path, point=0.01, before=None, not_before=None):
            bars = real_reader(path, point, before=before, not_before=not_before)
            self.loaded.append((before, not_before, bars[0].time if bars else None, bars[-1].time if bars else None))
            return bars

        self._patches = {"read_mt5_bars": final_test.read_mt5_bars, "choose_primary": final_test.choose_primary}
        final_test.read_mt5_bars = spy

    def tearDown(self):
        for name, value in self._patches.items():
            setattr(final_test, name, value)

    def test_validation_never_loads_the_holdout_and_runs_once(self):
        text, data = final_test.validation(self.export, 0.01, self.out, check_run_004=False)
        self.assertTrue(all(last < VALIDATION_ENDS for _, _, _, last in self.loaded))
        self.assertEqual([before for before, _, _, _ in self.loaded], [DEVELOPMENT_ENDS, VALIDATION_ENDS])
        self.assertIn("Nothing from the holdout part was loaded.", text)
        self.assertEqual(len(data["candidates"]), 4)
        self.assertEqual(json.loads((self.out / "validation.json").read_text())["fingerprint"], fingerprint())
        with self.assertRaises(SystemExit):
            final_test.validation(self.export, 0.01, self.out, check_run_004=False)

    def test_too_few_trades_stops_at_validation_and_the_holdout_stays_shut(self):
        text, data = final_test.validation(self.export, 0.01, self.out, check_run_004=False)
        self.assertIsNone(data["primary"])                       # 45 days cannot give 100 trades
        self.assertIn("STOPPED AT VALIDATION", text)
        before = len(self.loaded)
        with self.assertRaises(SystemExit):
            final_test.holdout(self.export, 0.01, self.out)
        self.assertEqual(len(self.loaded), before)               # nothing was read
        self.assertFalse((self.out / "holdout.json").exists())

    def test_a_tool_that_does_not_reproduce_run_004_stops_before_validation(self):
        with self.assertRaises(SystemExit) as stopped:
            final_test.validation(self.export, 0.01, self.out)   # made-up prices cannot match run 004
        self.assertIn("NOT loaded", str(stopped.exception))
        self.assertEqual([before for before, _, _, _ in self.loaded], [DEVELOPMENT_ENDS])
        self.assertFalse((self.out / "validation.json").exists())

    def test_the_holdout_needs_validation_first(self):
        with self.assertRaises(SystemExit):
            final_test.holdout(self.export, 0.01, self.out)
        self.assertEqual(self.loaded, [])

    def test_the_holdout_runs_the_primary_once_and_only_on_its_own_part(self):
        final_test.choose_primary = lambda summaries: 1          # force a primary: made-up prices have no edge
        final_test.validation(self.export, 0.01, self.out, check_run_004=False)
        self.loaded.clear()
        text, data = final_test.holdout(self.export, 0.01, self.out)
        self.assertEqual(len(self.loaded), 1)
        self.assertEqual(self.loaded[0][:2], (None, VALIDATION_ENDS - 14 * 86400))
        self.assertEqual(data["primary"], final_test.CANDIDATES[1].name)
        self.assertIn(data["label"], ("INCONCLUSIVE", "FAIL", "PROVISIONAL", "ROBUST PASS"))
        self.assertEqual(data["label"], "INCONCLUSIVE")          # 40 days: under 100 trades
        self.assertIn("# Outcome: INCONCLUSIVE", text)
        self.assertIn("Holdout part: 2026-05-", text)
        self.assertTrue((self.out / "holdout.md").exists())
        with self.assertRaises(SystemExit):
            final_test.holdout(self.export, 0.01, self.out)

    def test_a_changed_protocol_blocks_the_holdout(self):
        final_test.choose_primary = lambda summaries: 0
        final_test.validation(self.export, 0.01, self.out, check_run_004=False)
        lock = self.out / "validation.json"
        saved = json.loads(lock.read_text())
        saved["fingerprint"] = "0" * 64
        lock.write_text(json.dumps(saved))
        self.loaded.clear()
        with self.assertRaises(SystemExit) as stopped:
            final_test.holdout(self.export, 0.01, self.out)
        self.assertIn("changed after validation", str(stopped.exception))
        self.assertEqual(self.loaded, [])


if __name__ == "__main__":
    unittest.main()
