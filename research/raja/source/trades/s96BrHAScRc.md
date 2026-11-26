# s96BrHAScRc - "How I Trade Gold Profitably" (streamed 16 Sep 2023, 1:11:17)

- **Platform:** MetaTrader 5 (Dominion Markets build) running a replay add-on ("Simulator1.0-N6" in the
  Navigator; he calls it the MT5 simulator). This is NOT Soft4FX on MT4. The replayed chart is a custom
  symbol titled `!STANDARD_X` with the timeframe after it (for example `[!STANDARD_X,M30]`).
- **Where the equivalents are:** replay date, time and weekday are printed at the top left of the chart
  ("Standard chart - M15 / 2023.04.17 08:30:56 / Monday") and again in the orange simulator panel
  ("Mon, 17/04/2023 08:30:56"). The order box is called "Visual Buy" / "Visual Sell" and shows max risk
  in percent and dollars, SL and TP price, the distance in the simulator's own "pips", and reward-to-risk.
  The simulator also has a Sessions panel and a History / Closed trades table.
- **Instrument:** XAUUSD (gold), three decimals. Spread fixed at "15.0 pips" in the panel = 0.15 dollars.
- **Account:** 50,000 dollars simulated ("funded account" size). Ended at 54,991.46 (+9.98%).
- **Replay dates covered:** Monday 17 April 2023 to Friday 21 April 2023 (one trading week). Trades on
  Mon, Tue, Wed and Fri. Thursday 20 April: no trade.
- **Software setup at 0:00 to 7:55 skipped as instructed.**

## Pip size in this video

His pip is **0.10 dollars**. The simulator's pip is 0.01 dollars (ten times smaller). Both are on screen
together several times:

| Video time | What the screen shows | What he says |
|---|---|---|
| 16:00 | Order box: SL 2004.792 against entry 2006.265 = 1.473 dollars, labelled "-147.0 pips" | "13 14 pips" (16:40) |
| 21:45 | Crosshair measure 2009.92 to 2012.91: "2991 points" = 2.991 dollars | "30 pip range" (21:40) |
| 26:30 | Crosshair measure to 2011.261: "3574 points" = 3.574 dollars | "your stop loss is 35 pips" (26:25) |
| 29:10 | Order box: SL 2.943 dollars away, labelled "-294.0 pips" | "30 pips" (28:42) |
| 35:45 | Order box: SL 2.524 dollars away, labelled "-252.0 pips" | "25 pips stop" (35:40) |
| 38:45 | Order box: SL 1.539 dollars away, labelled "-153.0 pips" | "15 pips stop" (38:40) |
| 58:58 | Two range lines at 1996.47 and 1990.23 = 6.24 dollars | "60 pip range" (59:15) |
| 1:09:08 | Closed-trades table, drawdown column "-52.0" (0.52 dollars) | "Five pip draw down" (1:08:55) |

No contradiction anywhere in the video. This agrees with the earlier finding (later platforms 0.10; the
2022 simulator also counted 0.01 as a pip while he spoke in 0.10 pips).

## Clock / timezone

The replay clock is **broker server time, UTC+3** (Eastern European summer time). Evidence:
- He says the 01:00 bar is 6 pm Eastern and 08:00 is 1 am Eastern (8:00 to 9:20). In April New York is
  UTC-4, so chart time = New York + 7 h = UTC+3.
- The Sessions panel (frame 20:10) is a 0 to 24 hour strip in chart time: the London block starts at 10
  and the New York block at 15. 10:00 UTC+3 = 08:00 London (summer time); 15:00 UTC+3 = 08:00 New York.
- He calls 08:00 chart time "pre-London ... 2 hours before London open" (8:20).

So: chart 08:00 = 05:00 UTC = 06:00 London = 01:00 New York. Chart 10:00 = London open. Chart 13:00 =
"pre New York ... 6:00 a.m. Eastern" (24:55). Chart 15:00 = 08:00 New York.

## Zones as drawn in this video

Same habit as the other videos, with one addition:
- Thin grey rectangles drawn along the **edge of candle bodies** of the last few 30-minute candles: the
  upper one on the body tops (closes/opens) of the consolidation, the lower one on the body bottoms.
  Wicks stick out through them. The range bands on the 30-minute chart are about 0.15 to 0.55 dollars
  thick (1.5 to 5.5 of his pips).
- **Addition:** on the two bands that define the range he is waiting on, he also lays a thin orange
  horizontal line through the band, running the full width of the chart, with a price tag on the axis
  (2005.03 / 2003.82 on Monday; 2001.19 / 1998.06 on Tuesday; 2004.97 / 2002.58 on Wednesday;
  1996.47 / 1990.23 on Thursday). The orange line is the level he talks about breaking.
- Higher-timeframe support bands are thicker: the daily/4-hour support under Monday's price is about
  1989.5 to 1991.5 (about 2 dollars); a Friday support band is about 1991.9 to 1992.8.
- He moves and redraws the range bands as the range changes. On Tuesday the middle band sat at 1996.46 at
  08:31 (frame 32:50) and the range was redrawn as 2001.19 / 1998.06 by 10:30 (frame 35:15).
- He deletes everything at the start of each new day ("remove all these analysis", 41:45; 57:15).

---

# Trades

All prices and times below are read from the order box, the open-order row, or the simulator's own
History and Closed-trades tables (frames 1:08:48 and 1:09:08), which list every fill. Where a number comes
only from the transcript it is marked (transcript). "R" = multiple of the initial dollar risk.

## Trade 1 - Monday buy, pre-London break of a consolidation

- **Video time:** entry about 16:10 (order box at 16:00, filled order row at 16:20). Partial closes at
  about 17:35 and 18:15. Last piece closed about 20:05.
- **Replay time:** entry Mon 17.04.2023 **08:30:56** (05:30:56 UTC, 06:30 London). First partial 08:48:26,
  second 08:52:17, last piece 10:24:07.
- **Chart at entry:** XAUUSD, M30.
- **Direction and prices:** BUY 1.69 lots at **2006.265**. Stop **2004.792**. Stop distance **1.473
  dollars**; order box says "-147.0 pips, -248.94 USD"; he says "13 14 pips" (16:40). A take-profit of
  2013.138 is recorded on the opening fill, but he says he is removing it to let the trade run (16:05).
- **Risk:** order box "Max. Risk: 0.50% (250.00 USD)". He says he would normally use 1%.
- **What was drawn (frames 11:10, 13:30):** two thin grey bands on the M30 chart, each with an orange line
  through it. Upper band about 2005.03, roughly 0.15 to 0.2 dollars thick, lying on the body tops of the
  sideways candles; several wicks poke 0.5 to 1.0 dollars above it. Lower band about 2003.82, same
  thickness, on the body bottoms. The bands start about 6 to 8 thirty-minute candles back (the 04:00 to
  05:00 candles), i.e. they frame only the last 3 to 4 hours. He also measured the room below the range:
  crosshair read "2980 points" (2.98 dollars) down to 2000.59; the captions have him say "313 pips",
  most likely "31" (11:10).
- **Higher timeframes:**
  - Daily (frame 9:24): Friday's candle is a large bearish candle (roughly 2040 down to 2004) whose lower
    wick reached about 1992 and came back. A grey band about 2 dollars thick sits at about 1990 to 1991.5
    on the body bottoms of the candles from about 10 to 11 April. He reads it as support rejected, so price
    may go up (9:15).
  - 4-hour (frame 9:50): the same band is visible; the last closed 4-hour candle dipped under the previous
    candle's low and still closed bullish. His read: bullish (9:40).
  - 1-hour (transcript, 10:10): last candle small-bodied, "very little volume".
  - 30-minute: small candles side by side = consolidation; wait for a close outside the two bands.
- **Entry trigger:** the M30 candle 08:00 to 08:30 **closed** at 2005.225 (status bar in frame 13:30: O
  2004.345, H 2005.265, L 2003.715, C 2005.225). That is a close about 0.2 above the upper band, with almost
  no top wick (0.04) and a body of about 0.9 dollars. He then waited for the next candle to push above
  the earlier wick highs and bought **56 seconds into the new, still open, 30-minute candle**, when the ask
  had reached 2006.265.
- **Stated reason:** "it closed above this resistance we had at 2005 ... this 30-minute candle has no wick
  on the top" (13:20). And on time of day: pre-London is a volume window (19:20).
- **Stop logic:** below the low of the candle he entered on. "there's no business for this candle to
  continue to break its own low" (16:30).
- **Management:**
  1. After the 08:30 to 08:45 M15 candle closed bullish and the next one broke its high, stop moved up to
     2006.144 (0.12 below entry). "we can bring our stops below this new 15-minute candle" (17:20).
  2. 08:48:26: closed **1.35 lots (80%)** at 2009.215 (+2.95 dollars, +398.25 USD) and stop to break-even
     2006.265. "close 80% ... put stops at break even. Now we got a free trade" (17:35).
  3. 08:52:17: closed 0.31 lots (about 90% of the rest) at 2011.715 (+5.45, +168.95 USD). Reason: the move
     was stretched. "the more away price moves ... there's a very good probability we can retrace" (18:05).
  4. 10:24:07: closed the last 0.03 lots at 2011.715 (+5.45, +16.35 USD) while showing the session panel.
- **Outcome:** **+583.55 USD = +1.17% = about +2.3R.** Worst drawdown 0.52 dollars. 17.5 minutes to the
  first partial; 1 h 53 min until the last 0.03 lots closed.
- **Afterwards:** he calls it "a risky trade, which is why I lowered down my risk" (22:00).

## Trade 2 - Monday buy, first 30-minute support after the breakout

- **Video time:** entry about 22:55 (order box at 22:50). Target hit about 23:50.
- **Replay time:** entry Mon 17.04.2023 **12:00:00** (09:00 UTC, 10:00 London). Exit 12:12:12.
- **Chart at entry:** XAUUSD, M30.
- **Direction and prices:** BUY 1.50 lots at **2009.925**. Stop **2008.242**. Stop distance **1.683
  dollars**; order box "-168.0 pips, -252.45 USD". Target **2011.626** (+1.701 dollars). The order box
  frame, taken before he finished dragging the line, shows TP 2011.829; the fill table shows 2011.626. He
  wanted "one to one risk reward" (22:50) and speaks of getting "13 14 pips" out of the range (22:35).
- **Risk:** "Max. Risk: 0.50% (252.92 USD)".
- **What was drawn (frame 21:45):** upper band about 2012.85, about 0.35 thick, across the body tops of the
  three candles at the high (09:00 to 10:30); their wicks reach about 2014.8 above it. Lower band about
  2009.0 (orange tag 2009.01 later), about 0.4 thick, on the body bottoms of the last two candles; the last
  candle's wick hangs about 0.8 below it. He measured from the candle body up to the upper band: "2991
  points" = "30 pip range" (he stresses he measures from the body, not the wick, 24:35).
- **Higher timeframes:** not re-checked for this trade. Context is the morning breakout.
- **Entry trigger:** after three bearish 30-minute candles down from the high, the 11:30 to 12:00 candle
  **closed** bullish: small body (about 0.3 to 0.5 dollars), lower wick about 0.9, small top wick. He bought
  at the open of the next candle, exactly 12:00:00.
- **Stated reason:** "A support is formed when we have a bullish candle closing after bearish candle."
  (23:30). And: room to the high is 30 pips, so 13 to 14 pips is reachable (22:30).
- **Stop logic:** "Stops are going to go below this candle" (22:42), i.e. just under the trigger candle's
  wick low.
- **Management:** none. Fixed target.
- **Outcome:** target filled at 2011.626. **+255.15 USD = +1.0R.** Held 12 min 12 s. Drawdown 0.31 dollars.
- **Afterwards:** he rejects a viewer's objection that the candle was too small: on the 30-minute and
  1-hour, a support after an up-move is enough (23:00).

## Trade 3 - Monday sell, retest of broken support, into a news candle

- **Video time:** entry about 29:12 (order box at 29:10). Target hit about 29:20.
- **Replay time:** entry Mon 17.04.2023 **15:30:00** (12:30 UTC, 08:30 New York). Exit 15:30:21.
- **Chart at entry:** XAUUSD, M30 (he flicked to M15 at 28:55 and back).
- **Direction and prices:** SELL 0.43 lots at **2007.614**. Stop **2010.557**. Stop distance **2.943
  dollars**; order box "-294.0 pips, -126.55 USD"; he says "30 pips" (28:42). Target **2003.613** (4.00
  dollars) in the fill table; the order-box frame shows 2004.601 before he finished dragging it.
- **Risk:** "Max. Risk: 0.25% (127.10 USD)". He halved the risk because of the wide stop: "we're going to
  reduce our risk even more" (29:00).
- **What was drawn (frame 29:10):** the lower band from Trade 2 at about 2009.0 (about 0.4 thick, orange
  line tagged 2009.01), now overhead as resistance; the 2012.85 band above it.
- **Higher timeframes:** none checked. This is the same morning's structure seen from below.
- **Entry trigger:** the 15:00 to 15:30 M30 candle **closed** bearish under the 2009.0 band after its wick
  had pushed up through the band to about 2010.4. He sold at the close, 15:30:00.
- **Stated reason:** "we have a resistance formed with a retest on the 30 minute time frame" (28:25).
- **Stop logic:** above the wick high of that candle (2010.557).
- **Management:** none.
- **Outcome:** target filled 21 seconds later. **+172.04 USD = +1.36R.** Drawdown 0. The next candle was a
  news spike. He had not checked: "Oh, was this news? I didn't even look at the news." (29:10). He says he
  will "ignore this win" (29:25).

## Trade 4 - Tuesday buy, London-open break of the range (stop from the 15-minute chart)

- **Video time:** entry about 35:50 (order box at 35:45). Stop tightened about 36:05. Partial about 36:30.
  Stopped at break-even about 37:00.
- **Replay time:** entry Tue 18.04.2023 **10:30:00** (07:30 UTC, 08:30 London). Partial 10:37:03.
  Remainder stopped 10:48:43.
- **Chart at entry:** M15 on screen for the order (M30 a moment before and after).
- **Direction and prices:** BUY 1.01 lots at **2002.085**. Stop **1999.561**. Stop distance **2.524
  dollars**; order box "-252.0 pips, -254.92 USD"; he says "25 pips stop. It's still pretty big" (35:40).
  TP on the fill 2007.378, not meant as a fixed target.
- **Risk:** "Max. Risk: 0.50% (255.05 USD)".
- **What was drawn (frame 35:15):** range bands with orange lines at **2001.19** (upper, about 0.25 thick,
  on the body tops of the two candles at the 08:00 high) and **1998.06** (lower, about 0.3 thick, on body
  bottoms; wicks reach about 1996.7 below). Width 3.13 dollars: "This is 30 pip range" (34:17). A separate
  thicker support band at about 1993.2 to 1993.9 lower down, on the body bottoms of the overnight lows.
- **Higher timeframes:** 4-hour (viewed, frame not kept): fell from about 2011 to 1992 on Monday, then two
  bullish candles back to about 1998; he first reads possible rejection lower (30:15). 1-hour: price had
  broken above an hourly resistance with clean candles to the left, so he switches to looking for support
  and continuation up. "We looked at the 4 hour for a bias." (31:15).
- **Entry trigger:** the candle ending 10:30 (a 15-minute close and also the 10:00 to 10:30 M30 close)
  **closed** above the 2001.19 band, at London open. Bought at 10:30:00.
- **Stated reason:** "15-minute candle is closing above this area. We have clean range to the left hand
  side ... this is in London open" (34:45).
- **Stop logic:** the 30-minute candle would need a 34 to 38 pip stop, which he rejects; he uses the low of
  the 15-minute candle instead. "I'm going to put the stop based on the 15minut time frame" (35:38).
- **Management:**
  1. When the next candle broke the high: stop tightened from 1999.561 to **2001.150**, i.e. just under the
     2001.19 band (frame 36:20). "I'm going to bring my stops in a little tighter" (36:10).
  2. 10:37:03: closed **0.91 lots (90%)** at 2003.755 (+1.67 dollars, +151.97 USD). He says "16 17 pips"
     (36:25). Stop on the rest to break-even 2002.085.
  3. 10:48:43: remaining 0.10 lots stopped at 2002.085, 0.00 USD.
- **Outcome:** **+151.97 USD = +0.6R.** Drawdown 0.74 dollars. 7 minutes to the partial, 19 in total.
- **Afterwards:** he says he took the partial early because he suspected trouble at the highs to the left
  ("had a little bit of a epiphany", 38:05).

## Trade 5 - Tuesday buy, continuation after a no-bottom-wick candle (the only loss)

- **Video time:** entry about 38:55 (order box at 38:45). Stop trailed about 39:55. Closed by hand 41:10.
- **Replay time:** entry Tue 18.04.2023 **12:00:00** (09:00 UTC, 10:00 London). Exit 12:26:07.
- **Chart at entry:** XAUUSD, M30.
- **Direction and prices:** BUY 1.57 lots at **2003.285**. Initial stop **2001.661** (fill table). Stop
  distance **1.624 dollars**. The order-box frame, before he finished dragging, shows 2001.746 "-153.0
  pips"; he says "15 pips stop" (38:40). TP on the fill 2007.747, placed far away ("all the way up").
- **Risk:** "Max. Risk: 0.50% (255.81 USD)".
- **What was drawn (frame 38:45):** the 2001.19 band (now below price) and the orange line at about 1998.1.
  Nothing new drawn for this trade.
- **Higher timeframes:** none re-checked.
- **Entry trigger:** the 11:30 to 12:00 M30 candle **closed** bullish above the 2001.19 band with no lower
  wick; the candle before it was small-bodied (which he had read as low volume, 37:30). Bought at 12:00:00.
- **Stated reason:** "whenever a candle is closing bullish above resistance, has no wick at the bottom ...
  very good probability for the next candle to go up" (38:55).
- **Stop logic:** below the trigger candle.
- **Management:**
  1. After the 12:00 to 12:15 M15 candle closed bullish: stop trailed up to **2002.157**, under that candle
     (frame 39:57). "Let's trail this stop loss below the 15-minute candle" (39:50).
  2. 12:26:07: **closed the whole position by hand** at 2002.505, before the stop. "I know it's going to hit
     my stop ... Why would I stay in the trade" (41:00).
- **Outcome:** **-122.46 USD = about -0.5R** (-0.78 dollars a lot). Worst drawdown 0.98 dollars. Held 26
  min. Within about 90 seconds of his exit the bid was 2001.10 (scan frame, not kept), so the trailed stop
  at 2002.157 would have filled for about -177 USD and the original stop for about -255 USD.
- **Afterwards:** "there was a fake out. I don't know. I'm not going to focus on fake outs." (41:50).

## Trade 6 - Wednesday sell, pre-London break below the range (largest winner)

- **Video time:** entry about 49:50 to 50:05 (open order visible at 50:12). Break-even about 50:20. Partial
  52:05. Rest closed about 52:45.
- **Replay time:** entry Wed 19.04.2023 **08:45:03** (05:45 UTC, 06:45 London). Partial 09:17:43. Rest
  closed 09:28:08.
- **Chart at entry:** **M15** (frame 48:12, 50:12).
- **Direction and prices:** SELL 1.28 lots at **2001.675**. Stop **2003.665**. Stop distance **1.990
  dollars**. TP on the fill 1994.972, removed later ("let's remove the ... take profit", 51:30). His spoken
  pip figure for this stop is not clear in the captions (UNREADABLE; the order box was not on screen in any
  frame I pulled).
- **Risk:** panel set to 0.50%; 1.28 lots x 1.99 = about 255 USD. He likens it to Monday's first trade and
  says he normally uses 1% (48:30).
- **What was drawn (frames 46:50, 48:12):** range bands with orange lines at **2004.97** (upper, about 0.45
  thick, on the body tops of the overnight candles, starting about 8 candles back) and **2002.58** (lower,
  about 0.55 thick). The lower band is an older one that runs back across Tuesday, touching body edges on
  both days. Width about 2.4 dollars. A third band at about 2009.2 to 2009.8 marks Tuesday's high.
- **Higher timeframes:** Daily (frame 44:52): two small candles sitting on the low of last Friday's big
  bearish candle near 2004; he reads the daily as having made support (45:10). 4-hour: "creating a
  resistance" (transcript, 45:30). 1-hour (frame 45:52): the 2002.6 band under price and the 2009.5 band
  above; he calls the room "30 32 pips" (45:55). At the moment of entry he re-checks: 1-hour breaking down,
  4-hour breaking its low, daily coming down (48:00).
- **Entry trigger:** the 08:30 to 08:45 **M15** candle **closed** below the lower band (close about 2001.7,
  low about 2000.9), a full-bodied bearish candle. He sold 3 seconds after that 15-minute close. The
  30-minute candle (08:30 to 09:00) was still open.
- **Stated reason:** "it's kind of like the same idea we had on Monday" (48:35), i.e. long consolidation
  then a break in the pre-London window.
- **Stop logic:** above the high of that 15-minute candle, not above the band. Asked why not above the
  resistance: "it's going to be above the candle right here" (50:05).
- **Management:**
  1. By 08:54 (about 9 minutes in, price +1.3): stop to break-even 2001.675. "Put stops at break even ...
     It's a free trade now." (50:20).
  2. No early partial, on purpose: "since we're in profits on Wednesday, Thursdays, I don't secure
     positions" (50:40).
  3. 09:17:43: closed **1.15 lots (90%)** at 1991.905 (+9.77 dollars, +1,123.55 USD) as price reached an
     area that had rejected before (about 1993). "we're coming up to a rejection area" (52:00). Stop on the
     rest trailed to 1994.498.
  4. 09:28:08: closed the last 0.13 lots by hand at 1989.065 (+12.61, +163.93 USD).
- **Outcome:** **+1,287.48 USD = about +2.5% = about +5.0R.** Drawdown 0.48 dollars. Held 33 min to the
  partial, 43 min in total.
- **Afterwards:** "let positions run. If you are in profits from Monday and Tuesday, let them run on
  Wednesday and Thursday" (52:25).

## Trade 7 - Wednesday sell, first resistance in the new downtrend (stop from the 15-minute chart)

- **Video time:** entry about 54:10 (order box at 54:02, running order at 54:18). Partial about 54:35.
  Last piece closed while he stepped candles forward, about 55 to 56 min (not pinned to a frame).
- **Replay time:** entry Wed 19.04.2023 **11:00:00** (08:00 UTC, 09:00 London). Partial 11:07:41. Rest
  closed 11:48:58.
- **Chart at entry:** M15 for the order box, M30 for the decision.
- **Direction and prices:** SELL 1.54 lots at **1991.275**. Stop **1992.964**. Stop distance **1.689
  dollars**; he says "the stop is going to be 17 pips" (53:58). TP on the fill 1986.903, then removed.
- **Risk:** "Max. Risk: 0.50% (261.64 USD)".
- **What was drawn (frame 54:18):** one grey band at about 1994.3, about 0.4 thick, on the body tops of the
  two retrace candles (the bullish 10:00 candle's close and the bearish 10:30 candle's open); both wicks
  stick about 0.8 to 1.0 above it. Drawn from candles only one and two bars back.
- **Higher timeframes:** deliberately ignored. "It's a downtrend. I'm not looking at the 4 hour. Not
  looking at the daily." (53:30). He does cite a 1-hour wick left to fill below (54:55).
- **Entry trigger (frame 53:45):** after the fall, the 10:00 to 10:30 M30 candle was bullish (about 1991.0
  to 1994.1); the 10:30 to 11:00 candle **closed** bearish, giving back the whole body (close about 1991.3,
  top wick to about 1995). Sold at 11:00:00, at the close.
- **Stated reason:** "We have created resistance in a downtrend." (53:45).
- **Stop logic:** above the 30-minute candle would be "40 pips. Too big"; so above the last 15-minute
  candle instead. "we're putting the stops based off of the 15-minut time frame" (54:10).
- **Management:**
  1. 11:07:41: closed **1.39 lots (90%)** at 1987.598 (+3.677 dollars, +511.10 USD) and stop on the rest to
     break-even 1991.275. "I'm going to close 90%. Because this was not planned at all" (54:30).
  2. 11:48:58: last 0.15 lots closed at 1978.825 (+12.45, +186.75 USD).
- **Outcome:** **+697.85 USD = about +2.7R.** Drawdown 0.24 dollars. 7 min 41 s to the partial, 49 min in
  total.
- **Afterwards:** "I wish I could have caught this move" (56:40), about the size of the continuation.

## Trade 8 - Friday sell, break of the previous 30-minute low after an hourly support broke

- **Video time:** entry about 1:07:00 (price frame 1:06:42, order box 1:06:58). Break-even about 1:07:25.
  Partial about 1:07:40. Rest closed about 1:08:10.
- **Replay time:** entry Fri 21.04.2023 **08:11:36** (05:11 UTC, 06:11 London). Partial 08:35:36. Rest
  closed 09:34:35.
- **Chart at entry:** XAUUSD, M30.
- **Direction and prices:** SELL 3.88 lots at **1999.915**. Stop **2001.280**. Stop distance **1.365
  dollars**; he says "stop is like 13 pips or whatever" (1:06:55). TP on the fill 1997.387, then removed.
- **Risk:** "Max. Risk: 1.00% (530.26 USD)". The only 1% trade. "Let's go like 1%." (1:06:50).
- **What was drawn (frames 1:05:35, 1:06:42):** a thin band at about 2001.8 (tooltip reads "M30 Rectangle
  ... 2001.815"), about 0.3 thick, on the body bottoms of the last six or so hourly candles: the hourly
  support that has just been broken. A band at about 1997.4 lower down, marking the first "wick fill"
  target. A thick band at about 1991.9 to 1992.8 on Thursday morning's lows. Blue arrows are his
  explanation marks, not levels.
- **Higher timeframes:** Daily "just consolidating", ignored (transcript, 1:04:25). 4-hour "maybe starting
  to come down" (transcript). 1-hour (frame 1:05:35): the 07:00 candle closed at 2000.495, below the 2001.8
  band (status bar O 2002.075, H 2002.265, L 2000.235, C 2000.495). "1 hour candle has basically broken and
  closed below the support" (1:05:20).
- **Entry trigger:** on the M30 chart, lower highs and lower lows after the hourly break. He sold when the
  **still open** 08:00 to 08:30 candle broke the low of the previous 30-minute candle, 11 min 36 s into it.
  This is not a candle-close entry.
- **Stated reason:** "we broke support closed below support ... lower high and lower low to possibly fill
  these wicks" (1:06:25).
- **Stop logic:** above the high of the current 30-minute candle; the stop at 2001.28 sits about 0.5 under
  the broken band.
- **Management:**
  1. At the 08:30 candle close (price +1.7): stop to break-even 1999.915. "Let the candle close ... Put
     stops at break even." (1:07:15).
  2. 08:35:36: closed **3.49 lots (90%)** at 1995.765 (+4.15 dollars, +1,448.35 USD). "Close 90%. It's a
     Friday." (1:07:35).
  3. 09:34:35: last 0.39 lots closed at 1986.645 (+13.27, +517.53 USD).
- **Outcome:** **+1,965.88 USD = about +3.7R.** Drawdown 0.24 dollars. 24 min to the partial, 1 h 23 min
  in total.
- **Afterwards:** asked why he did not wait for a reversal wick: because it is Friday and there is an
  hourly wick to fill (1:07:50).

## Week summary (from the simulator's own tables)

| # | Day | Entry (chart time) | Side | Entry | Stop | Stop $ | Risk | Result USD | R |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Mon | 08:30:56 | Buy | 2006.265 | 2004.792 | 1.473 | 0.5% | +583.55 | +2.3 |
| 2 | Mon | 12:00:00 | Buy | 2009.925 | 2008.242 | 1.683 | 0.5% | +255.15 | +1.0 |
| 3 | Mon | 15:30:00 | Sell | 2007.614 | 2010.557 | 2.943 | 0.25% | +172.04 | +1.4 |
| 4 | Tue | 10:30:00 | Buy | 2002.085 | 1999.561 | 2.524 | 0.5% | +151.97 | +0.6 |
| 5 | Tue | 12:00:00 | Buy | 2003.285 | 2001.661 | 1.624 | 0.5% | -122.46 | -0.5 |
| 6 | Wed | 08:45:03 | Sell | 2001.675 | 2003.665 | 1.990 | 0.5% | +1,287.48 | +5.0 |
| 7 | Wed | 11:00:00 | Sell | 1991.275 | 1992.964 | 1.689 | 0.5% | +697.85 | +2.7 |
| 8 | Fri | 08:11:36 | Sell | 1999.915 | 2001.280 | 1.365 | 1.0% | +1,965.88 | +3.7 |

Seven winners, one loser, +4,991.46 USD. Wednesday and Friday's three trades made 3,951 of it. Every stop
was between 1.37 and 2.94 dollars (13.7 to 29.4 of his pips). Worst drawdown on any trade was 0.98 dollars.

---

# Trades he refused or waited on

1. **Mon 08:00 to 08:30, inside the consolidation.** Waits for a 30-minute close above 2005 or below about
   2003.5. "we have to wait for price to break and close above or below the range" (11:50).
2. **Mon 13:30, sell on the close below the 2009 support.** Refused: the stop above that candle measured
   3,574 points. "The stop is too big ... your stop loss is 35 pips." (26:25). Plan: wait for price to come
   back up, form resistance, then sell. This became Trade 3 two hours later.
3. **Mon 14:00 to 15:00.** Still waiting; reads a small-bodied candle as "Very low volume for price to move
   down" (27:10). Refuses to drop to the 15-minute for the entry (27:15).
4. **Tue 08:30, 30-minute rejection candle.** Measures the room: 19 pips. Refused. "For me, a range needs
   to be 25 pips plus" (33:00). He typed this rule on the chart and it stays on screen for the rest of the
   video.
5. **Tue 10:30, the same breakout with a 30-minute stop.** 34 to 38 pips, refused; taken with a 15-minute
   stop instead (Trade 4). "38 pips stop we don't want that" (35:35).
6. **Tue about 13:15, a possible buy if the next candle did not break the previous low.** Thinking aloud
   only, no order (42:10). It worked; he says he will act on it if it shows up again (43:05).
7. **Wed after Trade 7.** Looks for another 30-minute resistance to sell again; none formed (56:10).
8. **Thu 08:30 to 09:00, 30-minute candle breaking the range high mid-candle.** Would be about 19 pips;
   will not enter before the close. "I'd rather wait for the 30-minut candle to close. I don't want to take
   any impulse entry" (1:00:05).
9. **Thu 09:00, after that candle closed above the small band at about 1993.3.** Skipped. "we got all these
   rejections to the left hand side, and ... I don't want to risk my gains." (1:01:30). Price then rose
   about 40 pips without him (1:02:05).
10. **Thu 10:00 to 11:30.** Waits for a pullback and a 30-minute support to buy; a candle closes, he does
    not like it. "I don't like it." (1:03:20). Refuses a 5-minute entry suggested by a viewer (1:03:30).
    No trade on Thursday.

# Rules he states in this video

- **Where to start the day:** pre-London, two hours before London open (08:00 chart time). "This is 2 hours
  before London open." (8:22).
- **Volume windows:** Asian open, pre-London, London open, pre-New York, New York open, NYSE open (19:00).
  "volume comes in chunks and we got to wait for those volume chunks" (20:15).
- **Top-down order:** daily first ("where is price most likely to head", 9:05), then 4-hour for bias, then
  1-hour and 30-minute for supports and resistances. The 1-hour picture overrides the 4-hour bias (31:10).
- **The 30-minute candle confirms.** "we're going to focus only on the 30 minute time frame" (12:20).
  "15 minute is low confirmation, weak confirmation." (28:10). (But see the frame findings: Trade 6.)
- **The 15-minute chart is for stop placement only**, when the 30-minute stop is too wide. "if the stop
  loss is too big on a 30-minut time frame, then put the stop loss based on a 15-minut time frame" (55:45).
- **Consolidation:** small candles side by side; wait for a close outside. "the longer the price
  consolidates, the harder the break" (11:55).
- **Minimum room:** "For me, a range needs to be 25 pips plus" (33:00). Measured from the candle body, not
  the wick (24:35).
- **Stop too wide = no trade yet:** wait for the retest (26:35). What he did in this video: a 25-pip stop
  taken at 0.5% risk, a 30-pip stop taken at 0.25%, and 34 to 40 pip stops refused.
- **What a support / resistance is:** a bullish candle closing after bearish candles (23:30); two candles
  are enough (24:55). Resistance is the mirror (53:45).
- **Candle reading:** a close above resistance with no top wick, or a bullish close with no bottom wick,
  favours continuation (13:25, 38:55). A small-bodied close means low volume for the next candle (37:30).
- **Stop placement:** beyond the trigger candle's extreme, because that candle has "no business" breaking
  its own low (16:30); above the candle, not above the zone (50:05).
- **Sizing:** normally 1%; 0.5% for the first trade of the week and for riskier setups (15:40); 0.25% when
  the stop is about 30 pips (29:00); 1% on Friday with the week well in profit (1:06:50).
- **Management depends on the day of the week.** Monday and Tuesday: take partials and go to break-even.
  Wednesday and Thursday, if already up on the week: break-even but no early partial. "I don't secure
  positions because I'm already in profits" (50:50). Confirmed again at 57:30.
- **Trailing:** when a 15-minute candle closes in his favour and the next breaks its extreme, the stop goes
  behind that 15-minute candle (17:20, 39:50).
- **Do not wait for the stop** when the trade has clearly failed (41:00).
- **Protect the week:** on Thursday he passes a valid-looking break to keep the week's gains (1:01:30).
- **How far left to look:** only the nearest structure, then the next one if that breaks (1:00:45).
- **Wick fills as targets:** unfilled wicks on the 1-hour chart are where he expects price to go (54:55,
  1:05:45).
- **News:** he did not check the calendar before Trade 3 and treats that win as luck (29:10, 44:55). He
  removes the simulator's news lines from the chart (29:50). No news rule is stated.
- **Not waiting for the break of the previous high** (42:45): he gives a reason about confidence in the
  analysis, then appears to take it back in the next breath. Unclear; do not treat as a rule.
- **Trade length:** "Hardly a trade lasted more than 1 hour" (1:09:15).

# What the frames show that the transcript alone would not

1. **Every price, lot size and fill time.** The simulator's History and Closed-trades tables (1:08:48,
   1:09:08) list all 22 fills. The transcript gives none of the prices.
2. **The pip proof**, eight separate ways (table at the top).
3. **The timezone**, from the Sessions panel: chart time is UTC+3.
4. **When he actually clicks, relative to the candle:**
   - Trades 2, 3, 5, 7: exactly on the 30-minute close (replay clock xx:00:00 or xx:30:00; he steps the
     replay one bar at a time with the Forward button, so he is acting on the just-closed candle).
   - Trade 4: on a close that is both a 15-minute and a 30-minute boundary.
   - Trade 1: 56 seconds into the next 30-minute candle, after it had already moved 1.0 dollar beyond the
     trigger candle's close.
   - **Trade 6: on a 15-minute close (08:45:03), with the 30-minute candle still open.** This is his biggest
     winner and it contradicts "only the 30 minute" said twenty minutes earlier in the video.
   - **Trade 8: mid-candle (08:11:36), on the break of the previous 30-minute low.** Also not a close.
5. **Stops sit beyond the trigger candle, not beyond the zone.** Distances: 1.47, 1.68, 2.94, 2.52, 1.62,
   1.99, 1.69, 1.37 dollars. Lot size is computed by the simulator from the risk percent.
6. **The take-profit in the order box is usually a placeholder.** Only Trades 2 and 3 used a real fixed
   target (1.0R and 1.36R). On the others he removed it and managed by hand.
7. **Partials are 80% once and 90% every other time**, leaving a 10% runner that he keeps for 20 minutes to
   nearly two hours. The runners' closes: +5.45, 0.00, +12.61, +12.45, +13.27 dollars.
8. **Where the first partial came:** Mon +2.95 (2.0R); Tue +1.67 (0.66R); Wed +9.77 (4.9R) and +3.68
   (2.2R); Fri +4.15 (3.0R). So the "let it run mid-week" rule is visible in the numbers.
9. **Trade 3 lasted 21 seconds** inside a spike at 15:30 chart time = 08:30 New York, a standard US data
   release time. The simulator filled the target with no slippage.
10. **Trade 5 was closed by hand at -0.78** while the trailed stop was at -1.13; price went through the
    stop level about a minute and a half later.
11. **Zones:** thin grey rectangles on body edges plus a full-width orange line through the two range
    bands; redrawn as the range evolves; wiped each morning.
12. **A typed on-screen note** from 33:10 to the end: "For me to take a trade, range needs to be 25+pips".
13. **All entries fall in three time windows:** 08:11 to 08:45 chart time (pre-London, 05:11 to 05:45 UTC),
    10:30 to 12:00 (London morning, 07:30 to 09:00 UTC), and one at 15:30 (08:30 New York).

# Is this the "Video 12" of the older transcript-only notes?

**No. This video is not that one.** Reasons:
- It is 1:11:17 long. The notes cite events at about 1:15 and 1:19, which cannot exist here.
- The transcript contains no mention of ADP, NFP, pending orders or an accidental lot size (searched: zero
  hits). No pending order is placed in any frame; all eight entries are market orders.
- The replay week is 17 to 21 April 2023, which is not a first-Friday (jobs report) week.
- At about 21:40 he is not refusing a trade for a 27-pip stop; he is measuring a 30-pip range and then
  buys (Trade 2). The stop-size refusal here is at 26:25 and the figure is 35 pips.
- There is no losing buy "from support" at about 33 minutes. At 33 minutes he is refusing a 19-pip range.
  The only loss is Trade 5, entered at about 38:55 and closed by hand at 41:10.
- There is no sell between 36 and 46 minutes; that stretch is Tuesday's two buys and commentary. His
  partials here are 80% / 90% and 90% / rest, never 50% then 90%. Lot sizes run from 0.43 to 3.88 and are
  all set by the risk-percent field; nothing is sized at 2 lots by mistake.

An unverified lead only: a keyword search of the other transcripts finds "NFP" spoken between 1:15 and
1:31 in `Gvlg1wV3zQY.txt`. I did not read that video; "ADP" does not appear under that spelling in any
long transcript, so the captions may have garbled it.

# Could not be read / open questions

- **Trade 6:** the order box was never on screen in the frames I pulled, and his spoken pip figure for the
  stop is garbled in the captions ("26 ... 25"). Prices are from the order row and the fill table.
- **Trade 7 and the runners generally:** the video second at which each last piece closed is approximate;
  the replay times are exact (fill table).
- **Order-box versus fill:** for Trades 2, 3 and 5 the order-box frame shows a TP or SL that differs from
  the fill table by 0.1 to 1.0 dollars, because he was still dragging the lines. I have used the fill table.
- **Friday's band at about 1997.4:** I could not tell which candle feature it is anchored to. He calls the
  area a wick to fill.
- **Tuesday 1-hour resistance:** in the 1-hour frame at 31:00 a band is at about 2000.6 above price, while
  the 30-minute chart a minute later has the orange-lined band at 1996.46. Which of these he means by "we
  broke above this resistance" is not certain.
- **Higher-timeframe views not kept as frames:** Monday 1-hour, Tuesday 4-hour and 1-hour, Wednesday
  4-hour, Thursday daily/4-hour/1-hour, Friday daily/4-hour. Where described, the source is marked
  (transcript) or "viewed, not kept".
- **Which news release** produced the 15:30 spike on 17 April: not shown on screen.
- **Simulator realism:** fixed 0.15 spread, no slippage, a target filled inside a 21-second news candle.
  Live results would differ on Trade 3 at least.
- **Monday Trade 1 pip wording:** he says "13 14 pips" for a stop the box shows as 14.7; treated as loose
  rounding.

## Frames kept (36), in `frames/s96BrHAScRc/`

09:24 daily Mon; 09:50 4-hour Mon; 11:10 M30 bands and room measure; 13:30 trigger candle closed; 16:00
order box T1; 16:20 open order T1; 17:45 after 80% close; 18:20 after second close; 20:10 Sessions panel;
21:45 T2 bands and 30-pip measure; 22:50 order box T2; 26:30 refused sell, 3,574-point stop; 29:10 order
box T3; 32:50 Tue 19-pip range; 35:15 Tue range at London open; 35:45 order box T4; 36:20 T4 tightened
stop; 38:45 order box T5; 39:57 T5 trailed stop; 41:12 T5 manual close; 44:52 daily Wed; 45:52 1-hour Wed;
46:50 M30 range Wed; 48:12 M15 break; 50:12 open order T6; 52:05 T6 partial; 53:45 T7 trigger candle;
54:18 T7 running; 58:58 Thu range; 1:01:30 Thu skipped break; 1:05:35 1-hour Fri; 1:06:42 Fri entry
moment; 1:06:58 order box T8; 1:07:27 T8 at break-even; 1:08:48 History table; 1:09:08 Closed-trades table.
