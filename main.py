# SPDX-License-Identifier: MIT
"""Entry point for the news-image-20261121 round-3 program.

Copies the pre-rendered front page (entry.png, in this repository) to
$MAKEFUN_OUTPUT_DIR/entry.png and verifies the output: PNG magic bytes,
size at most 1 MiB, and dimensions 1024x1024. Standard library only.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
WANT_W, WANT_H = 1024, 1024


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit" % size)
    w, h = png_size(dest)
    if (w, h) != (WANT_W, WANT_H):
        raise SystemExit("entry.png is %dx%d, want %dx%d" % (w, h, WANT_W, WANT_H))
    print("wrote %s (%d bytes, %dx%d)" % (dest, size, w, h))
    return 0


if __name__ == "__main__":
    sys.exit(main())
