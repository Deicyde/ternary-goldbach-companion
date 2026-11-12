"""Eq 2.2: |sum_n f(n)e(alpha n)| <= min(|f|_1 + |f'|_1/2, (|f'|_1/2)/|sin(pi alpha)|).

Claim: for f only compactly supported and piecewise continuous, with |f'|_1 the L1 norm of f'
counting jumps |f(x+) - f(x-)| (as the book prescribes after (2.1)), (2.2) fails when f takes an
isolated value at an integer (e.g. f = 1_{0}); it holds with |f'|_1 replaced by the pointwise
total variation.

Book inputs (notprem.tex):
  - l.126-130: the contribution of an exceptional point x_i to |f^(k)|_1 is
    |lim_{x->x_i+} f^(k-1)(x) - lim_{x->x_i-} f^(k-1)(x)| (k = 1: the jump of f).
  - l.143-155: (2.2) for f: R -> C compactly supported and piecewise continuous, and the
    justification sum_n |f(n)| <= |f|_1 + |f'|_1/2.

The test functions are piecewise constant: a finite list of open intervals with constant
values plus finitely many point values, so |f|_1, |f'|_1 (jumps between one-sided limits) and
the pointwise total variation are computed exactly with fractions.

Confirms if: for f = 1_{0} and for f = 1_{[-1,1]} - 0.01*1_{0} the left side of (2.2) exceeds
its right side, while the bound with the pointwise total variation holds for every test f.

Run: python3 -I eq_2_2.py

Ported from a 2026-11-06 check script.
"""
import cmath
import math
from fractions import Fraction as F


class Step:
    """f = sum of c on open intervals (a,b) (disjoint) plus overriding point values."""

    def __init__(self, pieces, points):
        self.pieces = pieces            # list of (a, b, c), a < b
        self.points = points            # dict x -> value

    def lim(self, x, side):
        # one-sided limit at x: value on the piece containing (x, x+eps) or (x-eps, x)
        for a, b, c in self.pieces:
            if (side > 0 and a <= x < b) or (side < 0 and a < x <= b):
                return c
        return F(0)

    def val(self, x):
        if x in self.points:
            return self.points[x]
        for a, b, c in self.pieces:
            if a < x < b:
                return c
        return self.lim(x, 1)           # endpoint of a piece with no point value: right limit

    def breaks(self):
        s = set(self.points)
        for a, b, _ in self.pieces:
            s |= {a, b}
        return sorted(s)

    def L1(self):
        return sum(abs(c) * (b - a) for a, b, c in self.pieces)

    def L1_deriv(self):
        # f' = 0 on each piece; each break contributes |f(x+) - f(x-)|
        return sum(abs(self.lim(x, 1) - self.lim(x, -1)) for x in self.breaks())

    def total_variation(self):
        tv = F(0)
        for x in self.breaks():
            l, v, r = self.lim(x, -1), self.val(x), self.lim(x, 1)
            tv += abs(v - l) + abs(r - v)
        return tv

    def lhs(self, alpha):
        lo = math.floor(min(self.breaks())) - 1
        hi = math.ceil(max(self.breaks())) + 1
        return abs(sum(complex(self.val(F(n))) * cmath.exp(2j * math.pi * alpha * n) for n in range(lo, hi + 1)))


def rhs(L1, D, alpha):
    s = abs(math.sin(math.pi * alpha))
    first = L1 + D / 2
    return min(first, D / 2 / s) if s > 1e-15 else first


tests = [
    ("1_{0}", Step([], {F(0): F(1)}), [0.0, 0.25, 0.5]),
    ("1_[-1,1] - 0.01*1_{0}", Step([(F(-1), F(1), F(1))], {F(-1): F(1), F(1): F(1), F(0): F(99, 100)}), [0.5]),
    ("1_[-1,1] + 0.01*1_{0}", Step([(F(-1), F(1), F(1))], {F(-1): F(1), F(1): F(1), F(0): F(101, 100)}), [0.0]),
    ("1_[-1,1] (no isolated value)", Step([(F(-1), F(1), F(1))], {F(-1): F(1), F(1): F(1)}), [0.0, 0.5, 0.3]),
]
fails_book, tv_ok = [], True
for name, f, alphas in tests:
    L1, D, TV = f.L1(), f.L1_deriv(), f.total_variation()
    for a in alphas:
        l = f.lhs(a)
        rb, rt = rhs(float(L1), float(D), a), rhs(float(L1), float(TV), a)
        bad = l > rb + 1e-12
        print("%-30s alpha=%.2f  LHS=%.4f  |f|_1=%s |f'|_1=%s -> RHS=%.4f %s ; TV=%s -> RHS_TV=%.4f %s"
              % (name, a, l, L1, D, rb, "FAILS" if bad else "holds", TV, rt,
                 "holds" if l <= rt + 1e-12 else "FAILS"))
        if bad:
            fails_book.append(name)
        tv_ok &= l <= rt + 1e-12

if "1_{0}" in fails_book and "1_[-1,1] - 0.01*1_{0}" in fails_book and tv_ok:
    print("CONFIRMED: (2.2) with |f'|_1 = L1 norm plus jumps fails for piecewise continuous f with an "
          "isolated integer value (1_{0}: 1 > 0), and holds with the pointwise total variation.")
else:
    print("NOT CONFIRMED: the test functions do not show (2.2) failing as claimed.")
