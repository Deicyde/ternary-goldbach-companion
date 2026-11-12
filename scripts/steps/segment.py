"""Segment the LaTeX of [H] (arXiv:1501.05438v2) or of arXiv:1312.7748v2 into displays and proof steps.

New code.  Deterministic: a scan of the arXiv source, with comments masked.

- Displays: every `\\[...\\]`, `$$...$$` and `equation` environment.  An unnumbered one outside
  every `proof` environment is a display item, `<section> display <n>`, numbered in order within
  its section (the section of the overlay's item list: `x.y` in the book, the top-level section in
  the paper).
- Proofs: the `proof` environments (the sources have no other proof markup: a `Proof` heading
  appears only as the optional argument of one `proof`).  A proof proves the theorem-like
  environment named by its optional argument's `\\ref`, else the nearest one before it.
- Steps of a proof, in order: each unnumbered display; each run of prose between two separators
  (a display, numbered or not; a paragraph break, i.e. a blank line or `\\par`; `\\item`; the begin
  or end of a list).  A run with no letter or digit (punctuation after a display, a `\\label`) is
  not a step.  A numbered display is its own item and is no step.  Footnotes stay inside their
  run.  A run that the splits file (`<overlay>-splits.json`) cuts at sentence boundaries becomes
  one step per piece.

Usage: python3 -I segment.py book|paper-2013 <source dir> <items json> <out dir> [<splits json>]
Writes <out dir>/<overlay>-displays.json and <out dir>/<overlay>-steps.json; offsets are
character offsets in the arXiv source file, end exclusive; lines are 1-based.
"""
import collections
import json
import os
import re
import sys

THM_ENVS = {'book': ('theorem', 'lemma', 'prop', 'corollary'),
            'paper-2013': ('thm', 'lem', 'prop', 'cor', 'main')}
LIST_ENVS = ('enumerate', 'itemize', 'description')
BOOK_FILES = ['introductionp', 'notprem', 'intromin', 'typeI', 'typeII', 'minarctotals', 'intromaj',
              'mellintran', 'expform', 'intmajarc', 'optcoor', 'l2normls', 'intminarc', 'conclusion',
              'normsapp', 'normfour', 'sumlaphi', 'othcheck']
APPENDIX_FROM = {'book': 'normsapp', 'paper-2013': None}
# a sentence ends at . ? or ! followed by space and a capital, a `$`, a `\\` command or `(`; not after
# these abbreviations
ABBREV = ('Lem', 'Lemma', 'Prop', 'Thm', 'Cor', 'Sec', 'Ch', 'Chap', 'cf', 'e.g', 'i.e', 'resp', 'Eq', 'eq',
          'etc', 'vs', 'Fig', 'Thms', 'Lems', 'Props', 'Secs', 'pp', 'p', 'no', 'Mr', 'Dr', 'St', 'al',
          'approx', 'Cors', 'Ex', 'Rem', 'Def', 'Prob', 'Conj', 'ff')


def mask_comments(raw):
    """The text with every comment (from an unescaped % to the end of its line) replaced by spaces."""
    out = list(raw)
    i, n = 0, len(raw)
    while i < n:
        c = raw[i]
        if c == '\\':
            i += 2
            continue
        if c == '%':
            j = raw.find('\n', i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = ' '
            i = j
            continue
        i += 1
    return ''.join(out)


def blank_lines(raw):
    """Offsets of paragraph breaks: lines that are empty or white in the raw text (a line that holds
    only a comment is no break)."""
    out, pos = [], 0
    for line in raw.split('\n'):
        if not line.strip():
            out.append((pos, pos + len(line)))
        pos += len(line) + 1
    return out


def brace_end(t, i):
    """t[i] == '{': the offset after its matching '}'."""
    depth = 0
    while i < len(t):
        c = t[i]
        if c == '\\':
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError('unbalanced braces')


def scan(t):
    """Tokens of the masked text: (kind, start, end, arg).  Kinds: begin, end (arg the environment),
    dopen/dclose (`\\[`, `\\]`, `$$`), par (`\\par`), item, section (arg (level, starred)), appendix,
    footnote (start, end of the whole `\\footnote{...}`)."""
    toks, i, n, inline = [], 0, len(t), False
    while i < n:
        c = t[i]
        if c == '\\':
            m = re.match(r'\\([A-Za-z]+|.)', t[i:])
            name = m.group(1)
            j = i + len(m.group(0))
            if name in ('begin', 'end'):
                mm = re.match(r'\s*\{([^}]*)\}', t[j:])
                toks.append((name, i, j + len(mm.group(0)), mm.group(1)))
                j += len(mm.group(0))
            elif name == '[':
                toks.append(('dopen', i, j, '\\['))
            elif name == ']':
                toks.append(('dclose', i, j, '\\]'))
            elif name == '(':
                inline = True
            elif name == ')':
                inline = False
            elif name == 'par':
                toks.append(('par', i, j, None))
            elif name == 'item':
                mm = re.match(r'\s*\[[^\]]*\]', t[j:])
                if mm:
                    j += len(mm.group(0))
                toks.append(('item', i, j, None))
            elif name in ('chapter', 'section', 'subsection', 'part'):
                star = t[j:j + 1] == '*'
                toks.append(('section', i, j, (name, star)))
            elif name == 'appendix':
                toks.append(('appendix', i, j, None))
            elif name == 'footnote':
                k = j
                while t[k].isspace():
                    k += 1
                e = brace_end(t, k)
                toks.append(('footnote', i, e, None))
            i = j
            continue
        if c == '$':
            if t[i:i + 2] == '$$' and not inline:
                toks.append(('dollars', i, i + 2, '$$'))
                i += 2
                continue
            inline = not inline
        i += 1
    return toks


class Source:
    def __init__(self, name, raw):
        self.name, self.raw = name, raw
        self.t = mask_comments(raw)
        self.line_starts = [0] + [m.end() for m in re.finditer('\n', raw)]
        self.toks = scan(self.t)

    def line(self, off):
        lo, hi = 0, len(self.line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.line_starts[mid] <= off:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    def text(self, s, e):
        """The source between s and e with comments removed (a comment-only line is dropped)."""
        lines = []
        raw_lines, clean_lines = self.raw[s:e].split('\n'), self.t[s:e].split('\n')
        for r, c in zip(raw_lines, clean_lines):
            if not c.strip() and r.strip():
                continue
            lines.append(c.rstrip())
        return '\n'.join(lines).strip()


def displays_of(src):
    """[(start, end, delim, numbered)] of every display, in order; also the spans of footnotes."""
    out, stack, foot = [], None, []
    for kind, s, e, arg in src.toks:
        if kind == 'footnote':
            foot.append((s, e))
        if stack is None:
            if kind == 'dopen':
                stack = ('\\[', s)
            elif kind == 'dollars':
                stack = ('$$', s)
            elif kind == 'begin' and arg in ('equation', 'equation*'):
                stack = (arg, s)
        else:
            d, s0 = stack
            if (d == '\\[' and kind == 'dclose') or (d == '$$' and kind == 'dollars') or \
               (kind == 'end' and arg == d):
                out.append((s0, e, d, d == 'equation'))
                stack = None
    if stack is not None:
        sys.exit(f'{src.name}: unclosed display at line {src.line(stack[1])}')
    return out, foot


def env_spans(src, names):
    """[(name, begin start, begin end, end start, end end, optional argument)] of the environments named."""
    out, open_ = [], []
    for kind, s, e, arg in src.toks:
        if kind == 'begin' and arg in names:
            opt = re.match(r'\s*\[([^\]]*)\]', src.t[e:])
            open_.append((arg, s, e + (len(opt.group(0)) if opt else 0), opt.group(1) if opt else None))
        elif kind == 'end' and arg in names:
            name, s0, e0, opt = open_.pop()
            if name != arg:
                sys.exit(f'{src.name}: {name} closed by {arg} at line {src.line(s)}')
            out.append((name, s0, e0, s, e, opt))
    return sorted(out, key=lambda x: x[1])


class Sections:
    """The section number at each offset, from the \\chapter/\\section commands in reading order."""

    def __init__(self, overlay, sources):
        self.marks = []  # (file index, offset, chapter, section)
        chap, sec, appendix = 0, 0, False
        letters = 'ABCDEFGHIJ'
        for fi, src in enumerate(sources):
            if APPENDIX_FROM[overlay] == src.name:
                appendix, chap = True, 0
            for kind, s, e, arg in src.toks:
                if kind == 'appendix' and overlay == 'paper-2013':
                    appendix, sec = True, 0
                if kind != 'section' or arg[1]:
                    continue
                level = arg[0]
                if overlay == 'book':
                    if level == 'chapter':
                        chap += 1
                        sec = 0
                        c = letters[chap - 1] if appendix else str(chap)
                        self.marks.append((fi, s, c, c))
                    elif level == 'section':
                        sec += 1
                        c = letters[chap - 1] if appendix else str(chap)
                        self.marks.append((fi, s, c, f'{c}.{sec}'))
                else:
                    if level == 'section':
                        sec += 1
                        c = letters[sec - 1] if appendix else str(sec)
                        self.marks.append((fi, s, c, c))

    def at(self, fi, off):
        cur = (None, None)
        for f, s, c, sec in self.marks:
            if (f, s) <= (fi, off):
                cur = (c, sec)
        return cur


def content(text):
    """Whether a run of prose holds a letter or digit once labels and spacing commands are dropped."""
    t = re.sub(r'\\label\{[^}]*\}', '', text)
    t = re.sub(r'\\(noindent|indent|medskip|smallskip|bigskip|hfill|qedhere|newline|vfill|quad|qquad|,|;|!)', '', t)
    t = re.sub(r'\\vspace\*?\{[^}]*\}', '', t)
    return re.search(r'[A-Za-z0-9]', t) is not None


LEAD = re.compile(r'(\s|\\noindent\b|\\indent\b|\\label\{[^}]*\}|\\medskip\b|\\smallskip\b|\\bigskip\b|\\vspace\*?\{[^}]*\})+')


def trim(src, s, e):
    """The run's start after white space and leading spacing commands (where a start marker can go:
    after `\\noindent`, which must come first), and its end after its last non-space character."""
    t = src.t
    while True:
        m = LEAD.match(t, s, e)
        if not m or m.end() == s:
            break
        s = m.end()
    while e > s and t[e - 1].isspace():
        e -= 1
    return s, e


def sentence_cuts(src, s, e, foot):
    """Offsets inside [s, e) where a sentence ends (after its final punctuation), outside math and
    footnotes.  Each cut c: the sentence before ends at c, the next starts after the spaces at c."""
    t, cuts, i, inline, depth = src.t, [], s, False, 0
    while i < e:
        c = t[i]
        if any(a <= i < b for a, b in foot):
            i = next(b for a, b in foot if a <= i < b)
            continue
        if c == '\\':
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        elif c == '$':
            inline = not inline
        elif c in '.?!' and not inline and depth == 0:
            j = i + 1
            while j < e and t[j] in ')\'"}':
                j += 1
            if j < e and t[j].isspace():
                k = j
                while k < e and t[k].isspace():
                    k += 1
                nxt = t[k:k + 1]
                word = re.search(r'([A-Za-z.]+)$', t[max(s, i - 12):i])
                w = word.group(1) if word else ''
                if k < e and (nxt.isupper() or nxt in '$(\\') and w not in ABBREV and not re.fullmatch(r'[A-Z]', w) \
                        and not (nxt == '\\' and re.match(r'\\(ref|eqref|cite)\b', t[k:])):
                    cuts.append(j)
        i += 1
    return cuts


def main():
    overlay, srcdir, items_path, outdir = sys.argv[1:5]
    splits = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else {}
    names = BOOK_FILES if overlay == 'book' else ['ternvin']
    sources = [Source(n, open(os.path.join(srcdir, n + '.tex'), encoding='ascii').read()) for n in names]
    items = json.load(open(items_path))['items']

    def item_file_line(it):
        if 'tex' in it:
            return it['tex']['file'][:-4], it['tex']['line']
        return it['chapter_file'], it['line']
    item_at = {item_file_line(it): it for it in items}
    by_label = {it['label']: it for it in items if it.get('label')}
    secs = Sections(overlay, sources)

    displays, steps, proofs, stats = [], [], [], collections.Counter()
    disp_n = collections.Counter()
    outside = {}
    for fi, src in enumerate(sources):
        disps, foot = displays_of(src)
        prf = env_spans(src, ('proof',))
        thms = env_spans(src, THM_ENVS[overlay])
        stats['displays_all'] += len(disps)
        in_foot = lambda off: any(a <= off < b for a, b in foot)
        for k, (s, e, d, numbered) in enumerate(disps):
            pr = next((p for p in prf if p[1] <= s < p[4]), None)
            chap, sec = secs.at(fi, s)
            rec = dict(file=src.name + '.tex', line=src.line(s), end_line=src.line(e - 1), start=s, end=e,
                       file_display=k + 1, delim=d, chapter=chap, section=sec)
            if numbered:
                continue
            if in_foot(s):
                rec['in_footnote'] = True
            if pr is None:
                disp_n[sec] += 1
                rec.update(id=f'{sec} display {disp_n[sec]}', kind='display', latex=src.text(s, e))
                thm = next((x for x in thms if x[1] <= s < x[4]), None)
                if thm:
                    it = item_at.get((src.name, src.line(thm[1])))
                    rec['inside_item'] = it['id'] if it else f'unnumbered {thm[0]}'
                displays.append(rec)
        # prose outside proofs (out of scope): runs between any two separators, outside proofs and
        # theorem-like statements, after \begin{document}
        doc0 = src.t.find('\\begin{document}')
        doc0 = doc0 + 16 if doc0 >= 0 else 0
        cuts = sorted([(s, e) for s, e, d, nb in disps] + [(a, b) for a, b in blank_lines(src.raw)] +
                      [(s, e) for kind, s, e, arg in src.toks if kind in ('par', 'item', 'begin', 'end', 'section')])
        cur = doc0
        for s, e in cuts + [(len(src.t), len(src.t))]:
            if s > cur:
                a, b = trim(src, cur, s)
                if a < b and content(src.t[a:b]) and not any(x[1] <= a < x[4] for x in prf + thms) \
                        and not in_foot(a) and '\\end{document}' not in src.t[doc0:a]:
                    sec = secs.at(fi, a)[1]
                    outside[sec or '-'] = outside.get(sec or '-', [0, 0])
                    outside[sec or '-'][0] += 1
                    outside[sec or '-'][1] += len(re.findall(r'[A-Za-z]{2,}', re.sub(r'\$[^$]*\$|\\[A-Za-z]+', ' ', src.t[a:b])))
            cur = max(cur, e)
        for name, bs, be, es, ee, opt in prf:
            # the item the proof proves
            it, how = None, None
            if opt:
                m = re.search(r'\\ref\{([^}]*)\}', opt)
                it = by_label.get(m.group(1)) if m else None
                how = 'optional argument'
            if it is None:
                before = [x for x in thms if x[4] <= bs]
                if not before:
                    sys.exit(f'{src.name}:{src.line(bs)}: proof with no theorem before it')
                x = before[-1]
                it = item_at.get((src.name, src.line(x[1])))
                how = 'preceding environment'
                if it is None:
                    it = dict(id='Main Theorem' if x[0] == 'main' else f'unnumbered {x[0]}', unnumbered=True)
                gap = src.t[x[4]:bs]
            pid = it['id']
            proofs.append(dict(item=pid, item_in_overlay=not it.get('unnumbered'), found_by=how,
                               file=src.name + '.tex', line=src.line(bs), end_line=src.line(ee - 1),
                               section=secs.at(fi, bs)[1], chapter=secs.at(fi, bs)[0]))
            # separators inside the proof body (not inside a footnote)
            seps = []
            for s, e, d, numbered in disps:
                if be <= s < es and not in_foot(s):
                    seps.append((s, e, 'display', numbered, d))
            for a, b in blank_lines(src.raw[be:es]):
                seps.append((be + a, be + b, 'par', None, None))
            for kind, s, e, arg in src.toks:
                if be <= s < es and not in_foot(s) and (kind in ('par', 'item') or
                                                         (kind in ('begin', 'end') and arg in LIST_ENVS)):
                    seps.append((s, e, kind, None, None))
            seps.sort()
            # drop separators inside displays (a blank line in a display does not occur, but be safe)
            clean, last = [], be
            for sp in seps:
                if sp[0] < last:
                    continue
                clean.append(sp)
                last = sp[1]
            psteps, cur = [], be
            for sp in clean + [(es, es, 'end', None, None)]:
                s, e = trim(src, cur, sp[0])
                if s < e:
                    if content(src.t[s:e]):
                        psteps.append(dict(kind='prose', start=s, end=e))
                    else:
                        stats['runs_without_words'] += 1
                if sp[2] == 'display' and not sp[3]:
                    psteps.append(dict(kind='display', start=sp[0], end=sp[1], delim=sp[4]))
                if sp[2] == 'display' and sp[3]:
                    stats['numbered_displays_in_proofs'] += 1
                cur = sp[1]
            # sentence splits of long runs
            out = []
            for st in psteps:
                key_ = f"{src.name}.tex:{st['start']}"
                if st['kind'] == 'prose' and key_ in splits:
                    cuts = sentence_cuts(src, st['start'], st['end'], foot)
                    groups = splits[key_]['groups']   # sentence counts per piece
                    if sum(groups) != len(cuts) + 1:
                        sys.exit(f'{key_}: split groups {groups} do not cover {len(cuts) + 1} sentences')
                    bounds, k = [], 0
                    for g in groups[:-1]:
                        k += g
                        bounds.append(cuts[k - 1])
                    a = st['start']
                    for b in bounds + [st['end']]:
                        s2, e2 = trim(src, a, b)
                        out.append(dict(kind='prose', start=s2, end=e2, split_from=key_))
                        a = b
                else:
                    out.append(st)
            for n, st in enumerate(out, 1):
                chap, sec = secs.at(fi, st['start'])
                rec = dict(proof_item=pid, step=n, id=f'{pid} step {n}', kind=st['kind'],
                           latex=src.text(st['start'], st['end']), file=src.name + '.tex',
                           line=src.line(st['start']), end_line=src.line(st['end'] - 1),
                           start=st['start'], end=st['end'], chapter=chap, section=sec,
                           proof_line=src.line(bs))
                if st['kind'] == 'display':
                    rec['delim'] = st['delim']
                    rec['file_display'] = next(k + 1 for k, d in enumerate(disps) if d[0] == st['start'])
                if st.get('split_from'):
                    rec['split_from'] = st['split_from']
                if st['kind'] == 'prose':
                    rec['sentences'] = len(sentence_cuts(src, st['start'], st['end'], foot)) + 1
                    if any(st['start'] <= a < st['end'] for a, b in foot):
                        rec['footnote'] = True
                steps.append(rec)
    # a proof item proved twice gets its steps numbered on
    seen = collections.Counter()
    for p in proofs:
        seen[p['item']] += 1
    dup = {k for k, v in seen.items() if v > 1}
    if dup:
        cnt = collections.Counter()
        for st in steps:
            if st['proof_item'] in dup:
                cnt[st['proof_item']] += 1
                st['step'] = cnt[st['proof_item']]
                st['id'] = f"{st['proof_item']} step {st['step']}"
    src_note = dict(book='arXiv:1501.05438v2 e-print, files in \\include order of 3nonpupbook.tex',
                    **{'paper-2013': 'arXiv:1312.7748v2 e-print, ternvin.tex'})[overlay]
    meta = dict(overlay=overlay, source=src_note,
                offsets='start/end: character offsets in the arXiv source file (end exclusive); line/end_line 1-based',
                latex='the source between start and end with comments removed')
    json.dump(dict(meta, displays=displays), open(os.path.join(outdir, f'{overlay}-displays.json'), 'w'),
              indent=1, ensure_ascii=False)
    json.dump(dict(meta, proofs=proofs, steps=steps,
                   counts=dict(stats, proofs=len(proofs), steps=len(steps), displays=len(displays)),
                   prose_outside_proofs=dict(
                       note='out of scope: runs of prose (between displays, paragraph breaks, list items and environment '
                            'boundaries) outside proofs and theorem-like statements; words: runs of two or more letters, '
                            'math dropped',
                       by_section={k: dict(runs=v[0], words=v[1]) for k, v in outside.items()},
                       runs=sum(v[0] for v in outside.values()), words=sum(v[1] for v in outside.values()))),
              open(os.path.join(outdir, f'{overlay}-steps.json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(dict(stats, proofs=len(proofs), steps=len(steps), displays=len(displays),
                          duplicate_proof_items=sorted(dup))))


if __name__ == '__main__':
    main()
