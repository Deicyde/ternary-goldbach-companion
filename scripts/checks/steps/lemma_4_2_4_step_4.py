# Lemma 4.2.4 display: u-range min(U, M/V) vs min(U, M/v); take q = 1 (second sum empty).
import math, sys
def Lam(n):
    for p in range(2, n+1):
        if n % p == 0:
            m = n
            while m % p == 0: m //= p
            return math.log(p) if m == 1 else 0.0
    return 0.0
def mu(n):
    r, p, m = 1, 2, n
    while p*p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0: return 0
            r = -r
        p += 1
    return -r if m > 1 else r
M, U, V, q = 60, 60, 9, 1
lhs = sum(Lam(v)*mu(a//v)/a for a in range(1, M+1) if a % 2 and a % q == 0
          for v in range(1, a+1) if a % v == 0 and a/U <= v <= V)
def rhs(lim):
    return sum(Lam(v)/v*sum(mu(u)/u for u in range(1, int(lim(v))+1) if u % 2 and u % q == 0)
               for v in range(1, V+1) if v % 2 and math.gcd(v, q) == 1)
pr = rhs(lambda v: min(U, M/V)); co = rhs(lambda v: min(U, M/v))
print("LHS =", lhs, " printed RHS (M/V) =", pr, " corrected RHS (M/v) =", co)
sys.exit(0 if abs(lhs - co) < 1e-12 and abs(lhs - pr) > 1e-6 else 1)
