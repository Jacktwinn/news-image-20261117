#!/usr/bin/env python3
"""Entry program for make.fun's "Sum up 17 November's world news in one
image" bounty.

Writes the bundled front-page image to the output path. Deterministic and
offline: it copies entry.png (shipped in this repository) to
$OUTPUT_DIR/entry.png (default /output), byte for byte.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
