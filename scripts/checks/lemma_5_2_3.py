"""Lemma 5.2.3 of [H] (H. A. Helfgott, The ternary Goldbach problem, arXiv:1501.05438v2).

Claim: display (5.52) of Lemma 5.2.3 sums over all m in (A0, A1], without the 'm odd' of
(5.50)-(5.51); as printed it is false, while the odd-m version (which is what the proof,
separating odd m via 2*alpha, gives) holds.

Book inputs (book/src/typeII.tex):
  - Lemma 5.2.3 hypotheses: W >= 1, W' >= W/2, 2 alpha = a/q + O*(1/(qQ)), q <= Q (lines 1143-1145);
  - (5.52): if A1 - A0 <= 2 varrho q and q <= rho Q, varrho, rho in [0,1], then
    sum_{A0<m<=A1} |sum_{W'<p<=W} (log p) e(alpha m p)|^2 <= (W - W' + q/(1 - varrho rho)) sum (log p)^2
    (lines 1161-1164; no 'm odd', unlike (5.50) line 1146 and (5.51) line 1153);
  - proof: "For odd m, m' ... |{alpha(m-m')}| = |{2 alpha (m-m')/2}|" (lines 1170-1177).
  (a, q) = 1 is imposed as well (the proof uses it).

Confirms the claim if, for parameters satisfying every hypothesis (checked in exact
rationals), the all-m left side exceeds the right side of (5.52) while the odd-m left side
does not.

Run: python3 -I lemma_5_2_3.py
Ported from a 2026-11-06 check script.
"""
import math
from fractions import Fraction as F


def primes_in(lo, hi):
    return [n for n in range(math.floor(lo) + 1, math.floor(hi) + 1)
            if n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))]


def S2(alpha, ps, m):
    """|sum_p (log p) e(alpha m p)|^2 = sum_{p,p'} log p log p' cos(2 pi alpha m (p-p')),
    phases reduced mod 1 exactly."""
    tot = 0.0
    for p in ps:
        for pp in ps:
            fr = (alpha * m * (p - pp)) % 1
            tot += math.log(p) * math.log(pp) * math.cos(2 * math.pi * float(fr))
    return tot


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
    lall = math.fsum(S2(alpha, ps, m) for m in ms)
    lodd = math.fsum(S2(alpha, ps, m) for m in ms if m % 2)
    print(f"{name}: W={W}, W'={Wp}, primes {ps}, q={q}, a={a}, alpha={alpha}, Q={Q}, "
          f"rho=q/Q, varrho={vr}, (A0,A1]=({A0},{A1}]; hypotheses hold: {hyp}")
    print(f"   RHS = {rhs:.4f}; LHS all m = {lall:.4f} (ratio {lall / rhs:.4f}); "
          f"LHS odd m = {lodd:.4f} (ratio {lodd / rhs:.4f})")
    return hyp and lall > rhs and lodd <= rhs


ok1 = run("Example 1", 100, 90, 101, 2, F(1, 101), 10**6, 1, 0, 202)
ok2 = run("Example 2", 1000, 990, 1009, 2, F(1, 1009), 10**7, 1, 0, 2018)
if ok1 and ok2:
    print("CONFIRMED: under all hypotheses of Lemma 5.2.3, (5.52) summed over all m fails "
          "(4227.45 > 2323.22 for W=100, q=101) while the odd-m sum satisfies the bound.")
else:
    print("NOT CONFIRMED: the examples do not separate the all-m and odd-m forms of (5.52).")
