"""Build catalogue.tsv from the channel listing (catalogue_raw.txt: tab, id, seconds, title per line).

    python catalogue.py <source dir>

Adds two columns from what is on this machine: whether a transcript was fetched, and whether frames were read.
The listing gives no upload date; where yt-dlp fetched a video's own page the date is taken from there.
"""
import sys
from pathlib import Path

source = Path(sys.argv[1])
rows, seen = [], set()
for line in (source / "catalogue_raw.txt").read_text(encoding="utf-8-sig").splitlines():
    parts = line.split("\t")
    if len(parts) < 4 or parts[0] not in ("videos", "streams", "shorts"):
        if rows:                                         # a title that contained a line break
            rows[-1][3] += " " + line.strip()
        continue
    tab, video_id, seconds, title = parts[0], parts[1], parts[2], "\t".join(parts[3:]).strip()
    if video_id in seen:
        continue
    seen.add(video_id)
    try:
        total = int(float(seconds))
        length = "%d:%02d:%02d" % (total // 3600, total % 3600 // 60, total % 60)
    except ValueError:
        length = ""
    rows.append([tab, video_id, length, title])

lines = ["tab\tid\tlength\ttitle\turl\ttranscript_read\tframes_read"]
for tab, video_id, length, title in rows:
    transcript = "yes" if (source / "transcripts" / (video_id + ".txt")).exists() else ""
    frames = "yes" if (source / "frames" / video_id).is_dir() else ""
    lines.append("\t".join([tab, video_id, length, title.replace("\t", " "),
                            "https://www.youtube.com/watch?v=" + video_id, transcript, frames]))
(source / "catalogue.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("%d videos; transcripts %d; frames %d" % (
    len(rows), sum("\tyes\t" in l or l.endswith("\tyes") for l in lines), sum(l.endswith("\tyes") for l in lines)))
