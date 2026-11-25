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


if __name__ == "__main__":
    unittest.main()
