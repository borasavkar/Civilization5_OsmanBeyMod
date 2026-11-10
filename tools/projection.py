"""
Map projection shared by every build script.

The map is real geography (Natural Earth) with a gentle, piecewise-linear zoom:
Anatolia, the Balkans and the Black Sea get more hexes per degree, while the
Sahara, the Rub' al Khali and the far north are compressed. Coastlines stay
recognisable, but the Ottoman heartland has room for cities.

Grid convention (same as Civilization V): x grows east, y grows north (y = 0 is
the southern row) and odd rows are shifted half a hex to the east.
"""
import math

W, H = 110, 84

# (longitude, fractional column)
LON_CP = [(-6.0, 0.0), (10.0, 17.0), (20.0, 32.0), (26.0, 46.0), (36.0, 74.0), (45.0, 93.0), (58.0, 110.0)]
# (latitude, fractional row)
LAT_CP = [(12.0, 0.0), (26.0, 18.0), (32.0, 30.0), (36.0, 42.0), (42.0, 64.0), (46.0, 75.0), (51.0, 84.0)]

LON_MIN, LON_MAX = LON_CP[0][0], LON_CP[-1][0]
LAT_MIN, LAT_MAX = LAT_CP[0][0], LAT_CP[-1][0]

SQRT3_2 = math.sqrt(3.0) / 2.0


def _interp(v, cps, inverse=False):
    a, b = (1, 0) if inverse else (0, 1)
    if v <= cps[0][a]:
        p, q = cps[0], cps[1]
    elif v >= cps[-1][a]:
        p, q = cps[-2], cps[-1]
    else:
        for i in range(len(cps) - 1):
            if cps[i][a] <= v <= cps[i + 1][a]:
                p, q = cps[i], cps[i + 1]
                break
    t = (v - p[a]) / (q[a] - p[a])
    return p[b] + t * (q[b] - p[b])


def lon_to_fx(lon):
    return _interp(lon, LON_CP)


def lat_to_fy(lat):
    return _interp(lat, LAT_CP)


def fx_to_lon(fx):
    return _interp(fx, LON_CP, inverse=True)


def fy_to_lat(fy):
    return _interp(fy, LAT_CP, inverse=True)


def cell_center_frac(x, y):
    """Centre of hex (x, y) in fractional grid units."""
    return x + 0.5 + (0.5 if y % 2 == 1 else 0.0), y + 0.5


def cell_center_lonlat(x, y):
    fx, fy = cell_center_frac(x, y)
    return fx_to_lon(fx), fy_to_lat(fy)


def lonlat_to_cell(lon, lat):
    """Nearest hex for a longitude/latitude pair."""
    fx, fy = lon_to_fx(lon), lat_to_fy(lat)
    y = int(math.floor(fy))
    y = max(0, min(H - 1, y))
    shift = 0.5 if y % 2 == 1 else 0.0
    x = int(math.floor(fx - shift))
    x = max(0, min(W - 1, x))
    return x, y


def to_plane(fx, fy):
    """Fractional grid coordinates -> hex plane (rows are sqrt(3)/2 apart)."""
    return fx, fy * SQRT3_2


def neighbors(x, y):
    if y % 2 == 0:
        dirs = [(-1, 0), (1, 0), (-1, 1), (0, 1), (-1, -1), (0, -1)]
    else:
        dirs = [(-1, 0), (1, 0), (0, 1), (1, 1), (0, -1), (1, -1)]
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < H:
            yield nx, ny


def hex_distance(x1, y1, x2, y2):
    def to_cube(x, y):
        q = x - (y - (y & 1)) // 2
        r = y
        return q, r, -q - r
    a, b = to_cube(x1, y1), to_cube(x2, y2)
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))
