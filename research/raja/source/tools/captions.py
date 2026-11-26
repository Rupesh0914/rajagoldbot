"""Download English captions for YouTube videos and write a timestamped plain-text transcript.

    python captions.py <out_dir> <video id> [<video id> ...]

Captions only, no video. One request per video, with a pause between videos and a slow retry when
YouTube answers "too many requests". The .vtt and .txt files it writes are the speaker's material:
they stay on this machine (.gitignore keeps them out of the repository).
"""
import re
import subprocess
import sys
import time
from pathlib import Path

YT_DLP = str(Path(sys.executable).with_name("yt-dlp.exe"))
CUE = re.compile(r"^(\d\d):(\d\d):(\d\d)\.\d+ --> ")
TAG = re.compile(r"<[^>]+>")
BLOCK_SECONDS = 20


def fetch(video_id, out_dir):
    """The .vtt path for the video, downloading it if it is not there yet. None if there are no captions."""
    have = sorted(out_dir.glob(video_id + ".*.vtt"))
    if have:
        return have[0]
    # "en-orig" is the speech as recognised; plain "en" can be a machine translation, which YouTube rate-limits hard.
    for wait, lang in ((0, "en-orig"), (5, "en"), (60, "en-orig"), (180, "en"), (420, "en-orig")):
        time.sleep(wait)
        run = subprocess.run(
            [YT_DLP, "--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", lang,
             "--sub-format", "vtt", "--no-warnings", "-o", str(out_dir / "%(id)s.%(ext)s"),
             "https://www.youtube.com/watch?v=" + video_id],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        have = sorted(out_dir.glob(video_id + ".*.vtt"))
        if have:
            return have[0]
        message = (run.stderr or run.stdout).strip().splitlines()[-1:] or ["no output"]
        if "429" in message[0]:
            print("  %s: rate limited on %s" % (video_id, lang), flush=True)
    print("  %s: no captions obtained, skipped" % video_id, flush=True)
    return None


def to_text(vtt_path):
    """Auto captions repeat each line as it scrolls: keep each spoken line once, in 20-second blocks."""
    blocks, last, stamp, at = [], None, None, 0
    for raw in vtt_path.read_text(encoding="utf-8", errors="replace").splitlines():
        cue = CUE.match(raw)
        if cue:
            at = int(cue[1]) * 3600 + int(cue[2]) * 60 + int(cue[3])
            continue
        line = TAG.sub("", raw).strip()
        if not line or line == last or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        last = line
        if stamp is None or at - stamp >= BLOCK_SECONDS:
            stamp = at
            blocks.append(["%d:%02d:%02d" % (at // 3600, at % 3600 // 60, at % 60)])
        blocks[-1].append(line)
    return "\n".join("[%s] %s" % (b[0], " ".join(b[1:])) for b in blocks) + "\n"


def main():
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    for video_id in sys.argv[2:]:
        text_path = out_dir / (video_id + ".txt")
        if text_path.exists():
            continue
        vtt = fetch(video_id, out_dir)
        if vtt:
            text_path.write_text(to_text(vtt), encoding="utf-8")
            print("  %s: %d bytes" % (video_id, text_path.stat().st_size))
        time.sleep(8)


if __name__ == "__main__":
    main()
