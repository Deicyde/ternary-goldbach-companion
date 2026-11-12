"""Compare the layouts of two PDFs word box by word box (`pdftotext -bbox`).

New code.  Used to show that the step markers change no layout: the build with the markers of
stepmarks.tex against the build with regionmarks.tex alone (whose boxes regions.py already
compared with the arXiv PDF), and each against the arXiv PDF.  A page is the same when both have
the same number of word boxes and each box of one has a box of the other at the same place
(to `tol` pt on every side; the text is not compared, since the two TeX versions' math fonts
extract to different characters).

Usage: python3 -I layout_check.py <pdf A> <pdf B> [<tol pt, default 0.01>] [<out json>]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regions import bbox_words  # noqa: E402


def same_page(a, b, tol):
    if len(a) != len(b):
        return False
    rest = sorted(b, key=lambda w: (round(w[2]), w[1]))
    for w in sorted(a, key=lambda w: (round(w[2]), w[1])):
        hit = next((k for k, v in enumerate(rest) if abs(v[1] - w[1]) <= tol and abs(v[2] - w[2]) <= tol
                    and abs(v[3] - w[3]) <= tol and abs(v[4] - w[4]) <= tol), None)
        if hit is None:
            return False
        rest.pop(hit)
    return True


def main():
    a, b = sys.argv[1:3]
    tol = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01
    A, B = bbox_words(a), bbox_words(b)
    diff = [p + 1 for p in range(min(len(A), len(B))) if not same_page(A[p][2], B[p][2], tol)]
    out = dict(a=a, b=b, tolerance_pt=tol, pages=[len(A), len(B)], pages_differing=diff,
               words=[sum(len(p[2]) for p in A), sum(len(p[2]) for p in B)])
    print(json.dumps(out))
    if len(sys.argv) > 4:
        json.dump(out, open(sys.argv[4], 'w'), indent=1)


main()
