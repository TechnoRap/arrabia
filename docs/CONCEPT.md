# EMBRACER.nl — websiteconcept

Antwoord op de ontwerpbrief (`docs/BRIEF.md`). Het concept is uitgewerkt als statische site: `python3 build.py`, daarna `public/` openen. Alle feiten komen uit `docs/CONTENT-SOURCE.md`; alles wat ontbreekt staat als placeholder in de pagina's.

## 1. Visuele richting

**Sfeer:** rustig, redactioneel, geloofwaardig. Een licht mineraal papier (`#f4f5f1`) met diepe blauwgroene tekst (`#1e3b3f`). Het logo bepaalt de kleuren: ijsblauw `#85cfe9` (oceaan/ijs), olijfgroen `#93a756` (land/leven), roest `#b75434` (accent, actieve staat, pins), antraciet `#565656` (secundaire tekst). Geen extra kleuren.

**Typografie:** Fraunces (zachte serif, grote koppen) voor titels; Inter voor lopende tekst en interface. Grote koppen, ruime witruimte, korte alinea's, tekst links uitgelijnd.

**Beeld:** aarde, water, ijs en leven. De wereldbol in de hero is een echte orthografische projectie van Natural Earth-data met de roestkleurige baan uit het logo. De kaart gebruikt dezelfde data (Equal Earth). De klimaatillustratie is de bestaande EMBRACER-illustratie uit Genially.

**Beweging:** zacht. Secties schuiven in bij scrollen, de bol draait langzaam, hotspots pulseren, een dunne doorlopende lijn (roest → blauw → groen) verbindt de verhalende secties. Alles werkt zonder beweging (`prefers-reduced-motion`) en zonder JavaScript.

## 2. Sitemap

```
Home                         index.html
Research                     research.html
  Project (SSP 1–8)          research/ssp-N.html
Explore                      explore/index.html
  Feedback loops             explore/feedback-loops.html
  Research sites (kaart)     explore/research-sites.html
Network                      network.html
Publications                 publications.html
  Publicatie (26)            publications/<doi-slug>.html
About                        about.html
Jobs                         jobs.html
Contact                      contact.html
Privacy                      privacy.html
Sign in                      signin.html        (besloten, visueel concept)
Visitor portal               portal.html        (besloten, visueel concept)
Admin / editor               admin.html         (besloten, visueel concept)
```

Navigatie: logo, Research, Explore, Network, Publications, About, Jobs, Contact, knop **Sign in**. Footer: adres, sitelinks, partners, financiering, privacy, link naar het portal.

## 3. Homepage-template (volgorde van secties)

1. **Hero** — eyebrow "Earth System Feedback Research Centre", kop "Climate change now and beyond 2100", centrale onderzoeksvraag, twee knoppen, draaiende wereldbol.
2. **One system** — vier tegels: Ice, Water, Life, Climate; elke tegel linkt naar een punt in de klimaatillustratie.
3. **Verhaal** — twee afwisselende tekst/beeld-rijen ("Emerging climate feedbacks", "Bridging the gap") langs de doorlopende lijn.
4. **Interactief 1: Nine feedback loops** — de klimaatillustratie met negen punten, paneel en onderwerpenlijst.
5. **Interactief 2: Where we work** — de kaart met vijf pins, paneel met projecten per locatie, lijst met locaties.
6. **Research** — drie uitgelichte projecten, link naar alle projecten.
7. **Publications** — drie recentste records uit de catalogus.
8. **Consortium + contact** — donkere afsluitende band met partners, financiering (NWO Summit) en contactknoppen.
9. **Footer.**

## 4. Herbruikbare detailindeling

Research-, publicatie- en Explore-detailpagina's delen één opbouw:

- **Page-head**: eyebrow (categorie · nummer), grote titel, één regel samenvatting, knoppenrij (primair: "See on the map"/"Open in repository", secundair: terug naar overzicht).
- **Twee kolommen** (`grid--sidebar`): links proza met vaste koppen (Summary, Approach, Climate processes, Results and impact; bij publicaties Summary, Keywords, Project), rechts kaarten met gekoppelde items (locaties, gerelateerde projecten, publicaties, record-gegevens, bijlagen).
- **Explore-pagina's**: page-head, dan de interactieve component, dan een context-sectie met twee kolommen tekst of kaarten.

Op smalle schermen worden de kolommen onder elkaar gezet; de zijkolom volgt onder de tekst.

## 5. Componenten en interacties

- **Explore-component** (`[data-explore]`): afbeelding of SVG-kaart + absoluut geplaatste "+"-punten (procentueel, dus schaalbaar) + paneel + genummerde onderwerpenlijst. Klik of Enter op een punt of lijstitem opent het paneel; pijltjestoetsen springen tussen punten; Esc sluit. De URL-hash onthoudt het onderwerp (`#permafrost`), zodat je kunt linken naar een punt. Op telefoons wordt het paneel een schuif van onderen en kan de afbeelding zijwaarts scrollen. Zonder JavaScript staan alle teksten gewoon onder elkaar in het paneel.
- **Kaart**: Natural Earth land, Equal Earth-projectie, pins op regio-niveau. Elke pin toont de SSP-projecten op die locatie en linkt naar de projectpagina.
- **Kaarten (cards)**: witte kaart met dunne rand; hele kaart klikbaar via een verborgen link; gekleurde varianten voor thema's; gestippelde variant voor placeholders.
- **Publicatiefilter**: zoekveld + jaar + type + project; telt resultaten en toont een lege staat. De lijst staat volledig in de HTML, het filter is een laagje bovenop.
- **Formulieren**: velden met zichtbare labels, foutmelding per veld, statusbalk met bevestiging of fout. In het concept wordt niets verzonden.
- **Hotspot-editor (admin)**: dubbelklik plaatst een punt, slepen of pijltjestoetsen verplaatsen het, eigenschappenpaneel (titel, x, y, categorie, uitleg, afbeelding, link), desktop/telefoon-preview, concept/gepubliceerd-status.
- **Knoppen**: één primaire (donker), een ghost-variant en een roest-variant voor de belangrijkste actie per pagina. Minimaal 44–48 px hoog.

## 6. Mobiel en toegankelijkheid

- Eén kolom onder 600 px, twee onder 960 px; geen horizontale scroll (gecontroleerd op 390 px breed).
- Menu-knop op telefoon; zonder JavaScript staat de navigatie gewoon in beeld.
- Skip-link, één `h1` per pagina, logische kopvolgorde, labels op alle velden, `alt` op alle beelden, zichtbare focusring, contrast van tekst op papier ≥ 7:1.
- Niets is alleen via hover bereikbaar; alle interactie werkt met toetsenbord.
- Reduced motion schakelt animatie en parallax uit; de inhoud verandert niet.

## 7. De interactieve modellen

Beide Genially-onderdelen zijn nagebouwd als inhoud, niet als code: een afbeelding plus een lijst punten in `data/feedback-loops.json` en `data/research-sites.json`. Dezelfde component rendert beide; een nieuw interactief onderdeel is een nieuwe afbeelding plus een nieuwe lijst. Dat is precies wat de editor (admin) later moet bewerken.

## Open punten voor Rabia

Zie het einde van `docs/CONTENT-SOURCE.md`: betekenis en volledige naam van "SSP", gebruiksrecht van de herofoto, thema-indeling van de projecten (nu een voorstel), teksten voor Research-detail en Network, welke publicaties bij welk project horen.
