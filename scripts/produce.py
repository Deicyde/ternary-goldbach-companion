"""Write book/annotations/: the Literature Links annotations of the book overlay.

New code, standard library only (formal-companion's route B: this producer writes the files,
`cf overlay sync` records them; formal-companion docs/overlay.md section 7 is the layout).

Reads data/items.json (the item list at the pin), data/regions-book.json (the items' regions on
the arXiv PDF), data/decls-P.json (the linked declarations at the pin: module, keyword line, kind,
statement) and data/pins.json, and writes

  book/annotations/_defaults.json            the PDF and the repository at the pin, as end templates
  book/annotations/<chapter>/<item>__<role>__<declaration>.json
  book/annotations/<chapter>/<item>/<role>__<declaration>.json   (an item with several records)

One record per (item, linked declaration); one checked absence (`noMatch`) for an item judged not
formalized whose absence was searched at the pin; one record with an empty object for any other
item that links nothing.  Every record names all the item's regions.

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
CLAIMS_ERROR = re.compile(r'(?i)\b(errat\w*|typo\w*|misprint\w*|wrong\w*|false\w*|incorrect\w*|mistake\w*|slip\w*|'
                          r'should read|flaw\w*|is not true|does not hold|fails?|correct(?:ed|ion|s)?|invalid)\b')
PREPRINT = re.compile(r'2013|2014|preprint|\bH13\b|\[HP?13')


def sentences(text):
    parts = re.split(r'(?<=\.)\s+(?=[A-Z`(\[])', ' '.join((text or '').split()))
    return [p for p in parts if p]


def terse(text, keep_errors):
    """At most two sentences, without claims that [H] errs (unless confirmed) or 2013 comparisons."""
    out = [s for s in sentences(text) if not PREPRINT.search(s) and (keep_errors or not CLAIMS_ERROR.search(s))]
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


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = lambda n: json.load(open(os.path.join(root, 'data', n), encoding='utf-8'))
    pins, items, regions, decls = data('pins.json'), data('items.json')['items'], data('regions-book.json'), \
        data('decls-P.json')['declarations']
    pdf, lean, mathlib = pins['pdf'], pins['lean'], pins['mathlib']
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
        common = {'locator': {'physical': pages, 'printed': [p - pdf['printed_page_offset'] for p in pages
                                                              if p - pdf['printed_page_offset'] >= 1]},
                  'provenance': prov}
        er = it['erratum']
        confirmed = er.get('present') and er.get('check', {}).get('state') == 'confirmed'
        note = terse(it.get('note') or '', keep_errors=bool(confirmed))
        if confirmed:
            kind = er['check'].get('kind') or er['kind']
            lead = 'Typo: ' if kind == 'typo' else 'Erratum: '
            first = (sentences(er['check']['note']) or [''])[0]
            note = (note.split('. ')[0].rstrip('.') + '. ' if note else '') + lead + first + \
                f" (checked by `{er['check']['script']}`)."
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
            role = 'key' if key else 'support'
            records.append(dict(base, relation=rel, subject=subject, object=[lean_end(l, role)],
                                extensions={NS: dict(common)}))
        if nf and v.get('absence_searched_at_P'):
            records.insert(0, dict(base, relation='noMatch', subject=subject,
                                   object=[{'type': 'lean', 'uri': lean['uri'], 'version': lean['commit']}],
                                   extensions={NS: dict(common)}))
            counts['checked_absences'] += 1
        elif not records:
            records.append(dict(base, subject=subject, object=[], extensions={NS: dict(common)}))
            counts['unlinked'] += 1
        for r in records:
            if note:
                r['note'] = note
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
        if len(records) == 1:
            paths = [f"{folder}/{file_name(key_of(records[0], False), '.json')}"]
        else:
            sub = file_name(it['id'])
            keys = [key_of(r, True) for r in records]
            names = [file_name(k, '.json') for k in keys]
            clash = collections.Counter(n.lower() for n in names)
            names = [file_name(k, '.json', force_hash=clash[n.lower()] > 1) for k, n in zip(keys, names)]
            if len({n.lower() for n in names}) != len(names):
                sys.exit(f"{it['id']}: two records share a file name")
            paths = [f"{folder}/{sub}/{n}" for n in names]
        for p, r in zip(paths, records):
            if p.lower() in {q.lower() for q in files}:
                sys.exit(f'two files named {p}')
            files[p] = r
            counts['records'] += 1
            counts[f"relation.{r.get('relation', 'none')}"] += 1
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
