# BrieBlue Character Pipeline

A local script kit that turns textile photos and character art into
manufacturable products: screen-print separations, embroidery vectors,
3D-printable character toys (STL), plush sewing patterns (SVG), and
localized ad images in 10 languages. Pure Python + Pillow + numpy.
No cloud, no accounts — your designs never leave the building.

## Original prompt

Ed, Nov 11, 2026: *"Let's start getting these together. Might as well
publish them. But then we will expand and improve them off line."*

The "them" is this character pipeline and the POS system
(`brieblue-booth-pos`). This repo is the publish-ready snapshot; both
keep being developed offline after publishing.

The kit itself was built 2026-10-10 from a suzani demo: old photo →
flattened → 10-color separation → cotton-blossom motif → cartoon
character → 67 mm STL + plush pattern. Every step in this kit produced
a real artifact that day. (Full run guide: `PIPELINE.md`, the original
README, kept verbatim.)

## The pipeline

```
photo → 01_flatten → 02_separate → 03_extract_motif → products
                                                        ├─ screen print / DTF (from 02)
                                                        ├─ embroidery vector (trace the motif, then digitize)
                                                        ├─ 04_character_stl (3D print toy)
                                                        └─ 05_plush_pattern (sewing pattern)
```

## How to run

```bash
pip install -r requirements.txt
# vectorization needs vtracer (for the embroidery-vector step):
pip install vtracer

# 1. Square up the photo (corners: top-left, top-right, bottom-right, bottom-left)
python 01_flatten.py photo.jpg flat.jpg --corners 125 148 1035 162 1110 835 20 805

# 2. Isolate N spot colors
python 02_separate.py flat.jpg flat-10color.jpg --colors 10

# 3. Pull a motif (transparent background)
python 03_extract_motif.py flat.jpg motif.png --center 752 548 --radius 50

# 4. Sample flower character → printable STL (example; adapt the part list)
python 04_character_stl.py character.stl

# 5. Sample flower character → plush sewing pattern (example; adapt the pieces)
python 05_plush_pattern.py character-plush-pattern.svg

# 6. Translate ad strings via local Glimmer (--mock tests without a model)
python 06_translate.py i18n/strings.example.json translations/ --langs all
python 06_translate.py i18n/strings.example.json translations/ --langs th hi --mock

# 7. Render localized ad images from a spec + translations
python 07_render_ad.py ad-spec.json translations/ ads/ --langs all
```

## Multilingual (the ad factory, local)

- `06_translate.py` — master strings JSON → per-language JSON via Glimmer
  (Ollama OpenAI-compatible API; `GLIMMER_HOST` / `GLIMMER_MODEL` env).
- `07_render_ad.py` — spec JSON (background, text slots) + translations →
  one PNG per language.
- `lib/i18n.py` — 10 languages (vi, zh-Hans, tl, ko, th, hi, ta, te, ur, ja),
  Noto fonts, raqm shaping for Thai/Indic/RTL. Automatic font fallback so
  Latin brand names never tofu inside Thai/Hindi/Tamil/Telugu/Urdu text.
- `i18n/languages.json`, `i18n/strings.example.json` — config + example.
- Note: Urdu uses Noto Nastaliq — give it generous vertical clearance;
  its line box is dramatically tall.

## What runs where

| Step | Local | Cloud |
|---|---|---|
| Flatten, color separation, motif extraction | ✅ | — |
| Vectorization (vtracer) | ✅ | — |
| 3D STL builder | ✅ | — |
| Plush pattern | ✅ | — |
| Cartoon character art (image generation) | ❌ text-out models only | ✅ image model |

The character-art step is the one handoff: the cloud model draws the
character, this kit manufactures everything from it.

## Library

- `lib/img.py` — flatten, separate_colors, extract_motif
- `lib/mesh.py` — sphere, torus, xform, write_stl (binary STL writer)
- `lib/i18n.py` — language table, fonts, shaped rendering
- `lib/glimmer_client.py` — local Glimmer via Ollama's OpenAI-compatible API

## Changes made for publication

- `04_character_stl.py`, `05_plush_pattern.py` — the sample scripts
  referenced the author's character by name (default output filenames,
  STL header, pattern title). Those references are now generic
  (`character.stl`, `character-plush-pattern.svg`). The sample part lists
  are unchanged — see the open question in "Not included" below.
- `lib/mesh.py` — docstring reference to the author's character made generic.
- The original run guide is kept verbatim as `PIPELINE.md`. Its steps 4–5
  still name the author's character in prose; the scripts themselves no
  longer do.

## Not included (and why)

- **The author's character files** (`blossom-character.stl`,
  `blossom-character-v2.stl`, `blossom-character-preview.png`,
  `blossom-plush-pattern.svg`): the author's own character IP. Not in
  this repo — the scripts in steps 4–5 are *example builders* with a
  sample flower-character part list, not the production files.
- **Generated outputs**: STL/SVG/PNG files the scripts produce, plus
  `translations/` and `ads/` — rebuild from the scripts.
- **Caches**: `__pycache__/`, `*.pyc`.
- **Open question — the sample part lists**: scripts 04 and 05 build a
  sample flower character whose geometry closely follows the author's
  character. If the character design itself is meant to stay private,
  the part lists should be swapped for a neutral placeholder character
  before publishing. That swap is a one-file change per script and is
  left for the author's decision.

## License

Not yet chosen — to be decided before publishing.
