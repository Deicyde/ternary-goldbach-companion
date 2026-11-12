"""Eq 4.30 (proof of Lemma 4.2.2): the display after (4.34) sets sum_{m <= M/q, m odd} m equal to
(M/q + 1)^2/4, which is only an upper bound.

Claim: since (pi^2 - 4)/(2 pi^2) = 4 (1/8 - 1/(2 pi^2)), the display's last '=' is equivalent to
sum_{m <= y, m odd} m = (y+1)^2/4 with y = M/q; this holds iff y is an odd integer, and '<='
always holds, which with M <= D gives the O*-term of (4.30).

Book inputs (typeI.tex): the display after (4.34) (lines 1095-1101); M = min(Q/2, D),
Q = floor(x/|delta q|) (656, 676); the O*-term of (4.30) (1015-1022).

Confirms if: the constant identity holds numerically, the sum is strictly below (y+1)^2/4 at
y = 2 and y = 4 (and at an admissible M/q), equality occurs on the grid exactly at odd integers,
and '<=' never fails.

Run: python3 -I eq_4_30.py

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
lhs_c = (PI**2 - 4) / (2 * PI**2)
rhs_c = 4 * (Dm(1) / 8 - 1 / (2 * PI**2))
ident = abs(lhs_c - rhs_c) < Dm(10) ** -50
print(f"(pi^2-4)/(2pi^2) = {lhs_c:.30f}\n4(1/8-1/2pi^2)   = {rhs_c:.30f}  identity: {ident}")


def S(y):
    return sum(m for m in range(1, math.floor(y) + 1) if m % 2)


for y in (F(2), F(4), F(1, 3), F(3), F(5)):
    print(f"y={y}: sum of odd m <= y = {S(y)}, (y+1)^2/4 = {(y + 1) ** 2 / 4}")
strict = S(F(2)) < F(9, 4) and S(F(4)) < F(25, 4)

le_ok, eq_set = True, []
for k in range(0, 8 * 300 + 1):
    y = F(k, 8)
    s, b = S(y), (y + 1) ** 2 / 4
    le_ok &= s <= b
    if s == b:
        eq_set.append(y)
eq_odd = all(y.denominator == 1 and y.numerator % 2 == 1 for y in eq_set) and len(eq_set) == 150
print(f"grid y = k/8 in [0,300]: '<=' always: {le_ok}; equality cases {len(eq_set)}, all odd integers: {eq_odd}")

# admissible M: x = 1e6, q = 5, delta = 1000 -> Q = 200, D = 500, M = min(Q/2, D) = 100, M/q = 20
x, q, delta, D = 10**6, 5, 1000, 500
Q = x // (delta * q)
M = min(F(Q, 2), D)
y = M / q
adm = S(y) < (y + 1) ** 2 / 4
print(f"admissible example x=1e6, q=5, |delta|=1000, Q0=100, D=500: Q={Q}, M={M}, M/q={y}: "
      f"sum={S(y)} < {(y + 1) ** 2 / 4}: {adm}; (M/q+1)^2 <= (D/q+1)^2: {(y + 1) ** 2 <= (F(D, q) + 1) ** 2}")
if ident and strict and le_ok and eq_odd and adm:
    print("CONFIRMED: sum_{m<=M/q, m odd} m equals (M/q+1)^2/4 only when M/q is an odd integer (e.g. 1 < 9/4 at M/q=2), so the printed '=' is only '<=', which suffices for (4.30).")
else:
    print("NOT CONFIRMED: the printed equality was not shown to fail, or the upper bound failed.")
