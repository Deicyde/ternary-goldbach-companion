"""Check of [H, Lemma 9.4.1] (constant 11.308 of the exponential part).

Claim: the proof does not give the stated constants. (1) Step (9.66) uses the
decreasing-f clause of Lemma 9.1.3, which drops the boundary term
f(T0) g_chi(T0), g_chi(T) = 0.5 log qT + 17.7; with it the method needs about
94 (q=1, H=25, T0=75), 69 (q=1, H=200, T0=250) and 28 at Sec. 9.6's heights.
(3) Even granting (9.66), 11.308 fails at T0-H = 50, T0 = 75: the last line
of (9.67) gives 11.3306 there, and the exact first line of (9.67) needs
11.3654 for q = 1. (Parts (2), complex chi, and (4), a typo, are not numerical.)

Book inputs (expform.tex):
  - 528-543  Lemma 9.1.3 and g_chi(T) = 0.5 log qT + 17.7.
  - 1473-1491 Lemma 9.4.1: H >= 25, T0 >= H + max(10 pi|delta|, 50); bound
             (11.308 sqrt(T0') e^{-0.1598 T0'} + 16.147|delta| e^{...}) log(qT0/2pi).
  - 1515-1533 g(tau), kappa_{1,1} = 4.017, |Mh(ir)|_1 <= 16.193918,
             f(tau) = |Mh|_1/(2pi) g(tau - H).
  - 1536-1544 (9.66); 1559-1578 (9.67) with 10.3532,
             a = 1/2 + (1 + 0.1598 pi/2)/log T0, and "at most 11.308".
  - 2190-2200 Sec. 9.6: H = 200, T0 = H + 250 r/q, r = 150000 (q odd).
Units: N = sqrt(T0-H) log(qT0/2pi) e^{-0.1598 (T0-H)}. At delta = 0 (allowed)
the Gaussian terms of g and of the lemma vanish, so no slack is available.

Confirms if: the zeta zero sum at q=1, H=25, T0=75 exceeds (9.66)'s right side
(so the boundary term is needed); with it the needed constant is far above
11.308 at all listed parameters; and, granting (9.66), the last line of (9.67)
and the exact first line both exceed 11.308 at q=1, H=25, T0=75.

Run: PYTHONPATH=<mpmath dir> python3 -s lemma_9_4_1.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 20
PI = mp.pi
c = mp.mpf("0.1598")
K = mp.mpf("4.017") * mp.mpf("16.193918") / (2 * PI)  # 10.3532


def norm(q, H, T0):
    return mp.sqrt(T0 - H) * mp.log(q * T0 / (2 * PI)) * mp.exp(-c * (T0 - H))


def first_line(q, H, T0):
    """Exact first line of (9.67) = right side of (9.66) at delta = 0."""
    y = T0 - H
    F = lambda u: K * mp.sqrt(u) * mp.exp(-c * u) * (mp.log(q * (u + H) / (2 * PI)) / (2 * PI) + 1 / (4 * (u + H)))
    return mp.quad(F, [y, y + 20, y + 100, mp.inf])


def boundary(q, H, T0):
    return K * mp.sqrt(T0 - H) * mp.exp(-c * (T0 - H)) * (mp.mpf("0.5") * mp.log(q * T0) + mp.mpf("17.7"))


# (1a) zeta test: the step (9.66) itself fails at q=1, H=25, T0=75
H, T0 = mp.mpf(25), mp.mpf(75)
f = lambda T: K * mp.sqrt(T - H) * mp.exp(-c * (T - H))
n = 19  # N(75) = 18
assert mp.zetazero(18).imag < 75 < mp.zetazero(19).imag
S = mp.mpf(0)
while True:
    gam = mp.zetazero(n).imag
    S += f(gam)
    n += 1
    if gam > 250:
        break
rhs = first_line(1, H, T0)
print("zeta, H=25, T0=75: sum f(gamma) =", mp.nstr(S, 7), " right side of (9.66) =", mp.nstr(rhs, 7))
ok1a = S > rhs

# (1b) constants needed with the boundary term restored
r = 150000
cases = [(1, 25, 75), (3, 25, 75), (1, 200, 250), (150000, 200, 200 + 250 * r // 150000),
         (3, 200, 200 + 250 * r // 3), (1, 200, 200 + 250 * r)]
ok1b = True
bs = []
for (q, h, t0) in cases:
    q, h, t0 = mp.mpf(q), mp.mpf(h), mp.mpf(t0)
    a = first_line(q, h, t0) / norm(q, h, t0)
    b = (first_line(q, h, t0) + boundary(q, h, t0)) / norm(q, h, t0)
    print("q=%s H=%s T0=%s: (9.66) as printed needs %s; with f(T0)g(T0) restored %s"
          % (mp.nstr(q, 7), mp.nstr(h, 4), mp.nstr(t0, 9), mp.nstr(a, 7), mp.nstr(b, 6)))
    ok1b = ok1b and b > 2 * 11.308
    bs.append(b)

# (3) granting (9.66), at q=1, H=25, T0=75
aa = mp.mpf("0.5") + (1 + c * PI / 2) / mp.log(75)
last = mp.mpf("10.3532") / (2 * PI) * (1 / c + aa / (c ** 2 * 50))
last100 = mp.mpf("10.3532") / (2 * PI) * (1 / c + (mp.mpf("0.5") + (1 + c * PI / 2) / mp.log(100)) / (c ** 2 * 50))
ex = first_line(1, 25, 75) / norm(1, 25, 75)
excess = (ex - mp.mpf("11.308")) * norm(1, 25, 75)
print("last line of (9.67)/N at T0-H=50: T0=75 ->", mp.nstr(last, 7), "; T0=100 ->", mp.nstr(last100, 7))
print("exact first line of (9.67)/N, q=1, H=25, T0=75:", mp.nstr(ex, 7), "; absolute excess over 11.308 N:", mp.nstr(excess, 4))
ok3 = last > 11.308 and ex > 11.308

if ok1a and ok1b and ok3:
    print("CONFIRMED: (9.66) fails for zeta at q=1, H=25, T0=75, restoring f(T0)g_chi(T0) needs constants %s to %s instead of 11.308, and even granting (9.66) the last line of (9.67) gives %s and the exact first line %s > 11.308 at q=1, T0=75, delta=0."
          % (mp.nstr(min(bs), 3), mp.nstr(max(bs), 3), mp.nstr(last, 6), mp.nstr(ex, 6)))
else:
    print("NOT CONFIRMED: the computed constants do not exceed 11.308 as claimed.")
