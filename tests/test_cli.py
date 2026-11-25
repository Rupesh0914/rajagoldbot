"""The command line used in the lessons."""
import contextlib
import io
import unittest

from rajabot.__main__ import main


def run(*argv) -> str:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        main(list(argv))
    return out.getvalue().strip()


class CandleCommand(unittest.TestCase):
    def test_the_two_candles_from_lesson_one(self):
        self.assertEqual(run("candle", "3750", "3758", "3748", "3756"),
                         "bullish candle: body 6.00, upper wick 2.00, lower wick 2.00, body is 60% of the candle")
        self.assertEqual(run("candle", "3756", "3760", "3740", "3755"),
                         "bearish candle: body 1.00, upper wick 4.00, lower wick 15.00, body is 5% of the candle")

    def test_prices_that_cannot_be_a_candle_are_refused(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            run("candle", "3750", "3749", "3748", "3756")       # high below the close


class LevelsCommand(unittest.TestCase):
    def test_the_lesson_two_story(self):
        out = run("levels")
        self.assertIn("NEW LEVEL: ceiling at 3761.00, made by the 09:00 candle, usable from 10:30", out)
        self.assertIn("NEW LEVEL: floor at 3742.00, made by the 10:30 candle, usable from 12:00", out)
        self.assertIn("BROKEN: closed through the ceiling at 3761.00", out)
        self.assertIn("Levels still standing: floor 3742.00\n", out)
        self.assertTrue(out.endswith("floor 3742.00: price has turned here once"))

    def test_a_stricter_strength_keeps_only_the_floor(self):
        out = run("levels", "--strength", "4")
        self.assertNotIn("ceiling", out)
        self.assertIn("Levels still standing: floor 3742.00\n", out)

    def test_the_example_where_price_turns_twice_at_the_same_area(self):
        out = run("levels", "--example", "twice")
        self.assertNotIn("BROKEN", out)
        self.assertIn("ceiling 3761.00: price has turned here 2 times", out)
        self.assertIn("ceiling 3760.00: price has turned here 2 times", out)
        self.assertIn("floor 3742.00: price has turned here once", out)

    def test_strength_below_one_is_refused(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            run("levels", "--strength", "0")


class DirectionCommand(unittest.TestCase):
    def test_the_lesson_three_examples(self):
        self.assertEqual(run("direction", "3700", "3710", "3705", "3720", "3730", "3725", "3740"),
                         "up: the last close 3740.00 is above 3700.00, the close 6 candles earlier. Look for buys only.")
        self.assertIn("Look for sells only", run("direction", "3740", "3730", "3735", "3720", "3710", "3715", "3700"))
        self.assertIn("unknown", run("direction", "3700", "3710"))

    def test_lookback_below_one_is_refused(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            run("direction", "3700", "3710", "--lookback", "0")


class StructureCommand(unittest.TestCase):
    def test_the_lesson_three_example_steps_up(self):
        out = run("structure")
        self.assertEqual(out.splitlines()[:4], ["peak at 3715.00", "dip  at 3697.00", "peak at 3731.00", "dip  at 3712.00"])
        self.assertIn("Structure: up", out)
        self.assertTrue(out.endswith("Closes rule (lesson 3, section 4): up"))


if __name__ == "__main__":
    unittest.main()
