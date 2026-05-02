# Claude Code Build Prompt

Paste this into Claude Code after opening the `ramayana-site/` folder.

---

## BEFORE RUNNING THIS PROMPT

Make sure you have already:
1. Deleted the two duplicate image files: `Valmiki_Ramayana__1_.jpg` and `DP152344__1_.jpg`
2. Renamed all images as specified in `IMAGES.md`
3. Placed all renamed images in `images/` (and `images/inline/book3_kabandha_inline.jpg`)

The images in `images/` should be exactly these 16 files:
- `cover_narrative_textile.jpg`
- `intro_valmiki_writing.jpg`
- `intro_manuscript_page.jpg`
- `intro_vishnu_shesha.jpg`
- `intro_vishnu_narayana.jpg`
- `intro_vishnu_hanuman.jpg`
- `book1_dasharatha_sage.jpg`
- `book3_kabandha.jpg`
- `book3_ravana_sculpture.jpg`
- `book4_rama_lakshmana_night.jpg`
- `book4_monkey_forest.jpg`
- `book5_hanuman_ravana_court.jpg`
- `book6_ravana_war_council.jpg`
- `book6_vibhishana_arrives.jpg`
- `book7_rama_enthroned.jpg`
- `book7_rama_court_ravi_varma.jpg`

---

## PROMPT

I have a folder with the following files:

- `source/rmahayana.txt` — the complete Valmiki Ramayana in English verse, Ralph T.H. Griffith translation (Project Gutenberg #24869). Structured as BOOK I through BOOK VI, each containing numbered Cantos in Roman numerals with titles.
- `source/valmiki_ramayana_deep_research.md` — a commentary guide covering every Book and Canto cluster, including "Key idea:" paragraphs at pivotal moments.
- `source/ramayana_index.html` — Sacred Text Archive index for structural reference.
- `images/` — 16 renamed public domain artworks from the Metropolitan Museum of Art. See the image list and descriptions in `IMAGES.md`.
- `images/inline/` — one inline illustration: `book3_kabandha_inline.jpg`.

Please build me a complete static website (pure HTML + CSS + vanilla JavaScript, no framework, no build step, deployable to GitHub Pages) with the features below.

---

### STRUCTURE AND NAVIGATION

- Landing page with a brief introduction to the Ramayana and a visual table of contents for all 7 Books.
- Persistent left sidebar (collapsible on mobile) listing all Books and Cantos as a navigation tree. Clicking a Canto jumps directly to it.
- Each Book section has a full-width illustrated header using the corresponding image from `images/` per this exact mapping:

| Book | Header image |
|------|-------------|
| Introduction / Landing | `cover_narrative_textile.jpg` (hero), `intro_valmiki_writing.jpg` (section header) |
| Book I — Bala Kanda | `book1_dasharatha_sage.jpg` |
| Book II — Ayodhya Kanda | `book1_dasharatha_sage.jpg` (reuse — no dedicated Book II image) |
| Book III — Aranya Kanda | `book3_kabandha.jpg` |
| Book IV — Kishkindha Kanda | `book4_rama_lakshmana_night.jpg` |
| Book V — Sundara Kanda | `book5_hanuman_ravana_court.jpg` |
| Book VI — Yuddha Kanda | `book6_ravana_war_council.jpg` |
| Book VII — Uttara Kanda | `book7_rama_enthroned.jpg` |

- The Introduction section should display three small side-by-side images: `intro_vishnu_shesha.jpg`, `intro_vishnu_narayana.jpg`, `intro_vishnu_hanuman.jpg` — these establish the cosmic context (Rama as Vishnu's avatar).
- The site's very last visual element (footer area above attribution) should be `book7_rama_court_ravi_varma.jpg` — the Ravi Varma Press coronation image — displayed as the closing image of the whole site.

---

### INLINE ILLUSTRATIONS

Place these images inline within the text at specific canto locations — not as headers, but as full-width inserts within the reading column:

| Image | Location |
|-------|----------|
| `intro_manuscript_page.jpg` | Top of the Introduction section, alongside the "What is the Ramayana?" text |
| `images/inline/book3_kabandha_inline.jpg` | Book III, between Cantos LXX–LXXIV (Kabandha section) |
| `book3_ravana_sculpture.jpg` | Book III, at Canto XXXI ("Rávan" — first appearance of Ravana in the narrative) |
| `book4_monkey_forest.jpg` | Book IV, at Cantos XXXVII–XLV (the dispatch of the search armies) |
| `book6_vibhishana_arrives.jpg` | Book VI, at Cantos XVII–XIX (Vibhishana's arrival and acceptance) |

All inline images: display with a max-width of 600px, centered, with a small caption below describing the scene. Use the descriptions from `IMAGES.md` for caption text.

---

### CORE FEATURE: ORIGINAL TEXT + COMMENTARY SIDE BY SIDE

- Each Canto: original Griffith verse on the LEFT, commentary from `valmiki_ramayana_deep_research.md` on the RIGHT.
- Desktop: two columns, independently scrollable. Toggle for synchronized scrolling.
- Mobile: stacked — text first, commentary below with a clear visual divider.
- "Key Idea" callout boxes wherever the research guide has a "Key idea:" paragraph — colored left border (#D4A017 gold), light background, slightly indented.
- Cantos without commentary: show "Commentary for this Canto is being prepared."

---

### CLICK-TO-HIGHLIGHT

- Every paragraph of the Griffith text is clickable.
- Click: highlights the paragraph (warm background), commentary panel scrolls to top of that Canto's commentary.
- Hover tooltip: "Click to see commentary."
- Second click removes highlight.

---

### SEARCH

- Search bar fixed at the top.
- Searches both text and commentary simultaneously.
- Highlights matching words in results.
- Returns a list of Canto links with context snippets.
- `Ctrl+F` / `Cmd+F` opens the site's own search when in reading view.

---

### READING MODE TOGGLES

- "Text only" / "Commentary only" / "Both" — saved to localStorage.
- Night mode / Day mode — saved to localStorage.

---

### DESIGN

**Typography (Google Fonts):**
- `"Cormorant Garamond"` (serif, 400 and 600) — Griffith verse text
- `"Inter"` (sans-serif, 400 and 500) — commentary, navigation, UI, captions

**Color palette:**
- Text panel: `#FDF6E3` (warm parchment)
- Commentary panel: `#FFFFFF`
- Accent / headings: `#C0542A` (deep saffron/rust)
- Key Idea callout border: `#D4A017` (warm gold)
- Navigation background: `#1A2340` (dark navy)
- Navigation text: `#EDE8D0` (light cream)
- Night mode bg: `#1C1C1E`, text: `#E8E0CC`

**Layout rules:**
- No emojis anywhere.
- Clean horizontal rules between Cantos — a simple styled `<hr>` or a decorative SVG divider.
- Thin progress bar at top of reading view showing scroll progress through current Book.
- Book header images: full-width banners, dark gradient overlay, Book title in large Cormorant Garamond over the image.
- All images lazy-loaded.
- If an image file is missing, show a solid color gradient banner — never a broken image icon.

---

### DATA ARCHITECTURE

**`data/text.js`** — parse `source/rmahayana.txt` into:

```javascript
const RAMAYANA_TEXT = [
  {
    book: "I",
    title: "Bala Kanda",
    subtitle: "The Book of Childhood",
    headerImage: "book1_dasharatha_sage.jpg",
    cantos: [
      {
        number: "I",
        title: "Nárad",
        paragraphs: ["To sainted Nárad, prince of those...", ...]
      },
      // all cantos
    ]
  },
  // Books II–VI plus Book VII summary
];
```

**`data/commentary.js`** — parse `source/valmiki_ramayana_deep_research.md` into:

```javascript
const RAMAYANA_COMMENTARY = [
  {
    book: "I",
    intro: "The Bala Kanda establishes...",
    cantoCommentaries: [
      {
        cantoNumbers: ["I"],
        cantoTitle: "Nárad",
        text: "This is the opening of the entire epic...",
        keyIdea: "Narada describes Rama with 16 specific noble qualities...",
        inlineImage: null
      },
      // ...
    ]
  }
];
```

Add the inline image filenames to the commentary entries for the five inline placements listed above.

Map commentary to text by matching Book number and Canto title keywords — use substring/fuzzy matching where exact title match fails.

---

### TECHNICAL

- Pure HTML + CSS + vanilla JavaScript. No npm, no webpack, no build pipeline.
- All content embedded in data JS files — no runtime fetching, works offline after first load.
- Single `index.html` entry point with anchor-based navigation.
- Keyboard-accessible sidebar (Tab, Enter, Arrow keys).
- `<meta>` tags for SEO and Open Graph.
- Include `404.html` (copy of `index.html`) for GitHub Pages.
- Include `_config.yml` with `theme: null` to disable Jekyll.

---

### FOOTER

Every page footer must include:

> Original text: *The Rámáyan of Válmíki*, translated by Ralph T.H. Griffith (1870–1874). Public domain via [Project Gutenberg #24869](https://www.gutenberg.org/ebooks/24869).
> Commentary: original scholarship. Illustrations: [The Metropolitan Museum of Art Open Access Collection](https://www.metmuseum.org/about-the-met/policies-and-documents/open-access). Public domain (CC0).

---

### HOW TO PROCEED

1. Read and fully parse `source/rmahayana.txt` — understand how Books and Cantos are delimited and how stanza breaks work.
2. Read `source/valmiki_ramayana_deep_research.md` — understand the commentary structure.
3. Generate `data/text.js` and confirm structure before proceeding.
4. Generate `data/commentary.js`.
5. Build `style.css`.
6. Build `index.html` and `site.js`.
7. Test that the site opens with no console errors.
8. Generate `404.html` and `_config.yml`.

Work methodically. Do not skip Step 1.

---

## FOLLOW-UP PROMPTS

**If Canto parsing is wrong:**
> "The Canto breaks in text.js are incorrect. In the source file, each Canto starts with the pattern 'Canto [Roman numeral]. [Title].' Please re-parse Books I and II only first, confirm the structure, then extend."

**If commentary mapping is patchy:**
> "Some Cantos show the placeholder instead of commentary. The commentary covers groups of Cantos together (e.g. Cantos I–IV together). Map each group entry to all Canto numbers it covers. Use substring matching on Canto titles."

**If images aren't showing:**
> "Images aren't displaying. The image files are in the images/ folder at the project root. Paths should be relative from index.html, e.g. images/book1_dasharatha_sage.jpg. Please check path resolution."

**If two-column layout breaks:**
> "The two-column layout collapses too early. Set the responsive breakpoint at 768px, not 1024px. Between 768–1024px use single-column with commentary collapsed behind a toggle."

**If the .jfif image doesn't display:**
> "The file book5_hanuman_ravana_court.jpg was originally a .jfif file. If it's not displaying, either convert it to JPEG using: `ffmpeg -i book5_hanuman_ravana_court.jpg output.jpg` or handle .jfif MIME type explicitly in the image tag."
