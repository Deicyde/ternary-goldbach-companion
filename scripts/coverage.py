"""Write docs/coverage.md and data/coverage.json: how much of each text [L] formalizes, by class.

New code, standard library only.  Everything is computed from the annotations as the viewer reads them
(<overlay>/pdf-overlay/annotations.bundle.json, written by `cf overlay sync`) and from the data files:
data/items.json and data/items-paper-2013.json (chapters, errata), data/<overlay>-displays.json and
data/<overlay>-steps.json (chapters, pages, LaTeX), data/<overlay>-{displays,steps}-mapping.json (the
confirmed text errors, the searches, how each verdict was checked).  It also rewrites the README's
"Coverage" section, between its two `coverage` comment lines.

Records and their class (the definitions are written into docs/coverage.md):
- a statement is a numbered theorem, lemma, proposition or corollary; a display is a numbered equation
  or an unnumbered display outside proofs; a step is a proof step;
- an item's key relation is the strongest relation of its key links to calr3/ternary-goldbach or
  Mathlib, in the order of the classes; with no key link, a checked absence gives `noMatch`, and else a
  link that only supports the item counts as `relatedMatch`; links to this repository's lean/ and to
  the book's PDF are not links to [L];
- a record whose text a confirmed erratum (items.json) or a confirmed text error (the mapping's
  `text_error`) says is wrong is Deviates, whatever its relation.

Usage: python3 -I scripts/coverage.py [<repository root>]
"""
import collections
import json
import os
import re
import sys

NS = 'org.mathlib-initiative.formal-companion.overlay'
CLASSES = ('1-to-1', 'Faithful', 'Partial', 'Deviates', 'Absent', 'Unjudged')
CLASS_OF = {'exactMatch': '1-to-1', 'closeMatch': 'Faithful', 'broadMatch': 'Faithful', 'hasPart': 'Partial',
            'narrowMatch': 'Deviates', 'relatedMatch': 'Deviates', 'noMatch': 'Absent'}
FORMALIZED = ('1-to-1', 'Faithful')
STATEMENT_KINDS = {'theorem', 'lemma', 'proposition', 'corollary'}
TYPES = ('statements', 'displays', 'steps')
OVERLAYS = (('book', 'Helfgott, *The ternary Goldbach problem* (arXiv:1501.05438v2)', 'Chapter'),
            ('paper-2013', 'Helfgott, *The ternary Goldbach conjecture is true* (arXiv:1312.7748v2)', 'Section'))
PREFIX = 'TernaryGoldbach.'
LONGEST = 20

DEFINITIONS = """For each record take its key relation: for an item, the strongest relation of its key links;
for a step, its own relation.

| Class | Relations | Meaning |
|---|---|---|
| **1-to-1** | `exactMatch` | [L] states or establishes exactly this |
| **Faithful** | `closeMatch`, `broadMatch` | the same up to a named difference, or [L] proves more |
| **Partial** | `hasPart` | [L] carries part of it |
| **Deviates** | `narrowMatch`; a confirmed finding or erratum; `relatedMatch` where [L] argues differently | [L] proves less, or something else, or the text is wrong |
| **Absent** | `noMatch` | searched for, not in [L] |
| **Unjudged** | none | no completed verdict |

**"Formalized" means 1-to-1 + Faithful.** Report every percentage with its count, as
"41/52 (79%)". Never report a percentage without its denominator."""

METHOD = """AI agents judged every relation: the numbered items on 2026-11-06 (a mapper, a verifier and a judge per batch), re-judged at the pin on 2026-11-12, and the displays and proof steps on 2026-11-12 (a mapper and an independent verifier per batch, a judge on every disagreement, and an audit of the absences). Verdicts were checked mechanically (every declaration and line range against the build at the pin, every snippet against the pinned source), by a second agent's re-search of one agreed absence in five and then of every other agreed absence, and by a random 5% sample read by the session lead, itself an agent; a claim that the text is wrong counts only when two independent skeptics confirm it and a re-run check script or the Lean backs it. No person has reviewed any verdict."""


def frac(k, n):
    return f'{k}/{n} ({100 * k / n:.0f}%)' if n else '—'


def cell(text):
    return ' '.join(str(text).split()).replace('|', '\\|')


def decl_name(d):
    return d[len(PREFIX):] if d.startswith(PREFIX) else d


def first_sentence(text):
    text = ' '.join((text or '').split())
    m = re.search(r'(?<!\b[A-Z])(?<!\be\.g)(?<!\bi\.e)(?<!\bcf)(?<!\bp)(?<!\bpp)(?<!\bvs)(?<!\bThm)(?<!\bProp)'
                  r'(?<!\bLem)(?<!\bEq)(?<!\bCh)(?<!\bSec)(?<!\bCor)\.\s+(?=[A-Z(`\[])', text)
    return text[:m.start() + 1] if m else text


def chapter_key(ch):
    return (0, int(ch), '') if ch.isdigit() else (1, 0, ch)


def verification_words(v):
    steps = v.get('steps') or v.get('book_verification', {}).get('steps') or []
    words = []
    if any(s.startswith('judge') and 'noMatch' not in s for s in steps):
        words.append(f"judge ruling ({v.get('ruling', 'own record')})" if v.get('ruling') else 'judge ruling')
    elif any(s.startswith('absence audit') for s in steps):
        words.append('absence audit')
    elif any('noMatch search re-run' in s for s in steps):
        words.append('absence re-searched by a judge')
    else:
        words.append('mapper and verifier agreed')
    if any('sample check' in s for s in steps):
        words.append('changed in the sample check')
    if v.get('carried_from'):
        words.append(f"carried from book's {v['carried_from']}")
    return ', '.join(words)


def load(root, name):
    return json.load(open(os.path.join(root, 'data', name), encoding='utf-8'))


def overlay_records(root, overlay, lean_uris):
    """[{id, type, kind, chapter, page, relation, class, ...}] of one overlay."""
    bundle = json.load(open(os.path.join(root, overlay, 'pdf-overlay', 'annotations.bundle.json'), encoding='utf-8'))
    by_id = collections.defaultdict(list)
    for row in bundle['annotations']:
        by_id[row['annotation']['id']].append(row['annotation'])
    if overlay == 'book':
        items = {i['id']: i for i in load(root, 'items.json')['items']}
        chapter_of_item = {k: i['chapter'] for k, i in items.items()}
    else:
        items = {i['id']: i for i in load(root, 'items-paper-2013.json')['items']}
        chapter_of_item = {k: i['section'] for k, i in items.items()}
    texts = {d['id']: d for d in load(root, f'{overlay}-displays.json')['displays']}
    texts.update({s['id']: s for s in load(root, f'{overlay}-steps.json')['steps']})
    maps = {r['id']: r for k in ('displays', 'steps') for r in load(root, f'{overlay}-{k}-mapping.json')['records']}

    def page_of(recs):
        loc = recs[0].get('extensions', {}).get(NS, {}).get('locator', {})
        return (loc.get('printed') or loc.get('physical') or [None])[0]

    out = []
    for rid, recs in by_id.items():
        kind = recs[0]['kind']
        rec = {'id': rid, 'kind': kind, 'page': page_of(recs)}
        if kind == 'proof_step' or kind == 'display':
            m = maps[rid]
            r = recs[0]
            rec.update(type='steps' if kind == 'proof_step' else 'displays', chapter=texts[rid]['chapter' if overlay == 'book' else 'section'],
                       relation=r.get('relation'), note=r.get('note') or '', item=m.get('item'),
                       declarations=list(dict.fromkeys(e['location']['declaration'] for r in recs for e in r['object'])),
                       verification=verification_words(m['verification']),
                       length=len(' '.join(texts[rid]['latex'].split())))
            if m.get('text_error'):
                rec['erratum'] = {'kind': m['text_error']['kind'], 'evidence': m['text_error']['evidence'],
                                  'confirmed_by': m['text_error']['confirmed_by']}
            if rec['relation'] == 'noMatch':
                rec['searched'] = m.get('searched', {}).get('declarations') or rec['declarations']
        else:
            rec.update(type='statements' if kind in STATEMENT_KINDS else 'displays' if kind == 'equation' else 'other',
                       chapter=chapter_of_item[rid])
            lean = [r for r in recs if r['object'] and all(o.get('type') == 'lean' and o.get('uri') in lean_uris for o in r['object'])]
            key = [r for r in lean if r.get('relation') and r.get('relation') != 'noMatch'
                   and any(o.get('role') == 'key' for o in r['object'])]
            rank = lambda r: CLASSES.index(CLASS_OF.get(r['relation'], 'Unjudged'))
            if key:
                best = min(rank(r) for r in key)
                rec['relation'] = min((r for r in key if rank(r) == best), key=lambda r: r['relation'])['relation']
                rec['declarations'] = [r['object'][0]['location']['declaration'] for r in key if rank(r) == best]
            elif any(r.get('relation') == 'noMatch' for r in lean):
                rec['relation'], rec['declarations'] = 'noMatch', []
            elif any(r.get('relation') for r in lean):
                rec['relation'] = 'relatedMatch'
                rec['declarations'] = [r['object'][0]['location']['declaration'] for r in lean if r.get('relation')]
            else:
                rec['relation'], rec['declarations'] = None, []
            notes = [r.get('note') or '' for r in (lean or recs)]
            rec['note'] = next((n for n in notes if n), '')
            rec['verification'] = recs[0].get('extensions', {}).get(NS, {}).get('provenance', {}).get('method', '')
            er = items[rid].get('erratum', {}) if overlay == 'book' else {}
            if er.get('present') and er.get('check', {}).get('state') == 'confirmed':
                c = er['check']
                rec['erratum'] = {'kind': c.get('kind') or er['kind'],
                                  'evidence': f"lean/ `{c['theorem']}`" if c.get('theorem') else c['script']}
                said = next((m.group(1) for n in notes for m in [re.search(r'\b(?:Erratum|Typo): (.*)', n)] if m), '')
                if said:  # the note's erratum sentence, without the check it cites (the evidence column)
                    rec['erratum']['said'] = re.sub(r'\s*\((?:checked|proved) by [^()]*\)\.?$', '.', said)
        rec['class'] = 'Deviates' if rec.get('erratum') else CLASS_OF.get(rec['relation'], 'Unjudged')
        rec['relation_class'] = CLASS_OF.get(rec['relation'], 'Unjudged')
        out.append(rec)
    return out


def counts(recs):
    c = collections.Counter(r['class'] for r in recs)
    return {k: c[k] for k in CLASSES}


def summarize(recs):
    head = {}
    for t in TYPES:
        rs = [r for r in recs if r['type'] == t]
        head[t] = {'total': len(rs), 'classes': counts(rs), 'formalized': sum(1 for r in rs if r['class'] in FORMALIZED)}
    # displays split: numbered equations and unnumbered displays
    for sub, kind in (('numbered displays', 'equation'), ('unnumbered displays', 'display')):
        rs = [r for r in recs if r['kind'] == kind]
        head[sub] = {'total': len(rs), 'classes': counts(rs), 'formalized': sum(1 for r in rs if r['class'] in FORMALIZED)}
    chapters = []
    for ch in sorted({r['chapter'] for r in recs}, key=chapter_key):
        rs = [r for r in recs if r['chapter'] == ch and r['type'] in TYPES]
        row = {'chapter': ch}
        for t in TYPES:
            ts = [r for r in rs if r['type'] == t]
            row[t] = [sum(1 for r in ts if r['class'] in FORMALIZED), len(ts)]
        st = [r for r in rs if r['type'] == 'steps']
        row['steps_absent'] = [sum(1 for r in st if r['class'] == 'Absent'), len(st)]
        row['deviations'] = [sum(1 for r in rs if r['class'] == 'Deviates'), len(rs)]
        row['displays_1to1'] = [sum(1 for r in rs if r['type'] == 'displays' and r['class'] == '1-to-1'), row['displays'][1]]
        row['steps_1to1'] = [sum(1 for r in st if r['class'] == '1-to-1'), len(st)]
        row['displays_absent'] = [sum(1 for r in rs if r['type'] == 'displays' and r['class'] == 'Absent'), row['displays'][1]]
        chapters.append(row)
    return head, chapters


def extremes(chapters, t, label):
    rows = [(r[t][0] / r[t][1], r) for r in chapters if r[t][1]]
    if not rows:
        return f'no {t}'
    hi, lo = max(s for s, _ in rows), min(s for s, _ in rows)
    def name(s):
        rs = [r for v, r in rows if v == s]
        if len(rs) == 1:
            return f"{label.lower()} {rs[0]['chapter']}, {frac(*rs[0][t])}"
        return f"{label.lower()}s " + ', '.join(f"{r['chapter']} ({r[t][0]}/{r[t][1]})" for r in rs) + f', {100 * s:.0f}% each'
    if hi == lo:
        return f'the same share in every {label.lower()}: {name(hi)}'
    return f'most formalized {name(hi)}; least {name(lo)}'


def headline_table(head):
    lines = ['| | ' + ' | '.join(CLASSES) + ' | Formalized |', '|---|' + '---|' * (len(CLASSES) + 1)]
    for t in TYPES + ('numbered displays', 'unnumbered displays'):
        h = head[t]
        name = t.capitalize() if t in TYPES else f'&nbsp;&nbsp;of which {t}'
        lines.append(f'| {name} | ' + ' | '.join(frac(h['classes'][c], h['total']) for c in CLASSES)
                     + f" | **{frac(h['formalized'], h['total'])}** |")
    return lines


def chapter_table(chapters, label):
    lines = [f'| {label} | Statements formalized | Displays formalized | Steps formalized | Steps absent | Deviations |',
             '|---|---|---|---|---|---|']
    for r in chapters:
        lines.append(f"| {r['chapter']} | {frac(*r['statements'])} | {frac(*r['displays'])} | {frac(*r['steps'])} | "
                     f"{frac(*r['steps_absent'])} | {frac(*r['deviations'])} |")
    return lines


def extremes_line(chapters, label):
    return (f"By statement share: {extremes(chapters, 'statements', label)}. "
            f"By step share: {extremes(chapters, 'steps', label)}.")


def deviates_line(recs):
    st = [r for r in recs if r['type'] == 'statements' and r['class'] == 'Deviates']
    er = sum(1 for r in st if r.get('erratum'))
    rel = collections.Counter(r['relation'] for r in st if not r.get('erratum'))
    return (f"Of the {len(st)} statements that deviate, {er} have a confirmed erratum; of the others, [L] proves less "
            f"(`narrowMatch`) for {rel['narrowMatch']} and does the work another way (`relatedMatch`) for {rel['relatedMatch']}.")


def evidence(r):
    if r.get('erratum'):
        e = r['erratum']
        what = 'typo' if e['kind'] == 'typo' else 'error'
        how = f"`{e['evidence']}`" if not e['evidence'].startswith('lean/') else e['evidence']
        who = '; two skeptics' if e.get('confirmed_by') else ''
        return f'confirmed {what}: {how}{who}'
    return f"judged `{r['relation']}` ({r['verification']})"


def label_of(r):
    if r['type'] == 'steps':
        return r['id']
    if r['kind'] == 'equation':
        return f"({r['id'].split(' ', 1)[1]})"
    return r['id']


def decls_text(ds, cap=4):
    ds = [f'`{decl_name(d)}`' for d in ds]
    return ', '.join(ds[:cap]) + (f', … ({len(ds) - cap} more)' if len(ds) > cap else '') if ds else '—'


def write_doc(root, results):
    md = ['# Coverage', '',
          '> Unreviewed machine audit. AI agents produced every verdict; no mathematician has checked any of it.', '',
          'How much of each text [L] (calr3/ternary-goldbach at `' + results['pin'] + '`) formalizes, by record and by',
          'class. Written by `scripts/coverage.py` from the annotations and `data/`; the numbers are in',
          '`data/coverage.json`. Declarations are named without the `TernaryGoldbach.` prefix.', '',
          'Contents: 1. Headline · 2. By chapter · 3. 1-to-1 · 4. Deviations · 5. Absent · 6. Definitions and method', '']
    md += ['## 1. Headline', '']
    for ov, title, label in OVERLAYS:
        res = results['overlays'][ov]
        md += [f'### {title}', ''] + headline_table(res['headline']) + ['']
        o = res['other']
        if o:
            md += [f"Not counted: {o} figures and tables. Statements are the numbered theorems, lemmas, propositions"
                   " and corollaries; displays the numbered equations and the unnumbered displays outside proofs.", '']
        md += [deviates_line(res['records']), '']
        moved = res['erratum_moves']
        if moved:
            md += [f"Of the Deviates, {moved} records have a relation of another class but a confirmed erratum or text"
                   " error (section 4).", '']
    md += ['## 2. By chapter', '']
    for ov, title, label in OVERLAYS:
        res = results['overlays'][ov]
        md += [f'### {title}', ''] + chapter_table(res['chapters'], label) + ['', extremes_line(res['chapters'], label), '']
        if ov == 'book':
            md += ['A proof step is counted in the chapter where it is printed (the proof of Theorem 3.1.1 is in chapter 6).',
                   '"Deviations" counts the Deviates records among all the chapter\'s statements, displays and steps.', '']
    md += ['## 3. 1-to-1', '']
    for ov, title, label in OVERLAYS:
        res = results['overlays'][ov]
        recs = res['records']
        md += [f'### {title}', '', 'Statements:', '']
        one = [r for r in recs if r['type'] == 'statements' and r['class'] == '1-to-1']
        for r in sorted(one, key=lambda r: (chapter_key(r['chapter']), r['page'] or 0)):
            md.append(f"- {r['id']}: {decls_text(r['declarations'])}, p. {r['page']}")
        if not one:
            md.append('- none')
        md += ['', f'Displays and steps, by {label.lower()}:', '', f'| {label} | Displays 1-to-1 | Steps 1-to-1 |', '|---|---|---|']
        for c in res['chapters']:
            md.append(f"| {c['chapter']} | {frac(*c['displays_1to1'])} | {frac(*c['steps_1to1'])} |")
        md.append('')
    md += ['## 4. Deviations', '',
           'Every Deviates record, by chapter; in each chapter, the records with a confirmed erratum or text error come',
           'first. "Text against [L]" is the first sentence of the record\'s note. Evidence: the check that confirmed an',
           'error, or the judged relation and how it was judged.', '']
    for ov, title, label in OVERLAYS:
        res = results['overlays'][ov]
        recs = [r for r in res['records'] if r['class'] == 'Deviates' and r['type'] in TYPES]
        md += [f'### {title}', '']
        for c in res['chapters']:
            rs = [r for r in recs if r['chapter'] == c['chapter']]
            if not rs:
                continue
            rs.sort(key=lambda r: (not r.get('erratum'), TYPES.index(r['type']), r['page'] or 0))
            md += [f"#### {label} {c['chapter']} ({len(rs)})", '', '| Record | p. | Text against [L] | Declarations | Evidence |',
                   '|---|---|---|---|---|']
            for r in rs:
                said = r.get('erratum', {}).get('said') or first_sentence(r['note'])
                md.append(f"| {cell(label_of(r))} | {r['page']} | {cell(said) or '—'} | "
                          f"{cell(decls_text(r['declarations'], 3))} | {cell(evidence(r))} |")
            md.append('')
    md += ['## 5. Absent', '']
    for ov, title, label in OVERLAYS:
        res = results['overlays'][ov]
        recs = res['records']
        md += [f'### {title}', '', 'Absent statements:', '']
        ab = [r for r in recs if r['type'] == 'statements' and r['class'] == 'Absent']
        for r in sorted(ab, key=lambda r: (chapter_key(r['chapter']), r['page'] or 0)):
            md.append(f"- {r['id']}, p. {r['page']}: {cell(r['note']) or 'no note'}")
        if not ab:
            md.append('- none')
        md += ['', f'Absent displays and steps, by {label.lower()}:', '', f'| {label} | Displays absent | Steps absent |', '|---|---|---|']
        for c in res['chapters']:
            md.append(f"| {c['chapter']} | {frac(*c['displays_absent'])} | {frac(*c['steps_absent'])} |")
        md += ['', f'The {LONGEST} longest absent steps, the most text with no counterpart (length: characters of the step\'s LaTeX, whitespace collapsed); the last column is the record\'s note:', '',
               '| Step | p. | Length | Note |', '|---|---|---|---|']
        steps = sorted((r for r in recs if r['type'] == 'steps' and r['class'] == 'Absent'), key=lambda r: -r['length'])
        for r in steps[:LONGEST]:
            md.append(f"| {r['id']} | {r['page']} | {r['length']} | {cell(r['note'])} |")
        md.append('')
    md += ['## 6. Definitions and method', '', DEFINITIONS, '', METHOD, '',
           'How the class of a record is taken here: an item\'s key links are its links of role `key` to',
           'calr3/ternary-goldbach or Mathlib (not its links to this repository\'s `lean/` or to the book\'s PDF); with',
           'none, a checked absence makes it Absent, and a link that only supports it counts as `relatedMatch`. A',
           'record whose text a confirmed erratum (`data/items.json`) or text error (`text_error` in',
           '`data/<overlay>-{steps,displays}-mapping.json`) says is wrong is Deviates whatever its relation; the',
           '`class` field of the mapping files is the class of the relation alone. A paper item takes no erratum',
           'from its book counterpart.', '']
    open(os.path.join(root, 'docs', 'coverage.md'), 'w', encoding='utf-8').write('\n'.join(md))


def write_readme(root, results):
    path = os.path.join(root, 'README.md')
    text = open(path, encoding='utf-8').read()
    lines = ['<!-- coverage: written by scripts/coverage.py -->', '## Coverage', '',
             'Each statement, display and proof step has one class (`docs/coverage.md` section 6); "formalized" is',
             "1-to-1 + Faithful. Details, the paper's sections, the 1-to-1 list, every deviation and the absences:",
             '[`docs/coverage.md`](docs/coverage.md).', '']
    for ov, title, label in OVERLAYS:
        res = results['overlays'][ov]
        h = res['headline']
        lines += [f'{title}:', '', '| | Formalized | 1-to-1 | Deviates | Absent |', '|---|---|---|---|---|']
        for t in TYPES:
            lines.append(f"| {t.capitalize()} | {frac(h[t]['formalized'], h[t]['total'])} | {frac(h[t]['classes']['1-to-1'], h[t]['total'])} | "
                         f"{frac(h[t]['classes']['Deviates'], h[t]['total'])} | {frac(h[t]['classes']['Absent'], h[t]['total'])} |")
        lines += ['', deviates_line(res['records']), '']
        if ov == 'book':
            lines += chapter_table(res['chapters'], label) + ['', extremes_line(res['chapters'], label), '']
    lines.append('<!-- /coverage -->')
    block = '\n'.join(lines)
    rx = re.compile(r'<!-- coverage: written by scripts/coverage.py -->.*?<!-- /coverage -->', re.S)
    if rx.search(text):
        text = rx.sub(lambda m: block, text)
    else:
        anchor = '\n## Formal statements'
        if anchor not in text:
            sys.exit('README.md: no "## Formal statements" section to put the coverage before')
        text = text.replace(anchor, '\n' + block + '\n' + anchor, 1)
    open(path, 'w', encoding='utf-8').write(text)


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pins = load(root, 'pins.json')
    lean_uris = {pins['lean']['uri'], pins['mathlib']['uri']}
    results = {'schema': 'tg-companion/coverage', 'pin': pins['lean']['commit'], 'classes': list(CLASSES),
               'formalized': list(FORMALIZED), 'overlays': {}}
    for ov, title, label in OVERLAYS:
        recs = overlay_records(root, ov, lean_uris)
        head, chapters = summarize(recs)
        results['overlays'][ov] = {
            'title': title, 'unit': label.lower(), 'headline': head, 'chapters': chapters,
            'other': sum(1 for r in recs if r['type'] == 'other'),
            'erratum_moves': sum(1 for r in recs if r.get('erratum') and r['relation_class'] != 'Deviates'),
            'records': sorted(recs, key=lambda r: (TYPES.index(r['type']) if r['type'] in TYPES else 3,
                                                   chapter_key(r['chapter']), r['page'] or 0, r['id']))}
    write_doc(root, results)
    with open(os.path.join(root, 'data', 'coverage.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=1, ensure_ascii=False)
        f.write('\n')
    write_readme(root, results)
    for ov, *_ in OVERLAYS:
        h = results['overlays'][ov]['headline']
        print(ov, {t: f"{h[t]['formalized']}/{h[t]['total']}" for t in TYPES})


if __name__ == '__main__':
    main()
