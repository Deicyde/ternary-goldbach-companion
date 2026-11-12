"""Check of [H, Lemma 10.3.1] (lem:drujal), the coefficient log(2e^2 r) in (10.26).

Claim: the proof bounds sum_{q<=r odd} 1/q + sum_{q<=2r even} 2/q
= 2H(floor r) - H(floor(r/2))/2 by 2 log(er) - log(r/2) = log(2e^2 r), losing
the factor 1/2 on the last term.  The sum exceeds log(2e^2 r) for every
integer r >= 19 and every real r >= 21, hence on the lemma's range r >= 182.
Valid coefficients: 2 + (3/2) log r, or 2 log(er) - (1/2) log(r/2).  In
Section 14.1 the affected term is 1.32e-8 instead of 1.009e-8, negligible.

Book inputs:
  - intmajarc.tex:713-719  the harmonic-sum step.
  - intmajarc.tex:730-746  Lemma 10.3.1: r >= 182, coefficient delta0 r log(2e^2 r).
  - conclusion.tex:22,35   r = 150000, delta0 = 8; conclusion.tex:43-49
                           E_{eta+,r,delta0} <= 2.3992e-8; conclusion.tex:83
                           K_{r,2} <= 9.71e-21 x; conclusion.tex:90-92 the term.

Computes the sum exactly (Fractions for small n, fsum for large n) for
n = 1..300000 and compares with log(2e^2 n) and log(2e^2 (n+1)) (the sum is
constant on [n, n+1)); checks 2 + 1.5 log n >= sum; evaluates the Section 14.1
term.  Confirms if the sum exceeds log(2e^2 n) exactly for the integers
n >= 19, exceeds log(2e^2 (n+1)) for all 21 <= n <= 300000, and the claimed
alternative 2 + 1.5 log r holds throughout.

Run: python3 -I lemma_10_3_1.py

Ported from a 2026-11-06 check script.
"""
from fractions import Fraction as F
from math import log, fsum

NMAX = 300000
# H[n] as float with compensated summation
H = [0.0] * (NMAX + 1)
acc, comp = 0.0, 0.0
for n in range(1, NMAX + 1):
    y = 1.0 / n - comp
    t = acc + y
    comp = (t - acc) - y
    acc = t
    H[n] = acc
S = lambda n: 2 * H[n] - 0.5 * H[n // 2]

# exact check of the identity for small n
for n in (1, 2, 7, 19, 40):
    direct = sum(F(1, q) for q in range(1, n + 1, 2)) + sum(F(2, q) for q in range(2, 2 * n + 1, 2))
    ident = 2 * sum(F(1, q) for q in range(1, n + 1)) - F(1, 2) * sum(F(1, q) for q in range(1, n // 2 + 1))
    assert direct == ident

c = lambda r: log(2 * 2.718281828459045 ** 2 * r)
bad_int = [n for n in range(1, NMAX + 1) if S(n) > c(n)]
fails_all_real = all(S(n) > c(n + 1) for n in range(21, NMAX + 1))
alt_ok = all(S(n) <= 2 + 1.5 * log(n) + 1e-12 for n in range(1, NMAX + 1))
for r in (18, 19, 182, 150000):
    print("r=%6d: sum = %.6f  log(2e^2 r) = %.6f  2+1.5log r = %.6f  2log(er)-log(r/2)/2 = %.6f"
          % (r, S(r), c(r), 2 + 1.5 * log(r), 2 * (1 + log(r)) - 0.5 * log(r / 2)))
print("r=19.9: sum = %.6f  log(2e^2 r) = %.6f" % (S(19), c(19.9)))
print("integers n <= %d with sum > log(2e^2 n): first %d, count %d (expected %d)"
      % (NMAX, bad_int[0], len(bad_int), NMAX - 18))
print("sum > log(2e^2 (n+1)) for all 21 <= n <= %d:" % NMAX, fails_all_real)
print("sum <= 2 + 1.5 log n for all n <= %d:" % NMAX, alt_ok)
print("excess at n=%d minus (1/2)log n: %.5f" % (NMAX, S(NMAX) - c(NMAX) - 0.5 * log(NMAX)))

d0, r, E, K = 8, 150000, 2.3992e-8, 9.71e-21
t_print = d0 * r * c(r) * (E ** 2 + K)
t_true = d0 * r * S(r) * (E ** 2 + K)
print("Section 14.1 term: with log(2e^2 r) %.5g ; with the true sum %.5g (book prints <= 1.00393e-8)" % (t_print, t_true))

if bad_int == list(range(19, NMAX + 1)) and fails_all_real and alt_ok:
    print("CONFIRMED: sum_{q<=r odd}1/q + sum_{q<=2r even}2/q exceeds log(2e^2 r) for every integer r >= 19 and every real r >= 21 (r=182: %.4f > %.4f; r=150000: %.4f > %.4f), so (10.26)'s coefficient is not established; 2 + 1.5 log r is valid, and the Section 14.1 term becomes %.4g." % (S(182), c(182), S(150000), c(150000), t_true))
else:
    print("NOT CONFIRMED: the harmonic sum does not exceed log(2e^2 r) on the stated range.")
