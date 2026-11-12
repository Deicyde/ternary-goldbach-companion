"""Check of [H, Eq (12.34)] (eq:modo, kappa(q) >= (1-omega)(log q - sum_{p<p0} log p/p) + c_Delta).

Claim: (12.34) is stated for every prime p0 and every q < prod_{p<=p0} p, but
the exchange step needs log p0/p0 < log 2/2, which fails for p0 = 3; (12.34) is
false at q = 3, p0 = 3.  It holds for p0 >= 5, which covers every use in the
book (p0 >= 31, q >= 2.2*10^10).

Book inputs (l2normls.tex): 369-371 c_E = 1.3325822; 572-578 c+ = 1.36,
Q0,min = 10^5, rho <= 0.6; 607-613 omega(rho); 629 c_Delta = c+ - c_E;
631 1 - omega(rho) > 0; 694-701 kappa(q) = (1-omega)(log q - sum_{p|q} log p/p)
+ c_Delta; 736-746 (12.34) "for q < prod_{p<=p0} p, p0 a prime".
Method: exact evaluation at rho = 0.6 for q = 3, p0 = 3, and an exhaustive
scan of all q < prod_{p<=p0} p for primes p0 <= 13.  Since 1 - omega > 0, the
failure does not depend on rho.  Confirms if (q, p0) = (3, 3) fails and is
the only failure.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_12_34.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
cE, cp, l0 = mp.mpf('1.3325822'), mp.mpf('1.36'), mp.log(10 ** 5)
rho = mp.mpf('0.6')
om = (l0 + cp) / (l0 / rho + cE)
cD = cp - cE
print(f"rho = 0.6: 1 - omega = {mp.nstr(1-om,6)}, c_Delta = {mp.nstr(cD,6)}")
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
kappa = lambda q: (1 - om) * (mp.log(q) - sum(mp.log(p) / p for p in pf(q))) + cD
bound = lambda q, p0: (1 - om) * (mp.log(q) - sum(mp.log(p) / p for p in (2, 3, 5, 7, 11, 13) if p < p0)) + cD
print(f"log3/3 = {mp.nstr(mp.log(3)/3,6)} > log2/2 = {mp.nstr(mp.log(2)/2,6)}")
print(f"q=3, p0=3: kappa(3) = {mp.nstr(kappa(3),6)} < bound {mp.nstr(bound(3,3),6)}")
fails = []
prod = 1
for p0 in (2, 3, 5, 7, 11, 13):
    prod *= p0
    for q in range(1, prod):
        if kappa(q) < bound(q, p0) - mp.mpf(10) ** -20:
            fails.append((q, p0))
print(f"failures over all q < prod_(p<=p0) p, p0 <= 13: {fails}")
if fails == [(3, 3)]:
    print("CONFIRMED: (12.34) fails at q = 3, p0 = 3 (kappa(3) = %s < %s) and nowhere else for p0 <= 13." % (mp.nstr(kappa(3), 5), mp.nstr(bound(3, 3), 5)))
else:
    print("NOT CONFIRMED: the failure set is %s, not [(3, 3)]." % fails)
