"""Check of [H, Lemma 5.1.1] (eq. (5.9), and (5.12) in its proof).

Claim: (5.9) as printed, with the l-sum starting at
min((z/y)/min(r1,r2), z/(2 r1 r2)), is false: its left side differs from the
main term (5.10) by far more than the error (5.10)/(5.11). With max in place of
min (the range of (5.8), where the lemma is applied) it holds. A misprint.

Book inputs:
  - typeII.tex:191  (5.8): max(U/min(r1,r2), (x/W)/(2 r1 r2 s)) < l <= (x/W)/(r1 r2 s).
  - typeII.tex:202-207  (5.9): min(...) < l <= z/(r1 r2), (l, r1 r2)=1, l squarefree, (l,v)=1,
    r1,r2 < y, (r1,r2)=1, (r1 r2, v)=1.
  - typeII.tex:208-215  (5.10): main term (6z/pi^2)(v/sigma(v)) sum mu mu/(sigma sigma)
    (1 - max(1/2, r1/y, r2/y)), error 5.08 zeta(3/2)^2 y sqrt z prod_{p|v}(1+1/sqrt p)(1-p^{-3/2})^2.
  - typeII.tex:216-220  (5.11): for v=2, error 1.27 zeta(3/2)^2 y sqrt z (1+1/sqrt2)(1-2^{-3/2})^2.

Confirms if, in some case, |LHS(min) - main| exceeds the lemma's error while
|LHS(max) - main| is within it, in every case tested.

Run: python3 -I lemma_5_1_1.py

Ported from a 2026-11-06 check script.
"""
import math
from fractions import Fraction as F
from math import gcd


def zeta32():
    # Euler-Maclaurin: sum_{n<N} n^-1.5 + 2/sqrt N + N^-1.5/2 + (3/24) N^-2.5
    N = 10 ** 5
    s = math.fsum(n ** -1.5 for n in range(1, N))
    return s + 2 / math.sqrt(N) + 0.5 * N ** -1.5 + 0.125 * N ** -2.5


Z32 = zeta32()


def mu_sigma(n):
    m, s, k, p = 1, 1, n, 2
    while p * p <= k:
        if k % p == 0:
            k //= p
            if k % p == 0:
                return 0, None
            m, s = -m, s * (p + 1)
        p += 1
    if k > 1:
        m, s = -m, s * (k + 1)
    return m, s


def sqfree_sieve(N):
    sf = bytearray([1]) * (N + 1)
    sf[0] = 0
    p = 2
    while p * p <= N:
        for j in range(p * p, N + 1, p * p):
            sf[j] = 0
        p += 1
    return sf


def run(v, y, z):
    y, z = F(y), int(z)
    sf = sqfree_sieve(z)
    rs = [r for r in range(1, math.ceil(y)) if r < y and gcd(r, v) == 1 and mu_sigma(r)[0] != 0]
    lhs = {"min": 0, "max": 0}
    main = 0.0
    for r1 in rs:
        m1, s1 = mu_sigma(r1)
        for r2 in rs:
            if gcd(r1, r2) != 1:
                continue
            m2, s2 = mu_sigma(r2)
            P = r1 * r2
            t1 = (F(z) / y) / min(r1, r2)
            t2 = F(z, 2 * P)
            hi = math.floor(F(z, P))
            for kind, A in (("min", min(t1, t2)), ("max", max(t1, t2))):
                cnt = sum(1 for l in range(math.floor(A) + 1, hi + 1)
                          if sf[l] and gcd(l, P * v) == 1)
                lhs[kind] += m1 * m2 * cnt
            w = 1 - max(0.5, float(F(r1) / y), float(F(r2) / y))
            main += m1 * m2 / (s1 * s2) * w
    sv = mu_sigma(v)[1]
    main *= 6 * z / math.pi ** 2 * v / sv
    prod = 1.0
    for p in (2, 3, 5, 7):
        if v % p == 0:
            prod *= (1 + 1 / math.sqrt(p)) * (1 - p ** -1.5) ** 2
    err = (1.27 if v == 2 else 5.08) * Z32 ** 2 * float(y) * math.sqrt(z) * prod
    dmin, dmax = lhs["min"] - main, lhs["max"] - main
    print(f"v={v} y={float(y)} z={z}: LHS(min, printed)={lhs['min']} LHS(max)={lhs['max']} "
          f"main={main:.3f} err={'(5.11)' if v == 2 else '(5.10)'} {err:.3f}")
    print(f"    LHS(min)-main={dmin:.3f}  LHS(max)-main={dmax:.3f}")
    return abs(dmin) > err, abs(dmax) <= err


print(f"zeta(3/2) = {Z32:.15f}")
results = [run(2, F(3, 2), 10 ** 6), run(2, F(21, 2), 2 * 10 ** 6), run(1, F(3, 2), 10 ** 6)]
min_fails = any(r[0] for r in results)
max_ok = all(r[1] for r in results)
if min_fails and max_ok:
    print("CONFIRMED: with the printed lower limit min(...) the left side of (5.9) misses the "
          "main term (5.10) by more than the allowed error, while with max(...) (the range of "
          "(5.8)) it is within the error in every case.")
else:
    print(f"NOT CONFIRMED: min version fails somewhere={min_fails}, "
          f"max version within error everywhere={max_ok}.")
