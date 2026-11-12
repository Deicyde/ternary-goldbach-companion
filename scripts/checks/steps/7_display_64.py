# Check f_0 <= 0.4153461*sqrt(2/sqrt(r0)*5.73827) <= 0.069219 and the sum in display 65.
from math import log, sqrt, e
euler = 0.5772156649015329
mpf = float
r0 = mpf(150000)
F = lambda t: (e**euler)*log(t) + mpf('1.025742')
I1 = F(log(r0)) + 2*(e**euler)/log(r0)
print("I_{1,r0} =", I1)
s = sqrt(2/sqrt(r0)*mpf('5.73827'))
print("sqrt(2/sqrt(r0)*5.73827) =", s)
print("0.68659*s =", mpf('0.68659')*s, "(printed 0.11819, consistent)")
v = mpf('0.4153461')*s
print("0.4153461*s =", v, "(printed <= 0.069219)")
print("0.069219/s =", mpf('0.069219')/s)
print("0.431398*s =", mpf('0.431398')*s)
tot = v + mpf('0.016367') + mpf('0.001332')
print("corrected sum (display 65):", tot, " printed sum check:", mpf('0.069219')+mpf('0.016367')+mpf('0.001332'))
print("casbah corrected: 1.280418*sum =", mpf('1.280418')*tot, "(printed 0.111292)")
raise SystemExit(0 if v > mpf('0.069219') else 1)
