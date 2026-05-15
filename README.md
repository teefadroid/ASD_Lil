# ASD International — Website

A static, dependency-free corporate website for **ASD International Medical Requisites LLC**, a UAE-based pharmaceutical company.

## Design

- **Editorial pharma aesthetic** inspired by Eli Lilly's corporate language: cream paper canvas, navy ink, warm red accent, Fraunces serif paired with Inter, generous whitespace, full-bleed image moments and slow scroll reveals.
- **Footer recolored from the ASD logo** — deep blue (`#1B549A` / `#103564` / `#0A2247`) with an antelope-green accent (`#5BB133`).
- **Home-page centerpiece** is the existing `ASD.mp4` video, framed in a 4:5 navy-glass card with floating quality chips around it.

All design tokens live in [`assets/css/site.css`](./assets/css/site.css) under the `:root` block.

## Content

All company details — products, ingredients, benefits, dosage, contact info, address, LinkedIn — were scraped from the live `asdinternationaluae.com` site and restructured for the new layout in [`_build/build.py`](./_build/build.py).

| Page | Source |
| ---- | ------ |
| `index.html` | Hand-written hero + featured products + stats + CTA |
| `about.html` | Mission + technology pillars |
| `products.html` | Filterable grid of all 11 products |
| `products/<slug>.html` | One detail page per product (×11) |
| `partners.html` | Partnership models + CTA |
| `contact.html` | Phone, email, HQ address, embedded Google Map, contact form |

## Project layout

```
.
├── index.html               # Home page (hero + ASD.mp4 video)
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
│   ├── css/site.css         # Design tokens + components
│   ├── js/site.js           # Mobile menu, reveals, filters, form
│   ├── img/                 # Logo, favicon, product images, hero image
│   └── video/ASD.mp4        # Home-page centerpiece video
└── _build/build.py          # Static-site generator (header/footer/products)
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
