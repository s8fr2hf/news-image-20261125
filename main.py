"""Copy the pre-rendered front-page poster to the scoring output directory.

Pure standard library. The poster itself (entry.png) is committed in this
repository; this entrypoint only validates it and copies it to
$MAKEFUN_OUTPUT_DIR (default /output), then reads the copy back and checks
it is byte-identical to the source.
"""

import os
import struct
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
MAX_BYTES = 1 << 20  # 1 MiB
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def validate_png(data):
    """Check size, PNG magic and IHDR dimensions; return (width, height)."""
    if len(data) > MAX_BYTES:
        fail(f"poster is {len(data)} bytes, over the 1 MiB limit")
    if data[:8] != PNG_MAGIC:
        fail("poster is not a PNG file (bad magic bytes)")
    if len(data) < 24:
        fail("poster is too short to contain a PNG IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail(f"poster is {width}x{height}, expected "
             f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
    return width, height


def write_and_verify(target, data):
    """Write data to target, read it back and confirm byte equality."""
    try:
        target.write_bytes(data)
    except OSError as exc:
        fail(f"cannot write output poster: {exc}")
    try:
        written = target.read_bytes()
    except OSError as exc:
        fail(f"cannot read back output poster: {exc}")
    if written != data:
        fail("output poster differs from source poster after copy")


def main():
    repo_root = Path(__file__).resolve().parent
    source = repo_root / SOURCE_NAME
    if not source.is_file():
        fail(f"source poster not found: {source}")

    try:
        data = source.read_bytes()
    except OSError as exc:
        fail(f"cannot read source poster: {exc}")

    width, height = validate_png(data)

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        fail(f"cannot create output directory {output_dir}: {exc}")
    target = output_dir / SOURCE_NAME
    write_and_verify(target, data)

    print(f"wrote {target} ({len(data)} bytes, "
          f"{width}x{height}, verified byte-identical)")


if __name__ == "__main__":
    main()
