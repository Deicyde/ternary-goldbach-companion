"""Check of [H] Eq (2.16): the printed justification cannot give the constant 1.03884.

Item: Eq 2.16 (book/src/notprem.tex:334-338).
Claim: (2.16), sum_{n<=y} Lambda(n) n < 1.03884 y^2/2 for y > 663, is true, but the printed
justification for y > 200000, "(2.15) and partial summation", cannot give the constant 1.03884.

Book inputs:
  - (2.15) = eq:trado2, notprem.tex:325: psi(y) = sum_{n<=y} Lambda(n) < 1.03883 y for all y > 0.
  - (2.16) = eq:chronop, notprem.tex:334-338: S(y) = sum_{n<=y} Lambda(n) n < 1.03884 y^2/2 for
    y > 663, "where we use (2.15) and partial summation for y > 200000".

Method. Partial summation gives S(y) = y psi(y) - I(y) with I(y) = int_0^y psi = sum_{n<=y}
Lambda(n)(y - n). The only use (2.15) can have is to bound the term y psi(y) by 1.03883 y^2
(it gives no lower bound on psi, so no bound on -I(y)). Even with I(y) known exactly, the best
bound this route yields is P(y) y^2/2 with P(y) = (1.03883 y^2 - I(y))/(y^2/2). The script sieves
to N = 10^8, computes the minimum of P(y) over all real y in (200000, N] (exactly, piecewise),
and also checks (2.16) itself on (663, N] and its failure just below 663.

Confirms the claim if: min P(y) over (200000, N] > 1.03884 (the route cannot give 1.03884), and
S(y) < 1.03884 y^2/2 for all 663 < y <= N (the inequality itself holds in the checked range).

Run: python3 -I eq_2_16.py        (about 15 s)

Ported from a 2026-11-06 check script.
"""
import itertools
import math
import time

N = 10 ** 8
C15, C16 = 1.03883, 1.03884
t0 = time.time()

sv = bytearray([1]) * (N + 1)
sv[0] = sv[1] = 0
for i in range(2, math.isqrt(N) + 1):
    if sv[i]:
        sv[i * i::i] = bytes(len(range(i * i, N + 1, i)))
pp = [(p, p) for p in itertools.compress(range(N + 1), sv)]
for p in range(2, math.isqrt(N) + 1):
    if sv[p]:
        q = p * p
        while q <= N:
            pp.append((q, p))
            q *= p
pp.sort()
print(f"prime powers up to N = {N}: {len(pp)}")


def P_min_on(a, b, ps, SS):
    """min over y in [a, b) of 2*C15 - 2 ps/y + 2 SS/y^2 (psi, S constant there)."""
    best = min((2 * C15 - 2 * ps / y + 2 * SS / (y * y), y) for y in (a, b))
    ys = 2 * SS / ps
    if a <= ys < b:
        best = min(best, (2 * C15 - ps * ps / (2 * SS), ys))
    return best


psi = 0.0
S = 0.0
psic = Sc = 0.0  # Neumaier compensation


def addN(s, c, x):
    t = s + x
    c += ((s - t) + x) if abs(s) >= abs(x) else ((x - t) + s)
    return t, c


minP = (float("inf"), None)
maxR = (0.0, None)
lastbad = None
checkpoints = {660: None, 662: None, 663: None, 200000: None, 200001: None, 10 ** 6: None, N: None}
prev = 1
for q, p in pp + [(N + 1, None)]:
    ps, SS = psi + psic, S + Sc  # values of psi, S on [prev, q)
    for y in checkpoints:
        if prev <= y < q:
            checkpoints[y] = (ps, SS)
    if q > 200000 and ps > 0:
        a, b = max(float(prev), 200000.0), float(min(q, N))
        if b > a:
            minP = min(minP, P_min_on(a, b, ps, SS))
    if p is None:
        break
    lp = math.log(p)
    psi, psic = addN(psi, psic, lp)
    S, Sc = addN(S, Sc, q * lp)
    R = (S + Sc) / (q * q / 2)
    if q > 663 and R > maxR[0]:
        maxR = (R, q)
    if R >= C16:
        lastbad = (q, R)
    prev = q

for y, (ps, SS) in sorted(checkpoints.items()):
    I = y * ps - SS
    print(f"y={y:>9}: psi/y={ps / y:.7f}  S/(y^2/2)={SS / (y * y / 2):.7f}  "
          f"I/(y^2/2)={I / (y * y / 2):.7f}  route P=(1.03883y^2-I)/(y^2/2)={(C15 * y * y - I) / (y * y / 2):.7f}")
print(f"limit of the route: 2*1.03883 - 1 = {2 * C15 - 1:.5f}")
print(f"min of route P(y) over 200000 < y <= {N}: {minP[0]:.7f} at y = {minP[1]:.1f} (target 1.03884)")
# S is constant and y^2 grows on [663, next prime power), so the sup there is the limit y -> 663+.
r663 = checkpoints[663][1] / (663 * 663 / 2)
if r663 > maxR[0]:
    maxR = (r663, "663+")
print(f"sup of S(y)/(y^2/2) over 663 < y <= {N}: {maxR[0]:.7f} at y = {maxR[1]}")
print(f"last prime power q <= {N} with S(q)/(q^2/2) >= 1.03884: {lastbad}")
print(f"S(662)/(662^2/2) = {checkpoints[662][1] / (662 * 662 / 2):.7f}")
print(f"time {time.time() - t0:.1f} s")

route_fails = minP[0] > C16
ineq_holds = maxR[0] < C16 and lastbad is not None and lastbad[0] <= 663
if route_fails and ineq_holds:
    print(f"CONFIRMED: (2.15) with partial summation gives at best {minP[0]:.5f}*y^2/2 for 200000 < y <= {N}, "
          f"not 1.03884*y^2/2, while (2.16) itself holds on (663, {N}] (max ratio {maxR[0]:.5f}).")
else:
    print(f"NOT CONFIRMED: route minimum {minP[0]:.6f}, max S/(y^2/2) on (663,N] {maxR[0]:.6f}, last failure {lastbad}.")
