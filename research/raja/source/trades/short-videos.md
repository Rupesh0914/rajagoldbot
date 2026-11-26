# Four short videos: one live buy, one simulated buy, and his stop and target rules

Read by me (the main session) from the transcripts and frames.

## NOxfOi4EP_c - "How to do analysis on charts for Buys/Sells" (Aug 2024, 13:35)

- **Platform:** cTrader (Dominion Markets), live, filmed off a wall screen. Chart clock UTC+4. Date 7 Aug 2024.
- **Pip size:** the platform's own ruler reads "100 pips" over 10.0 dollars (0:03:05) and "50 pips" over 5.0 dollars
  (0:06:10); the stop label reads "Pips: -21.9" for 2.19 dollars (0:08:55). 1 pip = 0.10 dollars.
- The zone drawing in this video is described in `../TIMEFRAMES.md`, section 1.

### Trade - live buy from a support inside the range ("dynamic entry")

- **Video time:** 0:08:20 to 0:08:55. Reasons given at 0:11:27 to 0:12:09.
- **Real time:** filled at **14:00:48 on the chart clock (UTC+4) = 10:00:48 UTC = 06:00 New York, Wed 7 Aug 2024.**
- **Chart at entry:** 30-minute.
- **Direction and prices:** BUY 0.03 lots at **2394.47** (small second account, about 492 dollars). Stop **2392.28**.
  Target line at about **2399.2** (read from the axis).
- **Stop distance:** 2.19 dollars; the platform says 21.9 pips. About 1.4% of that account.
- **Target distance:** about 4.7 dollars, 47 pips, a little over twice the stop.
- **What was drawn:** resistance band about 2396.8 to 2397.3 (line 2397.06) on the body tops of the two candles at the
  morning high, wicks to about 2397.6. A short support band about 2389.2 to 2389.6 under the body bottoms of the red
  then green pair at the last low (11:30 and 12:00 chart time).
- **Higher timeframes:** 4-hour in a range between about 2386 and 2416.5. He treats both directions as open.
- **Entry trigger:** no break of resistance. Two supports had formed on the 30-minute (a low, a move up, a higher low).
  The 13:30 candle closed green; he bought 48 seconds into the 14:00 candle. Price was about 2.6 dollars under the
  resistance.
- **Stop placement:** just under the low of the previous 30-minute candle (wick low about 2392.4).
- **Target placement:** beyond the 2397 resistance, among the upper wicks left on 6 Aug (up to about 2399 to 2400): a
  wick fill.
- **Stated reason:** "we have a support formed ... price moved up and then we created another support" (0:11:27), with
  the pre-New-York volume coming.
- **Outcome:** not shown.

## BmpW93Hb62o - "Where to Place Your Take Profit" (Oct 2024, 9:07)

- **Platform:** cTrader "Market Replay" (a simulation). Replay clock UTC+4. Replay date **2 Oct 2024**.
- **Pip size:** "Pip value: $10.00" for 1.00 lot (100 ounces): 1 pip = 0.10 dollars. The target label reads
  "Pips: 61.7" for 6.17 dollars.

### Trade - simulated buy on the first clear up-close after a fall (teaching example)

- **Video time:** entry 0:03:50 to 0:04:11. Paused at 0:05:33. Reversal shown 0:08:01 to 0:08:21.
- **Replay time:** position created **02/10/2024 11:00:00 (UTC+4) = 07:00 UTC = 03:00 New York**, exactly on a
  30-minute close.
- **Chart at entry:** 30-minute.
- **Direction and prices:** BUY 5.00 lots at **2649.83**. Stop **2646.95**. Target then set at **2656.00**.
- **Stop distance:** 2.88 dollars, 28.8 pips. **Target distance:** 6.17 dollars, 61.7 pips.
- **What was drawn:** one purple band about 2647.6 to 2647.9 (0.3 dollars thick), just under the body bottoms of the red
  candle and the small green one at the low.
- **Before the entry (0:00:21 to 0:03:28):** price had fallen about 11 dollars in four 30-minute candles. He refuses
  three candles in a row: one closes with a small body; on the next an "impulse" break of the high fails and it closes
  the other way; the next closes up but small, with only a "12 pip range" above it. "because this body is so super
  small" (0:02:47).
- **Entry trigger:** the 10:30 candle closes green with a full body (about 2648.3 to 2649.9), the first clear up-close.
  "you got a candle closing bullish, we are creating support" (0:03:28). He buys on that close.
- **Stop placement:** under the band and under the lows of the last three candles (about 2647.3). He says the stop goes
  "below this candle" and not under the zone (0:04:11 to 0:04:33); here the two are almost the same place.
- **Target placement:** at the wick on the left, 61 to 63 pips away. He sets it there on purpose, to show it is too far.
- **Management and outcome:** at 11:09:58 the position reads "Pips: 36.6, $1,830.00" with price 2653.49. He leaves it;
  price turns and the position goes into loss (0:08:21). His point: he would have taken 30 to 40 pips and been out.

### His target rule (0:05:54 to 0:06:36, 0:08:21 to 0:08:42)

- Measure the clean range to the next obstacle on the left (a wick or a zone).
- Take **a fixed share of that range**, not a multiple of the stop: from 50 to 60 pips take 25 to 35; from 40 take 15 to
  20; from 50 take 20 to 25. "aim to get at least 50 to 60 percentage of that move" (0:08:42).
- "I secure that and then I leave the rest running" (0:06:15).
- He rejects fixed 1:2 and 1:3 targets: "throw that away, measure how big your range is" (0:08:21).

## mO5sISfLs-8 - "How to Set a Stop loss in Forex Trading" (Jan 2022, 9:44)

Drawings on a whiteboard, no chart, no trade. The rules:

- The stop goes beyond **the previous candle**, the one that confirmed the trade, not beyond the zone. "the best place to
  put your stop should be below the previous candle" (0:02:26).
- Why: in an up-move each candle should hold the previous candle's low. If the next candle breaks it, "it's no longer an
  uptrend" (0:03:07), so the trade idea is wrong at exactly that price.
- A stop beyond the zone is bigger, and a bigger loss tempts you to move it (0:07:35 to 0:08:17).
- "don't move your stops" (0:05:31).
- The confirming candle is a 30-minute or 1-hour close: "for scalping ... I focus on the 30 minute timeframe" (0:01:45).
  On the 15-minute "the confirmations aren't that strong" (0:02:06).
- The setup he uses as the example: an up-move, a pullback, a support forms, then a bullish close. He gives it "a 70 to
  80 percent chance" of retesting the new high (0:04:08).
- The candle he trades should be in a volume time: pre-London, London open, pre-New York, New York open (0:05:11).

## _aj37AaInxE and XAHyqVd5Fsw

No trade is placed in either. What they say about consolidation and about trading with the trend is in
`../TIMEFRAMES.md`, sections 2 to 4. The chart in XAHyqVd5Fsw shows prices of 192 to 197, so it is not gold.
