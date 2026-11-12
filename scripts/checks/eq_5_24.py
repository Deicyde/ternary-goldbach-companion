"""Check of [H, Eq (5.24)] and its footnote (proof of Lemma 5.1.2 area).

Claim: the footnote says that, in the case y_i = sqrt(x), a stronger inequality
with (1 - 3x^3) in place of (1 - x^3)^2 (1 - x^4) was proved by QEPCAD; that
stronger inequality is false for x > 0.5709, so the described check cannot cover
the stated range 0 < x < 1. Harmless: (5.24) itself holds on the whole range
(sampled) and is applied only with x = 1/p <= 1/2, where the stronger form holds.

Book inputs:
  - typeII.tex:522-526  (5.24): for x <= y1,y2 < 1 with y1^2, y2^2 <= x,
    1 + y1 y2/((1-y1+x)(1-y2+x)) <= (1-x^3)^2(1-x^4)/((1-y1y2)(1-y1y2^2)(1-y1^2y2)).
  - typeII.tex:527-539  reduction to boundary cases y1=y2, y_i=sqrt x, y_i=x; footnote with
    (1-3x^3) for the case y_i = sqrt x.
  - typeII.tex:541-546  (5.25): applied with x = 1/p, y_i = p^{-s_i}.

All signs are decided in exact rational arithmetic (x = t^2, y1 = t = sqrt x).
Confirms if: the stronger form fails at points with y1 = sqrt x and y2 strictly
between x and sqrt x for some x in (0.5709, 1), holds on a grid for x <= 1/2,
and (5.24) itself has no violation on a grid over the whole range.

Run: python3 -I eq_5_24.py

Ported from a 2026-11-06 check script.
"""
from fractions import Fraction as F


def gaps(x, y1, y2):
    """(RHS - LHS) for (5.24) and for the footnote's stronger form; exact."""
    lhs = 1 + y1 * y2 / ((1 - y1 + x) * (1 - y2 + x))
    den = (1 - y1 * y2) * (1 - y1 * y2 ** 2) * (1 - y1 ** 2 * y2)
    return ((1 - x ** 3) ** 2 * (1 - x ** 4) / den - lhs,
            (1 - 3 * x ** 3) / den - lhs)


# (a) the packet's point x=0.6, y1=sqrt(0.6), y2=0.6, in floating point
import math
x = 0.6
y1, y2 = math.sqrt(x), x
lhs = 1 + y1 * y2 / ((1 - y1 + x) * (1 - y2 + x))
den = (1 - y1 * y2) * (1 - y1 * y2 ** 2) * (1 - y1 ** 2 * y2)
print("(a) x=0.6, y1=sqrt x, y2=x: LHS=%.7f  stronger RHS=%.7f  (5.24) RHS=%.7f"
      % (lhs, (1 - 3 * x ** 3) / den, (1 - x ** 3) ** 2 * (1 - x ** 4) / den))

# (b) threshold of the stronger form at the corner y2 = x (y1 = t, x = t^2), exact bisection
lo, hi = F(70, 100), F(80, 100)
assert gaps(lo * lo, lo, lo * lo)[1] > 0 and gaps(hi * hi, hi, hi * hi)[1] < 0
for _ in range(50):
    mid = (lo + hi) / 2
    if gaps(mid * mid, mid, mid * mid)[1] > 0:
        lo = mid
    else:
        hi = mid
xstar = float(lo * lo)
print("(b) stronger form at corner y2=x changes sign at x* = %.10f" % xstar)

# (c) interior failures (y2 strictly between x and sqrt x): only case y_i = sqrt x covers them
interior_fail = []
for t in (F(7575, 10000), F(76, 100), F(77, 100), F(80, 100), F(85, 100), F(90, 100)):
    xx = t * t
    for u in (F(1, 1000), F(1, 100), F(1, 10), F(1, 2)):
        yy = xx + u * (t - xx)
        g = gaps(xx, t, yy)[1]
        if g < 0:
            interior_fail.append((float(xx), float(u), float(g)))
print("(c) interior failures (x, u, gap) with y2 = x + u(sqrt x - x):")
for row in interior_fail:
    print("     x=%.6f u=%.3f gap=%.4e" % row)

# (d) stronger form on a grid with x <= 1/2 (case y1 = sqrt x)
fails_d = npts_d = 0
for i in range(1, 141):
    t = F(i, 198)  # t <= 0.7071 ~ sqrt(1/2)
    xx = t * t
    if xx > F(1, 2):
        continue
    for k in range(0, 41):
        yy = xx + F(k, 40) * (t - xx)
        npts_d += 1
        if gaps(xx, t, yy)[1] < 0:
            fails_d += 1
print("(d) stronger form, x <= 1/2: %d exact points, %d failures" % (npts_d, fails_d))

# (e) (5.24) itself on the whole range: y_i = x + u_i (sqrt x - x)
neg_e = zero_e = npts_e = 0
for i in range(1, 100):
    t = F(i, 100)
    xx = t * t
    for a in range(0, 21):
        for b in range(a, 21):
            ya = xx + F(a, 20) * (t - xx)
            yb = xx + F(b, 20) * (t - xx)
            g = gaps(xx, ya, yb)[0]
            npts_e += 1
            if g < 0:
                neg_e += 1
            elif g == 0:
                zero_e += 1
print("(e) (5.24), 0<x<1: %d exact points, %d violations, %d equalities (y1=y2=x)"
      % (npts_e, neg_e, zero_e))

if interior_fail and 0.5 < xstar < 0.6 and fails_d == 0 and neg_e == 0:
    print("CONFIRMED: the footnote's stronger inequality with (1-3x^3) fails for x > %.4f "
          "(including interior points of the case y_i = sqrt x), so it cannot cover the stated "
          "range, while it holds for x <= 1/2 and (5.24) itself shows no violation on the "
          "whole range." % xstar)
else:
    print("NOT CONFIRMED: interior failures=%d, x*=%.4f, failures for x<=1/2=%d, "
          "(5.24) violations=%d." % (len(interior_fail), xstar, fails_d, neg_e))
