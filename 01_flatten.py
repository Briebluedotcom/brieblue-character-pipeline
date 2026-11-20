#!/usr/bin/env python3
"""01 — Flatten a textile photo via perspective correction.

Usage:
    python 01_flatten.py photo.jpg out.jpg --corners x1 y1 x2 y2 x3 y3 x4 y4
    corners: top-left, top-right, bottom-right, bottom-left (pixel coords).
"""
import argparse
import sys
sys.path.insert(0, 'lib')
from img import flatten

ap = argparse.ArgumentParser()
ap.add_argument('photo')
ap.add_argument('out')
ap.add_argument('--corners', nargs=8, type=float, required=True)
a = ap.parse_args()

corners = [(a.corners[i], a.corners[i + 1]) for i in range(0, 8, 2)]
flatten(a.photo, corners, a.out)
print('flattened ->', a.out)
