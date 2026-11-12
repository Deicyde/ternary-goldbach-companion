"""Eq 5.52 of [H] (H. A. Helfgott, The ternary Goldbach problem, arXiv:1501.05438v2).

Claim: as printed, (5.52) bounds the sum over all integers m in (A0, A1], which is false;
with 'm odd' (as in (5.50)-(5.51), and as the proof via 2*alpha gives) it holds. This check
uses many primes (W' = W/2) and also a non-zero perturbation of 2*alpha from a/q.

Book inputs (book/src/typeII.tex):
  - Lemma 5.2.3 hypotheses: W >= 1, W' >= W/2, 2 alpha = a/q + O*(1/(qQ)), q <= Q (lines 1143-1145);
  - (5.52): if A1 - A0 <= 2 varrho q and q <= rho Q, varrho, rho in [0,1], then
    sum_{A0<m<=A1} |sum_{W'<p<=W} (log p) e(alpha m p)|^2 <= (W - W' + q/(1 - varrho rho)) sum (log p)^2
    (lines 1161-1164);
  - (5.50), (5.51) carry 'm odd' (lines 1146, 1153); proof separates only odd m (lines 1170-1177).
  (a, q) = 1 is imposed as well.

Confirms the claim if, in each case (hypotheses checked in exact rationals), the all-m sum
exceeds the right side of (5.52) and the odd-m sum does not.

Run: python3 -I eq_5_52.py
Ported from a 2026-11-06 check script.
"""
import cmath
import math
from fractions import Fraction as F


def primes_in(lo, hi):
    return [n for n in range(math.floor(lo) + 1, math.floor(hi) + 1)
            if n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))]


def S2(alpha, ps, m):
    z = 0j
    for p in ps:
        fr = (alpha * m * p) % 1          # exact reduction of the phase
        z += math.log(p) * cmath.exp(2j * math.pi * float(fr))
    return abs(z) ** 2


def run(name, W, Wp, q, a, alpha, Q, vr, A0, A1):
    W, Wp, Q, vr, A0, A1 = map(F, (W, Wp, Q, vr, A0, A1))
    rho = F(q) / Q
    ps = primes_in(Wp, W)
    hyp = (W >= 1 and Wp >= W / 2 and abs(2 * alpha - F(a, q)) <= 1 / (q * Q) and q <= Q
           and A1 - A0 <= 2 * vr * q and q <= rho * Q and 0 <= vr <= 1 and 0 <= rho <= 1
           and math.gcd(a, q) == 1)
    ms = range(math.floor(A0) + 1, math.floor(A1) + 1)
    logsq = math.fsum(math.log(p) ** 2 for p in ps)
    rhs = float((W - Wp) + F(q) / (1 - vr * rho)) * logsq
    vals = {m: S2(alpha, ps, m) for m in ms}
    lall = math.fsum(vals.values())
    lodd = math.fsum(v for m, v in vals.items() if m % 2)
    print(f"{name}: W={W}, W'={Wp} ({len(ps)} primes), q={q}, a={a}, 2alpha-a/q="
          f"{2 * alpha - F(a, q)}, Q={Q}, rho=q/Q, varrho={vr}, (A0,A1]=({A0},{A1}]; "
          f"hypotheses hold: {hyp}")
    print(f"   RHS = {rhs:.4f}; LHS all m = {lall:.4f} (ratio {lall / rhs:.5f}); "
          f"LHS odd m = {lodd:.4f} (ratio {lodd / rhs:.5f})")
    return hyp and lall > rhs and lodd <= rhs


q, Q = 401, 10**7
ok1 = run("W'=W/2, delta=0", 400, 200, q, 1, F(1, 802), Q, 1, 0, 802)
Q2 = 10**6
alpha2 = (F(3, q) + F(1, 2 * q * Q2)) / 2
ok2 = run("W'=W/2, delta!=0, shifted A0", 400, 200, q, 3, alpha2, Q2, 1, F(1, 3), F(1, 3) + 802)
if ok1 and ok2:
    print("CONFIRMED: with 32 primes in (200,400] and all hypotheses of (5.52), the all-m sum "
          "exceeds the printed bound by a factor 1.33 while the odd-m sum is within it.")
else:
    print("NOT CONFIRMED: these cases do not separate the all-m and odd-m forms of (5.52).")
