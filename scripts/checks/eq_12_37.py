"""Check of [H, Eq (12.37)] (eq:hipowo) and its follow-up for q >= prod_{p<=37, p!=7} p.

Claim: in the follow-up, log q >= 0.8009 p1 - log 7 turns the denominator
log q - log p1 + 0.35152 into 0.8009t - log t - 1.59439, not the printed
0.8009t - log t + 0.07354; the reduced inequality then needs the constant
~7.63, not 6.74849 (which also does not follow from the printed denominator:
that route needs 7.43-7.48).  The conclusion survives (the corrected
inequality holds for t >= 37).  Also, (12.37), read with
q < prod_{p<=p0, p!=7} p, fails at (q, p0) = (3, 3) and (15, 5) and has a
non-positive denominator for tiny q.

Book inputs (l2normls.tex): 365-367 f_1; 369-371 c_E; 572-578 c+ = 1.36,
Q0,min = 10^5, rho <= 0.6; 607-613 omega; 629 c_Delta; 694-718 kappa, beta,
lambda (12.33); 752-762 (12.36)-(12.37); 888-900 the 84.351 bound with
denominator log q - log p1 + 0.35152; 904-911 the follow-up ("since
log q >= 0.8009 p1 - log 7", denominator 0.8009t - log t + 0.07354, "6.74849",
t >= 37); 874-881 the analogous step with 0.6924 t.
Method: recompute the denominator constant, the three candidate constants,
and the corrected inequality on t >= 37 (LHS increasing, RHS decreasing, so
t = 37 suffices; also scanned to t = 10^4); exhaustive scan of (12.37) for
primes p0 <= 13, q < prod_{p<=p0, p!=7} p, 210 not dividing q, rho = 0.6.
Confirms if the correct denominator constant is 0.35152 - log 7, the needed
constant exceeds 6.74849, the corrected inequality holds for t >= 37, and the
scan's failures are (3, 3), (15, 5) plus non-positive denominators only.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_12_37.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
L7 = mp.log(7)
k_const = mp.mpf('0.35152') - L7
print(f"denominator constant: 0.35152 - log 7 = {mp.nstr(k_const,6)} (printed +0.07354)")
base = mp.log(mp.mpf('84.351')) + L7
printed = base - mp.log(mp.mpf('0.6924'))
route1 = base - 3 * mp.log(mp.mpf('0.6924'))
ratio_pr = (mp.mpf('0.8009') * 37 - mp.log(37) + mp.mpf('0.07354')) / 37
route2 = base - 3 * mp.log(ratio_pr)
ratio_c = (mp.mpf('0.8009') * 37 - mp.log(37) + k_const) / 37
corr = base - 3 * mp.log(ratio_c)
print(f"log 84.351 + log 7 - log 0.6924 = {mp.nstr(printed,7)} (printed 6.74849: cube dropped)")
print(f"printed denominator: with 0.6924 t -> {mp.nstr(route1,6)}; with its t>=37 ratio {mp.nstr(ratio_pr,6)} -> {mp.nstr(route2,6)}")
print(f"corrected denominator: ratio at t = 37 is {mp.nstr(ratio_c,6)} (increasing in t) -> constant {mp.nstr(corr,6)}")
lhs = lambda t: mp.mpf('0.224') * t - mp.mpf('2.24742') * mp.cbrt(t)
rhs = lambda t: 3 * mp.log(mp.log(t)) - 3 * mp.log(t) + corr
m37 = lhs(37) - rhs(37)
scan_ok = all(lhs(t) > rhs(t) for t in range(37, 10001))
mono = all(lhs(t + 1) > lhs(t) and rhs(t + 1) < rhs(t) for t in range(37, 2000))
print(f"corrected inequality at t = 37: {mp.nstr(lhs(37),6)} > {mp.nstr(rhs(37),6)} (margin {mp.nstr(m37,4)}); holds on 37..10^4: {scan_ok}; monotone: {mono}")
# exhaustive scan of (12.37)
cE, cp, l0 = mp.mpf('1.3325822'), mp.mpf('1.36'), mp.log(10 ** 5)
rho = mp.mpf('0.6')
om = (l0 + cp) / (l0 / rho + cE); cD = cp - cE; beta = om / mp.cbrt(20000)
f1 = lambda p: (1 + mp.mpf(p) ** (-mp.mpf(2) / 3)) / (1 + (mp.cbrt(p) + mp.cbrt(p) ** 2) / (p * (p - 1)))
g = lambda p: mp.mpf(p) / (p - 1) * f1(p)
def pf(n):
    ps, d = [], 2
    while d * d <= n:
        if n % d == 0:
            ps.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        ps.append(n)
    return ps
def lam(q):
    ps = pf(q)
    kap = (1 - om) * (mp.log(q) - sum(mp.log(p) / p for p in ps)) + cD
    return (mp.fprod(g(p) for p in ps) * mp.mpf('7.284') * (1 + beta) / kap) ** 3
fails, negD = [], []
for p0 in (2, 3, 5, 7, 11, 13):
    ps = [p for p in (2, 3, 5, 11, 13) if p < p0]
    lim = mp.fprod([p for p in (2, 3, 5, 11, 13) if p <= p0])
    D0 = -sum(mp.log(p) / p for p in ps)
    G0 = mp.fprod(g(p) for p in ps)
    for q in range(1, int(lim)):
        if q % 210 == 0:
            continue
        D = (1 - om) * (mp.log(q) + D0) + cD
        if D <= 0:
            negD.append((q, p0)); continue
        r = (G0 * mp.mpf('7.284') * (1 + beta) / D) ** 3
        if lam(q) > r:
            fails.append((q, p0, mp.nstr(lam(q), 6), mp.nstr(r, 6)))
print(f"(12.37) scan: non-positive denominator at {negD}")
print(f"(12.37) scan: failures with positive denominator {fails}")
if abs(k_const + mp.mpf('1.59439')) < 1e-5 and corr > mp.mpf('6.74849') and route2 > mp.mpf('6.74849') \
        and m37 > 0 and scan_ok and mono and [f[:2] for f in fails] == [(3, 3), (15, 5)] and max(q for q, _ in negD) <= 3:
    print(f"CONFIRMED: the follow-up's denominator should be 0.8009t - log t - 1.59439 (not +0.07354) and the constant {mp.nstr(corr,6)} (not 6.74849); the corrected inequality still holds for t >= 37 (margin {mp.nstr(m37,4)}), and (12.37) itself fails at (3,3), (15,5) and for q <= 3 with non-positive denominator.")
else:
    print("NOT CONFIRMED: some recomputed value does not match the claim.")
