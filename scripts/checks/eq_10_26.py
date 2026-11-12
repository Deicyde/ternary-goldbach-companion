"""Check of [H, Eq (10.26)] (eq:bfpink), the error term delta0 r log(2e^2 r)(x E^2 + K_{r,2}).

Claim: the coefficient log(2e^2 r) is not established: the proof's sum
sum_{q<=r odd} 1/q + sum_{q<=2r even} 2/q = 2H(floor r) - H(floor(r/2))/2
exceeds log(2e^2 r) for every integer r >= 19 (so on all of r >= 182); a
valid coefficient is 2 + (3/2) log r.  The K_{r,2} part also needs the factor
phi(q) lost before (10.25).  In Section 14.1 the terms stay ~1e-8 x.

Book inputs:
  - intmajarc.tex:606-625  (10.25): error weights delta0 r x/q (q odd <= r),
                           2 delta0 r x/q (q even <= 2r), times (E^2 + K_{q,2}/x).
  - intmajarc.tex:713-719  the harmonic-sum step giving log(2e^2 r).
  - intmajarc.tex:730-738  (10.26), r >= 182.
  - conclusion.tex:22,35,43-49,83,90-92: r = 150000, delta0 = 8,
                           E <= 2.3992e-8, K_{r,2} <= 9.71e-21 x, the term
                           "<= 1.00393e-8".

Computes the sum for r = 182..200000 against log(2e^2 r), the Section 14.1
term with log(2e^2 r) and with the true sum, and the K-part with the factor
phi(q)/q restored (exact totient sums).  Confirms if the sum exceeds
log(2e^2 r) at every integer r in 182..200000 while 2 + 1.5 log r bounds it,
and the corrected Section 14.1 terms stay below 1e-7.

Run: python3 -I eq_10_26.py

Ported from a 2026-11-06 check script.
"""
from math import log, e

R = 200000
H = [0.0] * (R + 1)
for n in range(1, R + 1):
    H[n] = H[n - 1] + 1.0 / n
S = lambda n: 2 * H[n] - 0.5 * H[n // 2]
coef = lambda r: log(2 * e * e * r)

fail = all(S(n) > coef(n) for n in range(182, R + 1))
alt = all(S(n) <= 2 + 1.5 * log(n) for n in range(182, R + 1))
print("r=182: sum %.6f vs log(2e^2 r) %.6f ; r=150000: sum %.6f vs %.6f (2+1.5 log r = %.6f)"
      % (S(182), coef(182), S(150000), coef(150000), 2 + 1.5 * log(150000)))
print("sum > log(2e^2 r) for all integers 182 <= r <= %d: %s ; sum <= 2 + 1.5 log r there: %s" % (R, fail, alt))

d0, r, E, K = 8, 150000, 2.3992e-8, 9.71e-21
t_book = d0 * r * coef(r) * (E * E + K)
t_true = d0 * r * S(r) * (E * E + K)
# totients up to 2r
N = 2 * r
phi = list(range(N + 1))
for p in range(2, N + 1):
    if phi[p] == p:
        for m in range(p, N + 1, p):
            phi[m] -= phi[m] // p
w_phi = sum(phi[q] / q for q in range(1, r + 1, 2)) + 2 * sum(phi[q] / q for q in range(2, N + 1, 2))
k_phi = d0 * r * w_phi * K
print("Section 14.1: delta0 r log(2e^2 r)(E^2+K/x) = %.5g (book prints <= 1.00393e-8)" % t_book)
print("              with the true sum                = %.5g" % t_true)
print("              K-part with phi(q): weight %.1f -> %.4g" % (w_phi, k_phi))
small = t_true + k_phi < 1e-7

if fail and alt and small:
    print("CONFIRMED: the harmonic sum behind (10.26) exceeds log(2e^2 r) at every r in [182, %d] (19.0900 > 14.6115 at r = 150000), so the coefficient is not established; 2 + 1.5 log r holds, and in Section 14.1 the corrected terms (%.3g and %.3g) remain negligible." % (R, t_true, k_phi))
else:
    print("NOT CONFIRMED: the harmonic sum does not exceed log(2e^2 r) on r >= 182, or the corrected terms are not negligible.")
