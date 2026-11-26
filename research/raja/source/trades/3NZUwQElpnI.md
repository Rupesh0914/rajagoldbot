# 3NZUwQElpnI - "Gold Trading Simulation" (streamed 23 Jul 2022, 1:29:58)

- **Platform:** Soft4FX simulator on MetaTrader 4 (window title "ICMarkets-Live05", symbol `!STD_XAUUSD`, offline charts). Black-and-white candles: white = up, black = down.
- **Instrument:** gold (XAUUSD) only.
- **Simulated account:** 10,000 USD start, leverage 1:100, fixed spread shown as "Spread: 15.0 pips" (ask minus bid = 0.150 dollars on every frame).
- **Replay dates covered:** Mon 11 Apr 2022 08:00 to Thu 14 Apr 2022 15:54 (four trading days, each started at 08:00 on the simulator clock).
- **Trades:** 7 positions, all buys (one of them with an add-on order). 5 winners, 2 full losers. Equity 10,000.00 -> 11,070.95 (+10.71%).
- **Frames:** 38 kept in `frames\3NZUwQElpnI` (named by video time). Every number below was read from a frame unless it is marked "transcript" or "by eye".

## Pip size in this video

His spoken pip is **0.10 dollars**. The simulator's own "pip" is 0.01 dollars. Pairs where both are visible:

| Where | Dollars on screen | Simulator figure | What he says |
|---|---|---|---|
| Trade 1 stop (0:22:25) | 1942.472 - 1939.544 = 2.928 | "-292.8 pips" | "28 29 Pips" (0:21:53) |
| Trade 1 exit (0:31:40) | 1957.812 - 1942.472 = 15.340 | "1534.0" | "around 150 Pips" (0:31:25) |
| Trade 2 at partial close (0:40:50) | 1962.568 - 1959.082 = 3.486 | "348.6" | "32 33 34 Pips up" (0:40:42) |
| Trade 3 stop (0:52:55) | 1953.362 - 1950.920 = 2.442 | (row shows prices) | "around 24 Pips" (0:52:39) |
| Trade 5 exit (1:09:35) | 1978.233 - 1973.088 = 5.145 | "514.5" | "50 Pips" (1:09:25) |
| Trade 6 stop (1:20:55) | 1973.030 - 1971.398 = 1.632 | box "-117.6" before he moved the line | "15 16 Pips" (1:20:25) |

One mismatch: for trade 7 he says "24 23 Pips" (1:21:46) but the filled order's stop is 3.288 dollars away (32.9 of his pips); the order box at one instant showed 2.746 dollars. Neither equals 23-24.

One nuance: when he reads the simulator's spread setting aloud he uses the simulator's unit ("fixed spreads around 15 Pips", 0:09:25) - that is 0.15 dollars, i.e. 1.5 of his own pips.

## Clock and sessions

The panel at top right and the trade panel show broker server time, which is **New York + 7 hours (UTC+3 in April 2022)**. How I know: he says so ("this time right here 100 hours this means 6 p.m. Eastern", 0:10:47); he reads 12:06-12:19 on the panel as "5:15 a.m. eastern" (0:31:52); the simulator's Sessions bar puts the London block from hour 10 and the New York block from hour 15; and the US CPI release on Tue 12 Apr falls at 15:30 on this clock (08:30 New York).

His session labels on this clock: pre-London starts 08:00 (01:00 New York); London open 10:00; pre-New York from about 13:00-13:15 ("6 6:15 a.m.", 1:08:41); New York open 15:00 ("8 a.m. eastern", 1:27:02).

## How zones look in this video

Same style as the other videos: thin light-grey horizontal rectangles laid along the edges of candle bodies (where candles closed or opened), with wicks sticking through. Differences and specifics here:

- Thickness by timeframe (by eye from the axis): 30-minute and 1-hour bands are about 0.25 to 0.45 dollars thick; the 4-hour band about 0.5 to 1.2; the daily bands about 1.8 to 2.7.
- He often lays a thin horizontal line through a band, and the line's exact price is printed on the axis (for example 1941.038, 1940.794, 1947.779, 1959.265, 1951.671, 1971.962, 1963.838, 1972.205). These lines give the zone's intended price to three decimals.
- Bands are drawn from recent candles: on the 30-minute chart from roughly the last 30 candles (one trading day), on the 1-hour from the last one to two days, on the daily from the last 6 to 10 candles.
- He redraws constantly: at the start of day 2 he deletes every zone ("let's remove all these zones", 0:43:04) and draws just two on the 1-hour; on day 3 he moves a resistance band up when a new body top forms ("price made a new resistance so we're going to move this resistance up", 1:04:10).
- Targets are the next band on a higher timeframe (4-hour band 1957.45-1957.98 for trade 1) or an old wick ("this wck 1978", 1:06:34).

---

## Trade 1 - Monday pre-London buy, held to pre-New York (winner)

- **Video time:** order box 0:22:15-0:22:25, filled about 0:22:30. Main exit 0:31:40. Final exit 0:32:16.
- **Replay time:** entry Mon 11.04.2022 08:31:03. 90% closed Mon 11:50:04. Remainder closed Mon 12:19:56. Server time (New York + 7 h).
- **Chart at entry:** XAUUSD, M30.
- **Direction and prices:** BUY. Entry 1942.472 (ask; bid 1942.322). Stop 1939.544. No target: the box's default TP of 1942.502 was removed, the order row later shows an empty Take Profit cell.
- **Stop distance:** 2.928 dollars; box says "-292.8 pips"; he says "around 28 29 Pips".
- **Risk and size:** "Max. Risk 1.00% (100.00 USD)", loss at stop -99.55 USD, 0.34 lots.
- **What was drawn (frames 0:15:25, 0:17:35, 0:21:45):**
  - M30: upper band about 1947.90-1948.16 along the body tops of the 8 Apr 17:00 and 8 Apr 23:00-23:30 candles, wicks above it to about 1949.8. Lower band about 1940.93-1941.19 with a line at 1941.038, along the body bottoms of the 8 Apr 18:30-21:00 candles and the Monday 04:30-06:30 lows, wicks below it to about 1939.2. Both drawn from candles between 8 Apr 17:00 and 11 Apr 08:00 (about 30 candles).
  - H1: bands about 1947.53-1947.95 and 1940.67-1941.05 (line 1940.794), plus a third about 1933.80-1934.27 on top of the 8 Apr midday consolidation - his "1933" downside marker.
  - 4H: one band about 1935.0-1936.15 at the top of the 1-7 Apr range. Later a 4H band 1957.45-1957.98 at the body tops of the late-March 4H candles (the target).
  - Daily: band about 1936.5-1938.3 (top of the bodies of the previous week's candles; the level the last daily candle closed above) and band about 1916.9-1919.6 (bottom of those bodies).
- **Higher timeframes (frames 0:12:25, 0:13:30):** Daily - Friday's candle is white and closed above the 1937 band; Monday's candle so far is black (open 1946.138, high 1949.838, low 1940.168). He reads it as broken resistance, bias buys. 4H - two black candles pulling back from the 1949.8 high; he wants the 4H candle to wick down and turn up, with a support forming on 1H or 30M.
- **Entry trigger:** the M30 08:00 candle closed at 1940.422, below the 1941.04 band: a black candle, open about 1942.14, no upper wick, tiny lower wick. The 08:30 candle opened 1940.422, dipped to 1939.882 in its first seconds, then ran up through the 08:00 candle's high (candle reads O 1940.422 H 1942.352 L 1939.882). He bought at 08:31:03 - 63 seconds into the candle, candle still open. He calls the close below support a fake-out.
- **Stop placement:** 1939.544 is 0.34 below the entry candle's low (1939.882).
- **Stated reason:** "this is where I think an impul entry would work stop is going to be around 28 29 Pips" (0:21:53-0:22:15). Before that: "whenever a candle has no top Wick and it moves down this means there was so much bearish pressure" (0:21:32).
- **Management:**
  - No target: "there's going to be no takeprofit ... we're going to let the trade run till pre- New York" (0:22:15-0:22:36).
  - Conditional rule, not triggered: if the London-open 1H candle breaks the previous 1H candle's low he would close half ("we're going to be closing 50% of this trade", 0:28:37).
  - Stop moved 1939.544 -> 1941.011 at about Mon 10:40 (frame 0:30:12 shows it at 10:40:19), after the 10:00 1H candle broke the 09:00 candle's high. The new stop is about 0.3 under the lows of the 09:00 and 10:00 1H candles (about 1941.3 by eye) and still 1.46 below entry - not break-even. "we can move our stop loss down to the lows of the 1 hour candles" (0:29:18).
  - Talked about adding above 1948 (0:27:56) and again at 0:30:42; did not add.
  - 90% closed (0.31 of 0.34 lots) at Mon 11:50:04, bid 1957.812, +15.340 dollars, when price touched the 4H band 1957.45-1957.98. "we've actually tapped exactly in that area ... around 150 Pips 5% gain um probably going to close 90%" (0:31:25).
  - Remaining 0.03 lots: stop set to break-even 1942.472 (frame 0:32:16), then closed by hand at Mon 12:19:56, bid 1957.392 (+14.920).
- **Outcome:** equity 10,000.00 -> 10,521.11 (+521.11, +5.21%), about +5.2 times the amount risked. 3 h 19 min to the main exit, 3 h 49 min in total.
- **Afterwards:** nothing he would change; he presents it as the model trade - enter pre-London, no target, close at pre-New York.

## Trade 2 - Monday pre-New York buy on a 1-hour high break (winner)

- **Video time:** entry 0:38:50-0:39:10 (box in frame 0:39:05). 90% closed about 0:40:45. Rest closed about 0:41:25.
- **Replay time:** entry Mon 11.04.2022 14:33:58. 90% closed Mon 15:08:32. Remainder was still open at 15:20:23 (seen while scanning) and gone by 15:30:18 (frame 0:41:30) - exact second UNREADABLE.
- **Chart at entry:** XAUUSD, H1.
- **Direction and prices:** BUY. Entry 1959.082 (ask; bid 1958.932). Stop 1956.042. The box shows a TP line at 1964.815 ("573.3 pips") but the order row has no Take Profit.
- **Stop distance:** 3.040 dollars; box "-304.0 pips"; he gives no pip number, only "kind of a big stop over here" (0:38:52).
- **Risk and size:** "Max. Risk 1.00% (105.21 USD)", -103.36 USD at stop, 0.34 lots.
- **What was drawn (frames 0:38:50, 0:40:50):** H1 resistance band about 1958.1-1958.5 (line 1958.315) along the body tops of the 12:00 and 13:00 1H candles. Earlier (0:35:55, seen while scanning) an M30 support band about 1954.0 at the body bottoms of the 11:00-13:30 candles. The old lines 1947.779 and 1940.794 are still on the chart.
- **Higher timeframes:** 4H 12:00 candle pushing up after touching the 1957.5-1958 band; he says "the 4-Hour candle is also pushing up" (0:38:32).
- **Entry trigger:** the 13:00 1H candle is black with a small body (about 1958.1 down to 1956.4) and a long lower wick to about 1952.8 - his "rejection candle". The 14:00 1H candle (O 1956.338, L 1955.552) climbed back through the 13:00 candle's high and the band; he bought at 14:33:58, 34 minutes into the candle, candle open (H 1958.982 at that instant). He had refused the same idea 30 minutes earlier because the 14:00 M30 candle closed weak.
- **Stop placement:** 1956.042 is 0.30 under the 14:00 candle's open and about 0.4 under the 13:00 body, but 0.49 ABOVE the 14:00 candle's low (1955.552) and far above the 13:00 wick. He says "stops are going to be below this candle" (0:38:52).
- **Stated reason:** "we're breaking above the high right we're in pre- New York we're close to New York open" (0:38:12).
- **Management:**
  - Thought about adding when the New York-open candle broke the previous high, then: "we're not going to add anything over here we're just going to manage this trade" (0:40:20).
  - 90% closed (0.31 lots) at Mon 15:08:32, bid 1962.568, +3.486 dollars. "we're about 32 33 34 Pips up over here going to close 90%" (0:40:42).
  - Remaining 0.03 lots: stop left at the original 1956.042 (not moved to break-even). Closed by hand before 15:30: "CPI is coming right up so we're going to close the trade" (0:41:24). The equity change implies a close near 1962.9 (computed, not read).
- **Outcome:** equity 10,521.11 -> 10,640.67 (+119.56), about +1.16 times the risk. 35 minutes to the main exit, under 57 minutes in total.
- **Afterwards:** the 15:30 M30 candle ran to 1969.558 (seen while scanning). "imagine would have let let this trade run this would have been insane another 100 pip move" (0:41:44).
- **News note:** he calls the 15:30 Monday candle the "CPI candle". The simulator's own Economic News window (frame 0:32:25, clock Mon 13:00) lists no US CPI on 11 Apr; the only US item that day is "FOMC Member Bowman Speaks" at 16:30 (low impact), and "German Final CPI m/m" is listed for 12 Apr 09:00. US CPI was on Tuesday (see trade 4).

## Trade 3 - Tuesday buy after a 1-hour candle closed bullish on support (small winner)

- **Video time:** entry 0:52:25-0:52:50. 90% closed 0:53:15. Remainder stopped out about 0:54:45.
- **Replay time:** entry Tue 12.04.2022 13:00:03. 90% closed Tue 13:25:45. Remainder stopped at break-even some time before Tue 14:43:09 (exact time UNREADABLE).
- **Chart at entry:** XAUUSD, H1.
- **Direction and prices:** BUY. Entry 1953.362 (ask; bid 1953.212). Stop 1950.920. No target.
- **Stop distance:** 2.442 dollars; he says "around 24 Pips".
- **Risk and size:** "Max. Risk 1.00% (106.41 USD)", 0.43 lots.
- **What was drawn (frames 0:44:40, 0:50:25, 0:52:10):** all earlier zones deleted. On H1 a resistance band about 1959.1-1959.5 (line 1959.265) along the body tops of the 12 Apr 06:00-10:00 candles, wicks above to about 1960.2; a support band about 1951.5-1951.9 (line 1951.671) along the body bottoms of the 11 Apr 23:00 to 12 Apr 02:00 candles; a wider band about 1940.7-1941.5 at the bottom of Monday evening's drop. On M30 also a band about 1950.45 and a line at 1949.586 under an old wick.
- **Higher timeframes:** Daily - Monday's candle ended with a long upper wick back under resistance, Tuesday's is coming up to it again; he calls it "a 50/50 chance" (0:42:44). 4H - bias up "as long as price respects this price 1950" (0:43:24).
- **Entry trigger:** no trade through the whole London morning. The 12:00 1H candle reads O 1951.472, H 1953.782, L 1949.518, last 1953.188 with 22 seconds left (frame 0:52:10): a white candle with a long lower wick through the support band. The 12:30 M30 candle also closed white. He bought 3 seconds after the 1H candle closed.
- **Stop placement:** "stops are going to be um below the 30 minute candle around 24 Pips" (0:52:39). The stop (1950.920) is above the 1H candle's low (1949.518). The 12:30 M30 candle's low is UNREADABLE (no M30 frame at that moment).
- **Stated reason:** "I kind of want to wait for the 1our candle to close" (0:51:36); then "we waited for support to form support formed took a buy that's it" (0:53:23).
- **Management:**
  - 90% closed (0.39 lots) at Tue 13:25:45, bid 1955.678, +2.316 dollars (frame 0:53:15 shows the partial-close dialog mid-edit; the order left afterwards is 0.04 lots). "this candle has no bottom Wick so going to close 90% since we're in the New York session" (0:53:02).
  - Why so early: "I don't let trades run for a longer time in New York session because they're more prone to retrace" (0:53:43).
  - Remaining 0.04 lots: stop to break-even 1953.362; it was hit. Equity sits at 10,730.99 with no open orders at 14:43:09 (frame 0:54:50).
- **Outcome:** equity 10,640.67 -> 10,730.99 (+90.32), about +0.86 times the risk. 26 minutes to the main exit.
- **Afterwards:** none.

## Trade 4 - Tuesday buy on a 4-hour high break, 17 minutes before CPI (loser, stop widened)

- **Video time:** entry 0:56:00-0:56:25. Stopped out about 0:57:05.
- **Replay time:** entry Tue 12.04.2022 15:13:27. Stop moved while losing, between 15:24:30 and 15:27:05. Stopped out between 15:27:05 and 15:30:00 (the 15:30 M30 candle opens at 1955.352, already under the stop).
- **Chart at entry:** he decides on H4, places the order on H1.
- **Direction and prices:** BUY. Entry 1959.998 (ask; bid 1959.848). Initial stop 1956.712. Target kept this time: Take Profit 1963.769 on the order row (box 1963.984).
- **Stop distance:** 3.286 dollars at entry (box "-328.6 pips", -105.15 USD); no pip number spoken, "it's going to be a pretty big stop" (0:56:08). Then widened to 4.337 dollars (stop 1955.661).
- **Risk and size:** "Max. Risk 1.00% (107.31 USD)", 0.32 lots. Actual loss after widening: 138.78 USD = 1.3%.
- **What was drawn:** the 1959.265 resistance line and band, the 1951.6 support band.
- **Higher timeframes / trigger:** the 12:00 4H candle (O 1951.472, H 1960.108 at entry) pushed above the previous 4H candle's high at 15:13, in the New York-open hour, 3 h 13 min into the 4H candle. No lower-timeframe confirmation; he refuses to look at the 15-minute.
- **Stated reason:** "looking at price to continue pushing up till 1963 only based on the 4H hour" (0:56:08). Stop logic, a stop inside the range: "if we're breaking up on the 4 Hour there's no reason for price to continue back down" (0:56:29).
- **Management:** with the trade at -187 then -273 simulator pips he dragged the stop DOWN from 1956.712 to 1955.661: "let's place it in a much better um much better area below this candle" (0:56:53). It was hit minutes later, just before the 15:30 release. He had seen the event before entering ("we got CPI over here another one", 0:55:25).
- **Outcome:** equity 10,730.99 -> 10,592.21 (-138.78). Held at most 17 minutes. In the first 50 seconds after 15:30 the M30 candle ran from 1955.352 to 1961.408 (frame 0:57:12).
- **Afterwards:** "that was a unnecessary trade to take by the way that was um overtrading shouldn't have done that" (0:57:00).

## Trade 5 - Wednesday London buy on a 1-hour high break, 1.5% risk (winner)

- **Video time:** entry 1:05:33-1:06:20. Exit 1:09:35-1:09:55.
- **Replay time:** entry Wed 13.04.2022 11:15:36. Stop trailed by 12:04:24. Closed in full Wed 12:46:42.
- **Chart at entry:** XAUUSD, H1.
- **Direction and prices:** BUY. Entry 1973.088 (ask; bid 1972.938). Stop 1969.990. A TP line sat at 1979.816 for a moment and was removed (row shows none).
- **Stop distance:** 3.098 dollars; no pip number spoken.
- **Risk and size:** risk field 1.50%, 0.51 lots (0.51 x 3.098 x 100 = 158 USD).
- **What was drawn (frames 0:59:35, 1:04:20, 1:05:40):** H1 resistance band about 1971.8-1972.2 (line 1971.962) along the body tops of the 13 Apr 05:00-09:00 candles; a middle band about 1967.7-1968.1 at the body bottoms of the 06:00-08:00 candles; a support band about 1963.6-1964.0 (line 1963.838) at the body bottoms of the 02:00-03:00 candles. He moved the resistance band up once during the wait.
- **Higher timeframes:** Daily has broken up. 4H "is basically creating a support" (0:58:16), with room to an old wick.
- **Entry trigger:** the 09:00 1H candle is black (about 1971.9 to 1968.6). The 10:00 London-open candle reads O 1968.642, L 1965.593 with a long lower wick ("a lot of exhaustion Wicks at the bottom", 1:04:31) and closed white near 1971.1. The 11:00 candle (O 1971.083, L 1969.888) broke above that candle's high and the 1972 band; he bought at 11:15:36, 15.6 minutes into the candle, candle open. Before that he had refused to buy in anticipation.
- **Stop placement:** 1969.990 - level with the 11:00 candle's low (1969.888); the stop is 0.10 ABOVE that low. He says "stop is going to be below this area below this Wick" (1:06:14).
- **Stated reason:** "we're breaking the high right here so now we're going to increase our risk to let's say 1.5%" (1:05:33). And "only focusing on the 1H hour candles no 30 minute no 15 minute" (1:05:12).
- **Management:**
  - TP removed "because we're going to let it run till pre New York" (1:06:14).
  - Stop moved 1969.990 -> 1972.529 by Wed 12:04:24, after the 11:30 M30 candle closed; it sits under that candle's low (about 1973.0 by eye) and 0.56 under entry. "move the stops below this area because you know got to Trail the stop loss" (1:08:21).
  - Closed in full at Wed 12:46:42, bid 1978.233, +5.145 dollars, at Tuesday's high-wick area (about 1978-1979). "this trade is in 50 pip profits ... close everything probably yeah I say so because we're at a rejection area" (1:09:25-1:09:46).
- **Outcome:** equity 10,592.21 -> 10,854.61 (+262.40), about +1.66 times the risk. Held 1 h 31 min. He closed about 15-30 minutes before his own stated pre-New York time.
- **Afterwards:** "sometimes it continues pushing you know at that time you're like oh well I didn't know that" (1:13:27). On partials: "I don't take partials I experimented it with low risk but now just let them run" (1:09:05) - yet trades 1, 2, 3 and 7 in this same video use partial closes.

## Trade 6 - Thursday pre-London buy on "fresh support" (loser)

- **Video time:** entry 1:20:25-1:20:55. Stopped out by 1:21:10.
- **Replay time:** entry Thu 14.04.2022 09:34:02. Stopped out between 09:37:44 and 09:57:06 (exact time UNREADABLE).
- **Chart at entry:** XAUUSD, M30.
- **Direction and prices:** BUY. Entry 1973.030 (ask; bid 1972.880). Stop 1971.398. No target on the row.
- **Stop distance:** 1.632 dollars; he says "around 15 16 Pips".
- **Risk and size:** "Max. Risk 1.00% (108.55 USD)", 0.66 lots.
- **What was drawn (frames 1:18:10, 1:20:55):** M30 thin band about 1972.1-1972.3 (line 1972.205) at the body bottoms of the 08:30-09:00 candles - the "fresh support"; an M30 resistance band about 1979.6-1979.9 at the 03:30 body top; older bands about 1966.2 and 1963.7. On H1 a resistance band about 1981.0 and a thicker support band about 1972.75-1973.3.
- **Higher timeframes:** Daily strongly up. 4H has made a resistance. H1: "this is just ugly price action not every day is going to be a trade" (1:17:36).
- **Entry trigger:** not a high break. The 09:00 M30 candle left a long lower wick (to about 1971.2 by eye) and closed back above the band. He bought 4 minutes into the 09:30 M30 candle while that candle was black and falling (O 1973.508, last 1972.880). An anticipation buy.
- **Stop placement:** "stop is going to be just below this Weck" (1:20:25). The stop is 0.8 under the band; whether it clears the wick tip is UNREADABLE (they are within about 0.2 of each other).
- **Stated reason:** "30 minute candle creating fresh support we are in pre- London time" (1:20:05); "me risking 1% is no big deal" (1:20:45).
- **Management:** none. Price fell to 1970.588 inside the same M30 candle.
- **Outcome:** equity 10,854.61 -> 10,746.90 (-107.71), a full 1% loss. Held at most 23 minutes.
- **Afterwards:** "we thought it was easy but it's not that easy at all" (1:21:06).

## Trade 7 - Thursday London-open "second chance" buy, 2% plus a 0.5% add-on (winner)

- **Video time:** entry 1:21:26-1:22:10. Add-on 1:22:27-1:22:45. Main exit 1:23:40-1:23:55.
- **Replay time:** entry Thu 14.04.2022 10:04:51. Add-on Thu 10:09:37. Main exit Thu 10:39:01. Remainder to break-even by 10:52:47; stopped there some time between 11:41:19 and 15:11:46 (UNREADABLE).
- **Chart at entry:** box on M30, then H1.
- **Direction and prices:** BUY 0.65 lots at 1973.958, stop 1970.670. A TP line at about 1976.825 was removed ("we're going to remove these TPS", 1:22:27). ADD-ON: BUY 0.30 lots at 1972.451, stop 1970.687.
- **Stop distance:** main 3.288 dollars; add-on 1.764 dollars. He says "24 23 Pips" for the main one - this does not match the filled order (see pip section).
- **Risk and size:** main "Max. Risk 2.00% (214.94 USD)"; add-on risk field 0.50%. Together about 267 USD, 2.5% of equity.
- **What was drawn:** the 1972.2 band, re-set as a line at 1972.081 on H1 after the 09:00 candle closed ("we can adjust the zone now", 1:22:07).
- **Entry trigger:** the 09:00 1H candle closed white with a long lower wick down to 1970.588 (the wick that stopped trade 6). At London open the 10:00 M30 candle (O 1973.388, H 1974.287 at entry) broke above the 09:30 M30 candle's high (1973.508); he bought at 10:04:51, under 5 minutes into the candle.
- **Stop placement:** 1970.670 is 0.08 ABOVE the low of that wick (1970.588).
- **Stated reason:** "since we're doing a simulation we will give our buy a second chance" (1:21:26); "we want London open to continue pushing price up" (1:21:46).
- **Management:**
  - Add-on bought when the first order was 107.71 USD down (bid 1972.301), on the pull-back to the band: "as price retraces we're going to add to this position as well" (1:22:07). His reason: "I'm going to add maybe 0.5 over here because if we do lose this is not going to be a good outcome" (1:22:27).
  - At Thu 10:39:01, bid 1977.358 ("we're coming up towards 1977", 1:23:28): the 0.65 order was closed in full (+3.400 dollars) and 0.21 of the 0.30 add-on was closed (+4.907 dollars). He says "close 50% maybe or close let's say 70" (1:23:28-1:23:49) - the 70% applied only to the add-on. 0.09 lots left, about 9.5% of the total position.
  - Remaining 0.09 lots: stop to break-even 1972.451 (frame 1:24:10). Hit later; equity is flat at 11,070.95 with no orders by 15:11:46.
- **Outcome:** equity 10,746.90 -> 11,070.95 (+324.05), about +1.2 times the combined risk. 34 minutes to the main exit.
- **Afterwards:** none; he calls it "our last trade".

---

## Trades he refused or waited on

1. **Mon 08:00-08:30 (0:14:15-0:17:23).** No buy inside the 30-minute consolidation; waiting for a support to form. "it's very very tough ... lot of rejections right here" (0:14:15).
2. **Mon 08:30:00-08:30:04 (0:17:43-0:18:23).** The new M30 candle broke the previous low in 4 seconds; no sell. "wait for price to create a top Wick and once it breaks its low again then we can take a sell" (0:18:03). One minute later he bought (trade 1).
3. **Mon about 12:20-13:00 (0:33:19-0:35:05).** No sell after the rejection at 1957-1958 because the trend is up. "a sell is not valid if price is in an uptrend and we're creating a resistance to pull back" (0:34:24).
4. **Mon 14:00 (0:35:47-0:37:51).** No buy at the M30 support: "is this enough range to take a buy it's like a 16 pip range stop is like way too big" (0:35:47). Then the M30 candle closed small: "a weak bullish candle means no buys there's not enough volume" (0:37:51).
5. **Tue 08:00-12:59 (0:44:51-0:51:14).** No London trade. A high was broken in the first 30 seconds of a new 1H candle: "it's too soon we're breaking above the high now in the first 30 seconds" (0:47:18). Sells only under an old wick: "we need it to break below this Wick to the left hand side" (0:50:31). "looks like this London session isn't giving us that opportunity no clear Direction" (0:47:38).
6. **Wed 08:00-11:15 (0:59:18-1:05:12).** A fast move he let go ("too much volume over here got to wait", 1:00:00). No anticipation buy: "the safest buy is going to be when this candle breaks above the high and then continues to push up" (1:01:02). No sell: "even if we break below this Wick the range is like 20 Pips it's not enough" (1:02:46), against a stop he puts at 30 pips.
7. **Wed 15:16:01 (1:14:09-1:15:12).** Price 1980.298 breaking above a band at 1979.354 (frame 1:14:40); risk field set to 0.5; refused. "this not going to be a good buy because we're basically buying the top of the 4H hour" (1:14:51).
8. **Thu 08:00-09:00 (1:17:56-1:18:17).** A buy inside a 40-pip range refused: "the problem is this one hour candle close with no wick on the top" (1:17:56).
9. **Thu 09:00:19 (1:19:00-1:19:42).** The 1H candle closed under support and the next one broke the low at once; no sell. "the new 1 hour candle is breaking the low in the first 19 seconds this is not a great idea to take a sell" (1:19:00).
10. **Thu 13:00-15:54 (1:24:53-1:28:47).** No New York trade. "the best way to trade the 4 Hour is probably going to be break above 1980 to go up" (1:26:39). "sometimes you have to accept that some days you will not get good trades" (1:28:47).

## News in this video

No trade was taken as a news trade. He says "we're going to trade the CPI" (0:32:38) but what he does is:
- Monday: closes trade 2 before a 15:30 release he believes is CPI (the simulator calendar shows none that day) and watches the candle.
- Tuesday (real US CPI, 15:30): he is in trade 4, opened 17 minutes earlier on a 4-hour break; it is stopped out in the last minutes before the release.
- Thursday: he notes "retail sales data" (1:24:11) after closing trade 7 and takes nothing.
ADP and NFP do not appear anywhere in the video.

## Rules he states

- **Clock:** "whenever you see 800 hours this is 2 hours before London open" (0:11:08). Pre-London is where each day starts.
- **Confirmation timeframes:** 30-minute and 1-hour. "15 minute is not a strong enough confirmation time frame the 30 minute is" (0:37:11). "can you look at 15 minute no I'm not looking at the 15minute" (0:56:29).
- **Top-down order:** daily, then 4-hour, then 1-hour, then 30-minute, every day. "we got to justify this long bias on small time frames" (0:44:06).
- **First-seconds rule:** a break of the previous candle's high or low in the first seconds to a minute and a half of a new candle is not an entry (0:17:43, 0:47:18, 1:19:00).
- **Fake-out:** after a close beyond a zone that is reversed by the next candle, "there's a very high probability that price is going to continue pushing in the opposite direction" (0:20:09).
- **Sells:** "always in an uptrend wait for price to create support and wait for price to break support for sells" (0:34:44).
- **Buys in an uptrend:** "we're going to make a high wait for price to come down create support take a buy" (0:44:28).
- **Weak candle:** a small-bodied bullish close is not a buy signal (0:37:51).
- **Range versus stop:** the room to the next zone must exceed the stop (0:35:47, 1:02:46).
- **Market opens:** "the 1 hour candles will respect the lows and the highs of the previous candles because there's so much volume" (0:28:37).
- **Session structure:** "there are two four our candles that are in the London session" and two in New York (0:19:07-0:19:27); a pre-London trade is a bet on a large 4-hour candle.
- **Holding:** pre-London and London trades run with no target until pre-New York. "all my trades that run from pre- London till pre- New York they're closed all of them" (1:10:07). New York trades are held short (0:53:43).
- **Trailing:** under the lows of closed 1-hour candles (0:29:18); in practice also under a closed 30-minute candle (trade 5). Asked whether he only checks on 30-minute and 1-hour closes, he agrees (1:13:27).
- **Charts unattended:** "I don't watch the charts at this time during uh pre- London till New York open" (1:12:13).
- **Sizing:** 1% base. 1.5% when ahead: "we're going to leverage some of our profits because it's a Wednesday" (1:05:33). 2% only as a simulation "second chance" (1:21:26). Add-on 0.5%.
- **Do not buy the top of the 4-hour** (1:14:51).
- **Waiting:** "whenever you hope price is going to go certain way wait 10 minutes" (1:11:10).

## What the frames show that the transcript alone would not

1. Every trade is a buy, with exact entry, stop, lot size and equity after each one. The equity chain closes to the cent: 10,000.00 -> 10,521.11 -> 10,640.67 -> 10,730.99 -> 10,592.21 -> 10,854.61 -> 10,746.90 -> 11,070.95.
2. Stop distances at entry: 2.93, 3.04, 2.44, 3.29, 3.10, 1.63, 3.29 dollars (16 to 33 of his pips). Lot size is computed by the simulator from the risk percent and that distance.
3. "Below the wick" is loose. Trade 1's stop is 0.34 under the candle low; trade 2's is 0.49 above the low of the candle he names; trades 5 and 7 are 0.10 and 0.08 above the wick low. He places it by eye near the low, sometimes inside the wick.
4. Entries happen inside a forming candle, not at its close, except trade 3: 63 seconds into a 30-minute candle (trade 1), 34 minutes into a 1-hour candle (2), 3 seconds after a 1-hour close (3), 3 h 13 min into a 4-hour candle (4), 15.6 minutes into a 1-hour candle (5), 4 minutes into a 30-minute candle (6), under 5 minutes into the London-open candle (7).
5. After a partial close the leftover (0.03, 0.04, 0.09 lots) gets its stop moved to exact break-even in trades 1, 3 and 7; in trade 2 it kept the original stop.
6. Trade 4's stop was widened by 1.05 dollars while losing, turning a 1% loss into 1.3%. The transcript only says "a much better area".
7. Trade 7's exit was 100% of the main order and 70% of the add-on, not 70% of the whole. The add-on was bought while the first order was 108 USD under water.
8. The Monday 15:30 spike was not US CPI according to the simulator's own calendar.
9. Trade 4 was stopped just before the Tuesday CPI release, and the release then moved 6 dollars in his direction within 50 seconds.
10. Zone prices to three decimals, from the lines he lays through the bands, and how thin the bands are (a quarter to half a dollar on the 30-minute and 1-hour).
11. The first stop move in trade 1 was to under the 1-hour lows (1941.011), still 1.46 below entry - a trail, not a move to break-even.
12. The spread in the simulation is a fixed 0.15 dollars, so every buy fills 0.15 above the chart price.

## Could not be read / open questions

- Exact second and price of: the trade 2 remainder close (between 15:20:23 and 15:30:18; about 1962.9 implied), the trade 3 and trade 7 remainder stop-outs, the trade 4 and trade 6 stop-outs.
- The low of the Tue 12:30 30-minute candle (the reference for trade 3's stop).
- Whether trade 6's stop was below or inside the 09:00 wick (within about 0.2).
- Why he says "24 23 Pips" for trade 7 when the order is 3.288 dollars from its stop.
- Band edges without a line through them are by eye, good to about 0.2-0.3 dollars.
- No statistics or closed-trades tab is ever opened; results come from the equity field.
- The weekly chart was opened at the start but never used; the 15-minute appears once (1:14:30) without a decision made on it.
- The transcript's target "19 7465" (0:58:16) is ambiguous; later he names 1978 and the frames show the exit at 1978.233.

## Is this the "Video 12" of the older transcript-only notes?

**No.** Those notes describe a losing buy from support around 33 minutes, a resistance-retest sell around 36-46 minutes, a trade refused around 21:40 because of a 27-pip stop, an ADP stop-out around 1:15 and an NFP pending-order tactic around 1:19. In this video:
- there is no sell at all - all seven positions are buys;
- at 21:40-22:15 he takes a buy with a "28 29 Pips" stop; he does not refuse it;
- at 33 minutes he is explaining why he will not sell; nothing is open and nothing loses;
- 36-46 minutes is a refused buy, then the trade 2 buy and its close, then the start of a new day;
- at 1:15 he refuses a buy at the top of the 4-hour; at 1:19 he refuses a sell in the first 19 seconds of a candle;
- ADP and NFP are never mentioned, no pending order is ever placed (every order is a market order through the Visual Buy box), and the replay week of 11-14 Apr 2022 contains CPI and retail sales, not ADP or NFP.
The only resemblance is a long gold simulation with a stop of about 27-29 pips discussed near the 21-22 minute mark. "Video 12" is a different recording.
