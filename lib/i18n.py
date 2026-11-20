"""Multilingual text: language table, fonts, shaped rendering.

Uses Pillow + raqm (harfbuzz/fribidi) so Thai, Indic conjuncts, and
Urdu RTL all shape correctly. Fonts are Noto, resolved from languages.json.

Urdu gets automatic font fallback: Noto Nastaliq has no Latin glyphs, so
Latin brand names / dates inside Urdu text render in DejaVu Sans instead
of tofu. Other languages' fonts already cover Latin.
"""
import json
import os
import unicodedata
from PIL import ImageFont
from fontTools.ttLib import TTFont

_HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_HERE, '..', 'i18n', 'languages.json')) as f:
    LANGUAGES = json.load(f)

FALLBACK_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
LATIN_FALLBACK = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'

_cmap_cache = {}


def _coverage(font_path, index=0):
    """Set of codepoints covered by a font (cached)."""
    key = (font_path, index)
    if key not in _cmap_cache:
        _cmap_cache[key] = TTFont(font_path, fontNumber=index)['cmap'].getBestCmap()
    return _cmap_cache[key]


def _coverage_runs(text, font_path, index=0):
    """Split text into (covered, run) by primary-font glyph coverage."""
    cmap = _coverage(font_path, index)
    runs, cur, cur_ok = [], '', None
    for ch in text:
        ok = ord(ch) in cmap
        if cur_ok is None:
            cur_ok = ok
        if ok == cur_ok:
            cur += ch
        else:
            runs.append((cur_ok, cur))
            cur, cur_ok = ch, ok
    if cur:
        runs.append((cur_ok, cur))
    return runs


def get_font(lang_code, size=48):
    lang = LANGUAGES[lang_code]
    kw = {'index': lang['font_index']} if 'font_index' in lang else {}
    return ImageFont.truetype(lang['font'], size, **kw)


def _is_arabic(ch):
    return ('\u0600' <= ch <= '\u06FF' or '\u0750' <= ch <= '\u077F'
            or '\u08A0' <= ch <= '\u08FF' or '\uFB50' <= ch <= '\uFDFF'
            or '\uFE70' <= ch <= '\uFEFF')


def _script_runs(text):
    """Split into (is_arabic, run). Neutrals (space/digits/punct) join neighbors."""
    runs, cur, cur_ar = [], '', None
    for ch in text:
        if ch.strip() == '' or unicodedata.category(ch)[0] in 'NP':
            ar = cur_ar  # inherit; leading neutrals default below
        else:
            ar = _is_arabic(ch)
        if cur_ar is None:
            cur_ar = ar if ar is not None else False
            if ar is None:
                ar = False
        if ar == cur_ar:
            cur += ch
        else:
            runs.append((cur_ar, cur))
            cur, cur_ar = ch, ar
    if cur:
        runs.append((cur_ar, cur))
    return runs


def _draw_rtl_fallback(draw, xy, text, size, fill, anchor):
    """Urdu: shape each script run with its own font, lay out right-to-left.

    Latin brand names inside Urdu text get DejaVu instead of tofu.
    Ink centers are aligned across runs so mixed lines sit evenly.
    y follows the caller's vertical anchor ('t'/'m'/'b') for the first run.
    """
    x, y = xy
    primary = get_font('ur', size)
    fallback = ImageFont.truetype(FALLBACK_FONT, size)
    runs = _script_runs(text)
    fonts = [primary if is_ar else fallback for is_ar, _ in runs]
    dirs = ['rtl' if is_ar else 'ltr' for is_ar, _ in runs]

    # measure runs: anchor 'lt' puts box[0] at the run's left edge for both
    # directions (no anchor mirroring under RTL)
    widths, ink_c = [], []
    for (is_ar, run), font, d in zip(runs, fonts, dirs):
        box = font.getbbox(run, direction=d, anchor='lt')
        widths.append(box[2] - box[0])
        ink_c.append((box[1] + box[3]) / 2)

    total = sum(widths)
    h = anchor[0] if anchor else 'l'
    v = anchor[1:] if len(anchor) > 1 else 't'
    asc, desc = primary.getmetrics()
    lh = asc + desc
    y_top_ref = {'t': y, 'm': y - lh / 2, 'b': y - lh}.get(v, y)

    pen = x + total / 2 if h == 'm' else (x if h == 'r' else x + total)
    for (is_ar, run), font, d, w, ic in zip(runs, fonts, dirs, widths, ink_c):
        pen -= w
        draw.text((pen, y_top_ref + (ink_c[0] - ic)), run, font=font,
                  fill=fill, anchor='lt', direction=d)
    return primary


def _draw_ltr_fallback(draw, xy, runs, lang_code, size, fill, anchor):
    """Non-RTL: runs the primary font can't cover render in Noto Sans.

    Splits fall on script boundaries in practice (Thai/Latin, Devanagari/
    Latin), so shaping stays intact. Ink centers align across runs.
    """
    x, y = xy
    lang = LANGUAGES[lang_code]
    index = lang.get('font_index', 0)
    primary = get_font(lang_code, size)
    lfb = ImageFont.truetype(LATIN_FALLBACK, size)
    fonts = [primary if ok else lfb for ok, _ in runs]
    widths, ink_c = [], []
    for (_, run), font in zip(runs, fonts):
        box = font.getbbox(run, anchor='lt')
        widths.append(box[2] - box[0])
        ink_c.append((box[1] + box[3]) / 2)
    total = sum(widths)
    h = anchor[0] if anchor else 'l'
    v = anchor[1:] if len(anchor) > 1 else 't'
    asc, desc = primary.getmetrics()
    lh = asc + desc
    y_top_ref = {'t': y, 'm': y - lh / 2, 'b': y - lh}.get(v, y)
    pen = x if h == 'l' else (x - total / 2 if h == 'm' else x - total)
    for (_, run), font, w, ic in zip(runs, fonts, widths, ink_c):
        draw.text((pen, y_top_ref + (ink_c[0] - ic)), run, font=font,
                  fill=fill, anchor='lt')
        pen += w
    return primary


def draw_text(draw, xy, text, lang_code, size=48, fill=(0, 0, 0), anchor='la'):
    """Draw complex-script text. RTL handled automatically per language.

    Falls back gracefully when the primary font lacks glyphs (e.g. Latin
    brand names in Thai/Hindi/Tamil/Telugu ads).
    """
    if LANGUAGES[lang_code].get('rtl'):
        return _draw_rtl_fallback(draw, xy, text, size, fill, anchor)
    lang = LANGUAGES[lang_code]
    runs = _coverage_runs(text, lang['font'], lang.get('font_index', 0))
    if len(runs) == 1 and runs[0][0]:
        font = get_font(lang_code, size)
        draw.text(xy, text, font=font, fill=fill, anchor=anchor)
        return font
    return _draw_ltr_fallback(draw, xy, runs, lang_code, size, fill, anchor)


def text_size(text, lang_code, size=48):
    """Measured width/height for layout (uses raqm shaping)."""
    font = get_font(lang_code, size)
    direction = 'rtl' if LANGUAGES[lang_code].get('rtl') else None
    box = font.getbbox(text, direction=direction)
    return box[2] - box[0], box[3] - box[1]
