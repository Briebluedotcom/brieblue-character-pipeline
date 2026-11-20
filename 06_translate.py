#!/usr/bin/env python3
"""06 — Translate a strings JSON file into target languages via local Glimmer.

Usage:
    python 06_translate.py i18n/strings.example.json out_dir --langs th hi ta ur
    python 06_translate.py i18n/strings.example.json out_dir --langs all
    python 06_translate.py i18n/strings.example.json out_dir --langs th --mock

Writes out_dir/strings.<lang>.json per language.
--mock wraps text as [lang] text for pipeline testing WITHOUT a model.
Mock output is clearly marked and must never ship.
"""
import argparse
import json
import os
import sys
sys.path.insert(0, 'lib')
from i18n import LANGUAGES
from glimmer_client import translate

ap = argparse.ArgumentParser()
ap.add_argument('strings')
ap.add_argument('out_dir')
ap.add_argument('--langs', nargs='+', required=True,
                help="'all' or language codes, e.g. th hi ta")
ap.add_argument('--mock', action='store_true',
                help='test mode: no model calls, output marked [MOCK]')
a = ap.parse_args()

langs = sorted(LANGUAGES) if a.langs == ['all'] else a.langs
for lc in langs:
    if lc not in LANGUAGES:
        sys.exit(f'unknown language: {lc}')

with open(a.strings) as f:
    master = json.load(f)

os.makedirs(a.out_dir, exist_ok=True)
for lc in langs:
    lang_name = LANGUAGES[lc]['english']
    out = {}
    for key, text in master.items():
        if a.mock:
            out[key] = f'[MOCK-{lc}] {text}'
        else:
            print(f'translating [{key}] -> {lang_name}...')
            out[key] = translate(text, lang_name)
        print(f'  {lc}: {out[key][:60]}')
    path = os.path.join(a.out_dir, f'strings.{lc}.json')
    with open(path, 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print('wrote', path)
