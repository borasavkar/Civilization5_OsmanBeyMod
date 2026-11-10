#!/usr/bin/env python3
"""Draws tools/map_grid.txt and tools/map_rivers.txt (and start sites) to docs/map_preview.png."""
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from projection import H, W, cell_center_frac  # noqa: E402

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
COL = {"~": (38, 84, 140), "g": (96, 150, 64), "G": (70, 118, 48), "p": (176, 168, 96), "P": (140, 132, 72),
       "d": (226, 206, 150), "D": (190, 170, 116), "t": (150, 150, 140), "T": (120, 120, 112), "M": (110, 96, 88),
       "s": (240, 240, 240)}
S = 12


def main(out=None, marks=None):
    rows = [l.rstrip("\n") for l in open(os.path.join(TOOLS, "map_grid.txt"), encoding="utf-8") if l.strip()]
    img = Image.new("RGB", (int((W + 1) * S), int((H + 1) * S * 0.866) + S), (20, 20, 24))
    d = ImageDraw.Draw(img)
    r = S / math.sqrt(3)

    def center(x, y):
        fx, fy = cell_center_frac(x, y)
        return fx * S, (H - fy) * S * 0.866 + S * 0.5

    for y in range(H):
        row = rows[H - 1 - y]
        for x in range(W):
            cx, cy = center(x, y)
            pts = [(cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))) for a in range(30, 390, 60)]
            d.polygon(pts, fill=COL.get(row[x], (255, 0, 255)))
    for line in open(os.path.join(TOOLS, "map_rivers.txt"), encoding="utf-8"):
        x, y, kind, _ = map(int, line.split())
        cx, cy = center(x, y)
        angs = {1: (-30, 30), 2: (-90, -30), 3: (-90, -150)}[kind]
        a, b = [(cx + r * math.cos(math.radians(t)), cy - r * math.sin(math.radians(t))) for t in angs]
        d.line([a, b], fill=(60, 140, 255), width=2)
    for (x, y, label, color) in (marks or []):
        cx, cy = center(x, y)
        d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=color, outline=(0, 0, 0))
        d.text((cx + 5, cy - 6), label, fill=(255, 255, 255))
    out = out or os.path.join(ROOT, "docs", "map_preview.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out)
    print("preview:", out)


if __name__ == "__main__":
    main(*(sys.argv[1:2]))
