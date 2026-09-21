#!/usr/bin/env python3
"""Structural checks for index.html. Exit 1 on any failure."""
import re, sys, pathlib
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"
REQUIRED_IDS = ["about", "services", "igotmore", "recipes", "testimonials", "newsletter", "contact"]
ALLOWED_HEX = {"#f6f1ec", "#eae2d9", "#0b0a08", "#e8b33c", "#7a6350", "#5a4a3a", "#ffffff", "#fff", "#000", "#000000"}

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
        if hexv not in ALLOWED_HEX and hexv[1:] not in p.ids and len(hexv) in (4,7):
            fails.append(f"off-palette color {hexv}")
    text=" ".join(p.text)
    n_marked=len(re.findall(r"\[[^\]]*PLACEHOLDER[^\]]*\]", text))
    if n_marked != text.count("PLACEHOLDER"):
        fails.append(f"{text.count('PLACEHOLDER')-n_marked} PLACEHOLDER(s) not inside [brackets]")
    if re.search(r"\$\s?\d[\d,\.]*\s*(/|per|mo\b|month|hr\b|hour|session)", text, re.I):
        fails.append("a price appears in page text")
    for f in fails: print("FAIL", f)
    print("PASS" if not fails else f"{len(fails)} failure(s)"); sys.exit(1 if fails else 0)

if __name__=="__main__": main()
