"""Entry program for news-image-20261120.

Copies the repository's entry.png to the output directory make.fun gives
us ($MAKEFUN_OUTPUT_DIR, or /output). Standard library only, no network,
and a pure copy, so two runs always write the same bytes.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        sys.stderr.write("entry.png missing next to main.py\n")
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("copied entry.png to", target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
