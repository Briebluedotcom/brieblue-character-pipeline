#!/usr/bin/env python3
"""05 — EXAMPLE: flower character plush sewing pattern (SVG).

First-draft pattern: ~200mm finished toy, 6mm seam allowance INCLUDED,
solid lines = CUT, dashed = SEW. A plush maker refines fit and fabric
behavior from here.

Adapt it: change the piece shapes/sizes/labels, keep the SVG helpers.

Usage:
    python 05_plush_pattern.py character-plush-pattern.svg
"""
import sys

W, H = 900, 1100
SA = 6  # seam allowance, mm
P = []
P.append('<?xml version="1.0" encoding="UTF-8"?>')
P.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
P.append('<rect width="100%" height="100%" fill="white"/>')
P.append('<style>.lbl{font:600 22px sans-serif;fill:#222}.sub{font:16px sans-serif;fill:#555}'
         '.note{font:15px sans-serif;fill:#333}.cut{fill:none;stroke:#111;stroke-width:3}'
         '.sew{fill:none;stroke:#111;stroke-width:1.2;stroke-dasharray:7 5}'
         '.grain{stroke:#888;stroke-width:1.5;marker-end:url(#arr)}</style>')
P.append('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
         '<path d="M0,0 L6,3 L0,6" fill="none" stroke="#888" stroke-width="1.5"/></marker></defs>')
P.append('<text x="40" y="55" class="lbl">Character — plush pattern (first draft)</text>')
P.append('<text x="40" y="82" class="sub">Finished size ~200mm tall · 6mm seam allowance INCLUDED · solid = CUT, dashed = SEW</text>')


def label(x, y, name, spec):
    P.append(f'<text x="{x}" y="{y}" class="lbl">{name}</text>')
    P.append(f'<text x="{x}" y="{y + 24}" class="sub">{spec}</text>')


def grain(x1, y1, x2, y2):
    P.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="grain"/>')


# A: HEAD x2 — circles r=60
for cx in (140, 300):
    cy = 220
    P.append(f'<circle cx="{cx}" cy="{cy}" r="60" class="cut"/>')
    P.append(f'<circle cx="{cx}" cy="{cy}" r="{60 - SA}" class="sew"/>')
    grain(cx, cy + 30, cx, cy - 30)
label(60, 320, "A — HEAD", "cut 2 · pink minky")

# B: PETAL x18 — pointed petal, 90 long x 50 wide
cx, cy, L, Wd = 520, 220, 90, 50
P.append(f'<path d="M {cx} {cy - L / 2} C {cx + Wd / 2} {cy - L / 4}, {cx + Wd / 2} {cy + L / 4}, {cx} {cy + L / 2} '
         f'C {cx - Wd / 2} {cy + L / 4}, {cx - Wd / 2} {cy - L / 4}, {cx} {cy - L / 2} Z" class="cut"/>')
P.append(f'<path d="M {cx} {cy - L / 2 + SA} C {cx + Wd / 2 - SA} {cy - L / 4}, {cx + Wd / 2 - SA} {cy + L / 4}, {cx} {cy + L / 2 - SA} '
         f'C {cx - Wd / 2 + SA} {cy + L / 4}, {cx - Wd / 2 + SA} {cy - L / 4}, {cx} {cy - L / 2 + SA} Z" class="sew"/>')
grain(cx, cy + 28, cx, cy - 28)
label(440, 320, "B — PETAL", "cut 18 (9 pairs) · white fleece")

# C: BODY x2 — rounded rect 100x110
for x in (90, 230):
    y = 420
    P.append(f'<rect x="{x}" y="{y}" width="100" height="110" rx="30" class="cut"/>')
    P.append(f'<rect x="{x + SA}" y="{y + SA}" width="{100 - 2 * SA}" height="{110 - 2 * SA}" rx="24" class="sew"/>')
    grain(x + 50, y + 85, x + 50, y + 25)
label(60, 580, "C — BODY", "cut 2 · blue minky")

# D: ARM x4 — capsule 30x62
for x in (420, 490):
    y = 420
    P.append(f'<rect x="{x}" y="{y}" width="30" height="62" rx="15" class="cut"/>')
    P.append(f'<rect x="{x + SA}" y="{y + SA}" width="{30 - 2 * SA}" height="{62 - 2 * SA}" rx="9" class="sew"/>')
label(400, 580, "D — ARM", "cut 4 (2 pairs) · dark fleece")

# E: FOOT x4 — 44x30 rounded
for x in (600, 680):
    y = 420
    P.append(f'<rect x="{x}" y="{y}" width="44" height="30" rx="14" class="cut"/>')
    P.append(f'<rect x="{x + SA}" y="{y + SA}" width="{44 - 2 * SA}" height="{30 - 2 * SA}" rx="8" class="sew"/>')
label(590, 580, "E — FOOT", "cut 4 (2 pairs) · dark fleece")

# FACE guide — embroidery placement on head front
cx, cy, r = 150, 720, 60
P.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="cut"/>')
P.append(f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" class="sub">FACE PLACEMENT</text>')
for ex in (cx - 22, cx + 22):
    P.append(f'<ellipse cx="{ex}" cy="{cy - 12}" rx="9" ry="12" fill="#222"/>')
P.append(f'<path d="M {cx - 16} {cy + 18} Q {cx} {cy + 32} {cx + 16} {cy + 18}" fill="none" '
         f'stroke="#222" stroke-width="4" stroke-linecap="round"/>')
for bx in (cx - 36, cx + 36):
    P.append(f'<ellipse cx="{bx}" cy="{cy + 8}" rx="8" ry="6" fill="#e79ab2"/>')
P.append(f'<text x="{cx}" y="{cy + r + 30}" text-anchor="middle" class="sub">embroider / appliqué felt</text>')

notes = [
    "ASSEMBLY (first-draft order — your plush maker refines):",
    "1. Sew petal pairs right-sides together, turn, light stuff; topstitch 9 petals in a ring to head-back.",
    "2. Embroider face on head-front (or appliqué felt), then sew head front/back, stuff firmly.",
    "3. Sew body front/back, stuff; attach arms and feet before closing side seams.",
    "4. Ladder-stitch head to body. Fluff.",
    "FABRIC: minky or plush fleece for head/body; felt or fleece for petals; polyfill stuffing.",
]
y = 880
for n in notes:
    P.append(f'<text x="40" y="{y}" class="note">{n}</text>')
    y += 28

P.append('</svg>')
out = sys.argv[1] if len(sys.argv) > 1 else 'character-plush-pattern.svg'
open(out, 'w').write('\n'.join(P))
print('pattern ->', out)
