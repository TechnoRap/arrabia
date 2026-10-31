# EMBRACER concept site

Static concept website for embracer.nl (Earth System Feedback Research Centre), built from the design brief in `docs/BRIEF.md`.

## View it

```bash
python3 build.py && python3 -m http.server 4141 --directory public
```

Then open http://127.0.0.1:4141/ . Opening `public/index.html` straight from the file system also works.

## Structure

- `src/layout.html` header, footer, head. `src/pages/**` page bodies (front-matter comment on line 1). `src/templates/` detail-page templates.
- `data/` all content that is generated: feedback-loop hotspots, research sites, projects, 26 publication records, world map path.
- `assets/css/site.css` the design system (logo colours, type, components). `assets/js/site.js` progressive interactivity.
- `build.py` assembles `public/`. `tools/make_map.py` regenerates the world map path from Natural Earth data.
- `docs/CONTENT-SOURCE.md` what was collected from the current site and the two Genially interactives, plus open questions for Rabia.

No framework, no build dependencies beyond Python 3.
