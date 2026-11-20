#!/usr/bin/env python3
"""04 — EXAMPLE: flower character as a printable 3D toy (STL).

Sample part list: chibi flower character, ~67mm tall, single-color FDM,
face as raised geometry.

Adapt it: change the part list (positions/sizes), keep the mesh toolkit.
New characters = new part lists, same primitives.

Usage:
    python 04_character_stl.py character.stl
"""
import sys
sys.path.insert(0, 'lib')
import math
from mesh import sphere, torus, xform, write_stl

parts = []


def add(v, t, **kw):
    parts.append((xform(v, **kw), t))


# head
add(*sphere(20, 36, 48), tr=(0, 0, 36))
# petal ruff: 9 petals ringing the head
for i in range(9):
    th = 2 * math.pi * i / 9
    add(*sphere(1, 16, 24), scale=(7.5, 4.5, 12), rot=('y', math.pi / 2 - th),
        tr=(19 * math.cos(th), -2, 36 + 19 * math.sin(th)))
# body (bottom at z=0 so it sits flat)
add(*sphere(1, 28, 36), scale=(13, 11, 15), tr=(0, 0, 15))
# arms
add(*sphere(1, 14, 20), scale=(3.5, 3.5, 8), rot=('z', -0.35), tr=(-14.5, 0, 16))
add(*sphere(1, 14, 20), scale=(3.5, 3.5, 8), rot=('z', 0.35), tr=(14.5, 0, 16))
# feet
add(*sphere(1, 14, 20), scale=(5, 6.5, 3.5), tr=(-6.5, 1, 3.5))
add(*sphere(1, 14, 20), scale=(5, 6.5, 3.5), tr=(6.5, 1, 3.5))
# eyes (embedded ~1mm, print as raised detail)
add(*sphere(1, 14, 20), scale=(3.2, 1.5, 4.2), tr=(-7.5, 17, 40))
add(*sphere(1, 14, 20), scale=(3.2, 1.5, 4.2), tr=(7.5, 17, 40))
# smile: torus arc rotated into the face plane
add(*torus(6, 1.3, u0=3.8397, arc=1.7453, n_u=24),
    rot=('x', 1.5707963), tr=(0, 18.8, 31))
# blush
add(*sphere(1, 10, 14), scale=(3, 1.2, 2.2), tr=(-12.5, 14.8, 35))
add(*sphere(1, 10, 14), scale=(3, 1.2, 2.2), tr=(12.5, 14.8, 35))

out = sys.argv[1] if len(sys.argv) > 1 else 'character.stl'
path, ntris = write_stl(parts, out, header=b'Character - art toy')
print(f'{path}: {ntris} triangles')
