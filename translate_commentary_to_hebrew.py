#!/usr/bin/env python3
import json
import re
import sys
from google_trans_new import google_translator

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

translator = google_translator()

def load_json_from_file(filepath):
    """Load JSON from a .js file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'const RAMAYANA_COMMENTARY\s*=\s*(\{.*\});?\s*$', content, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    return {}

def translate_text(text, retries=3):
    """Translate text to Hebrew"""
    if not text or not text.strip():
        return text
    for attempt in range(retries):
        try:
            result = translator.translate(text, lang_src='en', lang_tgt='he')
            return result if result else text
        except:
            if attempt == retries - 1:
                return text
    return text

def translate_commentary(data):
    """Recursively translate all commentary text"""
    if isinstance(data, dict):
        translated = {}
        for key, value in data.items():
            if isinstance(value, str):
                if key in ['text', 'intro', 'keyIdea']:
                    print(f"  Translating {key}...")
                    translated[key] = translate_text(value)
                else:
                    translated[key] = value
            else:
                translated[key] = translate_commentary(value)
        return translated
    elif isinstance(data, list):
        return [translate_commentary(item) for item in data]
    else:
        return data

def main():
    en_file = r'C:\Users\Main\OneDrive\Documents\Neta\ramayana-site\data\commentary.js'
    he_file = r'C:\Users\Main\OneDrive\Documents\Neta\ramayana-site\data\commentary_he.js'

    print("Loading English commentary...")
    data = load_json_from_file(en_file)
    print(f"Translating all commentary to Hebrew (this takes 10-15 minutes)...\n")
    
    hebrew_data = translate_commentary(data)

    print("\nSaving Hebrew commentary...")
    with open(he_file, 'w', encoding='utf-8') as f:
        f.write('const RAMAYANA_COMMENTARY_HE=')
        f.write(json.dumps(hebrew_data, ensure_ascii=False, indent=2))
        f.write(';')

    print("DONE! All commentary translated to Hebrew.")
    print("Refresh your browser to see the updates!")

if __name__ == '__main__':
    main()
