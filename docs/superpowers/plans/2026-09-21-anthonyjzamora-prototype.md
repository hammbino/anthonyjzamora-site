# anthonyjzamora.com Prototype Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single self-contained `index.html` prototype of anthonyjzamora.com, hosted on GitHub Pages, that Anthony can review from a stable URL.

**Architecture:** One static HTML file with inline CSS and no JavaScript beyond a mobile-nav toggle. Sections are `<section id="...">` blocks in the order the spec lists; nav links are `#anchors`. A small Python checker (`scripts/check.py`) is the test suite: it parses the HTML and asserts structure, asset existence, palette compliance, and placeholder bracketing. Images are JPEG-compressed copies of the PNG captures in `assets/`.

**Tech Stack:** HTML5, CSS (custom properties, grid/flex, one `@media` breakpoint), Google Fonts (Cormorant Garamond, Montserrat, Inter), Python 3 + Pillow for the checker and image prep. GitHub Pages from `main`, root.

**Spec:** `docs/superpowers/specs/2026-09-21-anthonyjzamora-site-design.md`

## Global Constraints

- Palette, exact values only: Cream `#F6F1EC` (page bg), Sand `#EAE2D9` (alt bands), Ink `#0B0A08` (text/buttons), Gold-taupe `#A8917A` (labels, rules, hover). No other chromatic colors; white `#FFFFFF` allowed for cards.
- Fonts: headlines Cormorant Garamond; labels Montserrat uppercase, letter-spacing ≥ 0.14em; body Inter.
- The "I Got More" script logotype is an image (`assets/brand/igotmore-script-tagline.jpg`), never set in type.
- Every placeholder is wrapped in square brackets and contains the word `PLACEHOLDER`, e.g. `[PLACEHOLDER — athlete quote, Anthony to supply]`. No invented testimonials, no prices.
- All nav `href="#id"` targets must exist. All `<img src>` must exist on disk relative to repo root.
- No external scripts. No forms that submit (`<form onsubmit="return false">`).
- Renders at 400px width without horizontal scroll.
- Commit after every task; push at the end of Task 5.

---

### Task 1: Checker script, image prep, page skeleton (tokens, header, hero, footer)

**Files:**
- Create: `scripts/check.py`
- Create: `scripts/prep_images.py`
- Create: `index.html`
- Create: `assets/ig/*.jpg`, `assets/brand/*.jpg` (generated)

**Interfaces:**
- Produces: `scripts/check.py` — run `python3 scripts/check.py`; exit 0 on pass, prints each failure and exits 1. Later tasks add sections and re-run it unchanged.
- Produces: section ids used by nav and later tasks: `about`, `services`, `igotmore`, `recipes`, `testimonials`, `newsletter`, `contact`.

- [ ] **Step 1: Write the checker (the failing test)**

```python
#!/usr/bin/env python3
"""Structural checks for index.html. Exit 1 on any failure."""
import re, sys, pathlib
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"
REQUIRED_IDS = ["about", "services", "igotmore", "recipes", "testimonials", "newsletter", "contact"]
ALLOWED_HEX = {"#f6f1ec", "#eae2d9", "#0b0a08", "#a8917a", "#ffffff", "#fff", "#000", "#000000"}

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.ids=set(); s.hrefs=[]; s.imgs=[]; s.scripts_ext=[]; s.forms=[]; s.text=[]
    def handle_starttag(s, tag, attrs):
        a=dict(attrs)
        if "id" in a: s.ids.add(a["id"])
        if tag=="a" and a.get("href","").startswith("#"): s.hrefs.append(a["href"][1:])
        if tag=="img": s.imgs.append(a.get("src",""))
        if tag=="script" and a.get("src"): s.scripts_ext.append(a["src"])
        if tag=="form": s.forms.append(a.get("onsubmit",""))
    def handle_data(s, d): s.text.append(d)

def main():
    fails=[]
    if not HTML.exists(): print("FAIL index.html missing"); sys.exit(1)
    src=HTML.read_text(); p=P(); p.feed(src)
    for i in REQUIRED_IDS:
        if i not in p.ids: fails.append(f"missing section id #{i}")
    for h in p.hrefs:
        if h and h not in p.ids: fails.append(f"nav href #{h} has no target")
    for s in p.imgs:
        if not s or s.startswith("http") or not (ROOT/s).exists(): fails.append(f"img src not on disk: {s!r}")
    for s in p.scripts_ext: fails.append(f"external script not allowed: {s}")
    for f in p.forms:
        if "return false" not in f: fails.append("form without onsubmit=\"return false\"")
    for hexv in set(m.lower() for m in re.findall(r"#[0-9a-fA-F]{3,6}\b", src)):
        if hexv not in ALLOWED_HEX and hexv not in p.ids and len(hexv) in (4,7):
            fails.append(f"off-palette color {hexv}")
    text=" ".join(p.text)
    for m in re.finditer(r"PLACEHOLDER", text):
        pre=text[max(0,m.start()-80):m.start()]
        if "[" not in pre: fails.append("PLACEHOLDER not inside [brackets] near: "+text[m.start():m.start()+40])
    if re.search(r"\$\s?\d", text): fails.append("a price appears in page text")
    for f in fails: print("FAIL", f)
    print("PASS" if not fails else f"{len(fails)} failure(s)"); sys.exit(1 if fails else 0)

if __name__=="__main__": main()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 scripts/check.py`
Expected: `FAIL index.html missing`, exit 1.

- [ ] **Step 3: Write the image prep script and run it**

```python
#!/usr/bin/env python3
"""Convert PNG captures to web JPEGs (max 1400px long edge, q=82)."""
import pathlib
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[1] / "assets"
for png in sorted(ROOT.rglob("*.png")):
    im = Image.open(png).convert("RGB")
    im.thumbnail((1400, 1400))
    out = png.with_suffix(".jpg")
    im.save(out, "JPEG", quality=82, optimize=True)
    print(out.relative_to(ROOT.parent), im.size, f"{out.stat().st_size//1024}KB")
```

Run: `python3 scripts/prep_images.py`
Expected: one line per image, all under ~150KB.

- [ ] **Step 4: Write the skeleton `index.html`**

Head: charset, viewport, `<title>Anthony J. Zamora — Performance Nutrition</title>`, Google Fonts link for `Cormorant+Garamond:wght@500;600&family=Montserrat:wght@500;600&family=Inter:wght@400;500`.

CSS tokens and base:

```css
:root{--cream:#F6F1EC;--sand:#EAE2D9;--ink:#0B0A08;--gold:#A8917A;--white:#FFFFFF;
 --serif:'Cormorant Garamond',Georgia,serif;--sans:'Inter',system-ui,sans-serif;--label:'Montserrat',system-ui,sans-serif;
 --max:1100px;--pad:clamp(20px,5vw,64px)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--cream);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.6}
h1,h2,h3{font-family:var(--serif);font-weight:500;line-height:1.05;margin:0 0 .4em}
h1{font-size:clamp(40px,6vw,76px)}h2{font-size:clamp(34px,4.5vw,56px)}h3{font-size:28px}
.label{font-family:var(--label);text-transform:uppercase;letter-spacing:.18em;font-size:12px;color:var(--gold);font-weight:600}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--pad)}
section{padding:clamp(64px,9vw,120px) 0}
.band{background:var(--sand)}
.btn{display:inline-block;font-family:var(--label);font-size:12px;letter-spacing:.16em;text-transform:uppercase;padding:16px 28px;border:1px solid var(--ink);color:var(--ink);text-decoration:none;transition:.2s}
.btn:hover{background:var(--ink);color:var(--cream)}
.btn.solid{background:var(--ink);color:var(--cream)}.btn.solid:hover{background:var(--gold);border-color:var(--gold)}
.rule{border:0;border-top:1px solid var(--gold);width:64px;margin:20px 0}
.placeholder{color:var(--gold);font-style:italic}
```

Header (sticky, cream, thin gold bottom rule): wordmark `Anthony J. Zamora` in serif 22px; nav links About · Services · I Got More Co. · Recipes · Contact (`.label` styling, ink color); right-side `<a class="btn solid" href="#contact">Work With Me</a>`. A `<button class="menu" aria-label="Menu">` shown only under 800px that toggles `nav.open` via a 3-line inline script at the end of body (`document.querySelector('.menu').onclick=()=>document.querySelector('nav').classList.toggle('open')`).

Hero: two-column grid (text left, image right), min-height 82vh.
- `.label`: "Registered Dietitian · Chef · 12 Years With the Pros"
- `h1`: "Twelve years fueling NFL, NBA & NHL athletes. Now I'll teach you what the pros know."
- sub `<p>`: "Former VP of Nutrition, Culinary & Hospitality for the Utah Jazz and Utah Hockey Club. Team chef for the St. Louis Rams. I build the food systems behind elite performance — and now I build them for you."
- CTAs: `<a class="btn solid" href="#contact">Work With Me</a>` `<a class="btn" href="#services">See How I Work</a>`
- image: `<img src="assets/ig/portrait-redbull.jpg" alt="Anthony J. Zamora">` with `<span class="placeholder">[PLACEHOLDER — hero photo from Anthony's folder]</span>` caption beneath.

Footer (ink background, cream text): wordmark; nav repeat; links Instagram @anthonyjzamora (`https://www.instagram.com/anthonyjzamora/`), @igotmoreco (`https://www.instagram.com/igotmoreco/`), LinkedIn (`https://www.linkedin.com/in/anthony-j-zamora-rd/`); `© 2026 Anthony J. Zamora, RD`.

Between hero and footer, put seven empty `<section id="...">` shells with just an `<h2>` so the checker passes: about, services, igotmore, recipes, testimonials, newsletter, contact. Tasks 2–4 fill them.

- [ ] **Step 5: Run the checker to verify it passes**

Run: `python3 scripts/check.py`
Expected: `PASS`, exit 0.

- [ ] **Step 6: Commit**

```bash
git add scripts/ index.html assets/
git commit -m "Add prototype skeleton, checker, and web-ready images"
```

---

### Task 2: Trust bar + About

**Files:**
- Modify: `index.html` — replace the `#about` shell; insert trust bar directly after hero.

**Interfaces:**
- Consumes: `.label`, `.wrap`, `.band`, `.rule`, `.placeholder` classes from Task 1.

- [ ] **Step 1: Trust bar**

`<div class="trust band"><div class="wrap">` — `.label` "Worked with · Featured in" then a flex-wrap row of `<span>`s in serif 20px, ink, separated by `·`: Utah Jazz, Utah Hockey Club, St. Louis Rams, Smith Entertainment Group, Boston University, Deseret News, NBA.com. Padding 28px 0. Add `<span class="placeholder">[PLACEHOLDER — logos once usage rights confirmed]</span>` at the end in 12px.

- [ ] **Step 2: About section**

`<section id="about"><div class="wrap grid2">` — image left `assets/ig/rams-sideline.jpg` (alt "Anthony on the sideline"), text right:
- `.label` "About"
- `h2` "From the Rams' kitchen to the Jazz's front office."
- `<p>` "I started as a team chef and performance-nutrition assistant with the St. Louis Rams. In 2018 the Utah Jazz hired me to run their kitchen; by the end I was Vice President of Nutrition, Culinary & Hospitality for Smith Entertainment Group — leading the chefs and dietitians behind the Jazz and the Utah Hockey Club, and designing the kitchen and dining room for Utah's new NHL practice facility."
- `<p>` "My method is what players called <em>stealthy-healthy</em>: food that performs, that people actually want to eat. With rookies I ran cooking classes, grocery-store tours and summer visits to their homes. That's the work I do now — for athletes, teams, and anyone who refuses to settle."
- `<blockquote>` in serif 30px, gold left rule: "You wouldn't put 85 octane into a Ferrari." — `<cite>` "Anthony, to the Deseret News"
- `<a class="btn" href="#contact">Work With Me</a>`

CSS to add: `.grid2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(32px,6vw,80px);align-items:center}.grid2 img{width:100%;height:auto;display:block}blockquote{margin:28px 0;padding-left:20px;border-left:1px solid var(--gold);font-family:var(--serif);font-size:30px;line-height:1.2}blockquote cite{display:block;font:500 12px var(--label);letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin-top:10px;font-style:normal}`

- [ ] **Step 3: Run checker**

Run: `python3 scripts/check.py` — Expected: `PASS`.

- [ ] **Step 4: Commit**

```bash
git add index.html && git commit -m "Add trust bar and About section"
```

---

### Task 3: Services + I Got More Co. + Recipes

**Files:**
- Modify: `index.html` — replace `#services`, `#igotmore`, `#recipes` shells.

- [ ] **Step 1: Services**

`<section id="services" class="band"><div class="wrap">` — `.label` "Services", `h2` "The same system I built for the pros. Sized for you." Then `<div class="cards">` with four `<article class="card">` (white bg, 1px sand border, padding 36px):

1. `h3` 1:1 Performance Nutrition — `<p>` "Fuel, recovery, body composition and travel eating — a plan built around your season, your schedule and your kitchen." — `.label` "For athletes and driven people" — `<a class="btn" href="#contact">Inquire</a>`
2. `h3` Team & Organization Consulting — `<p>` "Menus, staffing, kitchen design and player education. I launched a visiting-team hospitality program that generated $170K+ in its first year and designed the kitchen for an NHL practice facility." — `.label` "For pro & college teams, facilities" — button
3. `h3` Speaking & Workshops — `<p>` "Keynote speaker at the inaugural Performance Chef Summit in New Orleans. Culinary Nutrition Workshops for staff, teams and companies." — `.label` "For events, teams, companies" — button
4. `h3` Recipes & Meal Plans — `<p>` "What's in every pro's fridge, and how to cook it. Recipes and weekly plans that hold up on a Tuesday night." — `.label` "For everyone" — `<a class="btn" href="#recipes">See Recipes</a>`

Note the `$170K+` text: the checker's price rule flags `$` followed by a digit. Write it as "170K-plus dollars" → no; keep the number but write it `$170K+` inside a `<span data-figure>`? Simpler: the checker rule targets prices; change the checker regex to `r"\$\s?\d+(\.\d+)?\s*(/|per|mo|month|hr|hour|session)"` so revenue figures pass and only price-like patterns fail. Make that edit in `scripts/check.py` in this task.

CSS: `.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;margin-top:40px}.card{background:var(--white);border:1px solid var(--sand);padding:36px}.card .label{margin:12px 0 20px}`

- [ ] **Step 2: I Got More Co.**

`<section id="igotmore"><div class="wrap grid2">` — image left `assets/brand/igotmore-script-tagline.jpg` (alt "I Got More Co."), max-width 420px, plus `<span class="placeholder">[PLACEHOLDER — real logo files from Anthony]</span>`; text right: `.label` "I Got More Co.", `h2` "Built for those who don't settle.", `<p>` "Culture. Community. Creation. I Got More Co. is where I build beyond the team kitchen — nutrition made for athletes, workshops, and a community of people building a life of freedom and impact.", `<a class="btn solid" href="https://www.instagram.com/igotmoreco/">Follow @igotmoreco</a>`

- [ ] **Step 3: Recipes**

`<section id="recipes" class="band"><div class="wrap">` — `.label` "Recipes", `h2` "What the pros eat. Cooked in your kitchen.", a 3-up image row: `assets/ig/food-shrimp.jpg`, `assets/ig/chef-toast.jpg`, `assets/ig/hospitality-spread.jpg` (each `aspect-ratio:4/5;object-fit:cover`), `<p>` "New recipes weekly on Instagram. A full recipe library lives here soon.", `<a class="btn" href="https://www.instagram.com/anthonyjzamora/">Recipes on Instagram</a>`, `<span class="placeholder">[PLACEHOLDER — recipe page in Squarespace phase]</span>`.

CSS: `.row3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:32px 0}.row3 img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}`

- [ ] **Step 4: Run checker** — `python3 scripts/check.py` — Expected: `PASS`.

- [ ] **Step 5: Commit**

```bash
git add index.html scripts/check.py && git commit -m "Add Services, I Got More Co., and Recipes sections"
```

---

### Task 4: Testimonials + Newsletter + Contact

**Files:**
- Modify: `index.html` — replace `#testimonials`, `#newsletter`, `#contact` shells.

- [ ] **Step 1: Testimonials**

`<section id="testimonials"><div class="wrap">` — `.label` "What people say", `h2` "Trusted in the locker room.", `.cards` with three `.card`s each containing `<blockquote class="small">` = `<span class="placeholder">[PLACEHOLDER — athlete or team quote, Anthony to supply]</span>` and `<cite>` = `<span class="placeholder">[PLACEHOLDER — name, team]</span>`. Third card spans: add `.cards.three{grid-template-columns:repeat(3,1fr)}`. `blockquote.small{font-size:22px;border:0;padding:0}`.

- [ ] **Step 2: Newsletter**

`<section id="newsletter" class="band"><div class="wrap narrow">` centered (`.narrow{max-width:640px;text-align:center}`): `.label` "Newsletter", `h2` "What the pros know. Weekly.", `<p>` "One email a week: a recipe, a habit from the locker room, and something I learned this week. No fluff.", `<form onsubmit="return false" class="inline">` with `<input type="email" placeholder="you@email.com" aria-label="Email">` + `<button class="btn solid" type="submit">Subscribe</button>`, then `<span class="placeholder">[PLACEHOLDER — connects to Squarespace newsletter block]</span>`.

CSS: `form.inline{display:flex;gap:12px;margin-top:24px}form.inline input{flex:1;padding:16px;border:1px solid var(--ink);background:var(--white);font:inherit}`

- [ ] **Step 3: Contact**

`<section id="contact"><div class="wrap grid2">` — left: `.label` "Contact", `h2` "Let's build your system.", `<p>` "Tell me what you're training for, who you're feeding, or what event you're planning. I'll reply within two business days." plus Instagram/LinkedIn links. Right: `<form onsubmit="return false" class="stack">` with labeled fields: Name (text), Email (email), I'm interested in (select: 1:1 Performance Nutrition / Team & Organization Consulting / Speaking & Workshops / Recipes & Meal Plans), Message (textarea rows=5), `<button class="btn solid">Send</button>`, `<span class="placeholder">[PLACEHOLDER — Squarespace form block]</span>`.

CSS: `form.stack{display:grid;gap:14px}form.stack label{font:600 12px var(--label);letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}form.stack input,form.stack select,form.stack textarea{width:100%;padding:14px;border:1px solid var(--ink);background:var(--white);font:inherit}`

- [ ] **Step 4: Run checker** — `python3 scripts/check.py` — Expected: `PASS`.

- [ ] **Step 5: Commit**

```bash
git add index.html && git commit -m "Add Testimonials, Newsletter, and Contact sections"
```

---

### Task 5: Responsive pass, browser verification, publish

**Files:**
- Modify: `index.html` — add the mobile media query.

- [ ] **Step 1: Mobile CSS**

```css
@media (max-width:800px){
 .grid2,.cards,.cards.three,.row3{grid-template-columns:1fr}
 .hero{min-height:auto}
 header nav{display:none;position:absolute;left:0;right:0;top:100%;background:var(--cream);padding:16px var(--pad);flex-direction:column;gap:14px;border-bottom:1px solid var(--gold)}
 header nav.open{display:flex}
 .menu{display:inline-block}
 header .btn{display:none}
 form.inline{flex-direction:column}
 blockquote{font-size:24px}
}
.menu{display:none;background:none;border:1px solid var(--ink);padding:8px 12px;font:600 11px var(--label);letter-spacing:.14em;text-transform:uppercase;cursor:pointer}
```

- [ ] **Step 2: Run checker** — `python3 scripts/check.py` — Expected: `PASS`.

- [ ] **Step 3: Browser verification (Chrome extension)**

Serve locally: `python3 -m http.server 8787 --directory /Users/jeffrey/Sandbox/Anthony` in the background. In Chrome: open `http://localhost:8787/`, screenshot desktop; resize window to 400 wide, screenshot; click each nav link and confirm the target heading is visible; check `read_console_messages` shows no errors; confirm no horizontal scrollbar at 400px (`document.documentElement.scrollWidth <= window.innerWidth` via javascript_tool). Save the two screenshots to `docs/screenshots/desktop.png` and `docs/screenshots/mobile.png`. Kill the server.

- [ ] **Step 4: Commit and push**

```bash
git add index.html docs/screenshots && git commit -m "Add responsive layout and verification screenshots"
git push origin main
```

- [ ] **Step 5: Verify GitHub Pages is live**

Run: `gh api repos/hammbino/anthonyjzamora-site/pages/builds/latest --jq '.status'` until `built`, then `curl -sI https://hammbino.github.io/anthonyjzamora-site/ | head -1` — Expected: `HTTP/2 200`. Open the URL in Chrome and screenshot to confirm it matches the local render.
