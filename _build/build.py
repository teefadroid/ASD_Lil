#!/usr/bin/env python3
"""
ASD International — static-site generator (Lilly-inspired editorial design).

Reads structured product data and emits:
  - products.html               (catalog with category tabs + thumb grid)
  - products/<slug>.html        (one detail page per product)
  - about.html, contact.html, partners.html

The home page (index.html) is hand-written; everything else flows from here so
that the header, footer, and chrome stay in sync across the whole site.
"""

import os
from textwrap import dedent

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Product data (scraped from asdinternationaluae.com, restructured)
# ---------------------------------------------------------------------------

PRODUCTS = [
    {
        "slug": "asd-iron",
        "name": "ASD Iron",
        "tagline": "Liposomal iron, gentle on the gut.",
        "category": "Iron Supplement",
        "image": "ASDIron.png",
        "short": "An advanced food supplement that uses liposomal and nanotechnology delivery to manage iron-deficiency anemia — without the metallic taste, constipation or gastric discomfort of traditional iron supplements.",
        "long": (
            "ASD Iron is engineered to manage various types of anemia using a unique "
            "liposomal and nanotechnology delivery system. The carrier protects the "
            "iron through the digestive tract, dramatically improving absorption and "
            "bioavailability while keeping the experience gentle and well-tolerated. "
            "Available as 30 capsules per pack."
        ),
        "form": "Capsules — 30 per pack",
        "dosage": "As directed by a healthcare professional.",
        "highlights": ["Liposomal delivery", "Nanotechnology", "Gentle on the gut"],
        "benefits": [
            "Supports normal cognitive function and the normal transport of oxygen in the body",
            "Contributes to the normal formation of hemoglobin and red blood cells (with Vitamin B12)",
            "Supports normal function of blood vessels and protects cells from oxidative stress (Vitamin C)",
            "Supports normal immune-system function and the cell-division process",
            "Free from common side effects — no constipation, metallic taste or gastric discomfort",
        ],
        "ingredients": [
            "Iron 30 mg",
            "Folic Acid 200 mcg",
            "Vitamin B12 200 mcg",
            "Vitamin C 80 mg",
        ],
        "featured": False,
    },
    {
        "slug": "asd-magnesium",
        "name": "ASD Magnesium",
        "tagline": "The UAE's first liposomal magnesium.",
        "category": "Minerals",
        "image": "ASDMagnesium.png",
        "short": "The first liposomal magnesium supplement in the UAE — 400 mg of magnesium per tablet, delivered with premium-quality liposomal technology for superior absorption.",
        "long": (
            "ASD Magnesium delivers a high dose of 400 mg of magnesium per tablet using "
            "premium liposomal technology. The result is superior absorption, enhanced "
            "efficacy, and optimal support for sleep, mood, muscle relaxation and bone "
            "strength."
        ),
        "form": "Tablets",
        "dosage": "As directed by a healthcare professional.",
        "highlights": ["400 mg per tablet", "Liposomal", "First in the UAE"],
        "benefits": [
            "Helps stabilise mood and sleep — supportive in anxiety and insomnia",
            "Reduces muscle cramps and spasms; supports smooth muscle relaxation",
            "Helps with mood swings, irritability and headaches associated with PMS",
            "Aids calcium and Vitamin D metabolism, improving bone strength and healing",
            "Plays an important role in migraine management by stabilising neuronal membranes",
        ],
        "ingredients": ["Liposomal Magnesium Oxide 400 mg"],
        "featured": False,
    },
    {
        "slug": "asd-sustained-vit",
        "name": "ASD Sustained Vit",
        "tagline": "Twenty essential nutrients, released steadily all day.",
        "category": "Vitamins & Minerals",
        "image": "ASDSustainedVit.png",
        "short": "A comprehensive formula containing 20 essential vitamins and minerals, paired with a patented sustained-release technology for steady, all-day support.",
        "long": (
            "ASD Sustained Vit is built on a patented sustained-release technology that "
            "spreads the delivery of 20 essential vitamins and minerals throughout the "
            "day. The result is steadier energy, sharper focus and long-lasting "
            "wellness support — without the spikes of traditional multivitamins."
        ),
        "form": "Tablets",
        "dosage": "As directed by a healthcare professional.",
        "highlights": ["20 nutrients", "Patented sustained release", "All-day support"],
        "benefits": [
            "Supports a healthy pregnancy",
            "Improves bone health",
            "Provides continuous energy and supports metabolism throughout the day",
            "Supports immunity and vision",
            "Enhances hormonal balance and thyroid function",
            "Protects from anemia and enhances focus",
        ],
        "ingredients": [
            "Calcium 155.5 mg", "Phosphorous 120 mg", "Magnesium 120 mg",
            "Vitamin C 36 mg", "Iron 21 mg", "Beta-Carotene 7.5 mg",
            "Vitamin B3 7.25 mg", "Vitamin B5 4.81 mg", "Vitamin E 4.41 mg",
            "Zinc 3.6 mg", "Vitamin B6 1.2 mg", "Vitamin B1 0.6 mg",
            "Vitamin B2 0.6 mg", "Manganese 0.6 mg", "Copper 0.48 mg",
            "Folic Acid 400 µg", "Iodine 48 µg", "Selenium 30 mcg",
            "Vitamin D3 400 IU / 10 µg", "Vitamin B12 1.2 µg",
        ],
        "featured": True,
    },
    {
        "slug": "zinco-q10",
        "name": "Zinco Q10",
        "tagline": "Dual antioxidant defense in a single capsule.",
        "category": "Antioxidants & Minerals",
        "image": "ZincoQ10_v2.png",
        "short": "A patent formula combining Zinc with Coenzyme Q10 — a dual antioxidant defense system that supports cellular energy and overall wellness.",
        "long": (
            "Zinco Q10 brings together two of the most important antioxidants in human "
            "biology — Zinc and Coenzyme Q10 — in a single, easy-to-take capsule. The "
            "combination supports immunity, fertility, hormonal balance and exercise "
            "performance. Available in capsules — 30 per pack."
        ),
        "form": "Capsules — 30 per pack",
        "dosage": "One tablet twice daily, or as directed by your doctor.",
        "highlights": ["Patent formula", "Dual antioxidant", "Cellular energy"],
        "benefits": [
            "Immunity booster",
            "Supports male and female fertility",
            "Hormone-level regulation without side effects",
            "Supports heart health and diabetes management",
            "Promotes healthy skin aging, wound healing, and reduces headaches",
            "Supports exercise performance",
        ],
        "ingredients": ["Zinc Citrate 25 mg", "Coenzyme Q10 100 mg"],
        "featured": True,
    },
    {
        "slug": "asd-carniplex",
        "name": "ASD Carniplex",
        "tagline": "600 mg of L-Carnitine for energy and metabolism.",
        "category": "Specialty Supplement",
        "image": "ASDCarneplex.png",
        "short": "A premium supplement featuring 600 mg of L-Carnitine per capsule for energy production, fertility support and recovery.",
        "long": (
            "L-Carnitine plays a central role in cellular energy production and the "
            "metabolism of fatty acids. ASD Carniplex delivers 600 mg per capsule — a "
            "potent dose for fertility support, fatigue management, weight management "
            "and post-exercise recovery."
        ),
        "form": "Capsules",
        "dosage": "As directed by a healthcare professional.",
        "highlights": ["600 mg L-Carnitine", "Energy & metabolism", "Recovery"],
        "benefits": [
            "Supports fertility in men by increasing sperm motility and morphology",
            "Supports fertility in women by improving oocyte (ova) quality",
            "Helps manage chronic fatigue and improve overall wellness",
            "Improves post-viral fatigue",
            "Supports weight management",
            "Enhances lipid profile for hyperlipidemic patients",
            "Boosts stamina and reduces post-exercise fatigue",
        ],
        "ingredients": ["L-Carnitine 600 mg"],
        "featured": False,
    },
    {
        "slug": "inpro",
        "name": "INPRO",
        "tagline": "Lactoferrin + Hyaluronic Acid suppository.",
        "category": "Specialty Supplement",
        "image": "Inpro.png",
        "short": "A rectal suppository combining Lactoferrin and Hyaluronic Acid — systemic antibacterial and anti-inflammatory action for anorectal and pelvic conditions.",
        "long": (
            "INPRO combines Lactoferrin and Hyaluronic Acid in a rectal suppository "
            "with systemic antibacterial and anti-inflammatory action. It is suitable "
            "for both male and female patients across a range of anorectal and pelvic "
            "conditions. Available in two pack sizes — 10 and 20 suppositories."
        ),
        "form": "Rectal suppositories — packs of 10 or 20",
        "dosage": "1 to 2 suppositories daily, or as directed by a doctor.",
        "highlights": ["Lactoferrin", "Hyaluronic Acid", "Dual action"],
        "benefits": [
            "An effective choice for hemorrhoids, anorectal diseases and constipation",
            "For males: chronic prostatitis, chronic pelvic-pain syndrome, bacterial infections",
            "For females: chronic pelvic-pain syndrome, cystitis, vaginitis and other infectious diseases",
            "Dual antibacterial and anti-inflammatory systemic action",
            "Suitable for both male and female patients",
        ],
        "ingredients": [
            "Lactoferrin (rectal suppository)",
            "Hyaluronic Acid (rectal suppository)",
        ],
        "featured": True,
    },
    {
        "slug": "asd-semifer-10mg",
        "name": "ASD Semifer 10 mg",
        "tagline": "Liposomal iron for the youngest patients.",
        "category": "Iron Supplement",
        "image": "ASDSemifer10.png",
        "short": "10 mg liposomal iron formulated for preterm infants, infants and young children below three years of age.",
        "long": (
            "ASD Semifer 10 mg is designed for preterm infants, infants and young "
            "children below three years old. It is indicated for the treatment and "
            "prevention of iron-deficiency anemia in preterm infants, exclusively "
            "breastfed babies, infants in rapid-growth phases and children with low "
            "dietary iron intake."
        ),
        "form": "Liposomal iron — 10 mg per 8 ml vial",
        "dosage": "Infants 6 months–1 year: 1 vial daily. Children 1–3 years: 1–2 vials daily.",
        "highlights": ["Liposomal", "Pediatric (under 3y)", "Preterm-friendly"],
        "benefits": [
            "Reduction of tiredness and fatigue",
            "Support of normal immune-system function",
            "Normal formation of red blood cells and hemoglobin",
            "Support of normal cognitive development",
            "Contribution to normal energy-yielding metabolism",
        ],
        "ingredients": ["Liposomal Iron 10 mg per 8 ml vial"],
        "featured": False,
    },
    {
        "slug": "asd-semifer-14mg",
        "name": "ASD Semifer 14 mg",
        "tagline": "Liposomal iron for children and adolescents.",
        "category": "Iron Supplement",
        "image": "ASDSemifer14.png",
        "short": "14 mg liposomal iron for children from three years old and adolescents — for the treatment and prevention of iron deficiency.",
        "long": (
            "ASD Semifer 14 mg is formulated for children from three years old and "
            "adolescents, for the treatment and prevention of iron deficiency and "
            "iron-deficiency anemia."
        ),
        "form": "Liposomal iron — 14 mg per 10 ml vial",
        "dosage": "1 to 2 vials daily depending on individual needs.",
        "highlights": ["Liposomal", "Children 3y+", "Adolescents"],
        "benefits": [
            "Reduction of tiredness and fatigue",
            "Support of normal immune-system function",
            "Formation of red blood cells and hemoglobin",
            "Support of normal cognitive function",
            "Contribution to normal energy-yielding metabolism",
        ],
        "ingredients": ["Liposomal Iron 14 mg per 10 ml vial"],
        "featured": False,
    },
    {
        "slug": "asd-semifer-40mg",
        "name": "ASD Semifer 40 mg",
        "tagline": "Liposomal iron for adults — including pregnancy and athletes.",
        "category": "Iron Supplement",
        "image": "ASDSemifer40.png",
        "short": "40 mg liposomal iron for adults, including pregnant women, athletes, and individuals with low dietary intake such as vegetarians.",
        "long": (
            "ASD Semifer 40 mg is the adult dose in the Semifer range — designed for "
            "the prevention and treatment of iron-deficiency anemia in adults, "
            "especially those with increased iron needs (pregnancy, athletes) or low "
            "dietary intake (vegetarians)."
        ),
        "form": "Liposomal iron — 40 mg per 10 ml vial",
        "dosage": "1 to 2 vials daily for adults.",
        "highlights": ["Liposomal", "High dose", "Adults"],
        "benefits": [
            "Reduction of tiredness and fatigue",
            "Normal immune-system function",
            "Formation of red blood cells and hemoglobin",
            "Support of normal cognitive and metabolic function",
        ],
        "ingredients": ["Liposomal Iron 40 mg per 10 ml vial"],
        "featured": False,
    },
    {
        "slug": "asd-chelazen",
        "name": "ASD Chelazen",
        "tagline": "Iron bisglycinate, with chelation and nanotechnology.",
        "category": "Iron Supplement",
        "image": "ASDChelazen.png",
        "short": "A premium iron-bisglycinate supplement using chelation and nanotechnology — superior absorption, gentle on the digestive system.",
        "long": (
            "Iron bisglycinate is a chelated form of iron known for its superior "
            "absorption and gentle impact on the digestive system. ASD Chelazen pairs "
            "this with nanotechnology to maximise bioavailability while minimising GI "
            "side effects. Each capsule delivers 20 mg of iron bisglycinate, making it "
            "ideal for patients sensitive to traditional iron supplements."
        ),
        "form": "Capsules — 20 mg iron bisglycinate per capsule",
        "dosage": "1 capsule twice daily, or as recommended by your physician.",
        "highlights": ["Iron bisglycinate", "Chelated", "Nano-technology"],
        "benefits": [
            "Maximises bioavailability and efficacy via iron chelation and nanotechnology",
            "Enhanced tolerability — ideal for gastric-sensitive patients",
            "Reduces side effects of nausea, gastric upset and constipation",
            "Bisglycinate protects iron from gastric food interaction",
            "Supports immunity and reduces fatigue caused by iron-deficiency anemia (IDA)",
        ],
        "ingredients": ["Iron Bisglycinate (as iron) 20 mg"],
        "featured": False,
    },
    {
        "slug": "asd-magneflex",
        "name": "ASD Magneflex",
        "tagline": "Magnesium glycerophosphate — a flexible dose for every age.",
        "category": "Minerals",
        "image": "ASDMagneflex.png",
        "short": "The only magnesium supplement in the UAE delivering 4 mmol (97 mg) of elemental magnesium per capsule, as magnesium glycerophosphate.",
        "long": (
            "ASD Magneflex delivers magnesium as glycerophosphate — a gentle, well-"
            "absorbed magnesium salt that achieves high bioavailability within 2–3 "
            "hours. Each capsule provides 4 mmol (97 mg) of elemental magnesium, "
            "making it suitable for both children and adults. Free from artificial "
            "colours and gluten."
        ),
        "form": "Capsules — 4 mmol (97 mg) elemental Mg",
        "dosage": "Adults: 1 capsule three times daily. Children: 1 capsule twice daily.",
        "highlights": ["Glycerophosphate", "Flexible dose", "Gluten-free"],
        "benefits": [
            "Muscle: reduces cramps, spasms and muscle twitching",
            "Energy: supports energy levels and reduces tiredness",
            "Bones: supports bone health by assisting proper calcium utilisation",
            "Migraine: helps reduce migraine frequency",
            "Sleep & anxiety: helps enhance quality of sleep and reduce anxiety",
            "Safe: free from artificial colours and gluten",
        ],
        "ingredients": ["Magnesium Glycerophosphate 97 mg elemental Mg (4 mmol)"],
        "featured": False,
    },
]

CATEGORIES = []
for p in PRODUCTS:
    if p["category"] not in CATEGORIES:
        CATEGORIES.append(p["category"])


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

def header(active, base=""):
    return dedent(f"""\
    <header class="site-header">
      <div class="container nav">
        <a href="{base}index.html" class="brand" aria-label="ASD International home">
          <img src="{base}assets/img/asd-logo.png" alt="ASD International" />
          <span class="brand-text">
            <strong>ASD International</strong>
            <span>Innovation for your health</span>
          </span>
        </a>
        <nav data-nav>
          <ul class="nav-links">
            <li><a href="{base}index.html">Home</a></li>
            <li><a href="{base}products.html">Products</a></li>
            <li><a href="{base}about.html">About</a></li>
            <li><a href="{base}partners.html">Partners</a></li>
            <li><a href="{base}contact.html">Contact</a></li>
          </ul>
        </nav>
        <div class="nav-cta">
          <a class="icon-link" href="https://www.linkedin.com/company/asd-international-medical-requisites" target="_blank" rel="noopener" aria-label="LinkedIn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>
          </a>
          <a class="btn btn-red btn-sm" href="{base}contact.html">Get in touch</a>
          <button class="menu-btn" data-menu-btn aria-label="Open menu" aria-expanded="false">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/></svg>
          </button>
        </div>
      </div>
      <div class="mobile-panel" data-mobile-panel>
        <ul>
          <li><a href="{base}index.html">Home</a></li>
          <li><a href="{base}products.html">Products</a></li>
          <li><a href="{base}about.html">About</a></li>
          <li><a href="{base}partners.html">Partners</a></li>
          <li><a href="{base}contact.html">Contact</a></li>
        </ul>
      </div>
    </header>
    """)


def footer(base=""):
    return dedent(f"""\
    <footer class="site-footer footer">
      <div class="container footer-top">
        <div class="footer-brand">
          <img src="{base}assets/img/asd-logo.png" alt="ASD International" />
          <p class="footer-tag">Innovation for your health</p>
          <p class="footer-desc">ASD International is committed to advancing human health through science-backed, pharmaceutical-grade nutritional supplements.</p>
        </div>
        <div>
          <h4>Company</h4>
          <ul>
            <li><a href="{base}index.html">Home</a></li>
            <li><a href="{base}about.html">About us</a></li>
            <li><a href="{base}partners.html">Partners</a></li>
            <li><a href="{base}contact.html">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>Products</h4>
          <ul>
            <li><a href="{base}products/asd-iron.html">ASD Iron</a></li>
            <li><a href="{base}products/asd-magnesium.html">ASD Magnesium</a></li>
            <li><a href="{base}products/asd-sustained-vit.html">ASD Sustained Vit</a></li>
            <li><a href="{base}products/zinco-q10.html">Zinco Q10</a></li>
            <li><a href="{base}products/asd-carniplex.html">ASD Carniplex</a></li>
            <li><a href="{base}products/asd-magneflex.html">ASD Magneflex</a></li>
          </ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul class="footer-contact">
            <li>
              <svg class="ico" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              <a href="tel:+97122459549">+971 2 245 9549</a>
            </li>
            <li>
              <svg class="ico" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.99 5.73a2 2 0 0 1-2.02 0L2 7"/></svg>
              <a href="mailto:info@asdinternational.co">info@asdinternational.co</a>
            </li>
            <li>
              <svg class="ico" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 4.99-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 14.99 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>
              <span>Block 2-Store No.3, ICAD III,<br/>Abu Dhabi, UAE</span>
            </li>
          </ul>
        </div>
      </div>
      <div class="container">
        <div class="footer-bottom">
          <p>© <span data-year>2026</span> ASD International Medical Requisites LLC. All rights reserved.</p>
          <div class="social-row">
            <a href="https://www.linkedin.com/company/asd-international-medical-requisites" target="_blank" rel="noopener" aria-label="LinkedIn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>
            </a>
            <a href="mailto:info@asdinternational.co" aria-label="Email">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.99 5.73a2 2 0 0 1-2.02 0L2 7"/></svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
    """)


def page(title, description, body_html, base="", extra_head=""):
    return dedent(f"""\
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>{title}</title>
      <meta name="description" content="{description}" />
      <link rel="icon" href="{base}assets/img/favicon.png" type="image/png" />
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
      <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <link rel="stylesheet" href="{base}assets/css/site.css" />
      {extra_head}
    </head>
    <body>
    {body_html}
    <script src="{base}assets/js/site.js"></script>
    </body>
    </html>
    """)


# Reusable arrow SVG snippet
ARROW = '<svg class="arrow" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def page_about():
    body = header("about") + dedent(f"""\
    <main>
      <section class="page-head">
        <div class="container">
          <p class="crumb"><a href="index.html">Home</a><span class="sep">/</span>About</p>
          <h1>A medicine company that puts health above all.</h1>
          <p class="lead">ASD International is a UAE-based pharmaceutical company committed to advancing human health across the GCC and the Middle East.</p>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="split">
            <div class="split-image reveal">
              <img src="assets/img/quality-commitment.png" alt="ASD International — quality commitment" loading="lazy" />
            </div>
            <div class="split-text reveal">
              <span class="eyebrow eyebrow-red">Our story</span>
              <h2>From Abu Dhabi, for the region.</h2>
              <p class="lead">
                ASD International Medical Requisites LLC is a leading medical company
                based in the United Arab Emirates. Our headquarters in ICAD III, Abu
                Dhabi, gives us the manufacturing rigor and regulatory access to serve
                healthcare professionals across the UAE and the wider GCC.
              </p>
              <p>
                Our unwavering commitment to quality is what sets us apart. We believe
                that patients in our region deserve nothing but the best service and
                care — supplements engineered with the rigor of pharmaceuticals and
                the bioavailability of natural wellness.
              </p>
              <p>
                Every product in our portfolio is built on advanced delivery
                technology — chelation, sustained release, liposomal carriers and
                nanotechnology — designed to make every milligram count.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="red-band">
        <div class="container">
          <span class="eyebrow eyebrow-light">Our purpose</span>
          <p class="quote">"We unite scientific rigor with care for the patient — to make every dose work the way the body needs it to."</p>
          <p class="quote-attrib">
            ASD International
            <span class="role">Innovation for your health</span>
          </p>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="heading-block reveal">
            <div>
              <span class="eyebrow">What sets us apart</span>
              <h2>The science inside every ASD product.</h2>
            </div>
            <p class="lead">Six commitments that run through every formula in our portfolio — from the ingredients we source to the technology we use to deliver them.</p>
          </div>

          <div class="action-row" style="padding:0;">
            <div class="action-cell reveal">
              <h3>Liposomal delivery.</h3>
              <p>Lipid-based carriers protect active ingredients through digestion, dramatically improving absorption and tolerability — used in ASD Iron, ASD Magnesium and the Semifer range.</p>
            </div>
            <div class="action-cell reveal">
              <h3>Chelation.</h3>
              <p>Minerals bound to amino acids — like the iron bisglycinate in ASD Chelazen — for superior bioavailability and gentler GI tolerance.</p>
            </div>
            <div class="action-cell reveal">
              <h3>Sustained release.</h3>
              <p>Patented technology that releases nutrients gradually over the course of the day — for steady energy, focus and wellness, as in ASD Sustained Vit.</p>
            </div>
            <div class="action-cell reveal">
              <h3>Nanotechnology.</h3>
              <p>Particle-size engineering that increases surface area and absorption efficiency, used across the ASD Iron and Chelazen formulations.</p>
            </div>
            <div class="action-cell reveal">
              <h3>Patent formulas.</h3>
              <p>Selected combinations — such as Zinco Q10 — are patent-protected formulas designed for synergistic action.</p>
            </div>
            <div class="action-cell reveal">
              <h3>Pharmaceutical-grade.</h3>
              <p>Sourced and verified at pharmaceutical standards, with batch-level traceability and rigorous quality control.</p>
            </div>
          </div>
        </div>
      </section>

      <section class="section bleed-grey">
        <div class="container">
          <div class="split reverse">
            <div class="split-image reveal">
              <img src="assets/img/ASDSustainedVit.png" alt="ASD Sustained Vit" loading="lazy" style="object-fit:contain;background:#F0EDE8;padding:3rem;" />
            </div>
            <div class="split-text reveal">
              <span class="eyebrow eyebrow-red">Our portfolio</span>
              <h2>Eleven products. One standard.</h2>
              <p class="lead">A focused portfolio of pharmaceutical-grade nutritional supplements — for energy, immunity, fertility, recovery and pediatric care.</p>
              <a class="link-arrow mt-2" href="products.html">Explore products {ARROW}</a>
            </div>
          </div>
        </div>
      </section>
    </main>
    """) + footer()
    return page(
        "About | ASD International",
        "ASD International is a UAE-based pharmaceutical company committed to advancing human health through science-backed nutritional supplements.",
        body,
    )


def page_partners():
    body = header("partners") + dedent(f"""\
    <main>
      <section class="page-head">
        <div class="container">
          <p class="crumb"><a href="index.html">Home</a><span class="sep">/</span>Partners</p>
          <h1>Bring ASD products to your market.</h1>
          <p class="lead">We work with pharmacies, hospital groups, distributors and clinical partners across the GCC and the Middle East.</p>
        </div>
      </section>

      <section class="section bleed-grey">
        <div class="container">
          <div class="heading-block reveal">
            <div>
              <span class="eyebrow">How we work together</span>
              <h2>Three ways to partner with ASD.</h2>
            </div>
            <p class="lead">Choose the relationship that fits your organisation — pharmacy, healthcare practice or regional distributor — and our team will guide you through the next steps.</p>
          </div>

          <div class="action-row" style="padding:0;">
            <div class="action-cell reveal">
              <div class="ico">
                <svg xmlns="http://www.w3.org/2000/svg" width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
              </div>
              <h3>Pharmacy networks.</h3>
              <p>Stocking, training and merchandising support for pharmacies across the UAE and the wider region — backed by clinical content for your pharmacists.</p>
              <a class="link-arrow" href="contact.html">Stock our products {ARROW}</a>
            </div>
            <div class="action-cell reveal">
              <div class="ico">
                <svg xmlns="http://www.w3.org/2000/svg" width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l3-9 4 18 3-9h4"/></svg>
              </div>
              <h3>Healthcare professionals.</h3>
              <p>Sample requests, scientific literature and direct support for prescribers and clinical teams looking to recommend ASD products.</p>
              <a class="link-arrow" href="contact.html">Request samples {ARROW}</a>
            </div>
            <div class="action-cell reveal">
              <div class="ico">
                <svg xmlns="http://www.w3.org/2000/svg" width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/></svg>
              </div>
              <h3>Regional distribution.</h3>
              <p>Looking to import ASD products into your country across the GCC or the Middle East? We can discuss exclusive and non-exclusive arrangements.</p>
              <a class="link-arrow" href="contact.html">Distribute ASD {ARROW}</a>
            </div>
          </div>
        </div>
      </section>

      <section class="red-band">
        <div class="container">
          <span class="eyebrow eyebrow-light">Why partner with ASD</span>
          <div class="red-band-grid">
            <div>
              <p class="quote">"Trusted by healthcare professionals across the UAE and the GCC — formulas designed to be felt, tolerated and recommended."</p>
            </div>
            <div class="red-band-side">
              <h3>What you get when you partner with us.</h3>
              <p>Pharmaceutical-grade products, clinical content for your team, regulatory support across GCC markets, and a direct line to our medical team for any patient question that comes up.</p>
              <a class="link-arrow on-red" href="contact.html">Start a conversation {ARROW}</a>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="split">
            <div class="split-image reveal">
              <img src="assets/img/quality-commitment.png" alt="ASD International quality" loading="lazy" />
            </div>
            <div class="split-text reveal">
              <span class="eyebrow eyebrow-red">Next steps</span>
              <h2>Tell us about your market.</h2>
              <p class="lead">Share your channels, your country and the products you'd like to carry. Our team will respond within two business days with a tailored proposal.</p>
              <a class="link-arrow mt-2" href="contact.html">Get in touch {ARROW}</a>
            </div>
          </div>
        </div>
      </section>
    </main>
    """) + footer()
    return page(
        "Partners | ASD International",
        "Partner with ASD International — pharmacy networks, healthcare professionals and regional distribution across the GCC and the Middle East.",
        body,
    )


def page_contact():
    body = header("contact") + dedent(f"""\
    <main>
      <section class="page-head">
        <div class="container">
          <p class="crumb"><a href="index.html">Home</a><span class="sep">/</span>Contact</p>
          <h1>Let's connect.</h1>
          <p class="lead">Whether you're a healthcare professional, a potential partner, or simply have a question about our products — we're here to help.</p>
        </div>
      </section>

      <section class="section">
        <div class="container contact-grid">
          <div class="reveal">
            <div class="info-stack">
              <span class="eyebrow eyebrow-red">Get in touch</span>
              <h3>Contact information</h3>
              <p class="muted">Our dedicated team is available Monday through Friday, 9:00 AM to 5:00 PM (GST).</p>
              <div class="rule"></div>
              <ul class="info-list">
                <li>
                  <span class="ico">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                  </span>
                  <div><strong>Phone</strong><div class="info-val"><a href="tel:+97122459549">+971 2 245 9549</a></div></div>
                </li>
                <li>
                  <span class="ico">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.99 5.73a2 2 0 0 1-2.02 0L2 7"/></svg>
                  </span>
                  <div><strong>Email</strong><div class="info-val"><a href="mailto:info@asdinternational.co">info@asdinternational.co</a></div></div>
                </li>
                <li>
                  <span class="ico">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 4.99-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 14.99 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  </span>
                  <div><strong>Headquarters</strong>
                    <div class="info-val">Block 2 — Store No. 3<br/>Abu Dhabi Industrial City — ICAD III<br/>Abu Dhabi, United Arab Emirates</div>
                  </div>
                </li>
                <li>
                  <span class="ico">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>
                  </span>
                  <div><strong>LinkedIn</strong>
                    <div class="info-val"><a href="https://www.linkedin.com/company/asd-international-medical-requisites" target="_blank" rel="noopener">ASD International Medical Requisites</a></div>
                  </div>
                </li>
              </ul>
              <div class="map-frame">
                <iframe
                  src="https://maps.google.com/maps?q=ASD%20International%20Medical%20Requisites%20LLC&t=&z=15&ie=UTF8&iwloc=&output=embed"
                  loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"
                  title="ASD International on Google Maps"></iframe>
              </div>
            </div>
          </div>

          <div class="reveal">
            <div class="form-stack">
              <span class="eyebrow eyebrow-red">Send a message</span>
              <h3>How can we help?</h3>
              <p class="muted">Tell us a little about you and we'll get back to you within two business days.</p>
              <form data-contact-form novalidate>
                <div class="form-row cols-2">
                  <div class="form-field">
                    <label for="name">Full name</label>
                    <input id="name" name="name" type="text" required autocomplete="name" />
                  </div>
                  <div class="form-field">
                    <label for="email">Email</label>
                    <input id="email" name="email" type="email" required autocomplete="email" />
                  </div>
                </div>
                <div class="form-row cols-2">
                  <div class="form-field">
                    <label for="phone">Phone (optional)</label>
                    <input id="phone" name="phone" type="tel" autocomplete="tel" />
                  </div>
                  <div class="form-field">
                    <label for="subject">Subject</label>
                    <select id="subject" name="subject">
                      <option>General inquiry</option>
                      <option>Product information</option>
                      <option>Partnership / distribution</option>
                      <option>Healthcare professional</option>
                      <option>Press / media</option>
                    </select>
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-field">
                    <label for="message">Message</label>
                    <textarea id="message" name="message" required placeholder="How can we help?"></textarea>
                  </div>
                </div>
                <button class="btn btn-red btn-lg mt-2" type="submit">
                  Send message {ARROW}
                </button>
                <p class="form-note">By sending this message you agree to be contacted by ASD International. We do not share your information with third parties.</p>
                <div class="form-success" data-form-success>Thanks — your message is ready in your email client. We'll be in touch shortly.</div>
              </form>
            </div>
          </div>
        </div>
      </section>
    </main>
    """) + footer()
    return page(
        "Contact | ASD International",
        "Get in touch with ASD International for product inquiries, distribution opportunities and partnerships.",
        body,
    )


def page_products_index():
    thumbs_html_parts = []
    for p in PRODUCTS:
        thumbs_html_parts.append(dedent(f"""\
          <a class="thumb reveal" href="products/{p['slug']}.html" data-category="{p['category']}">
            <div class="thumb-img"><img src="assets/img/{p['image']}" alt="{p['name']}" loading="lazy" /></div>
            <p class="thumb-cat">{p['category']}</p>
            <h3 class="thumb-label">{p['name']}</h3>
            <span class="thumb-link">Explore product →</span>
          </a>
        """))
    thumbs_html = ''.join(thumbs_html_parts)

    filters_html = '<button class="chip-filter active" data-filter="all">All products</button>\n'
    for c in CATEGORIES:
        filters_html += f'        <button class="chip-filter" data-filter="{c}">{c}</button>\n'

    body = header("products") + dedent(f"""\
    <main>
      <section class="page-head">
        <div class="container">
          <p class="crumb"><a href="index.html">Home</a><span class="sep">/</span>Products</p>
          <h1>Eleven products. One standard.</h1>
          <p class="lead">Pharmaceutical-grade nutritional supplements — engineered with advanced delivery systems for absorption you can feel.</p>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="filter-bar reveal">
        {filters_html}      </div>

          <div class="thumb-grid" data-product-grid>
        {thumbs_html}      </div>
        </div>
      </section>

      <section class="red-band">
        <div class="container">
          <div class="red-band-grid">
            <div>
              <p class="quote">"Need help matching a product to a patient profile, condition or stage of life?"</p>
            </div>
            <div class="red-band-side">
              <h3>Talk to our medical team.</h3>
              <p>Our team can guide you through the portfolio, answer formulation questions, and direct you to the right ASD product for the case in front of you.</p>
              <a class="link-arrow on-red" href="contact.html">Get in touch {ARROW}</a>
            </div>
          </div>
        </div>
      </section>
    </main>
    """) + footer()
    return page(
        "Products | ASD International",
        "Explore the ASD International product portfolio — 11 pharmaceutical-grade nutritional supplements across iron, magnesium, vitamins and specialty care.",
        body,
    )


def page_product_detail(p):
    benefits_html = '\n'.join(f'        <li>{b}</li>' for b in p['benefits'])
    ingredients_html = '\n'.join(f'        <li>{i}</li>' for i in p['ingredients'])
    highlights_html = ''.join(f'<span>{h}</span>' for h in p['highlights'])

    related = [r for r in PRODUCTS if r['slug'] != p['slug'] and r['category'] == p['category']][:4]
    if len(related) < 4:
        for r in PRODUCTS:
            if r['slug'] != p['slug'] and r not in related:
                related.append(r)
            if len(related) == 4:
                break

    related_thumbs = []
    for r in related:
        related_thumbs.append(dedent(f"""\
        <a class="thumb reveal" href="{r['slug']}.html">
          <div class="thumb-img"><img src="../assets/img/{r['image']}" alt="{r['name']}" loading="lazy" /></div>
          <p class="thumb-cat">{r['category']}</p>
          <h3 class="thumb-label">{r['name']}</h3>
          <span class="thumb-link">Explore product →</span>
        </a>
        """))

    body = header(f"product:{p['slug']}", base="../") + dedent(f"""\
    <main>
      <section class="page-head">
        <div class="container">
          <p class="crumb"><a href="../index.html">Home</a><span class="sep">/</span><a href="../products.html">Products</a><span class="sep">/</span>{p['name']}</p>
          <span class="eyebrow eyebrow-red">{p['category']}</span>
          <h1>{p['name']}</h1>
          <p class="lead">{p['tagline']}</p>
        </div>
      </section>

      <section class="section">
        <div class="container product-detail">
          <div class="reveal">
            <div class="product-hero-img">
              <img src="../assets/img/{p['image']}" alt="{p['name']}" />
            </div>
          </div>

          <div class="reveal">
            <div class="highlights">{highlights_html}</div>
            <h2>{p['tagline']}</h2>
            <p class="lead mt-3">{p['short']}</p>
            <p>{p['long']}</p>

            <div class="spec-grid">
              <div class="spec">
                <h4>Form &amp; pack</h4>
                <p class="value">{p['form']}</p>
              </div>
              <div class="spec">
                <h4>Dosage</h4>
                <p class="value">{p['dosage']}</p>
              </div>
            </div>

            <div class="list-block">
              <h3>Key benefits</h3>
              <ul class="bullet-list">
        {benefits_html}
              </ul>
            </div>

            <div class="list-block">
              <h3>Composition</h3>
              <ul class="bullet-list dots">
        {ingredients_html}
              </ul>
            </div>

            <div class="mt-6">
              <a class="btn btn-red btn-lg" href="../contact.html">Inquire about {p['name']} {ARROW}</a>
              <a class="link-arrow" href="../products.html" style="margin-left:1.5rem;">All products {ARROW}</a>
            </div>

            <p class="form-note mt-4">
              This information is for healthcare professionals and informational purposes
              only and is not a substitute for medical advice. Please consult a qualified
              healthcare provider before starting any supplement.
            </p>
          </div>
        </div>
      </section>

      <section class="section bleed-grey">
        <div class="container">
          <div class="heading-block reveal">
            <div>
              <span class="eyebrow">More from our portfolio</span>
              <h2>You may also be interested in.</h2>
            </div>
            <p class="lead">Other ASD products in adjacent categories — for related conditions, life stages or use-cases.</p>
          </div>
          <div class="thumb-grid">
        {''.join(related_thumbs)}      </div>
        </div>
      </section>
    </main>
    """) + footer(base="../")

    return page(
        f"{p['name']} | ASD International",
        p['short'],
        body,
        base="../",
    )


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {path}")


def main():
    print("Building ASD International site (Lilly-style)...")
    write("about.html",    page_about())
    write("partners.html", page_partners())
    write("contact.html",  page_contact())
    write("products.html", page_products_index())
    for p in PRODUCTS:
        write(f"products/{p['slug']}.html", page_product_detail(p))
    print(f"Done — {len(PRODUCTS)} product pages + 4 main pages.")


if __name__ == "__main__":
    main()
