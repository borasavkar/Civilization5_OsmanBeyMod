#!/usr/bin/env python3
"""Embeds tools/map_grid.txt, tools/map_rivers.txt and the historic sites into the map script."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data  # noqa: E402
from projection import H, W, fy_to_lat, lonlat_to_cell  # noqa: E402

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
OUT = os.path.join(ROOT, "Osman Bey", "Maps", "OB_Ottoman1299.lua")


def main():
    rows = [l.rstrip("\n") for l in open(os.path.join(TOOLS, "map_grid.txt"), encoding="utf-8") if l.strip()]
    assert len(rows) == H and all(len(r) == W for r in rows)
    rivers = [tuple(map(int, l.split())) for l in open(os.path.join(TOOLS, "map_rivers.txt"), encoding="utf-8") if l.strip()]

    out = ["-- Map data. Source: Natural Earth (public domain). Rows are listed from north to south.",
           "OB_MAP = {}",
           "OB_MAP.Width = %d" % W,
           "OB_MAP.Height = %d" % H,
           "OB_MAP.Rows = {"]
    out += ['"%s",' % r for r in rows]
    out.append("}")
    out.append("OB_MAP.LatRows = {" + ", ".join("%.1f" % fy_to_lat(y + 0.5) for y in range(H)) + "}")
    out.append("OB_MAP.Rivers = {")
    line = []
    for r in rivers:
        line.append("{%d,%d,%d,%d}," % r)
        if len(line) == 12:
            out.append("".join(line))
            line = []
    if line:
        out.append("".join(line))
    out.append("}")

    out.append("OB_MAP.MajorStarts = {")
    for civ, lon, lat, label in data.MAJOR_STARTS:
        x, y = lonlat_to_cell(lon, lat)
        out.append('\t{"%s", %d, %d}, -- %s' % (civ, x, y, label))
    out.append("}")

    out.append("OB_MAP.MinorSites = {")
    for t, lon, lat in data.BASE_MINOR_SITES:
        x, y = lonlat_to_cell(lon, lat)
        out.append('\t["%s"] = {%d, %d},' % (t, x, y))
    for key, v in data.NEW_MINORS.items():
        x, y = lonlat_to_cell(v[4], v[5])
        out.append('\t["MINOR_CIV_OB_%s"] = {%d, %d},' % (key, x, y))
    out.append("}")

    out.append("OB_MAP.ScenarioCities = {")
    for civ, cities in data.SCENARIO_CITIES.items():
        cells = ", ".join("{%d, %d}" % lonlat_to_cell(lon, lat) for _, lon, lat, _ in cities)
        out.append('\t["%s"] = {%s},' % (civ, cells))
    out.append("}")

    with open(os.path.join(TOOLS, "map_template.lua"), encoding="utf-8") as fh:
        tpl = fh.read()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(tpl.replace("--@@MAPDATA@@", "\n".join(out)))
    print("map script:", OUT, "(%d river edges)" % len(rivers))


if __name__ == "__main__":
    main()
