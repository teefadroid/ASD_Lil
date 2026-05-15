# ASD International — Website

A static, dependency-free corporate website for **ASD International Medical Requisites LLC**, a UAE-based pharmaceutical company.

## Design

Modeled on the editorial language of **[lilly.com](https://www.lilly.com/)**:

- **Full-bleed video hero** with a large serif headline overlaid in white — *"A medicine company should do more than just make medicine."*
- **Three-column action row** under the hero (Find care / Access medicine / Partner with us), each cell with a top border + icon + serif heading + small copy + arrow link, matching Lilly's hero-bottom pattern.
- **Product Support grid** with square thumbnail tiles + serif label below — same treatment Lilly uses for the "Condition Support" section (Cancer / Diabetes / Migraine, etc.).
- **Image+text splits** with oversized serif headlines like *"Our job's not done once the formula is made."*
- **Full-bleed RED band** with a patient pull-quote in italic serif — Lilly's patient-story treatment, recolored in ASD red (`#D52B1E`).
- **Bottom-bordered form fields** instead of boxed inputs.
- **No rounded glass cards or gradient blobs** — flat, editorial pharma.
- **EB Garamond** for headlines, **Inter** for body.

The **footer** is the only deviation from Lilly's red palette — it stays in **logo-derived blue + green** (`#103564 → #0A2247` background with `#5BB133` accents) per the brief.

All design tokens live in [`assets/css/site.css`](./assets/css/site.css) under the `:root` block.

## Content

All company details — products, ingredients, benefits, dosage, contact info, address, LinkedIn — were scraped from the live `asdinternationaluae.com` site and restructured for the new layout in [`_build/build.py`](./_build/build.py).

| Page | Source |
| ---- | ------ |
| `index.html` | Hand-written: full-bleed video hero + 3-col action row + product thumb grid + image-split + red pull-quote + partner split |
| `about.html` | Story split + red purpose-quote band + 6-card technology pillars + reverse split |
| `products.html` | Filterable thumb grid (categories) + red CTA band |
| `products/<slug>.html` | One detail page per product (×11) — image, highlights row, spec grid, benefits, composition, related thumbs |
| `partners.html` | 3-col partnership models + red "what you get" band + image split |
| `contact.html` | Phone, email, HQ address, embedded Google Map + bottom-bordered contact form |

## Project layout

```
.
├── index.html
├── about.html
├── products.html
├── partners.html
├── contact.html
├── products/
│   ├── asd-iron.html
│   ├── asd-magnesium.html
│   ├── asd-sustained-vit.html
│   ├── zinco-q10.html
│   ├── asd-carniplex.html
│   ├── inpro.html
│   ├── asd-semifer-10mg.html
│   ├── asd-semifer-14mg.html
│   ├── asd-semifer-40mg.html
│   ├── asd-chelazen.html
│   └── asd-magneflex.html
├── assets/
│   ├── css/site.css
│   ├── js/site.js
│   ├── img/                 # Logo, favicon, product images, hero image
│   └── video/ASD.mp4        # Full-bleed hero video
└── _build/build.py          # Static-site generator
```

## Running locally

There is **no build step at runtime** — everything is plain HTML/CSS/JS. Just serve the folder:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Regenerating the section pages

If you change product data, copy or layout, edit the `PRODUCTS` list in `_build/build.py` and re-run:

```bash
python3 _build/build.py
```

This rewrites `about.html`, `partners.html`, `contact.html`, `products.html` and every `products/<slug>.html`.

The home page (`index.html`) is hand-curated and is **not** touched by the generator.

## Contact

- **Phone:** +971 2 245 9549
- **Email:** info@asdinternational.co
- **Headquarters:** Block 2 — Store No. 3, Abu Dhabi Industrial City — ICAD III, Abu Dhabi, UAE
- **LinkedIn:** [ASD International Medical Requisites](https://www.linkedin.com/company/asd-international-medical-requisites)
