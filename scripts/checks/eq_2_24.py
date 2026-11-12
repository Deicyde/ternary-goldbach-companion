"""Check of the remark after [H] Eq (2.24): |sum_{n<=x} mu(n)/n| <= 1/(2 sqrt x) fails at x = 7727068587.

Item: Eq 2.24 (book/src/notprem.tex:400-402; the remark is at notprem.tex:410-412).
Claim: the remark says |m(x)| <= 1/(2 sqrt x), m(x) = sum_{n<=x} mu(n)/n, holds for all
3 <= x <= 7727068587 and fails at x = 7727068588 - eps; in fact it already fails at
x = T = 7727068587 (mu(T) = +1), so the printed range is false at its right endpoint.

Book input: notprem.tex:410-412, "the stronger bound |sum_{n<=x} mu(n)/n| <= 1/(2 sqrt x) holds for
all 3 <= x <= 7727068587, but not for x = 7727068588 - eps".

Method.
  1. Factor T by trial division and compute mu(T).
  2. Compute m(T) by the recursion sum_{k<=v} m(v/k)/k = 1, i.e.
       m(v) = 1 - sum_{2<=d<=sqrt v} m(floor(v/d))/d - sum_{w<sqrt v} m(w) (H(b_w) - H(a_w)),
     with m(w) for w <= Y taken from a Moebius sieve to Y (exact fixed-point prefix sums
     sum mu(n) floor(2^100/n)), and harmonic differences by Euler-Maclaurin (a >= sqrt Y).
     Sums are formed with math.fsum. The recursion is validated against the direct sieve
     value at x = Y, and m(T) is computed with two different Y; the two must agree far inside
     the margin m(T) - 1/(2 sqrt T) (about 4.6e-11).
  3. Since m is constant on [T, T+1), the bound fails at x = T iff m(T) > 1/(2 sqrt T).

Confirms the claim if: mu(T) = +1 and m(T) - 1/(2 sqrt T) exceeds 1000 times the observed
discrepancy between the independent evaluations (and also m(T-1) = m(T) - 1/T satisfies the bound).
The script does not rescan 3 <= x < T.

Run: python3 -I eq_2_24.py        (about 15 s)

Ported from a 2026-11-06 check script.
"""
import math
import time
from array import array

T = 7727068587
t0 = time.time()


def factor(n):
    f, d = [], 2
    while d * d <= n:
        while n % d == 0:
            f.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f.append(n)
    return f


fT = factor(T)
muT = 0 if len(set(fT)) < len(fT) else (-1) ** len(fT)
print(f"T = {T} = {' * '.join(map(str, fT))}, mu(T) = {muT}")

Y = 10 ** 7
# Moebius sieve to Y
mu = bytearray([1]) * (Y + 1)  # parity of #prime factors: 1 = even, 0 = odd (we flip)
sqf = bytearray([1]) * (Y + 1)
comp = bytearray(Y + 1)
for p in range(2, Y + 1):
    if comp[p]:
        continue
    if p <= Y // p:
        comp[p * p::p] = b"\x01" * len(range(p * p, Y + 1, p))
        sqf[p * p::p * p] = bytes(len(range(p * p, Y + 1, p * p)))
    for m in range(p, Y + 1, p):
        mu[m] ^= 1
print(f"sieve to Y = {Y} done ({time.time() - t0:.0f} s)")

TWO100 = 1 << 100
mt = array("d", [0.0]) * (Y + 1)
S = 0
M = 0
for n in range(1, Y + 1):
    if sqf[n]:
        if mu[n]:
            S += TWO100 // n
            M += 1
        else:
            S -= TWO100 // n
            M -= 1
    mt[n] = S / TWO100
del mu, sqf, comp
print(f"prefix sums done ({time.time() - t0:.0f} s); M(10^7) = {M} (known value 1037)  m(10^7) = {mt[Y]:.15e}")


def dH(a, b):
    """H(b) - H(a), a large."""
    A, B, D = float(a), float(b), float(b - a)
    return (math.log1p(D / A) - D / (2 * A * B) + D * (A + B) / (12 * A * A * B * B)
            - D * (A + B) * (A * A + B * B) / (120 * A ** 4 * B ** 4))


def m_rec(x, Yu):
    """m(x) by the recursion, using mt[w] for w <= Yu."""
    assert Yu * Yu >= x and Yu <= Y
    K = x // (Yu + 1)
    big = [0.0] * (K + 2)
    for k in range(K, 0, -1):
        v = x // k
        Dd = math.isqrt(v)
        terms = [1.0]
        for d in range(2, Dd + 1):
            w = v // d
            terms.append(-(mt[w] if w <= Yu else big[k * d]) / d)
        for w in range(1, v // (Dd + 1) + 1):
            b, a = v // w, max(v // (w + 1), Dd)
            if b > a:
                terms.append(-mt[w] * dH(a, b))
        big[k] = math.fsum(terms)
    return big[1]


# validation of the recursion against the direct sieve
for xv, Yv in ((Y, 10 ** 5), (Y, 10 ** 6)):
    r = m_rec(xv, Yv)
    print(f"validation: recursion m({xv}) with Y={Yv}: {r:.15e}, sieve {mt[xv]:.15e}, diff {r - mt[xv]:.2e}")
val_diff = max(abs(m_rec(Y, Yv) - mt[Y]) for Yv in (10 ** 5, 10 ** 6))

vals = {}
for Yv in (5 * 10 ** 6, 10 ** 7):
    vals[Yv] = m_rec(T, Yv)
    print(f"m(T) with Y = {Yv}: {vals[Yv]:.15e}  ({time.time() - t0:.0f} s)")
mT = vals[10 ** 7]
disc = max(abs(vals[5 * 10 ** 6] - mT), val_diff, 1e-15)
half = 1 / (2 * math.sqrt(T))
gap = mT - half
mT1 = mT - muT / T
print(f"1/(2 sqrt T) = {half:.15e}")
print(f"m(T) - 1/(2 sqrt T) = {gap:.6e};  2 sqrt(T) m(T) = {2 * math.sqrt(T) * mT:.8f}")
print(f"m(T-1) = m(T) - mu(T)/T = {mT1:.15e};  2 sqrt(T) m(T-1) = {2 * math.sqrt(T) * mT1:.8f}")
print(f"largest discrepancy between independent evaluations: {disc:.2e}")
print(f"time {time.time() - t0:.0f} s")

if muT == 1 and gap > 1000 * disc and abs(mT1) < half:
    print(f"CONFIRMED: m(7727068587) = {mT:.10e} exceeds 1/(2 sqrt T) = {half:.10e} by {gap:.3e}, so the remark's "
          f"bound already fails at its endpoint x = 7727068587 (mu(T) = +1), not first at 7727068588 - eps.")
else:
    print(f"NOT CONFIRMED: mu(T) = {muT}, m(T) - 1/(2 sqrt T) = {gap:.3e}, discrepancy {disc:.2e}.")
