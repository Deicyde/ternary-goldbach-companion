"""Write book/annotations/: the Literature Links annotations of the book overlay.

New code, standard library only (formal-companion's route B: this producer writes the files,
`cf overlay sync` records them; formal-companion docs/overlay.md section 7 is the layout).

Reads data/items.json (the item list at the pin), data/regions-book.json (the items' regions on
the arXiv PDF), data/decls-P.json (the linked declarations at the pin: module, keyword line, kind,
statement), data/pins.json and data/statements.json (the items stated as printed in lean/), and writes

  book/annotations/_defaults.json            the PDF and the repository at the pin, as end templates
  book/annotations/<chapter>/<item>__<role>__<declaration>.json
  book/annotations/<chapter>/<item>/<role>__<declaration>.json   (an item with several records)

One record per (item, linked declaration), and per statement of the item in lean/; one checked
absence (`noMatch`) for an item judged not formalized whose absence was searched at the pin; one
record with an empty object for any other item that links nothing.  Every record names all the item's regions.

The unnumbered displays outside proofs are items of kind `display`, written like the numbered ones
(one record per declaration, or one checked absence).  The steps of an item's proof are records of
kind `proof_step` in the item's folder, `<item>/step-001.json`, ...: each end names the `lines` of a
declaration with their snippet and `proof_context`, and a `noMatch` step names the declarations it was
checked against, with no snippet (proof_overlay; formal-companion docs/overlay.md section 7).  An item
with a proof always has a folder.  The displays and steps come from data/<overlay>-displays.json,
data/<overlay>-steps.json, their -mapping.json files and data/<overlay>-regions-steps.json.

Usage: python3 -I scripts/produce.py [<repository root>]
"""
import collections
import hashlib
import json
import os
import re
import shutil
import sys

NS = 'org.mathlib-initiative.formal-companion.overlay'
ROLES = ('key', 'attributed', 'support', 'example', 'helper')
UNSAFE = re.compile(r'[^A-Za-z0-9._-]')
RESERVED = re.compile(r'(?i)(con|prn|aux|nul|com[0-9]|lpt[0-9])')
MAX_NAME = 120

# The item's status (TAXONOMY.md, 2026-11-06) -> the relation of its key links (subject: the book's
# item, object: the declaration; Literature Links docs/companion.md, "Relation").
RELATION = {
    'exact': 'exactMatch',
    'definition-match': 'exactMatch',
    'hypothesis': 'exactMatch',          # the hypothesis states the claim; the record's status says it is assumed
    'stronger': 'broadMatch',            # the declaration is more general
    'weaker': 'narrowMatch',             # the book's item is more general
    'variant': 'relatedMatch',
    'definition-differs': 'relatedMatch',
    'inlined': 'relatedMatch',           # the declaration's proof carries the item as a step
    'replaced': 'relatedMatch',          # the declaration does the item's work by another argument
    'not-formalized-not-needed': 'relatedMatch',
    'not-formalized-gap': 'relatedMatch',
    'unclear': 'relatedMatch',
}
# The item's status -> the record's Literature Links status.
STATUS = {
    'exact': 'formalized', 'definition-match': 'formalized', 'stronger': 'formalized', 'inlined': 'formalized',
    'weaker': 'partial', 'variant': 'partial', 'definition-differs': 'partial',
    'replaced': 'not_formalized', 'hypothesis': 'not_formalized',
    'not-formalized-not-needed': 'not_formalized', 'not-formalized-gap': 'not_formalized', 'unclear': 'partial',
}
# A link's role in the mapping (TAXONOMY.md lean[].relation) -> its role on the overlay.
KEY_LINKS = {'states', 'states-weaker', 'states-variant', 'defines', 'hypothesis'}
TITLE = {'theorem': 'Theorem', 'lemma': 'Lemma', 'proposition': 'Proposition', 'corollary': 'Corollary',
         'figure': 'Figure', 'table': 'Table'}
STATEMENT_PROVENANCE = {'actor': 'agent', 'method': 'stated as printed (2026-11-06); compared with the LaTeX and built at the pin',
                        'confirmed_by_human': False}
CLAIMS_ERROR = re.compile(r'(?i)\b(errat\w*|typo\w*|misprint\w*|wrong\w*|false\w*|incorrect\w*|mistake\w*|slip\w*|'
                          r'should read|flaw\w*|is not true|does not hold|fails?|correct(?:ed|ion|s)?|invalid|misquot\w*|misstat\w*|'
                          r'should be|reversed|lacks?|omits?|omitted|not established|does not follow|unproved|too (?:small|large)|'
                          r'survives|without the minus sign|gap|repair\w*|must move)\b')
PREPRINT = re.compile(r'2013|2014|preprint|\bH13\b|\[HP?13')


# the 2026-11-06 skeptics' phrasing ("the claim survives": the erratum claim was not refuted) -> what holds
JARGON = [(re.compile(r'\b[Tt]he (?:gap )?claim survives,? as (an? [^.;:,()]+)'), r'it is \1'),
          (re.compile(r'\b[Tt]he claim survives, granting\b'), 'it stands, granting'),
          (re.compile(r'(?:[,;]\s*|\s+)(?:and |so )?the (?:gap )?claim survives(?: as stated)?(?=[.;:,)])'), ''),
          (re.compile(r'(?:(?<=^)|(?<=[.;]\s))The (?:gap )?claim survives(?: as stated)?[.;:,]?\s*'), ''),
          (re.compile(r"\b[Tt]he packet's (main )?claim"), r'the \1claim'),
          (re.compile(r'\b[Tt]he claim survives\b'), 'the erratum stands'), (re.compile(r'\bdoes not survive\b'), 'does not hold'),
          (re.compile(r'\bsurvives\b'), 'still holds'), (re.compile(r'\bsurvive\b'), 'still hold'),
          (re.compile(r'\s+([.;,])'), r'\1'), (re.compile(r'[;,]\s*$'), '.'), (re.compile(r'\.\.$'), '.')]


def dejargon(text):
    text = ' '.join((text or '').split())
    for rx, rep in JARGON:
        text = rx.sub(rep, text)
    return re.sub(r'(^|[.;:]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper() if m.group(1) in ('', ) or
                  m.group(1).startswith('.') else m.group(0), text).strip()


ABBREVIATION = re.compile(r'(?:\b(?:e\.g|i\.e|cf|Prop|Thm|Lem|Cor|Ch|Sec|Eq|Eqs|pp?|resp|vs|approx|ca|al|Fig|No)\.|\b[A-Z]\.)$')


def sentences(text):
    out, cur = [], ''
    for part in re.split(r'(?<=[.!?])\s+', ' '.join((text or '').split())):
        cur = f'{cur} {part}'.strip()
        if not ABBREVIATION.search(cur):
            out.append(cur)
            cur = ''
    return out + ([cur] if cur else [])


def terse(text, keep_errors):
    """At most two sentences, without claims that [H] errs (unless confirmed) or 2013 comparisons."""
    out = [s for s in sentences(dejargon(text)) if not PREPRINT.search(s) and (keep_errors or not CLAIMS_ERROR.search(s))]
    return ' '.join(out[:2])


def file_name(key, suffix='', force_hash=False):
    """formal-companion's rule (scripts/overlay/shards.py): unsafe characters as `-`, and a name that is
    too long, reserved, `_defaults.json` or equal to another ignoring case ends in a hash of the key."""
    stem = UNSAFE.sub('-', key)
    if stem.startswith('.'):
        stem = '-' + stem[1:]
    if force_hash or len(stem) + len(suffix) > MAX_NAME or RESERVED.fullmatch(stem.split('.', 1)[0]) \
            or (stem + suffix).lower() == '_defaults.json':
        tail = '-' + hashlib.sha256(key.encode('utf-8')).hexdigest()[:10]
        stem = stem[:MAX_NAME - len(suffix) - len(tail)] + tail
    return stem + suffix


def folder_of(item):
    ch = item['chapter']
    return f'ch{int(ch):02d}' if ch.isdigit() else f'app{ch}'


def title_of(item):
    if item['kind'] == 'equation':
        return f"Equation ({item['number']})"
    return f"{TITLE[item['kind']]} {item['number']}"


# A display's or a step's relation -> its record's status (formal-companion's proof-step fixture).
STEP_STATUS = {'exactMatch': 'formalized', 'closeMatch': 'formalized', 'broadMatch': 'formalized',
               'noMatch': 'not_formalized'}


def step_note(r):
    """The mapping's note in at most two sentences, keeping the one that cites a confirmed text error."""
    s = sentences(r.get('note') or '')
    if len(s) > 2 and r.get('text_error'):
        cites = [x for x in s[1:] if r['text_error']['evidence'] in x or 'confirmed' in x]
        s = [s[0], cites[-1]] if cites else s
    return ' '.join(s[:2])


def step_provenance(r):
    v = r['verification']
    steps = v.get('steps') or v.get('book_verification', {}).get('steps') or []
    method = '; '.join(steps)
    if v.get('carried_from'):
        method = f"carried from {v['carried_from']}, the same LaTeX" + (f' ({method})' if method else '')
    return {'actor': 'agent', 'method': method, 'confirmed_by_human': False}


def proof_overlay(root, overlay, pdf, lean, mathlib, folder):
    """The unnumbered displays outside proofs and the proof steps of `overlay`, from
    data/<overlay>-{displays,steps}.json (the segmentation), data/<overlay>-{displays,steps}-mapping.json
    (the links) and data/<overlay>-regions-steps.json (the regions).  `folder(record)` is the section
    folder of a display.  Returns ({path: record} of the display items, {item id: [step records in
    proof order]})."""
    data = lambda n: json.load(open(os.path.join(root, 'data', n), encoding='utf-8'))
    regions = data(f'{overlay}-regions-steps.json')
    if regions['pdf']['sha256'] != pdf['sha256']:
        sys.exit(f'{overlay}-regions-steps.json is of another PDF')
    offset = pdf['printed_page_offset']
    texts = {d['id']: d for d in data(f'{overlay}-displays.json')['displays']}
    texts.update({s['id']: s for s in data(f'{overlay}-steps.json')['steps']})
    maps = {k: data(f'{overlay}-{k}-mapping.json') for k in ('displays', 'steps')}
    for m in maps.values():
        if m['lean']['commit'] != lean['commit'] or m['mathlib']['commit'] != mathlib['commit'] or m['mapped'] != m['total']:
            sys.exit(f"{overlay}-{m['kind']}-mapping.json is of another pin, or incomplete")

    def end(e, snippet):
        repo = lean if e['repo'] == 'lean' else mathlib
        a, b = e['lines']
        ext = {'declaration': {'id': e['declaration']}}
        if snippet:
            ext['snippet'] = {'text': e['snippet'], 'line': a, 'truncated': False}
            ext['proof_context'] = {k: e['proof_context'][k] for k in ('declaration', 'lines', 'conclusion')}
        ext['destination'] = {'resolution': 'exact', 'href': f"{repo['uri']}/blob/{repo['commit']}/{e['file']}",
                              'fragment': f'L{a}-L{b}'}
        o = {'location': {'declaration': e['declaration'], 'module': e['module'], 'lines': [a, b]}}
        if snippet:
            o['role'] = 'key'
        o['extensions'] = {NS: ext}
        if e['repo'] != 'lean':  # an end with its own uri takes nothing from the template: write it whole
            o = {'type': 'lean', 'uri': repo['uri'], 'version': repo['commit'], **o}
        return o

    def subject(rid, title):
        regs = regions['displays'].get(rid) or regions['steps'].get(rid)
        if not regs:
            sys.exit(f'{rid}: no region')
        out = []
        for n, g in enumerate(regs):
            ext = {'region': f'{rid}#{n}' if len(regs) > 1 else rid}
            if g.get('quads'):
                ext['quads'] = g['quads']
            out.append({'location': {'page': g['page'], 'rect': g['rect']}, 'title': title, 'extensions': {NS: ext}})
        return out

    def record(r, kind, title, ends, extra=None):
        subj = subject(r['id'], title)
        pages = sorted({s['location']['page'] for s in subj})
        ext = {'locator': {'physical': pages, 'printed': [p - offset for p in pages if p - offset >= 1]},
               'provenance': step_provenance(r), **(extra or {})}
        out = {'id': r['id'], 'kind': kind, 'status': STEP_STATUS.get(r['relation'], 'partial'),
               'relation': r['relation']}
        note = step_note(r)
        if note:
            out['note'] = note
        out.update(subject=subj, object=ends, extensions={NS: ext})
        return out

    displays = {}
    for r in maps['displays']['records']:
        d = texts[r['id']]
        absent = r['relation'] == 'noMatch'
        if absent:  # one checked absence, naming the declarations it was checked against
            groups = {'noMatch': [end(e, False) for e in r['ends']]}
        else:  # one record per declaration, one end per range of it
            groups = {}
            for e in r['ends']:
                groups.setdefault(f"key__{e['declaration']}", []).append(end(e, True))
        recs = [(k, record(r, 'display', d['title'], ends)) for k, ends in groups.items()]
        sec = folder(d)
        if len(recs) == 1:
            paths = [f"{sec}/{file_name(r['id'] + '__' + recs[0][0], '.json')}"]
        else:
            names = [file_name(k, '.json') for k, _ in recs]
            clash = collections.Counter(n.lower() for n in names)
            names = [file_name(k, '.json', force_hash=clash[n.lower()] > 1) for (k, _), n in zip(recs, names)]
            paths = [f"{sec}/{file_name(r['id'])}/{n}" for n in names]
        for p, (_, rec) in zip(paths, recs):
            displays[p] = rec

    steps = collections.defaultdict(list)
    for r in maps['steps']['records']:
        s = texts[r['id']]
        pages = sorted({g['page'] - offset for g in regions['steps'][r['id']]})
        where = f'p. {pages[0]}' if len(pages) == 1 else f'pp. {pages[0]}–{pages[-1]}'
        title = f"{r['id']}: {'Display' if s['kind'] == 'display' else 'Text'}, {where}"
        absent = r['relation'] == 'noMatch'
        extra = {'proof': {'kind': r['proof_kind'], **({'summary': r['summary']} if r.get('summary') else {})}} \
            if r.get('proof_kind') and not absent else None
        rec = record(r, 'proof_step', title, [end(e, not absent) for e in r['ends']], extra)
        steps[r['item']].append((s['step'], rec))
    steps = {k: [rec for _, rec in sorted(v, key=lambda x: x[0])] for k, v in steps.items()}
    return displays, steps


def step_files(folder, step_records):
    """`<item folder>/step-001.json`, ...: names that sort in the order of the proof."""
    return {f'{folder}/step-{n:03d}.json': r for n, r in enumerate(step_records, 1)}


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = lambda n: json.load(open(os.path.join(root, 'data', n), encoding='utf-8'))
    pins, items, regions, decls = data('pins.json'), data('items.json')['items'], data('regions-book.json'), \
        data('decls-P.json')['declarations']
    pdf, lean, mathlib = pins['pdf'], pins['lean'], pins['mathlib']
    stmt_path = os.path.join(root, 'data', 'statements.json')
    stmt_doc = json.load(open(stmt_path, encoding='utf-8')) if os.path.exists(stmt_path) else {'statements': []}
    statements = collections.defaultdict(list)
    for st in stmt_doc['statements']:
        statements[st['item']].append(st)
    if regions['pdf']['sha256'] != pdf['sha256'] or regions['pdf']['pages'] != pdf['physical_page_count']:
        sys.exit('regions-book.json is of another PDF')

    defaults = {
        'subject': {
            'type': 'pdf', 'uri': pdf['uri'], 'sha256': pdf['sha256'],
            'citation': pdf['citation'], 'identifiers': pdf['identifiers'],
            'extensions': {NS: {'source_id': pdf['source_id'], 'bytes': pdf['bytes'],
                                'physical_page_count': pdf['physical_page_count']}}},
        'object': {'type': 'lean', 'uri': lean['uri'], 'version': lean['commit']},
    }

    def lean_end(l, role):
        d = decls[l['decl']]
        ext = {'declaration': {'id': l['decl'], 'kind': d['kind']}, 'snippet': d['snippet']}
        if d.get('private'):
            ext['declaration']['private'] = True
        repo = lean if d['source'] == 'project' else mathlib
        path = d['module'].replace('.', '/') + '.lean'
        ext['destination'] = {'resolution': 'exact', 'href': f"{repo['uri']}/blob/{repo['commit']}/{path}",
                              'fragment': f"L{d['line']}"}
        end = {'location': {'declaration': l['decl'], 'module': d['module']}, 'role': role, 'extensions': {NS: ext}}
        if d['source'] != 'project':  # an end with its own uri takes nothing from the template: write it whole
            end = {'type': 'lean', 'uri': repo['uri'], 'version': repo['commit'], **end}
        return end

    display_files, steps = proof_overlay(root, 'book', pdf, lean, mathlib, folder_of)
    out_dir = os.path.join(root, 'book', 'annotations')
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    counts = collections.Counter()
    files = {}
    for it in items:
        regs = regions['items'].get(it['id'])
        if not regs:
            counts['items_without_region'] += 1
            continue
        subject = [{'location': {'page': r['page'], 'rect': r['rect']}, 'title': title_of(it),
                    'extensions': {NS: {'region': f"{it['id']}#{n}" if len(regs) > 1 else it['id']}}}
                   for n, r in enumerate(regs)]
        pages = sorted({r['page'] for r in regs})
        v = it['verification']
        prov = {'actor': 'agent', 'method': 're-judged at the pin' if v['rejudged'] else 'mapped, verified, judged',
                'confirmed_by_human': False}
        if it.get('relations_at_P'):
            prov['method'] += '; key relations re-judged blind, statement against statement (2026-11-12)'
        common = {'locator': {'physical': pages, 'printed': [p - pdf['printed_page_offset'] for p in pages
                                                              if p - pdf['printed_page_offset'] >= 1]},
                  'provenance': prov}
        er = it['erratum']
        confirmed = er.get('present') and er.get('check', {}).get('state') == 'confirmed'
        note = terse(it.get('note') or '', keep_errors=False)  # a confirmed erratum is stated from its check, below
        if not note and it.get('neutral_note'):  # what [L] states instead, for a note left empty by the strip
            note = terse(it['neutral_note'], keep_errors=False)
        if confirmed:
            kind = er['check'].get('kind') or er['kind']
            lead = 'Typo: ' if kind == 'typo' else 'Erratum: '
            first = (sentences(dejargon(er['check']['note'])) or [''])[0]
            how = f"proved by `{er['check']['theorem']}` in `{er['check']['script']}`" if er['check'].get('theorem') \
                else f"checked by `{er['check']['script']}`"
            note = (sentences(note)[0].rstrip('.') + '. ' if note else '') + lead + first.rstrip('.') + f' ({how}).'
        base = {'id': it['id'], 'kind': it['kind'], 'status': STATUS[it['status']]}
        records = []
        nf = it['status'].startswith('not-formalized')
        seen = {}
        for l in it['lean']:  # a declaration linked twice keeps its first, key-most link
            if l['decl'] not in seen or (l['relation'] in KEY_LINKS and seen[l['decl']]['relation'] not in KEY_LINKS):
                seen[l['decl']] = l
        for l in seen.values():
            key = (l['relation'] in KEY_LINKS or (l['relation'] == 'proves-inline' and it['status'] == 'inlined')
                   or (l['relation'] == 'replaces' and it['status'] == 'replaced')) and not nf
            if l['relation'] == 'hypothesis' and decls[l['decl']]['kind'] != 'def':
                key = False
            if l['relation'] == 'states-weaker':
                rel = 'narrowMatch'
            elif l['relation'] == 'states-variant':
                rel = 'relatedMatch'
            else:
                rel = RELATION[it['status']] if key else 'relatedMatch'
            if key and l['decl'] in it.get('relations_at_P', {}):  # re-judged on 2026-11-12 (scripts/mapping/review_fixes.py)
                rel = it['relations_at_P'][l['decl']]
            role = 'key' if key else 'support'
            records.append(dict(base, relation=rel, subject=subject, object=[lean_end(l, role)],
                                extensions={NS: dict(common)}))
        if nf and v.get('absence_searched_at_P'):
            records.insert(0, dict(base, relation='noMatch', subject=subject,
                                   object=[{'type': 'lean', 'uri': lean['uri'], 'version': lean['commit']}],
                                   extensions={NS: dict(common)}))
            counts['checked_absences'] += 1
        elif not records and not statements.get(it['id']):
            records.append(dict(base, subject=subject, object=[], extensions={NS: dict(common)}))
            counts['unlinked'] += 1
        # an item judged formalized whose re-judged key links state no more than a part or a special case of it
        if base['status'] == 'formalized' and it.get('relations_at_P') and not any(
                r.get('relation') in ('exactMatch', 'closeMatch', 'broadMatch') and r['object'][0].get('role') == 'key'
                for r in records if r['object']):
            for r in records:
                r['status'] = 'partial'
            counts['formalized_to_partial'] += 1
        for r in records:
            if note:
                r['note'] = note
        # the item stated as printed in this repository's lean/ (data/statements.json), with what the
        # file proves about it in the note
        for st in statements.get(it['id'], []):
            src = stmt_doc['repository']
            end = {'type': 'lean', 'uri': src['uri'], 'version': src['version'],
                   'location': {'declaration': st['declaration'], 'module': st['module']}, 'role': 'key',
                   'extensions': {NS: {'declaration': {'id': st['declaration'], 'kind': 'def'},
                                       'snippet': {'text': st['snippet'], 'line': st['line'], 'truncated': st['truncated']},
                                       'destination': {'resolution': 'exact',
                                                       'href': f"{src['uri']}/blob/{src['version']}/{st['file']}",
                                                       'fragment': f"L{st['line']}"}}}}
            records.append(dict(base, relation=st.get('relation', 'exactMatch'), subject=subject, object=[end], note=st['note'],
                                extensions={NS: dict(common, provenance=STATEMENT_PROVENANCE)}))
            counts['formal_statements'] += 1
        # file names: <item>__<role>__<declaration>, or a folder for an item with several records
        def key_of(r, in_item):
            if r.get('relation') == 'noMatch' or not r['object']:
                return 'noMatch' if in_item and r.get('relation') == 'noMatch' else it['id'] if not in_item else 'unlinked'
            o = r['object'][0]
            rest = f"{o['role']}__{o['location']['declaration']}"
            return rest if in_item else f"{it['id']}__{rest}"
        folder = folder_of(it)
        records.sort(key=lambda r: (r.get('relation') != 'noMatch',
                                    ROLES.index(r['object'][0]['role']) if r['object'] and 'role' in r['object'][0] else -1,
                                    r['object'][0]['location']['declaration'] if r['object'] and 'location' in r['object'][0] else ''))
        if len(records) == 1 and it['id'] not in steps:
            paths = [f"{folder}/{file_name(key_of(records[0], False), '.json')}"]
        else:  # an item with several records, or with a proof: a folder
            sub = file_name(it['id'])
            keys = [key_of(r, True) for r in records]
            names = [file_name(k, '.json') for k in keys]
            clash = collections.Counter(n.lower() for n in names)
            names = [file_name(k, '.json', force_hash=clash[n.lower()] > 1) for k, n in zip(keys, names)]
            if len({n.lower() for n in names}) != len(names):
                sys.exit(f"{it['id']}: two records share a file name")
            paths = [f"{folder}/{sub}/{n}" for n in names]
        proof = step_files(f"{folder}/{file_name(it['id'])}", steps.pop(it['id'], []))
        counts['proof_steps'] += len(proof)
        for p, r in list(zip(paths, records)) + list(proof.items()):
            if p.lower() in {q.lower() for q in files}:
                sys.exit(f'two files named {p}')
            files[p] = r
            counts['records'] += 1
            counts[f"relation.{r.get('relation', 'none')}"] += 1
    if steps:
        sys.exit(f'steps of items not in the overlay: {sorted(steps)}')
    for p, r in display_files.items():
        if p.lower() in {q.lower() for q in files}:
            sys.exit(f'two files named {p}')
        files[p] = r
        counts['display_records'] += 1
        counts[f"relation.{r.get('relation', 'none')}"] += 1
    counts['displays'] = len({r['id'] for r in display_files.values()})
    with open(os.path.join(out_dir, '_defaults.json'), 'w', encoding='utf-8') as f:
        json.dump(defaults, f, indent=2, ensure_ascii=False)
        f.write('\n')
    for p, r in sorted(files.items()):
        path = os.path.join(out_dir, *p.split('/'))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(r, f, indent=2, ensure_ascii=False)
            f.write('\n')
    print(json.dumps(dict(sorted(counts.items())), indent=1))


if __name__ == '__main__':
    main()
