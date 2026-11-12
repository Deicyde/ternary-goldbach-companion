"""Regions of the numbered items of [H] on the arXiv PDF (arXiv:1501.05438v2).

New code.  Pipeline:

1. `build.sh` recompiles [H]'s arXiv source with `regionmarks.tex`, which records
   `\\pdfsavepos` markers (formal-companion's informalize marker mechanism) around every
   theorem-like item, numbered display and float.
2. This script turns the markers of that build into boxes on the rebuilt PDF: a display spans
   the text width, from the first to the last ink of the display (its words, from
   `pdftotext -bbox`); a theorem-like item covers its statement, from its head line to its last
   line or closing display, one region per page; a figure or table covers its float, a float
   with two captions split at the first caption.
3. Each box is carried to the arXiv PDF.  Where the words inside the box sit on the same page
   of the arXiv PDF at the same place (to 1 pt), the box is kept (`method: marker`).  The
   rebuilt layout is not the arXiv layout on every page (a newer TeX), so otherwise the box's
   words are found in the arXiv PDF's own word boxes, on that page and its neighbours, and the
   region is the span of the matched words, again across the text width (`method: words`); a
   display moves as one box, to where the arXiv PDF prints its number at the margin
   (`method: number`).
4. Checks on the arXiv PDF: the crop of each item's first region (`pdftotext -f p -l p -x -y -W
   -H`, in points) holds the item's printed number; regions of two items overlap only where one
   item holds the other.

Usage: python3 -I regions.py <build dir> <arXiv PDF> <items json> <out regions json> [<main file> <arXiv id>]
(defaults: `3nonpupbook`, `arXiv:1501.05438v2`, the book; `ternvin`, `arXiv:1312.7748v2` is the 2013 paper)
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

SP_PER_BP = 65781.76
PAD = 2.0


def bbox_words(pdf):
    """Per physical page: (width, height, [(text, x0, y0, x1, y1)]) from pdftotext -bbox."""
    out = subprocess.run(['pdftotext', '-bbox', pdf, '-'], capture_output=True, text=True).stdout
    pages, cur = [], None
    for line in out.splitlines():
        m = re.search(r'<page width="([\d.]+)" height="([\d.]+)">', line)
        if m:
            cur = (float(m.group(1)), float(m.group(2)), [])
            pages.append(cur)
            continue
        m = re.search(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', line)
        if m and cur is not None:
            t = m.group(5).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
            cur[2].append((t, float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))))
    return pages


def read_aux(build):
    marks, enddisp, geo, afterdisp = {}, {}, {}, set()
    for f in glob.glob(os.path.join(build, '*.aux')):
        s = open(f, encoding='latin-1').read()
        for name, x, y, p in re.findall(r'\\zref@newlabel\{([^}]*)\}\{\\posx\{(\d+)\}\\posy\{(\d+)\}\\abspage\{(\d+)\}\}', s):
            marks[name] = (int(p), int(x) / SP_PER_BP, int(y) / SP_PER_BP)
        for n, k in re.findall(r'\\rmenddisp\{([^}]*)\}\{(\d+)\}', s):
            enddisp[n] = int(k)
        afterdisp |= {int(k) for k in re.findall(r'\\rmafterdisp\{(\d+)\}', s)}
        m = re.search(r'\\rmgeometry\{([^}]*)\}', s)
        if m:
            geo = {k: int(v) / SP_PER_BP for k, v in (kv.split('=') for kv in m.group(1).split(','))}
    return marks, enddisp, geo, afterdisp


class Layout:
    def __init__(self, geo):
        self.H = geo['pdfpageheight']
        self.top = geo['texttop']
        self.bottom = geo['texttop'] + geo['textheight']
        self.width = geo['textwidth']
        self.odd, self.even = geo['textleft'], geo['evenleft']

    def y(self, mark):
        return self.H - mark[2]

    def left(self, page):
        return self.odd if page % 2 else self.even


def words_in(words, y0, y1, x0, x1):
    return [w for w in words if y0 < (w[2] + w[4]) / 2 < y1 and x0 - 30 < w[1] and w[3] < x1 + 30]


def read_sources(build):
    """The rebuilt source files, by name without `.tex`, as lists of lines; a file whose line holds
    `\\input{regionmarks}` (added before `\\begin{document}` by build.sh) has it removed, so lines
    are the arXiv source's."""
    out = {}
    for f in glob.glob(os.path.join(build, '*.tex')):
        lines = open(f, encoding='latin-1').read().split('\n')
        out[os.path.basename(f)[:-4]] = [l for l in lines if l.strip() != '\\input{regionmarks}']
    return out


def last_word(src, it):
    """The last word of text before the item's environment in its source (comments and blank lines
    skipped), letters and digits only, or None when that text ends in a command or a display."""
    lines = src.get(it['chapter_file'])
    if not lines:
        return None
    for k in range(it['line'] - 2, max(it['line'] - 40, -1), -1):
        t = re.sub(r'(?<!\\)%.*', '', lines[k]).strip()
        if not t:
            continue
        if t.endswith(('}', '\\]', '$$')) and not t.endswith('$'):
            return None
        m = re.search(r'([A-Za-z0-9]+)[^A-Za-z0-9]*$', t)
        return m.group(1) if m else None
    return None


def raw_boxes(items, marks, enddisp, afterdisp, L, mine, src):
    """Item id -> [(page, y0, y1)] on the rebuilt PDF, and the marker names used."""
    by_kind = collections.defaultdict(list)
    for it in items:
        by_kind['thm' if it['kind'] in ('theorem', 'lemma', 'proposition', 'corollary') else it['kind']].append(it)
    # an unnumbered theorem-like head (the 2013 paper's Main Theorem) is no item
    heads = sorted(((m, n[4:-5]) for n, m in marks.items() if n.startswith('thm:') and n.endswith(':head')
                    and n != 'thm::head'),
                   key=lambda t: (t[0][0], -t[0][2]))
    tags = sorted(((int(re.match(r'eq:(\d+):', n).group(1)), n.split('tag=')[1]) for n in marks if ':tag=' in n))
    boxes, notes = {}, collections.defaultdict(list)

    def span(page, lo, hi, floor=None):
        ws = words_in(mine[page - 1][2], lo, hi, L.left(page), L.left(page) + L.width)
        if not ws:
            return (page, lo, hi)
        top = min(w[2] for w in ws)
        if floor is not None:  # a tall glyph (a radical) reaches above the display: not into the line before it
            top = max(top, floor)
        return (page, top, max(w[4] for w in ws))

    # theorem-like items, matched in document order
    thms = by_kind['thm']
    if len(heads) != len(thms):
        sys.exit(f'{len(heads)} theorem heads, {len(thms)} theorem-like items')
    for (head, num), it in zip(heads, thms):
        if num != it['number']:
            notes[it['id']].append(f'rebuilt PDF numbers it {num}')
        if f'thm:{num}:below' in marks:
            end = marks[f'thm:{num}:below']
        elif num in enddisp:
            end = marks[f'disp:{enddisp[num]}:post']
        else:
            sys.exit(f'no end of {it["id"]}')
        p, q = head[0], end[0]
        hb = L.y(head)
        out = []
        for page in range(p, q + 1):
            lo = hb - 9 if page == p else L.top - 3
            hi = L.y(end) + 0.5 if page == q else L.bottom + 6
            out.append(span(page, lo, hi))
        boxes[it['id']] = out
    # numbered displays, in document order
    eqs = by_kind['equation']
    if len(tags) != len(eqs):
        sys.exit(f'{len(tags)} equation numbers, {len(eqs)} equation items')
    for (k, num), it in zip(tags, eqs):
        if num != it['number']:
            notes[it['id']].append(f'rebuilt PDF numbers it {num}')
        tag, post, pre = marks[f'eq:{k}:tag={num}'], marks[f'eq:{k}:post'], marks.get(f'eq:{k}:pre')
        page = tag[0]
        if post[0] != page:
            sys.exit(f'{it["id"]}: number and display end on different pages')
        # the display starts below the line before it and below any display above it on the page
        above = [L.y(m) for n, m in marks.items() if n.endswith(':post') and m[0] == page and L.y(m) < L.y(tag) - 1
                 and m is not post]
        floor = None
        if pre and pre[0] == page:
            lo = max([L.y(pre)] + above)
            floor = L.y(pre) + 1
        elif k in afterdisp:
            # it follows a display directly: it starts where that display ends, or at the top of
            # the text block when that display is on the page before
            lo = max(above) if above else L.top - 3
        else:
            # no marker before it: a display that opens a paragraph or a list item.  If the source's
            # text before the environment ends in a word, the display starts below where the rebuilt
            # page prints that word, between the display above and the number
            last = last_word(src, it)
            hits = [w for w in mine[page - 1][2] if last and key(w) == last and max(above + [0]) < w[2] < L.y(tag)
                    and L.left(page) - 2 <= w[1] <= L.left(page) + L.width]
            if hits:
                lo = max(w[4] for w in hits)
                floor = lo + 1
            else:
                # as far above the number's baseline as the display reaches below it
                lo = max([2 * L.y(tag) - L.y(post) - 2] + above)
                notes[it['id']].append('display top estimated: no line before the display')
        boxes[it['id']] = [span(page, lo, L.y(post) + 0.5, floor)]
    return boxes, notes


def float_regions(it, marks, arx, L):
    """A figure or table: found on the arXiv PDF by its caption.  Every float of [H] stands at the
    top of its page with its caption below it, so the region runs from the top of the text block
    to the caption's last line; two captions side by side split the text width between them."""
    cap = marks.get(f"cap:{it['kind']}:{it['number']}")
    if cap is None:
        return None, 'no caption marker'
    label = 'Figure' if it['kind'] == 'figure' else 'Table'
    for pg in (cap[0], cap[0] - 1, cap[0] + 1):
        ws = arx[pg - 1][2]
        for i in range(len(ws) - 1):
            if ws[i][0] == label and ws[i + 1][0] == it['number'] + ':':
                x0 = ws[i][1]
                beside = [w for w in ws if w[0] == label and abs(w[2] - ws[i][2]) < 1 and w[1] != x0]
                left, right = L.left(pg) - PAD, L.left(pg) + L.width + PAD
                if beside:
                    other = beside[0][1]
                    if other > x0:
                        right = other - 6
                    else:
                        left = x0 - 6
                outer = not beside or beside[0][1] < x0   # this float's right edge is the text block's
                col = [w for w in ws if left - 1 <= w[1] and w[3] <= right + (12 if outer else 1) and w[2] >= ws[i][2] - 1]
                col.sort(key=lambda w: w[2])
                bottom = ws[i][4]
                for w in col:
                    if w[2] <= bottom + 4:
                        bottom = max(bottom, w[4])
                if outer:  # a caption line may stick out of the text block
                    right = max([right] + [w[3] + PAD for w in col if w[2] <= bottom])
                W, H = arx[pg - 1][0], arx[pg - 1][1]
                top = L.top - PAD
                return [dict(page=pg, rect=[round(left / W, 5), round(top / H, 5),
                                            round((right - left) / W, 5), round((bottom + PAD - top) / H, 5)],
                             method='caption')], None
    return None, 'caption not found in the arXiv PDF'


def key(w):
    return re.sub(r'[^A-Za-z0-9]', '', w[0])


def carry_display(box, num, mine, arx, L):
    """A display moves as one box: find its number at the margin of the arXiv PDF (the side the
    rebuilt PDF prints it on) and shift the rebuilt box by the number's displacement.  Of several such tokens, take the one
    whose surroundings hold most of the box's words, and at least 60% of them."""
    page, y0, y1 = box
    tag = f'({num})'
    mt = [w for w in mine[page - 1][2] if w[0] == tag and y0 - 1 <= w[2] and w[4] <= y1 + 1]
    if not mt:
        return None
    mt = mt[0]
    # the number's margin: the right one in [H]; the left one in the 2013 paper (amsart, leqno)
    at_left = abs(mt[1] - L.left(page)) <= 2
    mw = collections.Counter(key(w) for w in words_in(mine[page - 1][2], y0 - 0.5, y1 + 0.5, L.left(page),
                                                       L.left(page) + L.width) if key(w))
    best, n = None, 0
    for pg in (page - 1, page, page + 1):
        if not 1 <= pg <= len(arx):
            continue
        for w in arx[pg - 1][2]:
            if w[0] != tag or (abs(w[1] - L.left(pg)) > 2 if at_left else abs(w[3] - (L.left(pg) + L.width)) > 2):
                continue
            n += 1
            d = w[2] - mt[2]
            aw = collections.Counter(key(v) for v in words_in(arx[pg - 1][2], y0 + d - 0.5, y1 + d + 0.5, L.left(pg),
                                                              L.left(pg) + L.width) if key(v))
            score = sum((mw & aw).values())
            if best is None or score > best[0]:
                best = (score, pg, d)
    if best is None or (n > 1 and best[0] < 0.6 * sum(mw.values())):
        return None
    _, pg, d = best
    # the number may wrap to a line of its own in one build and not the other: then the display's
    # words move by another displacement than the number.  Take the displacement most of the
    # display's words agree on (to 1 pt), and add the number's box
    body = [w for w in words_in(mine[page - 1][2], y0 - 0.5, y1 + 0.5, L.left(page), L.left(page) + L.width)
            if key(w) and w is not mt]
    votes = collections.Counter()
    for w in body:
        ds = {round(v[2] - w[2]) for v in arx[pg - 1][2]
              if key(v) == key(w) and abs(v[1] - w[1]) <= 20 and abs(v[2] - w[2]) <= 40}
        votes.update(ds)
    if body and votes:
        dw, nv = votes.most_common(1)[0]
        if abs(dw - d) > 1.5 and nv >= 0.6 * len(body):
            at = next(v for v in arx[pg - 1][2] if v[0] == tag and abs(v[2] - (mt[2] + d)) < 0.01)
            return [(pg, min(y0 + dw, at[2]), max(y1 + dw, at[4]), 'number')]
    return [(pg, y0 + d, y1 + d, 'number')]


def carry(box, mine, arx, L, num=None, identity_only=False):
    """Carry one rebuilt-PDF box to the arXiv PDF: [(page, y0, y1, method)] or None."""
    page, y0, y1 = box
    ws = words_in(mine[page - 1][2], y0 - 0.5, y1 + 0.5, L.left(page), L.left(page) + L.width)
    if not ws:
        return [(page, y0, y1, 'marker-no-words')]
    # the same layout here: a word box of the arXiv page at each word box of the rebuilt box
    # (positions only: the two builds' math fonts extract to different characters)
    there = arx[page - 1][2]
    same = sum(1 for w in ws if any(abs(w[1] - v[1]) <= 1 and abs(w[2] - v[2]) <= 1 and abs(w[3] - v[3]) <= 1.5
                                    for v in there))
    if same >= 0.95 * len(ws):
        return [(page, y0, y1, 'marker')]
    if num is not None:
        return carry_display(box, num, mine, arx, L)
    if identity_only:
        return None
    return carry_words([box], mine, arx, L)


def carry_words(boxes, mine, arx, L):
    """Find the words of an item's boxes (letters and digits only, in order) in the arXiv PDF's
    word boxes, from the page before its first box to the page after its last."""
    mw = [w for (page, y0, y1) in boxes
          for w in words_in(mine[page - 1][2], y0 - 0.5, y1 + 0.5, L.left(page), L.left(page) + L.width) if key(w)]
    first, last = boxes[0][0], boxes[-1][0]
    cand = [(pg, w) for pg in range(first - 1, last + 2) if 1 <= pg <= len(arx) for w in arx[pg - 1][2] if key(w)]
    sm = difflib.SequenceMatcher(None, [key(w) for w in mw], [key(c[1]) for c in cand], autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 3 or (b.size >= 1 and len(mw) <= 4)]
    # keep the densest run of blocks: stray matches of common words lie far from it
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
    per = collections.defaultdict(list)
    for pg, w in got:
        per[pg].append(w)
    return [(pg, min(w[2] for w in v), max(w[4] for w in v), 'words') for pg, v in sorted(per.items())]


def crop_text(pdf, page, rect, size):
    W, H = size
    x, y, w, h = rect[0] * W, rect[1] * H, rect[2] * W, rect[3] * H
    return subprocess.run(['pdftotext', '-f', str(page), '-l', str(page), '-x', str(int(x)), '-y', str(int(y)),
                           '-W', str(int(w + 1)), '-H', str(int(h + 1)), pdf, '-'], capture_output=True, text=True).stdout


def printed_number(it):
    if it['kind'] == 'equation':
        return f"({it['number']})"
    return it['number']


def main():
    build, pdf, items_path, out_path = sys.argv[1:5]
    main_file, identifier = (sys.argv[5:7] + ['3nonpupbook', 'arXiv:1501.05438v2'][len(sys.argv[5:7]):])
    items = json.load(open(items_path))['items']
    marks, enddisp, geo, afterdisp = read_aux(build)
    L = Layout(geo)
    mine = bbox_words(os.path.join(build, main_file + '.pdf'))
    arx = bbox_words(pdf)
    if len(mine) != len(arx):
        sys.exit(f'page counts differ: rebuilt {len(mine)}, arXiv {len(arx)}')
    boxes, notes = raw_boxes(items, marks, enddisp, afterdisp, L, mine, read_sources(build))

    regions, missing = {}, {}
    for it in items:
        iid = it['id']
        if it['kind'] in ('figure', 'table'):
            regs, why = float_regions(it, marks, arx, L)
            if regs:
                regions[iid] = regs
            else:
                missing[iid] = why
            continue
        if iid not in boxes:
            missing[iid] = '; '.join(notes[iid]) or 'no markers'
            continue
        per = collections.OrderedDict()
        if it['kind'] == 'equation':
            c = carry(boxes[iid][0], mine, arx, L, it['number'])
        else:
            parts = [carry(b, mine, arx, L, identity_only=True) for b in boxes[iid]]
            c = sum(parts, []) if all(parts) else carry_words(boxes[iid], mine, arx, L)
        if c is None:
            missing[iid] = 'words of the rebuilt box not found in the arXiv PDF'
            continue
        for pg, y0, y1, how in c:
            q = per.get(pg)
            per[pg] = (min(q[0], y0), max(q[1], y1), q[2] if q[2] == how else 'mixed') if q else (y0, y1, how)
        if per is None:
            continue
        regs = []
        for pg, (y0, y1, how) in per.items():
            W, H = arx[pg - 1][0], arx[pg - 1][1]
            x0 = L.left(pg) - PAD
            top, bot = max(0.0, y0 - PAD), min(H, y1 + PAD)
            regs.append(dict(page=pg, rect=[round(x0 / W, 5), round(top / H, 5), round((L.width + 2 * PAD) / W, 5),
                                            round((bot - top) / H, 5)], method=how))
        regions[iid] = regs

    # overlaps: shrink neighbouring boxes of items that do not nest to the midpoint between them
    src = {it['id']: it for it in items}
    def nests(a, b):
        A, B = src[a], src[b]
        return A['chapter_file'] == B['chapter_file'] and (A['line'] <= B['line'] <= B['end_line'] <= A['end_line']
                                                         or B['line'] <= A['line'] <= A['end_line'] <= B['end_line'])

    # a theorem-like item's box reaches down to the bottom of each display it holds on that page (a display's
    # box spans its ink, which can pass the last line of the item's words)
    holders = [i for i in regions if src[i]['kind'] not in ('equation', 'figure', 'table')]
    for e in [i for i in regions if src[i]['kind'] == 'equation']:
        for t in holders:
            A, B = src[t], src[e]
            if not (A['chapter_file'] == B['chapter_file'] and A['line'] <= B['line'] <= B['end_line'] <= A['end_line']):
                continue
            for re_ in regions[e]:
                for rt in regions[t]:
                    if rt['page'] == re_['page']:
                        top = min(rt['rect'][1], re_['rect'][1])
                        bot = max(rt['rect'][1] + rt['rect'][3], re_['rect'][1] + re_['rect'][3])
                        rt['rect'][1], rt['rect'][3] = round(top, 5), round(bot - top, 5)
    by_page = collections.defaultdict(list)
    for iid, regs in regions.items():
        for r in regs:
            by_page[r['page']].append((iid, r))
    overlaps = []
    for pg, lst in by_page.items():
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                (a, ra), (b, rb) = lst[i], lst[j]
                if nests(a, b):
                    continue
                if ra['rect'][0] + ra['rect'][2] <= rb['rect'][0] or rb['rect'][0] + rb['rect'][2] <= ra['rect'][0]:
                    continue
                ta, ba = ra['rect'][1], ra['rect'][1] + ra['rect'][3]
                tb, bb = rb['rect'][1], rb['rect'][1] + rb['rect'][3]
                if ta < bb and tb < ba:
                    upper, lower = (ra, rb) if ta <= tb else (rb, ra)
                    ub, lt = upper['rect'][1] + upper['rect'][3], lower['rect'][1]
                    mid = (ub + lt) / 2
                    if mid - upper['rect'][1] > 0.004 and lower['rect'][1] + lower['rect'][3] - mid > 0.004:
                        upper['rect'][3] = round(mid - upper['rect'][1] - 0.0002, 5)
                        lower['rect'][3] = round(lower['rect'][1] + lower['rect'][3] - mid - 0.0002, 5)
                        lower['rect'][1] = round(mid + 0.0002, 5)
                    else:
                        overlaps.append((pg, a, b))

    # acceptance: the crop of the first region holds the printed number
    fails, cont = [], 0
    for it in items:
        regs = regions.get(it['id'])
        if not regs:
            continue
        num = printed_number(it)
        for k, r in enumerate(regs):
            W, H = arx[r['page'] - 1][0], arx[r['page'] - 1][1]
            text = crop_text(pdf, r['page'], r['rect'], (W, H))
            r['holds_number'] = num in text
            if k == 0 and not r['holds_number']:
                fails.append((it['id'], r['page']))
            if k > 0:
                cont += 1
    sha = hashlib.sha256(open(pdf, 'rb').read()).hexdigest()
    methods = collections.Counter(r['method'] for regs in regions.values() for r in regs)
    out = dict(pdf=dict(identifier=identifier, sha256=sha, bytes=os.path.getsize(pdf), pages=len(arx)),
               coordinates='fractions of the displayed page (MediaBox, no rotation), from the top left: [x, y, w, h]',
               items={iid: regs for iid, regs in regions.items()},
               missing=missing, notes={k: v for k, v in notes.items() if v},
               checks=dict(regions=sum(len(v) for v in regions.values()), items_with_regions=len(regions),
                           methods=dict(methods), first_region_number_failures=fails,
                           continuation_regions=cont, overlaps_not_nested=overlaps))
    json.dump(out, open(out_path, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(out['checks'], indent=1))
    print('missing', missing)


main()
