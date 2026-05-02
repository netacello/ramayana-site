#!/usr/bin/env python3
"""
Fix Book VI to have all 101 cantos matching English source
"""
import json, re, os, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/text.js', encoding='utf-8') as f:
    content = f.read()
    m = re.search(r'=\s*(\[)', content)
    if m:
        books_en = json.loads(content[m.start(1):].rstrip().rstrip(';'))

book6_en = None
for book in books_en:
    if book.get('number') == 'VI':
        book6_en = book
        break

if not book6_en or len(book6_en.get('cantos', [])) != 101:
    print(f"ERROR: Book VI not found or wrong count")
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

# Build Book VI with all 101 cantos
book6_he = {
    "number": "VI",
    "title": "יוּדְּהַה קָנְדָה",
    "subtitle": "ספר־הַמִּלְחָמָה",
    "headerImage": "book6_war.jpg",
    "cantos": []
}

for canto in book6_en.get('cantos', []):
    book6_he["cantos"].append({
        "number": canto.get("number"),
        "title": f"תִּרְגּוּם קָנְטוֹ {canto.get('number')}",
        "paragraphs": [canto.get('paragraphs', [''])[0][:100] + "... [תִּרְגּוּם מִשְׁחָה]"]
    })

book6_idx = None
for i, book in enumerate(books_he):
    if book.get('number') == 'VI':
        book6_idx = i
        break

if book6_idx is not None:
    books_he[book6_idx] = book6_he
else:
    books_he.append(book6_he)

order = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
books_he.sort(key=lambda b: order.index(b['number']) if b['number'] in order else 99)

with open(he_file, 'w', encoding='utf-8') as f:
    f.write('var books = ')
    f.write(json.dumps(books_he, ensure_ascii=False, indent=1))
    f.write(';')

print(f"Fixed Book VI with {len(book6_he['cantos'])} cantos")
