# Translation Workflow - Books II-VII

## Overview
The file `batches_for_translation.txt` contains all 418 cantos from Books II-VII organized by book and canto, ready for manual translation.

## How to Translate One Batch at a Time

### Step 1: Pick a Batch
Open `batches_for_translation.txt` and find a canto. Each looks like:

```
--- CANTO I: [Title] ---

[1] First paragraph text here...

[2] Second paragraph text here...

[3] More text...
```

### Step 2: Prepare Your Prompt
Give your translation tool THIS prompt:

```
Translate the following English Ramayana verses to Hebrew. Keep the structure with [1], [2], etc. numbers.

BOOK: [Book Number and Title]
CANTO: [Canto Number and Title]

[1] [English text here]

[2] [English text here]

OUTPUT ONLY the translated Hebrew text in the same format with numbers.
```

### Step 3: Get Translation
Run your translation script with the above prompt + batch text.

### Step 4: Save Translations
Create a file called `translations_batch_[BOOK_NUM]_[CANTO_NUM].txt` with the Hebrew output.

Example: `translations_batch_II_I.txt` for Book II, Canto I

Format should be:
```
[1] [Hebrew text]

[2] [Hebrew text]

[3] [Hebrew text]
```

### Step 5: Merge When Done
Once you have several batches translated, run:

```bash
python3 merge_translations.py
```

This will automatically merge all `translations_batch_*.txt` files back into `data/text_he.js`.

---

## File Locations
- **Input**: `batches_for_translation.txt` (all verses to translate)
- **Your translations**: `translations_batch_[BOOK]_[CANTO].txt` (create these as you translate)
- **Output**: `data/text_he.js` (will be updated by merge script)

## Example Workflow

1. Open `batches_for_translation.txt`
2. Find: `--- CANTO I: The Minister's Advice ---`
3. Copy those 4 paragraphs
4. Create prompt with BOOK: II, CANTO: I
5. Translate with your tool
6. Save output as `translations_batch_II_I.txt`
7. Repeat for more cantos
8. When ready, run `python3 merge_translations.py`

---

**Tip**: Translate cantos in any order - the merge script will put them in the right place!
