"""Check of [H, Eq (6.56)] (simplified bound for |S_{I,1}|, first choice of parameters).

Claim: (6.56) is derived from (6.53), which inherits the all-n main term of (4.40).
Redone with the odd-n main term that the proof of Lemma 4.2.3 actually gives,
(x/2q) min(1, c_0/(pi delta)^2) with Mobius sums over (m,2q) = 1, the delta-factor is
4 times larger for odd q once |delta| >= sqrt(c_0)/pi = 1.787, and the (6.54)-(6.55)
maximisation with log^+(U/2q^2) gives 6.46333 in place of 6.11676; so (6.56) is not
established for odd q. (For even q the odd-m, q|m main term is empty, so nothing is lost.)

Book inputs:
  - minarctotals.tex:67-104  (6.3) first line; c_0 = 31.521, c_0' = 0.798437,
    |(log eta)^(t)| <= min(2 - log 4, 24 log 2/(pi^2 t^2)).
  - minarctotals.tex:137-138  c_{3,I} = 2.11104, c_{4,I} = 1.00303.
  - notprem.tex:376-393  (2.20) |sum_{(n,r)=1} mu(n)/n| <= 1, (2.22) <= (4/5)(r/phi(r))/log(x/r),
    (2.23) |sum mu(n)/n log(x/n)| <= 1.00303 r/phi(r); applied here with r = 2q.
  - typeI.tex:1015 (4.30) and typeI.tex:1236-1256 (proof of Lemma 4.2.3): odd-n main term
    (x/2q) eta^(-delta/2), sums over (m,2q) = 1, |eta^(t)| <= c_0/(2 pi t)^2.
  - minarctotals.tex:1285-1300  U = x^{2/3}/(9 sqrt(q delta_0)), y = x^{1/3}/6, Q = (3/4)x^{2/3};
    (6.52) x >= 2.16e20.
  - minarctotals.tex:1418-1441  (6.54)-(6.56): 7/4 log delta_0 q + 6.11676 and the error
    terms (0.67845 log x - 1.20818) x^{2/3}/sqrt(q delta_0) + 0.37864 x^{2/3}.

Confirms if (a) at an admissible point with odd q the corrected first line exceeds the
whole right side of (6.56), and (b) the maximisation constants come out as 6.11676
(printed, U/q^2) and 6.46333 (modulus 2q, U/2q^2), both by closed form and by a grid.

Run: python3 -I eq_6_56.py

Ported from a 2026-11-06 check script.
"""
import math
from math import log, sqrt

c0, c0p, c3, c4 = 31.521, 0.798437, 2.11104, 1.00303
L4 = 2 - log(4)


def is_prime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True


def grid_max(A):
    """max over x, t of min((4/5)/log^+(A x^{2/3}/(9 t^{5/2})), 1)(log(9 x^{1/3} sqrt t) + c3) + c4 - (7/4)log t."""
    best = -1e9
    for t in (2.0, 10.0, 1e4, 1e8):
        for k in range(0, 200001):
            lx = k * 0.001
            Lam = log(A) + (2 / 3) * lx - log(9) - 2.5 * log(t)
            mn = 1.0 if Lam <= 0.8 else 0.8 / Lam
            best = max(best, mn * (log(9) + lx / 3 + 0.5 * log(t) + c3) + c4 - 1.75 * log(t))
    return best


def main():
    # (b) constants
    k_book = log(27 / 2) + 0.4 + c3 + c4
    k_corr = log(27 / sqrt(2)) + 0.4 + c3 + c4
    g_book, g_corr = grid_max(4.0), grid_max(2.0)
    print("closed form: log(27/2)+2/5+c3+c4 = %.7f (printed 6.11676); log(27/sqrt2)+2/5+c3+c4 = %.7f"
          % (k_book, k_corr))
    print("grid maxima: U/q^2 -> %.6f ; U/2q^2 -> %.6f" % (g_book, g_corr))
    ok_b = abs(k_book - 6.11676) < 1e-5 and abs(k_corr - 6.46333) < 1e-5 and \
        abs(g_book - k_book) < 1e-3 and abs(g_corr - k_corr) < 1e-3
    print("delta-factor ratio c0/pi^2 / c0' = %.6f ; saturation |delta| = sqrt(c0)/pi = %.4f"
          % (c0 / math.pi ** 2 / c0p, sqrt(c0) / math.pi))

    # (a) admissible point
    x = 2.16e20; x23 = x ** (2 / 3); q = 999983
    y = x ** (1 / 3) / 6; Q = 0.75 * x23
    print("x=%.3e y=%.6e q=%d prime=%s q<=y=%s x/(qQ)=%.5f" % (x, y, q, is_prime(q), q <= y, x / (q * Q)))
    phi_q = q - 1; phi_2q = q - 1
    ok_a = is_prime(q) and q % 2 == 1 and q <= y
    for delta in (4.0, 8.0):
        ok_a = ok_a and abs(delta) <= x / (q * Q)
        d0 = max(2.0, abs(delta) / 4)
        U = x23 / (9 * sqrt(q * d0))
        lxU = log(x / U)
        main656 = (x / q) * min(1, c0p / delta ** 2) * (q / phi_q) * (1.75 * log(d0 * q) + 6.11676)
        err656 = (x23 / sqrt(q * d0)) * (0.67845 * log(x) - 1.20818) + 0.37864 * x23
        rhs = main656 + err656
        rr = 2 * q / phi_2q
        Lp = log(U / (2 * q * q))
        mu = 1.0 if Lp <= 0 else min(1.0, 0.8 * rr / Lp)
        F = (x / (2 * q)) * min(1, c0 / (math.pi * delta) ** 2) * (mu * lxU + c4 * rr) \
            + (x / (2 * q)) * min(L4, 24 * log(2) / (math.pi ** 2 * (delta / 2) ** 2)) * mu
        print("delta=%.0f: U=%.4e  RHS(6.56) = %.4e + %.4e = %.4e ; corrected first line = %.4e ; ratio %.3f"
              % (delta, U, main656, err656, rhs, F, F / rhs))
        ok_a = ok_a and F > rhs

    if ok_a and ok_b:
        print("CONFIRMED: for odd q the corrected first line (x/2q, c_0/(pi delta)^2, modulus 2q) exceeds the "
              "whole RHS of (6.56) at x = 2.16e20, q = 999983, delta = 4, 8, and the redone constant is "
              "%.5f instead of 6.11676." % k_corr)
    else:
        print("NOT CONFIRMED: corrected bound does not exceed (6.56) or constants differ (a=%s b=%s)." % (ok_a, ok_b))


if __name__ == "__main__":
    main()
