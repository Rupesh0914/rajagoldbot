# tcEZaXB0CxI: trade records

- **Video:** tcEZaXB0CxI, "How to Trade Gold the Right Way... A Full Live Simulation With Raja Banks", streamed 25 Aug 2023, 1:31:10.
- **Platform:** MetaTrader 5 (Dominion Markets MT5, hedge account) running an add-on replay tool titled "MT5 Simulator v1.0"
  (expert "Simulatorv1.4-PGV-29-7"). He says at 0:10:35 that it is not the Soft4FX one. Price data provider in the settings
  box: Dukascopy. Not the 2022 Soft4FX/MT4 setup.
- **Instrument:** XAUUSD, 3 digits, lot size 100 oz, starting balance 5,000 USD, leverage 1:100, fixed spread.
- **Replay dates:** Monday 20 March 2023 to Friday 24 March 2023 (start date 19/03/2023, chosen by the audience at 0:16:12).
  One trading day per weekday, each started at 08:00 chart time.
- **Where the clock is:** a small orange simulator panel shows weekday, date and time ("Mon, 20/03/2023 08:30:13") plus the
  live Buy/Sell prices, the spread and the equity. The MT5 window title shows the timeframe ("STANDARD_X,M30").
- **Order box:** "Visual Buy" / "Visual Sell" shows "Max. Risk: x% (USD)", SL price with pips and USD, TP price, reward-to-risk.
  A "Trade Panel" window lists open orders, and its History / Closed trades / Statistics tabs list everything at the end.
- **Frames:** 36 kept in `frames/tcEZaXB0CxI/`. Other moments quoted below were looked at as scan frames and then deleted.
- **Quotes:** from auto captions; obvious mishearings are corrected (caption "cell" = sell, "pre-lendon" = pre-London).

## Pip size in this video (checked, three ways)

His pip is 0.10 dollars. The simulator's pip is 0.01 dollars, ten times smaller, exactly as in the 2022 simulator.

1. Settings box (frame 0:16:45): "Pip size: 10 points (0.010)", "Spread: Fixed 150 points (0.150)". The panel then prints
   that 0.15 dollar spread as "Spread: 15.0 pips" (Buy 1973.525 / Sell 1973.375 at 0:21:00).
2. MT5 crosshair ruler against his words: frame 0:23:50 reads "3349 points" for 1972.74 down to 1969.39 (3.35 dollars) and
   he says "this is a 33 pip range" (0:23:45). Frame 0:26:20 reads "3564 points" for 1979.31 down to 1975.75 (3.56 dollars)
   and he says "35 pip range" (0:26:11).
3. Order boxes against his words:
   - Trade 2: SL 1976.352 on a sell at 1972.958 = 3.394 dollars, box says "-339.0 pips", he says "33 pip stop" (0:46:21).
   - Trade 4: SL 1937.868 on a buy at 1939.725 = 1.857 dollars, box says "-185.0 pips", he says "18 pip stop" (1:00:42).
   - Trade 5: SL 1974.448 on a buy at 1977.774 = 3.326 dollars, box says "-332.0 pips", he says "29 pips" (1:07:02). Here
     his spoken figure is about 4 pips smaller than the stop he actually placed.
   - Trade 1 final close: Trade Panel shows "1130.0" pips for +11.30 dollars, he says "a hundred and eleven pips" (0:30:23).

## Chart time zone (checked)

The settings box has "Time on charts: New York Close" (he picks it over GMT, frame 0:16:45). The built-in news calendar,
which uses the same clock, lists UK CPI at 10:00 on 22/03 (real time 07:00 GMT), the Federal Funds Rate at 21:00 on 22/03
(real 18:00 GMT = 14:00 New York) and Canadian CPI at 15:30 on 21/03 (real 12:30 GMT). So in this week chart time = GMT+3 =
New York time + 7 hours = Dubai time - 1 hour.

His session words on this clock (read from the panel at the moment he says them):
- "pre-London ... around 8 A.M" (0:20:39): 08:00 chart = 05:00 GMT = 01:00 New York.
- "London open": he says it at 09:53 chart on Tuesday (0:42:33), "in one hour" at 09:03 on Wednesday (0:57:49), and at 10:06
  on Friday (1:16:54). So his London open is 10:00 chart = 07:00 GMT = 03:00 New York. The simulator's own Sessions panel
  paints London from 11:00 and New York from 15:00.
- "New York open": 15:00 chart = 08:00 New York (trade 3). "NYSE open": 16:30 chart = 09:30 New York.

## Summary table (from the simulator's History tab, frame 1:21:25, all rows readable)

| # | Day (chart time) | Side | Lots | Entry | Initial stop | Stop in dollars / his pips | Risk shown | Exits | Result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Mon 20/03 08:30:13 | Buy | 0.46 | 1975.695 | 1974.067 | 1.628 / 16.3 | 1.50% | 0.37 at 1978.815 (08:47:37); 0.09 at 1986.995 (08:58:48) | +217.14 USD, 2.9 R |
| 2 | Tue 21/03 10:54:25 | Sell | 0.15 | 1972.958 | 1976.352 | 3.394 / 33.9 | 1.00% | 0.12 at 1968.675 (11:06:25); 0.03 at 1952.828 (17:45:47) | +111.79 USD, 2.2 R |
| 3 | Tue 21/03 15:02:47 | Sell | 0.12 | 1965.525 | 1967.703 | 2.178 / 21.8 | 0.50% | 0.12 at 1952.828 (17:45:47) | +152.36 USD, 5.8 R |
| 4 | Wed 22/03 11:00:12 | Buy | 0.44 | 1939.725 | 1937.868 | 1.857 / 18.6 | 1.50% | 0.35 at 1944.614 (11:18:12); 0.09 stopped at entry (14:44:36) | +171.12 USD, 2.1 R |
| 5 | Thu 23/03 08:00:00 | Buy | 0.08 | 1977.774 | 1974.448 | 3.326 / 33.3 | 0.50% | 0.04 at 1976.745 (08:15:43); 0.02 at 1978.555 (08:30:09); 0.02 at 1982.205 (09:29:45) | +6.30 USD, 0.24 R |
| 6 | Fri 24/03 09:16:21 | Sell | 0.66 | 1989.545 | 1991.250 | 1.705 / 17.1 | 2.00% | 0.53 at 1985.685 (09:33:48); 0.13 at 1986.645 (10:01:06) | +242.28 USD, 2.15 R |
| 7 | Fri 24/03 11:35:59 | Sell | 2.59 | 1987.525 | 1988.660 | 1.135 / 11.4 | 5.00% | 2.59 at 1981.545 (11:40:35) | +1548.82 USD, 5.3 R |

Balance 5,000.00 to 7,449.81 (+49.0%). Before trade 7 the balance was 5,900.99 (+18.0%); trade 7 alone is 63% of the week's
profit. Statistics tab (frame 1:20:40): 13 closing deals, 11 profitable, 2 "loss" (one of -4.12, one of 0.00), largest
profit 1548.82, max drawdown 80.29 (1.36%), 977,338 ticks. No trade lost its full stop.

All seven are market orders, each placed with the replay paused. No pending orders anywhere in the video.

---

## Trade 1: Monday buy on a 30-minute close above resistance

- **Video time:** entry about 0:26:20 to 0:26:50 (frame 0:26:50 shows the open order); partial at 0:28:55; final close 0:30:23 to 0:30:35.
- **Replay time:** entry Mon 20/03/2023 08:30:13; partial 08:47:37; final exit 08:58:48 (chart time, = 05:30 to 05:59 GMT,
  01:30 to 01:59 New York).
- **Instrument / timeframe on screen:** XAUUSD, M30.
- **Direction and prices:** Buy 0.46 lots at 1975.695. Stop 1974.067. Take-profit first set at 1979.372, then removed
  (Trade Panel in scan frame 0:27:15 shows the TP cell empty).
- **Stop distance:** 1.628 dollars = 16.3 of his pips. He does not say a pip figure for this stop.
- **Risk:** panel "Risk %: 1.50"; he says "we're going to risk let's say 1.5 percent" (0:25:48). 0.46 lots x 1.628 x 100 = 74.9 USD.
- **Zones drawn (frames 0:24:50, 0:26:20, 0:26:50):** three grey rectangles on M30, each about 0.3 to 0.45 dollars thick,
  drawn from candles 2 to 5 hours back the same morning.
  - Resistance band about 1974.85 to 1975.12: on the body tops of the swing-high candles around 04:30 to 05:00 (bullish
    close and bearish open near 1974.75), their upper wicks poke through to about 1975.3.
  - Support band about 1972.85 to 1973.20: on the body bottoms of the pullback candles around 05:30 to 06:30, lower wicks
    poke through to about 1972.4.
  - Lower support band about 1969.1 to 1969.55 with an orange horizontal line labelled 1969.37: at the body bottoms of the
    morning low (03:00 to 04:00 candles), wicks through to about 1968.0. He speaks of it as "1969".
  - First drawn on H1 (frame 0:23:50) at 1972.7 and 1969.4, then refined on M30.
- **Higher timeframes:** Daily (frame 0:21:50): steep rise through March; Friday 17 March is a very large bullish candle
  (status bar: O 1920.774, H 1988.998, C 1987.798); Monday's candle so far is small and red near 1975. He reads "the trend on
  the Daily is bullish" (0:21:42). H4 (0:22:10): stair-step up, last candles a red pullback then a small green; he reads
  "four hour ... creating a support". H1 (0:22:50, 0:23:50): pullback from about 1990 to 1969.5, then small green candles.
- **Entry trigger:** the 08:00 to 08:30 M30 candle closed bullish with its body from about 1974.75 up to about 1975.6, i.e.
  it opened under the resistance band and closed above it. Small body (about 0.85 dollars), short upper wick. He entered 13
  seconds into the next candle. Candle closed, not open.
- **Stated reason:** "we had price come down we created support and as we created support this candle is closed above" (0:25:48).
- **Where the stop really sits:** about 0.7 dollars under the bottom of the trigger candle's body, roughly level with the
  open/low of the candle before it (07:30) and about 0.9 above the middle support band. His words: "your stop loss is going
  to be below the previous candle" (0:26:11).
- **Target thinking:** measured 35 pips of room to about 1979.3, then says "take profit it doesn't matter" because of "a
  bigger clean range going all the way up till 1984" (0:26:32 to 0:26:54).
- **Management:**
  - 08:47:37, price 1978.815 (+3.12 dollars, panel "312.0"): closed 0.37 of 0.46 lots (80%), +115.44 USD, and moved the stop
    to entry 1975.695. Price was at his 1979 resistance. "close 80 put stop loss at break even and let the rest run" (0:29:02).
    He calls the profit "27 28 pip" just before (0:28:16); the panel shows 31.
  - 08:58:48, price 1986.995 (+11.30 dollars): closed the last 0.09 by hand, +101.70 USD. "we're going to secure these
    positions right here a hundred and eleven pips" (0:30:23).
- **Outcome:** +217.14 USD (+4.34%), 2.9 times the money risked (1.9 R on the first part, 6.9 R on the rest). Held 28.5
  minutes. The whole move happened inside the single 08:30 M30 candle.
- **Afterwards:** shows how he would handle having missed it (wait for a retrace and new support), then stops for the day:
  after "4.3 percent" in one trade he moves to the next day and skips New York (0:34:53 to 0:35:36).

## Trade 2: Tuesday sell, "impulse entry" after a broken support was retested

- **Video time:** order box 0:46:44, open at 0:46:50; partial 0:47:35; final close 0:52:55.
- **Replay time:** entry Tue 21/03/2023 10:54:25; partial 11:06:25; final 17:45:47 (entry = 07:54 GMT, 03:54 New York).
- **Timeframe on screen:** M30 for the decision, M15 to place the stop.
- **Direction and prices:** Sell 0.15 lots at 1972.958. Stop 1976.352. TP in the box 1969.011 (reward-to-risk 1.16), dragged
  lower to 1966.483 on accepting, then removed.
- **Stop distance:** 3.394 dollars. Box: "-339.0 pips, -50.91 USD". He says "33 pip stop" (0:46:21).
- **Risk:** box "Max. Risk: 1.00% (52.17 USD)". "since our stop loss is bigger we're going to lower our risk to one percent" (0:46:21).
- **Zones (frames 0:38:15, 0:41:20, 0:46:30):** Monday's zones are gone; he drew fresh ones at 08:00.
  - Resistance: thin band (about 0.3) with orange line labelled 1984.02, on the body tops of the 06:00 to 07:00 candles,
    one wick through to about 1985.
  - Minor support: very thin band and orange line at about 1979.85 (label partly legible), on the body bottoms of small
    candles 2 to 3 hours back.
  - Main support: band about 1975.65 to 1976.1, later with an orange line labelled about 1976.15; drawn at body bottoms of
    lows 5 to 13 hours back (Monday evening and early Tuesday), wicks through to about 1975.2.
  - Target band about 1966.5 to 1966.9, at the body bottom of Monday afternoon's low, roughly 15 hours back. He names "1966".
- **Higher timeframes:** Daily (frame 0:36:30): Monday closed as a small red body with a very long upper wick (to about
  2009); "still the daily is bullish but we're creating some sort of a resistance" (0:36:17). H4: three rising candles with
  shrinking bodies; he reads fading buying. H1: resistance band near 1984, "81 pip range".
- **Sequence before entry:**
  - 08:00 to 09:00: price mid-range between 1984 and 1979; no trade.
  - 09:19: price pushes under the 1979.85 line mid-candle; he refuses to sell (see refusals).
  - 09:30 candle: closes far below the 1976 support (status bar: O 1976.824, H 1976.835, L 1971.664, C 1973.245).
  - 10:00 candle: rallies to about 1978.8 by wick, back above the broken support, and closes green at about 1975.3, under
    the line. He will not sell a green close: "we cannot take a sell because the candle has still closed bullish" (0:44:37).
  - 10:30 candle: he waits for it to take out the previous candle's low.
- **Entry trigger:** mid-candle. The open 10:30 M30 candle makes a new low at 1972.958 (status bar at the paused entry: O
  1975.348, H 1977.248, L 1972.958), just under the 10:00 candle's low (about 1973.1 to 1973.2). That is still above the
  09:30 candle's wick low of 1971.664. "we broke below the low impulse entry one percent risk" (0:47:04).
- **Where the stop really sits:** 1976.352 is about 0.2 above the broken support line (1976.15), above the highs of the last
  two M15 candles. It is below the current M30 candle's high (1977.248). He explains: for an impulse entry the stop goes above
  the current candle ("45 pips"), not the previous one ("60 pips"); that being too big, he drops to the 15-minute chart for
  a 33-pip stop (0:46:00 to 0:46:21).
- **Management:**
  - 11:06:25 at 1968.675 (+4.28 dollars, panel "428.0"): closed 0.12 of 0.15 (80%), +51.40 USD, stop to entry 1972.958.
    "we're going to close let's say 80 percent ... stops at break even" (0:47:24 to 0:47:44).
  - About 15:05 (frame 0:52:05, while placing trade 3): stop on the remaining 0.03 dragged down to 1969.610 ("334.0 pips,
    10.04 USD" locked).
  - Later, with price near 1955: stop moved again to 1965.796 (Closed trades tab), just above the 1965.6 to 1966.05 band.
  - 17:45:47 at 1952.828 (+20.13 dollars): closed by hand, +60.39 USD. "the first position 0.03 ran 200 pips" (0:52:52).
- **Outcome:** +111.79 USD, 2.2 times the risk (1.26 R on the first part, 5.9 R on the remainder). Held 12 minutes to the
  partial, 6 h 51 m in all.

## Trade 3: Tuesday second sell at the New York open (added while trade 2's remainder was running)

- **Video time:** entry about 0:51:15 to 0:51:40; exit 0:52:55.
- **Replay time:** entry Tue 21/03/2023 15:02:47 (= 12:02 GMT, 08:02 New York); exit 17:45:47.
- **Timeframe on screen:** M30.
- **Direction and prices:** Sell 0.12 lots at 1965.525. Stop 1967.703. TP 1958.079 at entry, later removed.
- **Stop distance:** 2.178 dollars = 21.8 pips. No pip figure spoken.
- **Risk:** panel "Risk %: 0.50" (frame 0:51:40 scan). "when you're winning decrease your risk ... now we're taking an extra
  trade" (0:51:09 to 0:51:29).
- **Zone (frame 0:51:15):** one new grey band about 1965.6 to 1966.05, at the body bottoms of the consolidation candles
  from about 11:30 to 14:30 (and matching Monday's low area far left). Wicks under it reach about 1964.5 and one to 1962.8.
- **Context:** after the morning fall price went sideways for about three hours. He checks the calendar (frame 0:50:15 scan):
  only Canadian CPI at 15:30, which he dismisses, so he expects the New York open to break the range. "when price breaks
  below this ... previous low" (0:50:28).
- **Entry trigger:** mid-candle, 2 min 47 s into the 15:00 M30 candle, as price pushed through the band under the
  consolidation's body floor. Not below the extreme wick lows. "very good opportunity for an impulse entry" (0:50:48).
- **Where the stop sits:** about 1.7 above the band, above the bodies of the last consolidation candles.
- **Management:** stop moved to 1965.663 once price had collapsed (frame 0:52:40: "-13.0 pips, -1.66 USD", i.e. entry plus
  the spread, on the band). The collapse came on the 16:30 candle (NYSE open), from about 1964 to about 1952.7. Closed by
  hand at 1952.828 at 17:45:47. He says "let's forward this till London close ... close everything right here" (0:52:31 to 0:52:52).
- **Outcome:** +12.70 dollars = "126 pips" (0:52:52), +152.36 USD, 5.8 R. Held 2 h 43 m.

## Trade 4: Wednesday "fake-out" buy

- **Video time:** order box 1:01:10; partial 1:02:20; remainder stopped at entry, noticed at 1:04:35.
- **Replay time:** entry Wed 22/03/2023 11:00:12 (= 08:00 GMT, 04:00 New York); partial 11:18:12; stop-out 14:44:36.
- **Timeframe on screen:** M30 for the decision, M15 for the stop.
- **Direction and prices:** Buy 0.44 lots at 1939.725. Stop 1937.868. TP 1944.868 at entry, then removed.
- **Stop distance:** 1.857 dollars. Box: "-185.0 pips, -81.71 USD". He says "18 pip stop" (1:00:42).
- **Risk:** box "Max. Risk: 1.50% (82.22 USD)". "we're going to move on to our regular risk 1.5" (1:00:42).
- **Zones (frames 0:56:50, 1:00:10):** resistance band about 1944.3 to 1944.7 with orange line 1944.46, on body tops 3 to 5
  hours back with a wick through to about 1945.8; support band about 1937.9 to 1938.4 with orange line 1938.09, on body
  bottoms from the previous evening and from 07:00 to 08:00, wicks through to about 1935.
- **Higher timeframes:** H4 (scan 0:55:45): two days of falling candles from about 1985; last H4 candle bearish (O 1943.415,
  C 1939.215). H1: range between about 1944 and 1936.4. He calls it "a very difficult price action because we're in a range" (0:56:00).
- **Sequence:** the 10:00 M30 candle (the UK CPI release is at 10:00 on the calendar, frame scan 0:54:40) fell from about
  1942.3 and closed at about 1935.9, below support, wick to about 1934.2. The 10:30 candle closed green at about 1939.6, back
  above the support band.
- **Entry trigger:** that 10:30 candle closing back inside the range. Entered 12 seconds after its close. Closed candle,
  large green body (about 3.7 dollars) that recovered most of the breakdown candle.
- **Stated reason:** "I think this is a really good fake out why because we have a 50 pip range" (1:00:22).
- **Where the stop sits:** about 0.2 under the support line (1938.09), under the last M15 candle. A stop under the M30 candle
  would have been "40 pips" (1:00:42), so he used the M15.
- **Management:** 11:18:12 at 1944.614 (+4.89 dollars, panel "488.0"), exactly at the resistance band: closed 0.35 of 0.44
  (80%), +171.12 USD, stop to entry. "let's close another 80 percent same idea put stops at break even" (1:02:06). The last
  0.09 was stopped at 1939.725 at 14:44:36 for 0.00.
- **Outcome:** +171.12 USD, 2.1 R. 18 minutes to the partial.
- **Afterwards:** "garbage price action" (1:04:35). He redrew support lower at 1935.52 (frame scan 1:03:40) and planned a sell
  on a break of that low; it never broke. The evening spike was FOMC: "we don't trade news" (1:04:56).

## Trade 5: Thursday buy, cut down quickly

- **Video time:** order box 1:07:45; cuts at 1:08:15 and about 1:08:55; final close 1:10:18.
- **Replay time:** entry Thu 23/03/2023 08:00:00 (= 05:00 GMT, 01:00 New York); exits 08:15:43, 08:30:09, 09:29:45.
- **Timeframe on screen:** M30, then M15 for the stop.
- **Direction and prices:** Buy 0.08 lots at 1977.774. Stop 1974.448. TP 1984.075 (box first showed 1983.872, reward-to-risk
  1.83). This is the only trade where the TP was left on.
- **Stop distance:** 3.326 dollars. Box: "-332.0 pips, -26.61 USD". He says "the stop loss is like 29 pips" (1:07:02).
- **Risk:** box "Max. Risk: 0.50% (28.26 USD)". "we're going to lower our risk because the stop loss is bigger" (1:07:22).
- **Zones (frames 1:07:45, 1:08:15):** resistance band about 1984.05 (the same level as Tuesday's resistance), which is also
  where the TP sits; support band about 1972.8 to 1973.3 drawn where candle bodies topped late Wednesday and where the
  morning's candles broke up through.
- **Higher timeframes:** Daily (scan 1:05:50): Wednesday closed strongly up after the Fed; "daily is pushing up". H4 (scan
  1:06:25): V-shaped recovery from about 1936; resistance "51 pips away"; last candle "no wick on the top". H1: bodies
  getting smaller.
- **Entry trigger:** the 07:30 M30 candle "closed above the previous candle" (1:07:02) with support beneath. Entered at
  08:00:00, the first second of the next candle.
- **Where the stop sits:** under the lows of the last four M15 candles, about 1.2 above the support band.
- **Management:**
  - 08:15:43: the first M15 candle after entry closed bearish; closed half (0.04) at 1976.745, -4.12 USD. "we're going to
    manage risk because we wanted price to move up" (1:08:24).
  - 08:30:09: the M30 candle closed green but small; closed half of the rest (0.02) at 1978.555, +1.56 USD. "the size of the
    30 minute candle is small which means maybe the volume going up is decreasing" (1:08:45).
  - By 09:15: stop on the last 0.02 moved to entry (frame scan 1:09:50).
  - 09:29:45: closed the last 0.02 at 1982.205, +8.86 USD. He calls the move "53 pips" (1:10:10).
- **Outcome:** +6.30 USD, 0.24 R. Price went on toward the target after he had cut to a quarter size. Held 1 h 30 m.
- **His comment:** "I'm very patient with my profitable setups but I'm very impatient with my risky setups" (1:09:05).

## Trade 6: Friday sell on a break below a consolidation

- **Video time:** order box 1:15:22; partial 1:15:58; final close about 1:16:45.
- **Replay time:** entry Fri 24/03/2023 09:16:21 (= 06:16 GMT, 02:16 New York); partial 09:33:48; final 10:01:06.
- **Timeframe on screen:** M30.
- **Direction and prices:** Sell 0.66 lots at 1989.545. Stop 1991.250. TP 1983.666 in the box (reward-to-risk 3.45), then removed.
- **Stop distance:** 1.705 dollars. Box: "-170.0 pips, -112.53 USD". No pip figure spoken for the stop.
- **Risk:** box "Max. Risk: 2.00% (113.17 USD)". "we're going to go with a massive two percent risk" (1:15:07).
- **Zones (frame 1:12:50):** resistance band about 1993.63 to 1993.95 on the body tops of the overnight consolidation; support
  band about 1989.96 to 1990.24 on its body bottoms (wicks through to about 1989.2); an older long band about 1983.7 from
  Thursday's breakout base, which is where the box TP sat. All about 0.3 dollars thick. Consolidation about 7 hours old.
- **Higher timeframes:** Daily "still bullish"; H4 "basically consolidating" so "there's a huge break coming up" (1:11:37);
  H1 (scan 1:12:12): tight box between about 1990 and 1994, "36 pip range". Plan: a break and close above 1994 or below 1989,
  with "57 pip range" below and "43 pip" above (1:12:40).
- **Sequence:** the 08:00 candle fell to the support, wicked to about 1989.2 and closed on the band: "we closed back in the
  range" so no sell (1:13:24). The 08:30 candle left a tiny body near 1990.3 with an upper wick of about 2.7 dollars.
- **Entry trigger:** mid-candle, 16 minutes into the 09:00 M30 candle, when price had pushed about 0.4 under the support band
  and under the body lows. It had not yet passed the 08:00 candle's wick low (about 1989.25). "impulse entry right there as
  we're breaking below the low" (1:14:47).
- **Where the stop sits:** about 0.4 above the high of the current (09:00) candle. "stop losses above this candle" (1:15:27).
- **Management:** 09:33:48 at 1985.685 (+3.86 dollars, panel "386.0"): closed 0.53 of 0.66 (80%), +204.58 USD, stop to entry.
  "let's close partials eighty percent close and let the rest run" (1:15:49). He had named 25 to 29 pips of profit a moment
  earlier. 10:01:06 at 1986.645: closed the last 0.13 by hand, +37.70 USD, to set up the next trade.
- **Outcome:** +242.28 USD, 2.15 R. Held 45 minutes.

## Trade 7: Friday retest sell at 5% risk with an 11-pip stop

- **Video time:** order box 1:18:14; open at 1:18:22; stop moved 1:18:45; closed about 1:18:58.
- **Replay time:** entry Fri 24/03/2023 11:35:59 (= 08:35 GMT, 04:35 New York); exit 11:40:35.
- **Timeframe on screen:** M15 (the M30 was used to see the retest).
- **Direction and prices:** Sell 2.59 lots at 1987.525. Stop 1988.660. TP 1983.544 at entry, then removed.
- **Stop distance:** 1.135 dollars = 11.4 pips. The box first read SL 1988.339 ("-81.0 pips, -294.67 USD"); he then dragged
  it "just a little bit up higher" (1:18:17), which made the tool cut the lot size to keep 5%.
- **Risk:** box "Max. Risk: 5.00% (295.05 USD)". "since we've made gains ... I can risk five percent" (1:17:57 to 1:18:17).
- **Zone (frames 1:17:30, 1:18:22):** one orange horizontal line labelled 1989.56, at the underside of the broken
  consolidation support (and at his trade 6 entry). The old grey bands remain above.
- **Sequence:** after trade 6 price based near 1985.5 and climbed back. The 11:00 M30 candle spiked up through the line to
  about 1992.7 and closed down near 1986.9: "we created resistance with a huge candle" (1:17:16). On M15 that is a green
  candle to about 1991.6 followed by a red one from about 1991.6 to 1986.9.
- **Entry trigger:** mid-candle on the M15, before the previous candle's low had broken. He had said he would wait for a
  wick up and a break of the previous low, then entered early: "let's just take a five percent sale" (1:17:57). Entry is
  about 2 dollars below the retest line.
- **Where the stop sits:** inside the body of the previous red M15 candle, about 0.9 below the retest line. Not above any
  candle high. He calls a normal stop here "way too big" (1:17:37).
- **Management:** when the previous low broke and the panel read "151.0" (11:38:18), stop moved to 1987.374, 0.15 beyond
  entry: "I can bring my stop loss in profit now" (1:18:37). Closed all at 1981.545 at 11:40:35.
- **Outcome:** +5.98 dollars = 59.8 pips, +1548.82 USD, 5.3 R. Held 4 min 36 s. Equity jumped from +18% to +49%.
- **Afterwards:** "normally I would not do five percent mostly I do like maybe like three percent two percent" (1:19:45).

---

## Trades he refused or waited on

1. **Mon 08:00 (0:24:46 to 0:25:28):** price between support and a 1975 resistance. "wait for a candle to close above or
   ... close below the support" (0:25:08). The next close gave trade 1.
2. **Mon 09:30 to 10:06 (0:33:08 to 0:34:53):** looking for a second buy on a retest. A 15-minute candle closed with no upper
   wick: "no trade" (0:33:08). Price then broke the high early in a new candle: "it's in the first five minutes" (0:34:31).
   It ran without him: "we've missed a trade but that's still fine" (0:34:53).
3. **Mon New York session (0:35:16):** skipped after +4.3% on the day.
4. **Tue 08:00 to 09:00 (0:38:21 to 0:39:24):** "we're in the middle of a range so we're not going to do anything" (0:38:42).
   No buy because the M30 had not closed bullish; no sell because price sat on support.
5. **Tue 09:19 (0:40:27 to 0:41:31, frame 0:41:20):** price slipping under the 1979.85 line mid-candle. No sell without a
   close, and "your stop is like almost 30 pips ... stop losses have to be maximum 25 pips" (0:41:09). He accepts having
   missed that leg.
6. **Tue 10:30 (0:44:16 to 0:45:17):** candle closed below 1976 but green. "wait for price to break the previous low and
   then we may look to take a sell" (0:44:57). That became trade 2.
7. **Wed 08:00 to 09:42 (0:56:21 to 0:58:32):** range with small bodies. "this is 20 to 21 pips yeah not interested there's
   no need to force anything" (0:58:10).
8. **Wed after trade 4 (1:03:34 to 1:04:35):** sell only "if we break below the low" of the new support, for "58 pips"; no break.
9. **Wed evening FOMC (1:04:56 to 1:05:16):** not traded.
10. **Fri 08:30 (1:13:03 to 1:13:44):** candle closed back inside the range. "can we take a sell no we closed back in the
    range can we take a buy absolutely no" (1:13:24).
11. **Fri 10:00 to 11:30 (1:16:32 to 1:17:37):** after trade 6, waited an hour and a half for price to come back up and form
    resistance before selling again.

## Rules he states in this video

**The "Strategy breakdown" chapter (0:10:42 to 0:13:47).** It is not a rule list. The screen shows only the webcam over an
empty MT5 window (scan frame 0:12:50); nothing is written or drawn. What he says there:
- The session's aim: "how I hold positions what's the thought process ... managing the risk" (0:12:23 to 0:12:44), plus
  whether trades can be held longer, taking risk off, adding positions, losing less when a trade goes against him (0:12:44 to 0:13:04).
- "I don't focus on any highs I don't focus on any lows I just focus on simple price action" (0:13:25), answering a
  question about the previous day's high and low.
- "my RR is uh more than one to one" (0:13:25).
- One full week will be simulated and "every trade opportunity" explained (0:13:04).

**Set-up and timeframes**
- Do not replay data older than "eight months nine months because market dynamics are all the shifting" (0:14:48).
- "I'm only going to be looking at the 15 minute 30 minute one hour and four hour" (0:16:32); in practice he opens the
  daily first every morning.
- No indicators or trend lines (1:09:49, 1:10:32).

**When there is volume (0:17:33 to 0:18:54, spoken, nothing on screen)**
- Asian open; pre-London; London open; pre-New York; New York open; NYSE open; London close.
- "London open you can have volume on gold if pre London had no volume" (0:18:14).
- Not every window fires; if one is quiet "you're gonna skip on to the next time" (0:18:34).
- His working day: "from pre-London London open all the way into New York open" (0:20:19). "you guys see why I take my
  trades at pre London because of volume" (0:29:42).
- A consolidation breaks "when there's volume in the market ... when there's news in the market" (0:49:47 to 0:50:08).

**Reading order each morning**
- "step number one is to identify the trend and the trend on the Daily is bullish" (0:21:42). Then H4, H1, M30.
- Bullish higher timeframe: look for support forming on the lower one (0:22:03). Fading bodies on H4: look for resistance
  forming on the lower one (0:36:58 to 0:37:19).
- "whenever you see the bodies of the candles get smaller ... the volume moving up starts to die" (0:36:58).
- Always ask how much room there is: he measures the "range" to the next level in pips before every decision.

**Which timeframe confirms**
- "supports on the 30 minute time frame are going to be much stronger than the supports on the 15 minute" (0:24:26).
- "we're only going to focus on the 30 minute because 30 minutes has strong confirmations" (0:31:03).
- "15 minutes are weak confirmations we want the 30 minute confirmation" (0:43:34).
- The M15 is used to find a smaller stop (0:46:00, 1:00:42, 1:07:02) and, on trade 5, as an early warning to cut size.

**Entry**
- Candle-close entry: wait for the M30 to close beyond the level in the trade's direction (0:25:08, 0:39:03).
- No sell after a bullish close and no buy after a bearish close, even beyond the level (0:44:37).
- "Impulse entry": after such a close, enter when price breaks the previous candle's low, without waiting for the close
  (0:44:57, 0:47:04, 0:50:48, 1:14:47).
- "you either want to take a sell at the top or a buy at the bottom" of a range, never the middle (0:38:21).
- A break that closes back inside the range is a fake-out and can be traded the other way (0:59:38, 1:00:22).
- Missed move: "wait for price to retrace create some support and then continue pushing up" (0:30:43).
- Do not act on a move "in the first five minutes" of a new candle (0:34:31).

**Stop**
- Buy: "your stop losses are below the previous 30 minute candle" (0:26:11).
- Impulse entry: the stop goes beyond "the current candle", not the previous one (0:46:00).
- "stop losses have to be maximum 25 pips" (0:41:09). He nevertheless took 33-pip stops twice (trades 2 and 5), each time
  cutting the risk percentage instead.

**Size**
- Base risk 1.5% (0:25:48, 1:00:42). Bigger stop: lower the risk (1% on trade 2, 0.5% on trade 5).
- Second trade on a day with a position already running: "when you're winning decrease your risk" (0:51:09), 0.5% on trade 3.
- Raise risk only late in a winning week: "the best way to go higher risk is always when you have made gains" (1:19:22).

**Management**
- "if you put your stops at break even without securing some profits you're going to have a very bad time" (0:28:38).
- Standard move: at the next level close about 80%, move the stop to entry, let the rest run (0:29:02, 0:47:24, 1:02:06, 1:15:49).
- Take-profit: placed in the box, then usually removed, "because what if price continues pushing down" (0:46:43, 1:15:07).
- If the next lower-timeframe candle closes against the trade, cut half at once (1:08:02); if the confirming candle is
  small, cut again (1:08:45).
- After a good day, stop: do not trade New York as well (0:35:16).

**News**
- "if you're a good trader you don't trade news" (1:04:56). He does check the calendar for USD items before the New York
  trade (0:50:08) and says Canadian data does not move gold.

## What the frames show that the transcript alone would not

- Every entry, stop, lot size, exit price and clock time: the transcript has none of the prices for trades 3, 6 and 7 and
  no times at all. The History tab gives them all.
- The simulator prints pips ten times larger than he speaks them, and why (pip size setting 0.01).
- The chart clock is New York close time, so his "8 AM pre-London" is 01:00 New York, and "London open" is 03:00 New York.
- Entries are of two kinds, and the clock separates them cleanly: trades 1, 4 and 5 were entered 0 to 13 seconds after an
  M30 candle closed; trades 2, 3, 6 and 7 were entered in the middle of a candle on a break.
- On break entries "the low" he waits for is the previous candle's low or the body floor at his band. Lower wick extremes
  further left were still untouched at entry on trades 2, 3 and 6.
- His stops are not at a fixed place relative to "the previous candle". Measured: trade 1 about 0.7 under the trigger
  candle's body; trade 2 just above the broken support line; trade 4 just under the support line; trade 6 about 0.4 above
  the current candle's high; trade 7 inside the previous candle's body. Stops ranged 11 to 34 pips.
- Zones: grey rectangles 0.3 to 0.5 dollars thick on body tops or body bottoms with wicks poking through, the same habit as
  in the other videos. New here: he usually lays an orange horizontal line with a price label through the band (1969.37,
  1984.02, 1976.15, 1944.46, 1938.09, 1935.52, 1989.56); he wipes and redraws zones every morning; there are never more than
  four on the chart; they are drawn from candles a few hours to about 15 hours back.
- Partial closes are 80% each time by lot count (0.37/0.46, 0.12/0.15, 0.35/0.44, 0.53/0.66), taken at 1.3 to 2.6 times the
  stop, each at a level he had drawn or named.
- The Wednesday "fake-out" breakdown candle is the 10:00 candle, the UK CPI release on his own calendar. He never links them.
- Tuesday's big fall that paid trades 2 and 3 is one candle, 16:30 chart time, the NYSE open.
- Trade 7's sizing: 2.59 lots on a 5,900 dollar account behind an 11-pip stop, held under five minutes, producing most of
  the week's result. The stop was first even tighter (8 pips) before he widened it.
- Trade 5's spoken stop (29 pips) and placed stop (33 pips) differ.
- Every order was placed with the replay paused, and the replay is fast-forwarded bar by bar between decisions.

## Could not be read / open questions

- Exact highs and lows of most trigger candles: the status bar shows OHLC only where the mouse hovered. Candle levels above
  marked "about" are read from the price axis and are good to roughly 0.1 to 0.2 dollars.
- What the "20 to 21 pips" at 0:58:10 measured (room to resistance or a stop): UNKNOWN, no ruler on screen.
- Replay times of the later stop moves on trades 2 and 3: the clock was hidden behind the modify box. Between 15:05 and 17:45.
- Replay time of trade 5's move to break-even: between 08:30:09 and 09:15:00.
- Why he calls 17:45 chart time "London close": UNKNOWN. The Sessions panel ends London at 20:00.
- Daily and H4 on Wednesday and Friday, and H1 on Thursday, were taken from his words only; I did not study those frames.
- The orange line labels 1979.85 and 1976.15 are small on screen; last digit uncertain.
- Whether the replay tool's fills (fixed 0.15 spread, instant fills while paused, Dukascopy ticks) match a live account: not testable here.

## Is this the "Video 12" of the older transcript-only notes? No.

Checked against each thing those notes describe:
- "Trade refused about 21:40 because the stop would be about 27 pips": at 21:40 here he is reading the daily trend before
  any trade. The only stop-size refusal is at 0:41:09 ("almost 30 pips", maximum 25). "27 pips" is never said.
- "Losing buy from support about 33 minutes": at 33 minutes here there is no position; he watches a retest he does not take.
  No trade in this video loses its stop.
- "Resistance-retest sell about 36 to 46 minutes, 50% then 90% of the rest, 2 lots by accident": 36 to 45 minutes here is
  Tuesday's analysis and waiting. The sell at 0:46:44 is a broken-support retest, 0.15 lots at 1%, closed 80% once. The only
  large-lot trade is trade 7 at 1:18 (2.59 lots, deliberate, closed in one piece). No 50% then 90% sequence exists.
- "ADP stop-out about 1:15": at 1:15 here he takes the winning 2% sell. The replay week (20 to 24 March 2023) has no ADP.
- "NFP pending-order tactic about 1:19": at 1:19 here he talks about when to raise risk. The week has no NFP, the Pending
  tab is never used, and the History tab lists only market orders.
- The words ADP, NFP, non-farm, pending, "2 lots" and "90 percent" do not occur anywhere in this transcript.

A lead, not checked by me: in the transcripts folder "ADP" occurs only in L1hqmAu1i2I and vt14tf4KYBU.
