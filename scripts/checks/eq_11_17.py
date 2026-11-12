"""Check of [H, Eq (11.17)] (eq:humo, proof of Lemma 11.2.1).

Claim: (11.17) collects the coefficients of x_r^{-1/6}, so the L_{2r}/r term
(13/2)e^gamma x_r^{-1/3} log x_r loglog x_r should enter with x_r^{-1/6}, not
x_r^{-1/3}.  With the correct term the ratio is 1.10 at x_r = e^33, so the
analytic step fails there; it holds only for log x_r >= 38.44.  Lemma 11.2.1
survives (direct evaluation: max g/h = 0.592).

Book inputs:
  - optcoor.tex:237-254  g_x(r), R_{x,t}, L_t, h(x) = 0.276 x^{-1/6}(log x)^{3/2}
                         + 1234 x^{-1/3} log x; digamma(r) = e^gamma loglog r +
                         2.50637/loglog r (optcoor.tex:283, 586).
  - optcoor.tex:256-262  Lemma 11.2.1: compare at x_r = (6r)^3, r >= 11.
  - optcoor.tex:296-312  first term <= (0.21 L (log L)^{3/2} + 3.47) x_r^{-1/6};
                         L_{2r} <= e^gamma loglog x_r((13/12) log x_r + 4.25) + ...
  - optcoor.tex:317-327  (11.17) and the ratio "< 1 ... true for x = e^33".
  - optcoor.tex:330-335  bisection on log x_r in [log 66^3, 33] only.

Computes the printed and corrected ratios at log x_r = 33, the crossing point
of the corrected ratio, and max g_{x_r}(x_r^{1/3}/6)/h(x_r) for log x_r in
[log 66^3, 700].  Confirms if the corrected ratio exceeds 1 at 33, crosses 1
near 38.44, and the direct max g/h is < 1 (lemma survives).

Run: PYTHONPATH=<mpmath dir> python3 -s eq_11_17.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
eg = mp.exp(mp.euler)


def ratio(L, corrected):
    ex = -mp.mpf(1) / 6 if corrected else -mp.mpf(1) / 3
    term = mp.mpf(13) / 2 * eg * mp.exp(ex * L) * L * mp.log(L)
    return (mp.mpf("0.21") * L * mp.log(L) ** 1.5 + mp.mpf("6.83") + term) / (mp.mpf("0.276") * L ** 1.5), term


rp, tp = ratio(mp.mpf(33), False)
rc, tc = ratio(mp.mpf(33), True)
print("log x_r = 33: printed term %s, ratio %s ; corrected term %s, ratio %s" % (mp.nstr(tp, 5), mp.nstr(rp, 6), mp.nstr(tc, 5), mp.nstr(rc, 6)))
cross = mp.findroot(lambda L: ratio(L, True)[0] - 1, 38)
print("corrected ratio = 1 at log x_r = %s" % mp.nstr(cross, 7))
grid = [mp.mpf(33) + k * mp.mpf("0.05") for k in range(int((cross - 33) / mp.mpf("0.05")))]
above = all(ratio(L, True)[0] > 1 for L in grid)
print("corrected ratio > 1 on all of [33, %s): %s" % (mp.nstr(cross, 6), above))

# direct evaluation of g/h at x_r = (6r)^3
dig = lambda r: eg * mp.log(mp.log(r)) + mp.mpf("2.50637") / mp.log(mp.log(r))
R = lambda x, t: mp.mpf("0.27125") * mp.log(1 + mp.log(4 * t) / (2 * mp.log(9 * mp.cbrt(x) / (mp.mpf("2.004") * t)))) + mp.mpf("0.41415")
Lt = lambda t: dig(t / 2) * (mp.mpf(13) / 4 * mp.log(t) + mp.mpf("7.82")) + mp.mpf("13.66") * mp.log(t) + mp.mpf("37.55")


def g(x, r):
    return ((R(x, 2 * r) * mp.log(2 * r) + mp.mpf("0.5")) * mp.sqrt(dig(r)) + mp.mpf("2.5")) / mp.sqrt(2 * r) + Lt(2 * r) / r + mp.mpf("3.36") * x ** (-mp.mpf(1) / 6)


h = lambda x: mp.mpf("0.276") * x ** (-mp.mpf(1) / 6) * mp.log(x) ** 1.5 + 1234 * x ** (-mp.mpf(1) / 3) * mp.log(x)
L0 = 3 * mp.log(66)
best, at = 0, None
n = 2000
for k in range(n + 1):
    L = L0 + (700 - L0) * k / n
    x = mp.exp(L)
    v = g(x, mp.cbrt(x) / 6) / h(x)
    if v > best:
        best, at = v, L
gap = max(g(mp.exp(L), mp.cbrt(mp.exp(L)) / 6) / h(mp.exp(L)) for L in mp.linspace(33, 38.5, 56))
print("max g/h on log x_r in [%s, 700]: %s at log x_r = %s ; on [33, 38.5]: %s" % (mp.nstr(L0, 5), mp.nstr(best, 5), mp.nstr(at, 5), mp.nstr(gap, 4)))

if rp < 1 < rc and abs(cross - mp.mpf("38.44")) < 0.01 and above and best < 1:
    print("CONFIRMED: with the x_r^{-1/6} the L_{2r}/r term requires, the ratio in (11.17) is %s > 1 at x_r = e^33 (printed %s) and falls below 1 only at log x_r = %s, so the proof leaves (33, %s) uncovered; directly g/h <= %s, so Lemma 11.2.1 survives." % (mp.nstr(rc, 4), mp.nstr(rp, 4), mp.nstr(cross, 5), mp.nstr(cross, 5), mp.nstr(best, 3)))
else:
    print("NOT CONFIRMED: the corrected ratio or the direct g/h check did not reproduce the claim.")
