"""Check of [H, eq. (9.91)] (the constant 8.39/(4 pi) in the first line).

Claim: the first line of (9.91) keeps the 2013 constant 8.39 although (9.89) now
has 8.45, so the stated step ((1/2pi)log(T/2pi) + 1/4T <= (1/2pi)log T) gives
8.45/(4pi) = 0.6724 > 0.668 and (9.73) constants 0.4646, 0.9143, 1.7123 instead
of 0.462, 0.909, 1.71.  The printed inequality still holds, because the
pointwise replacement loses about 30% near T0 (ratio < 1 for T < e^258).

Book inputs (expform.tex):
  - l.1960-1972 (9.89): f(T) = 8.45 (log x + (1/2)log T)(T/2 - H) e^{-pi(T-2H)/4}.
  - l.1978-1984 (9.90): RHS = int_{T0}^oo f(T)((1/2pi)log(T/2pi) + 1/4T) dT.
  - l.1985-1995 (9.91): "(1/2pi)log(T/2pi)+1/4T <= (1/2pi)log T", first line
    (8.39/4pi) int ((log x)(log T) + (log T)^2/2)(T-2H)e^{-pi(T-2H)/4} dT, then 0.668.
  - l.2001-2026: 4a/pi <= 1.6957, 4b/pi <= 2.1319; final 0.462, 0.909, 1.71.
  - l.2277-2290: H = 200, T0 = 450, x >= 10^12.

Confirms if: 8.45/(4pi) > 0.668 and the chain with it gives coefficients above
0.462/0.909/1.71, while the printed first line of (9.91) is still >= RHS(9.90)
(pointwise ratio < 1 for 200 <= T < e^258, and the integrals at the book's
H = 200, T0 = 450, x = 1e12 and at H = 25, T0 = 200).

Run: python3 -I eq_9_91.py

Ported from a 2026-11-06 check script.
"""
from math import log, pi, exp

C = 8.45 / (4 * pi)
print("8.39/(4pi) = %.5f  8.45/(4pi) = %.5f  (0.668 printed)" % (8.39 / (4 * pi), C))
k = C * 4 / pi
c = (k / 2 * (1 + 2.132 / 25), k * (1 + 1.696 / 25), 2 * k)
c51 = 2 * k * (1 + 0.051 / (log(25) + log(1e8)))
print("coefficients with 8.45/(4pi): %.4f %.4f %.4f (%.4f with the 0.051 term)  vs 0.462 0.909 1.71" % (c + (c51,)))

dens = lambda T: log(T / (2 * pi)) / (2 * pi) + 1 / (4 * T)
ratio = lambda T: 8.45 * dens(T) / (8.39 * log(T) / (2 * pi))
for T in (200, 450, 1e4, 1e50):
    print("pointwise 8.45*dens(T) / ((8.39/2pi) log T) at T=%g: %.4f" % (T, ratio(T)))
lo, hi = log(200.0), 300.0
for _ in range(200):
    m = (lo + hi) / 2
    if ratio(exp(m)) < 1:
        lo = m
    else:
        hi = m
print("pointwise ratio < 1 for 200 <= T < e^%.3f" % lo)


def simpson(F, A, B, n=40000):
    h = (B - A) / n
    s = F(A) + F(B)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * F(A + i * h)
    return s * h / 3


holds = True
for (H, T0, x) in ((200, 450, 1e12), (200, 450, 1e8), (25, 200, 1e8), (25, 200, 1e30)):
    L = log(x)
    sc = exp(-pi * (T0 - 2 * H) / 4)
    rhs = simpson(lambda T: 8.45 * (L + 0.5 * log(T)) * (T / 2 - H) * exp(-pi * (T - T0) / 4) * dens(T), T0, T0 + 120) * sc
    fl = 8.39 / (4 * pi) * simpson(lambda T: (L * log(T) + log(T) ** 2 / 2) * (T - 2 * H) * exp(-pi * (T - T0) / 4), T0, T0 + 120) * sc
    print("H=%d T0=%d x=%.0e: per log x RHS(9.90) = %.4e, first line of (9.91) = %.4e, ratio %.4f"
          % (H, T0, x, rhs / L, fl / L, rhs / fl))
    holds = holds and rhs <= fl

if C > 0.668 and c[0] > 0.462 and c[1] > 0.909 and c[2] > 1.71 and holds and lo > 250:
    print("CONFIRMED: (9.91) uses 8.39/(4pi) where (9.89)'s 8.45 gives %.5f > 0.668 (coefficients %.4f, %.4f, %.4f), but its printed first line still bounds RHS(9.90) for T0 < e^%.1f, so (9.73) is unaffected." % (C, c[0], c[1], c[2], lo))
else:
    print("NOT CONFIRMED: the 8.39 versus 8.45 computation does not behave as claimed.")
