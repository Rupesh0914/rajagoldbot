"""Command line for trying each lesson's piece: python -m rajabot <command>."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone

from .candles import NEW_YORK, Candle, describe
from .direction import DEFAULT_LOOKBACK, STRUCTURE_STRENGTH, direction, structure
from .direction import explain
from .examples import (LESSON_2, LESSON_2_TWICE, LESSON_3, LESSON_4_WEAK, LESSON_4_WICK, LESSON_5_ROOM,
                       LESSON_5_TIGHT)
from .levels import HIGH, LevelBook, find_swings
from .candles import Bar
from .levels import ZONE_SHARE
from .manage import HALVES, QUARTERS, SINGLE, Position, target_price
from .risk import DEFAULT_RISK_SHARE, Contract, NoTrade, describe_plan, plan_trade, position_size
from .space import DEFAULT_MIN_RATIO, describe_room, measure_room
from .trigger import DEFAULT_MIN_BODY, Signal, Skip, Trigger


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
        lines.append("Level quality (turns within %.2f of the level):" % book.reach)
        for level in book.levels:
            turns = book.turns_at(level.price)
            lines.append("    %s %.2f: price has turned here %s" % (
                level.name, level.price, "once" if turns == 1 else "%d times" % turns))
    else:
        lines.append("Levels still standing: none")
    return lines


SKIP_WORDS = {
    "both_ways": "it broke a ceiling and a floor at once",
    "weak_candle": "the candle is not convincing",
    "against_direction": "the direction does not agree",
    "weak_level": "price has not turned at this level often enough",
}


def trigger_story(candles: list[Candle], direction: str | None, min_body: float, min_turns: int,
                  strength: int = 2) -> list[str]:
    """Walk through candles one close at a time and say when there is a signal, a skip or nothing."""
    trigger = Trigger(LevelBook(strength), min_body, min_turns)
    lines = ["Direction: %s. Body needed: %d%% of the candle. Turns needed at the level: %d." % (
        direction or "filter off", round(100 * min_body), min_turns), ""]
    for candle in candles:
        before = list(trigger.book.levels)
        result = trigger.on_candle(candle, direction)
        lines.append("%s candle (high %.2f, low %.2f) closed at %.2f, %d%% body" % (
            _new_york(candle.time), candle.high, candle.low, candle.close, round(100 * candle.body_share)))
        for level in before:
            went_past = candle.high > level.price if level.kind == HIGH else candle.low < level.price
            if went_past and level in trigger.book.levels:
                lines.append("    Went through the %s at %.2f but closed back. A wick is not a break. No signal." % (
                    level.name, level.price))
        if isinstance(result, Signal):
            lines.append("    SIGNAL at %s: %s. Closed through the %s at %.2f." % (
                _new_york(result.time), result.side.upper(), result.level.name, result.level.price))
        elif isinstance(result, Skip):
            where = " at %.2f" % result.level.price if result.level else ""
            lines.append("    SKIPPED: broke the level%s, but %s. The level is used up." % (where, SKIP_WORDS[result.reason]))
    return lines


def room_story(candles: list[Candle], min_ratio: float, allow_open_space: bool, strength: int = 2) -> list[str]:
    """Find the signal in an example and measure the room ahead of it."""
    trigger = Trigger(LevelBook(strength))
    lines = []
    for candle in candles:
        result = trigger.on_candle(candle)
        if isinstance(result, Signal):
            lines.append("%s SIGNAL at %s: closed at %.2f through the %s at %.2f. Candle low %.2f, high %.2f." % (
                result.side.upper(), _new_york(result.time), candle.close, result.level.name, result.level.price,
                candle.low, candle.high))
            lines.append(describe_room(measure_room(result, trigger.book), min_ratio, allow_open_space))
            break
    else:
        lines.append("No signal in this example.")
    return lines


def plan_story(candles: list[Candle], balance: float, risk_percent: float, spread: float, usd_rate: float,
               currency: str, strength: int = 2) -> list[str]:
    """Find the signal in an example and work out entry, stop and size for it."""
    trigger = Trigger(LevelBook(strength))
    contract = Contract(usd_to_account=usd_rate)
    for candle in candles:
        result = trigger.on_candle(candle)
        if isinstance(result, Signal):
            average = trigger.book.reach / ZONE_SHARE
            lines = ["%s SIGNAL: closed at %.2f through the %s at %.2f. Candle low %.2f, high %.2f." % (
                         result.side.upper(), candle.close, result.level.name, result.level.price, candle.low, candle.high),
                     "Next minute: chart price %.2f, spread %.2f. Account %.2f%s, risking %.2f%%." % (
                         candle.close, spread, balance, (" " + currency) if currency else "", risk_percent),
                     ""]
            plan = plan_trade(result, candle.close, spread, balance, average, contract, risk_percent / 100)
            lines.append(describe_plan(plan, balance, currency))
            if not isinstance(plan, NoTrade):
                lines += ["", describe_room(measure_room(result, trigger.book, plan.entry, plan.distance)).split("\n", 1)[1]]
            return lines
    return ["No signal in this example."]


def _walk(prices: list[float], start: int, spread: float) -> list[Bar]:
    """One-minute bars that move in small steps through the given prices, in order."""
    bars, time, at = [], start, prices[0]
    for goal in prices[1:]:
        steps = max(1, int(abs(goal - at) / 0.25))
        for index in range(1, steps + 1):
            nxt = at + (goal - at) * index / steps if index < steps else goal
            last = bars[-1].close if bars else prices[0]
            bars.append(Bar(time, last, max(last, nxt), min(last, nxt), nxt, spread))
            time += 60
        at = goal
    return bars


def exits_story(balance: float, spread: float = 0.20) -> list[str]:
    """The lesson's trade ended three ways, under each exit style."""
    trigger = Trigger(LevelBook(2))
    for candle in LESSON_5_ROOM:
        result = trigger.on_candle(candle)
        if isinstance(result, Signal):
            break
    plan = plan_trade(result, result.candle.close, spread, balance, trigger.book.reach / ZONE_SHARE)
    room = measure_room(result, trigger.book, plan.entry, plan.distance)
    target = target_price(plan, room.wall, spread)
    reward = target - plan.entry
    lines = ["BUY %.2f lots. Entry %.2f. Stop %.2f (risk %.2f). Target %.2f, a touch in front of the ceiling at %.2f." % (
                 plan.lots, plan.entry, plan.stop, plan.distance, target, room.wall.price),
             "The target is %.2f away: %.2fR." % (reward, reward / plan.distance), ""]
    for style in (SINGLE, HALVES, QUARTERS):
        position = Position(plan, target, style, result.time, stop_buffer=spread)
        parts = ", ".join("%.2f lots at %.2f" % (leg.lots, leg.price) for leg in position.legs)
        lines.append("%-8s closes %s" % (style.name, parts))
    endings = [("Straight to the target", [plan.entry, target + 0.5]),
               ("60% of the way, then all the way back", [plan.entry, plan.entry + 0.6 * reward, plan.stop - 1.0]),
               ("Straight to the stop", [plan.entry, plan.stop - 0.5])]
    lines += ["", "%-40s %8s %8s %9s" % ("What price did", "single", "halves", "quarters")]
    for name, path in endings:
        results = []
        for style in (SINGLE, HALVES, QUARTERS):
            position = Position(plan, target, style, result.time, stop_buffer=spread)
            for bar in _walk(path, result.time, spread):
                position.on_bar(bar)
            results.append(position.result_r)
        lines.append("%-40s %+7.2fR %+7.2fR %+8.2fR" % (name, results[0], results[1], results[2]))
    return lines


def structure_story(candles: list[Candle], strength: int) -> list[str]:
    """Show the peaks and dips of the lesson's 4-hour example and what they add up to."""
    lines = []
    for swing in find_swings(candles, strength):
        lines.append("%s at %.2f" % ("peak" if swing.kind == HIGH else "dip ", swing.price))
    lines.append("")
    lines.append("Structure: %s" % structure(candles, strength))
    lines.append("Closes rule (lesson 3, section 4): %s" % direction(candles))
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
    levels.add_argument("--example", choices=("break", "twice"), default="break",
                        help="break: the ceiling gets broken. twice: price turns at the same area twice")
    commands.add_parser("structure", help="Lesson 3: peaks and dips stepping up, in the lesson's 4-hour example")
    trigger = commands.add_parser("trigger", help="Lesson 4: signal, skip or nothing in the lesson's examples")
    trigger.add_argument("--example", choices=("break", "wick", "weak"), default="break",
                         help="break: a clean close through. wick: pokes through, closes back. weak: closes through on a poor candle")
    trigger.add_argument("--direction", choices=("up", "down", "off"), default="up",
                         help="the direction reading from lesson 3 (off = filter switched off)")
    trigger.add_argument("--min-body", type=float, default=DEFAULT_MIN_BODY,
                         help="share of the candle that must be body (default %.2f)" % DEFAULT_MIN_BODY)
    trigger.add_argument("--min-turns", type=int, default=1,
                         help="times price must have turned at the level (default 1 = any level)")
    room = commands.add_parser("room", help="Lesson 5: is there room to run after the signal?")
    room.add_argument("--example", choices=("room", "tight", "open"), default="room",
                      help="room: a ceiling well above. tight: a ceiling just above. open: nothing in the way")
    room.add_argument("--min-ratio", type=float, default=DEFAULT_MIN_RATIO,
                      help="room needed, as a multiple of the risk (default %.1f)" % DEFAULT_MIN_RATIO)
    room.add_argument("--no-open-space", action="store_true", help="skip signals with no level ahead to aim at")
    plan = commands.add_parser("plan", help="Lesson 6: entry, stop and size for the lesson's signal")
    plan.add_argument("--balance", type=float, default=10000.0, help="account balance (default 10000)")
    plan.add_argument("--risk", type=float, default=100 * DEFAULT_RISK_SHARE,
                      help="percent of the account to risk (default %.1f)" % (100 * DEFAULT_RISK_SHARE))
    plan.add_argument("--spread", type=float, default=0.20, help="spread in dollars (default 0.20)")
    plan.add_argument("--usd-rate", type=float, default=1.0,
                      help="what one US dollar is worth in the account's currency (1.40 for a Canadian-dollar account at 1.40)")
    plan.add_argument("--currency", default="", help="label for the money lines, for example CAD")
    size = commands.add_parser("size", help="Lesson 6: lots for a given risk and stop distance")
    size.add_argument("risk_money", type=float, help="money you accept losing on the trade")
    size.add_argument("distance", type=float, help="entry to stop, in dollars of gold price")
    size.add_argument("--usd-rate", type=float, default=1.0, help="what one US dollar is worth in the account's currency")
    exits = commands.add_parser("exits", help="Lesson 7: the same trade ended three ways, under each exit style")
    exits.add_argument("--balance", type=float, default=100000.0,
                       help="account balance (default 100000, big enough to split evenly; try 10000 or 3000)")
    direction = commands.add_parser("direction", help="Lesson 3: which way, from 4-hour closing prices (oldest first)")
    direction.add_argument("closes", type=float, nargs="+", help="closing prices of closed 4-hour candles, oldest first")
    direction.add_argument("--lookback", type=int, default=DEFAULT_LOOKBACK,
                           help="how many candles back to compare with (default %d)" % DEFAULT_LOOKBACK)
    args = parser.parse_args(argv)

    if args.command == "candle":
        if args.high < max(args.open, args.close) or args.low > min(args.open, args.close):
            parser.error("the high must be the highest of the four prices and the low the lowest")
        print(describe(Candle(0, args.open, args.high, args.low, args.close, 1800)))
    elif args.command == "levels":
        if args.strength < 1:
            parser.error("strength must be 1 or more")
        example = LESSON_2 if args.example == "break" else LESSON_2_TWICE
        print("\n".join(levels_story(example, args.strength)))
    elif args.command == "trigger":
        if not 0 < args.min_body <= 1:
            parser.error("--min-body is a share: above 0, at most 1")
        if args.min_turns < 1:
            parser.error("--min-turns must be 1 or more")
        example = {"break": LESSON_2, "wick": LESSON_4_WICK, "weak": LESSON_4_WEAK}[args.example]
        reading = None if args.direction == "off" else args.direction
        print("\n".join(trigger_story(example, reading, args.min_body, args.min_turns)))
    elif args.command == "room":
        if args.min_ratio <= 0:
            parser.error("--min-ratio must be positive")
        example = {"room": LESSON_5_ROOM, "tight": LESSON_5_TIGHT, "open": LESSON_2}[args.example]
        print("\n".join(room_story(example, args.min_ratio, not args.no_open_space)))
    elif args.command == "plan":
        if args.balance <= 0 or not 0 < args.risk <= 5 or args.spread < 0 or args.usd_rate <= 0:
            parser.error("balance and usd-rate must be positive, risk above 0 and at most 5 percent, spread not negative")
        print("\n".join(plan_story(LESSON_5_ROOM, args.balance, args.risk, args.spread, args.usd_rate, args.currency)))
    elif args.command == "size":
        if args.risk_money <= 0 or args.distance <= 0 or args.usd_rate <= 0:
            parser.error("risk, distance and usd-rate must all be positive")
        contract = Contract(usd_to_account=args.usd_rate)
        lots = position_size(args.risk_money, args.distance, contract)
        if lots <= 0:
            print("No trade: even 0.01 lots would lose %.2f, more than the %.2f allowed." % (
                args.distance * contract.money_per_dollar(0.01), args.risk_money))
        else:
            print("%.2f lots. If stopped out: -%.2f. Each dollar gold moves is worth %.2f." % (
                lots, args.distance * contract.money_per_dollar(lots), contract.money_per_dollar(lots)))
    elif args.command == "exits":
        if args.balance < 2000:
            parser.error("with under 2000 the lesson's trade is too small to place at all")
        print("\n".join(exits_story(args.balance)))
    elif args.command == "structure":
        print("\n".join(structure_story(LESSON_3, STRUCTURE_STRENGTH)))
    elif args.command == "direction":
        if args.lookback < 1:
            parser.error("lookback must be 1 or more")
        print(explain(args.closes, args.lookback))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
