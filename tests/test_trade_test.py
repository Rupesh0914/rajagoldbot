"""The trade test (research/trade_test.py)."""
import unittest

from research.signal_check import DEVELOPMENT_ENDS
from research.trade_test import BASE, BENCHMARKS, SETUPS, check, summarise
from tests.test_signal_check import random_walk


class Summary(unittest.TestCase):
    def test_the_numbers(self):
        s = summarise([{"r": 1.5}, {"r": -1.0}, {"r": -1.0}, {"r": 2.0}, {"r": -0.5}])
        self.assertEqual(s["trades"], 5)
        self.assertAlmostEqual(s["win_share"], 0.4)
        self.assertAlmostEqual(s["average"], 0.2)
        self.assertAlmostEqual(s["profit_factor"], 3.5 / 2.5)
        self.assertAlmostEqual(s["total"], 1.0)
        self.assertAlmostEqual(s["drawdown"], 2.0)             # from +1.5 down to -0.5
        self.assertEqual(summarise([]), {"trades": 0})


class TheTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text, cls.data = check(random_walk(120, seed=3))

    def test_every_setup_is_reported(self):
        for setup in SETUPS + BENCHMARKS:
            self.assertIn(setup.name, self.data["setups"])
            self.assertIn("| %s |" % setup.name, self.text)
        for heading in ("## The setups", "## How the trades ended", "## How far the ladders got",
                        "## Inside the base setup", "## Signals the base setup did not trade", "## What this cannot say"):
            self.assertIn(heading, self.text)

    def test_random_prices_give_no_edge(self):
        benchmark = self.data["setups"][BENCHMARKS[0].name]
        self.assertGreater(benchmark["trades"], 100)
        self.assertTrue(-0.35 < benchmark["average"] < 0.2, benchmark["average"])
        self.assertLess(benchmark["average_2x"], benchmark["average"] + 0.05)

    def test_one_trade_at_a_time_and_only_in_session(self):
        base = self.data["setups"][BASE.name]
        self.assertGreater(base["trades"], 5)
        self.assertGreater(base["skips"].get("outside_session", 0), 0)
        unfiltered = self.data["setups"]["No hours or direction filter"]
        self.assertGreater(unfiltered["trades"], base["trades"])
        self.assertNotIn("outside_session", unfiltered["skips"])

    def test_it_refuses_history_past_the_development_part(self):
        with self.assertRaises(ValueError):
            check(random_walk(10, seed=1, start=DEVELOPMENT_ENDS - 5 * 86400))
        with self.assertRaises(ValueError):
            check(random_walk(2, seed=1))


if __name__ == "__main__":
    unittest.main()
