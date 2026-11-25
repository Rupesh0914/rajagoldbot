"""Command line for trying each lesson's piece: python -m rajabot <command>."""
from __future__ import annotations

import argparse

from .candles import Candle, describe


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rajabot", description="Try the pieces of the bot, one lesson at a time.")
    commands = parser.add_subparsers(dest="command", required=True)
    candle = commands.add_parser("candle", help="Lesson 1: describe one candle from its four prices")
    for name in ("open", "high", "low", "close"):
        candle.add_argument(name, type=float)
    args = parser.parse_args(argv)

    if args.command == "candle":
        if args.high < max(args.open, args.close) or args.low > min(args.open, args.close):
            parser.error("the high must be the highest of the four prices and the low the lowest")
        print(describe(Candle(0, args.open, args.high, args.low, args.close, 1800)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
