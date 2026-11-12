"""Lemma 4.2.1 (proof): five harmless slips in the proof text; the lemma itself holds.

Claim: (i) case (b)'s "min(c2 x/q, D) <= Q/2" with Q = floor(x/|delta q|) can fail by < 1/2,
though every integer m <= min(c2 x/q, D) has m <= Q/2; (ii) "(eps/(1+eps))Q >= (2|delta q|/x)Q > 1,
so q' >= 2" fails for eps < 1/7 and q' = 1 can occur; (iii) "D <= (Q+1)/2 => M >= floor(D)" fails
at D = (Q+1)/2, Q odd; (iv) the proof's M = min(Q/2, D) can lie below the stated min(Q0/2, D) for
non-integer Q0, with the same m-sum; (v) "R >= D" after (4.28) should read "R >= D'".

Book inputs (typeI.tex): hypotheses |delta/x| <= 1/(q Q0), q <= Q0, Q0 >= 16, c2 =
(3 pi/5 sqrt c0)(1 + sqrt(13/3)) and M in [min(Q0/2, D), D] (lines 602-634); Q = floor(x/|delta q|),
Q' = ceil((1+eps)Q), the parenthetical on q' >= 2 and M = min(Q/2, D) (lines 656-676);
"If D <= (Q+1)/2, then M >= floor(D)" (807); case (b) "Then min(c2 x/q, D) <= Q/2" (905-906);
"we have R >= D" (983-984), with R = max(c2 x/q, q/2). c0 = 31.521 (the value Ch. 6 uses for eta_2).

Confirms if: each of the five counterexamples satisfies the lemma's hypotheses and violates the
printed assertion, while the stated repair holds in each.

Run: python3 -I lemma_4_2_1.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as Dm, getcontext
from fractions import Fraction as F
import math

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
c0 = Dm("31.521")
c2 = 3 * PI / (5 * c0.sqrt()) * (1 + (Dm(13) / 3).sqrt())
fl = lambda v: int(Dm(v).to_integral_value(rounding="ROUND_FLOOR"))
print(f"c0 = {c0}, c2 = {c2:.12f}, 1/(2c2) = {1/(2*c2):.12f}")
ok = []

# (i) case (b), |delta| <= 1/(2 c2)
q, x, D, Q0 = Dm(2), Dm(1000), Dm(1000), Dm(16)
ad = 1 / (2 * c2)
X = x / (ad * q)
Q = fl(X)
Dp = min(c2 * x / q, D)
hyp = ad / x <= 1 / (q * Q0) and q <= Q0 and 1 <= D <= x and ad <= 1 / (2 * c2)
fails = Dp > Dm(Q) / 2
repair = fl(Dp) <= Dm(Q) / 2 and Dp - Dm(Q) / 2 < Dm(1) / 2
print(f"(i)   q=2, x=D=1000, |delta|=1/(2c2): hyp {hyp}; X={X:.6f}, Q={Q}, Q/2={Dm(Q)/2}, "
      f"min(c2x/q,D)={Dp:.6f}; printed '<= Q/2' fails: {fails}; floor(D')={fl(Dp)} <= Q/2: {repair}")
ok.append(hyp and fails and repair)

# (ii) q' >= 2 parenthetical, eps = 0.01
eps, q, a, Q0, x = F(1, 100), 16, 15, F(16), F(10**6)
X = F(33, 2)                      # x/|delta q|
delta = x / (X * q)               # delta > 0
Q = math.floor(X)
Qp = math.ceil((1 + eps) * Q)
hyp = delta / x <= 1 / (q * Q0) and q <= Q0 and math.gcd(a, q) == 1
lhs, rhs = eps / (1 + eps) * Q, 2 * delta * q / x * Q
alpha = F(a, q) + delta / x


def dist1(t):                     # distance to nearest integer
    t = t - math.floor(t)
    return min(t, 1 - t)


valid = [(ap, qp) for qp in range(1, Qp + 1) for ap in range(qp)
         if math.gcd(ap, qp) == 1 and dist1(alpha - F(ap, qp)) <= F(1, qp * Qp)]
not_aq = dist1(alpha - F(a, q)) > F(1, q * Qp)
thr = all((F(e, 1000) / (1 + F(e, 1000)) >= F(2) / 16) == (F(e, 1000) >= F(1, 7)) for e in range(1, 1001))
lhs07 = F(7, 100) / (1 + F(7, 100)) * Q
print(f"(ii)  eps=0.01, q=16, a=15, x=1e6, x/|dq|=16.5: hyp {hyp}; Q={Q}, Q'={Qp}; "
      f"(eps/(1+eps))Q={float(lhs):.6f} < (2|dq|/x)Q={float(rhs):.6f}: {lhs < rhs}")
print(f"      a/q excluded by Q': {not_aq}; valid a'/q' with q'<=Q' (a' mod q'): {valid}")
print(f"      eps/(1+eps) >= 2/Q0=1/8 iff eps >= 1/7 (grid eps=k/1000): {thr}; "
      f"at eps=0.07: {float(lhs07):.6f} < {float(rhs):.6f}: {lhs07 < rhs}")
ok.append(hyp and lhs < rhs and not_aq and (0, 1) in valid and thr and lhs07 < rhs)

# (iii) D = (Q+1)/2 with Q odd, case (a)
q, x, X, D, Q0 = Dm(1), Dm(1000), Dm("17.5"), Dm(9), Dm(16)
ad = x / (X * q)
Q = fl(X)
M = min(Dm(Q) / 2, D)
hyp = ad / x <= 1 / (q * Q0) and q <= Q0 and ad >= 1 / (2 * c2) and D > Q0 / 2
fails = D <= Dm(Q + 1) / 2 and not (M >= fl(D))
left = [m for m in range(1, fl(D) + 1) if m > M]
print(f"(iii) q=1, x=1000, x/|delta|=17.5, D=9: hyp {hyp}; Q={Q}, M={M}, floor(D)={fl(D)}; "
      f"'D<=(Q+1)/2 => M>=floor(D)' fails: {fails}; leftover m: {left}; "
      f"j-range of (4.17) at D=(Q+1)/2: floor((D-(Q+1)/2)/q')=0, log+(D/((Q+1)/2))=0")
ok.append(hyp and fails and left == [9])

# (iv) non-integer Q0, case (a)
q, Q0, x, D, X = Dm(1), Dm("16.5"), Dm(1000), Dm(1000), Dm("16.6")
ad = x / (X * q)
Q = fl(X)
M = min(Dm(Q) / 2, D)
lo = min(Q0 / 2, D)
hyp = ad / x <= 1 / (q * Q0) and q <= Q0 and ad >= 1 / (2 * c2)
same = fl(M / q) == fl(lo / q)
print(f"(iv)  Q0=16.5, q=1, x=D=1000, x/|delta|=16.6: hyp {hyp}; Q={Q}, M={M} < min(Q0/2,D)={lo}: "
      f"{M < lo}; floor(M/q)={fl(M/q)} = floor(min(Q0/2,D)/q)={fl(lo/q)}: {same}")
ok.append(hyp and M < lo and same)

# (v) R >= D vs R >= D', case (b) with c2 x/q < D, numbers of (i)
q, x, D = Dm(2), Dm(1000), Dm(1000)
Dp = min(c2 * x / q, D)
R = max(c2 * x / q, q / 2)
print(f"(v)   q=2, x=D=1000: D'={Dp:.6f}, R={R:.6f}, D={D}; 'R >= D' holds: {R >= D}; 'R >= D'' holds: {R >= Dp}")
ok.append(c2 * x / q < D and not (R >= D) and R >= Dp)

print("sub-claims confirmed:", ok)
if all(ok):
    print("CONFIRMED: all five printed assertions in the proof of Lemma 4.2.1 fail at admissible points while the stated local repairs hold.")
else:
    print("NOT CONFIRMED: at least one of the five sub-claims did not reproduce.")
