"""Check of [H, Eq (8.2)] (the constant c_{2,sigma,tau} of Theorem 8.0.1).

Claim: in deriving c_2 (before (8.41)), the min(2^{sigma+1/2},
sqrt(sec(2pi/5))/sin(pi/5)^sigma) picks the contour angle beta = pi/5 when
sigma > 1.4875, but the third term e^{-tau/6} 3^{sigma/2} is the I_3 bound for
beta = pi/6; for beta = pi/5 the book's I_3 estimate is
e^{-0.11803 tau}/tan(pi/5)^sigma.  With one contour per bound, the printed
derivation gives c_2 = 5.05219 (not 5.02186) at tau = 20, sigma = 3, and
kappa_{2,0} = 8.007 > 7.96, kappa_{1,0} = 4.958 > 4.903.  The printed c_2
survives: y_0 >= ell improves the I_3 bound to e^{-0.6295 tau}/tan(pi/5)^sigma.

Book inputs (mellintran.tex):
  - l.894-911: beta = pi/6 or pi/5 for rho <= 3/2, and the I_2 bound
    min(sqrt((pi/2)/cos(2pi/5)) |ell sin(pi/5)|^{-sigma}, sqrt(pi)|ell/2|^{-sigma}).
  - l.915-938: I_3 <= |x_1|^{-sigma} sqrt(pi/2) e^{-(1-tan^2 beta) tau/4}
    e^{-Re phi(u_{0,+})}, x_1 >= tan(beta) max(sqrt(tau), ell); also
    (1/2)(1-tan^2 beta) y_0^2 is the exponent gain.
  - l.947-956 and l.51-55 (8.2): c_2 = (1/2)(1 + min(2^{sigma+1/2},
    sqrt(sec 2pi/5)/sin(pi/5)^sigma) + e^{-tau/6}/(1/sqrt 3)^sigma).
  - l.498 (8.21): y_0 = Im u_{0,+} = (ell/2)(1 + upsilon(rho)) for ell > 0.
  - l.1380-1445 (proof of Cor 8.0.2): |tau| >= 20, c_2 <= 3.15692 (sigma in
    [1,2]), 5.02186 (sigma in [2,3]), Gamma factors 2.53596, 2.5881,
    kappa_{1,0} <= (4e-7 + 3.15692) 2.53596 sqrt(3/8) <= 4.903,
    kappa_{2,0} <= (4e-7 + 5.02186) 2.5881 sqrt(3/8) <= 7.96.
  - l.29-36 (8.1) for the numerical test of the printed bound.
All bounds are normalised by sqrt(pi/2) ell^{-sigma} e^{-Re phi(u_{0,+})}.

Confirms if: (a) for sigma > sigma* = 1.4875 and tau >= 20 the beta = pi/5
I_3 term exceeds the printed third term, and the one-contour c_2 values exceed
the printed ones and push kappa_{1,0}, kappa_{2,0} above 4.903, 7.96 (the gap);
(b) the repaired I_3 term is <= the printed third term for all tau, sigma >= 0
(the printed c_2 survives); (c) the computed |F_delta(s)| is below the printed
(8.1) second-case bound at sample points with sigma in [1.5, 3].

Run: PYTHONPATH=<dir containing mpmath> python3 -s eq_8_2.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp
from mpmath import mpf, mpc, pi, exp, sqrt, sin, tan, sec, log, acos, gamma, fabs

mp.mp.dps = 40

A6 = lambda sg: mpf(2) ** (sg + mpf(1) / 2)                     # I_2, beta = pi/6
A5 = lambda sg: sqrt(sec(2 * pi / 5)) / sin(pi / 5) ** sg       # I_2, beta = pi/5
g6 = (1 - tan(pi / 6) ** 2) / 4
g5 = (1 - tan(pi / 5) ** 2) / 4
C6 = lambda sg, t: exp(-g6 * t) / tan(pi / 6) ** sg             # I_3, beta = pi/6 (printed)
C5 = lambda sg, t: exp(-g5 * t) / tan(pi / 5) ** sg             # I_3, beta = pi/5 (book's estimate)
g5r = mpf(4) / 3 * (1 - tan(pi / 5) ** 2)
C5r = lambda sg, t: exp(-g5r * t) / tan(pi / 5) ** sg           # I_3, beta = pi/5, using y_0 >= ell

print("(1-tan^2(pi/6))/4 = %s (printed 1/6); 1/tan(pi/6) = %s (printed sqrt 3)" % (mp.nstr(g6, 10), mp.nstr(1 / tan(pi / 6), 10)))
print("(1-tan^2(pi/5))/4 = %s; 1/tan(pi/5) = %s" % (mp.nstr(g5, 10), mp.nstr(1 / tan(pi / 5), 10)))
sstar = log(sqrt(sec(2 * pi / 5)) / sqrt(2)) / log(2 * sin(pi / 5))
print("min switches to beta = pi/5 at sigma* = %s" % mp.nstr(sstar, 9))
print("C5 > C6 iff tau > %s sigma" % mp.nstr((log(tan(pi / 6) / tan(pi / 5))) / (g6 - g5) * -1, 8))

printed = lambda sg, t: (1 + min(A6(sg), A5(sg)) + C6(sg, t)) / 2
consistent = lambda sg, t: (1 + min(A6(sg) + C6(sg, t), A5(sg) + C5(sg, t))) / 2
repaired = lambda sg, t: (1 + min(A6(sg) + C6(sg, t), A5(sg) + C5r(sg, t))) / 2
gap = True
print("\ntau = 20 (worst case of tau >= 20):")
for sg in (1, 2, 3):
    p, c, r = printed(sg, 20), consistent(sg, 20), repaired(sg, 20)
    print("  sigma=%d: printed c_2=%s  one-contour (book I_3)=%s  one-contour (repaired I_3)=%s" % (
        sg, mp.nstr(p, 7), mp.nstr(c, 7), mp.nstr(r, 7)))
    if sg >= 2:
        gap = gap and c > p and C5(sg, 20) > C6(sg, 20)
k1p = (mpf('4e-7') + printed(2, 20)) * mpf('2.53596') * sqrt(mpf(3) / 8)
k1c = (mpf('4e-7') + consistent(2, 20)) * mpf('2.53596') * sqrt(mpf(3) / 8)
k2p = (mpf('4e-7') + printed(3, 20)) * mpf('2.5881') * sqrt(mpf(3) / 8)
k2c = (mpf('4e-7') + consistent(3, 20)) * mpf('2.5881') * sqrt(mpf(3) / 8)
print("  kappa_{1,0}: printed chain %s, one-contour %s (book: <= 4.903)" % (mp.nstr(k1p, 7), mp.nstr(k1c, 7)))
print("  kappa_{2,0}: printed chain %s, one-contour %s (book: <= 7.96)" % (mp.nstr(k2p, 7), mp.nstr(k2c, 7)))
gap = gap and k1c > mpf('4.903') and k2c > mpf('7.96') and k1p <= mpf('4.903') and k2p <= mpf('7.96')
# gap holds throughout sigma in (sigma*, 3], tau >= 20
gap_range = all(C5(sg, t) > C6(sg, t) for sg in (sstar + mpf('0.001'), mpf(2), mpf(3)) for t in (20, 50, 100))

print("\nRepair: y_0 = (ell/2)(1+upsilon) >= ell, ell^2 = 4tau/rho >= 8tau/3, so the I_3 exponent is >= %s tau" % mp.nstr(g5r, 8))
rep_ok = g5r >= g6 and 1 / tan(pi / 5) <= sqrt(3)
grid_rep = all(C5r(sg, t) <= C6(sg, t) and repaired(sg, t) <= printed(sg, t) + mpf(10) ** -30
               for sg in [mpf(k) / 10 for k in range(0, 31)] for t in [mpf(k) for k in range(0, 201, 5)])
print("  %s >= 1/6 and %s <= sqrt 3: %s; repaired c_2 <= printed c_2 on grid: %s" % (
    mp.nstr(g5r, 7), mp.nstr(1 / tan(pi / 5), 7), rep_ok, grid_rep))
print("  upsilon(3/2) = %s, arg u_{0,+} lower bound 1.28842 vs 2 pi/5 = %s" % (
    mp.nstr(sqrt((1 + sqrt(1 + mpf(9) / 4)) / 2), 7), mp.nstr(2 * pi / 5, 7)))


def F_pcfu(sigma, tau, delta):
    with mp.workdps(60):
        s = mpc(sigma, tau)
        r = exp((pi * 1j * delta) ** 2) * gamma(s) * mp.pcfu(s - mpf(1) / 2, -2j * pi * delta)
    return +r


def F_series(sigma, tau, delta):
    z = 2j * pi * mpf(delta)
    dps = int(40 + float((2 * pi * delta) ** 2 / 2) / 2.3 + 2 * abs(float(tau)))
    with mp.workdps(dps):
        s = mpc(sigma, tau)
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


def bound81_case2(sigma, tau, ell):
    rho = 4 * tau / ell ** 2
    ups = sqrt((1 + sqrt(rho ** 2 + 1)) / 2)
    E = (acos(1 / ups) - 2 * (ups - 1) / rho) / 2
    return fabs(gamma(mpc(sigma, tau))) * exp(pi / 2 * tau) * exp(-E * tau) * printed(sigma, tau) / ell ** sigma


print("\n|F_delta(s)| / printed (8.1) case-2 bound (tau > 0, delta < 0, so ell > 0):")
worst = mpf(0)
agree = True
for sg in (mpf('1.5'), mpf(2), mpf('2.5'), mpf(3)):
    for tau in (20, 40):
        for rho in ('0.05', '0.2', '0.5', '1', '1.5'):
            ell = sqrt(4 * mpf(tau) / mpf(rho))
            delta = -ell / (2 * pi)
            F = F_pcfu(sg, tau, delta)
            if rho in ('0.5', '1.5') and tau == 20:
                G = F_series(sg, tau, delta)
                agree = agree and fabs(F - G) <= mpf(10) ** -20 * fabs(G)
            worst = max(worst, fabs(F) / bound81_case2(sg, tau, ell))
print("  max ratio = %s (series/pcfu agreement: %s)" % (mp.nstr(worst, 6), agree))

if gap and gap_range and rep_ok and grid_rep and worst < 1 and agree:
    print("CONFIRMED: for sigma > 1.48748 the printed c_2 mixes the beta=pi/5 I_2 bound with the beta=pi/6 I_3 bound (one contour gives c_2 = %s at sigma=3, tau=20, kappa_{2,0} = %s > 7.96), but y_0 >= ell gives an I_3 bound e^{-0.6295 tau}/tan(pi/5)^sigma that restores the printed c_2." % (
        mp.nstr(consistent(3, 20), 6), mp.nstr(k2c, 5)))
else:
    print("NOT CONFIRMED: gap=%s (range %s), repair=%s/%s, numeric max ratio=%s, agree=%s." % (
        gap, gap_range, rep_ok, grid_rep, mp.nstr(worst, 5), agree))
