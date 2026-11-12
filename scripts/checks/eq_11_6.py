"""Check of [H, Eq (11.6)] (eq:jaram).

Claim: (11.6) inserts (11.5) at every rho in [0, N/x], but (11.5) comes from
Lemma 11.1.1, whose hypothesis ||eta_o(.+2-rho) - eta_o||_2 <= |eta_o|_2/2
holds only for |2-rho| <= 0.2493; for rho < 1.7507 the step is unjustified.
The statement is true: |eta_o|^2 - (1/2)(2-rho)^2 |eta_o'|^2 <= (eta_o*eta_o)(rho)
<= |eta_o|^2 for all rho.

Book inputs:
  - optcoor.tex:70-74    eta_o(t) = t^3(2-t)^3 e^{-(t-1)^2/2} on [0,2].
  - optcoor.tex:79-86    (11.4) conv(rho) = int eta_o(t) eta_o(2-rho+t) dt, "rho <= 2 close to 2".
  - optcoor.tex:88-93    Lemma 11.1.1 hypothesis |w-v| <= |v|/2.
  - optcoor.tex:114-131  (11.5): conv = |eta_o|^2 + O*(2.71 (2-rho)^2 |eta_o'|^2).
  - optcoor.tex:133-147  (11.6): (11.5) integrated over rho in [0, N/x].

Computes |eta_o|^2, |eta_o'|^2, d(s)^2 = ||eta_o(.+s) - eta_o||^2 =
2(|eta_o|^2 - conv(2-s)), the s* with d(s*) = |eta_o|/2, checks d is increasing
on [0,2], and checks 0 <= |eta_o|^2 - conv(2-s) <= s^2 |eta_o'|^2/2 on a grid.
Confirms if s* is about 0.2493 (so the hypothesis fails for rho < 1.7507,
d(2)/|eta_o| = sqrt 2) and the polarization bound holds throughout.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_11_6.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 20
eo = lambda t: t ** 3 * (2 - t) ** 3 * mp.exp(-(t - 1) ** 2 / 2) if 0 <= t <= 2 else mp.mpf(0)
n2 = mp.quad(lambda t: eo(t) ** 2, [0, 1, 2])
d2 = mp.quad(lambda t: (t ** 2 * (2 - t) ** 2 * mp.exp(-(t - 1) ** 2 / 2) * (3 * (2 - t) - 3 * t - t * (2 - t) * (t - 1))) ** 2, [0, 1, 2])
print("|eta_o|_2^2 = %s ; |eta_o'|_2^2 = %s" % (mp.nstr(n2, 12), mp.nstr(d2, 12)))


def conv2ms(s):  # conv(2-s) = int eta_o(t) eta_o(t+s) dt, support t in [0, 2-s]
    if s >= 2:
        return mp.mpf(0)
    return mp.quad(lambda t: eo(t) * eo(t + s), [0, (2 - s) / 2, 2 - s])


dd = lambda s: 2 * (n2 - conv2ms(s))
sstar = mp.findroot(lambda s: dd(s) - n2 / 4, 0.25)
print("hypothesis d(s) <= |eta_o|/2 holds iff s <= s* = %s, i.e. rho >= %s" % (mp.nstr(sstar, 10), mp.nstr(2 - sstar, 10)))
print("ratio d/|eta_o| at rho = 1.5, 1, 0: %s, %s, %s" % tuple(mp.nstr(mp.sqrt(dd(s) / n2), 7) for s in (0.5, 1, 2)))

grid = [mp.mpf(k) / 100 for k in range(1, 201)]
vals = [dd(s) for s in grid]
mono = all(b >= a for a, b in zip(vals, vals[1:]))
pol = all(0 <= v / 2 <= s ** 2 * d2 / 2 * (1 + mp.mpf(10) ** -12) for s, v in zip(grid, vals))
worst = max((v / 2) / (s ** 2 * d2) for s, v in zip(grid, vals))
print("d(s) nondecreasing on (0,2]: %s ; 0 <= |eta_o|^2 - conv <= s^2|eta_o'|^2/2 on grid: %s (max ratio %s, book allows 2.71)"
      % (mono, pol, mp.nstr(worst, 6)))
print("rho = 1: |eta_o|^2 - conv = %s <= (1/2)|eta_o'|^2 = %s" % (mp.nstr(n2 - conv2ms(1), 7), mp.nstr(d2 / 2, 7)))

if abs(sstar - mp.mpf("0.2493")) < 1e-3 and mono and pol:
    print("CONFIRMED: Lemma 11.1.1's hypothesis holds for (11.4) only when |2-rho| <= %s, so (11.6)'s use of (11.5) for rho in [0, %s) is unjustified, while polarization gives the needed bound with constant 1/2 for every rho." % (mp.nstr(sstar, 5), mp.nstr(2 - sstar, 5)))
else:
    print("NOT CONFIRMED: the threshold or the polarization bound did not reproduce.")
