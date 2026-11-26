# Brief: read one video and write its trade records

You are helping with a private study of how one trading educator (Raja Banks) trades gold. The goal
is an evidence-based record of **what he actually does on the chart**: where he enters, where the stop
and target are, what he had drawn, how he manages the trade. Earlier notes were made from transcripts
only; nobody had looked at the charts. Your job is one video: read its transcript, pull frames from
the video, LOOK at them, and write the record.

## What you have

- Transcript (auto captions, 20-second blocks with timestamps): `C:\Users\rupes\rajagoldbot\research\raja\source\transcripts\<VIDEO_ID>.txt`
- Video (video track only, 1080p): `C:\Users\rupes\rajagoldbot\research\raja\source\video\<VIDEO_ID>.mp4`
- Frame tool (PowerShell, run from `C:\Users\rupes\rajagoldbot`):
  `.\.venv-raja\Scripts\python research\raja\source\tools\frames.py research\raja\source\video\<VIDEO_ID>.mp4 research\raja\source\frames\<VIDEO_ID> 22:25 40:50 1:05:10`
  It writes `<hh-mm-ss>.jpg` per time. Options: `--every 20 <from> <to>` for a frame every 20 s;
  `--crop x0,y0,x1,y1` (fractions of the frame) with `--tag name` to save an enlarged part, useful for
  reading the price axis or an order box. View frames with the Read tool.
- Where to write: `C:\Users\rupes\rajagoldbot\research\raja\source\trades\<VIDEO_ID>.md`

## What is already known (check it, do not assume it)

- **Pip:** on his later platforms 1 pip on gold = 0.10 dollars (three on-screen proofs). In the 2022
  simulator the order box showed a stop of 2.93 dollars as "-292.8 pips" (the simulator counts 0.01
  as a pip) while he said "28, 29 pips". Whenever a stated pip figure and prices are both visible,
  record both so this can be confirmed or contradicted.
- **Zones:** in the videos read so far he draws thin grey bands at the edge of candle bodies (where
  candles closed), leaving the wicks sticking through. Say what you see in THIS video, including
  where it differs.
- **Simulator:** the older simulations are Soft4FX on MetaTrader 4. A panel at top right shows the
  replay date, time and weekday (for example "11.04.2022 08:31:03 Monday"), and the chart title shows
  the timeframe. The "Visual Buy/Sell" order box shows SL and TP prices and the risk. Newer videos use
  other platforms; find the equivalent.

## How to work

1. Read the whole transcript first. List every moment where he places, manages or closes a trade,
   refuses a trade, draws or explains zones, or states a rule. The video's chapter list (given below,
   if any) marks his trades.
2. Pull frames at those moments: just before the entry, at the entry (order box or the moment after
   the fill), at each stop move or partial close, at the exit, where he draws zones, and one of each
   higher-timeframe view he uses before the trade. Scan with `--every` if you need to find the exact
   second. Keep the saved set to about 25 to 35 frames for the video; delete scan frames you do not need.
3. Look at every frame you cite. Read prices off the price axis or the order box. If you cannot read
   something, write UNREADABLE. Never guess a number, and never fill a gap from the transcript without
   saying it came from the transcript.
4. Write the file.

## The file to write

Plain Markdown, in your own words. Start with: video id, title, the platform, instrument, the replay
dates covered, and how you found the pip size here. Then:

**One record per trade**, numbered, each with:
- video timestamp of entry and of exit
- replay DATE, TIME and weekday shown by the simulator at entry and at exit, and what timezone the
  clock appears to be in (say how you know, or UNKNOWN)
- instrument, chart timeframe on screen at entry
- direction; entry, stop and target PRICES; the stop distance in dollars AND what he calls it in pips
- risk he states (percent or money) and lot size if visible
- what was drawn: each zone's price, how thick, and where it sits relative to candles (body tops or
  bottoms, wick tips, swing points), and how far back the candles are that it is drawn from
- what the higher timeframes showed (daily, 4-hour, 1-hour), as he reads them and as the frame shows
- the entry trigger: which candle on which timeframe, closed or still open when he entered, and its
  shape (body size, wicks)
- his stated reason, as a short quote (under 25 words) with its timestamp
- each management action (partial close and how much, stop to break-even, trailing, exit) with the
  price, the replay time, and his stated reason with a short quote
- the outcome: profit or loss in dollars or pips or multiples of the stop, and how long it was held
- anything he says afterwards about what he would do differently

**Trades he refused or waited on**, each with the reason and a short quote.

**Rules he states in this video** (session times, which timeframe confirms, when he will not trade,
how he sizes, news), each with a timestamp and a short quote.

**What the frames show that the transcript alone would not.**

**Could not be read / open questions.**

## Rules

- Method only. Nothing about him personally, his business, promotions, or other people in the chat.
- Quotes under 25 words each, with timestamp. Everything else in your own words. Do not paste
  stretches of transcript.
- Describe each chart in words and numbers; the reader will not see the images.
- Work only inside `C:\Users\rupes\rajagoldbot\research\raja\source`. Do not use git, do not
  download anything, do not install anything, do not touch any other folder or program.
- Finish by replying with: how many trades you recorded, the replay dates, the pip finding, the three
  things most likely to change how a trading bot modelled on him should work, and what you could not read.
