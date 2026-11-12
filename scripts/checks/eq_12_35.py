"""Check of [H, Eq (12.35)] (eq:hipo, upper bound for lambda(q) when q < prod_{p<=p0} p).

Claim: as printed (any prime p0, any q < prod_{p<=p0} p) (12.35) fails in small
cases: its denominator is negative for tiny q (e.g. q = 1, p0 = 3), and the
exchange step needs g(p0) < g(2) for g(p) = (p/(p-1)) f_1(p), false for
p0 = 3, 5 (counterexamples q = 3, p0 = 3 and q = 15, p0 = 5).  It is valid for
p0 >= 7 with positive denominator, which covers the book's use.

Book inputs (l2normls.tex): 365-367 f_1; 369-371 c_E = 1.3325822; 572-578
c+ = 1.36, Q0,min = 10^5, rho <= 0.6; 607-613 omega(rho); 629 c_Delta; 694-701
kappa(q); 712 beta_rho = omega/20000^(1/3); 715-718 (12.33) lambda(q) =
((q/phi(q)) 7.284 (1+beta) f_1(q)/kappa(q))^3; 736-751 the monotonicity remark
and (12.35).
Method: rho = 0.6; g(p) for small p; exact lambda(q) against the right side of
(12.35) for all q < prod_{p<=p0} p, primes p0 <= 13.  Confirms if g(3), g(5) >
g(2) > g(7), the denominator is negative at q = 1, p0 = 3, and the failures
with positive denominator are exactly (3, 3) and (15, 5).

Run: PYTHONPATH=<mpmath dir> python3 -s eq_12_35.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
cE, cp, l0 = mp.mpf('1.3325822'), mp.mpf('1.36'), mp.log(10 ** 5)
rho = mp.mpf('0.6')
om = (l0 + cp) / (l0 / rho + cE)
cD = cp - cE
beta = om / mp.cbrt(20000)
f1 = lambda p: (1 + mp.mpf(p) ** (-mp.mpf(2) / 3)) / (1 + (mp.cbrt(p) + mp.cbrt(p) ** 2) / (p * (p - 1)))
g = lambda p: mp.mpf(p) / (p - 1) * f1(p)
print("g(p) = (p/(p-1)) f_1(p): " + ", ".join(f"g({p}) = {mp.nstr(g(p),6)}" for p in (2, 3, 5, 7, 11)))
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
    G = mp.fprod(g(p) for p in ps)
    return (G * mp.mpf('7.284') * (1 + beta) / kap) ** 3
def rhs(q, p0):
    ps = [p for p in (2, 3, 5, 7, 11, 13) if p < p0]
    D = (1 - om) * (mp.log(q) - sum(mp.log(p) / p for p in ps)) + cD
    return D, (mp.fprod(g(p) for p in ps) * mp.mpf('7.284') * (1 + beta) / D) ** 3
D1 = rhs(1, 3)[0]
print(f"q = 1, p0 = 3: denominator = {mp.nstr(D1,6)}")
fails, negD = [], []
prod = 1
for p0 in (2, 3, 5, 7, 11, 13):
    prod *= p0
    for q in range(1, prod):
        D, r = rhs(q, p0)
        if D <= 0:
            negD.append((q, p0))
        elif lam(q) > r:
            fails.append((q, p0, mp.nstr(lam(q), 6), mp.nstr(r, 6)))
print(f"denominator <= 0 at (q, p0): {negD}")
print(f"failures with positive denominator (q, p0, lambda, bound): {fails}")
if g(3) > g(2) and g(5) > g(2) and g(7) < g(2) and D1 < 0 and [f[:2] for f in fails] == [(3, 3), (15, 5)]:
    print("CONFIRMED: (12.35) fails at (q, p0) = (3, 3) and (15, 5) (g(3), g(5) > g(2)) and has a negative denominator for tiny q (e.g. q = 1, p0 = 3); no other failure for p0 <= 13.")
else:
    print("NOT CONFIRMED: the failure set differs from the claim.")
