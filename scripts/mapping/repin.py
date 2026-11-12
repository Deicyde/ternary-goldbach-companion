"""Re-pin the mapping from calr3/ternary-goldbach ce82a5b to P.

Each declaration the mapping names is resolved in two declaration indexes dumped from the elaborated
environments (`scripts/mapping/DeclIndex.lean`, run at ce82a5b and at P).  A project declaration is

* `unchanged`: same name, same elaborated type (`Expr.hash`), same value for a definition, same module, and no
  definition its type reaches through definition values changed;
* `moved`: same type (and value) under a new name or module;
* `changed`: its type differs, or (for a definition) its value, or a definition its type reaches changed;
* `gone`: no declaration of that name at P and none with the same type among the new names.

Mathlib declarations are `unchanged` when they resolve at P: both pins use the same Mathlib commit.
An item takes the worst class of its declarations (gone > changed > moved > unchanged).  An item with no
declaration is `unchanged`.  An item is flagged `cited_at_p` when a docstring at P that is new or differs from
ce82a5b cites its number on a declaration the mapping does not name, so that it is judged again.

A definition whose value hash differs but whose source text is identical at both commits (its value refers to
renumbered auxiliary `_proof_` constants) counts as unchanged.

Usage: python3 -I repin.py <items_merged.json> <index_old.json> <index_P.json> <mathlib_P.json> <tg checkout> <P>
       <out repin.json>
"""
import collections
import json
import re
import subprocess
import sys

ORDER = ['unchanged', 'moved', 'changed', 'gone']
OLD = 'ce82a5b2a4ed5039c4750c0d062f0b0f2b833be0'
DROPPED = {'TernaryGoldbach.RHUpTo', 'TernaryGoldbach.ButhePsi'}  # hypotheses removed after ce82a5b
FACT = re.compile(r'\[Fact TernaryGoldbach\.\w+\]\s*')


def strip_facts(t):
    t = FACT.sub('', t)
    t = re.sub(r'∀\s*,\s*', '', t)
    return ' '.join(t.split())


def main():
    items_path, old_path, p_path, ml_path, tg, pin, out_path = sys.argv[1:8]
    items = json.load(open(items_path))
    O = {d['name']: d for d in json.load(open(old_path))}
    P = {d['name']: d for d in json.load(open(p_path))}
    ML = {d['name']: d for d in json.load(open(ml_path))}

    def same(a, b):
        return a['type_hash'] == b['type_hash'] and a['kind'] == b['kind'] and a.get('value_hash') == b.get('value_hash')

    def source(rev, d):
        f = d['module'].replace('.', '/') + '.lean'
        text = subprocess.run(['git', '-C', tg, 'show', f'{rev}:{f}'], capture_output=True, text=True).stdout
        return '\n'.join(text.split('\n')[d['line'] - 1:d['end_line']])

    same_source = set()
    for n, d in O.items():
        if d['kind'] == 'def' and n in P and d['type_hash'] == P[n]['type_hash'] and not same(d, P[n]) \
                and source(OLD, d) == source(pin, P[n]):
            same_source.add(n)
            P[n] = {**P[n], 'value_hash': d['value_hash']}
    print('definitions with identical source and a different value hash:', sorted(same_source))
    changed_defs = {n for n, d in O.items() if d['kind'] == 'def' and (n not in P or not same(d, P[n]))}
    print('changed definitions:', len(changed_defs))
    by_hash = collections.defaultdict(list)
    for n, d in P.items():
        if n not in O:
            by_hash[(d['type_hash'], d['kind'], d.get('value_hash'))].append(n)

    reach_memo = {}

    def reached_changed(name):
        """Changed definitions reachable from `name`'s type through definition values (at ce82a5b)."""
        if name in reach_memo:
            return reach_memo[name]
        seen, todo, hit = set(), list(O[name]['type_consts']), set()
        while todo:
            c = todo.pop()
            if c in seen or c not in O:
                continue
            seen.add(c)
            if c in changed_defs:
                hit.add(c)
            if O[c]['kind'] == 'def':
                todo += O[c]['value_consts']
        reach_memo[name] = sorted(hit)
        return reach_memo[name]

    def resolve(name):
        if not name.startswith('TernaryGoldbach.'):
            m = ML.get(name)
            if m and m['found']:
                return dict(decl=name, cls='unchanged', module=m['module'], line=m['line'], source='mathlib')
            return dict(decl=name, cls='gone', source='mathlib', reason='not found at P')
        o = O.get(name)
        if o is None:
            return dict(decl=name, cls='gone', reason='not in the ce82a5b index')
        p = P.get(name)
        if p is None:
            cands = by_hash.get((o['type_hash'], o['kind'], o.get('value_hash')), [])
            if len(cands) == 1:
                q = P[cands[0]]
                return dict(decl=name, cls='moved', new_decl=cands[0], module=q['module'], line=q['line'],
                            old_module=o['module'], reason='same type under a new name')
            return dict(decl=name, cls='gone', old_module=o['module'], old_line=o['line'],
                        reason='no declaration of this name at P' + (f'; {len(cands)} same-type candidates' if cands else ''))
        r = dict(decl=name, module=p['module'], line=p['line'], end_line=p['end_line'], kind=p['kind'],
                 old_module=o['module'], old_line=o['line'], in_cone=p['in_cone'])
        why = []
        if o['type_hash'] != p['type_hash']:
            why.append('type differs only in its Fact hypotheses' if strip_facts(o['type']) == strip_facts(p['type'])
                       else 'type differs')
        if o['kind'] == 'def' and o.get('value_hash') != p.get('value_hash'):
            why.append('definition value differs')
        via = [c for c in reached_changed(name) if c != name]
        if why and why[0].startswith('type differs only in its Fact'):
            via = [c for c in via if c not in DROPPED]
        if via:
            why.append('reaches changed definitions: ' + ', '.join(via))
        if why:
            r.update(cls='changed', reason='; '.join(why), old_type=o['type'], new_type=p['type'],
                     old_facts=o.get('facts', []), new_facts=p.get('facts', []))
        elif o['module'] != p['module']:
            r.update(cls='moved', reason='same statement in a new module')
        else:
            r.update(cls='unchanged')
        return r

    # docstrings at P that are new or changed, for the absence search of declaration-free items
    new_docs = [(n, d['doc']) for n, d in P.items() if d['doc'] and (n not in O or O[n]['doc'] != d['doc'])]

    def cited(it):
        num = re.escape(it['number'])
        if it['kind'] == 'equation':
            pat = re.compile(r'\(' + num + r'\)')
        else:
            word = {'theorem': 'Thm|Theorem', 'lemma': 'Lemma|Lem', 'proposition': 'Prop|Proposition',
                    'corollary': 'Cor|Corollary', 'figure': 'Figure|Fig', 'table': 'Table'}[it['kind']]
            pat = re.compile(r'(?:' + word + r')\.?\s*' + num + r'(?![\d.]*\d)')
        return sorted({n for n, doc in new_docs if pat.search(doc)})

    out, counts = [], collections.Counter()
    for it in items:
        decls = [resolve(l['decl']) for l in it['lean']]
        cls = max((d['cls'] for d in decls), key=ORDER.index, default='unchanged')
        rec = dict(id=it['id'], cls=cls, decls=decls)
        named = {d['decl'] for d in decls} | {d.get('new_decl') for d in decls}
        c = [n for n in cited(it) if n not in named]
        if c:
            rec['cited_at_p'] = c
        rec['rejudge'] = cls in ('changed', 'gone') or it['verification']['protocol'] != 'complete' or bool(rec.get('cited_at_p'))
        rec['rejudge_reasons'] = ([cls] if cls in ('changed', 'gone') else []) + \
            (['unverified'] if it['verification']['protocol'] != 'complete' else []) + \
            (['cited at P'] if rec.get('cited_at_p') else [])
        counts[cls] += 1
        out.append(rec)
    json.dump(dict(old=OLD, new=pin, same_source_definitions=sorted(same_source), items=out), open(out_path, 'w'),
              indent=1, ensure_ascii=False)
    print('items by class', dict(counts))
    print('decls by class', dict(collections.Counter(d['cls'] for r in out for d in r['decls'])))
    print('changed reasons', collections.Counter(d['reason'].split(':')[0] for r in out for d in r['decls'] if d['cls'] == 'changed'))
    print('rejudge', sum(r['rejudge'] for r in out), collections.Counter(tuple(r['rejudge_reasons']) for r in out))


main()
