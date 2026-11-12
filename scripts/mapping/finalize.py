"""Assemble the item list at P (`data/items.json`) and the re-pin record (`data/repin.json`).

New code.  Inputs, all produced by this repository's scripts or by the review passes they feed:

* the merged 2026-11-06 mapping (`merge_journals.py`) and its re-pin classification (`repin.py`);
* the re-judged verdicts at P, one JSON file per batch of at most 20 items;
* the absence searches at P for items judged not formalized and not re-judged;
* the re-run erratum checks (`scripts/checks/`), one JSON file per batch;
* the declaration index at P (`DeclIndex.lean`), for each declaration's module, kind and the line
  of its keyword, checked against the source tree at P;
* the overrides of the sample check (item id -> status and note).

Usage: python3 -I finalize.py <items_merged.json> <repin.json> <rejudge dir> <absence dir> <errata dir>
       <lean_index_P.json> <mathlib_P.json> <tg checkout> <sample.json> <out dir>
"""
import collections
import glob
import json
import os
import re
import sys

FORMAL = {  # the 28 formal statements of 2026-11-06 that refute the printed claim; session 2 re-checks them
    'Eq 5.32': 'Companion/Book/Eq_5_32.lean', 'Eq 5.36': 'Companion/Book/Eq_5_36.lean',
    'Theorem 7.1.1': 'Companion/Book/Thm_7_1_1.lean', 'Proposition 11.2.3': 'Companion/Book/Prop_11_2_3.lean',
    'Proposition D.0.3': 'Companion/Book/Prop_D_0_3.lean'}
CLUSTER_C = {'Lemma C.1.1', 'Eq C.1', 'Lemma C.1.2', 'Eq C.2', 'Corollary C.1.3', 'Eq C.5'}
KEYWORD = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|nonrec|partial|unsafe)\s+)*'
                     r'(theorem|lemma|def|abbrev|structure|inductive|instance|class|opaque|axiom)\s+(\S+)')


def load_batches(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, '*.json'))):
        if os.path.basename(f) in ('INSTRUCTIONS.json',):
            continue
        data = json.load(open(f))
        for x in data.get('items', []):
            out[x['id']] = dict(x, batch=data.get('batch'))
    return out


def main():
    (merged_p, repin_p, rejudge_d, absence_d, errata_d, index_p, mathlib_p, tg, sample_p, out_d) = sys.argv[1:11]
    items = json.load(open(merged_p))
    repin = json.load(open(repin_p))
    rp = {r['id']: r for r in repin['items']}
    rej = load_batches(rejudge_d)
    absn = load_batches(absence_d)
    errs = load_batches(errata_d)
    P = {d['name']: d for d in json.load(open(index_p))}
    ML = {d['name']: d for d in json.load(open(mathlib_p)) if d['found']}
    sample = json.load(open(sample_p))
    files = {}

    def keyword_line(d):
        f = os.path.join(tg, d['module'].replace('.', '/') + '.lean')
        if f not in files:
            files[f] = open(f, encoding='utf-8').read().split('\n')
        lines, last = files[f], d['name'].split('.')[-1]
        for i in range(d['line'] - 1, min(len(lines), d['end_line'])):
            m = KEYWORD.match(lines[i])
            if m and m.group(2).split('.')[-1] == last:
                return i + 1, m.group(1)
        raise SystemExit(f"no keyword line for {d['name']} in {f} from line {d['line']}")

    def source_lines(module, source):
        root = tg if source == 'project' else os.path.join(tg, '.lake/packages/mathlib')
        f = os.path.join(root, module.replace('.', '/') + '.lean')
        if f not in files:
            files[f] = open(f, encoding='utf-8').read().split('\n')
        return files[f]

    def snippet(d, end_line):
        """A theorem's statement through its `:=`, a definition to its first blank line, both cut at
        60 lines."""
        lines = source_lines(d['module'], d['source'])
        start, out = d['line'] - 1, []
        for i in range(start, min(len(lines), end_line, start + 60)):
            if i > start and not lines[i].strip():
                break
            out.append(lines[i])
            if d['kind'] == 'theorem' and ':=' in lines[i]:
                out[-1] = lines[i][:lines[i].index(':=') + 2]
                break
        truncated = d['kind'] == 'theorem' and not out[-1].endswith(':=') or len(out) == 60
        return dict(text='\n'.join(out).rstrip(), line=d['line'], truncated=bool(truncated))

    def resolve(name):
        if name in P:
            line, kw = keyword_line(P[name])
            return dict(decl=name, module=P[name]['module'], line=line, kind=P[name]['kind'], keyword=kw,
                        source='project', private=P[name]['private'])
        if name in ML:
            m = ML[name]
            lines = source_lines(m['module'], 'mathlib')
            line = next(i + 1 for i in range(m['line'] - 1, len(lines))
                        if (KEYWORD.match(lines[i]) or [None, None, ''])[2].split('.')[-1] == name.split('.')[-1])
            return dict(decl=name, module=m['module'], line=line, kind=m['kind'], source='mathlib')
        raise SystemExit(f'{name} does not exist at P')

    out, problems = [], []
    for it in items:
        iid, r = it['id'], rp[it['id']]
        x = dict(id=iid, kind=it['kind'], number=it['number'], chapter=it['chapter'], section=it['section'],
                 label=it['label'], tex=dict(file=it['chapter_file'] + '.tex', line=it['tex_line'],
                                             end_line=it['tex_end_line']),
                 role=it['role'])
        verification = dict(protocol_2026_11_06=it['verification']['protocol'],
                            gaps_2026_11_06=it['verification']['gaps'], mapping_batch=it['mapping']['batch'],
                            mapping_how=it['mapping']['how'], repin=r['cls'], rejudged=False)
        if iid in rej:
            j = rej[iid]
            x.update(status=j['status'], confidence=j['confidence'], book_statement=j['book_statement'],
                     note=j['note'], evidence=j['evidence'])
            links = [dict(decl=l['decl'], relation=l['relation'], note=l.get('note', '')) for l in j['lean']]
            verification.update(rejudged=True, rejudge_batch=j['batch'], rejudge_reasons=r['rejudge_reasons'],
                                previous_status=it['status'])
            if j.get('searched'):
                verification['absence_searched_at_P'] = j['searched']
        else:
            x.update(status=it['status'], confidence=it['confidence'], book_statement=it['summary'],
                     note=it['notes'], evidence='')
            links = [dict(decl=d['new_decl'] if d.get('new_decl') else l['decl'], relation=l['relation'],
                          note=l['note']) for l, d in zip(it['lean'], r['decls'])]
        if iid in absn:
            a = absn[iid]
            verification['absence_searched_at_P'] = a['searched'] if not a['found'] else ''
            if a['found']:
                x.update(status=a['status'], note=a['note'], evidence=a['evidence'])
                links = [dict(decl=l['decl'], relation=l['relation'], note=l.get('note', '')) for l in a['lean']]
                verification['absence_search_found'] = True
            for l in a.get('related') or []:
                links.append(dict(decl=l['decl'], relation='uses', note=l.get('note', '')))
        if iid in sample:
            s = sample[iid]
            verification['sample_check'] = s['verdict']
            if s.get('status'):
                verification['sample_previous_status'] = x['status']
                x.update(status=s['status'], note=s['note'])
        lean = []
        for l in links:
            d = resolve(l['decl'])
            lean.append(dict(d, relation=l['relation'], note=l['note']))
        x['lean'] = lean
        # erratum
        e = it['erratum']
        er = dict(present=bool(e.get('present')), kind=e.get('kind', 'none'))
        if er['present']:
            er.update(description=e.get('description', ''), verdict_2026_11_06=e.get('verdict'))
            if iid in FORMAL:
                er['check'] = dict(state='pending formal check', formal_statement=FORMAL[iid])
            elif iid in errs:
                c = errs[iid]
                er['check'] = dict(state=c['result'], script=c.get('script', ''), command=c.get('command', ''),
                                   output_line=c.get('output_line', ''), note=c.get('note', ''), why=c.get('why', ''))
                if c.get('kind') and c['kind'] != er['kind']:
                    er['check']['kind'] = c['kind']
            elif iid in CLUSTER_C:
                er['check'] = dict(state='unconfirmed', why='Appendix C cluster of six, not re-checked')
            else:
                er['check'] = dict(state='unconfirmed', why='no check script re-run at P'
                                   if e.get('verdict') == 'confirmed' else f"2026-11-06 skeptics: {e.get('verdict')}")
        x['erratum'] = er
        x['verification'] = verification
        x['changes_since_2013'] = it['changes_since_2013']
        out.append(x)

    decls = {}
    for x in out:
        for l in x['lean']:
            if l['decl'] not in decls:
                end = P[l['decl']]['end_line'] if l['source'] == 'project' else l['line'] + 60
                decls[l['decl']] = dict(module=l['module'], line=l['line'], kind=l['kind'], source=l['source'],
                                        private=l.get('private', False), snippet=snippet(l, end))
    os.makedirs(out_d, exist_ok=True)
    json.dump(dict(pin='192ca57362fa3ee737cd83205cb9ea99526c4553', declarations=dict(sorted(decls.items()))),
              open(os.path.join(out_d, 'decls-P.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(dict(pin='192ca57362fa3ee737cd83205cb9ea99526c4553', items=out),
              open(os.path.join(out_d, 'items.json'), 'w'), indent=1, ensure_ascii=False)
    rej_list = [dict(id=k, old=rp[k] and next(i for i in items if i['id'] == k)['status'], new=v['status'],
                     batch=v['batch'], reasons=rp[k]['rejudge_reasons'], evidence=v['evidence'])
                for k, v in rej.items()]
    json.dump(dict(old=repin['old'], new=repin['new'], method='elaborated types (Expr.hash) and definition values, '
                   'from DeclIndex.lean run at both commits; see scripts/mapping/repin.py',
                   same_source_definitions=repin['same_source_definitions'],
                   counts=dict(collections.Counter(r['cls'] for r in repin['items'])),
                   items=[dict(id=r['id'], cls=r['cls'], rejudge_reasons=r['rejudge_reasons'],
                               decls=[{k: v for k, v in d.items() if k not in ('old_type', 'new_type')} for d in r['decls']],
                               **({'cited_at_p': r['cited_at_p']} if r.get('cited_at_p') else {}))
                          for r in repin['items']],
                   rejudged=rej_list),
              open(os.path.join(out_d, 'repin.json'), 'w'), indent=1, ensure_ascii=False)
    print('items', len(out), collections.Counter(x['status'] for x in out))
    print('rejudged', len(rej), 'status changes', [(d['id'], d['old'], d['new']) for d in rej_list if d['old'] != d['new']])
    print('errata checks', collections.Counter(x['erratum'].get('check', {}).get('state') for x in out if x['erratum']['present']))


main()
