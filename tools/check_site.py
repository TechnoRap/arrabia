#!/usr/bin/env python3
"""Checks public/: internal links and assets resolve, no {{ leftovers, one h1 per page,
every img has alt, every input has a label, no duplicate ids."""
import os, re, sys, html
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")
bad = 0
for dp, _, files in os.walk(ROOT):
    for fn in files:
        if not fn.endswith(".html"): continue
        p = os.path.join(dp, fn); rel = os.path.relpath(p, ROOT)
        s = open(p, encoding="utf-8").read()
        def err(msg):
            global bad; bad += 1; print(f"{rel}: {msg}")
        if "{{" in s: err("template leftover {{")
        n_h1 = len(re.findall(r"<h1[\s>]", s))
        if n_h1 != 1: err(f"{n_h1} h1 elements")
        for m in re.finditer(r"<img\b[^>]*>", s):
            if " alt=" not in m.group(0): err("img without alt: " + m.group(0)[:80])
        ids = re.findall(r'\sid="([^"]+)"', s)
        dups = {i for i in ids if ids.count(i) > 1}
        if dups: err("duplicate ids: " + ", ".join(sorted(dups)))
        for m in re.finditer(r"<(input|select|textarea)\b[^>]*>", s):
            tag = m.group(0)
            if 'type="hidden"' in tag or 'type="submit"' in tag: continue
            idm = re.search(r'\sid="([^"]+)"', tag)
            if not idm or f'for="{idm.group(1)}"' not in s:
                if "aria-label" not in tag: err("unlabelled field: " + tag[:80])
        for m in re.finditer(r'(?:href|src)="([^"#]*)(#[^"]*)?"', s):
            href, frag = m.group(1), m.group(2)
            if not href or href.startswith(("http", "mailto:", "data:", "tel:")): continue
            target = os.path.normpath(os.path.join(dp, href))
            if not os.path.exists(target): err(f"missing target {href}")
            elif frag and target.endswith(".html") and frag != "#":
                t = open(target, encoding="utf-8").read()
                if f'id="{frag[1:]}"' not in t and f"data-topic=\"{frag[1:]}\"" not in t: err(f"missing anchor {href}{frag}")
print("problems:", bad)
sys.exit(1 if bad else 0)
