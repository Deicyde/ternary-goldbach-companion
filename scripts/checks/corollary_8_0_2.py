"""Check of [H, Corollary 8.0.2] (bounds for |F_delta(s+k)| + |F_delta((1-s)+k)|).

Claim: the statement survives, but the printed proof has three defects.
(i) For rho < 3/2 the good-sign member of the pair is bounded via (8.3) -> (8.50), and
(8.3) is false for small rho (e.g. s = 1+20i, delta = 2), although (8.50) holds there by
a wide margin. (ii) kappa_{1,0}, kappa_{2,0} use c_2 <= 3.15692, 5.02186, which pair the
beta = pi/5 I_2 term with the beta = pi/6 I_3 term; one contour with the printed I_3
estimate gives c_2 = 3.19279, 5.05219 and kappa_{1,0} = 4.958 > 4.903,
kappa_{2,0} = 8.007 > 7.96 (a sharper I_3 estimate repairs this). (iii) The proof's final
display has kappa_{k,1}|tau|^k for the statement's |tau|^{k/2} (typo, not checked here).

Book inputs (mellintran.tex):
  - l.29-58 (8.1)-(8.2), upsilon(rho) = sqrt((1+sqrt(rho^2+1))/2), l = -2 pi delta,
    rho = 4 tau/l^2; l.60-70 (8.3) |F| <= |x0|^{-sigma} e^{-l^2/2} |Gamma(s)| e^{pi|tau|/2}
    ((1 + pi/2^{3/2}) e^{-pi|tau|/4} + (1/2) e^{-pi|tau|}), (8.4).
  - l.498-502 (8.28): x0 = (|l|/2) sqrt((j-1)/2), j = sqrt(1+rho^2).
  - l.112-140 Cor 8.0.2: sigma in [0,1], |tau| >= 20, k = 0,1,2, bounds
    kappa_{k,0}(|tau|/|l|)^k e^{-0.1065(2|tau|/|l|)^2} (rho < 3/2) and
    kappa_{k,1}|tau|^{k/2} e^{-0.1598|tau|} (rho >= 3/2), kappa = 3.001, 4.903, 7.96;
    3.286, 4.017, 5.13.
  - l.1308-1345 (8.50): for sgn(delta) = sgn(tau), rho <= 3/2:
    |F| <= |Gamma(s)| e^{pi tau/2} e^{-0.1598 tau} 4e-7/l^sigma.
  - l.1385-1445: (8.52) Gamma factors 2.51868, 2.53596, 2.5881; c_2 <= 1.94511, 3.15692,
    5.02186; kappa_{k,0} <= (4e-7 + c_2) * Gamma factor * sqrt(3/8).
  - l.894-956: beta = pi/6 or pi/5, I_2 and I_3 bounds; (8.42) c_2.
F is computed as e^{-pi^2 delta^2} Gamma(s) U(s - 1/2, -2 pi i delta) (mpmath pcfu) and
cross-checked against the power series sum (2 pi i delta)^n/n! 2^{(s+n)/2-1} Gamma((s+n)/2).

Confirms if: (i) at s = 1+20i, delta = 2, |F| exceeds the (8.3) bound but is below the
(8.50) bound; (ii) the one-contour c_2 values push kappa_{1,0}, kappa_{2,0} above the
printed values while the printed chain gives them; and the statement of Cor 8.0.2 holds
(ratio pair/bound < 1) on a grid of tau, sigma, k, rho covering both regimes.

Run: PYTHONPATH=<dir containing mpmath> python3 -s corollary_8_0_2.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp
from mpmath import mpf, mpc, pi, exp, sqrt, sin, tan, sec, gamma, fabs

mp.mp.dps = 30


def F_pcfu(s, delta):
    with mp.workdps(60):
        r = exp((pi * 1j * delta) ** 2) * gamma(s) * mp.pcfu(s - mpf(1) / 2, -2j * pi * delta)
    return +r


def F_series(s, delta):
    z = 2j * pi * mpf(delta)
    dps = int(40 + float((2 * pi * delta) ** 2 / 2) / 2.3 + 2 * abs(float(s.imag)))
    with mp.workdps(dps):
        s = mpc(s)
        tot, pre, n, mx = mpc(0), mpc(1), 0, mpf(0)
        while True:
            t = pre * mpf(2) ** ((n + s) / 2) * gamma((n + s) / 2)
            tot += t
            a = fabs(t)
            mx = max(mx, a)
            if n > 10 and n > 2 * fabs(z) ** 2 and a < mx * mpf(10) ** (-dps):
                break
            n += 1
            pre *= z / n
        r = tot / 2
    return +r


# (i) the (8.3) -> (8.50) step at s = 1 + 20i, delta = 2 (sgn delta = sgn tau)
sigma, tau, delta = mpf(1), mpf(20), mpf(2)
s = mpc(sigma, tau)
ell = -2 * pi * delta
rho = 4 * tau / ell ** 2
j = sqrt(1 + rho ** 2)
x0 = fabs(ell) / 2 * sqrt((j - 1) / 2)
Fp, Fs = F_pcfu(s, delta), F_series(s, delta)
agree0 = fabs(Fp - Fs) <= mpf(10) ** -20 * fabs(Fs)
G = fabs(gamma(s)) * exp(pi / 2 * tau)
rhs83 = x0 ** -sigma * exp(-ell ** 2 / 2) * G * ((1 + pi / mpf(2) ** 1.5) * exp(-pi * tau / 4)
                                                 + exp(-pi * tau) / 2)
x0b = mpf('0.84473') * tau / fabs(ell)
rhs83b = x0b ** -sigma * exp(-ell ** 2 / 2) * G * ((1 + pi / mpf(2) ** 1.5) * exp(-pi * tau / 4)
                                                   + exp(-pi * tau) / 2)
rhs850 = G * exp(-mpf('0.1598') * tau) * mpf('4e-7') / fabs(ell) ** sigma
print("(i) s = 1+20i, delta = 2: rho = %s, x0 = %s" % (mp.nstr(rho, 7), mp.nstr(x0, 7)))
print("    |F| = %s (pcfu) = %s (series), agree: %s" % (mp.nstr(fabs(Fp), 10), mp.nstr(fabs(Fs), 10), agree0))
print("    (8.3) RHS = %s (exact x0), %s (x0 >= 0.84473 tau/|l|)" % (mp.nstr(rhs83, 6), mp.nstr(rhs83b, 6)))
print("    (8.50) RHS = %s" % mp.nstr(rhs850, 6))
part_i = agree0 and fabs(Fs) > max(rhs83, rhs83b) and fabs(Fs) < rhs850

# (ii) c_2 and kappa_{1,0}, kappa_{2,0}
A6 = lambda sg: mpf(2) ** (sg + mpf(1) / 2)
A5 = lambda sg: sqrt(sec(2 * pi / 5)) / sin(pi / 5) ** sg
C6 = lambda sg, t: exp(-t / 6) * sqrt(3) ** sg
C5 = lambda sg, t: exp(-(1 - tan(pi / 5) ** 2) / 4 * t) / tan(pi / 5) ** sg
printed = lambda sg, t: (1 + min(A6(sg), A5(sg)) + C6(sg, t)) / 2
single = lambda sg, t: (1 + min(A6(sg) + C6(sg, t), A5(sg) + C5(sg, t))) / 2
c2p = [printed(sg, 20) for sg in (1, 2, 3)]
c2s = [single(sg, 20) for sg in (1, 2, 3)]
print("(ii) tau = 20: printed-formula c_2 = %s; one-contour c_2 = %s"
      % ([mp.nstr(v, 7) for v in c2p], [mp.nstr(v, 7) for v in c2s]))
r38 = sqrt(mpf(3) / 8)
kp = [(mpf('4e-7') + mpf(c)) * mpf(g) * r38 for c, g in (('1.94511', '2.51868'), ('3.15692', '2.53596'),
                                                          ('5.02186', '2.5881'))]
ks = [(mpf('4e-7') + c) * mpf(g) * r38 for c, g in zip(c2s, ('2.51868', '2.53596', '2.5881'))]
print("    printed chain kappa_{k,0} = %s (book 3.001, 4.903, 7.96)" % [mp.nstr(v, 7) for v in kp])
print("    one-contour   kappa_{k,0} = %s" % [mp.nstr(v, 7) for v in ks])
part_ii = (kp[0] <= mpf('3.001') and kp[1] <= mpf('4.903') and kp[2] <= mpf('7.96')
           and ks[1] > mpf('4.903') and ks[2] > mpf('7.96')
           and fabs(c2p[1] - mpf('3.15692')) < mpf('1e-5') and fabs(c2p[2] - mpf('5.02186')) < mpf('1e-5'))

# statement check
K0 = [mpf('3.001'), mpf('4.903'), mpf('7.96')]
K1 = [mpf('3.286'), mpf('4.017'), mpf('5.13')]
worst = (mpf(0), None)
npts = 0
cross_ok = True
for tau in (mpf(20), mpf(30), mpf(60)):
    for sigma in (mpf(0), mpf('0.02'), mpf('0.5'), mpf('0.98'), mpf(1)):
        for rho in ('0.05', '0.2', '0.5', '1', '1.4', '1.49', '1.5', '2', '5', '20', '100'):
            rho = mpf(rho)
            ell = sqrt(4 * tau / rho)
            delta = ell / (2 * pi)          # delta > 0; delta < 0 is the pair at 1 - sigma
            for k in range(3):
                a = F_pcfu(mpc(sigma + k, tau), delta)
                b = F_pcfu(mpc(1 - sigma + k, -tau), delta)
                if npts % 37 == 0:
                    a2 = F_series(mpc(sigma + k, tau), delta)
                    b2 = F_series(mpc(1 - sigma + k, -tau), delta)
                    cross_ok &= (fabs(a - a2) <= mpf(10) ** -15 * fabs(a2) + mpf(10) ** -300 and
                                 fabs(b - b2) <= mpf(10) ** -15 * fabs(b2) + mpf(10) ** -300)
                pair = fabs(a) + fabs(b)
                if rho < mpf('1.5'):
                    bnd = K0[k] * (tau / ell) ** k * exp(-mpf('0.1065') * (2 * tau / ell) ** 2)
                else:
                    bnd = K1[k] * tau ** (mpf(k) / 2) * exp(-mpf('0.1598') * tau)
                r = pair / bnd
                npts += 1
                if r > worst[0]:
                    worst = (r, (float(tau), float(sigma), float(rho), k))
print("statement: %d points, max pair/bound = %s at (tau, sigma, rho, k) = %s; series cross-check ok: %s"
      % (npts, mp.nstr(worst[0], 6), worst[1], cross_ok))
stmt_ok = worst[0] < 1 and cross_ok

if part_i and part_ii and stmt_ok:
    print("CONFIRMED: the statement of Cor 8.0.2 holds on the grid (max ratio %s), but at s = 1+20i, "
          "delta = 2 the cited (8.3) is false (|F| = %s > %s) though (8.50) holds (%s), and one-contour "
          "c_2 values give kappa_{1,0} = %s > 4.903, kappa_{2,0} = %s > 7.96."
          % (mp.nstr(worst[0], 3), mp.nstr(fabs(Fs), 4), mp.nstr(rhs83, 4), mp.nstr(rhs850, 4),
             mp.nstr(ks[1], 5), mp.nstr(ks[2], 5)))
else:
    print("NOT CONFIRMED: part_i=%s part_ii=%s statement_ok=%s (max ratio %s)."
          % (part_i, part_ii, stmt_ok, mp.nstr(worst[0], 5)))
