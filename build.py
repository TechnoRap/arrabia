#!/usr/bin/env python3
"""Static site builder for the EMBRACER concept site.

    python3 build.py        -> writes public/

Pages live in src/pages/**/*.html. Each starts with a front-matter comment:
    <!-- title: Research | nav: research | desc: One line. -->
The body is wrapped in src/layout.html. {{root}} becomes the relative path to
the site root ("" or "../"). Detail pages are generated from data/*.json.
"""
import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")
DATA = os.path.join(ROOT, "data")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def load(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


def render(tpl, ctx):
    """{{key}} replacement. Missing keys stay visible so they get noticed."""
    return re.sub(r"{{\s*(\w+)\s*}}", lambda m: str(ctx.get(m.group(1), m.group(0))), tpl)


def front_matter(text):
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    meta = {}
    if m:
        for part in m.group(1).split("|"):
            if ":" in part:
                k, v = part.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


LAYOUT = read(os.path.join(SRC, "layout.html"))


def page(rel, body, meta):
    depth = rel.count("/")
    root = "../" * depth
    ctx = {
        "root": root,
        "title": meta.get("title", "EMBRACER"),
        "desc": meta.get("desc", "EMBRACER, Earth System Feedback Research Centre."),
        "nav": meta.get("nav", ""),
        "bodyclass": meta.get("bodyclass", ""),
        "content": render(body, {"root": root}),
    }
    out = render(LAYOUT, ctx)
    # mark the active nav item
    out = out.replace(f'data-nav="{ctx["nav"]}"', f'data-nav="{ctx["nav"]}" aria-current="page"')
    write(rel, out)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ---------- explore components ----------

def explore_markup(topics, figure, kind, root):
    """topics: list of dicts id,label,x,y,tone,body(html). Returns section html."""
    hotspots, panels, items = [], [], []
    pfx = kind.lower()
    for i, t in enumerate(topics, 1):
        hotspots.append(
            f'<button class="hotspot hotspot--{t["tone"]}" style="--x:{t["x"]}%;--y:{t["y"]}%" '
            f'type="button" data-topic="{t["id"]}" aria-controls="{pfx}-{t["id"]}" aria-expanded="false">'
            f'<span aria-hidden="true">+</span><span class="sr-only">{html.escape(t["label"])}</span></button>'
        )
        panels.append(
            f'<article class="topic topic--{t["tone"]}" id="{pfx}-{t["id"]}" data-topic="{t["id"]}" tabindex="-1">'
            f'<p class="eyebrow">{i:02d} · {kind}</p><h3 class="topic__title">{html.escape(t["label"])}</h3>'
            f'{t["body"]}</article>'
        )
        items.append(
            f'<li><button type="button" class="explore__item" data-topic="{t["id"]}" aria-controls="{pfx}-{t["id"]}">'
            f'<span class="explore__num">{i:02d}</span>{html.escape(t["label"])}</button></li>'
        )
    return f"""
<div class="explore" data-explore>
  <div class="explore__stage">
    <div class="explore__scroll">
    <figure class="explore__figure">
      {figure}
      <div class="explore__hotspots">{"".join(hotspots)}</div>
    </figure>
    </div>
    <aside class="explore__panel" aria-live="polite">
      <button type="button" class="explore__close" data-explore-close aria-label="Close panel">×</button>
      {"".join(panels)}
    </aside>
  </div>
  <nav class="explore__list" aria-label="{kind} list">
    <p class="eyebrow">All {kind.lower()}s</p>
    <ol>{"".join(items)}</ol>
  </nav>
</div>"""


def feedback_loops_explore(root):
    topics = []
    for h in load("feedback-loops.json"):
        topics.append({**h, "body": f"<p>{html.escape(h['text'])}</p>"})
    figure = (f'<img src="{root}assets/img/feedback-loops.webp" width="1133" height="553" '
              f'alt="Illustration of a landscape block with ice sheets, permafrost, ocean, algae, forests, glaciers, '
              f'houses and groundwater; a carbon loop and a water loop arc through the atmosphere." loading="lazy">')
    return explore_markup(topics, figure, "Topic", root)


_map_n = [0]


def world_map_svg(sites, root):
    path = read(os.path.join(DATA, "world-land-path.txt")).strip()
    _map_n[0] += 1
    n = _map_n[0]
    # the clip hides the edge segments that route antimeridian crossings along the map border
    return (
        f'<svg class="worldmap" viewBox="0 -28 1000 549.7" role="img" aria-labelledby="worldmap-title-{n}">'
        f'<title id="worldmap-title-{n}">World map with EMBRACER research sites</title>'
        f'<clipPath id="worldmap-clip-{n}"><rect x="1" y="1" width="998" height="491.7"/></clipPath>'
        f'<path class="worldmap__land" clip-path="url(#worldmap-clip-{n})" d="{path}"/></svg>'
    )


def research_sites_explore(root):
    sites = load("research-sites.json")["sites"]
    projects = {p["id"]: p for p in load("projects.json")["projects"]}
    topics = []
    for s in sites:
        lis = []
        for p in s["projects"]:
            pid = "ssp-" + p["ssp"].split()[-1]
            lis.append(f'<li><a href="{root}research/{pid}.html"><strong>{p["ssp"]}</strong> {html.escape(p["text"])}</a></li>')
        body = f'<p class="topic__meta">{abs(s["lat"])}°{"N" if s["lat"]>=0 else "S"}, {abs(s["lon"])}°{"E" if s["lon"]>=0 else "W"} · approximate</p><ul class="topic__links">{"".join(lis)}</ul>'
        topics.append({"id": s["id"], "label": s["name"], "x": round(s["px"] / 10, 1), "y": round((s["py"] + 28) / 5.497, 1), "tone": "rust", "body": body})
    return explore_markup(topics, world_map_svg(sites, root), "Site", root)


def publications_list(root):
    pubs = load("publications.json")
    pubs = sorted(pubs, key=lambda r: (-int(r["year"]), r["title"].lower()))
    rows, years = [], sorted({str(r["year"]) for r in pubs}, reverse=True)
    for r in pubs:
        pid = slug(r["doi"])
        kws = [k.strip() for k in r["keywords"].split(",") if k.strip()][:4]
        tags = "".join(f'<span class="tag">{html.escape(k)}</span>' for k in kws)
        rtype = "Zenodo" if "zenodo" in r["repository"].lower() else html.escape(r["repository"])
        search = html.escape(r["keywords"].lower())
        rows.append(
            f'<li class="pub" data-year="{r["year"]}" data-type="{rtype}" data-project="" data-search="{search}">'
            f'<div class="pub__year">{r["year"]}</div><div>'
            f'<p class="pub__title"><a href="{root}publications/{pid}.html">{html.escape(r["title"])}</a></p>'
            f'<p class="pub__meta">{html.escape(r["authors"])} · {rtype} · <a href="https://doi.org/{r["doi"]}" rel="noopener">{r["doi"]}</a></p>'
            f'<div class="pub__tags">{tags}</div></div></li>')
    opts = "".join(f'<option value="{y}">{y}</option>' for y in years)
    return "".join(rows), opts, len(pubs)


def globe_svg(lat0=18.0, lon0=-30.0):
    """Orthographic globe of the land data for the hero. Back-side points are
    pushed to the horizon, which is good enough for 110m coastlines."""
    import math
    d = json.load(open(os.path.join(DATA, "land-110m.json"), encoding="utf-8"))
    sc, tr = d["transform"]["scale"], d["transform"]["translate"]
    arcs = []
    for arc in d["arcs"]:
        x = y = 0; pts = []
        for dx, dy in arc:
            x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
        arcs.append(pts)
    p0, l0 = math.radians(lat0), math.radians(lon0)
    R = 212.0
    def proj(lon, lat):
        lam, phi = math.radians(lon), math.radians(lat)
        cosc = math.sin(p0) * math.sin(phi) + math.cos(p0) * math.cos(phi) * math.cos(lam - l0)
        x = math.cos(phi) * math.sin(lam - l0)
        y = math.cos(p0) * math.sin(phi) - math.sin(p0) * math.cos(phi) * math.cos(lam - l0)
        if cosc < 0:  # behind the globe: snap to horizon
            n = math.hypot(x, y) or 1
            x, y = x / n, y / n
        return 300 + R * x, 300 - R * y
    def ring(idxs):
        pts = []
        for i in idxs:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(a if not pts else a[1:])
        return pts
    land = d["objects"]["land"]
    geoms = land["geometries"] if land["type"] == "GeometryCollection" else [land]
    path = ""
    for g in geoms:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        for poly in polys:
            for r in poly:
                pts = [proj(lon, lat) for lon, lat in ring(r)]
                # skip rings fully on the back side (all snapped to horizon)
                if all(abs(math.hypot(x - 300, y - 300) - R) < 0.5 for x, y in pts):
                    continue
                path += "M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    return path


# ---------- build ----------

def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    shutil.copytree(DATA, os.path.join(OUT, "data"))

    # static pages
    for dirpath, _, files in os.walk(os.path.join(SRC, "pages")):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, os.path.join(SRC, "pages"))
            meta, body = front_matter(read(full))
            root = "../" * rel.count("/")
            body = body.replace("{{explore_feedback_loops}}", feedback_loops_explore(root))
            body = body.replace("{{explore_research_sites}}", research_sites_explore(root))
            body = body.replace("{{worldmap}}", world_map_svg(None, root))
            if "data-worldpath" in body:
                body = body.replace('d="" data-worldpath', f'd="{globe_svg()}" data-worldpath')
            if "{{publications_list}}" in body:
                rows, opts, n = publications_list(root)
                body = body.replace("{{publications_list}}", rows).replace("{{pub_year_options}}", opts).replace("{{pub_count}}", str(n))
            page(rel, body, meta)

    # research detail pages
    tpl = read(os.path.join(SRC, "templates", "research-detail.html"))
    sites = {s["id"]: s for s in load("research-sites.json")["sites"]}
    fl = {h["id"]: h for h in load("feedback-loops.json")}
    projects = load("projects.json")["projects"]
    for p in projects:
        site_links = "".join(
            f'<li><a href="../explore/research-sites.html#{sid}">{sites[sid]["name"]}</a></li>' for sid in p["sites"])
        topic_links = "".join(
            f'<li><a href="../explore/feedback-loops.html#{t}">{fl[t]["label"]}</a></li>' for t in p["topics"])
        others = [q for q in projects if q["id"] != p["id"] and set(q["sites"]) & set(p["sites"])]
        related = "".join(
            f'<li><a href="{q["id"]}.html"><strong>{q["ssp"]}</strong> {html.escape(q["title"])}</a></li>' for q in others) or "<li>None yet.</li>"
        body = render(tpl, {**p, "title_html": html.escape(p["title"]), "site_links": site_links,
                            "topic_links": topic_links, "related": related})
        page(f"research/{p['id']}.html", body, {"title": f"{p['ssp']} · Research", "nav": "research", "desc": p["title"]})

    # publication detail pages
    tpl = read(os.path.join(SRC, "templates", "publication-detail.html"))
    pubs = load("publications.json")
    for r in pubs:
        pid = slug(r["doi"])
        r["id"] = pid
        kws = "".join(f'<li class="tag">{html.escape(k.strip())}</li>' for k in r["keywords"].split(",") if k.strip())
        body = render(tpl, {"id": pid, "title_html": html.escape(r["title"]), "year": r["year"],
                            "authors": html.escape(r["authors"]), "doi": r["doi"], "url": r["url"],
                            "repository": html.escape(r["repository"]), "keywords": kws})
        page(f"publications/{pid}.html", body, {"title": f"{r['title']} · Publication", "nav": "publications",
                                                "desc": r["title"]})
    # publications index gets its rows from data; write enriched json for the filter script
    write("data/publications.json", json.dumps(pubs, ensure_ascii=False, indent=1))
    print(f"built {sum(len(f) for _, _, f in os.walk(OUT))} files into public/")


if __name__ == "__main__":
    build()
