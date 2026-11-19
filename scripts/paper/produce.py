"""Write paper-2013/annotations/: the Literature Links annotations of the 2013 paper's overlay.

New code, standard library only (formal-companion's route B, as scripts/produce.py for the book).

Reads data/items-paper-2013.json (the numbered items of arXiv:1312.7748v2), data/regions-paper-2013.json
(their regions on the arXiv PDF), data/matches-paper-2013.json (each item's counterpart in [H], checked
by reading both LaTeX sources), data/regions-book.json, data/pins.json, and the book's records as the
reader reads them (book/pdf-overlay/annotations.bundle.json, written by `cf overlay sync`), and writes

  paper-2013/annotations/_defaults.json
  paper-2013/annotations/<section>/<item>__<role>__<declaration>.json
  paper-2013/annotations/<section>/<item>/<role>__<declaration>.json   (an item with several records)
  paper-2013/annotations/<section>/<item>/support__H.json             (the link to the book's item)

A paper item takes the Lean ends of its book item, one record per book record.  It keeps the book
record's relation and status when the two statements are the same up to notation; otherwise the
relation is at most `relatedMatch` and the note says what changed.  A book absence (`noMatch`) carries
over only to a statement that is the same.  One more record links the item to the book item's regions
on the book's PDF (`exactMatch` for the same statement, else `relatedMatch`).  An item with no
counterpart in [H] has one record with no relation and no object.

The displays outside proofs and the proof steps are written as for the book (produce.py, proof_overlay),
from data/paper-2013-*.json.

Usage: python3 -I scripts/paper/produce.py [<repository root>]
"""
import collections
import importlib.util
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('book_produce', os.path.join(HERE, '..', 'produce.py'))
book = importlib.util.module_from_spec(spec)
spec.loader.exec_module(book)
NS, ROLES, file_name = book.NS, book.ROLES, book.file_name

TITLE = {'theorem': 'Theorem', 'lemma': 'Lemma', 'proposition': 'Proposition', 'corollary': 'Corollary'}
# a record's status, for a statement that changed: no better than partial
CHANGED_STATUS = {'formalized': 'partial', 'partial': 'partial', 'not_formalized': 'not_formalized'}


def title_of(item):
    if item['kind'] == 'equation':
        return f"Equation ({item['number']})"
    return f"{TITLE[item['kind']]} {item['number']}"


def book_ref(book_id):
    """`Eq 11.12` -> `[H] (11.12)`; `Lemma 11.2.1` -> `[H] Lemma 11.2.1`."""
    kind, num = book_id.split(' ', 1)
    return f'[H] ({num})' if kind == 'Eq' else f'[H] {book_id}'


def folder_of(item):
    s = item['section']
    return f'sec{int(s):02d}' if s.isdigit() else f'app{s}'


def first_sentence(text):
    s = book.sentences(text or '')
    return s[0] if s else ''


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(HERE))
    data = lambda n: json.load(open(os.path.join(root, 'data', n), encoding='utf-8'))
    pins, items, regions, matches = data('pins.json'), data('items-paper-2013.json')['items'], \
        data('regions-paper-2013.json'), data('matches-paper-2013.json')['items']
    pdf = pins['pdf-paper-2013']
    if regions['pdf']['sha256'] != pdf['sha256'] or regions['pdf']['pages'] != pdf['physical_page_count']:
        sys.exit('regions-paper-2013.json is of another PDF')
    book_pdf, book_regions = pins['pdf'], data('regions-book.json')
    if book_regions['pdf']['sha256'] != book_pdf['sha256']:
        sys.exit('regions-book.json is of another PDF')
    book_regions = book_regions['items']
    bundle = json.load(open(os.path.join(root, 'book', 'pdf-overlay', 'annotations.bundle.json'), encoding='utf-8'))
    book_records = collections.defaultdict(list)
    for a in bundle['annotations']:
        book_records[a['annotation']['id']].append(a['annotation'])

    defaults = {
        'subject': {
            'type': 'pdf', 'uri': pdf['uri'], 'sha256': pdf['sha256'],
            'citation': pdf['citation'], 'identifiers': pdf['identifiers'],
            'extensions': {NS: {'source_id': pdf['source_id'], 'bytes': pdf['bytes'],
                                'physical_page_count': pdf['physical_page_count']}}},
        'object': {'type': 'lean', 'uri': pins['lean']['uri'], 'version': pins['lean']['commit']},
    }

    def lean_end(o):
        """A book record's Lean end, written whole where it is not of the repository at the pin."""
        o = json.loads(json.dumps(o))
        if o.get('uri') == pins['lean']['uri'] and o.get('version') == pins['lean']['commit']:
            o.pop('type', None), o.pop('uri', None), o.pop('version', None)
        return o

    display_files, steps = book.proof_overlay(root, 'paper-2013', pdf, pins['lean'], pins['mathlib'], folder_of)
    out_dir = os.path.join(root, 'paper-2013', 'annotations')
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    counts = collections.Counter()
    files = {}
    for it in items:
        regs = regions['items'][it['id']]
        m = matches[it['id']]
        subject = [{'location': {'page': r['page'], 'rect': r['rect']}, 'title': title_of(it),
                    'extensions': {NS: {'region': f"{it['id']}#{n}" if len(regs) > 1 else it['id']}}}
                   for n, r in enumerate(regs)]
        pages = sorted({r['page'] for r in regs})
        prov = {'actor': 'agent', 'method': m['method'], 'confirmed_by_human': False}
        common = {'locator': {'physical': pages, 'printed': [p - pdf['printed_page_offset'] for p in pages]},
                  'provenance': prov}
        base = {'id': it['id'], 'kind': it['kind']}
        records = []
        if not m['book']:
            records.append(dict(base, subject=subject, object=[], note='No counterpart in [H].',
                                extensions={NS: dict(common)}))
            counts['no_counterpart'] += 1
        else:
            ref, same = book_ref(m['book']), m['verdict'] == 'same'
            counts['same' if same else 'changed'] += 1
            for br in book_records[m['book']]:
                rel, status, obj = br.get('relation'), br.get('status'), br['object']
                if same:
                    note = f'As {ref}, up to notation.'
                    rest = book.terse(first_sentence(br.get('note')), keep_errors=False)
                    if rest:
                        note += ' ' + rest
                elif rel == 'noMatch':
                    # the absence was searched for the book's statement, not this one
                    rel, obj = None, []
                    note = f"{ref} changed it ({m['change']}); [H]'s version is not formalized at the pin."
                else:
                    if rel is not None:
                        rel = 'relatedMatch'
                    status = CHANGED_STATUS.get(status, status)
                    note = f"{ref} changed it ({m['change']}), so the link is at most related."
                r = dict(base)
                if status:
                    r['status'] = status
                if rel:
                    r['relation'] = rel
                r.update(subject=subject, object=[lean_end(o) for o in obj], note=note,
                         extensions={NS: dict(common)})
                records.append(r)
            # the book's item itself, on the book's PDF: a link of its own (Literature Links takes the
            # ends of one side jointly).  The end carries no overlay extension, so the viewer's card
            # links the book's PDF.
            book_end = [{'type': 'pdf', 'uri': book_pdf['uri'], 'sha256': book_pdf['sha256'],
                         'location': {'page': r['page'], 'rect': r['rect']}, 'title': f'{ref}', 'role': 'support'}
                        for r in book_regions[m['book']]]
            records.append(dict(base, relation='exactMatch' if same else 'relatedMatch', subject=subject,
                                object=book_end,
                                note=f'Counterpart in {ref}, the same statement up to notation.' if same
                                else f"Counterpart in {ref}, changed: {m['change']}.",
                                extensions={NS: dict(common)}))
            counts['book_links'] += 1
        # formalized needs a key declaration among the item's links, as in the book's producer
        # (formal-companion docs/overlay.md section 7)
        if any(r.get('status') == 'formalized' for r in records) and not any(
                o.get('role') == 'key' for r in records for o in r['object']):
            for r in records:
                if r.get('status') == 'formalized':
                    r['status'] = 'partial'
            counts['formalized_without_key_to_partial'] += 1
        # file names, as the book's producer names them
        def key_of(r, in_item):
            if r.get('relation') == 'noMatch':
                return 'noMatch' if in_item else f"{it['id']}__noMatch"
            if not r['object']:
                return 'unlinked' if in_item else it['id']
            o = r['object'][0]
            if o.get('type') == 'pdf':
                return f"{o['role']}__H" if in_item else f"{it['id']}__{o['role']}__H"
            rest = f"{o['role']}__{o['location']['declaration']}"
            return rest if in_item else f"{it['id']}__{rest}"
        records.sort(key=lambda r: (r.get('relation') != 'noMatch',
                                    ROLES.index(r['object'][0]['role']) if r['object'] and 'role' in r['object'][0] else -1,
                                    r['object'][0]['location'].get('declaration', '')
                                    if r['object'] and 'location' in r['object'][0] else ''))
        folder = folder_of(it)
        if len(records) == 1 and it['id'] not in steps:
            paths = [f"{folder}/{file_name(key_of(records[0], False), '.json')}"]
        else:  # an item with several records, or with a proof: a folder
            keys = [key_of(r, True) for r in records]
            names = [file_name(k, '.json') for k in keys]
            clash = collections.Counter(n.lower() for n in names)
            names = [file_name(k, '.json', force_hash=clash[n.lower()] > 1) for k, n in zip(keys, names)]
            if len({n.lower() for n in names}) != len(names):
                sys.exit(f"{it['id']}: two records share a file name")
            paths = [f"{folder}/{file_name(it['id'])}/{n}" for n in names]
        proof = book.step_files(f"{folder}/{file_name(it['id'])}", steps.pop(it['id'], []))
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
