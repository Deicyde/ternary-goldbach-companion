"""Check of [H, Lemma 11.1.1] (lem:gosor).

Claim: the proof establishes sqrt(1+x) = 1 + x/2 + O*(x^2/2^{3/2}) only for
|x| <= 1/2, then applies it to x = (|w|^2-|v|^2)/|v|^2, which ranges over
[-3/4, 5/4] under the hypothesis |w-v| <= |v|/2.  Misprints: (1-(tx)^2)^{3/2}
for (1+tx)^{3/2}, and '1+delta' for '1+<w-v,v>/|v|^2'.  The lemma is true.

Book inputs:
  - optcoor.tex:88-93   statement: |w-v| <= |v|/2 => <v,w> = |v||w| + O*(2.71|v-w|^2).
  - optcoor.tex:94-101  the Taylor step and its range |x| <= 1/2.
  - optcoor.tex:103-107 x = (2<w-v,v> + |w-v|^2)/|v|^2, remainder
                        O*((2 delta+delta^2)^2/2^{3/2}), constant 1/2 + (5/2)^2/2^{3/2}.

Computes: x for w = v/2 and w = 3v/2 (delta = 1/2); the least delta allowing
|x| > 1/2; the printed and the corrected Lagrange factor at x = -1/2; the sup
of |sqrt(1+x)-1-x/2|/x^2 on [-3/4, 5/4]; the constant; and a random test of
the lemma in R^5.  Confirms if x reaches -3/4 and 5/4 (outside |x| <= 1/2),
the printed factor differs from the correct one, and the statement still holds
(sup <= 2^{-3/2}, random ratio <= 2.71).

Run: PYTHONPATH=<mpmath dir> python3 -s lemma_11_1_1.py

Ported from a 2026-11-06 check script.
"""
import random
import mpmath as mp

mp.mp.dps = 30


def xval(v, w):
    nv2 = sum(a * a for a in v)
    return (sum(b * b for b in w) - nv2) / nv2


v = [mp.mpf(1), mp.mpf(0)]
x_lo = xval(v, [mp.mpf("0.5"), 0])
x_hi = xval(v, [mp.mpf("1.5"), 0])
print("delta = 1/2: w = v/2 gives x = %s ; w = 3v/2 gives x = %s" % (x_lo, x_hi))
print("|x| > 1/2 possible once delta > sqrt(1.5) - 1 = %s" % mp.nstr(mp.sqrt(1.5) - 1, 8))

x = mp.mpf(-0.5)
printed = max(1 / (4 * (1 - (t * x) ** 2) ** 1.5) for t in mp.linspace(0, 1, 2001))
correct = max(1 / (4 * (1 + t * x) ** 1.5) for t in mp.linspace(0, 1, 2001))
print("x = -1/2: printed max 1/(4(1-(tx)^2)^{3/2}) = %s ; correct max 1/(4(1+tx)^{3/2}) = %s"
      % (mp.nstr(printed, 6), mp.nstr(correct, 6)))

ratio = lambda x: abs(mp.sqrt(1 + x) - 1 - x / 2) / x ** 2
grid = [x for x in mp.linspace(-0.75, 1.25, 4001) if x != 0]
sup = max(ratio(x) for x in grid)
print("sup_{x in [-3/4,5/4]} |sqrt(1+x)-1-x/2|/x^2 = %s (<= 2^{-3/2} = %s)" % (mp.nstr(sup, 8), mp.nstr(2 ** -1.5, 8)))
fail_at = mp.findroot(lambda x: ratio(x) - 2 ** -1.5, -0.96)
print("2^{-3/2} bound fails only below x = %s" % mp.nstr(fail_at, 8))
const = mp.mpf(1) / 2 + mp.mpf(25) / 4 / 2 ** mp.mpf(1.5)
print("1/2 + (5/2)^2/2^{3/2} = %s" % mp.nstr(const, 8))

random.seed(1)
worst = 0.0
for _ in range(100000):
    vv = [random.gauss(0, 1) for _ in range(5)]
    nv = sum(a * a for a in vv) ** 0.5
    d = [random.gauss(0, 1) for _ in range(5)]
    nd = sum(a * a for a in d) ** 0.5
    s = random.random() * 0.5 * nv / nd
    ww = [a + s * b for a, b in zip(vv, d)]
    nw = sum(a * a for a in ww) ** 0.5
    dist2 = sum((a - b) ** 2 for a, b in zip(vv, ww))
    if dist2 > 0:
        worst = max(worst, abs(sum(a * b for a, b in zip(vv, ww)) - nv * nw) / dist2)
print("random test (R^5, |w-v| <= |v|/2): sup |<v,w> - |v||w|| / |v-w|^2 = %.6f" % worst)

if x_lo < -0.5 and x_hi > 0.5 and abs(printed - correct) > 0.1 and sup <= 2 ** -1.5 and worst <= 2.71:
    print("CONFIRMED: under |w-v| <= |v|/2 the proof's x reaches %s and %s, outside the range |x| <= 1/2 where its Taylor bound was shown (and the printed remainder factor is %s instead of %s at x = -1/2), though the bound itself holds on [-3/4, 5/4] (sup %s) and the lemma is true." % (mp.nstr(x_lo, 3), mp.nstr(x_hi, 3), mp.nstr(printed, 3), mp.nstr(correct, 3), mp.nstr(sup, 4)))
else:
    print("NOT CONFIRMED: the range of x or the misprint did not reproduce, or the lemma failed.")
