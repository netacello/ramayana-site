#!/usr/bin/env python3
"""
Translation using MyMemory Translation API (free, no authentication needed)
More reliable than google-trans-new which is blocked
"""

import json
import time
import sys
import requests
from urllib.parse import quote

# Load the text data
print("Loading English text...")
with open('data/text.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    books_en = json.loads(content[start:end])

print(f"Loaded {len(books_en)} books")

# MyMemory API endpoint
API_URL = "https://api.mymemory.translated.net/get"

stats = {
    'total': 0,
    'success': 0,
    'failed': 0,
    'start_time': time.time()
}

def translate_mymemory(text):
    """Translate using MyMemory API with retry logic"""
    if not text or len(text.strip()) == 0:
        return text

    # Limit length to avoid URL limits
    if len(text) > 500:
        parts = [text[i:i+500] for i in range(0, len(text), 500)]
        return ''.join([translate_mymemory(part) for part in parts])

    stats['total'] += 1

    for attempt in range(3):
        try:
            params = {
                'q': text,
                'langpair': 'en|he'
            }
            response = requests.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('responseStatus') == 200:
                translated = data.get('responseData', {}).get('translatedText', '')
                if translated:
                    stats['success'] += 1
                    return translated

            # If failed, retry
            if attempt < 2:
                wait_time = (attempt + 1) * 2
                print(f"      Retry {attempt + 1}/3 (waiting {wait_time}s)")
                time.sleep(wait_time)

        except Exception as e:
            if attempt < 2:
                wait_time = (attempt + 1) * 2
                print(f"      Error: {str(e)[:60]} - Retry {attempt + 1}/3")
                time.sleep(wait_time)
            else:
                print(f"      FAILED: {str(e)[:80]}")

    stats['failed'] += 1
    return text

# Translate all books
print("\n" + "="*70)
print("TRANSLATING WITH MyMemory API")
print("="*70)

for book_idx, book in enumerate(books_en, 1):
    book_num = book.get("number", "?")
    book_title = book.get("title", "Unknown")
    print(f"\nBook {book_num}: {book_title}")

    # Translate title and subtitle
    book["title"] = translate_mymemory(book["title"])
    if "subtitle" in book:
        book["subtitle"] = translate_mymemory(book["subtitle"])

    cantos = book.get("cantos", [])
    print(f"  Translating {len(cantos)} cantos...")

    for canto_idx, canto in enumerate(cantos):
        if (canto_idx + 1) % 5 == 0:
            elapsed = time.time() - stats['start_time']
            rate = stats['success'] / (elapsed/60) if elapsed > 0 else 0
            print(f"    Progress {canto_idx + 1}/{len(cantos)} | Elapsed: {elapsed/60:.1f}m | Rate: {rate:.0f}/min | Success: {stats['success']}, Failed: {stats['failed']}")

        # Translate canto title
        if "title" in canto:
            canto["title"] = translate_mymemory(canto["title"])

        # Translate paragraphs
        if "paragraphs" in canto:
            for para in canto["paragraphs"]:
                translate_mymemory(para)

print("\n" + "="*70)
print("Translation complete! Saving...")
print("="*70)

# Save to file
output_file = "data/text_he.js"
output_content = f"// auto-generated\nconst RAMAYANA_TEXT_HE={json.dumps(books_en, ensure_ascii=False, indent=2)};"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output_content)

file_size = len(output_content)
elapsed = time.time() - stats['start_time']

print(f"\n✅ COMPLETE!")
print(f"Saved: {output_file}")
print(f"Size: {file_size/1024/1024:.1f} MB")
print(f"Time: {elapsed/60:.1f} minutes")
print(f"Stats: {stats['success']} success, {stats['failed']} failed / {stats['total']} total")
print(f"\nRefresh browser now!")
