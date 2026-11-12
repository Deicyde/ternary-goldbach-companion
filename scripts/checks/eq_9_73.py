"""Check of [H, eq. (9.73)] (the e^{-pi T1/4} coefficients 0.462, 0.909, 1.71).

Claim: the proof does not establish 0.462, 0.909, 1.71.  (9.90) applies Lemma
9.1.3, which counts only zeros with Im(rho) > T0, to the sum over |Im rho| > T0
with f from (9.89) bounding a single zero, dropping a factor 2; (9.91) also keeps
the 2013 constant 8.39 where (9.89) has 8.45.  Redone with C = 2*8.45/(4 pi), the
coefficients are about 0.93, 1.83, 3.43, and (9.93)'s 5.123e-15 becomes about
1.03e-14 (9.21e-15 as x -> oo); with the book's 366.904/sqrt(x) this exceeds the
printed 5.123e-15 + 366.91/sqrt(x) for x > 1.71e24.

Book inputs (expform.tex):
  - l.1724-1729 (9.73); l.1960-1972 (9.89) f(T) = 8.45 (log x + (1/2)log T)(T/2-H)e^{-pi(T-2H)/4};
    (9.85) 41.73727/(4pi) <= 3.32135 and (9.87) 2.542 just above.
  - l.1978-1995 (9.90), (9.91): 8.39/(4pi), 0.668; l.2001-2026: 4a/pi <= 1.6957,
    4b/pi <= 2.1319, (4/pi)/25 <= 0.051, T1 >= 25, x >= 10^8; final display with 0.462, 0.909, 1.71.
  - l.2283-2290 (9.93): T1 = 50, H = 200, T0 = 450, x >= 10^12, 5.123e-15 + 366.91/sqrt(x).
  - l.528-543 Lemma 9.1.3 (9.24): sum over Im(rho) > y with density (1/2pi)log(qT/2pi).

Confirms if: the book's chain with 0.668 reproduces 0.462/0.909/1.71 (so the
chain is read correctly), the same chain with C = 2*8.45/(4pi) gives
coefficients near 0.929/1.828/3.433, (9.93) with them exceeds 5.123e-15, and
the exact doubled integral of (9.90) exceeds the printed first line at
H = 25, T0 = 200 (so no sharper bookkeeping rescues the printed coefficients).

Run: python3 -I eq_9_73.py

Ported from a 2026-11-06 check script.
"""
from math import log, pi, exp, sqrt

print("3.32135*2.542 = %.6f (9.89 has 8.45); 8.39/(4pi) = %.6f; 8.45/(4pi) = %.6f"
      % (3.32135 * 2.542, 8.39 / (4 * pi), 8.45 / (4 * pi)))
T1 = 25.0
a = 1 + (1 + 4 / (pi * T1)) / (log(T1) - 4 / (pi * T1))
b = 1 + (2 + 8 / (pi * T1)) / (log(T1) - 8 / (pi * T1))
print("at T1=25: 4a/pi = %.5f (<=1.6957), 4b/pi = %.5f (<=2.1319), (4/pi)/25 = %.5f (<=0.051)"
      % (4 * a / pi, 4 * b / pi, 4 / pi / 25))


def coeffs(C):
    k = C * 4 / pi
    return (k / 2 * (1 + 2.132 / 25), k * (1 + 1.696 / 25),
            2 * k * (1 + 0.051 / (log(25) + log(1e8))))


book = coeffs(0.668)
corr = coeffs(2 * 8.45 / (4 * pi))
print("book chain (C=0.668):           %.5f %.5f %.5f  (printed 0.462 0.909 1.71)" % book)
print("corrected chain (C=2*8.45/4pi): %.5f %.5f %.5f" % corr)


def first(c, T1, H, x):
    L = log(x)
    return ((c[0] * log(T1) ** 2 / L + c[1] * log(T1)) * T1 + c[2] * (1 + log(T1) / L) * H) * exp(-pi / 4 * T1)


x12 = 1e12
pb = first((0.462, 0.909, 1.71), 50, 200, x12)
pc = first(corr, 50, 200, x12)
pinf = (corr[1] * log(50) * 50 + corr[2] * 200) * exp(-pi / 4 * 50)
xpart = 2.445 * sqrt(450) * log(450) + 50.04
print("(9.93) at x=1e12: printed coeffs %.5e (book 5.123e-15), corrected %.5e, x->oo %.4e; x^-1/2 coeff %.4f"
      % (pb, pc, pinf, xpart))
lo, hi = 12.0, 40.0
ex = lambda lx: first(corr, 50, 200, 10 ** lx) + xpart / 10 ** (lx / 2) - (5.123e-15 + 366.91 / 10 ** (lx / 2))
for _ in range(200):
    m = (lo + hi) / 2
    if ex(m) > 0:
        hi = m
    else:
        lo = m
print("corrected bound exceeds printed 5.123e-15 + 366.91/sqrt(x) for x > %.3e" % 10 ** hi)


# exact doubled RHS of (9.90) at H = 25, T0 = 200 versus the printed first line
def simpson(F, A, B, n=40000):
    h = (B - A) / n
    s = F(A) + F(B)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * F(A + i * h)
    return s * h / 3


worst = 9.0
for (H, T0) in ((25, 200), (25, 250), (30, 200)):
    for x in (1e8, 1e12, 1e30):
        L = log(x)
        T1 = T0 - 2 * H
        sc = exp(pi * T1 / 4)
        fs = lambda T: 8.45 * (L + 0.5 * log(T)) * (T / 2 - H) * exp(-pi * (T - T0) / 4)
        I = simpson(lambda T: fs(T) * (log(T / (2 * pi)) / (2 * pi) + 1 / (4 * T)), T0, T0 + 120)
        P = first((0.462, 0.909, 1.71), T1, H, x) * sc * L
        print("H=%d T0=%d x=%.0e: 2*RHS(9.90) / (printed first line * log x) = %.4f" % (H, T0, x, 2 * I / P))
        worst = min(worst, 2 * I / P) if (H, T0) == (25, 200) else worst

ok = (abs(book[0] - 0.462) < 1e-3 and abs(book[1] - 0.909) < 1e-3 and abs(book[2] - 1.71) < 5e-3
      and abs(corr[0] - 0.929) < 2e-3 and abs(corr[1] - 1.828) < 2e-3 and abs(corr[2] - 3.433) < 2e-3
      and pc > 5.123e-15 and worst > 1 and 8.45 / (4 * pi) > 0.668)
if ok:
    print("CONFIRMED: with the factor 2 and 8.45 the book's chain gives %.4f, %.4f, %.4f (not 0.462, 0.909, 1.71) and (9.93) becomes %.4e, and the exact doubled integral already exceeds the printed first line by %.3f x at H=25, T0=200."
          % (corr[0], corr[1], corr[2], pc, worst))
else:
    print("NOT CONFIRMED: the recomputed coefficients do not differ from the printed ones as claimed.")
