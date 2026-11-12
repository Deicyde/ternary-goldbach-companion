"""Eq 5.48 of [H] (H. A. Helfgott, The ternary Goldbach problem, arXiv:1501.05438v2).

Claim: [H] gets "(5.48) <= sum (log p)^2" from Montgomery-Vaughan's weighted large sieve
[MV73, (1.6)] with W/2 in the role of N, but in (1.6) N is an integer at least the span
p_max - p_min + 1 of the primes in (W', W], which can exceed W/2 (by 1/2); the printed
inequality still holds, because the dilated form of (1.6) with N - 1 in place of N applies
and N - 1 < W - W' <= W/2.

Book inputs (book/src/typeII.tex):
  - Lemma 5.2.2 hypotheses W >= 1, W' >= W/2, Q >= 3.5W, q*R^2 < Q (lines 954-957, 1006-1009);
  - weight (W/2 + (3/2)(1/(qrR) - 1/Q)^(-1))^(-1) in (5.47)/(5.48) (lines 1024-1042);
  - "apply the large sieve with weights [MV73,(1.6)] ... separated by at least 1/qrR - 1/Q;
    (5.48) is at most sum (log p)^2" (lines 1043-1047);
  - points alpha(m0+a) + a'/r, a = 1..q, r <= R squarefree coprime to q, (a',r) = 1 (5.46).
  MV73 (1.6): sum_r (N + (3/2) delta_r^-1)^-1 |sum_{n=M+1}^{M+N} a_n e(n x_r)|^2 <= sum |a_n|^2,
  M, N integers.

Confirms the claim if: (A) for some admissible W the span of primes in (W/2, W] exceeds
W/2, and there the literal (1.6) weight is smaller than [H]'s; (B) span - 1 < W - W' on a
grid of (W, W'); (C) in book configurations the weighted quadratic form with [H]'s weights,
and random point sets with weights (N - 1 + 1.5/delta_r)^-1, have top eigenvalue < 1.

Run: python3 -I eq_5_48.py
Ported from a 2026-11-06 check script.
"""
import cmath
import math
import random
from fractions import Fraction


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


_LIM = 20001
_SIEVE = bytearray([1]) * (_LIM + 1)
_SIEVE[0] = _SIEVE[1] = 0
for _i in range(2, int(_LIM ** 0.5) + 1):
    if _SIEVE[_i]:
        _SIEVE[_i * _i::_i] = bytearray(len(_SIEVE[_i * _i::_i]))
# smallest prime > n and largest prime <= n, for n <= _LIM
_NEXT = [0] * (_LIM + 2)
_NEXT[_LIM + 1] = 10 ** 9
for _n in range(_LIM, -1, -1):
    _NEXT[_n] = _n if _SIEVE[_n] else _NEXT[_n + 1]
_PREV = [0] * (_LIM + 1)
for _n in range(_LIM + 1):
    _PREV[_n] = _n if _SIEVE[_n] else (_PREV[_n - 1] if _n else -1)


def prime_span(lo, hi):
    """(smallest, largest) prime in (lo, hi], or None."""
    a, b = _NEXT[math.floor(lo) + 1], _PREV[math.floor(hi)]
    return (a, b) if a <= b else None


def primes_in(lo, hi):
    return [p for p in range(math.floor(lo) + 1, math.floor(hi) + 1) if _SIEVE[p]]


def squarefree(n):
    d = 2
    while d * d <= n:
        if n % (d * d) == 0:
            return False
        d += 1
    return True


def dist1(x):
    return abs(x - round(x))


def jacobi_max_eig(A):
    """Largest eigenvalue of a real symmetric matrix (cyclic Jacobi rotations)."""
    n = len(A)
    A = [row[:] for row in A]
    for _sweep in range(100):
        off = sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-22:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-300:
                    continue
                th = (A[q][q] - A[p][p]) / (2 * A[p][q])
                t = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
    return max(A[i][i] for i in range(n))


def top_eig(points, weights, support):
    """Largest eigenvalue of sum_r w_r v_r v_r^*, v_r = (e(n x_r))_n, i.e. the best constant
    in sum_r w_r |S(x_r)|^2 <= C ||a||^2 on the given support; computed from the KxK Gram
    matrix G_rs = sqrt(w_r w_s) sum_n e(n (x_s - x_r)) through its real 2Kx2K form."""
    K = len(points)
    G = [[0j] * K for _ in range(K)]
    for r in range(K):
        for s in range(K):
            d = points[s] - points[r]
            G[r][s] = math.sqrt(weights[r] * weights[s]) * sum(
                cmath.exp(2j * math.pi * n * d) for n in support)
    M = [[0.0] * (2 * K) for _ in range(2 * K)]
    for i in range(K):
        for j in range(K):
            a, b = G[i][j].real, G[i][j].imag
            M[i][j] = a
            M[i][j + K] = -b
            M[i + K][j] = b
            M[i + K][j + K] = a
    return jacobi_max_eig(M)


print("=== A: span of primes in (W/2, W] vs W/2 ===")
exceed = []
for W in [5, 13, 37, 61, 73]:
    ps = primes_in(W / 2, W)
    span = ps[-1] - ps[0] + 1
    print(f"W={W}: primes {ps[0]}..{ps[-1]}, span N={span}, W/2={W/2}, excess={span - W/2}")
    if span > W / 2:
        exceed.append(W)
maxex = max(
    (prime_span(W / 2, W)[1] - prime_span(W / 2, W)[0] + 1 - W / 2)
    for W in range(3, 20001) if prime_span(W / 2, W))
print(f"max over integer 3<=W<=20000 of span - W/2 = {maxex}")
W, Q, q, R = 13, 3.5 * 13, 1, 2
lit_smaller = False
for r in (1, 2):
    db = 1 / (q * r * R) - 1 / Q
    wH = 1 / (W / 2 + 1.5 / db)
    wlit = 1 / (7 + 1.5 / db)
    wlit_true = 1 / (7 + 1.5 / (1 / 2))
    wnm1 = 1 / (6 + 1.5 / (1 / 2))
    print(f"W=13,q=1,R=2,r={r}: delta_book={db:.6f}; [H] weight {wH:.6f}; "
          f"(1.6) with N=7: {wlit:.6f} (book delta), {wlit_true:.6f} (true delta 1/2); "
          f"N-1 form with true delta: {wnm1:.6f}")
    if wlit < wH:
        lit_smaller = True
okA = bool(exceed) and lit_smaller

print("\n=== B: span - 1 < W - W' on a grid ===")
okB = True
worst = -1e9
for i in range(2, 8001):
    W = i / 4
    for j in range(0, 9):
        Wp = W / 2 + j * (W / 2) / 16
        sp = prime_span(Wp, W)
        if not sp:
            continue
        d = (sp[1] - sp[0]) - (W - Wp)
        worst = max(worst, d)
        if d >= 0:
            okB = False
print(f"max of (span - 1) - (W - W') over grid W in [0.5, 2000], W' in [W/2, W): {worst:.4f}")

print("\n=== C1: book configurations with [H]'s weights ===")
random.seed(548)
maxe_p = 0.0
maxe_all = 0.0
minratio = 1e9
cnt = 0
for W in [13, 21, 29, 37, 61]:
    Wp = W / 2
    Q = 3.5 * W
    ps = primes_in(Wp, W)
    ints = list(range(math.floor(Wp) + 1, math.floor(W) + 1))
    for q in range(1, 8):
        for R in [2, 3]:
            if not (q * R * R < Q and R <= Wp and q < W / 2):
                continue
            for trial in range(2):
                b = random.choice([x for x in range(q) if math.gcd(x, q) == 1])
                eps = random.uniform(-1, 1) / (q * Q)
                m0 = random.randint(-50, 50)
                pts, rs, rats, ks = [], [], [], []
                for a in range(1, q + 1):
                    for r in range(1, R + 1):
                        if not squarefree(r) or math.gcd(r, q) != 1:
                            continue
                        for ap in range(r):
                            if math.gcd(ap, r) != 1 and r > 1:
                                continue
                            if r == 1 and ap != 0:
                                continue
                            rat = (Fraction(b, q) * (m0 + a) + Fraction(ap, r)) % 1
                            pts.append(float(rat) + eps * (m0 + a))
                            rs.append(r)
                            rats.append(rat)
                            ks.append(m0 + a)
                dbook = [1 / (q * r * R) - 1 / Q for r in rs]
                for i in range(len(pts)):
                    da = min(dist1(float(rats[i] - rats[j]) + eps * (ks[i] - ks[j]))
                             for j in range(len(pts)) if j != i)
                    minratio = min(minratio, da / dbook[i])
                wH = [1 / (W / 2 + 1.5 / d) for d in dbook]
                maxe_p = max(maxe_p, top_eig(pts, wH, ps))
                maxe_all = max(maxe_all, top_eig(pts, wH, ints))
                cnt += 1
print(f"{cnt} configurations; min actual/book separation = {minratio:.5f}")
print(f"top eigenvalue with [H]'s weights: primes {maxe_p:.4f}, all integers of (W/2,W] {maxe_all:.4f}")
okC1 = minratio >= 1 and maxe_p < 1 and maxe_all < 1

print("\n=== C2: random point sets, weights (N - 1 + 1.5/delta_r)^-1 ===")
random.seed(1)
worst = 0.0
for trial in range(400):
    K = random.randint(2, 12)
    if random.random() < 0.5:
        pts = [random.random() for _ in range(K)]
    else:
        pts = [((i + random.uniform(-0.1, 0.1)) / K) % 1 for i in range(K)]
    deltas = [min(dist1(pts[i] - pts[j]) for j in range(K) if j != i) for i in range(K)]
    if min(deltas) < 1e-4:
        continue
    N = random.randint(1, 30)
    w = [1 / (N - 1 + 1.5 / d) for d in deltas]
    worst = max(worst, top_eig(pts, w, list(range(1, N + 1))))
print(f"max top eigenvalue = {worst:.4f}")
okC2 = worst < 1

if okA and okB and okC1 and okC2:
    print("CONFIRMED: the span of primes in (W/2,W] can exceed W/2 (W=13: 7 > 6.5), so the literal "
          "MV (1.6) does not give [H]'s weights, but the N-1 (dilated) form does since span-1 < W-W' <= W/2.")
else:
    print(f"NOT CONFIRMED: checks A={okA} B={okB} C1={okC1} C2={okC2} did not all pass.")
