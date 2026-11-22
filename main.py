#!/usr/bin/env python3
"""Entry point: render the front page and place it where make.fun expects.

Builds entry.png with generate_image.py (PIL, build-time only), then copies
it to $MAKEFUN_OUTPUT_DIR/entry.png and verifies the result: PNG magic,
size at most 1 MiB, and 1024x1024 pixels. Deterministic: running this
script twice writes byte-identical files.
"""
import hashlib
import os
import shutil
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1024 * 1024
WIDTH = 1024
HEIGHT = 1024


def png_dimensions(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("not a PNG file: %s" % path)
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    subprocess.run([sys.executable, os.path.join(HERE, "generate_image.py")],
                   check=True)
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    width, height = png_dimensions(dst)
    if size > MAX_BYTES:
        raise SystemExit("entry.png too big: %d bytes" % size)
    if (width, height) != (WIDTH, HEIGHT):
        raise SystemExit("wrong size: %dx%d" % (width, height))
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    src_digest = hashlib.sha256(open(src, "rb").read()).hexdigest()
    if digest != src_digest:
        raise SystemExit("copy mismatch: %s != %s" % (digest, src_digest))
    print("OK entry.png %d bytes %dx%d sha256=%s -> %s"
          % (size, width, height, digest, dst))


if __name__ == "__main__":
    main()
