#!/usr/bin/env python3
"""
Translation using Google Cloud Translation API (official, fast, reliable)
"""

import json
import time
import os
import requests

# Set API key
API_KEY = "REDACTED_GOOGLE_API_KEY"

# Load English text
print("Loading English Ramayana text...")
with open('data/text.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    books_en = json.loads(content[start:end])

print(f"[OK] Loaded {len(books_en)} books")

# Initialize Google Cloud Translation API
print("Initializing Google Cloud Translation API...")

stats = {
    'total_chars': 0,
    'start_time': time.time(),
    'books_done': 0
}

def translate_gcp(text):
    """Translate using Google Cloud Translation API"""
    if not text or len(text.strip()) == 0:
        return text

    try:
        url = "https://translation.googleapis.com/language/translate/v2"
        payload = {
            'q': text,
            'source_language': 'en',
            'target_language': 'he',
            'key': API_KEY
        }
        response = requests.post(url, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            translated = data['data']['translations'][0]['translatedText']
            stats['total_chars'] += len(text)
            return translated
        else:
            print(f"    Error {response.status_code}: {response.text[:100]}")
            return text
    except Exception as e:
        print(f"    Error: {str(e)[:100]}")
        return text

# Translate all books
print("\n" + "="*70)
print("TRANSLATING TO HEBREW (Google Cloud Translation API)")
print("="*70)

for book_idx, book in enumerate(books_en, 1):
    book_num = book.get("number", "?")
    book_title = book.get("title", "Unknown")
    print(f"\nBook {book_num}: {book_title}")

    # Translate title and subtitle
    book["title"] = translate_gcp(book["title"])
    if "subtitle" in book:
        book["subtitle"] = translate_gcp(book["subtitle"])

    cantos = book.get("cantos", [])
    print(f"  Translating {len(cantos)} cantos...")

    for canto_idx, canto in enumerate(cantos):
        if (canto_idx + 1) % 10 == 0 or canto_idx == 0:
            elapsed = time.time() - stats['start_time']
            rate = stats['total_chars'] / (elapsed/60) if elapsed > 0 else 0
            print(f"    Progress: {canto_idx + 1}/{len(cantos)} | Time: {elapsed/60:.1f}m | Chars: {stats['total_chars']:,} | Rate: {rate:,.0f} chars/min")

        # Translate canto title
        if "title" in canto:
            canto["title"] = translate_gcp(canto["title"])

        # Translate paragraphs
        if "paragraphs" in canto:
            for para_idx, paragraph in enumerate(canto["paragraphs"]):
                canto["paragraphs"][para_idx] = translate_gcp(paragraph)

    stats['books_done'] += 1

print("\n" + "="*70)
print("Translation complete! Saving to file...")
print("="*70)

# Save to file
output_file = "data/text_he.js"
output_content = f"// auto-generated\nconst RAMAYANA_TEXT_HE={json.dumps(books_en, ensure_ascii=False, indent=2)};"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output_content)

file_size = len(output_content)
elapsed = time.time() - stats['start_time']

print(f"\n[SUCCESS] Translation complete!")
print(f"Saved to: {output_file}")
print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
print(f"Total time: {elapsed/60:.1f} minutes")
print(f"Characters translated: {stats['total_chars']:,}")
print(f"Books completed: {stats['books_done']}/7")
print(f"\n[DONE] Refresh your browser to see the full Hebrew translation!")
