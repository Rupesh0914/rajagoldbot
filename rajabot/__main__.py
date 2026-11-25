"""Command line for trying each lesson's piece: python -m rajabot <command>."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone

from .candles import NEW_YORK, Candle, describe
from .examples import LESSON_2
from .levels import LevelBook


def _new_york(utc_seconds: int) -> str:
    return datetime.fromtimestamp(utc_seconds, timezone.utc).astimezone(NEW_YORK).strftime("%H:%M")


def levels_story(candles: list[Candle], strength: int) -> list[str]:
    """Walk through candles one close at a time and say what happened to the levels."""
    book = LevelBook(strength)
    lines = []
    for candle in candles:
        update = book.add(candle)
        lines.append("%s candle (high %.2f, low %.2f) closed at %.2f at %s" % (
            _new_york(candle.time), candle.high, candle.low, candle.close, _new_york(candle.close_time)))
        for level in update.expired:
            lines.append("    too old, dropped: %s %.2f" % (level.name, level.price))
        for level in update.broken:
            lines.append("    BROKEN: closed through the %s at %.2f. It is no longer a level." % (level.name, level.price))
        for level in update.new:
            lines.append("    NEW LEVEL: %s at %.2f, made by the %s candle, usable from %s" % (
                level.name, level.price, _new_york(level.made_at), _new_york(level.usable_from)))
    lines.append("")
    if book.levels:
        lines.append("Levels still standing: " + ", ".join("%s %.2f" % (l.name, l.price) for l in book.levels))
    else:
        lines.append("Levels still standing: none")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rajabot", description="Try the pieces of the bot, one lesson at a time.")
    commands = parser.add_subparsers(dest="command", required=True)
    candle = commands.add_parser("candle", help="Lesson 1: describe one candle from its four prices")
    for name in ("open", "high", "low", "close"):
        candle.add_argument(name, type=float)
    levels = commands.add_parser("levels", help="Lesson 2: watch levels appear and break in the lesson's example")
    levels.add_argument("--strength", type=int, default=2,
                        help="candles needed on each side of a swing (the lesson's example uses 2)")
    args = parser.parse_args(argv)

    if args.command == "candle":
        if args.high < max(args.open, args.close) or args.low > min(args.open, args.close):
            parser.error("the high must be the highest of the four prices and the low the lowest")
        print(describe(Candle(0, args.open, args.high, args.low, args.close, 1800)))
    elif args.command == "levels":
        if args.strength < 1:
            parser.error("strength must be 1 or more")
        print("\n".join(levels_story(LESSON_2, args.strength)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
