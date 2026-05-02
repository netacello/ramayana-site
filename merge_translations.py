#!/usr/bin/env python3
"""
Merge translated batches back into text_he.js
Run this after you've translated some batches with your tool
"""

import json
import os
import re
from pathlib import Path

print("Loading current text_he.js...")
with open('data/text_he.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    books_he = json.loads(content[start:end])

# Find all translation batch files
batch_files = list(Path('.').glob('translations_batch_*.txt'))
print(f"Found {len(batch_files)} batch translation files")

if len(batch_files) == 0:
    print("No translation batch files found!")
    print("Create files named: translations_batch_[BOOK]_[CANTO].txt")
    exit(1)

# Process each batch file
merged_count = 0
for batch_file in sorted(batch_files):
    filename = batch_file.name

    # Parse filename: translations_batch_II_I.txt
    match = re.match(r'translations_batch_([IVX]+)_(.+)\.txt', filename)
    if not match:
        print(f"Skipping {filename} - wrong format")
        continue

    book_num = match.group(1)
    canto_num = match.group(2)

    # Find book and canto indices
    book_idx = None
    for i, book in enumerate(books_he):
        if book.get('number') == book_num:
            book_idx = i
            break

    if book_idx is None:
        print(f"Warning: Book {book_num} not found, skipping {filename}")
        continue

    # Find canto in book
    canto_idx = None
    cantos = books_he[book_idx].get('cantos', [])
    for i, canto in enumerate(cantos):
        if canto.get('number') == canto_num:
            canto_idx = i
            break

    if canto_idx is None:
        print(f"Warning: Canto {canto_num} in Book {book_num} not found, skipping")
        continue

    # Parse translated batch file
    with open(batch_file, 'r', encoding='utf-8') as f:
        batch_content = f.read()

    # Extract paragraphs from format: [1] text, [2] text, etc.
    paragraphs = []
    lines = batch_content.strip().split('\n')
    current_para = []

    for line in lines:
        match = re.match(r'^\[(\d+)\]\s*(.*)', line)
        if match:
            if current_para:
                paragraphs.append('\n'.join(current_para).strip())
            current_para = [match.group(2)]
        elif line.strip() and current_para:
            current_para.append(line)

    if current_para:
        paragraphs.append('\n'.join(current_para).strip())

    # Update canto
    canto = cantos[canto_idx]
    old_count = len(canto.get('paragraphs', []))

    if len(paragraphs) != old_count:
        print(f"Warning: {filename} has {len(paragraphs)} paragraphs but expected {old_count}")

    canto['paragraphs'] = paragraphs
    merged_count += 1
    print(f"[OK] Merged Book {book_num} Canto {canto_num} ({len(paragraphs)} paragraphs)")

print(f"\n[MERGED] {merged_count} batches integrated into text_he.js")

# Save updated file
output_file = "data/text_he.js"
output_content = f"// auto-generated\nconst RAMAYANA_TEXT_HE={json.dumps(books_he, ensure_ascii=False, indent=2)};"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output_content)

file_size = len(output_content)
print(f"[SAVED] {output_file} ({file_size/1024/1024:.2f} MB)")
print(f"\nDone! Refresh browser to see updates.")
