# EMBRACER content source (collected 2026-10-31)

Everything below was taken from embracer.nl and the two Genially pages. Items marked **check with Rabia** are gaps or guesses.

## Brand colours (from the logo, `assets/img/logo-embracer.png`)

| Role | Hex | Where in the logo |
|---|---|---|
| Sky blue | `#85cfe9` | globe oceans |
| Olive green | `#93a756` | globe land |
| Rust orange | `#b75434` | orbit ring |
| Charcoal | `#565656` | wordmark "EMBRACER" and tagline |
| White | `#ffffff` | globe grid lines |

Tagline in the logo: **Earth System Feedback Research Centre**.

Not brand: `#2ea3f2` (Divi theme default blue, appears on every page) and the Divi greys. The old DESIGN.md in ~/Documents/EMBRACER lists `#82c0c7` and `#94a754` from the page CSS; the logo file gives the exact values above, so the logo wins.

## Current site pages and text

Navigation: Home, About, Jobs, Results, Contact. Footer: Privacy Statement.

**Home** — only a hero image (`assets/img/hero-reflection.jpg`, © Scott Cramer Photography, **check usage rights with Rabia**) with the title "Climate change now and beyond 2100".

**About**

> ### Emerging climate feedbacks
> More heatwaves in oceans, intensifying droughts on continents, thawing permafrost, melting icecaps. Consequences of climate change have begun emerging worldwide in the oceans, ice, land, and atmosphere.
>
> Complex feedbacks in Earth's climate system, triggered by ongoing CO2 emissions and warming, can influence global warming potentially much further. While the impacts of these feedbacks are expected to be relatively minor over the coming years to decades, they will determine the future of Earth's climate far beyond 2100.
>
> However, even in today's best climate models, scientific understanding of these feedbacks remains highly uncertain. This uncertainty risks underestimating sea level rise, the extremity of disruptive heatwaves, or spending huge resources on ineffective climate action plans.
>
> ### Bridging the gap
> At EMBRACER, we bring together a wide range of world-leading climate experts. Earth scientists, geochemists, oceanographers, polar researchers, hydrologists and ecologists collaborate to bridge the knowledge gap between predicting short-term and long-term climate change.
>
> We work at the very frontiers of knowledge on climate change, Earth's climate system and climate feedbacks, while enabling junior researchers' professional and leadership development, and fostering long term excellence and diversity in our field. Due to its interdisciplinary approach to connect different earth systems components, timescales and methods, EMBRACER is uniquely positioned to study climate change and feedbacks mechanisms of great importance to timescales of decades to millennia.
>
> EMBRACER is a 10-year research programme funded by the Summit grant from the Dutch Research Council NWO.

Partner logos on the About page: Vrije Universiteit Amsterdam, NIOZ, Wageningen University & Research, Utrecht University, Radboud Universiteit.

**Jobs** — empty page (title only).

**Results** — "Research Data Catalog": a table (Author(s), Title, Keywords, DOI / Repository Link) with keyword legend and filter, loaded from `harvested_data.json` (copied to `data/publications.json`, 26 Zenodo records).

**Contact**

- EMBRACER Office, Utrecht University, Faculty of Geosciences, Vening Meineszgebouw A, Princetonlaan 8a, 3584 CB Utrecht, info@embracer.nl
- Project Manager: dr. Sylvia Walter, S.Walter@uu.nl
- Data Support: Aristotelis Kandylas, a.kandylas@uu.nl
- Administrative Assistant: Nora Azergui, n.azergui@uu.nl
- Outreach & Education: Bjinse Dankert, b.t.dankert@uu.nl
- Two-step contact form (name, e-mail; then comments/questions).

## Interactive 1: Feedback Loops (Genially 6a8c24455837a6891d706f40)

One 1133×553 illustration (`assets/img/feedback-loops.webp`, labels baked in; `feedback-loops-labels.webp` is the second layer Genially stacks on top) with nine "+" hotspots. Each opens a tooltip. Hotspot positions (percent of the image) and texts: `data/feedback-loops.json`.

Hotspot colours in Genially: blue `rgba(117,195,240)` for Atmosphere, Ice sheets, Permafrost, Glaciers; dark blue `rgba(26,13,114)` for Ocean and Algae; green `rgba(63,102,25)` for Forests and Groundwater; orange `rgba(191,77,15)` for Humans.

## Interactive 2: Map of EMBRACER research sites (Genially 6a8c4ad7a1bc28f8f92a2b4e)

World map (`assets/img/world-map.webp`, 1600×900) with five pins. A pin opens a popup with the site name and its SSP projects (`data/research-sites.json`). Two of the popups link "SSP 5" / "SSP 7" to embracer.nl/about.

| Site | Projects |
|---|---|
| Arctic Tundra | SSP 1, SSP 5, SSP 6 |
| Ocean | SSP 3, SSP 4, SSP 5, SSP 6 |
| Amazon | SSP 2, SSP 8 |
| Himalaya | SSP 7, SSP 8 |
| Antarctica | SSP 5, SSP 6 |

SSP = Sub-Study Project (**check term with Rabia**). SSP 1–8 one-line descriptions are in the JSON.

## Gaps (new pages have no source text yet)

- **Research**: only the SSP one-liners and the About text exist. Need: SSP leads, institutions, methods, timeline.
- **Network**: only the five partner logos. Need: people, institutions, roles.
- **Publications**: 26 catalogue records exist (`data/publications.json`); the old DESIGN notes say Rabia keeps the catalogue.
- **Jobs**: empty on the live site.
