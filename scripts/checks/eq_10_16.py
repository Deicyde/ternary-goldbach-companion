"""Check of [H, Eq (10.16)] (eq:henki; also (10.25)): arcs of M_{delta0,r} may overlap.

Claim: from (10.16) on, the integral over the union M_{delta0,r} is computed
arc by arc, which needs the arcs to be pairwise disjoint; the hypotheses
(x >= 1, delta0 > 0, r >= 1 in Prop 10.4.1; r >= 182 in Lemma 10.3.1) do not
ensure this.  For integer r >= 2 the arcs are disjoint exactly when
x >= delta0 r (2r-1); for delta0 = 8, r = 150000 they overlap for every
x < 3.599988e11.  Harmless in the application (x >= 4.9e26).

Book inputs:
  - intmajarc.tex:33-41   (10.5) M_{delta0,r}: arcs (a/q -+ delta0 r/(2qx)) for
                          q <= r odd, (a/q -+ delta0 r/(qx)) for q <= 2r even,
                          (a,q) = 1; "delta0 > 0, r >= 1 are given".
  - intmajarc.tex:325-337 (10.16): integral over M as a sum over arcs.
  - intmajarc.tex:583-592 (10.25): same for |S_eta|^2.
  - intmajarc.tex:926-935 Prop 10.4.1 hypotheses; intmajarc.tex:730 Lemma 10.3.1.
  - conclusion.tex: delta0 = 8, r = 150000, x >= 4.9e26.

Computes, in exact rationals, (a) the overlap threshold for the pair
1/299998, 1/300000 at r = 150000, delta0 = 8; (b) by an adjacent-centre scan,
the exact disjointness threshold for r = 2..40 and compares it with
delta0 r(2r-1); (c) for r = 5, x = 300 < 360 and eta = max(0, 1-|t-1|), the
sum over arcs of int |S_eta|^2 versus the integral over the union (exact
Fourier integration).  Confirms if (a) gives 3.599988e11, (b) matches
delta0 r(2r-1) for all r, and in (c) the two sides differ.

Run: python3 -I eq_10_16.py

Ported from a 2026-11-06 check script.
"""
from fractions import Fraction as F
from math import gcd, pi, sin, cos, log

D0 = 8


def arcs(r):
    """centres a/q and radii (times x) of M_{D0,r}."""
    out = []
    for q in range(1, 2 * r + 1):
        if q % 2 == 1 and q > r:
            continue
        rad = F(D0 * r, 2 * q) if q % 2 else F(D0 * r, q)
        for a in range(q):
            if gcd(a, q) == 1:
                out.append((F(a, q), rad))
    out.sort()
    return out


def threshold(r):
    A = arcs(r)
    best = F(0)
    for i in range(len(A)):
        c1, r1 = A[i]
        c2, r2 = A[(i + 1) % len(A)]
        d = (c2 - c1) % 1
        best = max(best, (r1 + r2) / d)  # overlap iff x < (r1+r2)/d
    return best


# (a) r = 150000
r = 150000
c1, c2 = F(1, 2 * r), F(1, 2 * r - 2)
rad1, rad2 = F(D0 * r, 2 * r), F(D0 * r, 2 * r - 2)
thr = (rad1 + rad2) / (c2 - c1)
print("r=150000: arcs at 1/300000 (radius %s/x) and 1/299998 (radius %.10f/x)" % (rad1, float(rad2)))
print("  overlap iff x < %s ; delta0 r (2r-1) = %d" % (thr, D0 * r * (2 * r - 1)))
ok_a = thr == D0 * r * (2 * r - 1)
x0 = F(10 ** 11)
print("  q=1 arc radius at x=1e11: %.4g; centre 1/300000 = %.4g -> inside: %s"
      % (float(F(D0 * r, 2) / x0), float(c1), c1 < F(D0 * r, 2) / x0))

# (b) small r
ok_b = True
for r in range(2, 41):
    t = threshold(r)
    if t != D0 * r * (2 * r - 1):
        ok_b = False
        print("  r=%d: threshold %s != %d" % (r, t, D0 * r * (2 * r - 1)))
print("(b) exact disjointness threshold == delta0 r(2r-1) for r = 2..40:", ok_b,
      "(e.g. r=5: %s, r=40: %s)" % (threshold(5), threshold(40)))

# (c) failure of the arc-by-arc identity for |S|^2, r = 5, x = 300
r, x = 5, 300
eta = lambda t: max(0.0, 1 - abs(t - 1))


def Lam(n):
    for p in range(2, n + 1):
        if n % p == 0:
            m = n
            while m % p == 0:
                m //= p
            return log(p) if m == 1 else 0.0
    return 0.0


coef = {n: Lam(n) * eta(n / x) for n in range(1, 2 * x + 1)}
coef = {n: c for n, c in coef.items() if c}
ns = list(coef)
# G(h) = sum_{m-n=h} c_m c_n ; int_a^b |S|^2 = sum_h G(h) int_a^b e(h t) dt
G = {}
for m in ns:
    for n in ns:
        G[m - n] = G.get(m - n, 0.0) + coef[m] * coef[n]


def intS2(a, b):
    tot = 0.0
    for h, g in G.items():
        if h == 0:
            tot += g * (b - a)
        else:
            w = 2 * pi * h
            tot += g * (sin(w * b) - sin(w * a)) / w  # imaginary parts cancel (G symmetric)
    return tot


ivs = [(float(c - rad / x), float(c + rad / x)) for c, rad in arcs(r)]
sum_arcs = sum(intS2(a, b) for a, b in ivs)
# union on R/Z: unwrap into [0,1) pieces
pieces = []
for a, b in ivs:
    if a < 0:
        pieces += [(a + 1, 1.0), (0.0, b)]
    elif b > 1:
        pieces += [(a, 1.0), (0.0, b - 1)]
    else:
        pieces.append((a, b))
pieces.sort()
union = []
for a, b in pieces:
    if union and a <= union[-1][1]:
        union[-1] = (union[-1][0], max(union[-1][1], b))
    else:
        union.append((a, b))
int_union = sum(intS2(a, b) for a, b in union)
print("(c) r=5, x=300: total arc length %.6f, union measure %.6f"
      % (sum(b - a for a, b in ivs), sum(b - a for a, b in union)))
print("    sum over arcs of int|S|^2 = %.4f ; int over union = %.4f" % (sum_arcs, int_union))
ok_c = abs(sum_arcs - int_union) > 1e-6 * abs(int_union)

if ok_a and ok_b and ok_c:
    print("CONFIRMED: the arcs of M_{8,r} are disjoint only for x >= 8r(2r-1) (exact for r = 2..40; 3.599988e11 for r = 150000), which the hypotheses of Prop 10.4.1 and Lemma 10.3.1 do not require, and below it the arc-by-arc sum (10.25) differs from the integral over the union.")
else:
    print("NOT CONFIRMED: the overlap threshold or the failure of the arc-by-arc identity did not reproduce.")
