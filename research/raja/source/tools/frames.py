"""Save single frames of a video as JPEG.

    python frames.py <video file> <out_dir> <h:mm:ss or m:ss> [...]          one frame per time
    python frames.py <video file> <out_dir> --every 30 <from> <to>           one frame every 30 s
    add  --crop x0,y0,x1,y1  (fractions of the frame, e.g. 0.5,0,1,1) to save only part of it,
    add  --tag name          to append a name to the file (for crops)

Files are named <hh-mm-ss>.jpg. Frames are the speaker's material: they stay on this machine.
"""
import sys
from pathlib import Path

import cv2


def seconds(text):
    total = 0
    for part in text.split(":"):
        total = total * 60 + float(part)
    return total


def main():
    args = sys.argv[1:]
    crop, tag, every = None, "", None
    if "--crop" in args:
        i = args.index("--crop")
        crop = [float(v) for v in args[i + 1].split(",")]
        del args[i:i + 2]
    if "--tag" in args:
        i = args.index("--tag")
        tag = "_" + args[i + 1]
        del args[i:i + 2]
    if "--every" in args:
        i = args.index("--every")
        every = float(args[i + 1])
        del args[i:i + 2]
    video, out_dir, times = args[0], Path(args[1]), [seconds(t) for t in args[2:]]
    if every:
        start, end = times
        times = []
        while start <= end:
            times.append(start)
            start += every
    out_dir.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(video)
    if not capture.isOpened():
        sys.exit("cannot open " + video)
    for at in times:
        capture.set(cv2.CAP_PROP_POS_MSEC, at * 1000)
        ok, frame = capture.read()
        if not ok:
            print("no frame at %s" % at)
            continue
        if crop:
            h, w = frame.shape[:2]
            frame = frame[int(crop[1] * h):int(crop[3] * h), int(crop[0] * w):int(crop[2] * w)]
        whole = int(at)
        name = "%02d-%02d-%02d%s.jpg" % (whole // 3600, whole % 3600 // 60, whole % 60, tag)
        cv2.imwrite(str(out_dir / name), frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print("%d frames -> %s" % (len(times), out_dir))


if __name__ == "__main__":
    main()
