"""Eq 4.24 (case (b) of Lemmas 4.2.1/4.2.2): "min(c2 x/q, D) < Q/2" can fail by less than 1/2.

Claim: with Q = floor(x/|delta q|), the inequality min(c2 x/q, D) <= Q/2 that opens case (b), and
the strict form used to apply Lemma 4.1.2 for (4.24), fail in sub-case (i) (|delta| <= 1/2c2, near
1/2c2) and in sub-case (ii) (D <= Q0/2 with non-integer Q0); harmlessly, since
floor(D') <= floor(X/2) <= floor(X)/2 = Q/2 with X = x/|delta q|, D' = min(c2 x/q, D).
The |eta_1'|/2 in the first line of (4.24) for |eta'|_1/2 is a typo (not numerical).

Book inputs (typeI.tex): Lemma 4.2.1 hypotheses and c2 = (3 pi/5 sqrt c0)(1+sqrt(13/3)) (602-634);
Lemma 4.2.2's c2 = 6 pi/5 sqrt c0 (1002-1010); Q = floor(x/|delta q|) (656); "Case (b): |delta| <=
1/2c2 or D <= Q0/2. Then min(c2x/q,D) <= Q/2" (905-906); "applicable because min(c2x/q,D) < Q/2"
(916-918). c0 = 31.521.

Confirms if: at admissible points in both sub-cases (including q >= 2, where the q-not-dividing-m
sum is non-empty) D' > Q/2, while floor(D') <= Q/2 and D' - Q/2 < 1/2.

Run: python3 -I eq_4_24.py

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
c0 = Dm("31.521")
C2 = {"4.2.1": 3 * PI / (5 * c0.sqrt()) * (1 + (Dm(13) / 3).sqrt()), "4.2.2": 6 * PI / (5 * c0.sqrt())}
fl = lambda v: int(Dm(v).to_integral_value(rounding="ROUND_FLOOR"))
for k, v in C2.items():
    print(f"Lemma {k}: c2 = {v:.12f}, 1/(2c2) = {1/(2*v):.12f}")


def case(label, lem, sub, q, x, D, Q0, absd):
    c2 = C2[lem]
    q, x, D, Q0 = map(Dm, (q, x, D, Q0))
    X = x / (absd * q)
    Q = fl(X)
    Dp = min(c2 * x / q, D)
    hyp = absd / x <= 1 / (q * Q0) and q <= Q0 and Q0 >= 16 and 1 <= D <= x
    hyp = hyp and (absd <= 1 / (2 * c2) if sub == "i" else (absd >= 1 / (2 * c2) and D <= Q0 / 2))
    fails = not (Dp < Dm(Q) / 2) and not (Dp <= Dm(Q) / 2)
    rep = fl(Dp) <= Dm(Q) / 2 and Dp - Dm(Q) / 2 < Dm(1) / 2 and Dp <= X / 2 + Dm(10) ** -50  # equality when |delta| = 1/2c2
    print(f"{label} [Lemma {lem}, sub-case ({sub})]: hyp {hyp}; |delta|={absd:.6f}, X={X:.6f}, Q={Q}, "
          f"Q/2={Dm(Q)/2}, D'={Dp:.6f}; printed fails: {fails}; floor(D')={fl(Dp)} <= Q/2: {rep}")
    return hyp and fails and rep


r = []
r.append(case("A q=2, x=D=2000, |delta|=1/2c2", "4.2.1", "i", 2, 2000, 2000, 16, 1 / (2 * C2["4.2.1"])))
r.append(case("B q=2, x=D=2000, |delta|=0.4832", "4.2.1", "i", 2, 2000, 2000, 16, Dm("0.4832")))
r.append(case("C q=1, x=D=1000, |delta|=1/2c2", "4.2.2", "i", 1, 1000, 1000, 16, 1 / (2 * C2["4.2.2"])))
r.append(case("D q=2, x=D=1000, |delta|=1/2c2", "4.2.2", "i", 2, 1000, 1000, 16, 1 / (2 * C2["4.2.2"])))
r.append(case("E q=1, x=100, x/|delta|=16.7, Q0=16.5, D=8.25", "4.2.2", "ii", 1, 100, "8.25", "16.5",
              Dm(100) / Dm("16.7")))
for lem in ("4.2.1", "4.2.2"):
    r.append(case("F q=3, x=1000, x/|delta q|=16.7, Q0=16.5, D=8.25", lem, "ii", 3, 1000, "8.25", "16.5",
                  Dm(1000) / (Dm("16.7") * 3)))
print("all cases:", r)
if all(r):
    print("CONFIRMED: min(c2x/q,D) exceeds Q/2 = floor(x/|delta q|)/2 by less than 1/2 at admissible points of both sub-cases of case (b), while floor(D') <= Q/2 always holds.")
else:
    print("NOT CONFIRMED: some case-(b) example did not violate the printed inequality or broke the repair.")
