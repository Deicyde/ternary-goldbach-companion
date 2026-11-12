"""Eq (6.25) of [H] (arXiv:1501.05438v2): the main integral bound is false.

Claim: (6.25), int_1^{x/UW_0} (beta + beta^-1 2H_2(s))/2 ds/s <= (beta/2 + kappa_6/(4 beta)) log(x/UW_0),
is equivalent to (5.36) at T = x/UW_0, and (5.36) is false: the left side exceeds the right by
E(T)/beta with E(T) > 0 for T > 3.37 and E(T) = 0.02305 for T >= 16.

Book inputs:
  - the triple sum (5.28) (typeII.tex l. 647-648) with g_2 from the lemma at l. 393-398;
    G_2 is an upper bound for it, "<= G_v(S)" (l. 789-791); (5.32) (l. 803-806);
    H_2 = (4/pi^2) G_2 on [1,16), 0.15107 on [16, oo) ((5.35), l. 823-829);
    (5.36): int_1^T H_2(S) dS/S <= 0.15107 log T (l. 831-835).
  Since G_2 >= T_2 (the exact triple sum), int_1^T H_2 dS/S >= (4/pi^2) int_1^T T_2 dS/S
  (T <= 16), so E(T) below is a lower bound for the true excess over 0.15107 log T.
  - (6.25) and kappa_6 = 0.60428 (minarctotals.tex l. 679-686); first choice (6.49):
    x/UV = 2 sqrt(q delta_0) <= 2 sqrt(2y) (l. 1286-1298), W_0 = V there (l. 1327-1330).

Computed: E(T) exactly (piecewise rational T_2, 50-digit logs), its sign change, its value for
T >= 16, and LHS - RHS of (6.25) at beta = 1 for several T.

Confirms: E(T) > 0 on (3.37, oo) and the first-choice range of T reaches past 3.37.

Run: python3 -I eq_6_25.py

Ported from a 2026-11-06 check script.
"""
from fractions import Fraction as F
from decimal import Decimal as D, getcontext
from math import gcd

getcontext().prec = 50
PI = D("3.14159265358979323846264338327950288419716939937510")
C4PI2 = D(4) / (PI * PI)
C532 = D("0.37273")   # (5.32), v = 2
C536 = D("0.15107")   # (5.36), v = 2; H_2 = 0.15107 for S >= 16 ((5.35))
KAPPA6 = D("0.60428")
KAPPA7 = D("0.1281")
NMAX = 16


def mu(n):
    r, m, p = 1, n, 2
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            r = -r
        p += 1
    return -r if m > 1 else r


def sigma(n):
    return sum(d for d in range(1, n + 1) if n % d == 0)


def g2(n):
    """g_2(n) of the lemma at typeII.tex l. 393-398, exact; r1, r2 odd, coprime, squarefree."""
    tot = F(0)
    for r1 in range(1, n + 1, 2):
        for r2 in range(1, n + 1, 2):
            if gcd(r1, r2) == 1 and mu(r1) and mu(r2):
                tot += F(mu(r1) * mu(r2), sigma(r1) * sigma(r2))
    return tot


G2V = [F(0)] + [g2(n) for n in range(1, NMAX + 1)]


def T2(S):
    """the triple sum (5.28) (typeII.tex l. 647-648), v = 2: sum_{s<=S, s odd} (1/s) int_{1/2}^1 g_2(floor(uS/s)) du, S rational."""
    S = F(S)
    tot = F(0)
    for s in range(1, int(S) + 1, 2):
        integ = F(0)
        for m in range(1, int(S / s) + 1):
            lo = max(F(1, 2), F(m * s) / S)
            hi = min(F(1), F((m + 1) * s) / S)
            if hi > lo:
                integ += G2V[m] * (hi - lo)
        tot += integ / s
    return tot


def coeffs(n):
    """on (n, n+1), T_2(S) = a + b/S exactly; solved from two points, verified at a third."""
    s1, s2, s3 = F(n) + F(1, 3), F(n) + F(2, 3), F(n) + F(1, 7)
    t1, t2 = T2(s1), T2(s2)
    b = (t1 - t2) / (1 / s1 - 1 / s2)
    a = t1 - b / s1
    assert a + b / s3 == T2(s3)
    return a, b


CO = {n: coeffs(n) for n in range(1, 16)}


def dq(fr):
    return D(fr.numerator) / D(fr.denominator)


def intT2(T):
    """int_1^T T_2(S) dS/S for 1 <= T <= 16 (exact pieces, 50-digit logs)."""
    T = D(T)
    tot = D(0)
    n = 1
    while n < T and n < 16:
        hi = min(T, D(n + 1))
        a, b = CO[n]
        tot += dq(a) * (hi.ln() - D(n).ln()) + dq(b) * (D(1) / n - 1 / hi)
        n += 1
    return tot


def intH2_low(T):
    """lower bound for int_1^T H_2(S) dS/S: H_2 = (4/pi^2) G_2 >= (4/pi^2) T_2 on [1,16), = 0.15107 beyond."""
    T = D(T)
    if T <= 16:
        return C4PI2 * intT2(T)
    return C4PI2 * intT2(16) + C536 * (T.ln() - D(16).ln())


def E(T):
    """E(T) = (lower bound for) int_1^T H_2 dS/S - 0.15107 log T."""
    return intH2_low(T) - C536 * D(T).ln()


def core_report():
    print("g_2(1..8) =", [str(G2V[n]) for n in range(1, 9)])
    for n in range(1, 4):
        a, b = CO[n]
        print(f"T_2(S) on [{n},{n+1}) = {a} + ({b})/S")
    minT = min(min(dq(a + b / n), dq(a + b / (n + 1))) for n, (a, b) in CO.items())
    print("min of T_2 at the ends of the pieces of [1,16):", round(float(minT), 6))
    i4 = intT2(4)
    print(f"int_1^4 T_2 dS/S = {float(i4):.6f}  vs 0.37273 log 4 = {float(C532 * D(4).ln()):.6f}")
    print(f"int_1^4 H_2 dS/S >= {float(C4PI2 * i4):.6f}  vs 0.15107 log 4 = {float(C536 * D(4).ln()):.6f}")
    print(f"(4/pi^2) * 0.37273 = {float(C4PI2 * C532):.7f};  kappa_6 = 0.60428 = 4 * 0.15107: {KAPPA6 == 4 * C536}")
    for t in ["2", "3", "3.3", "3.4", "4", "8", "15.58", "16", "100", "1e6"]:
        print(f"   E({t}) = {float(E(t)):+.6f}")
    lo, hi = D(3), D(4)
    for _ in range(60):
        mid = (lo + hi) / 2
        if E(mid) > 0:
            hi = mid
        else:
            lo = mid
    pos = all(E(D("3.37") + D(k) / 100) > 0 for k in range(0, 1264))
    sup = max(E(D(1) + D(k) / 100) for k in range(0, 1501))
    e16 = E(16)
    print(f"E changes sign at T = {float(lo):.5f}; E > 0 on the grid [3.37, 16]: {pos}; "
          f"max on grid [1,16] = {float(sup):.6f}; E(T) = E(16) = {float(e16):.6f} for T >= 16")
    return dict(cross=lo, pos=pos, e16=e16, sup=sup)

def sigma_chain():
    """Lemma 5.2.2 proof (typeII.tex l. 1057-1069): weight bound needs 3 sigma/(1 - sigma W/Q) < 1."""
    s = 1 / (2 * D("0.50136").exp())
    c35 = 3 * s / (1 - s / D("3.5"))
    c1 = 3 * s / (1 - s)
    need = s / (1 - 3 * s)
    print(f"sigma = {float(s):.7f}; chain coefficient 3s/(1 - s W/Q): W/Q = 1/3.5 -> {float(c35):.6f}, "
          f"W/Q = 1 -> {float(c1):.6f}; the step needs Q/W >= s/(1-3s) = {float(need):.5f}")
    return c35 < 1, c1 > 1


def params_report():
    x = D("2.16e20")
    x13 = x ** (D(1) / 3)
    # first choice (6.49): Q = (3/4) x^{2/3}, U = x^{2/3}/(9 sqrt(q delta_0)), q delta_0 <= 2y = x^{1/3}/3
    r1 = D("0.75") * D(3).sqrt() / D("31.5") * x ** (D(1) / 6)
    print(f"first choice (6.49) at x0: Q/(3.5 x/U) >= 0.75 sqrt3/31.5 x^(1/6) = {float(r1):.3f}")
    # second choice (6.65): U = 500 sqrt6 x^{1/3}, Q = x/U; theta = 4, case (a) y < q <= x/8U, W in [8q, x/U]
    U = 500 * D(6).sqrt() * x13
    Q = x / U
    y = x13 / 6
    print(f"second choice (6.65) at x0: U = {float(U):.5g}, Q = x/U = {float(Q):.5g}, Q/(3.5 x/U) = {float(Q/(D('3.5')*x/U)):.4f}")
    print(f"   Q >= 3.5W fails for W in (x/3.5U, x/U] = ({float(x/(D('3.5')*U)):.5g}, {float(x/U):.5g}];"
          f" case (a) q in ({float(y):.4g}, {float(x/(8*U)):.5g}], W_0 = 8q;"
          f" for q > x/28U = {float(x/(28*U)):.4g} all of [W_0, x/U] violates it")
    return r1 >= 100, Q < D("3.5") * (x / U), D(8) * y < x / U

def opt_report(label, Lams, Phi=D(0)):
    """min_beta [beta (L+Phi)/2 + beta^-1 (kappa_6 L/4 + kappa_7/2 + E)] = sqrt((L+Phi)(kappa_6 L + 2kappa_7 + 4E))/sqrt2."""
    worse = True
    for L in Lams:
        T = L.exp()
        e = E(T)
        f_pr = KAPPA6 * L + 2 * KAPPA7
        f_co = f_pr + 4 * e
        print(f"   {label}: log T = {float(L):.3f} (T = {float(T):.4g}), E = {float(e):+.6f}: second factor printed {float(f_pr):.4f}, "
              f"needed {float(f_co):.4f} (+{float(100*(f_co/f_pr-1)):.2f}%)")
        if T > 4:
            worse = worse and f_co > f_pr
    return worse

r = core_report()
x = D("2.16e20"); y = x ** (D(1) / 3) / 6
Tmax = 2 * (2 * y).sqrt()
print(f"first choice: T = x/UV = 2 sqrt(q delta_0) in [2 sqrt 2, 2 sqrt(2y)] = [{float(2*D(2).sqrt()):.4f}, {float(Tmax):.1f}] at x0")
for T in ["4", "16", "100"]:
    beta = D(1)
    lhs = beta / 2 * D(T).ln() + intH2_low(T) / beta
    rhs = (beta / 2 + KAPPA6 / (4 * beta)) * D(T).ln()
    print(f"   T = {T}, beta = 1: LHS(6.25) >= {float(lhs):.6f} > RHS {float(rhs):.6f}: {lhs > rhs}  (diff {float(lhs-rhs):.6f})")
if r["pos"] and r["e16"] > 0 and Tmax > 16:
    print(f"CONFIRMED: (6.25) fails for every x/UW_0 > {float(r['cross']):.4f}: its left side exceeds the right by "
          f"E(T)/beta with E(T) = {float(r['e16']):.6f} for T >= 16, and the first choice gives T up to {float(Tmax):.0f}.")
else:
    print("NOT CONFIRMED: (5.36) and hence (6.25) are not violated as claimed.")
