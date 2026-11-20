#!/usr/bin/env python3
"""02 — Separate an image into N flat spot colors (screen-print style).

Usage:
    python 02_separate.py flat.jpg out.jpg --colors 10
"""
import argparse
import sys
sys.path.insert(0, 'lib')
from img import separate_colors

ap = argparse.ArgumentParser()
ap.add_argument('image')
ap.add_argument('out')
ap.add_argument('--colors', type=int, default=8)
a = ap.parse_args()

path, palette = separate_colors(a.image, a.colors, a.out)
print('separated ->', path)
print('palette:', ' '.join(palette))
