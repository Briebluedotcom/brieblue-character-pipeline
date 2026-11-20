# Heritage Pipeline — Glimmer-local script kit

Everything from the suzani demo, packaged to run on your own machine.
Pure Python + Pillow + numpy. No cloud, no accounts, your designs never
leave the building.

## The pipeline

```
photo → 01_flatten → 02_separate → 03_extract_motif → products
                                                        ├─ screen print / DTF (from 02)
                                                        ├─ embroidery vector (trace the motif, then digitize)
                                                        ├─ 04_character_stl (3D print toy)
                                                        └─ 05_plush_pattern (sewing pattern)
```

## Install

```bash
pip install -r requirements.txt
# vectorization needs vtracer (for the embroidery-vector step):
pip install vtracer
```

## Run

```bash
# 1. Square up the photo (corners: top-left, top-right, bottom-right, bottom-left)
python 01_flatten.py photo.jpg flat.jpg --corners 125 148 1035 162 1110 835 20 805

# 2. Isolate N spot colors
python 02_separate.py flat.jpg flat-10color.jpg --colors 10

# 3. Pull a motif (transparent background)
python 03_extract_motif.py flat.jpg motif.png --center 752 548 --radius 50

# 4. Blossom character → printable STL (example; adapt the part list)
python 04_character_stl.py blossom-character.stl

# 5. Blossom character → plush sewing pattern (example; adapt the pieces)
python 05_plush_pattern.py blossom-plush-pattern.svg

# 6. Translate ad strings via local Glimmer (--mock tests without a model)
python 06_translate.py i18n/strings.example.json translations/ --langs all
python 06_translate.py i18n/strings.example.json translations/ --langs th hi --mock

# 7. Render localized ad images from a spec + translations
python 07_render_ad.py ad-spec.json translations/ ads/ --langs all
```

## Multilingual (the ad factory, local)

- `06_translate.py` — master strings JSON → per-language JSON via Glimmer
  (Ollama OpenAI-compatible API; `GLIMMER_HOST`/`GLIMMER_MODEL` env).
- `07_render_ad.py` — spec JSON (background, text slots) + translations →
  one PNG per language.
- `lib/i18n.py` — 10 languages (vi, zh-Hans, tl, ko, th, hi, ta, te, ur, ja),
  Noto fonts, raqm shaping for Thai/Indic/RTL. Automatic font fallback so
  Latin brand names never tofu inside Thai/Hindi/Tamil/Telugu/Urdu text.
- `i18n/languages.json`, `i18n/strings.example.json` — config + example.
- Note: Urdu uses Noto Nastaliq — give it generous vertical clearance;
  its line box is dramatically tall.

## What runs where (the Spark ⇄ Glimmer split)

| Step | Glimmer-local | Cloud (Spark) |
|---|---|---|
| Flatten, color separation, motif extraction | ✅ | — |
| Vectorization (vtracer) | ✅ | — |
| 3D STL builder | ✅ | — |
| Plush pattern | ✅ | — |
| Cartoon character art (image generation) | ❌ Glimmer is text-out only | ✅ Spark/Muse Image |

The character-art step is the one handoff: Spark draws the character,
Glimmer manufactures everything from it.

## Library

- `lib/img.py` — flatten, separate_colors, extract_motif
- `lib/mesh.py` — sphere, torus, xform, write_stl (binary STL writer)

## Provenance

Built 2026-10-10 from the suzani demo: old photo → flattened →
10-color separation → cotton-blossom motif → cartoon character →
67mm STL + plush pattern. Every step in this kit produced a real
artifact that day.
