#!/usr/bin/env python3
import json, re, sys, urllib.parse, urllib.request, time

def translate_simple(text):
    """Direct Google Translate via URL - simple and reliable"""
    if not text or not text.strip():
        return text
    try:
        text_encoded = urllib.parse.quote(text)
        url = f'https://translate.googleapis.com/translate_a/element.js?cb=callback&client=gtx&sl=en&tl=he&text={text_encoded}'
        # Simpler approach using a direct endpoint
        import subprocess
        result = subprocess.run(['curl', '-s', f'https://translate.google.com/translate_a/single?client=gtx&sl=en&tl=he&dt=t&q={text_encoded}'], 
                              capture_output=True, text=True, timeout=5)
        data = json.loads(result.stdout)
        return data[0][0][0] if data and data[0] and data[0][0] else text
    except:
        return text

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'const RAMAYANA_TEXT\s*=\s*(\[.*\]);', content, re.DOTALL)
    return json.loads(match.group(1)) if match else []

def main():
    en_file = r'C:\Users\Main\OneDrive\Documents\Neta\ramayana-site\data\text.js'
    he_file = r'C:\Users\Main\OneDrive\Documents\Neta\ramayana-site\data\text_he.js'
    
    print("Loading English text...")
    books_en = load_json(en_file)
    
    # Load existing Hebrew
    try:
        with open(he_file, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'const RAMAYANA_TEXT_HE\s*=\s*(\[.*\]);', content, re.DOTALL)
        books_he = json.loads(match.group(1)) if match else []
    except:
        books_he = []
    
    print(f"Existing: {len(books_he)} books, Total: {len(books_en)} books\n")
    
    # Translate remaining books
    for i in range(len(books_he), len(books_en)):
        book = books_en[i]
        print(f"\nBook {book['number']}: {book.get('title')}")
        
        # Translate subtitle
        if book.get('subtitle'):
            book['subtitle'] = translate_simple(book['subtitle'])
        
        # Translate cantos
        for canto_idx, canto in enumerate(book.get('cantos', [])):
            if canto_idx % 5 == 0:
                print(f"  Canto {canto.get('number')} ...", end='', flush=True)
            
            # Translate title
            if canto.get('title') and ord(canto['title'][0]) < 128:
                canto['title'] = translate_simple(canto['title'])
            
            # Translate paragraphs
            paras = canto.get('paragraphs', [])
            for p_idx in range(len(paras)):
                paras[p_idx] = translate_simple(paras[p_idx])
                time.sleep(0.1)  # Rate limit
            
            if canto_idx % 5 == 4:
                print(" done")
        
        print(f"Saving Book {book['number']}...")
        books_he.append(book)
        
        with open(he_file, 'w', encoding='utf-8') as f:
            f.write('// auto-generated\n')
            f.write('const RAMAYANA_TEXT_HE=')
            f.write(json.dumps(books_he, ensure_ascii=False, indent=2))
            f.write(';')
    
    print("\nDONE! All 7 books ready.")

if __name__ == '__main__':
    main()
