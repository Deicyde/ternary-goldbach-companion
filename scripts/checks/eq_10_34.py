"""Check of [H, Eq (10.34)] (eq:teresa), the sqrt(B_+) sqrt(B_*) term.

Claim: the bound for the error part of S_{eta_1} with S_{eta_2}, S_{eta_3}
replaced by their main terms (10.32) is unjustified: those main terms do not
depend on a, so the sum sum_a err_1(a) e(-Na/q) appears, which the l2 data
bound only by sqrt(phi(q)) x E_+, not x E_+.  Arguing as for the S_{eta_2}
term gives sqrt(L_{r,delta0}) <= 3.6875 |eta_+|_2 in place of
sqrt(B_+) = 1.6812 |eta_+|_2 (r = 150000); in Section 14.2 line 2 of (10.36)
rises from 1.7316e-6/kappa to 2.333e-6/kappa and (14.27) survives.

Book inputs:
  - intmajarc.tex:870-897 S_{eta_2} step, (10.32) main term mu(q)/phi(q)
                          eta^(-delta) x, (10.33) with weights mu^2/phi^2 <= 2.82643.
  - intmajarc.tex:898-917 "in the same way" for S_{eta_1}; (10.34), B_+ = 2.82643|eta_+|_2^2.
  - intmajarc.tex:640-643 L_{r,delta0} <= 2|eta|_2^2 sum_{q<=r odd} mu^2/phi.
  - conclusion.tex:428-437 line 2 of (10.36): E_* = 1.33805e-8/kappa, E_+ =
                          2.3922e-8, A = 8.7806, |eta_+|_2 <= 0.80014,
                          |eta_*|_2^2 <= 1.77082/kappa, kappa = 49.
  - conclusion.tex:455-477 (14.26), (14.27): 2.9387e-5 sqrt(pi/2)/kappa,
                          C0 C >= (1.0594003 - 0.001102)/kappa, claimed >= 1.058259/kappa.

(a) Toy: q = 101, N = 7, E_1(a) = phi^{-1} sum_chi chi(a) tau(chibar) e_chi with
|e_chi| <= 1/sqrt(q*) (x E_+ = 1) and aligned phases; checks sum_a |E_1|^2 <= 1
and compares |sum_a E_1(a) e(-Na/q)| with 1.  (b) sqrt(2 sum mu^2/phi) at
r = 150000.  (c) Section 14.2 with sqrt(B_+) replaced by sqrt(L).
Confirms if (a) exceeds 1 (near sqrt(phi(q)) = 10), (b) gives 3.6875 > 1.6812,
and (c) gives about 2.333e-6/kappa with (14.27) still >= 1.058259/kappa.

Run: python3 -I eq_10_34.py

Ported from a 2026-11-06 check script.
"""
import cmath
from math import pi, sqrt, log

# (a) toy
q, N = 101, 7
phiq = q - 1
g = 2  # primitive root mod 101
ind, t = {}, 1
for j in range(phiq):
    ind[t] = j
    t = t * g % q
e = lambda y: cmath.exp(2j * pi * y)
E1 = {a: 0j for a in range(1, q)}
for k in range(phiq):
    chi = {a: e(ind[a] * k / phiq) for a in range(1, q)}
    tau_bar = sum(chi[a].conjugate() * e(a / q) for a in range(1, q))
    tau_N = sum(chi[a] * e(-N * a / q) for a in range(1, q))
    mag = 1.0 if k == 0 else 1 / sqrt(q)
    ph = tau_bar * tau_N
    echi = mag * ph.conjugate() / abs(ph)
    for a in range(1, q):
        E1[a] += chi[a] * tau_bar * echi / phiq
l2 = sum(abs(v) ** 2 for v in E1.values())
asum = abs(sum(E1[a] * e(-N * a / q) for a in range(1, q)))
print("(a) q=101: sum_a|E_1(a)|^2 = %.6f (<= (xE_+)^2 = 1); |sum_a E_1(a)e(-Na/q)| = %.4f; book needs <= 1; sqrt(phi) = %.1f"
      % (l2, asum, sqrt(phiq)))
ok_a = l2 <= 1 + 1e-9 and asum > 1

# (b) sum_{q<=r odd} mu^2/phi
r = 150000
phi = list(range(r + 1))
sqf = [True] * (r + 1)
for p in range(2, r + 1):
    if phi[p] == p:
        for m in range(p, r + 1, p):
            phi[m] -= phi[m] // p
        for m in range(p * p, r + 1, p * p):
            sqf[m] = False
Sodd = sum(1.0 / phi[n] for n in range(1, r + 1, 2) if sqf[n])
sL = sqrt(2 * Sodd)
sB = sqrt(2.82643)
print("(b) sum_{q<=r odd} mu^2/phi = %.7f ; sqrt(L)/|eta_+|_2 <= %.6f vs sqrt(B_+)/|eta_+|_2 = %.6f" % (Sodd, sL, sB))
ok_b = sL > sB

# (c) Section 14.2
kap, Es, Ep, A, np_, ns = 49, 1.33805e-8, 2.3922e-8, 8.7806, 0.80014, sqrt(1.77082)
line_book = Es * A + Ep * 1.6812 * (sqrt(A) + 1.6812 * np_) * ns * sqrt(kap)  # times 1/kappa
line_corr = Es * A + Ep * (sqrt(A) + sL * np_) * sB * ns * sqrt(kap)
first = 2.9387e-5 * sqrt(pi / 2)
xp = 4.9e26
tail = 43 * log(xp) ** 2 / xp * kap
low_book = 1.0594003 - 0.001102 - (first + line_book + tail)
low_corr = 1.0594003 - 0.001102 - (first + line_corr + tail)
print("(c) line 2 of (10.36): book %.6g/kappa, corrected %.6g/kappa" % (line_book, line_corr))
print("    total error (14.26): book %.6g/kappa, corrected %.6g/kappa" % (first + line_book + tail, first + line_corr + tail))
print("    (14.27) lower bound: book %.7f/kappa, corrected %.7f/kappa (printed 1.058259)" % (low_book, low_corr))
ok_c = abs(line_corr - 2.333e-6) < 1e-9 and low_corr >= 1.058259

if ok_a and ok_b and ok_c:
    print("CONFIRMED: the a-sum of the S_{eta_1} error against a-independent main terms reaches %.2f x E_+ for q=101 (book's step needs <= x E_+), the valid replacement for sqrt(B_+) is %.4f|eta_+|_2 not 1.6812|eta_+|_2, and line 2 of (10.36) becomes %.4g/kappa while (14.27) still holds (%.7f >= 1.058259)." % (asum, sL, line_corr, low_corr))
else:
    print("NOT CONFIRMED: ok_a=%s ok_b=%s ok_c=%s." % (ok_a, ok_b, ok_c))
