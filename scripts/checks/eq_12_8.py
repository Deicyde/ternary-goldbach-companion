"""Check of [H, Eq (12.8)] (eq:cante, G(R) <= log R + 1.4709 for R >= 1).

Claim: [H] attributes (12.8) to [Ram95, Lemma 3.4], but the lemma it cites
under that number (the asymptotic (12.12)) yields (12.8) only for
R >= 1.46*10^5; the bound itself is [Ram95, Lemma 3.5(1)], and it is true and
sharp at R = 7.  The lemma numbering inside [Ram95] is not in the book; what is
checked here is the numerical part.

Book inputs:
  - l2normls.tex:332-336  (12.8) G(R) <= log R + 1.4709 for R >= 1, cited as
                          [Ram95, Lemma 3.4]; G(R) = sum_{r<=R} mu^2(r)/phi(r).
  - l2normls.tex:358-367  (12.12), also cited as [Ram95, Lem. 3.4]:
                          G_d(R) = (phi(d)/d)(log R + c_E + ...) + O*(7.284 R^(-1/3) f_1(d)),
                          with d = 1, f_1(1) = 1.
  - l2normls.tex:369-371  c_E = 1.3325822...
Method: G(n) - log n exactly (fractions -> floats) for n <= 2*10^5 (G is a step
function, so the sup over real R in [n, n+1) is at n); beyond, (12.12) gives
G(R) - log R <= c_E + 7.284 R^(-1/3).  Confirms if (12.8) holds, its max is at
R = 7 with value in (1.4707, 1.4709], and (12.12) alone fails to give (12.8)
below R0 = (7.284/(1.4709 - c_E))^3 ~ 1.46*10^5 (e.g. at R = 7).

Run: python3 -I eq_12_8.py

Ported from a 2026-11-06 check script.
"""
import math

N = 200000
CE = 1.3325822
# sieve phi and squarefree
phi = list(range(N + 1))
sqf = bytearray([1]) * (N + 1)
for p in range(2, N + 1):
    if phi[p] == p:
        for k in range(p, N + 1, p):
            phi[k] -= phi[k] // p
        pp = p * p
        for k in range(pp, N + 1, pp):
            sqf[k] = 0
G = 0.0
best = (-1e9, 0)
for n in range(1, N + 1):
    if sqf[n]:
        G += 1.0 / phi[n]
    d = G - math.log(n)
    if d > best[0]:
        best = (d, n)
print(f"max_{{1<=n<={N}}} G(n) - log n = {best[0]:.7f} at n = {best[1]}")
exact7 = 41 / 12 - math.log(7)
print(f"G(7) - log 7 = 41/12 - log 7 = {exact7:.7f}")
R0 = (7.284 / (1.4709 - CE)) ** 3
print(f"(12.12) gives G(R) <= log R + 1.4709 only for R >= {R0:.1f}")
print(f"(12.12) at R = 7: c_E + 7.284*7^(-1/3) = {CE + 7.284 * 7 ** (-1/3):.4f} > 1.4709")
tail_ok = CE + 7.284 * N ** (-1 / 3) <= 1.4709
print(f"(12.12) covers R >= {N}: {tail_ok}")
ok = best[0] <= 1.4709 and best[1] == 7 and 1.4707 < exact7 <= 1.4709 and R0 > 1.4e5 and tail_ok \
    and CE + 7.284 * 7 ** (-1/3) > 1.4709
if ok:
    print(f"CONFIRMED: (12.8) holds with maximum 41/12 - log 7 = {exact7:.7f} at R = 7, but (12.12), which the book cites as the same [Ram95, Lemma 3.4], yields it only for R >= {R0:.0f}.")
else:
    print("NOT CONFIRMED: the computed values do not match the claim.")
