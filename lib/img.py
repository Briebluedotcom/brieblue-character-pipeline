"""Image steps of the heritage pipeline: flatten, color separation, motif extraction.

Pure Python + Pillow + numpy. Runs anywhere — this is the Glimmer-local part.
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np


def flatten(photo_path, corners, out_path, out_size=None):
    """Perspective-correct a textile photo.

    corners: [(x, y)] x4 in order: top-left, top-right, bottom-right, bottom-left.
    Estimate them by viewing the photo; precision matters less than order.
    """
    im = Image.open(photo_path).convert('RGB')
    (tl, tr, br, bl) = corners

    def dist(a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    if out_size is None:
        w = int((dist(tl, tr) + dist(bl, br)) / 2)
        h = int((dist(tl, bl) + dist(tr, br)) / 2)
        out_size = (w, h)

    def find_coeffs(dst, src):
        m = []
        for (x1, y1), (x2, y2) in zip(dst, src):
            m.append([x1, y1, 1, 0, 0, 0, -x2 * x1, -x2 * y1])
            m.append([0, 0, 0, x1, y1, 1, -y2 * x1, -y2 * y1])
        return np.linalg.solve(np.array(m), np.array(src).reshape(8))

    dst = [(0, 0), (out_size[0], 0), (out_size[0], out_size[1]), (0, out_size[1])]
    coeffs = find_coeffs(dst, [tl, tr, br, bl])
    flat = im.transform(out_size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    flat.save(out_path)
    return out_path


def separate_colors(img_path, k, out_path, seed=7, iters=25):
    """K-means color separation -> flat spot colors, screen-print style.

    k = number of spot colors. Returns (out_path, palette hex list).
    For production, hand-tune the palette after this first pass.
    """
    rng = np.random.default_rng(seed)
    im = Image.open(img_path).convert('RGB')
    a = np.array(im).reshape(-1, 3).astype(np.float32)
    sample = a[rng.choice(a.shape[0], min(60000, a.shape[0]), replace=False)]
    centers = sample[rng.choice(sample.shape[0], k, replace=False)].copy()
    for _ in range(iters):
        d = ((sample[:, None, :] - centers[None, :, :]) ** 2).sum(-1)
        lab = d.argmin(1)
        new = np.array([sample[lab == i].mean(0) if (lab == i).any() else centers[i]
                        for i in range(k)])
        if np.allclose(new, centers):
            break
        centers = new
    d = ((a[:, None, :] - centers[None, :, :]) ** 2).sum(-1)
    out = centers[d.argmin(1)].astype(np.uint8).reshape(im.size[1], im.size[0], 3)
    Image.fromarray(out).save(out_path)
    palette = ['#%02x%02x%02x' % tuple(c.astype(int)) for c in centers]
    return out_path, palette


def extract_motif(img_path, cx, cy, r, out_path, feather=1.0):
    """Cut a circular motif with transparent background.

    Works best on flattened images. For packed borders, keep r tight —
    neighbors intrude fast.
    """
    im = Image.open(img_path).convert('RGB')
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    rgba = im.convert('RGBA')
    rgba.putalpha(mask)
    rgba.crop((cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4)).save(out_path)
    return out_path
