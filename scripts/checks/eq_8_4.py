"""Check of [H, Eq (8.4)] (Theorem 8.0.1, lower bounds for x0).

Claim: the first case of (8.4), |x0| >= 0.51729 sqrt(tau) "for rho arbitrary",
is false for rho < 3/2: x0/sqrt(tau) = sqrt((j(rho)-1)/(2 rho)) increases from
0 and reaches 0.51729 only at rho = 3/2 (1.49997 after rounding).  The proof
(8.46) derives it only for rho >= 3/2 and Cor 8.0.2 uses it only there, so it
is harmless; it should read "for rho >= 3/2".  The second case is correct.

Book inputs (mellintran.tex):
  - l.66-70: (8.4) |x0| >= 0.51729 sqrt(tau) (rho arbitrary),
    0.84473 |tau|/|ell| (rho <= 3/2).
  - l.748: x0 = Re u_{0,+}; l.498 (8.21): Re u_{0,+} = (|ell|/2) sqrt((j-1)/2),
    j = sqrt(1+rho^2), rho = 4 tau/ell^2; u_{0,+} is a root of
    u^2 - i ell u - i tau = 0 (l.449-456).
  - l.1222-1231 (8.46): "for rho >= 3/2, (j(rho)-1)/rho is minimal at rho = 3/2".
  - l.1335-1336 (proof of Cor 8.0.2): the only use, "(0.51729 sqrt tau)^{-sigma} for rho >= 3/2".

Confirms if: the closed form of x0 matches the saddle root, x0/sqrt(tau) is
increasing, is below 0.51729 at rho = 0.5 and 1.4, and crosses 0.51729 only at
rho* in (1.49, 1.5]; and x0|ell|/|tau| >= 0.84473 on (0, 3/2].

Run: PYTHONPATH=<dir containing mpmath> python3 -s eq_8_4.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp
from mpmath import mpf, sqrt, fabs

mp.mp.dps = 40

# closed form versus the saddle root
tau, ell = mpf(20), mpf(-12)
roots = [(1j * ell + sg * sqrt(-ell ** 2 + 4j * tau)) / 2 for sg in (1, -1)]
rho = 4 * tau / ell ** 2
j = sqrt(1 + rho ** 2)
cf = fabs(ell) / 2 * sqrt((j - 1) / 2)
re_up = max(mp.re(r) for r in roots)
print("tau=20, ell=-12: max Re root = %s, closed form x0 = %s" % (mp.nstr(re_up, 15), mp.nstr(cf, 15)))
cf_ok = fabs(re_up - cf) < mpf(10) ** -30

ratio = lambda r: sqrt((sqrt(1 + r ** 2) - 1) / (2 * r))       # x0/sqrt(tau)
second = lambda r: sqrt(2 * (sqrt(1 + r ** 2) - 1)) / r        # x0 |ell| / |tau|
for r in ('0.01', '0.5', '1', '1.4', '1.49', '1.5', '2', '1e8'):
    r = mpf(r)
    print("rho=%-6s x0/sqrt(tau)=%s  x0|ell|/|tau|=%s" % (mp.nstr(r, 4), mp.nstr(ratio(r), 8), mp.nstr(second(r), 8)))
grid = [mpf(k) / 1000 for k in range(1, 3001)]
vals = [ratio(r) for r in grid]
incr = all(vals[k] < vals[k + 1] for k in range(len(vals) - 1))
rstar = mp.findroot(lambda r: ratio(r) - mpf('0.51729'), 1.5)
min2 = min(second(r) for r in grid if r <= 1.5)
print("increasing on (0,3]: %s; ratio = 0.51729 at rho* = %s" % (incr, mp.nstr(rstar, 10)))
print("constants: sqrt(sqrt13-2)/sqrt6 = %s, 2 sqrt(sqrt13-2)/3 = %s" % (
    mp.nstr(sqrt(sqrt(13) - 2) / sqrt(6), 10), mp.nstr(2 * sqrt(sqrt(13) - 2) / 3, 10)))
print("min over (0,1.5] of x0|ell|/|tau| = %s" % mp.nstr(min2, 10))

if (cf_ok and incr and ratio(mpf('0.5')) < mpf('0.51729') and ratio(mpf('1.4')) < mpf('0.51729')
        and 1.49 < rstar <= 1.5 and min2 >= mpf('0.84473')):
    print("CONFIRMED: x0/sqrt(tau) = sqrt((j(rho)-1)/(2rho)) is %s at rho=0.5 and reaches 0.51729 only at rho=%s, so the first case of (8.4) holds only for rho>=3/2 (as proved in (8.46)); the second case is correct." % (
        mp.nstr(ratio(mpf('0.5')), 5), mp.nstr(rstar, 6)))
else:
    print("NOT CONFIRMED: closed form ok=%s, increasing=%s, rho*=%s, second-case min=%s." % (
        cf_ok, incr, mp.nstr(rstar, 6), mp.nstr(min2, 6)))
