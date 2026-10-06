#!/usr/bin/env python3
"""MZM Construction — build (1. + 2. fázis)
A src/index.html-ből önálló, egyfájlos index.html-t készít:
  • minden kép és betűtípus data-URI-ként,
  • a GSAP + ScrollTrigger könyvtárak inline-ba ágyazva
    (a CDN-es <script> tag-eket lecseréli a helyi példányokra).
Így a sandboxos előnézetben (nincs hálózat) is minden fut.
A forrásban a CDN hivatkozások maradnak — éles honlapon a build
helyett nyugodtan használhatók a CDN tag-ek közvetlenül.
"""
import base64, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent   # /home/user/mzm
SRC  = (ROOT / 'src' / 'index.html').read_text(encoding='utf-8')

def data_uri(path: pathlib.Path, mime: str) -> str:
    b = path.read_bytes()
    return f"data:{mime};base64," + base64.b64encode(b).decode('ascii')

html = SRC

# ── 1) JS könyvtárak: CDN tag → inline ────────────────────────────────
gsap_js = (ROOT/'assets/js/gsap.min.js').read_text(encoding='utf-8')
st_js   = (ROOT/'assets/js/ScrollTrigger.min.js').read_text(encoding='utf-8')
assert '</script' not in gsap_js and '</script' not in st_js, "a lib nem inline-olható biztonságosan"

html, n1 = re.subn(
    r'<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]+/dist/gsap\.min\.js"\s*></script>',
    lambda m: '<script>\n/* GSAP 3.13.0 — inline a sandboxos előnézethez; CDN: https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js */\n' + gsap_js + '\n</script>',
    html, count=1)
html, n2 = re.subn(
    r'<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]+/dist/ScrollTrigger\.min\.js"\s*></script>',
    lambda m: '<script>\n/* ScrollTrigger 3.13.0 — inline a sandboxos előnézethez; CDN: https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js */\n' + st_js + '\n</script>',
    html, count=1)
assert n1 == 1 and n2 == 1, f"CDN csere nem sikerült: {n1}, {n2}"

# ── 2) Betűtípusok ────────────────────────────────────────────────────
html = html.replace("assets/fonts/hedviglettersserif.woff2", "__FONT_HEDVIG__")
html = html.replace("assets/fonts/archivo.woff2", "__FONT_ARCHIVO__")
html = html.replace("__FONT_HEDVIG__", data_uri(ROOT/'assets/fonts/hedviglettersserif.woff2', 'font/woff2'))
html = html.replace("__FONT_ARCHIVO__", data_uri(ROOT/'assets/fonts/archivo.woff2', 'font/woff2'))

# ── 3) Képek (people1..9 + gal1..6, optimalizált változat) ───────────
for i in range(1, 10):
    html = html.replace(f"assets/img/people{i}.jpg", f"__IMG_PEOPLE{i}__")
for i in range(1, 7):
    html = html.replace(f"assets/img/gal{i}.jpg", f"__IMG_GAL{i}__")
for i in range(1, 10):
    html = html.replace(f"__IMG_PEOPLE{i}__", data_uri(ROOT/f'assets/img/opt/people{i}.jpg', 'image/jpeg'))
for i in range(1, 7):
    html = html.replace(f"__IMG_GAL{i}__", data_uri(ROOT/f'assets/img/opt/gal{i}.jpg', 'image/jpeg'))

out = ROOT/'index.html'
out.write_text(html, encoding='utf-8')
print(f"OK -> {out}  ({out.stat().st_size/1024:.0f} KB)")

# ── 4) Ellenőrzés ─────────────────────────────────────────────────────
leftover = re.findall(r'(?:src|href)="(assets/[^"]+)"', html)
print("leftover asset refs:", leftover or "nincs ✓")
print("CDN maradvány:", "cdn.jsdelivr" in html.split('</title>')[1] and "VAN (hiba)" or "nincs ✓")
