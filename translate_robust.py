#!/usr/bin/env python3
"""
Robust translation using google-trans-new with retry logic, batching, and error handling
"""

import json
import time
import sys
from google_trans_new import google_translator

# Load the text data directly from the file
print("Loading English text...")
with open('data/text.js', 'r', encoding='utf-8') as f:
    content = f.read()
    # Extract the JSON from const RAMAYANA_TEXT=[...];
    start = content.find('[')
    end = content.rfind(']') + 1
    books_en = json.loads(content[start:end])

print(f"Loaded {len(books_en)} books")

# Initialize translator with session reuse
translator = google_translator()

# Track stats
stats = {
    'total_paragraphs': 0,
    'successful': 0,
    'failed': 0,
    'start_time': time.time()
}

def translate_with_retry(text, max_retries=5, backoff=2):
    """Translate text with exponential backoff retry logic"""
    if not text or not text.strip():
        return text

    # Limit text length to avoid token limits
    max_len = 500
    if len(text) > max_len:
        # Split and translate parts
        parts = [text[i:i+max_len] for i in range(0, len(text), max_len)]
        translated_parts = []
        for part in parts:
            translated_parts.append(translate_with_retry(part, max_retries, backoff))
        return ''.join(translated_parts)

    for attempt in range(max_retries):
        try:
            result = translator.translate(text, lang_src='en', lang_tgt='he')
            if result:
                stats['successful'] += 1
                return result
            else:
                # Translation returned empty, try again
                if attempt < max_retries - 1:
                    wait_time = backoff ** attempt
                    print(f"    Retry {attempt + 1}/{max_retries} (empty result, waiting {wait_time}s)")
                    time.sleep(wait_time)
                continue
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = backoff ** attempt
                print(f"    Retry {attempt + 1}/{max_retries} ({str(e)[:50]}, waiting {wait_time}s)")
                time.sleep(wait_time)
            else:
                print(f"    FAILED after {max_retries} attempts: {str(e)[:100]}")
                stats['failed'] += 1
                return text  # Return original on final failure

    stats['failed'] += 1
    return text

# Translate all books
print("\n" + "="*70)
print("TRANSLATING ALL BOOKS TO HEBREW (WITH RETRY LOGIC)")
print("="*70)

for book_idx, book in enumerate(books_en, 1):
    book_num = book.get("number", "?")
    book_title = book.get("title", "Unknown")
    print(f"\nBook {book_num}: {book_title}")

    # Translate book title and subtitle
    print(f"  Translating title and subtitle...")
    book["title"] = translate_with_retry(book["title"])
    if "subtitle" in book:
        book["subtitle"] = translate_with_retry(book["subtitle"])

    cantos = book.get("cantos", [])
    print(f"  Translating {len(cantos)} cantos...")

    for canto_idx, canto in enumerate(cantos):
        if (canto_idx + 1) % 5 == 0 or canto_idx == 0:
            elapsed = time.time() - stats['start_time']
            print(f"    Canto {canto_idx + 1}/{len(cantos)} - Elapsed: {elapsed/60:.1f}min - Success: {stats['successful']}, Failed: {stats['failed']}")

        # Translate canto title
        if "title" in canto:
            canto["title"] = translate_with_retry(canto["title"])

        # Translate paragraphs
        if "paragraphs" in canto:
            for para_idx, paragraph in enumerate(canto["paragraphs"]):
                stats['total_paragraphs'] += 1
                canto["paragraphs"][para_idx] = translate_with_retry(paragraph)

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

print(f"\n✅ SUCCESS!")
print(f"Saved to: {output_file}")
print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
print(f"Total time: {elapsed/60:.1f} minutes")
print(f"Paragraphs: {stats['total_paragraphs']} (Success: {stats['successful']}, Failed: {stats['failed']})")
print(f"\nRefresh your browser to see the Hebrew translation!")
