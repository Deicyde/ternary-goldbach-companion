"""Regions of the displays and proof steps of [H] (arXiv:1501.05438v2) or arXiv:1312.7748v2 on the arXiv PDF.

New code.  Pipeline:

1. `build_steps.sh` recompiles the arXiv source with `regionmarks.tex` and `stepmarks.tex`, and
   with `\\rmS{n}`/`\\rmE{n}` around every prose step (`insert_marks.py`).  `layout_check.py` shows
   that this build has the word boxes of the regionmarks.tex build, to 0.01 pt.
2. On the rebuilt PDF: a display spans the text width, from below the line before it (marker
   `ds:k:pre`, or the display above, or the top of the text block) to its last ink (marker
   `disp:k:post`), cut to its words.  A prose step runs from its start marker to its end marker:
   the words of the text block after the start (on the start's line, right of it) and before the
   end (on the end's line, left of it), less footnotes.  Its region on a page is one rectangle, or,
   where a line is shared with the step before or after (a paragraph cut between sentences), up to
   three quads: the rest of the first line, the full lines, the start of the last line.
3. Each line of a step, and each display, is carried to the arXiv PDF: the arXiv word boxes at the
   same x (to 1 pt) and the same width vote for its displacement; the line moves by the displacement
   that most of its words share (at least 60%; `method: marker` when every line is in place, to
   1 pt, else `shift`).  Where that fails (the line breaks differ) the step's words are found in
   order among the arXiv words (`method: words`).
4. Checks on the arXiv PDF (`pdftotext -x -y -W -H` crops): a display's crop holds its distinctive
   tokens (numbers of two or more digits, words in `\\text`, operator names); a step's crop holds
   its first and last words (math dropped, letters compared); no word of a step lies in another
   step's region; regions of steps of one proof do not overlap.

Usage: python3 -I steps.py <build dir> <arXiv PDF> <displays json> <steps json> <items' regions json> <out json> <main> <arXiv id> <printed page offset>
"""
import collections
import difflib
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regions import bbox_words, read_aux, Layout, key  # noqa: E402

PAD = 2.0
XPAD = 1.5


def read_step_aux(build, main):
    displine, dsafter, noend = {}, set(), set()
    for f in glob.glob(os.path.join(build, '*.aux')):
        s = open(f, encoding='latin-1').read()
        for k, fn, ln in re.findall(r'\\rmdispline\{(\d+)\}\{([^}]*)\}\{(\d+)\}', s):
            displine[int(k)] = (fn or main + '.tex', int(ln))
        dsafter |= {int(k) for k in re.findall(r'\\rmdsafter\{(\d+)\}', s)}
        noend |= {int(k) for k in re.findall(r'\\rmnoend\{(\d+)\}', s)}
    return displine, dsafter, noend


def cy(w):
    return (w[2] + w[4]) / 2


class Page:
    """The rebuilt page's words in the text block, without footnotes."""

    def __init__(self, pg, mine, marks, L):
        self.pg = pg
        fn = [L.y(m) for n, m in marks.items() if n.startswith('fn:') and m[0] == pg]
        self.fn_top = min(fn) - 0.75 * L.bskip - 2 if fn else None
        left = L.left(pg)
        self.words = [w for w in mine[pg - 1][2] if left - 30 < w[1] and w[3] < left + L.width + 30
                      and L.top - 4 < cy(w) < L.bottom + 4 and (self.fn_top is None or cy(w) < self.fn_top)]


def lines_of(ws, L):
    """Group words into lines: the baselines of text-size words, each word to the nearest one."""
    if not ws:
        return []
    fs = L.fontsize
    anchors = sorted(w[4] - 0.216 * fs for w in ws if 0.8 * fs <= w[4] - w[2] <= 1.05 * fs)
    base = []
    for b in anchors:
        if base and b - base[-1][0] < 0.5 * L.bskip:
            base[-1].append(b)
        else:
            base.append([b])
    base = [sum(b) / len(b) for b in base]
    if not base:
        base = [max(w[4] for w in ws)]
    out = collections.defaultdict(list)
    for w in ws:
        b = min(base, key=lambda b: abs(cy(w) - (b - 0.23 * fs)))
        out[b].append(w)
    return [sorted(out[b], key=lambda w: w[1]) for b in sorted(out)]


def carry_block(ws, pg, arx, L, max_d=80):
    """Candidate displacements [(votes, page, dy)] of a block of words of rebuilt page pg on the arXiv
    PDF, best first: the arXiv word boxes at the same x and width vote, a box with the same letters
    counting twice; a candidate needs at least 60% of the words to agree (to 1 pt)."""
    votes = collections.Counter()
    for w in ws:
        seen = set()
        for p2 in (pg - 1, pg, pg + 1):
            if not 1 <= p2 <= len(arx):
                continue
            off = (p2 - pg) * L.H
            for v in arx[p2 - 1][2]:
                if abs(v[1] - w[1]) <= 1 and abs((v[3] - v[1]) - (w[3] - w[1])) <= 1.5:
                    d = v[2] + off - w[2]
                    if abs(d) <= max_d + (L.H if p2 != pg else 0):
                        r = round(d * 2) / 2
                        if (p2, r) not in seen:
                            seen.add((p2, r))
                            votes[(p2, r)] += 1 + (key(v) == key(w) and key(w) != '')
    out, done = [], set()
    for (p2, r), _ in votes.most_common(20):
        if any(q == p2 and abs(s - r) <= 1 for q, s in done):
            continue
        done.add((p2, r))
        off = (p2 - pg) * L.H
        ds = [v[2] + off - w[2] for w in ws for v in arx[p2 - 1][2]
              if abs(v[1] - w[1]) <= 1 and abs(v[2] + off - w[2] - r) <= 1]
        agree = sum(1 for w in ws if any(abs(v[1] - w[1]) <= 1 and abs(v[2] + off - w[2] - r) <= 1
                                         for v in arx[p2 - 1][2]))
        if agree < 0.6 * len(ws):
            continue
        n = sum(c for (q, s), c in votes.items() if q == p2 and abs(s - r) <= 1)
        ds.sort()
        out.append((n, p2, ds[len(ds) // 2] - off))
    out.sort(key=lambda c: -c[0])
    return out


class Carrier:
    """Displacements of blocks on the arXiv PDF.  A block whose best candidate has no close rival
    (90% of its votes) is placed at once; the others take, of their close candidates, the one
    nearest the displacement of the nearest placed block on the same rebuilt page."""

    def __init__(self, arx, L):
        self.arx, self.L, self.anchors = arx, L, collections.defaultdict(list)

    def first(self, ws, pg):
        c = carry_block(ws, pg, self.arx, self.L)
        if not c:
            return None
        close = [x for x in c if x[0] >= 0.9 * c[0][0]]
        if len(close) == 1:
            self.anchors[pg].append((sum(cy(w) for w in ws) / len(ws), c[0][1], c[0][2]))
            return (c[0][1], c[0][2])
        return close

    def resolve(self, ws, pg, close):
        y = sum(cy(w) for w in ws) / len(ws)
        a = sorted(self.anchors[pg], key=lambda t: abs(t[0] - y))
        ref = (a[0][1] - pg) * self.L.H + a[0][2] if a else 0.0
        best = min(close, key=lambda x: abs((x[1] - pg) * self.L.H + x[2] - ref))
        return (best[1], best[2])


def crop(pdf, page, r, size):
    W, H = size
    x0, y0, x1, y1 = r
    return subprocess.run(['pdftotext', '-f', str(page), '-l', str(page), '-x', str(int(x0)), '-y', str(int(y0)),
                           '-W', str(int(x1 - x0 + 1)), '-H', str(int(y1 - y0 + 1)), pdf, '-'],
                          capture_output=True, text=True).stdout


def norm(t):
    t = unicodedata.normalize('NFKD', unicodedata.normalize('NFKC', t))
    t = re.sub(r'-\s*\n\s*', '', t)
    return re.sub(r'[^a-z0-9]', '', t.lower())


def strip_tex(latex):
    """Text of a prose step for its first and last words: math, references, citations, labels and
    footnotes dropped; accents folded."""
    t = latex
    t = re.sub(r'\\footnote\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}', ' ', t)
    t = re.sub(r'\$\$.*?\$\$|\$[^$]*\$|\\\(.*?\\\)', ' MATH ', t, flags=re.S)
    t = re.sub(r'\\(label|ref|eqref|cite|pageref)(\[[^\]]*\])?\{[^}]*\}', ' REF ', t)
    t = re.sub(r'\\[\'"`^~=.]\{?([A-Za-z])\}?', r'\1', t)
    t = re.sub(r'\\(textbf|textit|emph|textrm|mathrm|text|mbox)\{', ' ', t)
    t = re.sub(r'\\[A-Za-z]+\*?', ' ', t)
    t = t.replace('--', ' ').replace('~', ' ')
    return [w for w in re.findall(r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*', t) if w not in ('MATH', 'REF')]


OPS = ('log', 'exp', 'max', 'min', 'sup', 'inf', 'lim', 'sin', 'cos', 'arg', 'deg', 'gcd')


def distinctive(latex):
    t = re.sub(r'\\(label|ref|eqref|cite)(\[[^\]]*\])?\{[^}]*\}', ' ', latex)
    toks = re.findall(r'\d+(?:\.\d+)?', t)
    toks = [x for x in toks if len(x.replace('.', '')) >= 2]
    for m in re.finditer(r'\\(?:text|mbox|textrm|mathrm|textit)\{([^{}]*)\}', t):
        txt = re.sub(r'\$[^$]*\$|\\[A-Za-z]+', ' ', m.group(1))
        toks += [w for w in re.findall(r'[A-Za-z]{3,}', txt)]
    toks += [o for o in OPS if re.search(r'\\' + o + r'(?![A-Za-z])', t)]
    return sorted(set(toks))


def rect_of(quads):
    return [min(q[0] for q in quads), min(q[1] for q in quads), max(q[2] for q in quads), max(q[3] for q in quads)]


def inter(a, b, eps=0.3):
    return a[0] < b[2] - eps and b[0] < a[2] - eps and a[1] < b[3] - eps and b[1] < a[3] - eps


def main():
    build, pdf, disp_path, steps_path, items_regions, out_path, main_file, identifier, offset = sys.argv[1:10]
    offset = int(offset)
    item_regs = json.load(open(items_regions))['items']
    D = json.load(open(disp_path))
    S = json.load(open(steps_path))
    marks, enddisp, geo, afterdisp = read_aux(build)
    displine, dsafter, noend = read_step_aux(build, main_file)
    L = Layout(geo)
    L.bskip = geo['baselineskip']
    L.fontsize = round(geo['baselineskip'] / 1.2)
    mine = bbox_words(os.path.join(build, main_file + '.pdf'))
    arx = bbox_words(pdf)
    if len(mine) != len(arx):
        sys.exit('page counts differ')
    pages = {}

    def page(pg):
        if pg not in pages:
            pages[pg] = Page(pg, mine, marks, L)
        return pages[pg]

    missing, notes = {}, collections.defaultdict(list)
    D_by_id = {r['id']: r for r in D['displays']}
    # -- displays: the k of each display, by its order in its file
    by_file = collections.defaultdict(list)
    for k in sorted(displine):
        by_file[displine[k][0]].append(k)
    # the main file of the build has one line more (the \input of the markers) after the preamble
    main_shift = 0
    msrc = open(os.path.join(build, main_file + '.tex'), encoding='ascii').read().split('\n')
    ins_line = next(i + 1 for i, l in enumerate(msrc) if l.startswith('\\input{regionmarks}\\input{stepmarks}'))

    def k_of(rec):
        ks = by_file[rec['file']]
        k = ks[rec['file_display'] - 1]
        ln = displine[k][1]
        if rec['file'] == main_file + '.tex' and ln > ins_line:
            ln -= 1
        if not rec['line'] <= ln <= rec['end_line'] + 1:
            notes[rec['id']].append(f'display counter {k} opens at line {ln}, not {rec["line"]}')
        return k

    def last_word_before(rec):
        """The last word of the source text before a display (comments, blank lines and the step markers
        skipped), letters and digits only, or None when that text ends in a command or a display."""
        lines = open(os.path.join(build, rec['file']), encoding='ascii').read().split('\n')
        k = rec['line'] - 1 + (1 if rec['file'] == main_file + '.tex' and rec['line'] >= ins_line else 0)
        head = lines[k][:lines[k].find('\\[')] if '\\[' in lines[k] else ''
        for t in [head] + [lines[j] for j in range(k - 1, max(k - 40, -1), -1)]:
            t = re.sub(r'\\rm[SE]\{\d+\}', '', re.sub(r'(?<!\\)%.*', '', t)).strip()
            if not t:
                continue
            if t.endswith(('}', '\\]', '$$')) and not t.endswith('$'):
                return None
            m = re.search(r'([A-Za-z0-9]+)[^A-Za-z0-9]*$', t)
            return m.group(1) if m else None
        return None

    all_post = {int(n.split(':')[1]): m for n, m in marks.items() if n.startswith('disp:') and n.endswith(':post')}
    step_marks = [m for n, m in marks.items() if n.startswith('st:')]

    def display_box(rec):
        k = k_of(rec)
        post = all_post.get(k)
        if post is None:
            return None, f'no end marker for display {k}'
        pg = post[0]
        hi = L.y(post) + 0.5
        above = [L.y(m) for kk, m in all_post.items() if m[0] == pg and L.y(m) < hi - 2 and kk != k]
        pre = marks.get(f'ds:{k}:pre')
        floor = None
        if pre and pre[0] == pg:
            lo = max([L.y(pre)] + above)
            floor = L.y(pre) + 1
        elif pre or k in dsafter:
            lo = max(above) if above else L.top - 3
        else:
            # \[ in vertical mode (after a blank line), or $$: below the nearest marker above it on the
            # page, and below where the rebuilt page prints the last word of the source text before it
            near = [L.y(m) for m in step_marks + list(all_post.values()) if m[0] == pg and L.y(m) < hi - 4]
            lo = max(near) + 0.5 if near else L.top - 3
            last = last_word_before(rec)
            hits = [w for w in page(pg).words if last and key(w) == last and lo < cy(w) < hi]
            if hits:
                lo = max(w[4] for w in hits)
                floor = lo + 1
                notes[rec['id']].append(f'top below the last word before it, "{last}"')
            else:
                notes[rec['id']].append('top from the nearest marker above' if near else "top: the text block's top")
        ws = [w for w in page(pg).words if lo < cy(w) < hi and L.left(pg) - 30 < w[1]]
        if not ws:
            return None, 'no words in the display box'
        top = min(w[2] for w in ws)
        if floor is not None:
            top = max(top, floor)
        return (pg, ws, top, max(w[4] for w in ws)), None

    C = Carrier(arx, L)

    def in_place(ws, pg):
        """regions.py's test: 95% of the words have an arXiv word box at the same place (1 pt; 1.5 pt at the right)."""
        there = arx[pg - 1][2]
        same = sum(1 for w in ws if any(abs(w[1] - v[1]) <= 1 and abs(w[2] - v[2]) <= 1 and abs(w[3] - v[3]) <= 1.5
                                        for v in there))
        return same >= 0.95 * len(ws)

    def finish_display(box, c):
        """The arXiv box of a display, from its displacement or, without one, its words in order."""
        pg, ws, top, bot = box
        if isinstance(c, list):
            c = C.resolve(ws, pg, c)
        if c is not None:
            p2, dy = c
            return p2, top + dy, bot + dy, 'marker' if p2 == pg and abs(dy) <= 1 and in_place(ws, pg) else 'shift'
        got = seq_match(ws, pg, pg)
        if got is None or len({p for p, _ in got}) != 1:
            return None
        return got[0][0], min(v[2] for _, v in got), max(v[4] for _, v in got), 'words'

    def seq_match(ws, first, last):
        mw = [w for w in ws if key(w)]
        cand = [(p, v) for p in range(first - 1, last + 2) if 1 <= p <= len(arx) for v in arx[p - 1][2] if key(v)]
        sm = difflib.SequenceMatcher(None, [key(w) for w in mw], [key(c[1]) for c in cand], autojunk=False)
        blocks = [b for b in sm.get_matching_blocks() if b.size >= 3 or (b.size >= 1 and len(mw) <= 4)]
        runs, cur = [], []
        for b in blocks:
            if cur and b.b - (cur[-1].b + cur[-1].size) > max(30, len(mw) // 2):
                runs.append(cur)
                cur = []
            cur.append(b)
        if cur:
            runs.append(cur)
        got = []
        for b in max(runs, key=lambda r: sum(x.size for x in r), default=[]):
            got += cand[b.b:b.b + b.size]
        if not mw or len(got) < 0.8 * len(mw):
            return None
        return got

    # -- prose steps on the rebuilt PDF: per page, the step's words and its lines
    steps = S['steps']
    sm = {}
    for n, st in enumerate(steps):
        if st['kind'] != 'prose':
            continue
        s, e = marks.get(f'st:{n}:s'), marks.get(f'st:{n}:e')
        if s is None or e is None or n in noend:
            missing[st['id']] = 'no start or end marker'
            continue
        sm[n] = (s, e)

    def prose_parts(n):
        """[(page, lines)] of the n-th step on the rebuilt PDF; lines are lists of words.  The first line is
        the words on the start marker's line (from its x on), the last the words on the end marker's line
        (up to its x); the others are grouped by lines_of."""
        (ps, xs, _), (pe, xe, _) = sm[n]
        bs, be = L.y(sm[n][0]), L.y(sm[n][1])
        up, down = 0.75 * L.bskip, 0.25 * L.bskip
        parts = []
        for pg in range(ps, pe + 1):
            head, mid, tail = [], [], []
            for w in page(pg).words:
                c = cy(w)
                on_s = pg == ps and bs - up <= c < bs + down
                on_e = pg == pe and be - up < c <= be + down
                if pg == ps and (c < bs - up or (on_s and w[1] < xs - 0.5)):
                    continue
                if pg == pe and (c > be + down or (on_e and w[3] > xe + 0.5)):
                    continue
                if on_s:
                    head.append(w)
                elif on_e:
                    tail.append(w)
                else:
                    mid.append(w)
            ls = ([sorted(head, key=lambda w: w[1])] if head else []) + lines_of(mid, L) + \
                 ([sorted(tail, key=lambda w: w[1])] if tail else [])
            parts.append((pg, ls))
        return [(pg, ls) for pg, ls in parts if ls]

    # shared lines: a step's first line is shared when the step before ends on it, and so on
    def same_line(a, b):
        return a[0] == b[0] and abs(a[2] - b[2]) < 0.3 * L.bskip

    # -- carry everything to the arXiv PDF: first the blocks that place themselves, then the others
    regions_d, regions_s, words_s, line_counts = {}, {}, {}, {}
    first = {}
    for rec in D['displays'] + [st for st in steps if st['kind'] == 'display']:
        box, why = display_box(rec)
        if box is None:
            missing[rec['id']] = why
            continue
        first[rec['id']] = (box, C.first(box[1], box[0]))
    parts_of = {}
    for n, st in enumerate(steps):
        if st['kind'] != 'prose' or n not in sm:
            continue
        parts = prose_parts(n)
        if not parts:
            missing[st['id']] = 'no words between the markers'
            continue
        parts_of[n] = [(pg, [(ln, C.first(ln, pg)) for ln in ls]) for pg, ls in parts]
    for rec in D['displays'] + [st for st in steps if st['kind'] == 'display']:
        if rec['id'] not in first:
            continue
        c = finish_display(*first[rec['id']])
        if c is None:
            missing[rec['id']] = 'words of the rebuilt box not found in the arXiv PDF'
            continue
        p2, y0, y1, how = c
        if rec['kind'] == 'display' and 'proof_item' not in rec:
            regions_d[rec['id']] = [dict(page=p2, box=[L.left(p2) - PAD, y0 - PAD, L.left(p2) + L.width + PAD, y1 + PAD],
                                         method=how)]
        else:
            regions_s[rec['id']] = [dict(page=p2, quads=[[L.left(p2), y0, L.left(p2) + L.width, y1]], method=how)]
            words_s[rec['id']] = [(p2, v) for v in arx[p2 - 1][2]
                                  if y0 < cy(v) < y1 and L.left(p2) - 30 < v[1] < L.left(p2) + L.width + 30]
    for n, parts in parts_of.items():
        st = steps[n]
        line_counts[st['id']] = sum(len(ls) for _, ls in parts)
        prev_shared = n - 1 in sm and steps[n - 1]['proof_item'] == st['proof_item'] and same_line(sm[n - 1][1], sm[n][0])
        next_shared = n + 1 in sm and steps[n + 1]['proof_item'] == st['proof_item'] and same_line(sm[n][1], sm[n + 1][0])
        # carry line by line
        mapped, how = [], 'marker'
        for pg, ls in parts:
            for ln, c in ls:
                if isinstance(c, list):
                    c = C.resolve(ln, pg, c)
                if c is None:
                    mapped = None
                    break
                p2, dy = c
                if not (p2 == pg and abs(dy) <= 1):
                    how = 'shift'
                mapped.append((p2, [(v[0], v[1], v[2] + dy, v[3], v[4] + dy) for v in ln], pg, ln, dy))
            if mapped is None:
                break
        if mapped and how == 'marker' and not all(in_place([w for ln, _ in ls for w in ln], pg) for pg, ls in parts):
            how = 'shift'
        # the lines must stay in order
        if mapped and any((b[0], b[1][0][2]) <= (a[0], a[1][0][2]) for a, b in zip(mapped, mapped[1:])):
            mapped = None
        if mapped is None:
            allw = [w for pg, ls in parts for ln, _ in ls for w in ln]
            got = seq_match(allw, parts[0][0], parts[-1][0])
            if got is None:
                missing[st['id']] = 'words of the rebuilt step not found in the arXiv PDF'
                continue
            how = 'words'
            mapped = []
            byp = collections.defaultdict(list)
            for p2, v in got:
                byp[p2].append(v)
            for p2 in sorted(byp):
                for ln in lines_of(byp[p2], L):
                    mapped.append((p2, ln, None, None, None))
        # the full lines' extent on the arXiv page: every arXiv word on the line, within the column
        out, own = [], []
        for i, (p2, ln, pg, myln, dy) in enumerate(mapped):
            top, bot = min(v[2] for v in ln), max(v[4] for v in ln)
            if pg is not None:
                # the whole rebuilt line (other steps' words too) gives the line's height
                full = [w for w in page(pg).words if min(x[2] for x in myln) - 0.5 <= cy(w) <= max(x[4] for x in myln) + 0.5]
                top = min([top] + [w[2] + dy for w in full if abs(cy(w) - cy(myln[0])) < 0.6 * L.bskip])
                bot = max([bot] + [w[4] + dy for w in full if abs(cy(w) - cy(myln[0])) < 0.6 * L.bskip])
            x0, x1 = L.left(p2), L.left(p2) + L.width
            if i == 0 and prev_shared:
                x0 = min(v[1] for v in ln) - XPAD
            if i == len(mapped) - 1 and next_shared:
                x1 = max(v[3] for v in ln) + XPAD
            out.append((p2, [x0, top, x1, bot]))
            own += [(p2, v) for v in ln]
        # merge full lines into blocks, per page
        regs = []
        for p2 in sorted({p for p, _ in out}, key=lambda p: [q for q, _ in out].index(p)):
            rs = [r for p, r in out if p == p2]
            quads = []
            for r in rs:
                if quads and quads[-1][0] == r[0] and quads[-1][2] == r[2] and r[0] == L.left(p2) and r[2] == L.left(p2) + L.width:
                    quads[-1] = [r[0], quads[-1][1], r[2], max(quads[-1][3], r[3])]
                else:
                    quads.append(list(r))
            regs.append(dict(page=p2, quads=quads, method=how))
        regions_s[st['id']] = regs
        words_s[st['id']] = own

    # -- padding: up to PAD above and below, never past the midpoint to another new region on the page
    allregs = [(i, r, 'd') for i, rs in regions_d.items() for r in rs]
    for i, rs in regions_s.items():
        for r in rs:
            for q in r['quads']:
                q[1] -= PAD
                q[3] += PAD
            allregs.append((i, r, 's'))
    for i, r, kind in allregs:
        if kind == 'd':
            r['quads'] = [r.pop('box')]
    by_page = collections.defaultdict(list)
    for i, r, kind in allregs:
        by_page[r['page']].append((i, r))
    for pg, lst in by_page.items():
        qs = [(i, q) for i, r in lst for q in r['quads']]
        for a in range(len(qs)):
            for b in range(a + 1, len(qs)):
                (ia, qa), (ib, qb) = qs[a], qs[b]
                if ia == ib or not inter(qa, qb, 0):
                    continue
                upper, lower = (qa, qb) if qa[1] <= qb[1] else (qb, qa)
                if lower[1] >= upper[1] + 1 and upper[3] <= lower[3] - 1:
                    mid = (upper[3] + lower[1]) / 2
                    upper[3], lower[1] = mid - 0.05, mid + 0.05
    # the items' regions (regions.py) bound the padding too; a display inside a theorem-like item may lie in it
    item_rect = collections.defaultdict(list)
    for iid, regs in item_regs.items():
        for r in regs:
            W, H = arx[r['page'] - 1][0], arx[r['page'] - 1][1]
            x, y, w, h = r['rect']
            item_rect[r['page']].append((iid, [x * W, y * H, (x + w) * W, (y + h) * H]))
    item_overlaps = []
    for i, r, kind in allregs:
        inside = (D_by_id.get(i) or {}).get('inside_item')
        for q in r['quads']:
            for iid, o in item_rect[r['page']]:
                if iid == inside or not inter(q, o, 0):
                    continue
                # the item's box may reach into the padding and the font boxes' overhang below a line's
                # depth (a display set close to the line before it): cut, keeping most of a line
                if o[1] <= q[1] and q[3] - o[3] >= 0.6 * L.bskip:
                    q[1] = o[3] + 0.05
                elif o[3] >= q[3] and o[1] - q[1] >= 0.6 * L.bskip:
                    q[3] = o[1] - 0.05
                else:
                    item_overlaps.append((i, iid, r['page']))
    # -- checks on the arXiv PDF
    fails = collections.defaultdict(list)
    size = {p: (arx[p - 1][0], arx[p - 1][1]) for p in range(1, len(arx) + 1)}

    strict = []

    def centre_text(p2, q):
        return ' '.join(v[0] for v in arx[p2 - 1][2] if q[0] < (v[1] + v[3]) / 2 < q[2] and q[1] < cy(v) < q[3])

    def crop_all(regs):
        return '\n'.join(crop(pdf, r['page'], q, size[r['page']]) for r in regs for q in r['quads'])

    recs = {r['id']: r for r in D['displays']}
    recs.update({s['id']: s for s in steps})
    tok_none, word_share, low_share_in_place = [], [], []
    for i, regs in list(regions_d.items()) + [(i, r) for i, r in regions_s.items() if recs[i]['kind'] == 'display']:
        toks = distinctive(recs[i]['latex'])
        text = norm(crop_all(regs))
        # and the letters of the rebuilt display's words (each two or more letters or digits)
        mk = [norm(w[0]) for w in first[i][0][1] if len(norm(w[0])) >= 2]
        if mk:
            share = sum(1 for k in mk if k in text) / len(mk)
            word_share.append(share)
            # a box in place on the arXiv page (method marker) has the rebuilt words' boxes; their
            # letters can differ (the math fonts of the two TeX versions extract differently)
            if share < 0.8 and any(r['method'] != 'marker' for r in regs):
                fails['display_words'].append((i, round(share, 2)))
            elif share < 0.8:
                low_share_in_place.append((i, round(share, 2)))
        if not toks:
            tok_none.append(i)
            if not text:
                fails['display_crop_empty'].append(i)
            continue
        lost = [t for t in toks if norm(t) not in text]
        if lost:
            fails['display_tokens'].append((i, lost))
    for i, regs in regions_s.items():
        if recs[i]['kind'] != 'prose':
            continue
        ws = strip_tex(recs[i]['latex'])
        if not ws:
            fails['no_words'].append(i)
            continue
        # the words whose centre lies in the region's first (last) two quads, and pdftotext's crop, which
        # keeps only words wholly inside
        fq = [(regs[0]['page'], q) for q in regs[0]['quads'][:2]]
        lq = [(regs[-1]['page'], q) for q in regs[-1]['quads'][-2:]]
        for name, qs, w in (('first_word', fq, ws[0]), ('last_word', lq, ws[-1])):
            if norm(w) not in norm(' '.join(centre_text(p2, q) for p2, q in qs)):
                fails[name].append((i, w))
            elif norm(w) not in norm('\n'.join(crop(pdf, p2, q, size[p2]) for p2, q in qs)):
                strict.append((i, name, w))
    # no word of a step in another step's region; no overlap between steps of one proof
    q_by_page = collections.defaultdict(list)
    for i, regs in regions_s.items():
        for r in regs:
            for q in r['quads']:
                q_by_page[r['page']].append((i, q))
    for i, own in words_s.items():
        for p2, v in own:
            c = ((v[1] + v[3]) / 2, cy(v))
            for j, q in q_by_page[p2]:
                if j != i and q[0] < c[0] < q[2] and q[1] < c[1] < q[3]:
                    fails['word_in_other_step'].append((i, j, p2, v[0]))
    for pg, lst in q_by_page.items():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                (ia, qa), (ib, qb) = lst[a], lst[b]
                if ia != ib and inter(qa, qb):
                    same = recs[ia]['proof_item'] == recs[ib]['proof_item']
                    fails['overlap_same_proof' if same else 'overlap_other_proof'].append((ia, ib, pg))
    for (i, regs) in regions_s.items():
        if len({r['page'] for r in regs}) != len(regs):
            fails['two_regions_on_a_page'].append(i)

    def emit(regs):
        out = []
        for r in regs:
            W, H = size[r['page']]
            qs = r['quads']
            bb = rect_of(qs)
            d = dict(page=r['page'], rect=[round(bb[0] / W, 5), round(bb[1] / H, 5), round((bb[2] - bb[0]) / W, 5),
                                           round((bb[3] - bb[1]) / H, 5)], method=r['method'])
            if len(qs) > 1:
                d['quads'] = [[round(v, 5) for v in (q[0] / W, q[1] / H, q[2] / W, q[1] / H, q[2] / W, q[3] / H, q[0] / W, q[3] / H)]
                              for q in qs]
            out.append(d)
        return out
    sha = hashlib.sha256(open(pdf, 'rb').read()).hexdigest()
    methods = collections.Counter(r['method'] for regs in list(regions_d.values()) + list(regions_s.values()) for r in regs)
    out = dict(pdf=dict(identifier=identifier, sha256=sha, bytes=os.path.getsize(pdf), pages=len(arx),
                        printed_page_offset=offset),
               coordinates='fractions of the displayed page (MediaBox, no rotation), from the top left: rect [x, y, w, h]; '
                           'quads [x0, y0, x1, y1, x2, y2, x3, y3] (top left, top right, bottom right, bottom left) where a '
                           'region is not one rectangle',
               displays={i: emit(r) for i, r in regions_d.items()},
               steps={i: emit(r) for i, r in regions_s.items()},
               printed_lines={i: n for i, n in line_counts.items() if n is not None},
               missing=missing, notes={k: v for k, v in notes.items() if v},
               checks=dict(displays=len(D['displays']), displays_with_regions=len(regions_d),
                           steps=len(steps), steps_with_regions=len(regions_s),
                           regions=sum(len(v) for v in list(regions_d.values()) + list(regions_s.values())),
                           methods=dict(methods), displays_without_distinctive_tokens=len(tok_none),
                           display_word_share_min=round(min(word_share), 3) if word_share else None,
                           overlaps_with_items=item_overlaps,
                           display_word_share_below_80_in_place=low_share_in_place,
                           word_held_by_centre_not_wholly=strict,
                           failures={k: v for k, v in fails.items()}))
    json.dump(out, open(out_path, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in out['checks'].items() if k != 'failures'}))
    print(json.dumps({k: len(v) for k, v in fails.items()}), 'missing', len(missing))


if __name__ == '__main__':
    main()
