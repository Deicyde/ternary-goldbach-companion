"""Check of [H, Eq (4.50)] (eq:cupcake3, Lemma 4.2.4): its last O*-term.

Claim: the last O*-term of (4.50), (1/4 - 1/pi^2) c_0 (U+1)^2 V log q/(2x),
is not established as printed: it rests on the last step of (4.55), which
uses sum_{p^a<=V, p|q} (log p) p^a <= V log q, and that is false; the
argument gives the term only with an extra factor 3/2. The printed bound
(4.50) itself is not refuted.

Book inputs:
  - typeI.tex:1516-1522  (4.50), c_4 = 1.03884 (typeI.tex:1538), D = UV.
  - typeI.tex:1640-1645  (4.54): prefactor (pi^2-4)|eta''^|_inf/(2 pi^2 x)
    times the double sum over u<=U, v<=V, uv odd, uv<=M, q|uv, u squarefree
    of Lambda(v) u v.
  - typeI.tex:1650-1662  (4.55), final line M^2 log V/4q + (3c_4/4) MV
    + (U+1)^2 V log q/4.
  - typeI.tex:1496-1507  hypotheses (Q_0 >= max(2e, 2 sqrt x),
    UV + (19/18)Q_0 <= x/5.6, |delta/x| <= 1/qQ_0); typeI.tex:1569
    M = min(UV, Q/2), Q = floor(x/|delta q|) (typeI.tex:656).
  - c_0 = 31.521 (minarctotals.tex:1925).

Confirms if: (a) (pi^2-4)/(2pi^2) = 2(1/4 - 1/pi^2), so (4.54) times the last
term of (4.55) is exactly the last O*-term of (4.50); (b) the step
sum (log p)p^a <= V log q fails (q=3, V=9) and at an admissible instance the
middle line of (4.55) exceeds its final line even in total, but not the final
line with 3/2 on its last term; (c) at the same instance (4.54) is below the
printed O*-term of (4.50), so the bound itself is not refuted there.

Run: python3 -I eq_4_50.py

Ported from a 2026-11-06 check script.
"""
import math

C4 = 1.03884
C0 = 31.521
NMAX = 1000
LAMP = [0] * (NMAX + 1)
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


ok = True
k1 = (math.pi ** 2 - 4) / (2 * math.pi ** 2)
k2 = 2 * (0.25 - 1 / math.pi ** 2)
print(f"(a) (pi^2-4)/(2pi^2) = {k1:.15f}, 2(1/4-1/pi^2) = {k2:.15f}")
ok &= abs(k1 - k2) < 1e-14

q, V = 3, 9
l = sum(math.log(LAMP[v]) * v for v in range(3, V + 1) if LAMP[v] and q % LAMP[v] == 0)
print(f"\n(b) q=3, V=9: sum (log p) p^a = {l:.5f} > V log q = {V*math.log(q):.5f}: {l > V*math.log(q)}")
ok &= l > V * math.log(q)

x, q, U, V = 10 ** 6, 3, 726, 243
Q0 = 2 * math.sqrt(x)                 # = 2000
Q = math.isqrt(4 * x)                 # floor(x/|delta q|) with |delta| q = x/Q0
M = min(U * V, Q / 2)
hyp = U * V + 19 / 18 * Q0 <= x / 5.6 and q <= Q0 and Q0 >= 2 * math.e
print(f"   instance x=1e6, q=3, Q0=2sqrt x={Q0}, |delta|={x/Q0/q:.3f}, Q={Q}, M={M}, U={U}, V={V};"
      f" UV+(19/18)Q0={U*V+19/18*Q0:.1f} <= x/5.6={x/5.6:.1f}: {hyp}")
mid = sum(lam(v) * v * ((M / v) ** 2 / (4 * q) + 3 * M / (4 * v)) for v in range(3, V + 1) if LAMP[v] and math.gcd(v, 2 * q) == 1) \
    + sum(math.log(LAMP[v]) * v * (U + 1) ** 2 / 4 for v in range(3, V + 1) if LAMP[v] and LAMP[v] % 2 and q % LAMP[v] == 0)
t = (M * M * math.log(V) / (4 * q), 3 * C4 / 4 * M * V, (U + 1) ** 2 / 4 * V * math.log(q))
fin, finc = sum(t), t[0] + t[1] + 1.5 * t[2]
print(f"   (4.55) middle = {mid:.5g}, final = {fin:.5g}, final with 3/2 = {finc:.5g}")
ok &= hyp and mid > fin and mid <= finc

S = 0.0
for v in range(3, V + 1, 2):
    if LAMP[v]:
        for u in range(1, min(U, math.floor(M / v)) + 1, 2):
            if SQF[u] and (u * v) % q == 0:
                S += lam(v) * u * v
term454 = k1 * C0 / x * S
D = U * V
printed_O = (0.25 - 1 / math.pi ** 2) * C0 * (D * D * math.log(V) / (2 * q * x) + 1.5 * C4 * U * V * V / x
                                             + (U + 1) ** 2 * V * math.log(q) / (2 * x))
print(f"\n(c) (4.54) double sum = {S:.5g}; (4.54) = {term454:.5g}; printed O*-term of (4.50) = {printed_O:.5g}")
ok &= term454 <= printed_O

if ok:
    print(f"CONFIRMED: the last O*-term of (4.50) needs sum (log p)p^a <= V log q, which fails (12 log 3 > 9 log 3 at q=3, V=9; (4.55) middle {mid:.4g} > final {fin:.4g} at an admissible instance), the argument gives it only with a factor 3/2, and (4.54) = {term454:.3g} stays below the printed O*-term {printed_O:.3g}.")
else:
    print("NOT CONFIRMED: some part of the (4.50) claim did not reproduce.")
