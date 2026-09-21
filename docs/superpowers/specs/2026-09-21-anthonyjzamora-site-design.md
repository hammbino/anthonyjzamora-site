# anthonyjzamora.com — Site Design Spec

**Date:** 2026-09-21
**Status:** Approved in conversation (Jeffrey), pending Anthony's review of the prototype
**Final platform:** Squarespace (domain already registered there, currently showing "Coming Soon")
**This phase:** static HTML prototype hosted on GitHub Pages for Anthony's review

## 1. Who and why

Anthony J. Zamora — Registered Dietitian and trained chef (BU Professional Culinary
Arts 2016; dietetics/performance nutrition, Tennessee). Team chef / performance
nutrition assistant with the St. Louis Rams; hired by the Utah Jazz in 2018 as team
chef; became VP of Nutrition, Culinary & Hospitality at Smith Entertainment Group
(Jazz, Utah Hockey Club). Now independent: "Fed NFL, NBA, NHL athletes for 12 years.
Now teaching what the pros know."

Founder of **I Got More Co. LLC** (@igotmoreco) — "Built for those who don't settle.
Culture. Community. Creation."

**Goal of the site:** win clients now (1:1, teams, speaking, recipes/meal plans) and
seed the "branch out" (newsletter/audience, course, cookbook) without padding.

**Brand decision:** the site is *Anthony J. Zamora the person*; I Got More Co. is a
company he offers, featured in its own section (later its own page), not the
header logo.

## 2. References

- danchurchill.com — the brand/content model (hero tagline, about, newsletter,
  book, credentials, press bar). Black/white, big photography, whitespace.
- christinaychu.com — the services/lead-gen model (services nav, testimonials,
  contact). Squarespace; proves the look is reproducible there.

Chosen approach: **credentials-first** (approach A). Hero leads with the 12-years-
with-pros story because nobody else in his market has it.

## 3. Page structure (Home, single scrolling page)

1. **Header** — "Anthony J. Zamora" wordmark; nav: About · Services · I Got More Co.
   · Recipes · Contact; "Work With Me" button.
2. **Hero** — full-width photo. H1: "Twelve years fueling NFL, NBA & NHL athletes.
   Now I'll teach you what the pros know." Sub: Registered Dietitian · Chef · Former
   VP of Nutrition, Culinary & Hospitality, Utah Jazz / Utah Hockey Club. CTAs:
   Work With Me (→ Contact), See How I Work (→ Services).
3. **Trust bar** — Utah Jazz · Utah Hockey Club · St. Louis Rams · Smith
   Entertainment Group · Boston University · Deseret News · NBA.com. Text-only in
   prototype.
4. **About (short)** — Rams → Jazz → VP arc; "stealthy-healthy"; pull-quote "You
   wouldn't put 85 octane into a Ferrari."; rookie cooking classes / grocery tours /
   summer visits as proof he already teaches.
5. **Services** — four cards, each with promise + who it's for + button to Contact:
   - 1:1 Performance Nutrition
   - Team & Organization Consulting (visiting-team hospitality program that
     generated $170K+ in year one; designed the NHL practice-facility kitchen)
   - Speaking & Workshops (keynote, inaugural Performance Chef Summit, New Orleans;
     Culinary Nutrition Workshop)
   - Recipes & Meal Plans (links to Instagram until a recipe page exists)
6. **I Got More Co.** — banded section with script logo, his tagline, one paragraph,
   one CTA.
7. **Testimonials** — three cards, bracketed placeholders. No invented quotes.
8. **Newsletter** — email capture; copy: "what the pros know, weekly". Mock form.
9. **Contact** — name, email, interest dropdown (four services), message. Mock form.
10. **Footer** — nav repeat, Instagram (@anthonyjzamora, @igotmoreco), LinkedIn,
    © Anthony J. Zamora, RD.

Subpages (About, Services, Contact) are anchor sections in the prototype; real
pages in Squarespace.

## 4. Visual direction (matches I Got More Co. brand)

Sampled from @igotmoreco posts:

| Token | Hex | Use |
|---|---|---|
| Cream | `#F6F1EC` | page background |
| Sand | `#EAE2D9` | alternate section bands |
| Ink | `#0B0A08` | text, buttons |
| Gold-taupe | `#A8917A` | thin rules, borders, button hover — decorative only (2.7:1 on cream, fails AA for text) |
| Gold-taupe text | `#6E5946` | small-caps labels, captions, form labels, cites (5.9:1 on cream, 5.2:1 on sand) |

- Headlines: elegant serif (Cormorant Garamond / Playfair Display — Squarespace has
  both). Labels: wide-tracked uppercase sans (Montserrat). Body: clean sans.
- The "I Got More" script logotype is used as an image, never imitated in type.
- Tone: "private chef to the pros" — quiet, premium, editorial. Photos get room;
  minimal overlay text.
- No green, no neon, no stock photography. Empty slots stay as labeled placeholders.
- Layout: ~1100px content column, generous whitespace, cream/white/sand rhythm.
  Mobile stacks to one column; nav collapses.

## 5. Content sources and placeholders

Everything Anthony has already posted publicly on Instagram or that appears in
press is fair to use in the prototype; he reviews before anything goes live.

Sources: IG bios (@anthonyjzamora, @igotmoreco), Deseret News (2019), NBA.com/Jazz,
Spiceology interview, BU Gastronomy spotlight (Apr 2025), ASPDA mentor listing,
LinkedIn headline.

Placeholders, visibly bracketed: testimonials, pricing (none shown), forms (mock),
photos (screenshot captures from IG in `assets/ig/`, to be swapped from Anthony's
folder), logo (captures in `assets/brand/`, need real SVG/PNG).

Still needed from Anthony (none block the prototype): testimonials, logo files,
hi-res photos, hero headshot preference, final service names.

## 6. Prototype deliverable

- `index.html` at repo root, self-contained (inline CSS, no build, no framework),
  Google Fonts for the typefaces Squarespace offers.
- Assets under `assets/`.
- Hosted on GitHub Pages from `main` so Anthony gets a stable URL that does not
  depend on Jeffrey's machine.
- Tested: desktop and ~400px width render; every nav link lands on its section; no
  console errors; every placeholder bracketed.
- Out of scope: working forms/newsletter, recipe page, subpage routing, SEO/meta
  polish — Squarespace phase.

## 7. Next phase (after Anthony approves)

Rebuild in Squarespace: choose template, set Site Styles from the palette, build
sections, wire form + newsletter blocks, connect the domain (already there), then
Anthony replaces placeholder photos and testimonials.
