#!/usr/bin/env python3
"""Translate cantos XXXVII–XLI to Hebrew following _book1_he.json pattern."""

import anthropic
import json
import os
import re

# Config
MODEL = 'claude-sonnet-4-6'
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

NAME_MAP = {
    'Rama': 'ראמה',
    'Ráma': 'ראמה',
    'Rāma': 'ראמה',
    'Sita': 'סיטה',
    'Síta': 'סיטה',
    'Sītā': 'סיטה',
    'Lakshmana': 'לקשמנה',
    'Lakshman': 'לקשמנה',
    'Hanuman': 'האנומאן',
    'Hanumán': 'האנומאן',
    'Hanumān': 'האנומאן',
    'Ravana': 'ראוונה',
    'Rávana': 'ראוונה',
    'Rāvaṇa': 'ראוונה',
    'Dasaratha': 'דשארת׳ה',
    'Daśaratha': 'דשארת׳ה',
    'Valmiki': 'ואלמיקי',
    'Válmíki': 'ואלמיקי',
    'Vālmīki': 'ואלמיקי',
    'Bharata': 'בהאראטה',
    'Shatrughna': 'שאטרוגנה',
    'Kaikeyi': 'קייקיי',
    'Kaushalya': 'קאושאליה',
    'Sumitra': 'סומיטרה',
    'Sugriva': 'סוגריווה',
    'Vali': 'ואלי',
    'Jatayu': 'ג׳טאיו',
    'Vibhishana': 'ויביישאנה',
    'Indra': 'אינדרה',
    'Vishnu': 'וישנו',
    'Brahma': 'ברהמה',
    'Shiva': 'שיווה',
    'Lanka': 'לאנקה',
    'Ayodhya': 'איודה׳יה',
    'Kishkindha': 'קישקינד׳ה',
    'Dandaka': 'דאנדאקה',
    'Janaka': 'ג׳נקה',
    'Narad': 'נארד',
}

VERSE_SYSTEM_PROMPT = """You are an expert literary translator specializing in translating Sanskrit epics from English into Hebrew.
Your task: translate Ramayana verse (Griffith's 19th-century English translation) into flowing, beautiful Modern Literary Hebrew (עברית ספרותית).

Rules:
1. Use the following transliterations for Sanskrit proper nouns (NEVER translate them):
""" + '\n'.join(f'   {en} → {he}' for en, he in NAME_MAP.items()) + """

2. Produce poetic, literary Hebrew that flows naturally — not word-for-word translation.
3. Preserve the devotional and epic register of the original.
4. Each input paragraph → one output paragraph. Return EXACTLY the same number of paragraphs.
5. Separate output paragraphs with a single blank line.
6. Output ONLY the translated text. No explanations, no headers.
"""

def load_js_data(filename):
    """Load a JS data file and return the Python object."""
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    m = re.search(r'=\s*(\[|\{)', raw)
    if not m:
        raise ValueError(f'Cannot find data in {filename}')
    json_str = raw[m.start(1):]
    json_str = json_str.rstrip().rstrip(';')
    return json.loads(json_str)

def translate_paragraphs(client, paragraphs, canto_num, canto_title):
    """Translate a list of paragraphs using Claude."""
    if not paragraphs:
        return []

    joined = '\n\n'.join(paragraphs)
    user_msg = f'Canto {canto_num}: {canto_title}\n\nTranslate the following into Hebrew:\n\n{joined}'

    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        system=VERSE_SYSTEM_PROMPT,
        messages=[{'role': 'user', 'content': user_msg}]
    )
    result_text = response.content[0].text.strip()
    result_paras = [p.strip() for p in result_text.split('\n\n') if p.strip()]
    return result_paras

def main():
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        print('ERROR: ANTHROPIC_API_KEY environment variable not set.')
        return 1

    client = anthropic.Anthropic(api_key=api_key)

    # Load source and existing Hebrew data
    print('Loading source data…')
    source_text = load_js_data('text.js')
    book1 = source_text[0]

    with open(os.path.join(DATA_DIR, '_book1_he.json'), 'r', encoding='utf-8') as f:
        existing_he = json.load(f)

    print(f'Book I: {len(book1["cantos"])} cantos in English')
    print(f'Existing Hebrew: {len(existing_he)} items')

    # Find start canto (XXXVII is at index 37, after Invocation + I–XXXVI)
    start_index = 37
    target_cantos = ['XXXVII', 'XXXVIII', 'XXXIX', 'XL', 'XLI']

    cantos_he = list(existing_he)

    for target_canto in target_cantos:
        # Find canto in English source
        en_canto = None
        for c in book1['cantos']:
            if c['number'] == target_canto:
                en_canto = c
                break

        if not en_canto:
            print(f'  ✗ Canto {target_canto} not found in source')
            continue

        print(f'\nTranslating Canto {target_canto} ({en_canto["title"]})…', end='', flush=True)

        paras_he = translate_paragraphs(client, en_canto['paragraphs'], target_canto, en_canto['title'])

        canto_he = {
            'number': target_canto,
            'title': en_canto['title'],
            'paragraphs': paras_he,
        }
        if en_canto.get('inlineImage'):
            canto_he['inlineImage'] = en_canto['inlineImage']

        cantos_he.append(canto_he)
        print(f' {len(paras_he)} stanzas ✓')

    # Write updated Hebrew data
    out_path = os.path.join(DATA_DIR, '_book1_he.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(cantos_he, f, ensure_ascii=False, separators=(',', ':'), indent=0)

    print(f'\n✓ Wrote {out_path} ({len(cantos_he)} items)')
    return 0

if __name__ == '__main__':
    exit(main())
