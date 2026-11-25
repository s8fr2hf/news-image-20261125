#!/usr/bin/env python3
"""Entry program for news-image-20261125.

The front page image entry.png is committed in this repository (drawn
by render.py with Pillow at build time). This program copies that
committed image to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png)
and validates it: PNG magic, at most 1 MiB, exactly 1024 x 1024.
Standard library only, so it runs in the grader's stdlib-only sandbox,
which has no Pillow and no DejaVu fonts: nothing is re-rendered here.
Deterministic: two runs produce byte-identical output.
"""

import os
import shutil
import struct

MAX_BYTES = 1048576
EXPECTED_SIZE = (1024, 1024)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    with open(src, "rb") as fh:
        data = fh.read()

    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit"
                         % len(data))
    # Read width and height from the PNG IHDR chunk with struct.
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED_SIZE:
        raise SystemExit("entry.png is %dx%d, expected 1024x1024"
                         % (width, height))

    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)
    # Verify the copy landed intact: re-read the destination and compare.
    with open(dest, "rb") as fh:
        written = fh.read()
    if written != data:
        raise SystemExit("entry.png copy mismatch: wrote %d bytes, "
                         "read back %d" % (len(data), len(written)))
    print("wrote %s (%dx%d, %d bytes)" % (dest, width, height, len(data)))


if __name__ == "__main__":
    main()
