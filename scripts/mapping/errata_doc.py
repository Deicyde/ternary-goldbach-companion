"""Write docs/errata.md: the claims that [H] errs which a re-run check in scripts/checks/, or a compiled
Lean refutation in lean/ (scripts/mapping/formal_errata.py), confirms.

New code.  Reads data/items.json and data/regions-book.json; lists only errata whose check state is `confirmed`.

Usage: python3 -I errata_doc.py <repository root>
"""
import json
import os
import sys

root = sys.argv[1]
items = json.load(open(os.path.join(root, 'data', 'items.json')))['items']
regions = json.load(open(os.path.join(root, 'data', 'regions-book.json')))['items']
rows = [x for x in items if x['erratum'].get('check', {}).get('state') == 'confirmed']
kind = lambda x: x['erratum']['check'].get('kind') or x['erratum']['kind']
lines = ['# Confirmed errata of arXiv:1501.05438v2', '',
         'Each claim below was confirmed by the numerical check named beside it, re-run on the recorded',
         'date (`data/checks-run.json`), or by the Lean theorem named beside it, which proves the printed',
         'statement false and was built at the pin (`lean/`). The checks and the Lean files were written and',
         'judged by AI agents; no person has reviewed them. Claims not confirmed this way are not listed.',
         'Printed page numbers.', '',
         '| Item | p. | Kind | What | Check |', '|---|---|---|---|---|']
for x in rows:
    note = ' '.join(x['erratum']['check']['note'].split()).replace('|', '\\|')
    pages = sorted({r['page'] - 10 for r in regions.get(x['id'], [])}) or ['']
    c = x['erratum']['check']
    how = f"`{c['script']}`, `{c['theorem'].split('.')[-1]}`" if c.get('theorem') else f"`{c['script']}`"
    lines.append(f"| {x['id']} | {pages[0]} | {kind(x)} | {note} | {how} |")
lines.append('')
os.makedirs(os.path.join(root, 'docs'), exist_ok=True)
open(os.path.join(root, 'docs', 'errata.md'), 'w', encoding='utf-8').write('\n'.join(lines))
print(len(rows), 'confirmed errata,', sum(kind(x) == 'typo' for x in rows), 'of them typos')
