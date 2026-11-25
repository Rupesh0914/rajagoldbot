# Lesson 4: The trigger

Lessons 2 and 3 gave the bot a map (the levels) and a direction. This lesson is the moment it
says: "this is a signal".

## 1. The trigger in one sentence

> A 30-minute candle **closes** through a level, the candle is convincing, and the direction
> agrees.

- Closes above a ceiling: a **buy** signal.
- Closes below a floor: a **sell** signal.

This is the setup the notes call break-and-close continuation: price has been held by a level,
it finally gets through, and the bet is that it keeps going.

That is the bet. Section 11 says how it has done so far on real prices: on its own, not well.

## 2. The four checks

When a 30-minute candle closes, the bot asks, in this order:

| # | Check | If it fails |
|---|---|---|
| 1 | Did the candle **close** beyond a standing level? | Nothing happened. No signal, and the level stays |
| 2 | Is the candle **convincing**? | Skipped: "weak candle" |
| 3 | Does the **direction** from Lesson 3 agree? | Skipped: "against direction" |
| 4 | Is the **level good enough**? (the level-quality option from Lesson 2) | Skipped: "weak level" |

All four pass: a signal.

(The code has one more guard: if a single candle somehow closed above a ceiling and below a floor
at once, it gives no side and skips. With levels built the way Lesson 2 builds them this should
not happen, so it is a safety net and not a fifth rule to learn.)

## 3. Check 1: a close, not a poke

From Lesson 1: only the close counts.

The ceiling is at 3761. A candle spikes to 3764 and closes at 3760.

```
   3764  |          <- went through
   3761 -|--------  <- the ceiling
   3760 [ ]         <- closed back under it
        [ ]
```

Buyers pushed through and could not hold it. That is not a break. It is the level doing its job.
The bot does nothing, and the ceiling stays on the map.

Traders who buy the moment price pokes above a level can be caught when it falls back. Waiting
for the close costs a slightly worse price and is meant to avoid that. How many traps it avoids
is something we have not measured.

## 4. Check 2: is the candle convincing?

A candle can close beyond a level and still be a poor candle. The bot wants two things from it:

1. **It closed in the direction of the break.** For a buy, the candle closed higher than it
   opened. For a sell, lower.
2. **Enough of it is body.** At least half of the candle's height must be body, not wick.

Two candles that both close above the 3761 ceiling:

| | Open | High | Low | Close | Body share | Verdict |
|---|---|---|---|---|---|---|
| Convincing | 3756 | 3763 | 3755 | 3762 | 75% | Signal |
| Poor | 3756 | 3768 | 3755 | 3761.5 | 42% | Skipped |

The second candle went all the way to 3768 and was sold back to 3761.5. It closed above the
ceiling by 50 cents, with a long upper wick. Sellers were waiting up there. Raja favours candles
that are mostly body over candles with long wicks, though he gives no exact figure.

**"At least half" is our number.** The candidates were 50%, 65% and 80%, taken from your research
notes. The first test went against the stricter ones: candles over 80% body won 47.7% of the
time afterwards, against 52.3% for candles of 50% to 65% body. A very full candle may mean the
move is already spent by the time it closes. So the rule stays at 50%, as a minimum that screens
out wick-heavy candles. It is not a claim that fuller is better.

**What happens to the level after a skipped break?** It is used up. Price did close through it,
so it is no longer a ceiling. The bot does not wait around for a second chance at the same
level.

## 5. Check 3: the direction agrees

A buy signal needs the direction to be up. A sell needs down. Anything else (flat, mixed,
unknown) and the break is skipped.

This is where Lesson 3 pays off. A ceiling breaking while gold is falling on the 4-hour chart is
often just a bounce, and the bot leaves it alone.

## 6. Check 4: level quality (optional)

From Lesson 2, section 8: the bot can count how many times price has turned at a level. With
this option switched on, a break only counts if price had turned there at least twice. The usual
reasoning is that a level that held twice has more traders watching it.

It is switched off. In our tests it added nothing once the hours and direction filters were on.

## 7. One candle, two levels

Sometimes two ceilings sit close together, say 3760 and 3761, and one strong candle closes above
both. That is one signal, not two. The signal level is the **furthest** one broken (3761): the
last wall the candle had to get through. Both levels are used up.

## 8. A signal is not yet a trade

A signal means "this is worth looking at". Before the bot places anything, three more things
must pass:

- **Room to run** (Lesson 5): is there open space ahead, or another level in the way?
- **Stop and size** (Lesson 6): where is the idea proven wrong, and how much to risk?
- **When not to trade** (Lesson 8): the right hours, no news, not a sideways market.

The signal exists the moment the candle closes, never earlier. The bot would enter on the next
minute.

## 9. Every skip is written down

When the bot skips a break, it records the time, the side, the level and the reason. This
matters more than it sounds:

- You can check its thinking. "Why didn't it take the 14:30 break?" has an answer.
- It keeps the testing honest. Lesson 9 counts every skipped signal next to every trade, so
  nothing is hidden.

## 10. What Raja does differently

- **He sometimes enters before the close.** The notes show both: waiting for the 30-minute close,
  and entering as price breaks through. He treats the early entry as riskier. The bot waits for
  the close. The early version is Lesson 14 and gets its own test.
- **He judges the candle by eye.** "Strong candle" has no number in the videos. The body share is
  our measure of it.

## 11. What our tests have said so far

Results on the first 13 months of your Eightcap history. Clues, not proof. Details are in
`research/results`.

- **A level break on its own was a coin flip:** 50.0% over 784 signals.
- **Any strong candle did as well, with no level at all.** With the New York hours and the
  4-hour direction added, level breaks won 54.2% and plain strong candles 53.2%, on six times as
  many signals.
- **In whole trades the plain strong candle did best.** Stop behind the candle, target at twice
  the risk: +0.105 R a trade over 646 trades, the only setup clearly above zero.

So the honest position is: the hours and the direction are doing the work, and the level break
has not yet shown that it adds anything. It stays in the bot as an option under test. The
working setup is the plain strong candle in the right hours and direction.

## What the bot piece does

`rajabot/trigger.py` is fed each closed 30-minute candle together with the current direction. It
updates the levels and answers one of three things: a **signal** (with the side, the level and
the candle), a **skip** (with the reason), or nothing.

Its tests check that every signal uses a level that was already known before the signal candle
opened, and that a signal never changes when later prices arrive.

Try the three cases from this lesson:

```
python -m rajabot trigger                      # a clean close through: BUY signal
python -m rajabot trigger --example wick       # pokes through, closes back: nothing
python -m rajabot trigger --example weak       # closes through on a poor candle: skipped
```

And see the other checks at work on the clean break:

```
python -m rajabot trigger --direction down     # the direction does not agree
python -m rajabot trigger --min-body 0.8       # a stricter candle rule
python -m rajabot trigger --min-turns 2        # only levels that held twice
```

## Practice on a real chart

On the 30-minute XAUUSD chart, find three places where a candle closed above a recent swing high
or below a recent swing low. For each one, work out the body share (body divided by the whole
height) and check the 4-hour direction at that moment. Would the bot have signalled? Then look at
what price did over the next few hours. Do not draw conclusions from three examples. The point
is to get fast at seeing the four checks.

## Check yourself

1. A floor is at 3742. A candle drops to 3739 and closes at 3743. Signal, skip or nothing?
2. A ceiling is at 3800. A candle opens at 3794, reaches 3812, dips to 3793 and closes at 3801.
   Direction is up. What does the bot do, and what happens to the ceiling?
3. A floor is at 3742. A candle opens at 3748, high 3749, low 3739, close 3740. Direction is up.
   What does the bot do?
4. One candle closes above ceilings at 3760 and 3761. How many signals, and at which level?
5. The bot has a buy signal. Does it buy?

<details>
<summary>Answers</summary>

1. Nothing. It poked below the floor but closed above it. The floor stays.
2. Skip, "weak candle". The body is 7 (3794 to 3801) and the whole candle is 19 (3793 to 3812).
   That is 37% body, under the 50% needed. The ceiling is used up, because price did close
   above it.
3. Skip, "against direction". The candle is a convincing break of the floor (body 8 of 10), but a
   sell needs the direction to be down.
4. One signal, at 3761, the furthest level broken. Both ceilings are used up.
5. Not yet. Room to run, the stop and size, and the when-not-to-trade rules must still pass.

</details>

## Next

Lesson 5: room to run. Before taking a signal, is there open space ahead, or is the next level
so close that the trade has nowhere to go?
