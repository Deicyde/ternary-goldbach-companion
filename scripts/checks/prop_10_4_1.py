"""Check of [H, Proposition 10.4.1] (prop:nefumo), effect on Section 14.2.

Claim: the second error line of (10.36) uses sqrt(B_+) = 1.6812|eta_+|_2,
which drops a sqrt(phi(q)) in the a-sum of the S_{eta_1}-error; the argument
supports sqrt(L_{r,delta0}(eta_+)) instead.  Also the proof needs disjoint
arcs (x >= 2 delta0 r^2) though only x >= 1 is assumed: at x = 1 every arc has
half-width >= delta0/2.  All harmless in Section 14: with the sqrt(L)
correction and the misprinted E_* of (14.17), (14.26)'s 3.85628e-5 becomes
4.0221e-5 (x^2/kappa) and (14.27) still holds.

Book inputs:
  - intmajarc.tex:33-41   arcs of M_{delta0,r}; intmajarc.tex:926-936 x >= 1,
                          delta0 > 0, r >= 1; (10.36) at intmajarc.tex:944-956.
  - intmajarc.tex:640-643 L_{r,delta0} <= 2|eta|_2^2 sum_{q<=r odd} mu^2/phi.
  - conclusion.tex:282-290 (14.17): E_* <= (2.485e-19 + (381500 + 76 sqrt(300000))
                          / sqrt(1e25))/kappa, printed <= 1.33805e-8/kappa.
  - conclusion.tex:428-437 line 2: E_+ = 2.3922e-8, A = 8.7806, |eta_+|_2 <= 0.80014,
                          |eta_*|_2^2 <= 1.77082/kappa, kappa = 49.
  - conclusion.tex:240-260 C_{eta_o,eta_*} >= (1/kappa)(|phi|_1|eta_o|_2^2 -
                          |eta_o|_2^2(2+1/(2kappa^2))e^{-2kappa^2}) - 2.0002/kappa^3,
                          |phi|_1 = sqrt(pi/2); conclusion.tex:96 |eta_o|_2 >= 0.8001287.
  - conclusion.tex:455-477 (14.26): 2.9387e-5 sqrt(pi/2)/kappa + line 2 +
                          43 (log x)^2 x; C_0 >= 1.3203236; (14.27) >= 1.058259/kappa.

Confirms if: at x = 1 the arcs' total length exceeds 1 (so they overlap), the
corrected (14.26) error is about 4.022e-5/kappa, and the unrounded lower bound
for C_0 C minus it is still >= 1.058259/kappa.

Run: python3 -I prop_10_4_1.py

Ported from a 2026-11-06 check script.
"""
from math import sqrt, pi, log, exp, gcd

# disjointness at x = 1 (delta0 = 8, small r suffices to see the overlap)
d0 = 8
for r in (1, 2, 5):
    tot = 0.0
    minhw = 1e9
    for q in range(1, 2 * r + 1):
        if q % 2 and q > r:
            continue
        hw = d0 * r / (2 * q) if q % 2 else d0 * r / q
        minhw = min(minhw, hw)
        tot += 2 * hw * sum(1 for a in range(q) if gcd(a, q) == 1)
    print("x=1, delta0=8, r=%d: smallest half-width %.3f (>= delta0/2 = 4), total arc length %.1f > 1" % (r, minhw, tot))
ok_disj = minhw >= d0 / 2 and tot > 1

# sum mu^2/phi over odd q <= 150000
R = 150000
phi = list(range(R + 1))
sqf = [True] * (R + 1)
for p in range(2, R + 1):
    if phi[p] == p:
        for m in range(p, R + 1, p):
            phi[m] -= phi[m] // p
        for m in range(p * p, R + 1, p * p):
            sqf[m] = False
sL = sqrt(2 * sum(1.0 / phi[n] for n in range(1, R + 1, 2) if sqf[n]))
sB = sqrt(2.82643)

kap = 49
Es_print = 1.33805e-8
Es_true = 2.485e-19 + (381500 + 76 * sqrt(300000)) / sqrt(1e25)
print("(14.17): E_* kappa = %.6g (printed 1.33805e-8)" % Es_true)
Ep, A, np_, ns = 2.3922e-8, 8.7806, 0.80014, sqrt(1.77082)


def line2(Es, s):
    return Es * A + Ep * (sqrt(A) + s * np_) * sB * ns * sqrt(kap)


l_book = line2(Es_print, 1.6812)
l_fix = line2(Es_true, sL)
first = 2.9387e-5 * sqrt(pi / 2)
tail = 43 * log(4.9e26) ** 2 / 4.9e26 * kap
err_book, err_fix = first + l_book + tail, first + l_fix + tail
print("line 2 (x^2/kappa): book %.6g ; with sqrt(L) = %.5f|eta_+|_2 and true E_*: %.6g" % (l_book, sL, l_fix))
print("(14.26) error (x^2/kappa): book %.6g ; corrected %.6g" % (err_book, err_fix))
eo2 = 0.8001287 ** 2
cc = 1.3203236 * (sqrt(pi / 2) * eo2 - eo2 * (2 + 1 / (2 * kap ** 2)) * exp(-2 * kap ** 2) - 2.0002 / kap ** 2)
print("C_0 C kappa >= %.7f (unrounded; book rounds to 1.0594003 - 0.001102 = 1.0582983)" % cc)
low = cc - err_fix
print("(14.27): %.8f - %.6g = %.8f vs 1.058259" % (cc, err_fix, low))
ok14 = abs(err_fix - 4.0221e-5) < 2e-9 and low >= 1.058259

if ok_disj and sL > sB and ok14:
    print("CONFIRMED: at x = 1 the arcs of M_{8,r} have half-width >= 4 and overlap, sqrt(L) = %.4f|eta_+|_2 replaces 1.6812|eta_+|_2, and with this and the true E_* the (14.26) error is %.5g x^2/kappa, so (14.27) still holds (%.7f >= 1.058259) using the unrounded C_0 C bound." % (sL, err_fix, low))
else:
    print("NOT CONFIRMED: ok_disj=%s sL>sB=%s ok14=%s (lower bound %.8f)." % (ok_disj, sL > sB, ok14, low))
