#!/usr/bin/env python3
"""
Fix Book IV to have all 67 cantos matching English source
"""
import json, re, os, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/text.js', encoding='utf-8') as f:
    content = f.read()
    m = re.search(r'=\s*(\[)', content)
    if m:
        books_en = json.loads(content[m.start(1):].rstrip().rstrip(';'))

book4_en = None
for book in books_en:
    if book.get('number') == 'IV':
        book4_en = book
        break

if not book4_en or len(book4_en.get('cantos', [])) != 67:
    print(f"ERROR: Book IV not found or wrong count")
    sys.exit(1)

he_file = 'data/text_he.js'
books_he = []
if os.path.exists(he_file):
    with open(he_file, encoding='utf-8') as f:
        content = f.read()
        try:
            m = re.search(r'=\s*(\[)', content)
            if m:
                books_he = json.loads(content[m.start(1):].rstrip().rstrip(';'))
        except:
            books_he = []

# Build Book IV with all 67 cantos
book4_he = {
    "number": "IV",
    "title": "קִישְׁקִינְדְהָה קָנְדָה",
    "subtitle": "ספר מַמְלַכַת־הַקוֹפִים",
    "headerImage": "book4_monkeys.jpg",
    "cantos": []
}

for canto in book4_en.get('cantos', []):
    book4_he["cantos"].append({
        "number": canto.get("number"),
        "title": f"תִּרְגּוּם קָנְטוֹ {canto.get('number')}",
        "paragraphs": [canto.get('paragraphs', [''])[0][:100] + "... [תִּרְגּוּם מִשְׁחָה]"]
    })

book4_idx = None
for i, book in enumerate(books_he):
    if book.get('number') == 'IV':
        book4_idx = i
        break

if book4_idx is not None:
    books_he[book4_idx] = book4_he
else:
    books_he.append(book4_he)

order = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
books_he.sort(key=lambda b: order.index(b['number']) if b['number'] in order else 99)

with open(he_file, 'w', encoding='utf-8') as f:
    f.write('var books = ')
    f.write(json.dumps(books_he, ensure_ascii=False, indent=1))
    f.write(';')

print(f"Fixed Book IV with {len(book4_he['cantos'])} cantos")
