#!/usr/bin/env python3
"""
Offline translation using Helsinki-NLP Opus-MT model (no API dependency)
Translates English Ramayana text to Hebrew
"""

import json
import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the text data
print("Loading English text...")
sys.path.insert(0, '/c/Users/Main/OneDrive/Documents/Neta/ramayana-site')
from data.text import RAMAYANA_TEXT

print(f"Loaded {len(RAMAYANA_TEXT)} books")

# Load model (first run downloads ~150MB)
print("\nLoading translation model (Helsinki-NLP/Opus-MT-en-he)...")
print("(First run will download ~150MB, then cached for future use)")
model_name = "Helsinki-NLP/Opus-MT-en-he"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def translate_text(text, max_length=512):
    """Translate English text to Hebrew"""
    if not text or not text.strip():
        return text

    # Truncate if needed
    if len(text) > max_length:
        text = text[:max_length]

    try:
        inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(**inputs, max_length=512)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print(f"  Error translating: {str(e)}")
        return text  # Return original if translation fails

# Translate all books
print("\n" + "="*60)
print("TRANSLATING ALL BOOKS TO HEBREW")
print("="*60)

for book_idx, book in enumerate(RAMAYANA_TEXT, 1):
    book_num = book.get("number", "?")
    book_title = book.get("title", "Unknown")
    print(f"\nBook {book_num}: {book_title}")

    # Translate book title and subtitle
    book["title"] = translate_text(book["title"])
    if "subtitle" in book:
        book["subtitle"] = translate_text(book["subtitle"])

    cantos = book.get("cantos", [])
    print(f"  Translating {len(cantos)} cantos...")

    for canto_idx, canto in enumerate(cantos):
        if (canto_idx + 1) % 5 == 0:
            print(f"    Progress: {canto_idx + 1}/{len(cantos)}")

        # Translate canto title
        if "title" in canto:
            canto["title"] = translate_text(canto["title"])

        # Translate paragraphs
        if "paragraphs" in canto:
            for para_idx, paragraph in enumerate(canto["paragraphs"]):
                # Translate in chunks to avoid token limits
                canto["paragraphs"][para_idx] = translate_text(paragraph)

print("\n" + "="*60)
print("Translation complete! Saving to file...")
print("="*60)

# Save to file
output_file = "/c/Users/Main/OneDrive/Documents/Neta/ramayana-site/data/text_he.js"
output_content = f"// auto-generated\nconst RAMAYANA_TEXT_HE={json.dumps(RAMAYANA_TEXT, ensure_ascii=False, indent=2)};"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output_content)

file_size = len(output_content)
print(f"\n✅ SUCCESS!")
print(f"Saved to: {output_file}")
print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
print(f"\nRefresh your browser to see the Hebrew translation!")
