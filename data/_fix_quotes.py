"""
Fix _translate_batch.py:
- The prior replacement turned every `",\r\n` into `"",\r\n`
- We want to revert ONLY the cases NOT preceded by backslash
  (backslash-preceded = speech-mark endings, those should stay as \",\r\n -> \"",\r\n)
- Non-backslash cases (like "I"") should be reverted: "" -> "
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/_translate_batch.py', 'rb') as f:
    raw = bytearray(f.read())

fixed = 0
i = 0
result = bytearray()
while i < len(raw):
    # Check for 0x22 0x22 (double-double-quote)
    if (raw[i] == 0x22 and i + 1 < len(raw) and raw[i+1] == 0x22):
        # Is this preceded by backslash (0x5c)?
        preceded_by_backslash = (len(result) > 0 and result[-1] == 0x5c)
        if preceded_by_backslash:
            # Keep as-is: \""  (this was the correct speech-mark fix)
            result.append(raw[i])
        else:
            # Remove the extra " — revert the wrong change
            result.append(raw[i])  # keep first "
            i += 1  # skip the second "
            fixed += 1
    else:
        result.append(raw[i])
    i += 1

with open('data/_translate_batch.py', 'wb') as f:
    f.write(bytes(result))

print(f'Reverted {fixed} wrong double-quotes')
print('Done.')
