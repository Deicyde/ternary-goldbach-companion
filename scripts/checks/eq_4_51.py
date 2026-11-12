"""Check of [H, Eq (4.51)] (eq:piececake, Lemma 4.2.4, case (b)).

Claim: (i) c_1 is printed as 1 + |eta'|_1/(2x/D), but bounding T_{m,o} with
(4.36) gives 1 + |eta'|_1/(x/D); (ii) the closing remark that the bound also
holds when R = q/2 fails: the j=0 term of (4.62) then gives sqrt3 q log(q/2)
> sqrt3 q log(c_2 x/q), and the book's own chain (m <= q/2 term + (4.61) +
(4.62)) exceeds the printed (4.51) at admissible parameters, while for
R = c_2 x/q the chain stays below (4.51); (iii) log(q/2) < 0 at q = 1.

Book inputs:
  - typeI.tex:1524-1538  (4.51) and c_1 = 1 + |eta'|_1/(2x/D), D = UV;
    typeI.tex:1496-1507 hypotheses; c_2 = 6 pi/(5 sqrt c_0) (typeI.tex:1502).
  - typeI.tex:1114-1121  (4.36) and the resulting c_1 = 1 + |eta'|_1/(x/D).
  - typeI.tex:1787-1790  the m <= q/2 term; typeI.tex:1800 R = max(c_2x/q, q/2);
    typeI.tex:1805-1823  (4.61), (4.62); typeI.tex:1824-1838 the sum and the
    remark '(or R = q/2 ...)'.
  - c_0 = 31.521, |eta_2'|_1 = 8 log 2 (minarctotals.tex:1925, 1936).

Confirms if: (a) at x=1e12, q=Q_0=D=1e10 (U=V=1e5, delta=0) and at
x=1e20, q=D=1e17, all hypotheses hold, R = q/2, and the chain exceeds the
printed (4.51); (b) over a grid with R = c_2x/q and D > R the chain is at most
the printed (4.51); (c) the m <= q/2 term is negative at q = 1; (d) the c_1
values differ as stated (at D/x = 1/6: 1.462 vs 1.924).

Run: python3 -I eq_4_51.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as Dd, getcontext

getcontext().prec = 60
PI = Dd("3.141592653589793238462643383279502884197169399375105820974944")
E = Dd(1).exp()
ln = lambda v: Dd(v).ln()
sq = lambda v: Dd(v).sqrt()
logp = lambda v: ln(v) if Dd(v) > 1 else Dd(0)
S3 = sq(3)
c0 = Dd("31.521")
eta1 = 8 * ln(2)
c2 = 6 * PI / (5 * sq(c0))


def c1_printed(x, D):
    return 1 + eta1 / (2 * x / D)


def c1_odd(x, D):
    return 1 + eta1 / (x / D)


def small_m(x, q):  # the m <= q/2 term
    return 2 * eta1 / PI * q * max(Dd(1), ln(c0 * E ** 3 * q * q / (4 * PI * eta1 * x))) * ln(q / 2)


def printed451(x, q, D, c1):
    k = 2 * sq(c0 * c1) / PI
    return (k * (D * ln(D / sq(E)) + q * (S3 * ln(c2 * x / q) + ln(D) / 2 * logp(D / (q / 2))))
            + 3 * c1 / 2 * (x / q) * ln(D) * logp(D / (c2 * x / q))
            + small_m(x, q)
            + 3 * c1 / (2 * sq(2 * c2)) * sq(x) * ln(c2 * x / 2)
            + 25 * c0 / (4 * PI ** 2) * (2 * c2) ** Dd("1.5") * sq(x) * ln(x))


def chain(x, q, D, c1):
    """m<=q/2 term + (4.60) [if q^2 < 2c2x] + (3c1/2)(4.61) + (2 sqrt(c0c1)/pi) q (4.62) [if D > R]."""
    k = 2 * sq(c0 * c1) / PI
    tot = small_m(x, q)
    R = max(c2 * x / q, q / 2)
    if q * q < 2 * c2 * x:
        Dp = min(c2 * x / q, D)
        tot += 5 * c0 * c2 / (3 * PI ** 2) * Dp * ln(Dp / sq(E)) + 25 * c0 / (4 * PI ** 2) * (2 * c2) ** Dd("1.5") * sq(x) * ln(x)
    if D > R:
        g1 = x / R * ln(R) + x / q * ln(D) * logp(D / R)                       # first line of (4.61)
        g2 = S3 * ln(R) + (D * ln(D / E) - R * ln(R / E)) / q + ln(D) / 2 * ln(D / R)  # (4.62)
        tot += 3 * c1 / 2 * g1 + k * q * g2
    return tot, R


def hyps(x, q, Q0, U, V):
    D = U * V
    return (Q0 >= max(2 * E, 2 * sq(x)) and q <= Q0 and x >= E ** 2 * c2 / 2
            and U >= 1 and V >= 1 and D + Dd(19) / 18 * Q0 <= x / Dd("5.6"))


ok = True
print("c2 =", f"{float(c2):.10f}")
print("\n(a) R = q/2 examples (delta = 0, Q0 = q)")
exc = []
for (x, q, U, V) in ((Dd(10) ** 12, Dd(10) ** 10, Dd(10) ** 5, Dd(10) ** 5),
                     (Dd(10) ** 20, Dd(10) ** 17, Dd(10) ** 8, Dd(10) ** 9)):
    D = U * V
    c1 = c1_printed(x, D)
    P = printed451(x, q, D, c1)
    C, R = chain(x, q, D, c1)
    h = hyps(x, q, q, U, V)
    print(f"   x={float(x):.0e} q={float(q):.0e} D={float(D):.0e}: hyps {h}, R=q/2: {R == q/2};"
          f" printed (4.51) = {float(P):.6e}, chain = {float(C):.6e}, ratio {float(C/P):.5f}")
    print(f"      j=0: sqrt3 q log(q/2) = {float(S3*q*ln(q/2)):.4e} vs sqrt3 q log(c2x/q) = {float(S3*q*ln(c2*x/q)):.4e}")
    ok &= h and R == q / 2 and C > P
    exc.append(C / P)

print("\n(b) R = c2x/q grid (q^2 < 2c2x, D > R), printed c1 on both sides")
worst, warg, n = Dd(0), None, 0
for ex in (8, 12, 16, 20, 24, 30):
    x = Dd(10) ** ex
    for fq in ("0.5", "0.6", "0.7", "0.8", "0.9", "0.95", "0.99"):
        q = Dd(int((2 * c2 * x).sqrt() ** (2 * Dd(fq))))
        if q < 2 or q * q >= 2 * c2 * x:
            continue
        for fD in ("0.3", "0.5", "0.6", "0.7", "0.8", "0.9", "0.95", "0.99"):
            D = Dd(int(x ** Dd(fD)))
            if D + Dd(19) / 18 * q > x / Dd("5.6") or D <= c2 * x / q:
                continue
            c1 = c1_printed(x, D)
            C, R = chain(x, q, D, c1)
            r = C / printed451(x, q, D, c1)
            n += 1
            if r > worst:
                worst, warg = r, (ex, float(q), float(D))
print(f"   {n} points, max chain/printed = {float(worst):.6f} at (log10 x, q, D) = {warg}")
ok &= n > 0 and worst <= 1

print("\n(c) q = 1")
t = small_m(Dd(10) ** 12, Dd(1))
print(f"   m <= q/2 term at x=1e12, q=1: {float(t):.4f}")
ok &= t < 0

print("\n(d) c_1")
x = Dd(10) ** 12
D = x / 6
a, b = c1_printed(x, D), c1_odd(x, D)
print(f"   D/x=1/6: printed {float(a):.4f}, from (4.36) {float(b):.4f}")
ok &= abs(float(a) - 1.4621) < 1e-3 and abs(float(b) - 1.9242) < 1e-3

if ok:
    print(f"CONFIRMED: with R = q/2 the book's chain exceeds the printed (4.51) (ratios {float(exc[0]):.4f}, {float(exc[1]):.4f}) while it stays below it for R = c_2x/q (max {float(worst):.4f}); the m <= q/2 term is negative at q = 1, and c_1 should be 1+|eta'|_1/(x/D).")
else:
    print("NOT CONFIRMED: some part of the (4.51) claim did not reproduce.")
