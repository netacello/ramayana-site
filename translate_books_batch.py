#!/usr/bin/env python3
import json, re, sys
from google_trans_new import google_translator

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

translator = google_translator()

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'const RAMAYANA_TEXT\s*=\s*(\[.*\]);', content, re.DOTALL)
    return json.loads(match.group(1)) if match else []

def translate_batch(texts):
    """Translate multiple texts at once (more efficient)"""
    if not texts:
        return texts
    try:
        # Join with delimiter
        batch = '\n|||SPLIT|||\n'.join(texts)
        result = translator.translate(batch, lang_src='en', lang_tgt='he')
        # Split back
        return result.split('\n|||SPLIT|||\n') if result else texts
    except:
        return texts

def translate_book(book, start_canto_idx=0):
    """Translate a single book efficiently"""
    print(f"\nBook {book['number']}: {book.get('title', '?')}")
    
    for canto_idx, canto in enumerate(book['cantos']):
        if canto_idx < start_canto_idx:
            continue
            
        # Batch translate paragraphs
        paras = canto.get('paragraphs', [])
        if paras:
            print(f"  Canto {canto.get('number', '?')}: {len(paras)} paragraphs...", end='', flush=True)
            canto['paragraphs'] = translate_batch(paras)
            print(" done")
        
        # Translate title if needed
        if canto.get('title') and ord(canto['title'][0]) < 128:
            canto['title'] = translator.translate(canto['title'], lang_src='en', lang_tgt='he') or canto['title']
    
    return book

def main():
    en_file = r'C:\Users\Main\OneDrive\Documents\Neta\ramayana-site\data\text.js'
    he_file = r'C:\Users\Main\OneDrive\Documents\Neta\ramayana-site\data\text_he.js'
    
    print("Loading English text...")
    books_en = load_json(en_file)
    
    # Load existing Hebrew data (Book I already done)
    try:
        with open(he_file, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'const RAMAYANA_TEXT_HE\s*=\s*(\[.*\]);', content, re.DOTALL)
        books_he = json.loads(match.group(1)) if match else []
    except:
        books_he = []
    
    print(f"Existing Hebrew books: {len(books_he)}")
    print(f"English books: {len(books_en)}\n")
    
    # Translate books II onwards
    start_from_book = len(books_he)
    for i in range(start_from_book, len(books_en)):
        books_en[i] = translate_book(books_en[i])
        books_he.append(books_en[i]) if i >= len(books_he) else books_he.__setitem__(i, books_en[i])
        
        # Save after each book
        print(f"Saving Book {books_en[i]['number']}...")
        with open(he_file, 'w', encoding='utf-8') as f:
            f.write('// auto-generated\n')
            f.write('const RAMAYANA_TEXT_HE=')
            f.write(json.dumps(books_he, ensure_ascii=False, indent=2))
            f.write(';')
    
    print("\nDONE! All books translated.")
    print("Refresh browser to see all 7 books in Hebrew!")

if __name__ == '__main__':
    main()
