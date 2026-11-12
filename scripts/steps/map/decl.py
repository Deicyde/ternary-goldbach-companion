#!/usr/bin/env python3
"""Resolve Lean declarations of ternary-goldbach at the pin.
  decl.py NAME            full name(s) ending in NAME, with file and full line range
  decl.py FILE:LINE       the declaration(s) whose range contains that line
Mathlib names resolve too (paths under .lake/packages/mathlib/). Paths are relative to ~/tg-companion/tg. Private names print as written in source."""
import json,sys,os
ROOT=__import__('os').environ.get('TG_COMPANION',__import__('os').path.expanduser('~/tg-companion'))
H=os.path.dirname(os.path.abspath(__file__))
idx=json.load(open(os.path.join(H,'declindex.json')))
_ml=None
def ml():
    global _ml
    if _ml is None: _ml=json.load(open(os.path.join(H,'mathlib-index.json')))
    return _ml
def show(n,v):
    nm=n
    if n.startswith('_private.'):
        nm=n.split('.0.',1)[1]+'   (private)'
    print(f"{nm}\t{v['file']}\t{v['lines'][0]}-{v['lines'][1]}")
for a in sys.argv[1:]:
    if ':' in a and a.split(':')[-1].isdigit():
        f,l=a.rsplit(':',1); l=int(l); f=f.replace(os.path.join(ROOT,'tg/'),'')
        src=idx if not f.startswith('.lake') else ml()
        hits=[(n,v) for n,v in src.items() if v['file']==f and v['lines'][0]<=l<=v['lines'][1] and not any(s in n for s in ('.match_','._proof_','._aux','.proof_'))]
        hits.sort(key=lambda t:t[1]['lines'][1]-t[1]['lines'][0])
        for n,v in hits[:3]: show(n,v)
        if not hits: print('no declaration contains',a)
    else:
        hits=[(n,v) for n,v in idx.items() if n==a or n.endswith('.'+a)]
        if not hits: hits=[(n,v) for n,v in ml().items() if n==a or n.endswith('.'+a)]
        for n,v in hits[:10]: show(n,v)
        if not hits: print('not found:',a)
