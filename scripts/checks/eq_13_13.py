"""Check of [H, Eq (13.13)] (eq:gypo, the g(r_1) coefficient in M of Theorem 13.2.1).

Claim: the jump constant -2.14938 = -2(log(3/8) + c+ - (8/15)c-) was computed
with the 2013 values c+ = 2.3912, c- = 0.6294; with the book's c+ = 2.0532,
c- = 0.6394 it is -1.46271, so M is understated.  Ch. 14's "<= 7/15"
(kappa = 49, before (14.43)) then fails, but the final bound survives:
Z <= 1.0175 x^2/kappa < 1.058259 x^2/kappa.

Book inputs:
  - intminarc.tex:186-188  r_1 = (3/8)(x/kappa)^(4/15), x >= 10^25 kappa;
  - intminarc.tex:221-233  (13.13) with -2.14938, c+ = 2.0532, c- = 0.6394;
  - intminarc.tex:402-422  H(r) = (log(r+1)+c+)/(log sqrt x + c-) for r < r_1,
                           1 for r >= r_1, and the jump bound ending in -2.14938;
  - conclusion.tex:755-765 kappa = 49, "<= 7/15", (14.43) 7/15 g(r_1) S <= 0.30517x;
  - conclusion.tex:919-942 (14.48) M <= 0.38492x + 0.30517x + 0.114988x,
                           (14.49) T term 3.5776e-4, E term 1.0532e-11,
                           |phi|_1 = sqrt(pi/2), Z <= 1.00948 x^2/kappa, x >= 4.9e26;
  - conclusion.tex:478     major-arc lower bound 1.058259 x^2/kappa.
Method: recompute the constant with both sets of c+-; the exact jump
1 - H(r_1^-) at kappa = 49, x = 4.9e26 (its maximum over x >= 4.9e26, since
the jump decreases in x) against the printed bound; the exact-minus-printed
difference (0.686665 - 2 log(1+1/r_1))/(log x + 2c-) > 0; rescale (14.43) by
jump/(7/15) and redo (14.48)-(14.49).
Confirms if the constant with the book's c+- is -1.46271 (2013 values give
-2.14938), the exact jump exceeds both the printed bound and 7/15, and the
repaired Z is below 1.058259 x^2/kappa.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_13_13.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
const = lambda cp, cm: -2 * (mp.log(mp.mpf(3) / 8) + cp - mp.mpf(8) / 15 * cm)
cp, cm = mp.mpf('2.0532'), mp.mpf('0.6394')
c_book, c_2013 = const(cp, cm), const(mp.mpf('2.3912'), mp.mpf('0.6294'))
print(f"-2(log 3/8 + c+ - (8/15)c-): book c+- -> {mp.nstr(c_book,7)}; 2013 c+- -> {mp.nstr(c_2013,7)} (printed -2.14938)")
kap = mp.mpf(49)
def jump(x):
    r1 = mp.mpf(3) / 8 * (x / kap) ** (mp.mpf(4) / 15)
    return 1 - (mp.log(r1 + 1) + cp) / (mp.log(mp.sqrt(x)) + cm), r1
printed = lambda x: mp.mpf(7) / 15 + (mp.mpf('-2.14938') + mp.mpf(8) / 15 * mp.log(kap)) / (mp.log(x) + 2 * cm)
x0 = mp.mpf('4.9e26')
j0, r1 = jump(x0)
print(f"kappa = 49, x = 4.9e26: exact jump {mp.nstr(j0,6)}, printed bound {mp.nstr(printed(x0),6)}, 7/15 = {mp.nstr(mp.mpf(7)/15,6)}")
diff_formula = (c_book + mp.mpf('2.14938') - 2 * mp.log(1 + 1 / r1)) / (mp.log(x0) + 2 * cm)
dec = all(jump(x0 * 10 ** k)[0] > jump(x0 * 10 ** (k + 1))[0] > mp.mpf(7) / 15 for k in range(0, 40))
print(f"exact - printed at x0 = {mp.nstr(j0 - printed(x0),6)} (formula {mp.nstr(diff_formula,6)}); jump decreasing and > 7/15 on x0..x0*10^40: {dec}")
t43 = mp.mpf('0.30517') * j0 / (mp.mpf(7) / 15)
M = mp.mpf('0.38492') + t43 + mp.mpf('0.114988')
phi1 = mp.sqrt(mp.pi / 2)
Z = (mp.sqrt(phi1 * (M + mp.mpf('3.5776e-4'))) + mp.sqrt(mp.mpf('1.0532e-11'))) ** 2
Zbook = (mp.sqrt(phi1 * (mp.mpf('0.80508') + mp.mpf('3.5776e-4'))) + mp.sqrt(mp.mpf('1.0532e-11'))) ** 2
print(f"rescaled (14.43): {mp.nstr(t43,6)} x; M <= {mp.nstr(M,6)} x; Z <= {mp.nstr(Z,6)} x^2/kappa (book chain gives {mp.nstr(Zbook,6)}); major arcs 1.058259")
if abs(c_book - mp.mpf('-1.46271')) < 1e-5 and abs(c_2013 - mp.mpf('-2.14938')) < 1e-5 and j0 > printed(x0) \
        and j0 > mp.mpf(7) / 15 and dec and Z < mp.mpf('1.058259'):
    print(f"CONFIRMED: with the book's c+ = 2.0532, c- = 0.6394 the jump constant is {mp.nstr(c_book,6)}, not -2.14938 (the 2013 value), so at kappa = 49 the jump {mp.nstr(j0,6)} exceeds 7/15; the repaired Z <= {mp.nstr(Z,5)} x^2/kappa stays below 1.058259 x^2/kappa.")
else:
    print("NOT CONFIRMED: the recomputed constants do not match the claim.")
