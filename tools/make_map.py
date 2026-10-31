#!/usr/bin/env python3
"""Regenerate data/world-land-path.txt (Equal Earth, 1000 x 493.7) from data/land-110m.json.
Rings that cross the antimeridian are split into pieces that close along the map outline,
and tiny rings that span the whole width (islands on the antimeridian) are dropped."""
import json, math, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "data", "land-110m.json")))
sc, tr = d["transform"]["scale"], d["transform"]["translate"]
arcs = []
for arc in d["arcs"]:
    x = y = 0; pts = []
    for dx, dy in arc:
        x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
    arcs.append(pts)
A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
M = math.sqrt(3) / 2
def proj(lon, lat):
    lam, phi = math.radians(lon), math.radians(lat)
    th = math.asin(M * math.sin(phi)); t2 = th * th; t6 = t2 * t2 * t2
    x = lam * math.cos(th) / (M * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)))
    y = th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))
    return x, -y
def ring(idxs):
    pts = []
    for i in idxs:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a if not pts else a[1:])
    return pts
land = d["objects"]["land"]
geoms = land["geometries"] if land["type"] == "GeometryCollection" else [land]
rings = []
for g in geoms:
    for poly in (g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]):
        for r in poly:
            rings.append(ring(r))
xs, ys = [], []
for r in rings:
    for lon, lat in r:
        x, y = proj(lon, lat); xs.append(x); ys.append(y)
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
W = 1000; s = W / (maxx - minx); H = (maxy - miny) * s
def P(lon, lat):
    x, y = proj(lon, lat); return (x - minx) * s, (y - miny) * s
path = ""
for r in rings:
    lons = [lon for lon, lat in r]
    if max(lons) - min(lons) > 300 and len(r) < 40:
        continue  # tiny ring straddling the antimeridian (Fiji): drop
    pts = [P(lon, lat) for lon, lat in r]
    chunks = [[]]
    for i, p in enumerate(pts):
        if i and abs(p[0] - pts[i - 1][0]) > W / 2:  # jump across the antimeridian
            east = pts[i - 1][0] > W / 2
            chunks[-1].append((P(180 if east else -180, r[i - 1][1])[0], pts[i - 1][1]))
            chunks.append([(P(-180 if east else 180, r[i][1])[0], p[1])])
        chunks[-1].append(p)
    if len(chunks) > 1:
        chunks[0] = chunks.pop() + chunks[0]  # the ring wraps: last piece continues into the first
    for c in chunks:  # Z closes each piece along the map outline
        path += "M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in c) + "Z"
open(os.path.join(ROOT, "data", "world-land-path.txt"), "w").write(path)
print("viewBox 0 0", W, round(H, 1), "rings", len(rings))
