"""Merge the 2026-11-06 mapping journals into one item list, and record whether each item's protocol completed.

The protocol (workflow `helfgott-companion-map`), per batch: a mapper; a verifier; a judge for the entries the
verifier disputes (any verdict but `agree`, unless a `correct` keeps the status, the set of declarations and the
presence of an erratum) and for ids the verifier lists as missing; two skeptics per claimed erratum whose kind is
not `typo` or `numbering-issue`.  The merge rule is the workflow's own: mapper, then minor verifier corrections,
then judge decisions.

An item is `unverified` when a step of its own protocol has no result: no mapper entry, no verifier result for its
batch or no review of the item, no judge decision for a disputed item, or fewer than two skeptic results for its
erratum.  An item is also `unverified` when any agent of its batch failed, even an agent of another item's
protocol (the literal reading of "a failed agent in its batch").

Usage: python3 -I merge_journals.py <book_items.json> <batches.json> <out.json> <journal.jsonl> [...]
"""
import collections
import json
import re
import sys

NOT_SKEPTIC = ('none', 'typo', 'numbering-issue')


def load(path):
    started, res, failed = {}, {}, []
    for line in open(path):
        r = json.loads(line)
        if r.get('type') == 'started':
            started[r['key']] = r.get('label')
        elif r.get('type') == 'result':
            res[r.get('label') or started.get(r['key'])] = r.get('result', r.get('value'))
        elif r.get('type') == 'failed':
            failed.append(started.get(r['key']))
    return res, failed


def decl_set(e):
    return sorted(l['decl'] for l in e.get('lean', []))


def has_erratum(e):
    return bool((e.get('erratum') or {}).get('present'))


def main():
    book_path, batches_path, out_path, journals = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    book = json.load(open(book_path))['items']
    batches = {b['id']: b for b in json.load(open(batches_path))}
    res, failed, origin = {}, collections.defaultdict(list), {}
    for j in journals:
        r, f = load(j)
        run = re.search(r'wf_[0-9a-f-]+', j).group(0)
        for k in r:
            origin[k] = run
        res.update(r)
        for lab in f:
            failed[lab.split(':')[1]].append(lab)

    final, info = {}, {}
    for bid, b in batches.items():
        m = res.get(f'map:{bid}')
        if m is None:
            continue
        v, j = res.get(f'verify:{bid}'), res.get(f'judge:{bid}')
        entries = {x['id']: x for x in m['items']}
        how = {i: 'mapper' for i in entries}
        gaps = collections.defaultdict(list)
        reviewed, disputed = set(), set()
        if v is None:
            for i in entries:
                gaps[i].append('no verifier result')
        else:
            for r in v['reviews']:
                mine = entries.get(r['id'])
                if not mine:
                    continue
                reviewed.add(r['id'])
                if r['verdict'] == 'agree':
                    how[r['id']] = 'mapper+verifier-agreed'
                    continue
                c = r.get('corrected')
                if r['verdict'] == 'correct' and c and c['status'] == mine['status'] and decl_set(c) == decl_set(mine) \
                        and has_erratum(c) == has_erratum(mine):
                    entries[r['id']] = {**c, 'id': r['id']}
                    how[r['id']] = 'verifier-corrected'
                    continue
                disputed.add(r['id'])
            for i in entries:
                if i not in reviewed:
                    gaps[i].append('no verifier review of the item')
            disputed |= {i for i in (v.get('missing') or []) if i not in entries}
        decided = set()
        if j:
            for d in j['decisions']:
                entries[d['id']] = {**d['final'], 'id': d['id']}
                how[d['id']] = 'judged'
                decided.add(d['id'])
        for i in disputed - decided:
            gaps[i].append('disputed, no judge decision' if i in entries else 'omitted by mapper, no judge entry')
        for i in b['items']:
            if i not in entries:
                gaps[i].append('no entry')
        for i in set(b['items']) | set(entries):
            e = entries.get(i)
            sk = []
            if e and has_erratum(e) and e['erratum'].get('kind') not in NOT_SKEPTIC:
                sk = [res.get(f'refute:{bid}:{i}:{k}') for k in (1, 2)]
                n = sum(1 for x in sk if x is not None)
                if n < 2:
                    gaps[i].append(f'{2 - n} of 2 skeptic results missing')
            info[i] = dict(batch=bid, run=origin.get(f'map:{bid}'), how=how.get(i, 'none'),
                           disputed=i in disputed, skeptics=[x for x in sk if x is not None],
                           gaps=gaps[i], batch_failed_agents=failed.get(bid, []))
            if e:
                final[i] = e

    out = []
    for meta in book:
        i = meta['id']
        e, p = final.get(i), info.get(i)
        er = dict((e or {}).get('erratum') or {'present': False, 'kind': 'none'})
        if er.get('present'):
            vs = (p or {}).get('skeptics', [])
            if er.get('kind') in NOT_SKEPTIC:
                er['verdict'] = 'not-checked'
            elif len(vs) < 2:
                er['verdict'] = 'incomplete'
            else:
                nref = sum(1 for x in vs if x.get('refuted'))
                er['verdict'] = 'confirmed' if nref == 0 else ('rejected' if nref == len(vs) else 'disputed')
            er['skeptics'] = [dict(refuted=x.get('refuted'), reason=x.get('reason', ''),
                                   evidence=x.get('evidence', ''),
                                   corrected_description=x.get('corrected_description', '')) for x in vs]
        gaps = list((p or {}).get('gaps', ['no batch']))
        if (p or {}).get('batch_failed_agents'):
            gaps.append('failed agent in batch: ' + ', '.join(p['batch_failed_agents']))
        out.append(dict(
            id=i, kind=meta['kind'], number=meta['number'], chapter=meta['chapter'], section=meta['section'],
            page=meta['page'], phys_page=meta['phys_page'], label=meta['label'],
            chapter_file=meta['chapter_file'], tex_line=meta['line'], tex_end_line=meta['end_line'],
            summary=(e or {}).get('summary', ''), role=(e or {}).get('role'), status=(e or {}).get('status'),
            confidence=(e or {}).get('confidence'),
            lean=[dict(decl=l['decl'], relation=l.get('relation'), where=l.get('where', ''), note=l.get('note', ''))
                  for l in (e or {}).get('lean', [])],
            erratum=er, literature=(e or {}).get('literature', []),
            changes_since_2013=(e or {}).get('changes_since_2013', ''), notes=(e or {}).get('notes', ''),
            mapping=dict(batch=(p or {}).get('batch'), run=(p or {}).get('run'), how=(p or {}).get('how'),
                         disputed=(p or {}).get('disputed'), batch_failed_agents=(p or {}).get('batch_failed_agents', [])),
            verification=dict(protocol='complete' if not gaps else 'unverified', gaps=gaps)))
    json.dump(out, open(out_path, 'w'), indent=1, ensure_ascii=False)
    c = collections.Counter(x['verification']['protocol'] for x in out)
    print(len(out), 'items;', dict(c))
    print('status', dict(collections.Counter(x['status'] for x in out)))
    print('how', dict(collections.Counter(x['mapping']['how'] for x in out)))
    print('gaps', dict(collections.Counter(g.split(':')[0] for x in out for g in x['verification']['gaps'])))
    print('unverified by own protocol only', sum(1 for x in out if any(not g.startswith('failed agent')
                                                                      for g in x['verification']['gaps'])))
    print('errata', dict(collections.Counter(f"{x['erratum']['kind']}:{x['erratum'].get('verdict')}"
                                             for x in out if x['erratum'].get('present'))))
    print('items in a batch with a failed agent', sum(1 for x in out if x['mapping']['batch_failed_agents']))


main()
