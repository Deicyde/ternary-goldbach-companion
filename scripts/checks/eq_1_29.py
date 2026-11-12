"""Eq 1.29: "By Cauchy-Schwarz, the integrand is at most sqrt(S1(U,W) S2(V,W))".

Claim: since eta_1 = 2 on [1/2,1], the integrand of (1.28) is 4 * sum_m c_m sum_n Lambda(n) e(alpha m n)
over the unweighted ranges of (1.29), so Cauchy-Schwarz gives 4 sqrt(S1 S2), not sqrt(S1 S2); the
bound with the 4 holds (harmless slip, Ch. 5 (5.3) carries the 4).

Book inputs (introductionp.tex):
  - l.1336-1337: S = sum_m (1 * mu_{>U})(m) sum_{n>V} Lambda(n) e(alpha m n) eta(mn/x).
  - l.1346-1347: eta_1 = 2 on [1/2,1], 0 elsewhere; eta = eta_2 = eta_1 *_M eta_1.
  - l.1354-1357, (1.28): S = int_V^{x/U} sum_m c_m eta_1(m/(x/W)) sum_{n>=V} Lambda(n) e(alpha m n)
    eta_1(n/W) dW/W, c_m = sum_{d|m, d>U} mu(d).
  - l.1358-1363: the sentence and S1, S2 of (1.29), both unweighted.

Confirms if: (a) (1.28) reproduces S exactly at a small case, and the same integral with
indicators in place of eta_1 gives exactly S/4 (so the integrand carries the factor 4);
(b) at x = 1015000, U = V = 100, W = 10^4, alpha = 1/101 the integrand exceeds sqrt(S1 S2)
but not 4 sqrt(S1 S2).

Run: python3 -I eq_1_29.py

Ported from a 2026-11-06 check script.
"""
import cmath
import math
from fractions import Fraction


def sieve(N):
    mu = [1] * (N + 1)
    lam = [0.0] * (N + 1)
    comp = bytearray(N + 1)
    for p in range(2, N + 1):
        if comp[p]:
            continue
        for j in range(2 * p, N + 1, p):
            comp[j] = 1
        for j in range(p, N + 1, p):
            mu[j] = -mu[j]
        for j in range(p * p, N + 1, p * p):
            mu[j] = 0
        q, lp = p, math.log(p)
        while q <= N:
            lam[q] = lp
            q *= p
    return mu, lam


def cm(m, U, mu):
    return sum(mu[d] for d in range(U + 1, m + 1) if m % d == 0)


def e(t):
    return cmath.exp(2j * math.pi * t)


def eta2(t):
    # eta_1 *_M eta_1 with eta_1 = 2*1_[1/2,1]: 4 * log-length of [1/2,1] cap [t,2t]
    lo, hi = max(0.5, t), min(1.0, 2 * t)
    return 4 * math.log(hi / lo) if hi > lo else 0.0


ok = True
print("(a) identity (1.28) at x=300, U=3, V=6, alpha=3/17")
x, U, V = 300, 3, 6
alpha = Fraction(3, 17)
mu, lam = sieve(x)
S = 0j
S_w = 0j   # (1.28) with eta_1 weights, integrated exactly in W
S_i = 0j   # same with indicators 1_[1/2,1] in place of eta_1
for m in range(1, x + 1):
    c = cm(m, U, mu)
    if c == 0:
        continue
    for n in range(1, x // m + 1):
        if lam[n] == 0:
            continue
        ph = e(float((alpha * m * n) % 1))
        if n > V:
            S += c * lam[n] * ph * eta2(m * n / x)
        if n >= V:
            # W-range where eta_1(mW/x) eta_1(n/W) != 0, intersected with [V, x/U]
            lo = max(x / (2 * m), n, V)
            hi = min(x / m, 2 * n, x / U)
            if hi > lo:
                L = math.log(hi / lo)
                S_w += 4 * c * lam[n] * ph * L
                S_i += c * lam[n] * ph * L
print("  S direct        =", S)
print("  (1.28) eta_1    =", S_w)
print("  indicators      =", S_i, " 4*indicators =", 4 * S_i)
ok &= abs(S - S_w) < 1e-9 and abs(S - 4 * S_i) < 1e-9

print("(b) pointwise: x=1015000, U=V=100, W=10^4, alpha=1/101")
x, U, V, W = 1015000, 100, 100, 10000
alpha = Fraction(1, 101)
mu, lam = sieve(W)
ms = [m for m in range(1, x // W + 1) if Fraction(x, 2 * W) <= m]          # x/2W <= m <= x/W
ns = [n for n in range(max(V, W // 2), W + 1) if 2 * n >= W]               # max(V,W/2) <= n <= W
c = {m: (cm(m, U, mu) if m > U else 0) for m in ms}
b = {m: sum(lam[n] * e(float((alpha * m * n) % 1)) for n in ns if lam[n]) for m in ms}
S1 = sum(c[m] ** 2 for m in ms if Fraction(x, 2 * W) < m)
S2 = sum(abs(b[m]) ** 2 for m in ms)
integrand = abs(4 * sum(c[m] * b[m] for m in ms))     # eta_1(mW/x) eta_1(n/W) = 2*2
cs = math.sqrt(S1 * S2)
print("  nonzero c_m:", {m: v for m, v in c.items() if v})
print("  |integrand| = %.6f   sqrt(S1 S2) = %.6f   ratio = %.6f   4 sqrt(S1 S2) = %.6f"
      % (integrand, cs, integrand / cs, 4 * cs))
ok &= integrand > cs and integrand <= 4 * cs

if ok:
    print("CONFIRMED: the integrand of (1.28) is 4 times the unweighted bilinear sum and exceeds "
          "sqrt(S1 S2) (ratio %.4f at x=1015000, W=10^4, alpha=1/101), so Cauchy-Schwarz gives "
          "4 sqrt(S1 S2)." % (integrand / cs))
else:
    print("NOT CONFIRMED: the identity or the pointwise comparison does not show the missing factor 4.")
