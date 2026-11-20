"""Client for the local Glimmer model via Ollama's OpenAI-compatible API.

Set GLIMMER_HOST / GLIMMER_MODEL env vars, or pass explicitly.
No model needed at import time — calls fail only when actually used.
"""
import json
import os
import urllib.request

HOST = os.environ.get('GLIMMER_HOST', 'http://localhost:11434')
MODEL = os.environ.get('GLIMMER_MODEL', 'glimmer:30b')


def chat(messages, model=None, temperature=0.3, timeout=180):
    body = json.dumps({
        "model": model or MODEL,
        "messages": messages,
        "temperature": temperature,
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        HOST.rstrip('/') + '/v1/chat/completions',
        data=body,
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    return data['choices'][0]['message']['content']


TRANSLATE_SYSTEM = (
    "You are a professional translator for marketing copy. "
    "Translate accurately but naturally, as a native speaker would write it. "
    "Keep it short and punchy — this goes on an ad image. "
    "Return ONLY the translation, no explanations or quotes."
)


def translate(text, target_lang, source_lang='English', model=None):
    """Translate marketing text. target_lang like 'Thai', 'Hindi', 'Urdu'."""
    return chat(
        [
            {"role": "system", "content": TRANSLATE_SYSTEM},
            {"role": "user",
             "content": f"Translate this {source_lang} marketing text into {target_lang}:\n\n{text}"},
        ],
        model=model,
    ).strip()
