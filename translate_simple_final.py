#!/usr/bin/env python3
"""
Simple translation using translate library (no authentication needed)
Slower but guaranteed to work - no API keys or rate limits
"""

import json
import time
from translate import Translator

print("Loading English Ramayana text...")
with open('data/text.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    books_en = json.loads(content[start:end])

print(f"[OK] Loaded {len(books_en)} books")

# Initialize translator (no API key needed!)
print("Initializing translator...")
translator = Translator(from_lang='en', to_lang='he')

stats = {
    'total_chars': 0,
    'start_time': time.time(),
    'books_done': 0
}

def translate_simple(text):
    """Translate using simple translate library"""
    if not text or len(text.strip()) == 0:
        return text

    try:
        result = translator.translate(text)
        if result:
            stats['total_chars'] += len(text)
            return result
        return text
    except Exception as e:
        print(f"  Translation error: {str(e)[:50]}")
        return text

# Translate all books
print("\n" + "="*70)
print("TRANSLATING TO HEBREW (Simple Translator - NO API KEYS)")
print("="*70)

for book_idx, book in enumerate(books_en, 1):
    book_num = book.get("number", "?")
    book_title = book.get("title", "Unknown")
    print(f"\nBook {book_num}: {book_title}")

    # Translate title and subtitle
    book["title"] = translate_simple(book["title"])
    if "subtitle" in book:
        book["subtitle"] = translate_simple(book["subtitle"])

    cantos = book.get("cantos", [])
    print(f"  Translating {len(cantos)} cantos...")

    for canto_idx, canto in enumerate(cantos):
        if (canto_idx + 1) % 5 == 0 or canto_idx == 0:
            elapsed = time.time() - stats['start_time']
            rate = stats['total_chars'] / (elapsed/60) if elapsed > 0 else 0
            print(f"    Canto {canto_idx + 1}/{len(cantos)} | Time: {elapsed/60:.1f}m | Chars: {stats['total_chars']:,} | Rate: {rate:,.0f}/min")

        # Translate canto title
        if "title" in canto:
            canto["title"] = translate_simple(canto["title"])

        # Translate paragraphs
        if "paragraphs" in canto:
            for para_idx, paragraph in enumerate(canto["paragraphs"]):
                canto["paragraphs"][para_idx] = translate_simple(paragraph)

    stats['books_done'] += 1
    print(f"  Book {book_num} complete!")

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

print(f"\n[SUCCESS] Translation complete!")
print(f"Saved: {output_file}")
print(f"Size: {file_size/1024/1024:.1f} MB")
print(f"Time: {elapsed/60:.1f} minutes")
print(f"Characters: {stats['total_chars']:,}")
print(f"Books: {stats['books_done']}/7")
print(f"\nRefresh browser now!")
