#!/usr/bin/env python3
import json, re, urllib.request, urllib.parse, time, sys

def translate_text(text):
    """Translate using Google Translate API directly"""
    if not text or len(text.strip()) < 2:
        return text
    try:
        # URL encode the text
        params = urllib.parse.urlencode({'client': 'gtx', 'sl': 'en', 'tl': 'he', 'dt': 't', 'q': text})
        url = f'https://translate.googleapis.com/translate_a/single?{params}'
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data[0][0][0] if data and data[0] and data[0][0] else text
    except Exception as e:
        print(f"    Translation error: {text[:30]}...")
        return text

def load_english():
    with open(r'C:\Users\Main\OneDrive\Documents\Neta\ramayana-site\data\text.js', 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'const RAMAYANA_TEXT\s*=\s*(\[.*\]);', content, re.DOTALL)
    return json.loads(match.group(1)) if match else []

# Load English
print("Loading...")
books = load_english()

# Get Hebrew versions
try:
    with open(r'C:\Users\Main\OneDrive\Documents\Neta\ramayana-site\data\text_he.js', 'r', encoding='utf-8') as f:
        match = re.search(r'const RAMAYANA_TEXT_HE\s*=\s*(\[.*\]);', f.read(), re.DOTALL)
    he_books = json.loads(match.group(1)) if match else []
except:
    he_books = []

print(f"Starting from book {len(he_books) + 1}...\n")

# Translate each book
for i in range(len(he_books), len(books)):
    book = books[i]
    print(f"Book {book['number']}: {book.get('title', '?')}")
    
    # Translate subtitle
    if book.get('subtitle'):
        book['subtitle'] = translate_text(book['subtitle'])
        time.sleep(0.2)
    
    # Translate cantos
    for c_idx, canto in enumerate(book.get('cantos', [])):
        canto_num = canto.get('number', '?')
        
        # Translate title
        if canto.get('title') and ord(canto['title'][0]) < 128:
            canto['title'] = translate_text(canto['title'])
            time.sleep(0.2)
        
        # Translate paragraphs
        for p_idx in range(len(canto.get('paragraphs', []))):
            canto['paragraphs'][p_idx] = translate_text(canto['paragraphs'][p_idx])
            time.sleep(0.15)
        
        if (c_idx + 1) % 3 == 0:
            print(f"  Canto {c_idx + 1}/{len(book['cantos'])} done")
    
    he_books.append(book)
    
    # Save after each book
    with open(r'C:\Users\Main\OneDrive\Documents\Neta\ramayana-site\data\text_he.js', 'w', encoding='utf-8') as f:
        f.write('// auto-generated\n')
        f.write('const RAMAYANA_TEXT_HE=')
        f.write(json.dumps(he_books, ensure_ascii=False, indent=2))
        f.write(';')
    print(f"  Saved Book {book['number']}\n")

print("ALL DONE! Refresh browser now.")
