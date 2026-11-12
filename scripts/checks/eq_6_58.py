"""Check of [H, Eq (6.58)] (bound for the terms (6.12) of |S_{I,2}|, first choice of parameters).

Claim: (i) the Mobius bound before (6.12) uses (4/5)(q/phi(q))/log^+(M_v/2q^2) for the
sum over (m,2q) = 1, but (2.22) at modulus 2q gives (4/5)(2q/phi(2q)), twice as large for
odd q; so the first term of (6.58) is not established for odd q (doubling it suffices).
(ii) The display before (6.57) bounds q/(2 sqrt(q delta_0)) by y^{1/6}/2^{3/2}; the right
bound is y^{1/2}/2^{3/2}; harmless, 0.00153 sqrt(x) still holds.

Book inputs:
  - notprem.tex:385-389  (2.22) sum_{n<=x,(n,r)=1} mu(n)/n = O*((4/5)(r/phi(r))/log(x/r)).
  - minarctotals.tex:259-263  the bound min((4/5)(q/phi(q))/log^+(M_v/2q^2), 1).
  - minarctotals.tex:347-353  (6.12) first line (x/2phi(q)) min(1, c_0/(pi delta)^2)
    min((4/5)/log^+(Q/4Vq^2), 1) log Vq; Q/V = y = x^{1/3}/6, V = 9x^{1/3}/2.
  - minarctotals.tex:1449-1488  second-line display (y^{1/6}/2^{3/2}), (6.57), (6.58):
    min(1, 4c_0'/delta^2)(3/2 log q + 2.74107) x/phi(q) + 0.29315 x/(q^2 delta_0)
    + (0.0434 log x + 0.1959) x^{2/3}; c_{8,I_2} = 1.17257 (l.380), c_{10,I} = 9.37301.
  - minarctotals.tex:1285-1300 parameters; (6.52) x >= 2.16e20; c_0' = 0.798437.

Confirms if (i) at an admissible odd q the first line of (6.12) with the factor
(4/5)(2q/phi(2q)) exceeds the whole right side of (6.58), while the doubled first term
covers it for all odd q <= y at x = x_0; and (ii) the printed inequality
q/(2 sqrt(q delta_0)) <= y^{1/6}/2^{3/2} fails at an admissible point, but with
y^{1/2}/2^{3/2} the sqrt(x)-coefficient stays <= 0.00153 for x >= 2.16e20.

Run: python3 -I eq_6_58.py

Ported from a 2026-11-06 check script.
"""
import math
from math import log, sqrt

c0, c0p = 31.521, 0.798437
c8I2, c10I = 1.17257, 9.37301


def phi(n):
    r = n; m = n; p = 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0: m //= p
            r -= r // p
        p += 1
    if m > 1: r -= r // m
    return r


def line1_612(x, q, factor):
    """(x/2q) min(factor (q/phi(q)) /log^+(y/4q^2), 1) log(Vq), with delta small (min(1, c0/(pi d)^2) = 1)."""
    y = x ** (1 / 3) / 6; V = 4.5 * x ** (1 / 3)
    L = log(y / (4 * q * q))
    mn = 1.0 if L <= 0 else min(factor * q / phi(q) / L, 1.0)
    return x / (2 * q) * mn * log(V * q)


def rhs658(x, q, d0):
    return (1.5 * log(q) + 2.74107) * x / phi(q) + 0.29315 * x / (q * q * d0) \
        + (0.0434 * log(x) + 0.1959) * x ** (2 / 3)


def main():
    x = 2.16e20; d0 = 2.0; delta = 0.5
    y = x ** (1 / 3) / 6
    print("x0 = %.3e, y = %.6e, 1/(2 c_2) = %.4f, delta = %.2f -> min(1, c0/(pi delta)^2) = %.0f, min(1, 4c0'/delta^2) = %.0f"
          % (x, y, 5 * sqrt(c0) / (12 * math.pi), delta, min(1, c0 / (math.pi * delta) ** 2), min(1, 4 * c0p / delta ** 2)))
    # (i)
    for q in (1, 3, 223):
        print("q=%d: 2q/phi(2q) = %.4f vs q/phi(q) = %.4f" % (q, 2 * q / phi(2 * q), q / phi(q)))
    q = 223
    corr = line1_612(x, q, 1.6); book = line1_612(x, q, 0.8); tot = rhs658(x, q, d0)
    print("q=223: (6.12) line 1 with (4/5)(2q/phi(2q)): %.6f x ; with printed (4/5)(q/phi(q)): %.6f x ;"
          " all of (6.58): %.6f x" % (corr / x, book / x, tot / x))
    fails = corr > tot
    # doubled first term suffices for every odd q <= y at x0 (scan)
    worst = 1e9; nfail = 0; nscan = 0
    for q in range(1, int(y) + 1, 2):
        c = line1_612(x, q, 1.6)
        dbl = 2 * (1.5 * log(q) + 2.74107) * x / phi(q)
        worst = min(worst, dbl / c)
        nscan += 1
        if c > rhs658(x, q, d0): nfail += 1
    print("odd q <= y scanned: %d ; corrected line 1 exceeds all of (6.58) for %d of them ;"
          " min (doubled first term)/(corrected line 1) = %.4f" % (nscan, nfail, worst))
    ok_i = fails and worst >= 1.0

    # (ii)
    qy = int(y); d0b = 2.0
    ok_adm = 8.0 <= x / (qy * 0.75 * x ** (2 / 3)) + 1e-9  # |delta| = 8 -> delta_0 = 2 allowed
    lhs = qy / (2 * sqrt(qy * d0b)); printed = y ** (1 / 6) / 2 ** 1.5; right = sqrt(y) / 2 ** 1.5
    print("q = y = %d, delta_0 = 2 (|delta|<=x/(qQ)=%.3f): q/(2 sqrt(q delta_0)) = %.4f vs printed y^(1/6)/2^(3/2) = %.4f,"
          " y^(1/2)/2^(3/2) = %.4f" % (qy, x / (qy * 0.75 * x ** (2 / 3)), lhs, printed, right))

    def coef(X, Ybound):
        yy = X ** (1 / 3) / 6
        s = c8I2 * (9 * X ** (1 / 3) / (2 * sqrt(2)) + 27 / 8) \
            + c10I / 2 * Ybound(X, yy) * (log(X) / 3 + log(4.5))
        return s / sqrt(X)
    cp = coef(x, lambda X, yy: yy ** (1 / 6) / 2 ** 1.5)
    cy = coef(x, lambda X, yy: yy ** 0.5 / 2 ** 1.5)
    cx = coef(x, lambda X, yy: X ** (1 / 6) / 2 ** 1.5)
    mx = max(coef(x * 10 ** (k / 10), lambda X, yy: yy ** 0.5 / 2 ** 1.5) for k in range(0, 300))
    print("sqrt(x)-coefficient at x0: printed %.7f, with y^(1/2) %.7f, with x^(1/6) %.7f ; max over [x0, 1e30 x0] with y^(1/2): %.7f"
          % (cp, cy, cx, mx))
    ok_ii = ok_adm and lhs > printed and mx <= 0.00153

    if ok_i and ok_ii:
        print("CONFIRMED: with (2.22) at modulus 2q the first line of (6.12) at q = 223, x = 2.16e20 is %.5f x > "
              "%.5f x = all of (6.58) (doubling the first term suffices), and y^{1/6}/2^{3/2} should be "
              "y^{1/2}/2^{3/2}, which keeps 0.00153 sqrt(x)." % (corr / x, tot / x))
    else:
        print("NOT CONFIRMED: (i)=%s (ii)=%s." % (ok_i, ok_ii))


if __name__ == "__main__":
    main()
