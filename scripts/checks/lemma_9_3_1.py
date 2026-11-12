"""Check of [H, Lemma 9.3.1] (lem:festavign), proof.

Claim: the printed proof does not give the stated constants 6.11 and 1.578:
(a) step (9.49) is false (Lemma 9.1.3's decreasing-f clause drops
f(T0)g_chi(T0)); (b) (9.51) treats the constant (1/4T)*T = 1/4 as
(1/2pi)(pi/2)/T, and is false at T0 = 50; (c) the bound 1.578 in (9.54) uses
T0 >= 4 pi^2 |delta|, which the hypothesis T0 >= max(10 pi |delta|, 50) does not
give; (d) the pairing rho <-> 1 - rho holds only for real chi. The lemma
itself is not claimed false.

Book inputs (expform.tex):
  - l.1050: T0 >= max(10 pi |delta|, 50); l.1073: pairing rho, 1 - rho.
  - l.1081-1091 (9.48): f(tau) = 5.13 |tau| e^{-0.1598|tau|} (+ Gaussian term only
    when |tau| < (3/2)(pi delta)^2; absent for delta = 0).
  - l.1099-1103 (9.49); l.536-538 (9.25) g_chi(T) = 0.5 log qT + 17.7.
  - l.1109-1131 (9.50)-(9.51): c = 0.1598, c1 = pi/2, y = T0, a <= 1.299.
  - l.1228-1239 (9.54): first line coefficients 1.487, 2.194, 2.566, bound 1.578,
    "using several times the assumption that T0 >= 4 pi^2 |delta|".
Tests: (a) zeta, delta = 0, T0 = 52.97, zeros via mpmath.zetazero;
(b) (9.51) at T0 = 50 (the log q parts of both sides are equal, so q drops out);
(c) first line of (9.54) at q = 1, |delta| = 5, T0 = 50 pi (= 10 pi |delta|);
(d) chi mod 5 with chi(2) = i via mpmath.dirichlet.

Confirms if (a), (b), (c) each fail as printed and (d) shows 1 - rho is not a
zero for a zero rho.

Run: PYTHONPATH=<mpmath dir> python3 -s lemma_9_3_1.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 25
c = mp.mpf("0.1598")
k21 = mp.mpf("5.13")

# (a)
zeros = []
n = 1
while True:
    t = mp.zetazero(n).imag
    if t > 400:
        break
    zeros.append(t)
    n += 1
q, T0 = 1, mp.mpf("52.97")
f = lambda T: k21 * T * mp.e ** (-c * T)
L = mp.fsum(f(t) for t in zeros if t > T0)
R = mp.quad(lambda T: f(T) * (mp.log(q * T / (2 * mp.pi)) / (2 * mp.pi) + 1 / (4 * T)), [T0, 400, mp.inf])
lemma_exp = 6.11 * T0 * mp.log(q * T0 / (2 * mp.pi)) * mp.e ** (-c * T0)
print("(a) zeta, T0=52.97: LHS(9.49) =", mp.nstr(L, 7), " RHS(9.49) =", mp.nstr(R, 7),
      " (lemma's 6.11 term =", mp.nstr(lemma_exp, 7), ")")
ok_a = L > R

# (b) (9.51) at T0 = 50, in units of e^{-c T0}/(2 pi), q-independent part
T0 = mp.mpf(50)
c1 = mp.pi / 2
J = mp.e ** (c * T0) * mp.quad(lambda T: T * mp.log(T) * mp.e ** (-c * T), [T0, mp.inf])
const = mp.e ** (c * T0) * 2 * mp.pi * mp.quad(lambda T: mp.mpf(1) / 4 * mp.e ** (-c * T), [T0, mp.inf])
a = (mp.log(T0) / c + 1 / c + c1 / T0) / (mp.log(T0) / c - 1 / (c ** 2 * T0))
lhs_b = J + const
rhs_b = (T0 / c + a / c ** 2) * mp.log(T0)
print("(b) T0=50: J + 2pi*(1/4)int e^{-cT} = %s (= J + pi/(2c)); (T0/c + a/c^2) log T0 = %s, a = %s"
      % (mp.nstr(lhs_b, 9), mp.nstr(rhs_b, 9), mp.nstr(a, 7)))
ok_b = lhs_b > rhs_b

# (c) first line of (9.54) / (T0 log(qT0/2pi)) at q=1, |delta|=5, T0=10 pi |delta|
q, d = 1, mp.mpf(5)
T0 = 10 * mp.pi * d
first = ((1.487 * T0 + 2.194 * d) * mp.log(q * d / 2) + 1.487 * T0 * mp.log(T0 / (mp.pi * d))
         + 2.566 * d * mp.log(mp.e * T0 / (mp.pi * d)))
ratio_c = first / (T0 * mp.log(q * T0 / (2 * mp.pi)))
second_c = 1.487 + 2.566 * (1 + 1 / mp.log(T0 / (mp.pi * d))) / (T0 / d)
print("(c) q=1, |delta|=5, T0=50pi: first line of (9.54)/(T0 log(qT0/2pi)) = %s; second line coefficient %s; printed 1.578"
      % (mp.nstr(ratio_c, 6), mp.nstr(second_c, 6)))
ok_c = ratio_c > 1.578

# (d)
chi = [0, 1, 1j, -1j, -1]
t0 = mp.findroot(lambda t: mp.dirichlet(mp.mpf(0.5) + 1j * t, chi), mp.mpf("6.18358"))
rho = mp.mpf(0.5) + 1j * mp.re(t0)
la, lb = abs(mp.dirichlet(rho, chi)), abs(mp.dirichlet(1 - rho, chi))
print("(d) chi mod 5, chi(2)=i: |L(rho)| = %s, |L(1-rho)| = %s at rho = 1/2+%si" % (mp.nstr(la, 3), mp.nstr(lb, 5), mp.nstr(mp.im(rho), 9)))
ok_d = la < 1e-10 and lb > 1

if ok_a and ok_b and ok_c and ok_d:
    print("CONFIRMED: (9.49) fails for zeta at T0 = 52.97 (%s > %s), (9.51) fails at T0 = 50 (%s > %s), the first line "
          "of (9.54) gives %s > 1.578 at T0 = 10 pi |delta|, and 1 - rho is not a zero for chi mod 5 with chi(2) = i."
          % (mp.nstr(L, 5), mp.nstr(R, 5), mp.nstr(lhs_b, 6), mp.nstr(rhs_b, 6), mp.nstr(ratio_c, 4)))
else:
    print("NOT CONFIRMED: parts (a,b,c,d) = %s, %s, %s, %s" % (ok_a, ok_b, ok_c, ok_d))
