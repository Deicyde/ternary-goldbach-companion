"""Check of [H, Eq (4.55)] (eq:etoile, proof of Lemma 4.2.4).

Claim: the last '<=' of (4.55) is false: it needs
sum_{p^a<=V, p odd, p|q} (log p) p^a <= V log q, but that sum can approach
(3/2) V log q, so the provable last term is (3/2)(U+1)^2 V log q/4. The
double sum of (4.54) still stays below the printed final line. Side typo:
the estimate before (4.55), 'sum_{u<=R, u odd, q|u} <= R^2/4q + 3R/4', omits
the summand u (with u it is true).

Book inputs:
  - typeI.tex:1650-1662  (4.55): first, middle and final lines, c_4 = 1.03884.
  - typeI.tex:1640-1645  (4.54) double sum: u<=U, v<=V, uv odd, uv<=M, q|uv,
    u squarefree, Lambda(v) u v.
  - typeI.tex:1647  the estimate for sum_{u<=R, u odd, q|u}.
  - typeI.tex:1496-1507  hypotheses of Lemma 4.2.4: |delta/x| <= 1/qQ_0,
    q <= Q_0, Q_0 >= max(2e, 2 sqrt x), UV + (19/18)Q_0 <= x/5.6;
    typeI.tex:1569 M = min(UV, Q/2); typeI.tex:656 Q = floor(x/|delta q|)
    (applied to 2 alpha, typeI.tex:1561-1563).

Confirms if: (a) the isolated inequality fails (q=3, V=9 and V=243);
(b) at an admissible instance (x=140600, Q_0=2 sqrt x, q=3, |delta|q=x/Q_0,
U=100, V=243) the middle line exceeds the final line; (c) the middle line is
at most the final line with the factor 3/2 on its last term; (d) the (4.54)
double sum is below the printed final line at that instance and over a small
scan of (q, U, V, M) with q <= M <= UV; (e) the estimate with summand u holds for odd q.

Run: python3 -I eq_4_55.py

Ported from a 2026-11-06 check script.
"""
import math

C4 = 1.03884
NMAX = 4000
LAMP = [0] * (NMAX + 1)  # p if n = p^k (k >= 1)
for p in range(2, NMAX + 1):
    if all(p % d for d in range(2, int(p ** 0.5) + 1)):
        pk = p
        while pk <= NMAX:
            LAMP[pk] = p
            pk *= p
SQF = bytearray([1]) * (NMAX + 1)
for d in range(2, int(NMAX ** 0.5) + 1):
    SQF[d * d::d * d] = bytearray(len(SQF[d * d::d * d]))


def lam(v):
    return math.log(LAMP[v]) if LAMP[v] else 0.0


def odd_mult_sum(R, d):
    """sum of u <= R, u odd, d | u (d odd)."""
    K = math.floor(R / d + 1e-12)
    m = (K + 1) // 2
    return d * m * m


def lines(q, U, V, M):
    a1 = sum(lam(v) * v * odd_mult_sum(min(U, M / v), q) for v in range(3, V + 1) if LAMP[v] and math.gcd(v, 2 * q) == 1)
    b1 = sum(math.log(LAMP[v]) * v * odd_mult_sum(U, q // math.gcd(q, v))
             for v in range(3, V + 1) if LAMP[v] and LAMP[v] % 2 and q % LAMP[v] == 0)
    a2 = sum(lam(v) * v * ((M / v) ** 2 / (4 * q) + 3 * M / (4 * v))
             for v in range(3, V + 1) if LAMP[v] and math.gcd(v, 2 * q) == 1)
    b2 = sum(math.log(LAMP[v]) * v * (U + 1) ** 2 / 4
             for v in range(3, V + 1) if LAMP[v] and LAMP[v] % 2 and q % LAMP[v] == 0)
    t = (M * M * math.log(V) / (4 * q), 3 * C4 / 4 * M * V, (U + 1) ** 2 / 4 * V * math.log(q))
    return a1 + b1, a2 + b2, t


def double_sum(q, U, V, M):
    s = 0.0
    for v in range(3, V + 1, 2):
        if not LAMP[v]:
            continue
        for u in range(1, min(U, math.floor(M / v + 1e-12)) + 1, 2):
            if SQF[u] and (u * v) % q == 0:
                s += lam(v) * u * v
    return s


def pp_sum(q, V):
    return sum(math.log(LAMP[v]) * v for v in range(3, V + 1) if LAMP[v] and LAMP[v] % 2 and q % LAMP[v] == 0)


ok = True
print("(a) sum_{p^a<=V, p odd, p|q} (log p) p^a vs V log q")
fails = 0
for q, V in ((3, 9), (3, 243), (3, 2187), (5, 25), (9, 81)):
    l = pp_sum(q, V)
    print(f"   q={q} V={V}: {l:.5f} vs {V*math.log(q):.5f}  ratio {l/(V*math.log(q)):.6f} (<= 1.5: {l <= 1.5*V*math.log(q)})")
    fails += l > V * math.log(q)
ok &= fails > 0

print("\n(b)-(d) admissible instance")
x, q, U, V = 140600, 3, 100, 243
Q0 = 2 * math.sqrt(x)
dq = x / Q0                      # |delta| q, so |delta/x| = 1/(q Q0)
Q = math.isqrt(4 * x)            # floor(x/|delta q|) = floor(2 sqrt x), exact
M = min(U * V, Q / 2)
hyp = (U * V + 19 / 18 * Q0 <= x / 5.6) and q <= Q0 and Q0 >= max(2 * math.e, 2 * math.sqrt(x))
print(f"   Q0={Q0:.4f}, Q={Q}, M={M}, |delta|={dq/q:.4f}; UV+(19/18)Q0={U*V+19/18*Q0:.2f} <= x/5.6={x/5.6:.2f}; hyps: {hyp}")
L1, L2, t = lines(q, U, V, M)
L3 = sum(t)
L3c = t[0] + t[1] + 1.5 * t[2]
S = double_sum(q, U, V, M)
print(f"   first line {L1:.6g}, middle {L2:.6g}, final {L3:.6g} (= {t[0]:.6g} + {t[1]:.6g} + {t[2]:.6g})")
print(f"   middle/final = {L2/L3:.4f}, first/final = {L1/L3:.4f}; final with 3/2: {L3c:.6g}; (4.54) double sum = {S:.6g}")
ok &= hyp and L2 > L3 and L1 <= L2 and L2 <= L3c and S <= L3

# small admissible scan of the double sum against the printed final line
worst, warg, n = 0.0, None, 0
for q in (3, 5, 7, 9, 15, 19, 21, 45):
    for U in (q, 2 * q, 10, 40, 100):
        for V in (q, 9, 27, 50, 120, 243):
            for M in sorted({U * V, (U * V) // 2, max(q, (U * V) // 5)}):
                if M < q or M > U * V:
                    continue
                _, _, t = lines(q, U, V, M)
                r = double_sum(q, U, V, M) / sum(t)
                n += 1
                if r > worst:
                    worst, warg = r, (q, U, V, M)
print(f"   scan: {n} cases (q,U,V,M), q<=M<=UV, max (4.54)/final = {worst:.4f} at {warg}")
ok &= worst <= 1

print("\n(e) sum_{u<=R, u odd, q|u} u <= R^2/4q + 3R/4 for odd q < 100, R <= 600")
bad = 0
for q in range(1, 100, 2):
    for R in range(1, 601):
        if odd_mult_sum(R, q) > R * R / (4 * q) + 3 * R / 4 + 1e-9:
            bad += 1
print("   violations:", bad)
ok &= bad == 0

if ok:
    print(f"CONFIRMED: the last '<=' of (4.55) fails (middle line {L2:.4g} > final line {L3:.4g} at an admissible instance) because sum (log p)p^a can exceed V log q (ratio up to 3/2); with the factor 3/2 it holds, and the (4.54) double sum stays below the printed final line.")
else:
    print("NOT CONFIRMED: some part of the (4.55) claim did not reproduce.")
