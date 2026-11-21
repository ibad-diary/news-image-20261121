#!/usr/bin/env python3
"""Copy the pre-rendered front page to the make.fun output directory.

Reads entry.png next to this file, verifies it (PNG magic, <= 1 MiB,
dimensions <= 1024x1024 from the IHDR chunk), then copies it verbatim to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Deterministic: running
twice produces byte-identical output.
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024
MAX_DIM = 1024


def main():
    with open(SRC, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        sys.exit("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < 33 or data[12:16] != b"IHDR":
        sys.exit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        sys.exit("entry.png is %dx%d, over the %dx%d limit"
                 % (width, height, MAX_DIM, MAX_DIM))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote %s (%dx%d, %d bytes)" % (dst, width, height, len(data)))


if __name__ == "__main__":
    main()
