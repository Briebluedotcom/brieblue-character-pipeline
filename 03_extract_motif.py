#!/usr/bin/env python3
"""03 — Cut a circular motif with transparent background.

Usage:
    python 03_extract_motif.py flat.jpg motif.png --center 752 548 --radius 50
"""
import argparse
import sys
sys.path.insert(0, 'lib')
from img import extract_motif

ap = argparse.ArgumentParser()
ap.add_argument('image')
ap.add_argument('out')
ap.add_argument('--center', nargs=2, type=float, required=True)
ap.add_argument('--radius', type=float, required=True)
a = ap.parse_args()

extract_motif(a.image, a.center[0], a.center[1], a.radius, a.out)
print('motif ->', a.out)
