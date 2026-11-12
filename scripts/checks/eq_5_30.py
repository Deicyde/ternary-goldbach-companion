"""Check of [H, (5.30)] (Euler-Maclaurin error in the coefficient of g_v(m)).

Item: Eq 5.30 (typeII.tex:677-683, odd-n display typeII.tex:684-695).

Claim: the error chain in (5.30) is garbled (f'(3/2m), f'(s/(m+1)), (2m/s)^2,
((m+1)/s)^2 should have S), and the step (1/12) int|f''| =
(1/6)(|f'(S/2m)| + |f'(S/(m+1))|) is wrong: f' has total variation
6(m+1)^2/S^2 and |f'(S/2m-)| = 2m^2/S^2, so the book's own method gives
(m+1)^2/(2S^2) (all n) or (m+1)^2/S^2 (odd n); this is at most the printed
(5m^2+2m+1)/(6S^2) (resp. /(3S^2)) for m >= 3 but not for m = 1, 2, where the
printed bound nevertheless holds numerically for S >= 10^4.

Book inputs: the piecewise f of typeII.tex:672-676 (f = 1/S on (S/2m, S/(m+1)],
1/t - m/S on (S/(m+1), S/m], (m+1)/S - 1/2t on (S/2(m+1), S/2m], 0 elsewhere);
(5.30) eq:etex at typeII.tex:677-683 and its odd-n analogue at 684-695;
the printed error c_{v,0}(5m^2+2m+1)/S^2 with c_{1,0}=1/6, c_{2,0}=1/3
(typeII.tex:711-713, 733-735), used for m <= C_0 = 10000 and S >= 100000
(typeII.tex:770-782).

Part 1 (exact rationals, S = 1 scaling): total variation of f', one-sided
values, the method's bound vs the printed bound for m = 1..60.
Part 2 (50-digit Decimal): Q(S) = S^2 (sum_{(n,v)=1} f(n) - L) with
L = (phi(v)/2v) log(1+1/m), for m = 1, 2, v = 1, 2, at every unit piece of S
in [10^4, 10^6) (on each piece sum f(n) = K1 + K2/S exactly, so |Q| is
maximal at an endpoint or the vertex), plus a brute-force cross-check.

Confirms the claim if: TV = 6(m+1)^2 and |f'(S/2m-)| = 2m^2 for all m tested,
the method bound exceeds the printed one exactly for m in {1, 2}, and the
scanned max |Q| stays below the printed constant for m = 1, 2, v = 1, 2.

Run: python3 -I eq_5_30.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as D, getcontext
from fractions import Fraction as Fr

getcontext().prec = 50

# ---------------- Part 1: exact total variation ----------------


def bps(m):
    return Fr(1, 2 * (m + 1)), Fr(1, 2 * m), Fr(1, m + 1), Fr(1, m)


def fp(t, m, side):
    """one-sided derivative of F (S = 1 version of f); side=-1 left, +1 right"""
    a1, a2, a3, a4 = bps(m)

    def inside(lo, hi):
        return (lo < t <= hi) if side < 0 else (lo <= t < hi)
    if inside(a1, a2):
        return 1 / (2 * t * t)
    if inside(a2, a3):
        return Fr(0)
    if inside(a3, a4):
        return -1 / (t * t)
    return Fr(0)


def F(t, m):
    a1, a2, a3, a4 = bps(m)
    if a1 < t <= a2:
        return (m + 1) - 1 / (2 * t)
    if a2 < t <= a3:
        return Fr(1)
    if a3 < t <= a4:
        return 1 / t - m
    return Fr(0)


ok_part1 = True
fail_ms = []
print("Part 1: exact values in units of 1/S^2")
for m in range(1, 61):
    a1, a2, a3, a4 = bps(m)
    pts = sorted({a1, a2, a3, a4})
    # F continuous, so int|f''| = TV(f') = sum|jumps| + variation on monotone pieces
    eps = Fr(1, 10**40)
    for a in pts:
        assert abs(F(a, m) - F(a + eps, m)) < Fr(1, 10**30)
    jumps = sum(abs(fp(a, m, +1) - fp(a, m, -1)) for a in pts)
    mono = abs(fp(a1, m, +1) - fp(a2, m, -1)) + (abs(fp(a3, m, +1) - fp(a4, m, -1)) if a3 < a4 else 0)
    TV = jumps + mono
    if TV != 6 * (m + 1) ** 2:
        ok_part1 = False
    if fp(a2, m, -1) != 2 * m * m:
        ok_part1 = False
    method1 = TV / 12          # |B_2/2| <= 1/12, all n
    method2 = TV / 6           # odd n
    printed1 = Fr(5 * m * m + 2 * m + 1, 6)
    printed2 = Fr(5 * m * m + 2 * m + 1, 3)
    book_step = Fr(1, 6) * (fp(a2, m, -1) + abs(fp(a3, m, +1)))
    if method1 > printed1 or method2 > printed2:
        fail_ms.append(m)
    if m <= 4:
        print(f" m={m}: TV(f')={TV} (6(m+1)^2={6*(m+1)**2}); |f'(S/2m-)|={fp(a2,m,-1)} vs (2m)^2={(2*m)**2};"
              f" book step (1/6)(|f'(S/2m-)|+|f'(S/(m+1)+)|)={book_step} vs (1/12)TV={method1}")
        print(f"       all n: method {method1} vs printed {printed1};  odd n: method {method2} vs printed {printed2}")
print(f" m in 1..60 where the method's bound exceeds the printed bound: {fail_ms}")
ok_part1 = ok_part1 and fail_ms == [1, 2]

# ---------------- Part 2: numerical scan for m = 1, 2 ----------------


def brute(m, v, S):
    S = D(S)
    tot = D(0)
    n = 1
    while n <= S / m:
        if v == 1 or n % 2 == 1:
            t = D(n)
            if S / (2 * (m + 1)) < t <= S / (2 * m):
                tot += D(m + 1) / S - 1 / (2 * t)
            elif S / (2 * m) < t <= S / (m + 1):
                tot += 1 / S
            elif S / (m + 1) < t <= S / m:
                tot += 1 / t - D(m) / S
        n += 1
    return tot


def scan(m, v, N0, N1, checkpoints=()):
    ks = [m, m + 1, 2 * m, 2 * (m + 1)]
    L = (D(m + 1) / D(m)).ln() / (2 if v == 1 else 4)
    ok = (lambda n: True) if v == 1 else (lambda n: n % 2 == 1)

    def count(a, b):
        return b - a if v == 1 else (b + 1) // 2 - (a + 1) // 2

    def idx(S0, k):  # floor(S/k) for S in (S0, S0+1)
        return (2 * S0 + 1) // (2 * k)
    a = {k: idx(N0, k) for k in ks}
    H = {}
    for k in ks:
        H[k] = sum((D(1) / n for n in range(1, a[k] + 1) if ok(n)), D(0))
    printed = D(5 * m * m + 2 * m + 1) / (6 if v == 1 else 3)
    best, arg, nviol = D(0), None, 0
    for S0 in range(N0, N1):
        for k in ks:
            na = idx(S0, k)
            while a[k] < na:
                a[k] += 1
                if ok(a[k]):
                    H[k] += D(1) / a[k]
        A1, A2, A3, A4 = a[2 * (m + 1)], a[2 * m], a[m + 1], a[m]
        K1 = (H[m] - H[m + 1]) - (H[2 * m] - H[2 * (m + 1)]) / 2
        K2 = (m + 1) * count(A1, A2) + count(A2, A3) - m * count(A3, A4)
        c2 = K1 - L
        cands = [D(S0), D(S0 + 1)]
        if c2 != 0:
            Sv = -D(K2) / (2 * c2)
            if D(S0) < Sv < D(S0 + 1):
                cands.append(Sv)
        if S0 in checkpoints:
            Sx = D(S0) + D("0.37")
            direct = (brute(m, v, Sx) - L) * Sx * Sx
            piece = c2 * Sx * Sx + K2 * Sx
            assert abs(direct - piece) < D(10) ** -30, (m, v, S0, direct, piece)
        for S in cands:
            Q = abs(c2 * S * S + K2 * S)
            if Q > best:
                best, arg = Q, S
            if Q > printed:
                nviol += 1
    return best, arg, printed, nviol


N0, N1 = 10**4, 10**6
ok_part2 = True
print(f"Part 2: max over S in [{N0}, {N1}) of S^2 |sum_(n,v)=1 f(n) - (phi(v)/2v) log(1+1/m)|")
for m in (1, 2):
    for v in (1, 2):
        best, arg, printed, nviol = scan(m, v, N0, N1, checkpoints=(N0, N0 + 7, 54321))
        print(f" m={m} v={v}: max = {best:.10f} at S = {arg:.4f}; printed c_v0(5m^2+2m+1) = {printed:.6f};"
              f" pieces exceeding printed: {nviol}")
        if nviol or best > printed:
            ok_part2 = False

if ok_part1 and ok_part2:
    print("CONFIRMED: (5.30) misprints S as s/3 and bounds the variation of f' wrongly; the book's own method "
          "gives (m+1)^2/(2S^2) (odd n: (m+1)^2/S^2), which proves the printed bound only for m >= 3, "
          "while for m = 1, 2 the printed bound holds numerically for 10^4 <= S < 10^6.")
else:
    print(f"NOT CONFIRMED: exact part ok={ok_part1}, numerical part ok={ok_part2}.")
