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


class TriggerCommand(unittest.TestCase):
    def test_the_clean_break_is_a_buy_signal(self):
        out = run("trigger")
        self.assertIn("SIGNAL at 12:30: BUY. Closed through the ceiling at 3761.00.", out)
        self.assertNotIn("SKIPPED", out)

    def test_the_wick_is_nothing(self):
        out = run("trigger", "--example", "wick")
        self.assertIn("A wick is not a break. No signal.", out)
        self.assertNotIn("SIGNAL at", out)
        self.assertNotIn("SKIPPED", out)

    def test_the_weak_candle_is_skipped(self):
        out = run("trigger", "--example", "weak")
        self.assertIn("SKIPPED: broke the level at 3761.00, but the candle is not convincing.", out)

    def test_direction_and_level_quality_options(self):
        self.assertIn("the direction does not agree", run("trigger", "--direction", "down"))
        self.assertIn("SIGNAL at 12:30: BUY", run("trigger", "--direction", "off"))
        self.assertIn("has not turned at this level often enough", run("trigger", "--min-turns", "2"))
        self.assertIn("the candle is not convincing", run("trigger", "--min-body", "0.8"))

    def test_bad_settings_are_refused(self):
        for bad in (("--min-body", "0"), ("--min-body", "1.5"), ("--min-turns", "0")):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                run("trigger", *bad)


class RoomCommand(unittest.TestCase):
    def test_the_three_examples(self):
        out = run("room")
        self.assertIn("Next ceiling in the way: 3775.00. Room: 13.00.", out)
        self.assertIn("Room is 1.62 times the risk. Needed: 1.00.", out)
        self.assertTrue(out.endswith("ENOUGH ROOM."))
        self.assertTrue(run("room", "--example", "tight").endswith("NOT ENOUGH ROOM: skipped."))
        self.assertIn("No level in the way: open space.", run("room", "--example", "open"))

    def test_the_options(self):
        self.assertTrue(run("room", "--min-ratio", "2").endswith("NOT ENOUGH ROOM: skipped."))
        self.assertIn("open space is switched off", run("room", "--example", "open", "--no-open-space"))
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            run("room", "--min-ratio", "0")


class PlanAndSizeCommands(unittest.TestCase):
    def test_the_lesson_six_plan(self):
        out = run("plan")
        self.assertIn("BUY 0.05 lots.", out)
        self.assertIn("Entry 3762.20. Stop 3753.80. Distance 8.40.", out)
        self.assertIn("If stopped out: -42.00, which is 0.42% of the account. That is 1R.", out)
        self.assertIn("Room is 1.52 times the risk.", out)

    def test_a_canadian_account_and_a_small_account(self):
        out = run("plan", "--usd-rate", "1.40", "--currency", "CAD")
        self.assertIn("BUY 0.04 lots.", out)
        self.assertIn("-47.04 CAD", out)
        self.assertIn("NO TRADE: size below min", run("plan", "--balance", "500"))

    def test_size(self):
        self.assertEqual(run("size", "50", "8.4"),
                         "0.05 lots. If stopped out: -42.00. Each dollar gold moves is worth 5.00.")
        self.assertTrue(run("size", "5", "8.4").startswith("No trade"))
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            run("plan", "--risk", "6")


class ExitsCommand(unittest.TestCase):
    def test_the_same_trade_ended_three_ways(self):
        out = run("exits")
        self.assertIn("Target 3774.80, a touch in front of the ceiling at 3775.00.", out)
        self.assertIn("The target is 12.60 away: 1.50R.", out)
        lines = {line[:40].strip(): line[40:].split() for line in out.splitlines() if line.endswith("R")}
        self.assertEqual(lines["Straight to the target"], ["+1.50R", "+1.12R", "+0.93R"])
        self.assertEqual(lines["60% of the way, then all the way back"], ["-1.00R", "+0.38R", "+0.46R"])
        self.assertEqual(lines["Straight to the stop"], ["-1.00R", "-1.00R", "-1.00R"])

    def test_a_small_account_gets_fewer_parts(self):
        self.assertIn("quarters closes 0.01 lots at 3768.50", run("exits", "--balance", "3000"))
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            run("exits", "--balance", "500")


class GateCommands(unittest.TestCase):
    def test_the_lesson_eight_moments(self):
        out = run("gate")
        for line in ("Tuesday 1 Dec, 09:30, spread 0.15              OK to trade",
                     "Tuesday 1 Dec, 05:00, spread 0.15              NO: outside the New York session",
                     "Tuesday 1 Dec, 10:00, spread 0.80              NO: the spread is too wide",
                     "Friday 4 Dec, 08:15 (jobs report at 08:30)     NO: scheduled news",
                     "12:30, a new signal                            NO: lost 3R today",
                     "Thursday 3 Dec, 09:30: a new day               OK to trade"):
            self.assertIn(line, out)

    def test_progress(self):
        self.assertEqual(run("progress", "3750", "3754", "3758", "3762", "3766"),
                         "Net move 16.00, distance travelled 16.00: progress 1.00. Not sideways.")
        self.assertTrue(run("progress", "3750", "3756", "3751", "3757", "3750", "3755", "3751").endswith("Sideways (under 0.20)."))
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            run("progress", "3750", "3751")


if __name__ == "__main__":
    unittest.main()
