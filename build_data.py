#!/usr/bin/env python3
"""
Ramayana site data builder.
Run once:  python build_data.py
Outputs:   data/text.js, data/commentary.js
"""

import re, json, sys
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)

# ─── book metadata ─────────────────────────────────────────────────────────────

BOOK_META = {
    "I":   ("Bala Kanda",       "The Book of Childhood",     "book1_dasharatha_sage.jpg"),
    "II":  ("Ayodhya Kanda",    "The Book of Ayodhya",       "book1_dasharatha_sage.jpg"),
    "III": ("Aranya Kanda",     "The Book of the Forest",    "book3_kabandha.jpg"),
    "IV":  ("Kishkindha Kanda", "The Book of Kishkindha",    "book4_rama_lakshmana_night.jpg"),
    "V":   ("Sundara Kanda",    "The Beautiful Book",         "book5_hanuman_ravana_court.jpg"),
    "VI":  ("Yuddha Kanda",     "The Book of War",            "book6_ravana_war_council.jpg"),
    "VII": ("Uttara Kanda",     "The Book of the Aftermath",  "book7_rama_enthroned.jpg"),
}

# Inline images: (book_number, canto_roman) -> image info
INLINE_IMAGES = {
    ("III", "XXXI"):   {
        "src": "images/book3_ravana_sculpture.jpg",
        "caption": "Ravana in deep meditation: ten-headed, twenty-armed, each hand in a different gesture. Bronze sculpture, Southeast Asian, 10th–12th century. The serenity of the face captures the paradox — Ravana possessed genuine spiritual mastery."
    },
    ("III", "LXX"):    {
        "src": "images/inline/book3_kabandha_inline.jpg",
        "caption": "Rama and Lakshmana battle Kabandha, the headless demon with arms of enormous reach. Indian miniature, Pahari or Rajasthani, 17th–18th century."
    },
    ("IV",  "XXXVII"): {
        "src": "images/book4_monkey_forest.jpg",
        "caption": "The monkey armies gathering in the forest: multiple simultaneous scenes of the search parties assembling and departing in all directions. Mughal or Deccani miniature, 17th–18th century."
    },
    ("VI",  "XVII"):   {
        "src": "images/book6_vibhishana_arrives.jpg",
        "caption": "Vibhishana arrives before Rama, who receives him from his pavilion as the assembled forces look on. Mughal miniature, late 16th–early 17th century."
    },
}

# ─── text parser ───────────────────────────────────────────────────────────────

FOOTNOTE_RE = re.compile(r'\([0-9]+\)')
BOOK_RE     = re.compile(r'^BOOK\s+([IVXLCDM]+)\.')
CANTO_RE    = re.compile(r'^Canto\s+([IVXLCDM]+)\.\s+(.+)$')
INVOC_RE    = re.compile(r'^INVOCATION')

STOP_TOKENS = ('APPENDIX', 'ADDITIONAL NOTES', 'INDEX OF PRINCIPAL', '*** END OF')


def strip_fn(s):
    return FOOTNOTE_RE.sub('', s)


def clean_title(raw):
    t = re.sub(r'\.\([0-9]+\)$', '', raw)
    return strip_fn(t).rstrip('.').strip()


class TextParser:
    def __init__(self):
        self.books       = []
        self.cur_book    = None
        self.cur_canto   = None
        self.stanza      = []
        self.paras       = []
        self.inv_stanza  = []
        self.inv_paras   = []
        self.in_invoc    = False

    def _flush_stanza(self):
        if self.stanza:
            para = '\n'.join(strip_fn(l) for l in self.stanza).strip()
            if para:
                self.paras.append(para)
            self.stanza = []

    def _flush_inv_stanza(self):
        if self.inv_stanza:
            para = '\n'.join(strip_fn(l) for l in self.inv_stanza).strip()
            if para:
                self.inv_paras.append(para)
            self.inv_stanza = []

    def _flush_canto(self):
        if self.cur_canto is not None:
            self._flush_stanza()
            self.cur_canto['paragraphs'] = list(self.paras)
            self.cur_book['cantos'].append(self.cur_canto)
            self.cur_canto = None
            self.paras = []

    def _flush_book(self):
        if self.cur_book is not None:
            self._flush_canto()
            self.books.append(self.cur_book)
            self.cur_book = None

    def parse(self, filepath):
        lines = Path(filepath).read_text(encoding='utf-8', errors='replace').splitlines()

        # locate body start
        start = 0
        for i, l in enumerate(lines):
            if INVOC_RE.match(l.strip()):
                start = i
                break

        # locate body end
        end = len(lines)
        for i in range(start + 200, len(lines)):
            s = lines[i].strip()
            if any(s.startswith(t) or t in s for t in STOP_TOKENS):
                end = i
                break

        self.in_invoc = True

        for line in lines[start:end]:
            s = line.strip()

            if INVOC_RE.match(s):
                continue   # skip the header token itself

            bm = BOOK_RE.match(s)
            if bm:
                num = bm.group(1)
                if num not in BOOK_META:
                    continue
                self.in_invoc = False
                self._flush_inv_stanza()
                self._flush_book()
                title, subtitle, img = BOOK_META[num]
                self.cur_book = {
                    'number': num, 'title': title,
                    'subtitle': subtitle, 'headerImage': img,
                    'cantos': []
                }
                continue

            cm = CANTO_RE.match(s)
            if cm and self.cur_book is not None and not self.in_invoc:
                self._flush_canto()
                cnum   = cm.group(1)
                ctitle = clean_title(cm.group(2))
                entry  = {'number': cnum, 'title': ctitle, 'paragraphs': []}
                img_key = (self.cur_book['number'], cnum)
                if img_key in INLINE_IMAGES:
                    entry['inlineImage'] = INLINE_IMAGES[img_key]
                self.cur_canto = entry
                continue

            if self.in_invoc:
                if s == '':
                    self._flush_inv_stanza()
                else:
                    self.inv_stanza.append(s)
            elif self.cur_canto is not None:
                if s == '':
                    self._flush_stanza()
                else:
                    self.stanza.append(s)

        # final flush
        self._flush_inv_stanza()
        self._flush_book()

        # prepend Invocation canto to Book I
        if self.books and self.inv_paras:
            self.books[0]['cantos'].insert(0, {
                'number': 'Invocation',
                'title':  'Invocation',
                'paragraphs': self.inv_paras
            })

        # Book VII (not in Griffith)
        t, s, img = BOOK_META['VII']
        self.books.append({'number': 'VII', 'title': t, 'subtitle': s,
                           'headerImage': img, 'cantos': []})
        return self.books


def write_text_js(books):
    out  = DATA / "text.js"
    body = json.dumps(books, ensure_ascii=False, separators=(',', ':'))
    out.write_text(f"// auto-generated — do not edit\nconst RAMAYANA_TEXT={body};\n",
                   encoding='utf-8')
    nc = sum(len(b['cantos']) for b in books)
    print(f"  text.js   {out.stat().st_size//1024} KB  |  {len(books)} books  |  {nc} cantos")


# ─── commentary parser ─────────────────────────────────────────────────────────

def roman_to_int(r):
    v = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    res = prev = 0
    for c in reversed(r.upper().strip()):
        x = v.get(c, 0)
        res += x if x >= prev else -x
        prev = x
    return res

def int_to_roman(n):
    pairs = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),
             (50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
    r = ''
    for val, sym in pairs:
        while n >= val:
            r += sym; n -= val
    return r

def expand_range(s):
    """'I–IV' or 'I-IV' -> ['I','II','III','IV']"""
    s = s.strip().replace('–','-').replace('—','-')
    if '-' in s:
        a, b = s.split('-', 1)
        ai, bi = roman_to_int(a.strip()), roman_to_int(b.strip())
        if ai and bi and bi >= ai:
            return [int_to_roman(i) for i in range(ai, bi+1)]
    ri = roman_to_int(s)
    return [int_to_roman(ri)] if ri else []

def clean_md(text):
    if not text:
        return ''
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*\n]+)\*',     r'\1', text)
    text = re.sub(r'^>\s*', '',  text, flags=re.MULTILINE)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# Matches bolded canto headings inside the commentary text
CANTO_ENTRY_RE = re.compile(
    r'\*\*Cantos?\s+([IVXLCDM]+(?:[–—-][IVXLCDM]+)?)\s*'
    r'[—–‒‐-]\s*([^*\n]+)\*\*\n?'
    r'(.*?)(?=\n\*\*(?:Canto|Key idea)|\Z)',
    re.DOTALL
)
KEY_IDEA_RE = re.compile(
    r'\*\*Key idea:\*\*\s*(.+?)(?=\n\n\*\*|\n#{2,}|\Z)',
    re.DOTALL
)

def parse_book_section(section_text):
    """Parse one # BOOK X: ... section from the markdown."""
    lines = section_text.split('\n')
    result = {'intro': '', 'cantoMap': {}}

    intro_lines, sections, cur_sec = [], [], None
    in_intro = True
    for line in lines[1:]:          # skip book heading
        if line.startswith('### '):
            in_intro = False
            if cur_sec is not None:
                sections.append(cur_sec)
            cur_sec = {'heading': line, 'body': ''}
        elif line.startswith('## '):
            pass                    # subtitle — skip
        elif in_intro:
            intro_lines.append(line)
        elif cur_sec is not None:
            cur_sec['body'] += line + '\n'

    if cur_sec:
        sections.append(cur_sec)

    result['intro'] = clean_md('\n'.join(intro_lines))

    for sec in sections:
        heading = sec['heading']
        body    = sec['body']

        # Canto range from section heading
        hm = re.search(r'Cantos?\s+([IVXLCDM]+(?:[–-][IVXLCDM]+)?)', heading, re.I)
        sec_cantos = expand_range(hm.group(1)) if hm else []

        # Individual canto entries within section
        entry_map = {}
        for m in CANTO_ENTRY_RE.finditer(body):
            raw_range  = m.group(1)
            entry_body = m.group(3).strip()

            ki_m = KEY_IDEA_RE.search(entry_body)
            key_idea = clean_md(ki_m.group(1)) if ki_m else None
            text_part = entry_body[:ki_m.start()].strip() if ki_m else entry_body

            cantos = expand_range(raw_range)
            if not cantos:
                cantos = [raw_range.strip()]

            for c in cantos:
                if c:
                    entry_map[c] = {
                        'text': clean_md(text_part),
                        'keyIdea': key_idea,
                        'inlineImage': None
                    }

        # If no per-canto entries found, use the whole section body for all range cantos
        if not entry_map and sec_cantos:
            ki_m = KEY_IDEA_RE.search(body)
            key_idea  = clean_md(ki_m.group(1)) if ki_m else None
            text_part = body[:ki_m.start()].strip() if ki_m else body

            for c in sec_cantos:
                entry_map[c] = {
                    'text': clean_md(text_part),
                    'keyIdea': key_idea,
                    'inlineImage': None
                }

        result['cantoMap'].update(entry_map)

    return result


def parse_commentary_file():
    md = (BASE / "valmiki_ramayana_deep_research.md").read_text(encoding='utf-8')

    # Split at each top-level # BOOK heading
    parts   = re.split(r'\n(?=# BOOK [IVX]+)', md)
    intro   = parts[0]
    result  = {
        'intro': {'text': clean_md(intro), 'keyIdea': None},
        'books': {}
    }

    for part in parts[1:]:
        bm = re.match(r'# BOOK ([IVX]+)', part)
        if not bm:
            continue
        book_num = bm.group(1)
        result['books'][book_num] = parse_book_section(part)

    # Book VII summary (not in source text, only in commentary)
    if 'VII' not in result['books']:
        result['books']['VII'] = {'intro': '', 'cantoMap': {}}
    # grab intro from the # BOOK VII section if present
    vii_m = re.search(r'# BOOK VII.*?\n(.*?)(?=\n# |\Z)', md, re.DOTALL)
    if vii_m:
        result['books']['VII']['intro'] = clean_md(vii_m.group(1)[:3000])

    return result


def write_commentary_js(data):
    out  = DATA / "commentary.js"
    body = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    out.write_text(f"// auto-generated — do not edit\nconst RAMAYANA_COMMENTARY={body};\n",
                   encoding='utf-8')
    print(f"  commentary.js   {out.stat().st_size//1024} KB")


# ─── main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("Building text.js …")
    parser = TextParser()
    books  = parser.parse(BASE / "rmahayana.txt")
    write_text_js(books)

    print("Building commentary.js …")
    commentary = parse_commentary_file()
    write_commentary_js(commentary)

    print("Done.")
