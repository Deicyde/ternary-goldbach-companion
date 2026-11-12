"""Eq 4.32 (Lemma 4.2.2, case (a), via the proof of Lemma 4.2.1): two harmless slips.

Claim: (1) halving the second line of (4.19) leaves (3/2)c1(2 + ((1+eps)/eps) log+ ...) x/Q with
Q = floor(x/|delta q|); replacing x/Q by x/Q0 needs floor(x/|delta q|) >= Q0, which fails for some
non-integer Q0 (Ch. 6 uses Q0 = Q/v); with X = x/|delta q| >= Q0, the terms 2x/(Q+1) and
q' >= eps X/(1+eps) give the stated bound. (2) "if D <= (Q+1)/2 then M >= floor(D)" fails at
D = (Q+1)/2 with Q odd, leaving the odd m = (Q+1)/2; (4.17)-(4.19) still cover it.

Book inputs (typeI.tex): Lemma 4.2.2 with c2 = 6 pi/5 sqrt c0, c1 = 1 + |eta'|_1/(x/D) and (4.32)
(lines 1002-1048); "the second line in (4.19) gets halved", "(4.16) gets multiplied by 2",
(4.37) 5c0c2/3pi^2 = 2 sqrt(c0)/pi (1123-1140); (4.19) (863-869); Q = floor(x/|delta q|) (656);
"If D <= (Q+1)/2, then M >= floor(D)" (807-809). c0 = 31.521, |eta'|_1 = 8 log 2 (eta_2).

Confirms if: in (1) all hypotheses hold, Q < Q0, the printed second-line term exceeds the stated one
and the repaired term (and repaired total) do not; in (2) the hypotheses hold, Q is odd,
D = (Q+1)/2, M < floor(D) and the odd m = (Q+1)/2 is left over.

Run: python3 -I eq_4_32.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as Dm, getcontext

getcontext().prec = 60


def machin_pi():
    def atan_inv(n):
        x = Dm(1) / n
        x2, s, t, k = x * x, x, x, 1
        while True:
            t = -t * x2
            k += 2
            if abs(t / k) < Dm(10) ** -65:
                return s
            s += t / k
    return 16 * atan_inv(5) - 4 * atan_inv(239)


PI = machin_pi()
lp = lambda t: max(t.ln(), Dm(0)) if t > 0 else Dm(0)
fl = lambda t: int(t.to_integral_value(rounding="ROUND_FLOOR"))
c0 = Dm("31.521")
c2 = 6 * PI / (5 * c0.sqrt())
etap = 8 * Dm(2).ln()
print(f"c2 = {c2:.12f}, 1/(2c2) = {1/(2*c2):.12f}")


def case_a(q, Q0, x, D, X, eps, show=True):
    q, Q0, x, D, X, eps = map(Dm, (q, Q0, x, D, X, eps))
    absd = x / (X * q)
    Q = fl(X)
    hyp = (absd / x <= 1 / (q * Q0) and q <= Q0 and Q0 >= 16 and 1 <= D <= x
           and absd >= 1 / (2 * c2) and D > Dm(Q + 1) / 2 and 0 < eps <= 1)
    c1 = 1 + etap / (x / D)
    k = (1 + eps) / eps
    L1, L2 = lp(D / (Dm(Q + 1) / 2)), lp(2 * D / X)
    K = 2 * (c0 * c1).sqrt() / PI
    s32 = (3 + 2 * eps).sqrt()
    P2 = Dm(3) / 2 * c1 * (2 + k * L1) * (x / Q)                     # printed second line, halved
    P1 = (K * (D + ((1 + eps) * s32 - Dm(1) / 2) * (Q + 1) + ((1 + eps) * Q + 1) / 2 * L1)
          + 2 * c0.sqrt() / PI * (Dm(Q) / 2))                          # (4.19) line 1 + doubled (4.16)[M=Q/2]
    S1 = K * (D + (1 + eps) * min(Dm(Q + 1), 2 * D) * (s32 + L2 / 2))  # (4.32) first line
    S2 = Dm(3) / 2 * c1 * (2 + k * L2) * (x / Q0)                      # (4.32) second line
    F2 = Dm(3) / 2 * c1 * (2 * x / (Q + 1) + k * (x / X) * L1)          # repaired second line
    if show:
        print(f"  eps={eps}: hyp {hyp}; Q={Q} < Q0={Q0}: {Q < Q0}; x/Q={x/Q:.6f}, x/Q0={x/Q0:.6f}; "
              f"printed 2nd line {P2:.4f} vs (4.32) {S2:.4f}; repaired {F2:.4f}; "
              f"totals printed {P1+P2:.4f}, (4.32) {S1+S2:.4f}, repaired {P1+F2:.4f}")
    return hyp and Q < Q0 and P2 > S2 and F2 <= S2 and P1 + F2 <= S1 + S2


print("(1) q=1, Q0=16.5, x=D=100, x/|delta|=16.7")
ok1 = all([case_a(1, "16.5", 100, 100, "16.7", e) for e in ("1", "0.5", "0.1", "0.01")])
ok1 = ok1 and all(case_a(1, "16.5", 100, 100, "16.7", Dm(i) / 1000, show=False) for i in range(1, 1001))
print("    holds for eps in {1,0.5,0.1,0.01} and eps = i/1000, i = 1..1000:", ok1)

print("(2) q=1, Q0=16, x=100, x/|delta|=17.5, D=9")
q, Q0, x, X, D = Dm(1), Dm(16), Dm(100), Dm("17.5"), Dm(9)
absd = x / (X * q)
Q = fl(X)
M = min(Dm(Q) / 2, D)
hyp2 = absd / x <= 1 / (q * Q0) and q <= Q0 and absd >= 1 / (2 * c2) and 1 <= D <= x
left = [m for m in range(1, fl(D) + 1) if m > M and m % 2]
ok2 = hyp2 and Q % 2 == 1 and D == Dm(Q + 1) / 2 and M < fl(D) and left == [(Q + 1) // 2]
print(f"    hyp {hyp2}; |delta|={absd:.6f}; Q={Q}, D=(Q+1)/2: {D == Dm(Q+1)/2}; M={M}, floor(D)={fl(D)}; "
      f"odd m in (M, D]: {left}; j-range floor((D-(Q+1)/2)/q') = {fl((D - Dm(Q+1)/2) / 1)}, "
      f"log+(D/((Q+1)/2)) = {lp(D / (Dm(Q+1)/2))}")
print("results:", ok1, ok2)
if ok1 and ok2:
    print("CONFIRMED: with floor(x/|delta q|) < Q0 the printed x/Q term exceeds the x/Q0 term of (4.32) while the repaired term fits, and 'M >= floor(D)' fails at D = (Q+1)/2 with Q odd.")
else:
    print("NOT CONFIRMED: one of the two slips did not reproduce or its repair failed.")
