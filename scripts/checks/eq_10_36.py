"""Check of [H, Eq (10.36)] (eq:opus111), lines 2 and 3.

Claim: line 2's factor 1.6812(sqrt A + 1.6812|eta_+|_2) rests on (10.34)'s
unjustified sqrt(B_+); line 1 lacks O*; and LS_eta uses log r although the
major arcs contain even moduli q <= 2r, which need log 2r
(q = 299986 has sum_{p|q} log p = 12.611 > log r = 11.918).  All negligible
in Section 14.2: line 2 becomes 2.333e-6/kappa and (14.27) still follows
(1.0582600 >= 1.058259 with the (14.17) correction).

Book inputs:
  - intmajarc.tex:33-41   (10.5): even q <= 2r are in M_{delta0,r}.
  - intmajarc.tex:815-836 integral of (10.11): max_{q<=r} sum_{p|q} log p ... -> log r.
  - intmajarc.tex:944-956 (10.36).
  - intmajarc.tex:640-643 L_{r,delta0} <= 2|eta|_2^2 sum_{q<=r odd} mu^2/phi.
  - conclusion.tex:282-290 (14.17); conclusion.tex:428-437 (line 2 numbers);
    conclusion.tex:240-260, 455-477 ((14.26), (14.27)); r = 150000, kappa = 49.

Computes max over squarefree even q <= 2r of sum_{p|q} log p (versus log r),
the Section 14.2 line 2 with sqrt(L) replacing sqrt(B_+), and the (14.27)
chain with the (14.17) value of E_* recomputed and the unrounded C_0 C bound.
Confirms if some even q <= 2r has sum_{p|q} log p > log r, line 2 becomes
2.333e-6/kappa, and (14.27) >= 1.058259/kappa still holds.

Run: python3 -I eq_10_36.py

Ported from a 2026-11-06 check script.
"""
from math import log, sqrt, pi, exp


def rad_log(n):
    s, p, m = 0.0, 2, n
    sqf = True
    while p * p <= m:
        if m % p == 0:
            s += log(p)
            m //= p
            if m % p == 0:
                sqf = False
                while m % p == 0:
                    m //= p
        p += 1
    if m > 1:
        s += log(m)
    return s, sqf


r = 150000
for q in (299986, 299998):
    s, sqf = rad_log(q)
    print("q=%d (even, <= 2r): squarefree %s, sum_{p|q} log p = %.4f vs log r = %.4f, log 2r = %.4f"
          % (q, sqf, s, log(r), log(2 * r)))
best = max(rad_log(q)[0] for q in range(2 * r - 200, 2 * r + 1, 2))
ok_log = best > log(r)

# Section 14.2
R = r
phi = list(range(R + 1))
sq = [True] * (R + 1)
for p in range(2, R + 1):
    if phi[p] == p:
        for m in range(p, R + 1, p):
            phi[m] -= phi[m] // p
        for m in range(p * p, R + 1, p * p):
            sq[m] = False
sL = sqrt(2 * sum(1.0 / phi[n] for n in range(1, R + 1, 2) if sq[n]))
kap, Ep, A, np_, ns, sB = 49, 2.3922e-8, 8.7806, 0.80014, sqrt(1.77082), sqrt(2.82643)
line2 = lambda Es, s: Es * A + Ep * (sqrt(A) + s * np_) * sB * ns * sqrt(kap)
Es_true = 2.485e-19 + (381500 + 76 * sqrt(300000)) / sqrt(1e25)
l_book, l_L, l_all = line2(1.33805e-8, 1.6812), line2(1.33805e-8, sL), line2(Es_true, sL)
print("line 2 (x^2/kappa): book %.6g ; sqrt(L) fix %.6g ; plus (14.17) E_* = %.5g/kappa: %.6g" % (l_book, l_L, Es_true, l_all))
first = 2.9387e-5 * sqrt(pi / 2)
tail = 43 * log(4.9e26) ** 2 / 4.9e26 * kap
eo2 = 0.8001287 ** 2
cc = 1.3203236 * (sqrt(pi / 2) * eo2 - eo2 * (2 + 1 / (2 * kap ** 2)) * exp(-2 * kap ** 2) - 2.0002 / kap ** 2)
low = cc - (first + l_all + tail)
low_rounded = 1.058298 - (first + l_all + tail)
print("(14.27): unrounded C_0 C kappa %.7f -> %.7f ; from the printed 1.058298 -> %.7f ; need 1.058259" % (cc, low, low_rounded))
ok14 = abs(l_L - 2.333e-6) < 1e-9 and low >= 1.058259

if ok_log and ok14:
    print("CONFIRMED: even moduli q <= 2r reach sum_{p|q} log p = %.4f > log r = %.4f, and with sqrt(L) for sqrt(B_+) line 2 of (10.36) is %.4g/kappa; (14.27) still holds (%.7f >= 1.058259) but only from the unrounded C_0 C bound (%.7f from the printed 1.058298)." % (best, log(r), l_L, low, low_rounded))
else:
    print("NOT CONFIRMED: ok_log=%s ok14=%s (lower bound %.8f)." % (ok_log, ok14, low))
