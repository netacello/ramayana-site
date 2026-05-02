#!/usr/bin/env python3
"""
Ramayana Hebrew Translation Batch Orchestrator

Workflow:
1. Extracts remaining cantos from English source
2. Groups them into 5-canto batches
3. For each batch, generates a prompt and waits for translation
4. Merges translations into _book1_he.json
5. Tracks progress across sessions

Usage:
  python batch_translator.py

Follow the on-screen instructions to paste translations from Claude.
"""

import json
import re
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent / 'data'

def load_js_data(filename):
    """Load a JS data file."""
    path = DATA_DIR / filename
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    m = re.search(r'=\s*(\[)', raw)
    if not m:
        raise ValueError(f'Cannot find data in {filename}')
    json_str = raw[m.start(1):].rstrip().rstrip(';')
    return json.loads(json_str)

def load_hebrew_cantos():
    """Load existing Hebrew translations."""
    path = DATA_DIR / '_book1_he.json'
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_translated_canto_numbers():
    """Return set of already-translated canto numbers."""
    he_cantos = load_hebrew_cantos()
    return {c['number'] for c in he_cantos}

def get_remaining_cantos():
    """Get all cantos not yet translated."""
    source_text = load_js_data('text.js')
    book1 = source_text[0]
    translated = get_translated_canto_numbers()

    remaining = [c for c in book1['cantos'] if c['number'] not in translated]
    return remaining

def create_batches(cantos, batch_size=5):
    """Split cantos into batches."""
    batches = []
    for i in range(0, len(cantos), batch_size):
        batch = cantos[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        batches.append((batch_num, batch))
    return batches

def save_hebrew_cantos(cantos):
    """Save Hebrew translations to file."""
    path = DATA_DIR / '_book1_he.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(cantos, f, ensure_ascii=False, separators=(',', ':'))
    print(f"✓ Saved {path}")

def display_batch_info(batch_num, cantos):
    """Show user info about the batch."""
    canto_nums = [c['number'] for c in cantos]
    para_counts = [len(c['paragraphs']) for c in cantos]
    total_paras = sum(para_counts)

    print(f"\n{'='*70}")
    print(f"BATCH {batch_num}")
    print(f"{'='*70}")
    print(f"Cantos: {', '.join(canto_nums)}")
    print(f"Total paragraphs: {total_paras}")
    for c, pc in zip(cantos, para_counts):
        print(f"  - {c['number']}: {c['title']} ({pc} para)")

def generate_prompt(cantos):
    """Generate the prompt to send to Claude."""
    canto_nums = ', '.join([c['number'] for c in cantos])

    prompt = f"""Translate cantos {canto_nums} to Hebrew following the established pattern.

For each canto, provide the JSON in this format (replace with actual translations):

[
  {{
    "number": "CANTO_NUM",
    "title": "English Title",
    "paragraphs": [
      "Hebrew paragraph 1",
      "Hebrew paragraph 2",
      ...
    ]
  }},
  ...
]

Use the NAME_MAP from translate_to_hebrew.py for proper noun transliterations.
Maintain literary Hebrew style consistent with existing translations (cantos I-XLVI).
Each paragraph should be poetic, not word-for-word.

Return ONLY the JSON array, no other text."""

    return prompt

def get_english_text(cantos):
    """Return formatted English text for reference."""
    output = []
    for c in cantos:
        output.append(f"\n{'='*60}")
        output.append(f"CANTO {c['number']}: {c['title']}")
        output.append(f"{'='*60}\n")
        for i, para in enumerate(c['paragraphs'], 1):
            output.append(f"[Paragraph {i}]\n{para}\n")
    return '\n'.join(output)

def save_batch_reference(batch_num, cantos):
    """Save English text to reference file."""
    filename = f'_batch_{batch_num}_source.txt'
    path = Path(filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(get_english_text(cantos))
    print(f"\nEnglish source saved to: {filename}")
    return filename

def prompt_for_translation(batch_num, cantos):
    """Guide user through translation process."""
    display_batch_info(batch_num, cantos)
    source_file = save_batch_reference(batch_num, cantos)

    print(f"\n{'='*70}")
    print("NEXT STEPS:")
    print(f"{'='*70}")
    print(f"\n1. Open {source_file} to see the English text")
    print(f"\n2. Copy the prompt below and send it to Claude:\n")

    prompt = generate_prompt(cantos)
    print(prompt)

    print(f"\n\n3. Claude will return JSON. Copy that JSON response.")
    print(f"\n4. Paste it below (press Enter twice when done):\n")

    lines = []
    empty_count = 0
    while empty_count < 2:
        line = input()
        if line.strip() == '':
            empty_count += 1
        else:
            empty_count = 0
            lines.append(line)

    translation_json = '\n'.join(lines)

    try:
        translations = json.loads(translation_json)
        if not isinstance(translations, list):
            translations = [translations]
        return translations
    except json.JSONDecodeError as e:
        print(f"\nERROR: Invalid JSON. {e}")
        print("Please try again.")
        return None

def main():
    print("\n🕉  Ramayana Hebrew Translation Batch Orchestrator\n")

    # Get status
    remaining = get_remaining_cantos()
    translated = get_translated_canto_numbers()
    total_source = 76  # Book I has 76 cantos

    print(f"Status:")
    print(f"  Translated: {len(translated)} cantos")
    print(f"  Remaining: {len(remaining)} cantos")
    print(f"  Total in source: {total_source} cantos\n")

    if not remaining:
        print("✓ All cantos translated!")
        return

    # Create batches
    batches = create_batches(remaining, batch_size=5)
    print(f"Batches to translate: {len(batches)}\n")

    # Process batches
    current_cantos = load_hebrew_cantos()

    for batch_num, cantos in batches:
        print(f"\n{'#'*70}")
        print(f"# Batch {batch_num} of {len(batches)}")
        print(f"{'#'*70}")

        translations = None
        while translations is None:
            translations = prompt_for_translation(batch_num, cantos)

        # Merge translations
        current_cantos.extend(translations)
        save_hebrew_cantos(current_cantos)

        # Ask if continuing
        if batch_num < len(batches):
            response = input(f"\n✓ Batch {batch_num} saved. Continue to batch {batch_num + 1}? (y/n): ").strip().lower()
            if response != 'y':
                print(f"\nStopping. {len(batches) - batch_num} batches remaining.")
                print(f"Run this script again to continue.")
                break

    print("\n✅ Translation complete!")
    final_cantos = load_hebrew_cantos()
    print(f"Total items in _book1_he.json: {len(final_cantos)}")

if __name__ == '__main__':
    main()
