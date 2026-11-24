#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261124 bounty.

Regenerates entry.png deterministically (stdlib only, no network) and
copies it to /output/entry.png, as the grader expects.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    sys.path.insert(0, HERE)
    import draw

    img = draw.build()
    src = os.path.join(HERE, "entry.png")
    img.save(src, "PNG", optimize=True)
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, "/output/entry.png")
    print("wrote /output/entry.png", os.path.getsize("/output/entry.png"), "bytes")


if __name__ == "__main__":
    main()
