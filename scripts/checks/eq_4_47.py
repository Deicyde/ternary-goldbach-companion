"""Check of [H, Eq (4.47)] (eq:bocio, proof of Lemma 4.2.3, case (b)).

Claim: the last '<=' of (4.47) (line 4 -> line 5) is false whenever
D < c_2 x/q, because it needs q D' >= c_2 x; the final bound (line 5) still
holds, since line 3 <= line 5. Also three typos: line 1 has c_0 q^3/(6x)
where Lemma 4.1.2 per block gives c_0 q^3/(4x) (line 2's constant); line 2 has
(1/q) int t log(x/t) dt where line 3 needs 1/q^2; and 'q^3/x <= (2c_2)^{3/2}'
lacks a factor sqrt(x).

Book inputs:
  - typeI.tex:1411-1430  the five lines of (4.47); typeI.tex:1431-1433
    D' = min(c_2 x/q, D) and the parenthetical bounds; typeI.tex:1408
    q^2 < 2 c_2 x.
  - typeI.tex:1169  c_2 = 6 pi/(5 sqrt c_0); minarctotals.tex:1925 c_0 = 31.521.
  - typeI.tex:188-200  Lemma 4.1.2: per block (20/(3 pi^2)) C q^2;
    typeI.tex:1114-1118 (4.36) third entry (m/x)(c_0/2)/sin^2, so
    C = (c_0/2)(j+1/2)q/x on the j-th block.

Confirms if: (a) at x=1e6, q=100, D'=1000 line 4 > line 5 and line4-line5
equals (5c_0c_2/3pi^2) 4 sqrt(2c_2x) log(c_2x/(qD')); (b) on a grid of
admissible (x,q,D') line 4 > line 5 at every point with qD' < c_2 x and
line 3 <= line 5 everywhere; (c) each typo is numerically inconsistent with
the neighbouring line as stated above.

Run: python3 -I eq_4_47.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as Dm, getcontext

getcontext().prec = 50
PI = Dm("3.14159265358979323846264338327950288419716939937510")
SQE = Dm("0.5").exp()
c0 = Dm("31.521")
c2 = 6 * PI / (5 * c0.sqrt())
u = 5 * c0 / (3 * PI ** 2)  # all lines below are in units of u


def ln(v):
    return Dm(v).ln()


def lines(x, q, Dp):
    x, q, Dp = Dm(x), Dm(q), Dm(Dp)
    k = 2 * q ** 3 / x  # 10 c0 q^3/(3 pi^2 x) in units u
    I0 = Dp * ln(x / Dp) + Dp                    # int_0^D' log(x/t)
    I1 = Dp * Dp / 2 * ln(x / Dp) + Dp * Dp / 4  # int_0^D' t log(x/t)
    L2p = k * (ln(2 * x / q) + I0 / q + I1 / q + Dp / q * ln(x / Dp))
    L2c = k * (ln(2 * x / q) + I0 / q + I1 / q ** 2 + Dp / q * ln(x / Dp))
    L3 = k * (ln(2 * x / q) + (2 * Dp / q + Dp * Dp / (2 * q * q)) * ln(SQE * x / Dp))
    r = (2 * c2 * x).sqrt()
    L4 = c2 * (4 * r * ln(2 * x / q) + 4 * r * ln(SQE * x / Dp) + Dp * ln(SQE * x / Dp))
    L5 = c2 * (Dp * ln(SQE * x / Dp) + 4 * r * ln(2 * SQE * x / c2))
    gap = c2 * 4 * r * ln(c2 * x / (q * Dp))
    return dict(L2p=L2p, L2c=L2c, L3=L3, L4=L4, L5=L5, gap=gap)


def blocksum(x, q, Dp, const):
    """const * q^3/x * sum_{1<=j<=D'/q+1/2} (j+1/2) log(x/((j-1/2)q)), units u."""
    x, q, Dp = Dm(x), Dm(q), Dm(Dp)
    s, j = Dm(0), 1
    while j <= Dp / q + Dm("0.5"):
        s += (j + Dm("0.5")) * ln(x / ((j - Dm("0.5")) * q))
        j += 1
    return const * q ** 3 / x * s


print("c0 =", c0, " c2 =", f"{float(c2):.10f}")
ok = True

# (a) test point
x, q, Dp = 10 ** 6, 100, 1000
r = lines(x, q, Dp)
print("\n(a) x=1e6, q=100, D'=1000; c2x/q =", f"{float(c2*x/q):.4f}", "; q^2<2c2x:", q * q < 2 * c2 * x)
for kk in ("L3", "L4", "L5", "gap"):
    print(f"   {kk:4s} = {float(r[kk]):.4f}")
ident = abs(r["L4"] - r["L5"] - r["gap"]) < Dm(10) ** -30
print("   line4 > line5:", r["L4"] > r["L5"], "; identity line4-line5 = gap:", ident)
ok &= r["L4"] > r["L5"] and ident

# (b) grid
tot = n_int = n_fail_int = 0
max35 = Dm(0)
arg = None
for ex in (4, 6, 8, 12, 20):
    xx = Dm(10) ** ex
    qmax = int((2 * c2 * xx).sqrt())
    while Dm(qmax) ** 2 >= 2 * c2 * xx:
        qmax -= 1
    qs = {2, 3, qmax}
    for i in range(18):
        qs.add(max(2, int(round(2 * (qmax / 2) ** (i / 17)))))
    for qq in sorted(qs):
        qq = Dm(qq)
        lo, hi = qq / 2, c2 * xx / qq
        if hi <= lo:
            continue
        for i in range(1, 41):
            Dp2 = hi if i == 40 else lo * (hi / lo) ** (Dm(i) / 40)
            rr = lines(xx, qq, Dp2)
            tot += 1
            if qq * Dp2 < c2 * xx * (1 - Dm(10) ** -30):
                n_int += 1
                if not rr["L4"] > rr["L5"]:
                    n_fail_int += 1
            if rr["L3"] / rr["L5"] > max35:
                max35, arg = rr["L3"] / rr["L5"], (ex, int(qq), f"{float(Dp2):.6g}")
print(f"\n(b) grid: {tot} points, {n_int} with qD' < c2x;"
      f" line4 <= line5 at {n_fail_int} of those")
print("   max line3/line5 =", f"{float(max35):.12f}", "at (log10 x, q, D') =", arg)
ok &= n_fail_int == 0 and max35 <= 1

# (c) typos
print("\n(c) typos")
correct_line1 = blocksum(x, q, Dp, 2)          # (10 c0/(3pi^2)) q^3/x * sum
printed_line1 = blocksum(x, q, Dp, Dm(4) / 3)  # (40/(3pi^2)) c0 q^3/(6x) * sum
print(f"   line1 printed (6x) = {float(printed_line1):.4f}; per-block Lemma 4.1.2 (4x) = {float(correct_line1):.4f}")
t1 = printed_line1 < correct_line1 and correct_line1 <= r["L2c"]
print(f"   line2 printed (1/q) = {float(r['L2p']):.4f}; with 1/q^2 = {float(r['L2c']):.4f}; line3 = {float(r['L3']):.4f}")
t2 = abs(r["L2c"] - r["L3"]) < Dm(10) ** -30 and abs(r["L2p"] - r["L3"]) > 1
xq, qq = Dm(10) ** 6, Dm(1000)
lhs, b1, b2 = qq ** 3 / xq, (2 * c2) ** Dm("1.5"), (2 * c2) ** Dm("1.5") * xq.sqrt()
print(f"   x=1e6, q=1000 (q^2<2c2x: {qq*qq < 2*c2*xq}): q^3/x = {float(lhs):.1f},"
      f" (2c2)^1.5 = {float(b1):.4f}, (2c2)^1.5 sqrt x = {float(b2):.1f}")
t3 = qq * qq < 2 * c2 * xq and lhs > b1 and lhs <= b2
print("   typo checks:", t1, t2, t3)
ok &= t1 and t2 and t3

if ok:
    print(f"CONFIRMED: the last '<=' of (4.47) fails whenever D < c_2 x/q (line 4 = {float(r['L4']):.0f} > line 5 = {float(r['L5']):.0f} in units 5c_0/3pi^2 at x=1e6, q=100, D'=1000), while line 3 <= line 5 on the whole grid (max ratio {float(max35):.10f}), and the three typos are as claimed.")
else:
    print("NOT CONFIRMED: at least one part of the (4.47) claim did not reproduce.")
