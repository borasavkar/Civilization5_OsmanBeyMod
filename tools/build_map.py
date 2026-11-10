#!/usr/bin/env python3
"""
Builds the "Ottoman Frontiers 1299" map from Natural Earth data.

Output:
  tools/map_grid.txt      one character per hex (north row first)
  tools/map_rivers.txt    river edges: x y kind flow
  Osman Bey/Maps/OB_Ottoman1299.lua   (assembled by assemble_map.py)

Hex characters:
  ~ sea / lake   g/G grassland (flat/hill)   p/P plains   d/D desert   t/T tundra   M mountain

Usage:  python tools/build_map.py <folder with Natural Earth .geojson files>
"""
import heapq
import json
import math
import os
import sys

from shapely.geometry import LineString, Point, shape
from shapely.ops import unary_union
from shapely.prepared import prep

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from projection import (H, W, cell_center_frac, fx_to_lon, fy_to_lat, lat_to_fy, lon_to_fx,  # noqa: E402
                        lonlat_to_cell, neighbors, to_plane)

GEO = sys.argv[1] if len(sys.argv) > 1 else "geo"
TOOLS = os.path.dirname(os.path.abspath(__file__))
GRID_FILE = os.path.join(TOOLS, "map_grid.txt")
RIVER_FILE = os.path.join(TOOLS, "map_rivers.txt")


def load(name):
    with open(os.path.join(GEO, name + ".geojson"), encoding="utf-8") as fh:
        return json.load(fh)["features"]


def noise(x, y, seed):
    n = (x * 374761393 + y * 668265263 + seed * 2246822519) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def smooth_noise(lon, lat, scale, seed):
    fx, fy = lon / scale, lat / scale
    x0, y0 = math.floor(fx), math.floor(fy)
    tx, ty = fx - x0, fy - y0
    tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
    a, b = noise(x0, y0, seed), noise(x0 + 1, y0, seed)
    c, d = noise(x0, y0 + 1, seed), noise(x0 + 1, y0 + 1, seed)
    return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty


# ------------------------------------------------------------------ data
# Modern reservoirs are left out: the map shows the world of 1299.
MODERN_LAKES = {"Lake Nasser", "Kremenchuk Reservoir", "Kakhovka Reservoir", "Lake Tharthar",
                "Razzaza Lake", "Lake Habbaniyah"}

land = unary_union([shape(f["geometry"]) for f in load("ne_50m_land")])
lakes = unary_union([shape(f["geometry"]) for f in load("ne_50m_lakes")
                     if f["properties"].get("name") not in MODERN_LAKES and shape(f["geometry"]).area > 0.09])
land = land.difference(lakes)
land_p = prep(land)

regions = load("ne_50m_geography_regions_polys")


def region_union(classes, exclude=()):
    geoms = [shape(f["geometry"]) for f in regions
             if f["properties"]["FEATURECLA"] in classes and f["properties"]["NAME"] not in exclude]
    return prep(unary_union(geoms)) if geoms else None


deserts = region_union({"Desert"})
ranges = region_union({"Range/mtn"}, exclude={"ETHIOPIAN HIGHLANDS"})
plateaus = region_union({"Plateau"}, exclude={"PENÍNSULA IBÉRICA"})

# Ranges missing from Natural Earth or too thin at this scale: (name, [(lon, lat)...], width in degrees)
EXTRA_RANGES = [
    ("Taurus", [(29.0, 36.9), (31.5, 36.9), (33.5, 36.8), (35.2, 37.3), (37.0, 37.9), (39.5, 38.3)], 0.45),
    ("Anti-Taurus", [(36.0, 38.6), (37.5, 39.3)], 0.30),
    ("Eastern Anatolia", [(39.5, 39.6), (41.5, 39.7), (43.3, 39.6)], 0.45),
    ("Pontic", [(31.5, 41.0), (34.0, 41.3), (36.5, 40.8), (39.0, 40.6), (41.5, 40.9)], 0.30),
    ("Ararat", [(43.6, 39.7), (44.3, 39.7)], 0.25),
    ("Uludag", [(29.1, 40.07), (29.3, 40.07)], 0.10),
    ("Amanus", [(36.1, 36.4), (36.5, 37.1)], 0.18),
    ("Lebanon", [(35.8, 33.3), (36.4, 34.6)], 0.25),
    ("Rhodope", [(23.5, 41.6), (25.5, 41.5)], 0.30),
    ("Balkan", [(22.6, 42.9), (25.5, 42.75), (27.0, 42.7)], 0.20),
    ("Pindus", [(20.6, 40.6), (21.4, 39.3), (22.0, 37.6)], 0.30),
    ("Olympus", [(22.2, 40.0), (22.5, 40.2)], 0.12),
    ("Crete", [(23.8, 35.3), (25.8, 35.15)], 0.10),
    ("Troodos", [(32.7, 34.95), (33.1, 34.95)], 0.10),
    ("Sinai", [(33.8, 28.6), (34.2, 29.2)], 0.25),
    ("Crimea", [(34.0, 44.7), (34.9, 44.85)], 0.12),
    ("Sicily", [(14.0, 37.9), (15.0, 37.75)], 0.15),
    ("Sardinia-Corsica", [(9.0, 40.0), (9.2, 42.0)], 0.20),
    ("Yemen", [(43.6, 13.5), (44.1, 15.5), (43.6, 17.5)], 0.40),
    ("Hajar", [(56.2, 24.5), (57.8, 23.2)], 0.30),
    ("Kopet Dag", [(55.0, 38.0), (58.0, 37.3)], 0.30),
    ("Kabylie-Aures", [(4.0, 36.5), (6.5, 35.3)], 0.25),
    ("Aurès", [(6.0, 35.2), (7.0, 35.1)], 0.15),
    ("Dinaric", [(15.8, 44.5), (18.5, 43.0), (19.8, 42.2)], 0.30),
]
extra_lines = [(LineString(pts), w) for _, pts, w in EXTRA_RANGES]


def near_extra_range(pt):
    return any(line.distance(pt) < w for line, w in extra_lines)


def land_fraction(x, y):
    fx, fy = cell_center_frac(x, y)
    hits = total = 0
    for dx in (-0.33, 0.0, 0.33):
        for dy in (-0.33, 0.0, 0.33):
            total += 1
            if land_p.contains(Point(fx_to_lon(fx + dx), fy_to_lat(fy + dy))):
                hits += 1
    return hits / total


def nile_lon(lat):
    if lat > 30.0:
        return 31.2
    if lat > 27.0:
        return 30.9 + (lat - 27.0) * 0.1
    if lat > 24.0:
        return 32.6 - (lat - 24.0) * 0.55
    if lat > 21.5:
        return 31.6 + (24.0 - lat) * 0.2
    return 30.5 + (21.5 - lat) * 0.4


# ----------------------------------------------------------- climate rules
def base_terrain(lon, lat, pt):
    """Flat terrain type: g p d t"""
    n = smooth_noise(lon, lat, 2.0, 7)
    # Nile valley stays green through the desert
    if 22.0 < lat < 31.6 and abs(lon - nile_lon(lat)) < 0.55:
        return "p" if n < 0.55 else "g"
    if lat > 49.0 and lon > 40.0:
        return "p" if n < 0.7 else "g"
    if deserts and deserts.contains(pt):
        return "d" if n < 0.93 else "p"
    # Sinai and the Negev
    if 32.4 < lon < 35.6 and 27.5 < lat < 31.25 and not (lon > 34.6 and lat > 30.9):
        return "d" if n < 0.85 else "p"
    # Arabian Peninsula
    if 35.0 < lon < 60.0 and lat < 31.0 and lon > 36.5 + (lat - 28) * 0.9 - 2:
        if lon < 45.5 and lat < 18.5:          # Yemen and Asir highlands
            return "p" if n < 0.55 else "g"
        if lon > 55.5 and lat < 25.5:          # Oman coast
            return "p" if n < 0.45 else "d"
        return "d" if n < 0.85 else "p"
    # Mesopotamia: green between the rivers, steppe outside
    if 38.0 < lon < 48.5 and 29.5 < lat < 37.0:
        if abs(lon - (44.0 - (lat - 33.0) * 0.9)) < 1.6:
            return "p" if n < 0.55 else "g"
        return "d" if n < 0.55 else "p"
    # Levant coast and Syria
    if 34.5 < lon < 38.5 and 31.0 < lat < 37.0:
        if lon < 36.3:
            return "p" if n < 0.5 else "g"
        return "p" if n < 0.6 else "d"
    # Iranian plateau
    if 48.0 < lon and 25.0 < lat < 37.0:
        if lat > 36.4 and lon < 54.0:          # Caspian shore (Gilan, Mazandaran)
            return "g"
        return "d" if n < 0.5 else "p"
    # Steppes north of the Black Sea and the Caspian
    if lon > 46.0 and 40.0 <= lat:
        if lat < 44.5:
            return "d" if n < 0.40 else "p"
        return "p" if n < 0.75 else "g"
    if 28.0 < lon < 46.0 and lat > 45.5:
        return "p" if n < 0.55 else "g"
    # North African coast
    if -6.0 < lon < 33.0 and 25.0 < lat < (37.5 if lon < 11.5 else 33.6):
        if lon < 11.0 and lat > 33.5:          # Maghreb Tell
            return "p" if n < 0.5 else "g"
        if 9.5 < lon < 11.5 and lat > 34.5:    # Ifriqiya
            return "p" if n < 0.6 else "g"
        if 20.0 < lon < 22.8 and lat > 32.2:   # Cyrenaica
            return "p"
        return "d" if n < 0.6 else "p"
    # Sahel
    if lat < 18.5 and lon < 40.0:
        return "p" if n < 0.7 else ("d" if lat > 15.0 else "g")
    # Horn of Africa
    if lon > 40.0 and lat < 15.0:
        return "d" if n < 0.5 else "p"
    # Anatolian plateau: drier plains, greener coasts
    if 26.0 < lon < 45.0 and 36.5 < lat < 41.3:
        if 31.0 < lon < 35.5 and 37.3 < lat < 39.8:
            return "p" if n < 0.75 else "d"
        return "p" if n < 0.55 else "g"
    if 30.0 <= lat < 45.0:
        return "p" if n < 0.45 else "g"
    return "g" if n < 0.65 else "p"


def relief(lon, lat, pt):
    """'' flat, 'H' hills, 'M' mountain"""
    r = noise(int(lon * 20), int(lat * 20), 11)
    if ranges and ranges.contains(pt):
        if r < 0.30:
            return "M"
        if r < 0.78:
            return "H"
        return ""
    if near_extra_range(pt):
        if r < 0.24:
            return "M"
        if r < 0.72:
            return "H"
        return ""
    if plateaus and plateaus.contains(pt):
        return "H" if r < 0.35 else ""
    if 26.0 < lon < 45.0 and 36.5 < lat < 41.5:      # Anatolia
        return "H" if r < 0.32 else ""
    if 19.0 < lon < 27.0 and 39.0 < lat < 44.0:      # Balkans
        return "H" if r < 0.30 else ""
    if 44.0 < lon < 58.0 and 29.0 < lat < 38.5:      # Iran
        return "H" if r < 0.25 else ""
    if 35.0 < lon < 38.0 and 30.0 < lat < 33.5:      # Judea, Transjordan
        return "H" if r < 0.30 else ""
    return "H" if r < 0.09 else ""


# Forced tiles: lines of (lon, lat) pairs and the character to draw.
FORCED_LINES = [
    ("~", [(29.00, 41.00), (29.06, 41.12), (29.12, 41.24)]),       # Bosphorus
    ("~", [(26.20, 40.03), (26.45, 40.22), (26.70, 40.42)]),       # Dardanelles
    ("~", [(-5.60, 35.95), (-5.30, 36.00)]),                       # Strait of Gibraltar
    ("~", [(43.40, 12.70), (43.30, 12.55)]),                       # Bab-el-Mandeb
    ("~", [(36.50, 45.15), (36.60, 45.40)]),                       # Kerch Strait
    ("~", [(56.30, 26.30), (56.50, 26.60)]),                       # Strait of Hormuz
    ("~", [(23.00, 38.30), (23.60, 38.70)]),                       # Euripus (Euboea)
    ("~", [(15.62, 38.20), (15.65, 38.30)]),                       # Strait of Messina
    ("d", [(32.30, 29.95), (32.35, 30.60), (32.30, 31.15)]),       # Isthmus of Suez
    ("~", [(28.60, 40.90), (27.80, 40.75)]),                       # Sea of Marmara
]


def forced_cells():
    out = {}
    for ch, pts in FORCED_LINES:
        line = LineString(pts)
        steps = max(2, int(line.length / 0.02))
        for i in range(steps + 1):
            p = line.interpolate(i / steps, normalized=True)
            out[lonlat_to_cell(p.x, p.y)] = ch
    return out


def build_grid():
    grid = [["~"] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if land_fraction(x, y) < 0.45:
                continue
            fx, fy = cell_center_frac(x, y)
            lon, lat = fx_to_lon(fx), fy_to_lat(fy)
            pt = Point(lon, lat)
            t = base_terrain(lon, lat, pt)
            rel = relief(lon, lat, pt)
            grid[y][x] = "M" if rel == "M" else (t.upper() if rel == "H" else t)
    for (x, y), ch in forced_cells().items():
        grid[y][x] = ch
    # Mountains next to straits or open water become hills; isolated mountains become hills.
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "M":
                nb = [grid[ny][nx] for nx, ny in neighbors(x, y)]
                if sum(1 for c in nb if c == "~") >= 3:
                    grid[y][x] = "P"
    # Single-tile islands of land in narrow straits are kept; lone lake tiles are kept (fresh water).
    return grid


# ------------------------------------------------------------------ rivers
RIVER_MIN_SCALERANK = 9
RIVER_SKIP = {"Gharraf Canal", "Shatt al Hillah", "Seine", "Loire", "Marne", "Yonne", "Vienne", "Tarn", "Dordogne",
              "Garonne", "Mosel", "Maas", "Schelde", "Weser", "Main", "Elbe", "Oder", "Vistula", "Bug", "Esla",
              "Doubs", "Tajo", "Duero", "Guadiana", "Guadalquivir", "Segre", "Mouhoun", "Nakanbé", "Bani", "Sokoto",
              "Komadugu Yobe", "Hadejia", "Chari", "Atrek", "Talkeh", "Ural", "Khopr"}
R = 1.0 / math.sqrt(3.0)


def vertex(cx, cy, angle_deg):
    a = math.radians(angle_deg)
    return (round(cx + R * math.cos(a), 3), round(cy + R * math.sin(a), 3))


def plot_plane_center(x, y):
    fx, fy = cell_center_frac(x, y)
    return to_plane(fx, fy)


def se_neighbor(x, y):
    return (x, y - 1) if y % 2 == 0 else (x + 1, y - 1)


def sw_neighbor(x, y):
    return (x - 1, y - 1) if y % 2 == 0 else (x, y - 1)


# kind: 1 = WOfRiver (east edge), 2 = NWOfRiver (south-east edge), 3 = NEOfRiver (south-west edge)
# flows: index into FlowDirectionTypes order N, NE, SE, S, SW, NW
FLOW = {"N": 0, "NE": 1, "SE": 2, "S": 3, "SW": 4, "NW": 5}


def build_river_graph(grid):
    adj = {}
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "~":
                continue
            cx, cy = plot_plane_center(x, y)
            owned = []
            if x + 1 < W and grid[y][x + 1] != "~":
                owned.append((1, vertex(cx, cy, -30), vertex(cx, cy, 30), "N", "S"))
            sx, sy = se_neighbor(x, y)
            if 0 <= sx < W and sy >= 0 and grid[sy][sx] != "~":
                owned.append((2, vertex(cx, cy, -90), vertex(cx, cy, -30), "NE", "SW"))
            wx, wy = sw_neighbor(x, y)
            if 0 <= wx < W and wy >= 0 and grid[wy][wx] != "~":
                owned.append((3, vertex(cx, cy, -90), vertex(cx, cy, -150), "NW", "SE"))
            for kind, a, b, fwd, back in owned:
                adj.setdefault(a, []).append((b, (x, y, kind, fwd)))
                adj.setdefault(b, []).append((a, (x, y, kind, back)))
    return adj


def nearest_vertex(verts_by_cell, p, maxd=1.2):
    best, bd = None, maxd
    cx, cy = int(p[0]), int(p[1] / 0.866)
    for gx in range(cx - 2, cx + 3):
        for gy in range(cy - 2, cy + 3):
            for v in verts_by_cell.get((gx, gy), ()):
                d = math.hypot(v[0] - p[0], v[1] - p[1])
                if d < bd:
                    best, bd = v, d
    return best


def shortest_path(adj, start, goal, limit=12.0):
    dist = {start: 0.0}
    prev = {}
    heap = [(math.hypot(start[0] - goal[0], start[1] - goal[1]), 0.0, start)]
    while heap:
        _, d, v = heapq.heappop(heap)
        if v == goal:
            path = [v]
            while v in prev:
                v = prev[v][0]
                path.append(v)
            path.reverse()
            return path, prev
        if d > limit or d > dist.get(v, 1e9):
            continue
        for w, info in adj.get(v, ()):
            nd = d + R
            if nd < dist.get(w, 1e9):
                dist[w] = nd
                prev[w] = (v, info)
                heapq.heappush(heap, (nd + math.hypot(w[0] - goal[0], w[1] - goal[1]), nd, w))
    return None, None


def edge_info(adj, a, b):
    for w, info in adj.get(a, ()):
        if w == b:
            return info
    return None


def build_rivers(grid):
    adj = build_river_graph(grid)
    verts_by_cell = {}
    for v in adj:
        verts_by_cell.setdefault((int(v[0]), int(v[1] / 0.866)), []).append(v)

    sea_cells = [(x, y) for y in range(H) for x in range(W) if grid[y][x] == "~"]
    sea_pts = [plot_plane_center(x, y) for x, y in sea_cells]

    def sea_distance(p):
        return min(math.hypot(p[0] - q[0], p[1] - q[1]) for q in sea_pts[::3])

    feats = load("ne_10m_rivers_lake_centerlines")
    lines = []
    for f in feats:
        p = f["properties"]
        name = p.get("name") or ""
        if name in RIVER_SKIP or (p.get("scalerank") or 99) > RIVER_MIN_SCALERANK:
            continue
        g = shape(f["geometry"])
        parts = list(g.geoms) if g.geom_type == "MultiLineString" else [g]
        for part in parts:
            pts = [(lon, lat) for lon, lat in part.coords
                   if -6.0 <= lon <= 58.0 and 12.0 <= lat <= 51.0]
            if len(pts) >= 2:
                lines.append((name, [to_plane(lon_to_fx(lon), lat_to_fy(lat)) for lon, lat in pts]))

    edges = {}
    used = 0
    for name, pts in lines:
        ls = LineString(pts)
        if ls.length < 2.0:
            continue
        # Mouth = the end closer to the sea; a tributary ends next to its main river,
        # which the "closer to the sea" test also gets right in nearly every case here.
        if sea_distance(pts[0]) < sea_distance(pts[-1]):
            ls = LineString(pts[::-1])
        n = max(2, int(ls.length / 0.8))
        targets = [ls.interpolate(i / n, normalized=True) for i in range(n + 1)]
        path = []
        cur = None
        for t in targets:
            v = nearest_vertex(verts_by_cell, (t.x, t.y))
            if v is None:
                continue
            if cur is None:
                cur = v
                path = [v]
                continue
            if v == cur:
                continue
            seg, _ = shortest_path(adj, cur, v)
            if seg is None:
                continue
            for w in seg[1:]:
                if w in path:                       # remove loops
                    path = path[:path.index(w) + 1]
                else:
                    path.append(w)
            cur = path[-1]
        if len(path) < 4:
            continue
        used += 1
        for a, b in zip(path, path[1:]):
            info = edge_info(adj, a, b)
            if info is None:
                continue
            x, y, kind, flow = info
            edges.setdefault((x, y, kind), FLOW[flow])
    print("rivers used: %d, edges: %d" % (used, len(edges)))
    return edges


def main():
    grid = build_grid()
    rows = ["".join(grid[y]) for y in range(H - 1, -1, -1)]     # north first
    with open(GRID_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")
    edges = build_rivers(grid)
    with open(RIVER_FILE, "w", encoding="utf-8") as fh:
        for (x, y, kind), flow in sorted(edges.items(), key=lambda e: (e[0][1], e[0][0], e[0][2])):
            fh.write("%d %d %d %d\n" % (x, y, kind, flow))
    land_count = sum(c != "~" for r in rows for c in r)
    print("map %dx%d, land %.1f%%" % (W, H, 100.0 * land_count / (W * H)))


if __name__ == "__main__":
    main()
