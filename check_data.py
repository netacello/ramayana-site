import json, re

with open("data/text.js", encoding="utf-8") as f:
    raw = f.read()

# Strip JS wrapper to get pure JSON
json_str = re.sub(r'^.*?RAMAYANA_TEXT=', '', raw, flags=re.DOTALL).rstrip(';\n \r')
data = json.loads(json_str)

for b in data:
    nc = len(b["cantos"])
    print(f"Book {b['number']} ({b['title']}): {nc} cantos", end="")
    if nc > 0:
        f_c = b["cantos"][0]
        l_c = b["cantos"][-1]
        print(f"  [{f_c['number']}..{l_c['number']}]", end="")
        # check paragraphs
        total_p = sum(len(c['paragraphs']) for c in b['cantos'])
        print(f"  {total_p} paras", end="")
    print()

# Check Book VI specifically
for b in data:
    if b['number'] == 'VI':
        print(f"\nBook VI canto list:")
        for c in b['cantos'][:5]:
            print(f"  {c['number']}: {c['title']} ({len(c['paragraphs'])} paras)")
        print("  ...")
        for c in b['cantos'][-5:]:
            print(f"  {c['number']}: {c['title']}")
