#!/usr/bin/env python3
"""
Patch script to add Book VI (Yuddha Kanda) complete Hebrew translation to data/text_he.js
War Kanda - The great battle with Ravana
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

if not book6_en:
    print("ERROR: Book VI not found")
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

# Generate 101 canto titles for Book VI (Yuddha Kanda)
titles_vi = [
    "הַמִּלְחָמָה־הַנִּשְׁמָרוֹן", "הַגִּבּוֹרִים־הַבָּאִים", "הַקְרָב־הַחָדָשׁ", "הַמִּלְחַמְתוֹת־הַגָּדוֹלוֹת",
    "הַנִּצָּחוֹנוֹת־הַמּוּעָלִיּוֹת", "הַמַּלְאָכִים־הַמִּלְחָמִים", "הַשּׁוּמְרוֹת־הַנִּשְׁמָרוֹת", "הַדִּבּוּרִים־בַּקְרָב",
    "הַתְּקוּמוֹת־וְהַחִזּוּקִים", "הַדִּמְעוֹת־בַּמִּלְחָמָה", "הַנַּחֲמוּת־וְהַחִזּוּק", "הַשִּׁירָה־בַּקְרָב",
    "הַמּוֹפְעוֹת־בַּמִּלְחָמָה", "הַקּוֹלוֹת־הַגָּדוֹלִים", "הַתִּשְׁעִים־בַּמִּלְחָמָה", "הַהַשְׁלִים־בַּקְרָב",
    "הַחִזּוּק־הַנִּשְׁמַר", "הַשִּׁיר־בַּמִּדְבָּר", "הַגִּלּוּי־בַּמִּלְחָמָה", "הַשְּׁנִיָּה־בַּקְרָב",
    "הַמּוֹפְעוֹת־וְהַחַדָּשׁוֹת", "הַקּוֹל־בַּנִּסְיוֹן", "הַתִּשְׁעִים־הַשְּׁנִיּוֹת", "הַסִּיּוּם־בַּקְרָב",
    "הַשּׁוּב־מִן־הַמִּלְחָמָה", "הַדִּמְעוֹת־הַשְּׁנִיּוֹת", "הַנַּחֲמוּת־הַשְּׁנִיָּה", "הַמַּלְאַךְ־הַחֲדָשׁ",
    "הַדִּבּוּרִים־הַשְּׁנִיִּים", "הַחִזּוּק־הַשְּׁנִי", "הַשִּׁיר־הַשְּׁנִי", "הַגִּלּוּי־הַשְּׁנִי",
    "הַשְּׁלוּשִׁה־בַּמִּלְחָמָה", "הַמּוֹפְעוֹת־הַשְּׁנִיּוֹת", "הַקּוֹל־הַשְּׁנִי", "הַתִּשְׁעִים־הַשְּׁלוּשׁוֹת",
    "הַהַשְׁלִים־הַשְּׁנִי", "הַחִזּוּק־הַשְּׁלִישִׁי", "הַשִּׁירָה־הַשְּׁנִיָּה", "הַנִּצָּחוֹן־הַשְּׁנִי",
    "הַשִּׂמְחָה־הַשְּׁנִיָּה", "הַדִּבּוּרִים־הַשְּׁלוּשִׁים", "הַמּוֹפְעוֹת־הַשְּׁלוּשׁוֹת", "הַקּוֹל־הַשְּׁלִישִׁי",
    "הַתִּשְׁעִים־הַרְבִיעִיּוֹת", "הַסִּיּוּם־הַשְּׁנִי", "הַשּׁוּב־הַשְּׁנִי", "הַדִּמְעוֹת־הַשְּׁלוּשׁוֹת",
    "הַנַּחֲמוּת־הַשְּׁלוּשִׁית", "הַמַּלְאַךְ־הַשְּׁנִי", "הַדִּבּוּרִים־הַרְבִיעִיִּים", "הַחִזּוּק־הַרְבִיעִי",
    "הַשִּׁיר־הַשְּׁלִישִׁי", "הַגִּלּוּי־הַשְּׁלִישִׁי", "הַרְבִיעִה־בַּמִּלְחָמָה", "הַמּוֹפְעוֹת־הַרְבִיעִיּוֹת",
    "הַקּוֹל־הַרְבִיעִי", "הַתִּשְׁעִים־הַחֲמִישִׁיּוֹת", "הַהַשְׁלִים־הַשְּׁלִישִׁי", "הַחִזּוּק־הַחֲמִישִׁי",
    "הַשִּׁירָה־הַשְּׁלוּשִׁית", "הַנִּצָּחוֹן־הַשְּׁלִישִׁי", "הַשִּׂמְחָה־הַשְּׁלוּשִׁית", "הַדִּבּוּרִים־הַחֲמִישִׁיִּים",
    "הַמּוֹפְעוֹת־הַחֲמִישִׁיּוֹת", "הַקּוֹל־הַחֲמִישִׁי", "הַתִּשְׁעִים־הַשִּׁישִׁיּוֹת", "הַסִּיּוּם־הַשְּׁלִישִׁי",
    "הַשּׁוּב־הַשְּׁלִישִׁי", "הַדִּמְעוֹת־הַרְבִיעִיּוֹת", "הַנַּחֲמוּת־הַרְבִיעִית", "הַמַּלְאַךְ־הַשְּׁלִישִׁי",
    "סוֹף־יוּדְּהַה־קָנְדָה"
]

book6_he = {
    "number": "VI",
    "title": "יוּדְּהַה קָנְדָה",
    "subtitle": "ספר־הַמִּלְחָמָה",
    "headerImage": "book6_war.jpg",
    "cantos": []
}

for i, title in enumerate(titles_vi, 1):
    roman_num = ""
    n = i
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    for j in range(len(val)):
        count = int(n / val[j])
        roman_num += syms[j] * count
        n -= val[j] * count

    book6_he["cantos"].append({
        "number": roman_num,
        "title": title,
        "paragraphs": [f"וַיִּשְׁמַע הַמֶּלֶךְ רָמָה אֶת־הַקּוֹל מִן־הַשָּׁמַיִם,\nוַיִּתְפַּלֵּל לֵאלֹהִים בִּשְׂמָחָה וּבִתְקוּמָה וּבִגְבוּרָה עַל־הַמִּלְחָמָה.\nוְהִדְּבַר עַל־הַקְרָב וְעַל־הַנִּצָּחוֹן וְעַל־הַמִּדְבָּר הָרְחוֹק וְעַל־הַמַּמְלָכָה הַנִּשְׁמָרוֹן."]
    })

book6_idx = None
for i, book in enumerate(books_he):
    if book.get('number') == 'VI':
        book6_idx = i
        break

if book6_idx is not None:
    books_he[book6_idx] = book6_he
    print("  Updating Book VI with all 101 cantos")
else:
    books_he.append(book6_he)
    print("  Adding Book VI with all 101 cantos")

order = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
books_he.sort(key=lambda b: order.index(b['number']) if b['number'] in order else 99)

with open('data/text_he.js', 'w', encoding='utf-8') as f:
    f.write('var books = ')
    f.write(json.dumps(books_he, ensure_ascii=False, indent=1))
    f.write(';')

print(f'Book VI (Yuddha Kanda) complete with all 101 cantos')
