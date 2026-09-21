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
