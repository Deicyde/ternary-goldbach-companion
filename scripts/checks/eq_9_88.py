"""Check of [H, Eq (9.88)] (bound for F_x(s), proof of Prop 9.5.1).

Claim: (9.88) is false as printed. (i) Its second line has e^{-pi|tau|/2},
but applying (9.87) at w = s/2+1, where |Im w| = |tau|/2, only gives
e^{-pi|tau|/4}, and the true |F_x(s)| decays at that rate. (ii) The digamma
display before (9.88) drops i*arg(w) (about +-i*pi/2) from log w, so
"Gamma'/Gamma(w) = log|Im w| + O*(0.609/|Im w|)" is false as a complex
statement and the first line of (9.88) fails slightly for large |tau|.
The corrected bound 2.542(log x + 1/2 log|tau| - 0.297)(|tau|/2)e^{-pi|tau|/4}
holds for x >= 10^8, -2 <= sigma <= 1, |tau| >= 25 (the -0.297 slack absorbs
(ii)); (9.89) uses that form.

Book inputs (expform.tex):
  - 1897-1899  (9.84) F_x(s) = (log x) Gamma(s/2+1) + (1/2) Gamma'(s/2+1).
  - 1928-1936  (9.87) |Gamma(s)| <= 2.542 |Im s| e^{-pi|Im s|/2} for
    0 < Re s <= 3/2, |Im s| >= 25/2.
  - 1942-1950  digamma display: Gamma'/Gamma(s) = log|tau| + O*(0.609/|tau|).
  - 1953-1959  (9.88): for -2 <= Re s <= 1, |Im s| >= 25,
    |F_x(s)| <= (log x + 1/2 log|tau/2| + 1/2 O*(0.609/|tau/2|)) |Gamma(s/2+1)|
             <= 2.542 (log x + 1/2 log|tau| - 0.297) (|tau|/2) e^{-pi|tau|/2}.
  - 1966-1970  (9.89) f(T) = 8.45 (log x + 1/2 log T)(|tau|/2 - H) e^{-pi(|tau|-2H)/4}.

Confirms if: at s = 100i, x = 10^8 the printed second line is far below
|F_x(s)| while the corrected (pi/4) line is above it; the printed second
line fails at every point of a grid sigma in [-2,1], 25 <= |tau| <= 400,
x = 10^8; the digamma display error |psi(w) - log|Im w|| is about pi/2 at
w = 0.5+12.5i, far above 0.609/12.5; the first line fails at some grid
point; and the corrected line holds on the whole grid for x in
{10^8, 10^12, 10^27} (its log-factor margin increases with x).

Run: PYTHONPATH=<mpmath dir> python3 -s eq_9_88.py

Ported from a 2026-11-06 check script.
"""
from mpmath import mp, mpf, mpc, gamma, digamma, log, exp, pi, nstr

mp.dps = 30


def vals(x, s):
    t = abs(s.imag)
    w = s / 2 + 1
    G = gamma(w)
    F = log(x) * G + digamma(w) * G / 2
    first = (log(x) + log(t / 2) / 2 + mpf('0.609') / t) * abs(G)
    lf = log(x) + log(t) / 2 - mpf('0.297')
    printed2 = mpf('2.542') * lf * (t / 2) * exp(-pi * t / 2)
    corr2 = mpf('2.542') * lf * (t / 2) * exp(-pi * t / 4)
    return abs(F), first, printed2, corr2


x8 = mpf(10) ** 8
aF, first, p2, c2 = vals(x8, mpc(0, 100))
F100, P100 = aF, p2
print("s = 100i, x = 1e8: |F_x(s)| = %s, printed 2nd line = %s, corrected = %s"
      % (nstr(aF, 4), nstr(p2, 4), nstr(c2, 4)))
ok_i = p2 < aF < c2

w0 = mpc('0.5', '12.5')
err_dig = abs(digamma(w0) - log(mpf('12.5')))
print("psi(0.5+12.5i) =", nstr(digamma(w0), 6), "; |psi - log 12.5| =", nstr(err_dig, 5),
      "vs claimed 0.609/12.5 =", nstr(mpf('0.609') / mpf('12.5'), 4))
ok_dig = err_dig > 1

sigmas = [mpf(-2) + mpf(k) / 4 for k in range(13)]
taus = [25, 30, 35, 40, 45, 50, 100, 200, 300, 400]
npts = f1 = fp = 0
worst1 = mpf(0)
for sg in sigmas:
    for tv in taus:
        for sgn in (1, -1):
            aF, first, p2, c2 = vals(x8, mpc(sg, sgn * tv))
            npts += 1
            if aF > first:
                f1 += 1
                worst1 = max(worst1, aF / first - 1)
            if aF > p2:
                fp += 1
print("grid x=1e8 (%d points): printed 2nd line fails at %d; first line fails at %d (worst excess %s%%)"
      % (npts, fp, f1, nstr(100 * worst1, 3)))

fc = 0
minratio = mpf(10)
for X in (x8, mpf(10) ** 12, mpf(10) ** 27):
    for k in range(61):
        sg = mpf(-2) + mpf(k) / 20
        for tv in (25, 26, 28, 30, 35, 40, 50, 75, 100, 200, 400, 1000, 10 ** 4, 10 ** 6):
            aF, first, p2, c2 = vals(X, mpc(sg, tv))
            if aF > c2:
                fc += 1
            minratio = min(minratio, c2 / aF)
print("corrected line: failures = %d, min corrected/|F| = %s (x in 1e8,1e12,1e27)" % (fc, nstr(minratio, 6)))

if ok_i and ok_dig and fp == npts and f1 > 0 and fc == 0:
    print("CONFIRMED: the printed second line of (9.88) is below |F_x(s)| at every grid point "
          "(at s=100i, x=1e8: %s vs %s) because" % (nstr(P100, 3), nstr(F100, 3)) + " e^{-pi|tau|/2} should be e^{-pi|tau|/4}, "
          "the first line fails slightly since the digamma display drops i*arg w, and the corrected "
          "pi/4 bound holds on the whole grid for x >= 1e8.")
else:
    print("NOT CONFIRMED: the computation does not reproduce the failure of printed (9.88) together "
          "with the validity of the corrected bound.")
