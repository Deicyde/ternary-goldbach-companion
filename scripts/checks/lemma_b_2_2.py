"""Check of [H, Lemma B.2.2] (|g(t) log y - k(t) 4 log 2| <= 7.87052 log y).

Claim: the proof asserts |arg(g(t)/k(t))| < 0.7 for t in [-2,2] (a full
period), but the true maximum is 0.854834, at t = +-0.49635. The conclusion
survives, since 0.8548 < pi/3, so (B.10) holds.

Book inputs:
  - notprem.tex l.34: e(x) = e^{2 pi i x}.
  - normfour.tex l.144-162: g(t) = 4e(-t/4) - 4e(-t/2) + e(-t),
    k(t) = 2e(-t/4) - e(-t/2), (B.10), |g| <= 7.87052 (Lemma B.1.1), and the
    assertion |arg(g/k)| < 0.7 < pi/3 on [-2,2].

Method: g and k have period 4; scan t in [-2,2] on a grid of 4*10^5 points,
refine the maximum of |arg(g/k)| by golden-section search, and evaluate
exactly at t = 1/2. Direct check of (B.10): with s = 4 log 2/log y in (0,2],
compute max over a grid of s and t of |g(t) - s k(t)|.

Confirms if: max |arg(g/k)| on [-2,2] exceeds 0.7 but is below pi/3, and the
direct sup of |g - s k| is at most 7.87052.

Run: python3 -I lemma_b_2_2.py

Ported from a 2026-11-06 check script.
"""
import cmath
import math

e = lambda x: cmath.exp(2j * math.pi * x)
g = lambda t: 4 * e(-t / 4) - 4 * e(-t / 2) + e(-t)
k = lambda t: 2 * e(-t / 4) - e(-t / 2)
A = lambda t: abs(cmath.phase(g(t) / k(t)))

N = 400000
best = max(((A(-2 + 4 * i / N), -2 + 4 * i / N) for i in range(N + 1)))
a, b = best[1] - 4 / N, best[1] + 4 / N
phi = (math.sqrt(5) - 1) / 2
for _ in range(80):
    c, d = b - phi * (b - a), a + phi * (b - a)
    if A(c) > A(d):
        b = d
    else:
        a = c
tmax = (a + b) / 2
print("max |arg(g/k)| on [-2,2] = %.7f at t = %.7f (g/k = %s)" % (A(tmax), tmax, g(tmax) / k(tmax)))
print("by symmetry also at t = %.7f: %.7f" % (-tmax, A(-tmax)))
print("at t = 1/2: |arg(g/k)| = %.7f, tan = %.7f, (26 + 19 sqrt 2)/46 = %.7f" %
      (A(0.5), math.tan(A(0.5)), (26 + 19 * math.sqrt(2)) / 46))
print("pi/3 = %.7f" % (math.pi / 3))

sup, arg = 0.0, None
for j in range(1, 201):
    s = 2 * j / 200
    for i in range(20001):
        t = -2 + 4 * i / 20000
        v = abs(g(t) - s * k(t))
        if v > sup:
            sup, arg = v, (s, t)
small = max(abs(g(-2 + 4 * i / 200000) - 1e-4 * k(-2 + 4 * i / 200000)) for i in range(200001))
print("max |g - s k| over s in [0.01, 2], t in [-2,2]: %.6f at s = %.2f, t = %.4f" % (sup, arg[0], arg[1]))
print("at s = 1e-4: max_t |g - s k| = %.6f (book |g| <= 7.87052)" % small)

ok = 0.7 < A(tmax) < math.pi / 3 and A(0.5) > 0.7 and max(sup, small) <= 7.87052
if ok:
    print("CONFIRMED: max |arg(g/k)| on [-2,2] is %.6f > 0.7 (at t = +-%.5f), but it is below pi/3 and max |g - s k| = %.6f <= 7.87052, so (B.10) still holds."
          % (A(tmax), abs(tmax), max(sup, small)))
else:
    print("NOT CONFIRMED: the computed maximum does not match the claim.")
