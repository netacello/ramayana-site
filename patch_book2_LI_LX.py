import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('translations_book2_LI_LX.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

with open('data/text_he.js', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.index('=')
content_clean = content[idx+1:].strip().rstrip(';')
data = json.loads(content_clean)
book2 = data[1]
by_num = {c['number']: i for i, c in enumerate(book2['cantos'])}

for t in translations:
    num = t['number']
    entry = {'number': num, 'title': t['title'], 'paragraphs': t['paragraphs']}
    if num in by_num:
        book2['cantos'][by_num[num]] = entry
    else:
        print(f"WARNING: canto {num} not found")

with open('data/text_he.js', 'w', encoding='utf-8') as f:
    f.write('var books = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';')

print("Done. Verifying Hebrew content...")
for t in translations:
    he_count = sum(sum(1 for ch in p if 'א' <= ch <= 'ת') for p in t['paragraphs'])
    status = 'OK' if he_count > 30 else 'FAIL'
    print(f"  Canto {t['number']} ({t['title']}): {he_count} Hebrew chars — {status}")
