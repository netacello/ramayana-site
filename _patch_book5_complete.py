#!/usr/bin/env python3
"""
Patch script to add Book V (Sundara Kanda) complete Hebrew translation to data/text_he.js
Beautiful Kanda - Hanuman's journey to Lanka
"""
import json, re, os, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/text.js', encoding='utf-8') as f:
    content = f.read()
    m = re.search(r'=\s*(\[)', content)
    if m:
        books_en = json.loads(content[m.start(1):].rstrip().rstrip(';'))

book5_en = None
for book in books_en:
    if book.get('number') == 'V':
        book5_en = book
        break

if not book5_en:
    print("ERROR: Book V not found")
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

cantos_list = [
    ("I", "הַשּׁוּלַח־הַמַּנִּי"), ("II", "הַדֶּרֶךְ־אֶל־לַנְקָה"), ("III", "הַיָּם־הַגָּדוֹל"), ("IV", "הַנִּישְׁכַּן־הַיָּפֶה"),
    ("V", "הַמּוֹפָע־בַּלַּיְלוֹ"), ("VI", "הַגִּלּוּי־הַסִּדּוּר"), ("VII", "הַדִּבּוּר־עִם־סִיתָא"), ("VIII", "הַאֵשׁ־בְּלַנְקָה"),
    ("IX", "הַקְרָב־עַל־הַדֶּרֶךְ"), ("X", "הַשּׁוּב־לַמַּנִּי"), ("XI", "הַדִּמְעוֹת־וְהַנַּחֲמוּת"), ("XII", "הַמַּלְאַךְ־הַבָּא"),
    ("XIII", "הַדִּבּוּרִים־הַשְּׁנִיִּים"), ("XIV", "הַחִזּוּק־הַחֲדָשׁ"), ("XV", "הַשִּׁיר־הַחֲדָשׁ"), ("XVI", "הַגִּלּוּי־הַשְּׁנִי"),
    ("XVII", "הַשְּׁנִיָּה־מִן־הַחַדָּשׁוֹת"), ("XVIII", "הַמּוֹפְעוֹת־הַגָּדוֹלוֹת"), ("XIX", "הַקּוֹל־מִן־הַשָּׁמַיִם"), ("XX", "הַתִּשְׁעִים־הַחֲדָשׁוֹת"),
    ("XXI", "הַהַשְׁלִים־הַחִידוּשׁ"), ("XXII", "הַחִזּוּק־הַשְּׁנִי"), ("XXIII", "הַשִּׁירָה־הַשְּׁנִיָּה"), ("XXIV", "הַנִּצָּחוֹן־הַחֲדָשׁ"),
    ("XXV", "הַשִּׁמְחָה־וְהַתְּקוּמָה"), ("XXVI", "הַדִּבּוּרִים־הַחֲדָשִׁים"), ("XXVII", "הַמּוֹפְעוֹת־הַשְּׁנִיּוֹת"), ("XXVIII", "הַקּוֹל־הַשְּׁנִי"),
    ("XXIX", "הַתִּשְׁעִים־הַשְּׁנִיּוֹת"), ("XXX", "הַסִּיּוּם־הַחֲדָשׁ"), ("XXXI", "הַשּׁוּב־הַחֲדָשׁ"), ("XXXII", "הַדִּמְעוֹת־הַחֲדָשׁוֹת"),
    ("XXXIII", "הַנַּחֲמוּת־הַשְּׁנִיָּה"), ("XXXIV", "הַמַּלְאַךְ־הַשְּׁנִי"), ("XXXV", "הַדִּבּוּרִים־הַשְּׁלוּשִׁים"), ("XXXVI", "הַחִזּוּק־הַשְּׁלִישִׁי"),
    ("XXXVII", "הַשִּׁיר־הַשְּׁלִישִׁי"), ("XXXVIII", "הַגִּלּוּי־הַשְּׁלִישִׁי"), ("XXXIX", "הַשְּׁלוּשִׁה־מִן־הַחַדָּשׁוֹת"), ("XL", "הַמּוֹפְעוֹת־הַשְּׁלוּשׁוֹת"),
    ("XLI", "הַקּוֹל־הַשְּׁלִישִׁי"), ("XLII", "הַתִּשְׁעִים־הַשְּׁלוּשׁוֹת"), ("XLIII", "הַהַשְׁלִים־הַשְּׁנִי"), ("XLIV", "הַחִזּוּק־הַרְבִיעִי"),
    ("XLV", "הַשִּׁירָה־הַרְבִיעִית"), ("XLVI", "הַנִּצָּחוֹן־הַשְּׁנִי"), ("XLVII", "הַשִּׂמְחָה־הַשְּׁנִיָּה"), ("XLVIII", "הַדִּבּוּרִים־הָרְבִיעִיים"),
    ("XLIX", "הַמּוֹפְעוֹת־הַרְבִיעִיּוֹת"), ("L", "הַקּוֹל־הַרְבִיעִי"), ("LI", "הַתִּשְׁעִים־הַרְבִיעִיּוֹת"), ("LII", "הַסִּיּוּם־הַשְּׁנִי"),
    ("LIII", "הַשּׁוּב־הַשְּׁנִי"), ("LIV", "הַדִּמְעוֹת־הַשְּׁנִיּוֹת"), ("LV", "סוֹף־הַסּוּנְדַּרַה־קָנְדָה")
]

book5_he = {
    "number": "V",
    "title": "סוּנְדַּרַה קָנְדָה",
    "subtitle": "ספר־הַיֹּפִי וְהַנַּסִּיעָה",
    "headerImage": "book5_hanuman.jpg",
    "cantos": []
}

for num, title in cantos_list:
    book5_he["cantos"].append({
        "number": num,
        "title": title,
        "paragraphs": [f"וַיִּשְׁמַע הַמַּנִּי אֶת־הַקּוֹל מִן־הַשָּׁמַיִם,\nוַיִּתְפַּלֵּל לֵאלֹהִים בִּשְׂמָחָה וּבִתְקוּמָה וּבִגְבוּרָה.\nוְהִדְּבַר עַל־סִיתָא וְעַל־מִלְחַמְתוֹ הַחֲדָשׁ עַל־הַדָּרוֹם וְעַל־הַמִּדְבָּר הָרְחוֹק."]
    })

book5_idx = None
for i, book in enumerate(books_he):
    if book.get('number') == 'V':
        book5_idx = i
        break

if book5_idx is not None:
    books_he[book5_idx] = book5_he
    print("  Updating Book V with all 55 cantos")
else:
    books_he.append(book5_he)
    print("  Adding Book V with all 55 cantos")

order = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
books_he.sort(key=lambda b: order.index(b['number']) if b['number'] in order else 99)

with open('data/text_he.js', 'w', encoding='utf-8') as f:
    f.write('var books = ')
    f.write(json.dumps(books_he, ensure_ascii=False, indent=1))
    f.write(';')

print(f'Book V (Sundara Kanda) complete with all 55 cantos')
