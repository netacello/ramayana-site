# The Valmiki Ramayana — Annotated Web Edition

A static website presenting the complete Valmiki Ramayana in the Griffith English verse translation (1870–1874), with full scholarly commentary displayed side by side. Illustrated with public domain artworks from the Metropolitan Museum of Art. Deployable to GitHub Pages with no build step.

---

## What This Site Does

- Displays the original Griffith verse text alongside structured commentary for every Book and Canto
- Side-by-side layout on desktop, stacked on mobile
- Click any paragraph of the original text to highlight it and jump to the relevant commentary
- Full-text search across both original text and commentary
- Reading mode toggles: Text only / Commentary only / Both
- Night mode / Day mode
- Illustrated Book headers and inline illustrations using real Met Museum artworks
- Progress indicator per Book
- Works fully offline after first load — no server, no dependencies, no build step

---

## File Structure

```
ramayana-site/
│
├── index.html                          ← Main entry point / landing page
├── site.js                             ← All JS logic (parsing, navigation, search, UI)
├── style.css                           ← All styles
│
├── data/
│   ├── text.js                         ← Parsed Griffith text as JS data structure
│   └── commentary.js                   ← Commentary mapped to cantos
│
├── images/
│   │
│   ├── cover_narrative_textile.jpg     ← Landing page hero (embroidered textile, all episodes)
│   ├── intro_valmiki_writing.jpg       ← Valmiki composing the Ramayana (Introduction + Book I)
│   ├── intro_manuscript_page.jpg       ← Illuminated Sanskrit manuscript page (Introduction)
│   ├── intro_vishnu_shesha.jpg         ← Vishnu reclining on Shesha serpent (Introduction)
│   ├── intro_vishnu_narayana.jpg       ← Shesha Narayana, Ravi Varma Press (Introduction)
│   ├── intro_vishnu_hanuman.jpg        ← Vishnu with Hanuman attending (Introduction)
│   ├── book1_dasharatha_sage.jpg       ← Dasharatha receiving a sage (Book I header)
│   ├── book3_kabandha.jpg              ← Rama and Lakshmana fighting Kabandha (Book III header)
│   ├── book3_ravana_sculpture.jpg      ← Ten-headed Ravana bronze sculpture (Book III inline)
│   ├── book4_rama_lakshmana_night.jpg  ← Rama and Lakshmana on rock under full moon (Book IV header)
│   ├── book4_monkey_forest.jpg         ← Monkeys on forested hillside (Book IV inline)
│   ├── book5_hanuman_ravana_court.jpg  ← Hanuman before Ravana's court (Book V header)
│   ├── book6_ravana_war_council.jpg    ← Ravana's war council with demon army (Book VI header)
│   ├── book6_vibhishana_arrives.jpg    ← Rama in pavilion receiving Vibhishana (Book VI inline)
│   ├── book7_rama_enthroned.jpg        ← Rama enthroned, folk style (Book VII header)
│   ├── book7_rama_court_ravi_varma.jpg ← Ravi Varma: Uttara Ramacharit coronation (site close)
│   │
│   └── inline/
│       └── book3_kabandha_inline.jpg   ← Copy of book3_kabandha.jpg for inline use
│
├── source/
│   ├── rmahayana.txt                   ← Original Griffith text (Project Gutenberg #24869)
│   ├── ramayana_index.html             ← Sacred Text Archive index (reference only)
│   └── valmiki_ramayana_deep_research.md  ← Full commentary guide
│
├── IMAGES.md                           ← Full image catalogue with identifications
├── PROMPT.md                           ← The Claude Code prompt used to build this site
└── README.md                           ← This file
```

---

## Before You Build: Rename the Images

The source images from the Met Museum need to be renamed before building. See `IMAGES.md` for the complete rename table. Quick summary:

1. Delete `Valmiki_Ramayana__1_.jpg` and `DP152344__1_.jpg` (duplicates)
2. Rename all remaining files as listed in `IMAGES.md`
3. Place renamed files in `images/` and `images/inline/` as indicated

---

## How to Run Locally

No build step required:

```bash
# Option 1: open directly
open index.html

# Option 2: serve locally (recommended — avoids file:// quirks)
python3 -m http.server 8080
# then visit http://localhost:8080
```

---

## How to Deploy to GitHub Pages

```bash
cd ramayana-site
git init
git add .
git commit -m "Initial build"
git remote add origin https://github.com/YOUR_USERNAME/ramayana-annotated.git
git push -u origin main
```

Then in your repo Settings → Pages → set source to `main` branch, root `/`.
Your site will be live at `https://YOUR_USERNAME.github.io/ramayana-annotated/`

---

## Attribution

**Original text:** *The Rámáyan of Válmíki*, translated by Ralph T.H. Griffith (1870–1874). Public domain. [Project Gutenberg #24869](https://www.gutenberg.org/ebooks/24869)

**Commentary:** Original scholarship compiled from the Griffith text and classical commentaries.

**Illustrations:** The Metropolitan Museum of Art Open Access Collection. Public domain (CC0). https://www.metmuseum.org/about-the-met/policies-and-documents/open-access

---

## License

Text and commentary: [MIT License](https://opensource.org/licenses/MIT). Images: public domain (CC0) via the Metropolitan Museum of Art.
