"""Minimal 3D mesh toolkit: primitives, transforms, binary STL writer.

Pure Python + numpy. No CAD software needed — this is how the example
character STL was built. Adapt the part lists for new characters.
Units are millimeters; Z is up.
"""
import numpy as np
import struct


def sphere(r, n_lat=28, n_lon=40):
    v = []
    for i in range(n_lat + 1):
        phi = -np.pi / 2 + np.pi * i / n_lat
        for j in range(n_lon + 1):
            th = 2 * np.pi * j / n_lon
            v.append((r * np.cos(phi) * np.cos(th),
                      r * np.cos(phi) * np.sin(th),
                      r * np.sin(phi)))
    t = []
    for i in range(n_lat):
        for j in range(n_lon):
            a = i * (n_lon + 1) + j
            b = a + 1
            c = a + n_lon + 1
            d = c + 1
            if i > 0:
                t.append((a, c, b))
            if i < n_lat - 1:
                t.append((b, c, d))
    return np.array(v), t


def torus(R, r, u0=0.0, arc=2 * np.pi, n_u=40, n_v=12):
    """Ring in the XY plane. u0/arc select a partial arc (radians)."""
    v = []
    for i in range(n_u + 1):
        u = u0 + arc * i / n_u
        for j in range(n_v + 1):
            w = 2 * np.pi * j / n_v
            v.append(((R + r * np.cos(w)) * np.cos(u),
                      (R + r * np.cos(w)) * np.sin(u),
                      r * np.sin(w)))
    t = []
    for i in range(n_u):
        for j in range(n_v):
            a = i * (n_v + 1) + j
            b = a + 1
            c = a + n_v + 1
            d = c + 1
            t += [(a, c, b), (b, c, d)]
    return np.array(v), t


def xform(v, scale=(1, 1, 1), rot=None, tr=(0, 0, 0)):
    """scale, then rotate (axis, radians), then translate."""
    v = v * np.array(scale)
    if rot:
        ax, a = rot
        c, s = np.cos(a), np.sin(a)
        if ax == 'x':
            M = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
        elif ax == 'y':
            M = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
        else:
            M = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        v = v @ M.T
    return v + np.array(tr)


def write_stl(parts, out_path, header=b'heritage pipeline model'):
    """parts: list of (verts, tris). Merged into one binary STL.

    Parts should intersect/overlap — slicers union them. Keep the model's
    lowest point at z=0 so it sits flat.
    """
    verts_list, tris_list, off = [], [], 0
    for v, t in parts:
        verts_list.append(v)
        tris_list += [(a + off, b + off, c + off) for a, b, c in t]
        off += len(v)
    V = np.vstack(verts_list)
    with open(out_path, 'wb') as f:
        f.write(header.ljust(80, b'\0')[:80])
        f.write(struct.pack('<I', len(tris_list)))
        for a, b, c in tris_list:
            pa, pb, pc = V[a], V[b], V[c]
            n = np.cross(pb - pa, pc - pa)
            l = np.linalg.norm(n)
            n = n / l if l > 0 else np.array([0., 0., 1.])
            f.write(struct.pack('<12fH', *n, *pa, *pb, *pc, 0))
    return out_path, len(tris_list)
