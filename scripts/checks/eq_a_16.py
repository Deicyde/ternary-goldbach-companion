"""Check of [H, (A.16)] (explicit formula for Mh).

Claim: the overall minus sign of (A.16) is wrong; the right side as printed
equals -Mh(s), and Mh(s) = +e^{-1/2}(-1)^{-s}(8 gamma(s+2,-2) + 12 gamma(s+3,-2)
+ 6 gamma(s+4,-2) + gamma(s+5,-2)). The formula is never used.

Book inputs:
  - normsapp.tex l.8-10: h(t) = t^2 (2-t)^3 e^{t-1/2} on [0,2].
  - normsapp.tex l.61: Mphi(s) = int_0^oo phi(x) x^s dx/x.
  - normsapp.tex l.100-102 (A.9): C_0 = Mh(0) = 92 e^{-1/2} - 12 e^{3/2}.
  - normsapp.tex l.215-221 (A.16) and gamma(s,x) = int_0^x e^{-t} t^{s-1} dt.

Method: at s = 0, 1, 2 every term is single-valued: gamma(n,x) =
(n-1)!(1 - e^{-x} sum_{k<n} x^k/k!) and (-1)^{-s} = +-1. Compare the printed
right side with Mh(s) computed by quadrature. At complex s use mpmath's
gammainc(a, 0, -2) and (-1)^{-s} = e^{-i pi s} (principal branches).

Confirms if: at s = 0, 1, 2 the printed right side equals -Mh(s) (and Mh > 0),
and at complex s the '+' version matches Mh(s) while the printed one does not.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_a_16.py

Ported from a 2026-11-06 check script.
"""
from mpmath import mp, mpf, mpc, exp, quad, gammainc, factorial, pi, e

mp.dps = 30

def Mh(s):
    return quad(lambda x: x**2 * (2 - x)**3 * exp(x - mpf(1) / 2) * x**(s - 1), [0, 1, 2])

def gam_int(n, x):  # lower incomplete gamma, integer n >= 1
    return factorial(n - 1) * (1 - exp(-x) * sum(x**k / factorial(k) for k in range(n)))

def bracket(G):
    return 8 * G(2) + 12 * G(3) + 6 * G(4) + G(5)

ok = True
for s in [0, 1, 2]:
    br = bracket(lambda j: gam_int(s + j, mpf(-2)))
    printed = -exp(-mpf(1) / 2) * (-1) ** (-s) * br
    true = Mh(s)
    print("s=%d: printed RHS = %s   Mh(s) = %s" % (s, mp.nstr(printed, 15), mp.nstr(true, 15)))
    ok &= abs(printed + true) < mpf(10) ** -20 and true > 0
C0 = 92 * exp(-mpf(1) / 2) - 12 * exp(mpf(3) / 2)
print("C_0 = 92e^{-1/2} - 12e^{3/2} =", mp.nstr(C0, 15))
ok &= abs(Mh(0) - C0) < mpf(10) ** -20

for s in [mpc(0, 2), mpc(0.3, 0.7), mpc(2.5, -3)]:
    br = bracket(lambda j: gammainc(s + j, 0, -2))
    plus = exp(-mpf(1) / 2) * exp(-1j * pi * s) * br
    true = Mh(s)
    print("s=%s: '+' version = %s  printed = %s  Mh = %s" % (mp.nstr(s, 3), mp.nstr(plus, 12), mp.nstr(-plus, 12), mp.nstr(true, 12)))
    ok &= abs(plus - true) < mpf(10) ** -15 and abs(-plus - true) > mpf(10) ** -3

if ok:
    print("CONFIRMED: the printed (A.16) equals -Mh(s) (e.g. -2.0205518 = -C_0 at s = 0), and the version with leading '+' matches Mh(s) at real and complex s.")
else:
    print("NOT CONFIRMED: the printed (A.16) is not -Mh(s) at the test points.")
