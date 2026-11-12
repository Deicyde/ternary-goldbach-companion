"""Check of [H, Lemma 9.2.1] (lem:garmonas), proof.

Claim: the proof fails for every chi: its step (9.35) (Lemma 9.1.3's clause
for real decreasing f) drops the boundary term f(T0)g_chi(T0) and is false
even for q = 1; for complex chi the pairing rho <-> 1 - rho used before (9.33)
also fails. A valid route (bound each zero by f, count all zeros, keep the
boundary term) gives twice the printed bound plus 2f(T0)(0.5 log qT0 + 17.7),
about 20 times the printed exponential term at q = 1, T0 = 50.

Book inputs (expform.tex):
  - l.770-786: Lemma 9.2.1, T0 >= 50, bound log(qT0/2pi)(3.53 e^{-0.1598 T0} + ...).
  - l.809-812: pairing "non-trivial zeros come in pairs rho, 1 - rho".
  - l.819-823 (9.34): f(tau) = 3.001 e^{-0.1065(tau/(pi delta))^2} + 3.286 e^{-0.1598|tau|}.
  - l.830-833 (9.35); l.536-538 (9.25) g_chi(T) = 0.5 log qT + 17.7.
Tests: (i) zeta, delta = 0.01, T0 = 52.9 (zeros via mpmath.zetazero);
(ii) chi mod 5 with chi(2) = i (values 1, i, -i, -1 at n = 1,2,3,4), L via
mpmath.dirichlet: is L(1 - rho) = 0 at the zero rho = 1/2 + 6.18358i?
(iii) size of the repaired exponential coefficient at q = 1, T0 = 50.

Confirms if (i) the left side of (9.35) exceeds its right side and (ii)
|L(1-rho, chi)| is far from 0 while |L(rho, chi)| ~ 0.

Run: PYTHONPATH=<mpmath dir> python3 -s lemma_9_2_1.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 25
c = mp.mpf("0.1598")
delta = mp.mpf("0.01")
f = lambda t: 3.001 * mp.e ** (-0.1065 * (t / (mp.pi * delta)) ** 2) + 3.286 * mp.e ** (-c * abs(t))
g = lambda q, T: 0.5 * mp.log(q * T) + 17.7

# (i) step (9.35) for zeta
zeros = []
n = 1
while True:
    t = mp.zetazero(n).imag
    if t > 300:
        break
    zeros.append(t)
    n += 1
T0 = mp.mpf("52.9")
L = mp.fsum(f(t) for t in zeros if t > T0)
R = mp.quad(lambda T: f(T) * (mp.log(T / (2 * mp.pi)) / (2 * mp.pi) + 1 / (4 * T)), [T0, 300, mp.inf])
print("(i) zeta, delta=0.01, T0=52.9: sum_{gamma>T0} f(gamma) =", mp.nstr(L, 8), " RHS(9.35) =", mp.nstr(R, 8))
ok1 = L > R

# (ii) pairing for complex chi mod 5
chi = [0, 1, 1j, -1j, -1]
rho0 = mp.findroot(lambda t: mp.dirichlet(mp.mpf(0.5) + 1j * t, chi), mp.mpf("6.18358"))
rho = mp.mpf(0.5) + 1j * mp.re(rho0)
a = abs(mp.dirichlet(rho, chi))
b = abs(mp.dirichlet(1 - rho, chi))
bbar = abs(mp.dirichlet(1 - mp.conj(rho), chi))
print("(ii) chi mod 5, chi(2)=i: rho = 1/2 + %si, |L(rho)| = %s, |L(1-rho)| = %s, |L(1-conj rho)| = %s"
      % (mp.nstr(mp.im(rho), 10), mp.nstr(a, 3), mp.nstr(b, 6), mp.nstr(bbar, 3)))
ok2 = a < 1e-10 and b > 1

# (iii) repaired vs printed exponential coefficient (units of e^{-0.1598 T0}), q = 1, T0 = 50
q, T0 = 1, 50
printed = 3.53 * mp.log(q * T0 / (2 * mp.pi))
repaired = 2 * printed + 2 * 3.286 * g(q, T0)
print("(iii) q=1, T0=50: printed coefficient %s, repaired %s (ratio %s)"
      % (mp.nstr(printed, 5), mp.nstr(repaired, 5), mp.nstr(repaired / printed, 4)))

if ok1 and ok2:
    print("CONFIRMED: step (9.35) of the proof fails for zeta (%s > %s at T0 = 52.9), and for chi mod 5 with "
          "chi(2) = i, 1 - rho is not a zero (|L(1-rho)| = %s)." % (mp.nstr(L, 5), mp.nstr(R, 5), mp.nstr(b, 4)))
else:
    print("NOT CONFIRMED: step (9.35) held for zeta or the pairing held for chi mod 5.")
