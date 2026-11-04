#!/usr/bin/env python3
"""Embed the edited face.svg into the fx-991EX entry in index.html."""
from pathlib import Path
import base64
import re

root = Path(__file__).resolve().parent.parent
page = root / 'index.html'
face = root / 'face.svg'
text = page.read_text(encoding='utf-8')
pattern = r"('CY234':\s*\{.*?faceSvg: ')([^']+)(')"
match = re.search(pattern, text, flags=re.S)
if not match:
    raise SystemExit('Could not find the fx-991EX face in index.html; no changes made.')
encoded = base64.b64encode(face.read_bytes()).decode('ascii')
page.write_text(text[:match.start(2)] + encoded + text[match.end(2):], encoding='utf-8')
print('Updated the embedded fx-991EX face in index.html.')
