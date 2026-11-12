"""Check of [H, Eq (9.35)] (eq:happin, proof of Lemma 9.2.1).

Claim: (9.35), sum_{Im rho > T0} f(Im rho) <= int_{T0}^oo f(T)((1/2pi)log(qT/2pi)
+ 1/(4T)) dT, is false even for q = 1: it is the decreasing-f clause of
Lemma 9.1.3, which drops the boundary term; the right side lacks
f(T0) g_chi(T0) with g_chi(T) = 0.5 log qT + 17.7.

Book inputs (expform.tex):
  - l.775: hypothesis T0 >= 50.
  - l.819-823 (9.34): f(tau) = 3.001 exp(-0.1065 (tau/(pi delta))^2)
    + 3.286 exp(-0.1598 |tau|).
  - l.830-833 (9.35) as above; l.536-538 (9.25) g_chi(T) = 0.5 log qT + 17.7.
Test case: zeta (q = 1), delta = 0.01 (the Gaussian term underflows to 0 for
tau >= 50), zeros from mpmath.zetazero up to height 330 (tail of the sum
bounded by the main-term integral times 2 beyond that height).

Confirms if: at T0 = 52.9 the left side exceeds the right side, (9.35)
fails at some T0 on a grid in [50,100], and adding f(T0)g(T0) to the right
side restores the inequality on the whole grid.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_9_35.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 25
q = 1
delta = mp.mpf("0.01")
HMAX = 330


def f(t):
    return 3.001 * mp.e ** (-0.1065 * (t / (mp.pi * delta)) ** 2) + 3.286 * mp.e ** (-0.1598 * abs(t))


def weight(T):
    return mp.log(q * T / (2 * mp.pi)) / (2 * mp.pi) + 1 / (4 * T)


g = lambda T: 0.5 * mp.log(q * T) + 17.7

zeros = []
n = 1
while True:
    t = mp.zetazero(n).imag
    if t > HMAX:
        break
    zeros.append(t)
    n += 1
print("zeta zeros up to height", HMAX, ":", len(zeros))
tail = 2 * mp.quad(lambda T: f(T) * weight(T), [HMAX, mp.inf])  # generous bound for zeros above HMAX


def lhs(T0):
    return mp.fsum(f(t) for t in zeros if t > T0)


def rhs(T0):
    return mp.quad(lambda T: f(T) * weight(T), [T0, HMAX, mp.inf])


T0 = mp.mpf("52.9")
L, R = lhs(T0), rhs(T0)
print("T0 = 52.9: LHS =", mp.nstr(L, 8), " RHS(9.35) =", mp.nstr(R, 8), " ratio =", mp.nstr(L / R, 5),
      " (sum tail above %d <= %s)" % (HMAX, mp.nstr(tail, 3)))
fails, worst, worst_T, repaired_ok = 0, 0, None, True
for k in range(201):
    T0g = 50 + mp.mpf(k) / 4
    Lg, Rg = lhs(T0g), rhs(T0g)
    if Lg > Rg:
        fails += 1
    if Lg / Rg > worst:
        worst, worst_T = Lg / Rg, T0g
    if Lg + tail > Rg + f(T0g) * g(T0g):
        repaired_ok = False
print("grid T0 = 50..100 step 0.25: (9.35) fails at", fails, "of 201 points; worst ratio",
      mp.nstr(worst, 5), "at T0 =", worst_T)
print("with f(T0) g(T0) added to the right side, holds on the whole grid:", repaired_ok)

if L > R and fails > 0 and repaired_ok:
    print("CONFIRMED: for zeta, delta = 0.01, T0 = 52.9 the left side of (9.35) is %s > %s, the right side; "
          "(9.35) fails at %d of 201 grid points and holds once f(T0)g(T0) is added." % (mp.nstr(L, 5), mp.nstr(R, 5), fails))
else:
    print("NOT CONFIRMED: (9.35) held at T0 = 52.9 or the repaired bound failed.")
