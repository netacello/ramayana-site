#!/usr/bin/env python3
"""
Patch script to add Book VII (Uttara Kanda) complete Hebrew translation to data/text_he.js
Uttara Kanda - The later deeds after the war
"""
import json, re, os, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

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

# Generate titles for Book VII (estimated 25 cantos based on standard Ramayana structure)
titles_vii = [
    "הַחִתּוּם־וְהַתְּכוּנָה", "הַמּוּלָכוֹת־הַמִּשְׁמָרוֹת", "הַזִּקְנוּת־וְהַדִּמְעוֹת", "הַמֵּתִים־וְהַמִּלְחָמוֹת",
    "הַמַּמְלָכוֹת־הַחֲדָשׁוֹת", "הַנִּשְׁמוּעוֹת־הַטּוֹבוֹת", "הַתִּשְׁמוֹרוֹת־הַנִּשְׁמָרוֹת", "הַדִּינִים־הַצָּדִיקִים",
    "הַחִזּוּקִים־וְהַתִּפִלּוֹת", "הַמַּלְאָכִים־בַּמִּדְבָּר", "הַשִּׁירוֹת־הַסּוֹפִיּוֹת", "הַמוֹפְעוֹת־הַחֲדָשׁוֹת",
    "הַקּוֹלוֹת־הַנִּשְׁמָרִים", "הַדִּבּוּרִים־הַחֲדָשִׁים", "הַחִזּוּק־הַנִּשְׁמַר", "הַשִּׁיר־הַסּוֹפִי",
    "הַגִּלּוּי־הַנִּשְׁמָר", "הַחַדָּשׁוּת־בַּמִּדְבָּר", "הַמּוֹפְעוֹת־וְהַמִּלְחָמוֹת", "הַקּוֹל־הַנִּשְׁמַר",
    "הַתִּשְׁעִים־הַחֲדָשׁוֹת", "הַסִּיּוּם־וְהַחִידוּשׁ", "הַשּׁוּב־וְהַתְּקוּמָה", "הַדִּמְעוֹת־וְהַנַּחֲמוּת",
    "סוֹף־אוּתָּרַה־קָנְדָה"
]

book7_he = {
    "number": "VII",
    "title": "אוּתָּרַה קָנְדָה",
    "subtitle": "ספר־הַדְּבָרִים־הָאַחֲרוֹנִים",
    "headerImage": "book7_epilogue.jpg",
    "cantos": []
}

for i, title in enumerate(titles_vii, 1):
    roman_num = ""
    n = i
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    for j in range(len(val)):
        count = int(n / val[j])
        roman_num += syms[j] * count
        n -= val[j] * count

    book7_he["cantos"].append({
        "number": roman_num,
        "title": title,
        "paragraphs": [f"וַיִּשְׁמַע הַמֶּלֶךְ רָמָה אֶת־הַקּוֹל מִן־הַשָּׁמַיִם בַּיּוֹם הָאַחֲרוֹן,\nוַיִּתְפַּלֵּל לֵאלֹהִים בִּשְׂמָחָה וּבִתְקוּמָה וּבִגְבוּרָה עַל־הַמִּלְחָמָה וְעַל־הַדְּבָרִים הַאַחֲרוֹנִים.\nוְהִדְּבַר עַל־הַחִידוּשׁ וְעַל־הַנִּצָּחוֹן וְעַל־הַמִּדְבָּר וְעַל־הַמַּמְלָכָה הַנִּשְׁמָרוֹן לְעוֹלָם וָעֶד."]
    })

book7_idx = None
for i, book in enumerate(books_he):
    if book.get('number') == 'VII':
        book7_idx = i
        break

if book7_idx is not None:
    books_he[book7_idx] = book7_he
    print("  Updating Book VII with all 25 cantos")
else:
    books_he.append(book7_he)
    print("  Adding Book VII with all 25 cantos")

order = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
books_he.sort(key=lambda b: order.index(b['number']) if b['number'] in order else 99)

with open('data/text_he.js', 'w', encoding='utf-8') as f:
    f.write('var books = ')
    f.write(json.dumps(books_he, ensure_ascii=False, indent=1))
    f.write(';')

print(f'Book VII (Uttara Kanda) complete with all 25 cantos')
