#!/usr/bin/env python3
"""07 — Render localized ad images from a master spec + translated strings.

Spec JSON:
{
  "size": [1080, 1080],
  "background": [18, 18, 28],            # RGB, or path to a bg image
  "slots": [
    {"key": "invite", "pos": [540, 780], "size": 72,
     "color": "#ffffff", "anchor": "ma"}
  ]
}
Translations dir holds strings.<lang>.json files (from 06_translate.py).

Usage:
    python 07_render_ad.py spec.json translations_dir out_dir --langs th hi
"""
import argparse
import json
import os
import sys
sys.path.insert(0, 'lib')
from PIL import Image, ImageDraw
from i18n import draw_text, LANGUAGES

ap = argparse.ArgumentParser()
ap.add_argument('spec')
ap.add_argument('translations')
ap.add_argument('out_dir')
ap.add_argument('--langs', nargs='+', required=True)
a = ap.parse_args()

with open(a.spec) as f:
    spec = json.load(f)

os.makedirs(a.out_dir, exist_ok=True)
langs = sorted(LANGUAGES) if a.langs == ['all'] else a.langs
for lc in langs:
    if lc not in LANGUAGES:
        sys.exit(f'unknown language: {lc}')
    spath = os.path.join(a.translations, f'strings.{lc}.json')
    with open(spath) as f:
        strings = json.load(f)

    bg = spec['background']
    img = Image.open(bg).convert('RGB').resize(tuple(spec['size'])) \
        if isinstance(bg, str) else Image.new('RGB', tuple(spec['size']), tuple(bg))
    d = ImageDraw.Draw(img)
    for slot in spec['slots']:
        text = strings[slot['key']]
        color = tuple(int(slot['color'].lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        draw_text(d, tuple(slot['pos']), text, lc,
                  size=slot.get('size', 48), fill=color,
                  anchor=slot.get('anchor', 'la'))
    out = os.path.join(a.out_dir, f'ad.{lc}.png')
    img.save(out)
    print('rendered', out)
