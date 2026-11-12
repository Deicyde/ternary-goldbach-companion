"""Check of [H, Theorem 7.1.4] (proof for general q in Sec. 9.6).

Claim: in the proof for general q, the term (9 + 11*1.2e6/q) x^{-1} is rewritten
inside (...)/sqrt(x) as 9/sqrt(x) + 1.32e6/(q sqrt(x)); since 11*1.2e6 = 1.32e7,
the coefficient should be 1.32e7. The stated bound of the theorem still holds.

Book inputs:
  - expform.tex:2229-2234  first bound for err: log(1.35e8/2pi)(7.9854e-16 +
    9.5777e-12/q) + ((1.634 log 1.35e8 + 12.43) sqrt(1.35e8)/sqrt(q)
    + 1.321 log 300000 + 34.51)/sqrt(x) + (9 + 11*1.2e6/q)/x
    + (log 300000)(11 + 6*1.2e6/q) x^{-3/2}.
  - expform.tex:2236-2240  the rewritten form, with 499845, 51.17,
    1.32e6/(q sqrt x), 9/sqrt x, 9.1e7/(qx), 139/x.
  - expform.tex:2242-2246 and intromaj.tex:178-206  x >= 1e12, 1 <= q <= 300000,
    final bound 1.3482e-14 + 1.617e-10/q + (499900/sqrt q + 52)/sqrt x.

Confirms if: 11*1.2e6 != 1.32e6 (it equals 1.32e7), and the first bound of
expform.tex:2229-2234 (with the correct coefficient) is still at most the final
bound for every q in 1..300000 at x = 1e12 (the worst case, since every term of
(first bound - final bound)*sqrt(x) beyond the constant ones decreases in x).

Run: python3 -I theorem_7_1_4.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as D, getcontext

getcontext().prec = 50
PI = D("3.14159265358979323846264338327950288419716939937510")

printed = D("1.32e6")
product = 11 * D("1.2e6")
print("11 * 1.2e6 =", product, "; printed coefficient =", printed,
      "; ratio =", product / printed)
slip = product != printed

L = (D("1.35e8") / (2 * PI)).ln()
A = L * D("7.9854e-16")
B = L * D("9.5777e-12")
C = (D("1.634") * D("1.35e8").ln() + D("12.43")) * D("1.35e8").sqrt()
K = D("1.321") * D(300000).ln() + D("34.51")
L3 = D(300000).ln()
print("log(1.35e8/2pi)*7.9854e-16 = %.8E (book 1.3482e-14)" % A)
print("log(1.35e8/2pi)*9.5777e-12 = %.8E (book 1.617e-10)" % B)
print("(1.634 log 1.35e8 + 12.43) sqrt(1.35e8) = %.4f (book 499845)" % C)
print("1.321 log 300000 + 34.51 = %.6f (book 51.17)" % K)
print("log 300000 * 6 * 1.2e6 = %.1f (book 9.1e7); 11 log 300000 = %.3f (book 139)"
      % (L3 * 6 * D("1.2e6"), L3 * 11))
consts_ok = (A <= D("1.3482e-14") and B <= D("1.617e-10") and C <= 499845
             and K <= D("51.17") and L3 * 6 * D("1.2e6") <= D("9.1e7")
             and L3 * 11 <= 139)


def first_bound(q, x):
    q = D(q)
    sx = x.sqrt()
    return (A + B / q + (C / q.sqrt() + K) / sx
            + (9 + 11 * D("1.2e6") / q) / x
            + L3 * (11 + 6 * D("1.2e6") / q) / (x * sx))


def final_bound(q, x):
    q = D(q)
    return D("1.3482e-14") + D("1.617e-10") / q + (D(499900) / q.sqrt() + 52) / x.sqrt()


x = D("1e12")
worst = None
for q in range(1, 300001):
    m = (final_bound(q, x) - first_bound(q, x)) * x.sqrt()
    if worst is None or m < worst[0]:
        worst = (m, q)
print("min over q in 1..300000 of (final - first)*sqrt(x) at x = 1e12: %.4f at q = %d"
      % worst)
# value the printed form gives vs correct, at q = 1, x = 1e12
print("1/q-coefficient inside (...) at x = 1e12: printed %.6f, correct %.6f"
      % (printed / x.sqrt() + D("9.1e7") / x, product / x.sqrt() + D("9.1e7") / x))
holds = worst[0] >= 0

if slip and holds and consts_ok:
    print("CONFIRMED: 11*1.2e6 = 1.32e7, not the printed 1.32e6, and with the correct "
          "coefficient the bound of Theorem 7.1.4 still holds for all q <= 300000, "
          "x >= 1e12 (min slack %.2f/sqrt(x))." % float(worst[0]))
else:
    print("NOT CONFIRMED: slip=%s, bound holds=%s, other constants ok=%s."
          % (slip, holds, consts_ok))
