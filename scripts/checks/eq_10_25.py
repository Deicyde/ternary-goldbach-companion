"""Check of [H, Eq (10.25)] (eq:juto) and the display before it.

Claim: the display before (10.25) attaches the per-residue error of (10.8),
K_{q,1}(2 max|S_eta| + K_{q,1}), to the sum over all phi(q) residues a with
no factor phi(q); and it replaces max_alpha |S_eta(alpha,x)| by |S_eta(0,x)|,
valid only for eta of constant sign (Lemma 10.3.1 allows any real eta).
Both are harmless: the corrected K-part of (10.26) stays below 1e-8 x.

Book inputs:
  - intmajarc.tex:197-203 (10.8): per-alpha error O*(2 sum_{p|q} log p
                          sum_k eta(p^k/x)).
  - intmajarc.tex:544-581 display: sum_a |S_eta(a/q+delta/x)|^2 = main +
                          K_{q,1}(2|S_eta(0,x)| + K_{q,1}); K_{q,2}.
  - intmajarc.tex:585-625 (10.25); Lemma 10.3.1 (intmajarc.tex:723-730):
                          eta: [0,oo) -> R in L1 cap Loo.
  - intmajarc.tex (10.26)-(10.27): K-part delta0 r log(2e^2 r) K_{r,2}.
  - conclusion.tex:78-83: K_{r,2} <= 9.71e-21 x; delta0 = 8, r = 150000.

(a) q = 9973 (prime), x = 10^4, eta = 1_[0,1], delta = 0: with the main term
M_a of (10.8) (weights mu/phi((q,n^oo))), E_a = S_a - M_a has |E_a| = D
for all a; compare Delta = sum_a (|S_a|^2 - |M_a|^2) with the per-residue
bound D(2|S(0,x)| + D) and with phi(q) times it.  (b) eta = 1_[0,1] -
1_(1,2], x = 10^6: |S_eta(0,x)| versus |S_eta(1/(2x),x)| (limit 4x/pi).
(c) the K-part of (10.26) with and without the factor phi(q).
Confirms if Delta exceeds the per-residue bound but not phi(q) times it,
|S_eta(1/(2x),x)| > 100 |S_eta(0,x)|, and the corrected K-part lies between
the printed one and 1e-8 x.

Run: python3 -I eq_10_25.py

Ported from a 2026-11-06 check script.
"""
import cmath
from math import log, sqrt, pi, e as E


def mangoldt(N):
    L = [0.0] * (N + 1)
    sieve = bytearray([1]) * (N + 1)
    for p in range(2, N + 1):
        if sieve[p]:
            sieve[p * p::p] = bytearray(len(range(p * p, N + 1, p)))
            pk = p
            while pk <= N:
                L[pk] = log(p)
                pk *= p
    return L


# (a) the sum over residues
q, x = 9973, 10 ** 4
L = mangoldt(2 * 10 ** 6)
c = {n: L[n] for n in range(1, x + 1) if L[n]}
w = lambda n: 1.0 if n % q else -1.0 / (q - 1)  # mu((q,n^oo))/phi((q,n^oo)), q prime
cM = {n: w(n) * v for n, v in c.items()}


def sum_over_units(coef):
    # sum_{a mod q, (a,q)=1} |sum c_n e(an/q)|^2 = q sum_b |C_b|^2 - |sum c_n|^2
    B = {}
    for n, v in coef.items():
        B[n % q] = B.get(n % q, 0.0) + v
    return q * sum(v * v for v in B.values()) - sum(coef.values()) ** 2


Delta = sum_over_units(c) - sum_over_units(cM)
D = log(q) * (1 + 1.0 / (q - 1))  # |E_a| = Lambda(q)|1 - w(q)|, the same for every a
S0 = sum(c.values())
per = D * (2 * S0 + D)
K1 = (1 + sqrt(q)) * log(x) ** 2
print("(a) q=%d x=%d: Delta = %.6g ; per-residue D(2S(0)+D) = %.6g (D = %.5f); ratio %.3f"
      % (q, x, Delta, per, D, Delta / per))
print("    phi(q) * per-residue bound = %.6g ; book's K_{q,1}(2S(0)+K_{q,1}) = %.6g" % ((q - 1) * per, K1 * (2 * S0 + K1)))
ok_a = abs(Delta) > per and abs(Delta) <= (q - 1) * per

# (b) sign step
x = 10 ** 6
s0 = sum(L[n] for n in range(1, x + 1)) - sum(L[n] for n in range(x + 1, 2 * x + 1))
s1 = 0j
for n in range(1, 2 * x + 1):
    if L[n]:
        s1 += (1 if n <= x else -1) * L[n] * cmath.exp(1j * pi * n / x)
print("(b) eta = 1_[0,1] - 1_(1,2], x=1e6: S(0,x)/x = %.6f ; |S(1/(2x),x)|/x = %.6f (4/pi = %.6f); sum Lambda|eta|/x = %.5f"
      % (s0 / x, abs(s1) / x, 4 / pi, sum(L[1:2 * x + 1]) / x))
ok_b = abs(s1) > 100 * abs(s0)

# (c) size of the K-part of (10.26)
d0, r, K2 = 8, 150000, 9.71e-21
printed = d0 * r * log(2 * E ** 2 * r) * K2
crude = d0 * r * K2 * (len(range(1, r + 1, 2)) + 2 * len(range(2, 2 * r + 1, 2)))  # phi(q)/q <= 1
print("(c) printed K-part %.4g x ; with phi(q) (phi(q)/q <= 1) %.4g x ; total error of (14.7) 0.0754 x" % (printed, crude))
ok_c = printed < crude < 1e-8

if ok_a and ok_b and ok_c:
    print("CONFIRMED: summing the per-residue (10.8) error over a needs more than one copy (q=9973: Delta = %.3g x the per-residue bound), max|S_eta| is not |S_eta(0,x)| for sign-changing eta (ratio %.0f at x=1e6), and the corrected K-part %.2g x is still negligible." % (Delta / per, abs(s1) / abs(s0), crude))
else:
    print("NOT CONFIRMED: one of the three computations did not reproduce the claim.")
