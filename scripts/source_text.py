"""Restore the source text of each proof step and display from the arXiv e-print.

The data files leave out the text of the book (arXiv:1501.05438v2) and the 2013 paper
(arXiv:1312.7748v2), which arXiv distributes under its non-exclusive licence. Each record locates
its passage by `file`, `start` and `end` (character offsets in the e-print's source, end
exclusive). `latex_chars` and `latex_sha256` describe the text. This script cuts the text again,
as scripts/steps/segment.py did, and checks it against both.

    python3 scripts/source_text.py <e-print dir> data/book-steps.json data/book-displays.json
    python3 scripts/source_text.py <e-print dir> data/paper-2013-steps.json --write <out dir>

<e-print dir> holds the unpacked e-print (`arxiv.org/e-print/1501.05438v2`, or `1312.7748v2`).
With `--write`, a copy of each file with `latex` restored goes to <out dir>; the region tools
read those copies. Exits 1 if any passage differs.
"""
import hashlib, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps'))
from segment import Source  # noqa: E402


def main(argv):
    out_dir = None
    if '--write' in argv:
        i = argv.index('--write')
        out_dir = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    src_dir, paths = argv[0], argv[1:]
    sources, bad, total = {}, 0, 0
    for path in paths:
        d = json.load(open(path, encoding='utf-8'))
        for key, recs in d.items():
            if not isinstance(recs, list):
                continue
            for r in recs:
                if not isinstance(r, dict) or 'latex_sha256' not in r:
                    continue
                name = r['file']
                if name not in sources:
                    raw = open(os.path.join(src_dir, name), encoding='ascii').read()
                    sources[name] = Source(name[:-4] if name.endswith('.tex') else name, raw)
                text = sources[name].text(r['start'], r['end'])
                total += 1
                if (hashlib.sha256(text.encode('utf-8')).hexdigest() != r['latex_sha256']
                        or len(' '.join(text.split())) != r['latex_chars']):
                    bad += 1
                    print(f'differs: {path} {r.get("id")}', file=sys.stderr)
                if out_dir:
                    r['latex'] = text
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            json.dump(d, open(os.path.join(out_dir, os.path.basename(path)), 'w', encoding='utf-8'),
                      indent=1, ensure_ascii=False)
    print(f'{total - bad} of {total} passages restored exactly')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
