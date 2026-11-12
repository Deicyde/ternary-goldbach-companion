"""Eq (3.2) of [H] (Theorem 3.1.1, case q <= x^{1/3}/6): the numerical parts of the claim
that the constant 0.5 is not established by the printed proof.

Claim: (6.77) halves the 0.67506 term twice, so the AM-GM constant is 0.81020, not the
printed 0.49911 (rounded to 0.5); hence [H]'s own (6.63) exceeds (3.2) by up to 2.65% for
prime q and about 3.2% for q with small phi(q)/q. Also (5.32)/(5.36) for v = 2 are false
((5.36) needs +0.0231), and the mu-sum bound before (6.12), done with (2.22) at modulus 2q,
gives 8/5 instead of 4/5, hence 8.21811 instead of 7.81811. The 2.5 and 3.36 terms are
correct roundings of 2.49157 and 3.35531.

Book inputs:
- (3.2), R_{x,t}, L_{x,t,q}: intromin.tex:84-111.
- (6.63) = eq:duaro: minarctotals.tex:1774-1786. AM-GM (6.76)-(6.77), rho, x_1 = 10^25,
  q_0 = 2*10^5: minarctotals.tex:2251-2288; C/log t <= 0.08659: minarctotals.tex:2290-2302.
- G_v, g_v, (5.32) = eq:passi, (5.36) = eq:velib, H_2: typeII.tex:393-398, 647-676,
  786-838.
- mu-sum bound with (m,2q)=1: minarctotals.tex:259-263; (2.22) = eq:ronsard:
  notprem.tex:385-389; (6.57)/(6.58): minarctotals.tex:1462-1488; 7.81811 assembled as
  6.11676 + 2.74107 - (3/2) log 2: minarctotals.tex:1430, 1729-1757.
- 3.35531: minarctotals.tex:1758-1767.

Confirms if: the correct AM-GM constant is 0.8102 and the printed expression is 0.4991;
(6.63)/(3.2) > 1.02 at prime q (x = 1e25, delta_0 = 2) and > 1.03 at q = 60060; with
0.8103 the ratio stays < 1 on a grid; int_1^4 G_2 dS/S > 0.37273 log 4 and the sup excess
of (5.36) is about 0.0231; the 8/5 route gives 8.21811.

Run: python3 -I eq_3_2.py

Ported from a 2026-11-06 check script.
"""
from fractions import Fraction as Fr
from math import log, sqrt, pi, gcd

X0 = 2.16e20


def C(x, t):
    return log(1 + log(4 * t) / (2 * log(9 * x ** (1 / 3) / (2.004 * t))))


def rhs63(x, q, phi, d0):
    t = d0 * q
    A = C(x, t) * (log(t) + 0.002) + log(4 * t) / 2
    B = 0.30214 * log(t) + 0.67506
    return (x / sqrt(d0 * phi) * sqrt(A * B) + 2.49157 * x / sqrt(t)
            + 2 * x / (d0 * phi) * (13 / 4 * log(t) + 7.81811)
            + 2 * x / t * (13.6516 * log(t) + 37.5415) + 3.35531 * x ** (5 / 6))


def rhs32(x, q, phi, d0, const=0.5):
    t = d0 * q
    R = 0.27125 * C(x, t) + 0.41415
    L = q / phi * (13 / 4 * log(t) + 7.82) + 13.66 * log(t) + 37.55
    return (R * log(t) + const) / sqrt(d0 * phi) * x + 2.5 * x / sqrt(t) + 2 * x / t * L + 3.36 * x ** (5 / 6)


def phi(n):
    r, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            r -= r // p
        p += 1
    if m > 1:
        r -= r // m
    return r


def isprime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


ok = []

# ---- 1. AM-GM constant in (6.77)
x1, q0 = 1e25, 2e5
rho = (C(x1, 2 * q0) * (log(2 * q0) + 0.002) + log(8 * q0) / 2) / (0.30214 * log(2 * q0) + 0.67506)
sr = sqrt(rho)
printed = 0.5 * (log(2) / sr + sr / 2 * 0.67506)
correct = log(4) / 2 / (2 * sr) + sr / 2 * 0.67506
print(f"rho = {rho:.7f} (book 3.397962), 1/(2 sqrt rho) = {1/(2*sr):.6f} (book 0.27125), "
      f"1/(4 sqrt rho)+0.30214 sqrt(rho)/2 = {1/(4*sr)+0.30214*sr/2:.6f} (book 0.4141)")
print(f"(6.77) printed constant = {printed:.6f} (book 0.49911); correct AM-GM constant = {correct:.6f}")
ok.append(abs(rho - 3.397962) < 1e-5 and abs(printed - 0.49911) < 1e-5 and abs(correct - 0.8102) < 1e-4)

# ---- 2. ratio (6.63)/(3.2)
x = 1e25
best = (0, None)
for q in range(80000, 100001):
    if isprime(q):
        r = rhs63(x, q, q - 1, 2) / rhs32(x, q, q - 1, 2)
        if r > best[0]:
            best = (r, q)
print(f"x=1e25, delta_0=2, prime q in [8e4,1e5]: max (6.63)/(3.2) = {best[0]:.5f} at q = {best[1]}")
r95 = rhs63(x, 95003, 95002, 2) / rhs32(x, 95003, 95002, 2)
print(f"  q = 95003: {r95:.6f}")
smooth = max((rhs63(10 ** e, q, phi(q), 2) / rhs32(10 ** e, q, phi(q), 2), e, q)
             for e in (23, 24, 25) for q in (30030, 60060))
print(f"q in {{30030, 60060}}, x in {{1e23,1e24,1e25}}: max ratio = {smooth[0]:.5f} (x=1e{smooth[1]}, q={smooth[2]})")
ok.append(1.025 < best[0] < 1.028 and 1.03 < smooth[0] < 1.033)
worst = 0
for e in [20.335, 21, 22, 23, 24, 25, 26, 27, 28, 30, 35, 40]:
    xx = max(10 ** e, X0)
    for k in range(400):
        q = 10 ** (k * 0.025)
        if q > xx ** (1 / 3) / 6:
            break
        for rp in (1.0, 0.5, 0.25, 1 / 2.3536, 1 / 5.2):
            ph = max(q * rp, 1)
            for d0 in (2, 2.5, 4, 10, 1000):
                if d0 * q > xx ** (1 / 3) / 3:
                    continue
                worst = max(worst, rhs63(xx, q, ph, d0) / rhs32(xx, q, ph, d0, const=0.8103))
print(f"grid max of (6.63)/(3.2 with 0.8103 for 0.5) = {worst:.5f}")
ok.append(worst < 1)

# ---- 3. (5.32) and (5.36) for v = 2, with G_2 the triple sum (5.?) computed exactly
V, M = 2, 16
mu = [1] * (M + 1)
sig = [0] * (M + 1)
for i in range(2, M + 1):
    if all(i % p for p in range(2, i)):
        for j in range(i, M + 1, i):
            mu[j] = -mu[j]
        for j in range(i * i, M + 1, i * i):
            mu[j] = 0
for d in range(1, M + 1):
    for j in range(d, M + 1, d):
        sig[j] += d
g = [Fr(0)] * (M + 1)          # g_v(m), Lemma lem:yutto
for m in range(1, M + 1):
    g[m] = g[m - 1]
    if m == 1:
        g[1] = Fr(1)
        continue
    if gcd(m, V) != 1 or mu[m] == 0:
        continue
    s = sum((Fr(mu[r], sig[r]) for r in range(1, m) if mu[r] and gcd(r, m) == 1 and gcd(r, V) == 1), Fr(0))
    g[m] += 2 * Fr(mu[m], sig[m]) * s


def Fint(y):                    # int_0^y g_v(floor w) dw
    n = int(y)
    if n == 0:
        return Fr(0)
    return sum(g[1:n], Fr(0)) + g[n] * (y - n)


def G(S):                       # (eq:grotto) exactly: sum_{s<=S,(s,v)=1} (1/s) int_{1/2}^1 g(uS/s) du
    S = Fr(S)
    tot = Fr(0)
    for s in range(1, int(S) + 1):
        if gcd(s, V) == 1:
            tot += Fint(S / s) - Fint(S / (2 * s))
    return tot / S


print(f"check G_2(3/2) = {float(G(Fr(3, 2))):.6f} vs book 1 - 1/S = {1 - 1/1.5:.6f}")
coef = []                       # on [n, n+1): G = b + a/S
for n in range(1, M):
    S1, S2, S3 = Fr(n), Fr(n) + Fr(1, 2), Fr(n) + Fr(9, 10)
    a = (G(S1) - G(S2)) / (1 / S1 - 1 / S2)
    b = G(S1) - a / S1
    assert G(S3) == b + a / S3
    coef.append((float(a), float(b)))


def intG(T):
    tot, n = 0.0, 1
    while n < T:
        a, b = coef[n - 1]
        hi = min(n + 1, T)
        tot += b * log(hi / n) + a * (1 / n - 1 / hi)
        n += 1
    return tot


I4 = intG(4)
print(f"(5.32), v=2: int_1^4 G_2 dS/S = {I4:.5f} vs 0.37273 log 4 = {0.37273*log(4):.5f}")
best = max(((4 / pi ** 2) * intG(1 + i * 0.001) - 0.15107 * log(1 + i * 0.001), 1 + i * 0.001) for i in range(15001))
print(f"(5.36), v=2: sup_T [int_1^T H_2 dS/S - 0.15107 log T] = {best[0]:.6f} at T = {best[1]:.3f}")
ok.append(I4 > 0.37273 * log(4) and 0.0228 < best[0] < 0.0233)

# ---- 4. mu-sum: (2.22) at modulus 2q gives (4/5)(2q/phi(2q)) = (8/5) q/phi(q) for odd q
c45, c85 = log(108) + 0.8, log(108) + 1.6
seven = 6.11676 + 2.74107 - 1.5 * log(2)
seven85 = 6.11676 + c85 / 2 - 1.5 * log(2)
print(f"(6.57): log 108 + 4/5 = {c45:.5f} (book 5.48214), half {c45/2:.5f} (book 2.74107); "
      f"with 8/5: half {c85/2:.5f}")
print(f"(6.63) constant: 6.11676 + 2.74107 - 1.5 log 2 = {seven:.5f} (book 7.81811); with 8/5: {seven85:.5f}")
ok.append(abs(seven - 7.81811) < 1e-5 and abs(seven85 - 8.21811) < 2e-5)

# ---- 5. roundings 2.49157 -> 2.5 and 3.35531 -> 3.36
t0 = log(X0)
low = (X0 ** (2 / 3) * (0.67845 * t0 - 1.20818) / sqrt(2) + 0.37864 * X0 ** (2 / 3)
       + (22.9812 * t0 + 411.424) * X0 ** (2 / 3)) / X0 ** (5 / 6) + 2.73908
print(f"x^(5/6) coefficient at x0 = {low:.5f} (book 3.35531)")
ok.append(abs(low - 3.35531) < 2e-5)

print("checks passed:", ok)
if all(ok):
    print("CONFIRMED: (6.77) should give 0.8102 not 0.49911, so (6.63) exceeds (3.2) by up to 2.65% "
          "(prime q) and 3.2% (q = 60060); (5.36) needs +0.0231 and the 8/5 mu-sum gives 8.21811.")
else:
    print("NOT CONFIRMED: at least one numerical part of the claim about (3.2) did not reproduce.")
