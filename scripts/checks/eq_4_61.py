"""Check of [H, Eq (4.61)] (proof of Lemma 4.2.4, case |delta| <= 1/2c_2).

Claim: the remark after (4.61), "where we use the assumption that x >= e^2 c/2"
(lemma hypothesis x >= e^2 c_2/2), is wrong: (4.61) needs sqrt(c_2 x/2) >= e,
i.e. x >= 2e^2/c_2; the slip is harmless because the other hypotheses force
x >= 150.76. The packet also claimed that the weights log(jq+R) in (4.61) are
invalid (lower end of the block); this script tests that too.

Book inputs:
  - typeI.tex:1502  c_2 = 6 pi/(5 sqrt(c_0)), hypothesis x >= e^2 c_2/2,
    Q_0 >= max(2e, 2 sqrt x); typeI.tex:1507 U,V >= 1, UV + (19/18)Q_0 <= x/5.6.
  - minarctotals.tex:1924  c_0 = 31.521.
  - typeI.tex:1800  R = max(c_2 x/q, q/2).
  - typeI.tex:1805-1811  (4.61) and the remark "x >= e^2 c/2".
  - typeI.tex:941-952 (4.25) blocks jq+R < m <= min((j+1)q+R, D);
    typeI.tex:1114-1118 (4.53) |T_{m,o}| <= x/2m + |eta'|_1/2 (A-terms).

Confirms if: (a) at a point satisfying the stated hypothesis but with
x < 2e^2/c_2, the second line of (4.61) is smaller than its left side, and
(b) the lemma's hypotheses imply x >= 2e^2/c_2 (harmless). Separately it
reports whether sup over each block of x log m / m is at most the book's
lower-end term (in which case the weight part of the packet claim is wrong).

Run: python3 -I eq_4_61.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as Dm, getcontext
import math

getcontext().prec = 50
PI = Dm("3.14159265358979323846264338327950288419716939937510")
E = Dm(1).exp()
c0 = Dm("31.521")
c2 = 6 * PI / (5 * c0.sqrt())
book_x = E ** 2 * c2 / 2
need_x = 2 * E ** 2 / c2
print("c2 = 6 pi/(5 sqrt c0)             =", c2)
print("stated hypothesis x >= e^2 c2/2   =", book_x)
print("needed  x >= 2 e^2/c2             =", need_x)
print("sqrt(c2 x/2) at x = e^2 c2/2      =", (c2 * book_x / 2).sqrt())

c2f = float(c2)
log = math.log


def blocks(R, D, q):
    J = math.floor((D - R) / q)
    return range(J + 1) if J >= 0 else range(0)


def lhs(x, q, R, D):
    return sum(x / (j * q + R) * log(j * q + R) for j in blocks(R, D, q))


def line1(x, q, R, D):
    return x / R * log(R) + x / q * 0.5 * (log(D) ** 2 - log(R) ** 2)


def line2(x, q, R, D):
    return (math.sqrt(2 * x / c2f) * log(math.sqrt(c2f * x / 2))
            + x / q * log(D) * max(0.0, log(D / R)))


# (a) counterexample under the stated hypothesis only
x, q = 10.0, 6
R = max(c2f * x / q, q / 2)
D = R * (1 + 1e-12)
L, r2 = lhs(x, q, R, D), line2(x, q, R, D)
print("\n(a) x=10 (>= %.4f, < %.4f), q=6, R=%.4f, D=R+: LHS=%.6f, line 2=%.6f"
      % (float(book_x), float(need_x), R, L, r2))
fails_at_stated = float(book_x) <= x < float(need_x) and L > r2

# (b) hypotheses UV>=1, Q0>=2 sqrt x, UV+(19/18)Q0<=x/5.6 force s=sqrt x with
#     s^2/5.6 - (19/9)s - 1 >= 0
a, b, c = Dm(1) / Dm("5.6"), -Dm(19) / Dm(9), Dm(-1)
s = (-b + (b * b - 4 * a * c).sqrt()) / (2 * a)
xmin = s * s
print("(b) hypotheses force x >=", xmin, "; then sqrt(c2 x/2) >=",
      (c2 * xmin / 2).sqrt(), "> e")
harmless = xmin >= need_x

# (c) scan admissible cases: chain of (4.61) and validity of lower-end weights
cases = chain_bad = weight_bad = 0
worst = 0.0
xs = [float(xmin) * 1.0001, 160.0, 1e3, 1e5, 1e8, 1e12, 1e20]
for x in xs:
    for qe in (0.0, 0.25, 0.5, 0.6, 0.75, 0.9):
        q = max(1, round(x ** qe))
        if q > x / 5.6:
            continue
        R = max(c2f * x / q, q / 2)
        for ratio in (1.0001, 1.5, 3.0, 10.0, 1e3, 1e6):
            D = R * ratio
            if D > x / 5.6 or (D - R) / q > 1e6:
                continue
            cases += 1
            L = lhs(x, q, R, D)
            if not (L <= line1(x, q, R, D) * (1 + 1e-12)
                    and line1(x, q, R, D) <= line2(x, q, R, D) * (1 + 1e-12)):
                chain_bad += 1
            need = 0.0
            for j in blocks(R, D, q):
                lo, hi = j * q + R, min((j + 1) * q + R, D)
                m0, m1 = math.floor(lo) + 1, math.floor(hi)
                if m1 >= m0:
                    need += max(x * log(m) / m for m in {m0, min(m0 + 1, m1), m1})
            worst = max(worst, need / L)
            if need > L * (1 + 1e-12):
                weight_bad += 1
print("(c) admissible cases:", cases, "; (4.61) chain failures:", chain_bad,
      "; blocks needing more than lower-end weight:", weight_bad,
      "; max needed/LHS = %.12f" % worst)
if weight_bad == 0:
    print("    => lower-end weights log(jq+R) in (4.61) are valid; the packet's"
          " weight objection does not apply to (4.61).")

if fails_at_stated and harmless and chain_bad == 0:
    print("CONFIRMED: the assumption cited after (4.61) (x >= e^2 c_2/2 = %.4f) does not "
          "give (4.61), which needs x >= 2e^2/c_2 = %.4f, but the lemma's other hypotheses "
          "force x >= %.3f, so the slip is harmless." % (float(book_x), float(need_x), float(xmin)))
else:
    print("NOT CONFIRMED: the stated assumption suffices or the slip is not harmless "
          "(fails=%s harmless=%s chain_bad=%d)." % (fails_at_stated, harmless, chain_bad))
