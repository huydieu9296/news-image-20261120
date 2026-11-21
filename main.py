#!/usr/bin/env python3
"""Validate entry.png and place a copy in the output directory.

The entry must be a whole PNG, 1024 by 1024 pixels, no more than
1 MiB, summing up the world news of Friday 20 November 2026. This
module uses only the standard library: it reads the IHDR chunk for
the dimensions, then writes the copy through a temporary file and
renames it into place so a failed run never leaves a partial file
behind. The copy is read back and checked again before the program
reports success.

Usage: python3 main.py [output-dir]
The output directory defaults to $MAKEFUN_OUTPUT_DIR, else /output.
"""

import hashlib
import os
import sys
from pathlib import Path

LIMIT = 1_048_576
SIZE = (1024, 1024)
MAGIC = b"\x89PNG\r\n\x1a\n"


class EntryError(Exception):
    """The entry.png on disk fails one of the format rules."""


def dimensions(blob):
    """Return (width, height) of a PNG blob, raising EntryError."""
    if blob[:8] != MAGIC:
        raise EntryError("bad magic bytes: not a PNG file")
    if len(blob) < 33 or blob[12:16] != b"IHDR":
        raise EntryError("no IHDR chunk in the first 33 bytes")
    wide = int.from_bytes(blob[16:20], "big")
    high = int.from_bytes(blob[20:24], "big")
    return wide, high


def validate(blob):
    """Check size and dimensions; return (width, height)."""
    if len(blob) > LIMIT:
        raise EntryError(f"{len(blob)} bytes, over the 1 MiB limit")
    wide, high = dimensions(blob)
    if (wide, high) != SIZE:
        raise EntryError(f"{wide}x{high}, expected 1024x1024")
    return wide, high


def place(source, out_dir):
    """Copy source into out_dir/entry.png atomically, then verify it."""
    blob = source.read_bytes()
    wide, high = validate(blob)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    staging = out_dir / ".entry.png.tmp"
    staging.write_bytes(blob)
    # os.replace is atomic on the same filesystem, so a failed run
    # never leaves a partial entry.png behind.
    os.replace(staging, dest)
    again = dest.read_bytes()
    if again != blob:
        raise EntryError("written copy differs from entry.png")
    validate(again)
    return dest, wide, high, hashlib.sha256(again).hexdigest()


def main(argv):
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: {source} missing; run draw_news.py first",
              file=sys.stderr)
        return 1
    if len(argv) > 2:
        print("usage: main.py [output-dir]", file=sys.stderr)
        return 2
    picked = argv[1] if len(argv) == 2 else os.environ.get(
        "MAKEFUN_OUTPUT_DIR", "/output")
    try:
        dest, wide, high, digest = place(source, Path(picked))
    except (OSError, EntryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"ok: entry.png {wide}x{high}, {dest.stat().st_size} bytes, "
          f"sha256 {digest}")
    print(f"copied to {dest} (verified: magic, size, dimensions, bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
