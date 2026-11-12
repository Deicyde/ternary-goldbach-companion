"""Check of [H, Lemma 5.2.1] (Montgomery step in the log-gain branch of (5.39)).

Item: Lemma 5.2.1 (lem:ogor, typeII.tex:887-901; proof typeII.tex:902-937).

Claim: the log-gain branch applies Montgomery's inequality to every squarefree
r <= R = (q(nu+upsilon))^{-1/2}, (r,q)=1; this needs all primes in (W',W]
coprime to r, i.e. R <= W', but the hypotheses allow R > W' (e.g. q=1,
nu+upsilon=10^-4, R=100, W'=10, W=20), where that branch is unproved.

Book inputs: hypotheses of Lemma 5.2.1 (q >= 1, nu+upsilon <= 1/q, W, W' >= 1,
W' >= W/2; typeII.tex:887-894); the bound (5.39) eq:crut (typeII.tex:895-900);
the Montgomery step to (5.40) eq:toyor (typeII.tex:912-921) with
R = 1/sqrt((nu+upsilon) q) (typeII.tex:927-928).

Montgomery's inequality in the form the book cites ([IK04, Lemma 7.15]):
if the support avoids omega(p) >= 1 residue classes mod each prime p | r, then
|S(alpha)|^2 prod_{p|r} omega(p)/(p-omega(p)) <= sum*_{a mod r} |S(alpha+a/r)|^2,
and the product is >= 1/phi(r).  Coprimality of r with the support is
sufficient, not necessary.

Computation:
 (A) in the claim's own example (support = primes in (10,20], R = 100) check
     that every prime p <= R misses a residue class of the support, and check
     |S(alpha)|^2/phi(r) <= sum*_{a mod r}|S(alpha+a/r)|^2 numerically for every
     squarefree r <= 100 and 400 values of alpha;
 (B) over all integer parts (floor W', floor W) with floor W' <= 3000 allowed by
     W' >= W/2, list the cases where some prime's residue classes are all
     covered by the support (the only cases where the step can fail);
 (C) in the degenerate case found, q = 1, k = 1, alpha_1 = 0,
     nu = upsilon = 1/18 (R = 3), W' = 1.5, W = 3: evaluate the left side of
     (5.39), the expression (5.40), and the right side of (5.39).

The claim is confirmed only if the step fails in the claim's own example (R > W'
with support primes dividing some r <= R).  Output NOT CONFIRMED if the step
holds there.

Run: python3 -I lemma_5_2_1.py

Ported from a 2026-11-06 check script.
"""
import cmath
import math
import random


def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def factor(n):
    ps, d = [], 2
    while d * d <= n:
        if n % d == 0:
            ps.append(d)
            n //= d
            if n % d == 0:
                return None  # not squarefree
        d += 1
    if n > 1:
        ps.append(n)
    return ps


def phi_sqf(ps):
    return math.prod(p - 1 for p in ps)


def S(alpha, supp):
    return sum(math.log(p) * cmath.exp(2j * math.pi * alpha * p) for p in supp)


# ---- (A) the claim's example ----
supp = [p for p in primes_upto(20) if p > 10]
R = 100
covered = [p for p in primes_upto(R) if len({x % p for x in supp}) == p]
print(f"(A) support = {supp}, R = {R}; primes p <= R whose classes are all hit by the support: {covered}")
shared = [r for r in range(2, R + 1) if factor(r) and any(r % p == 0 for p in supp)]
print(f"    squarefree r <= R sharing a prime with the support: {len(shared)} (e.g. {shared[:6]})")
random.seed(1)
alphas = [i / 400 for i in range(400)]
worst = 0.0
for r in range(1, R + 1):
    ps = factor(r)
    if ps is None:
        continue
    ph = phi_sqf(ps)
    for al in alphas:
        lhs = abs(S(al, supp)) ** 2 / ph
        rhs = sum(abs(S(al + a / r, supp)) ** 2 for a in range(1, r + 1) if math.gcd(a, r) == 1)
        if lhs > 0:
            worst = max(worst, lhs / rhs if rhs > 0 else float("inf"))
print(f"    max over r <= 100 squarefree, 400 alphas of |S(a)|^2/phi(r) / sum*|S(a+b/r)|^2 = {worst:.6f}")
example_step_holds = (not covered) and worst <= 1 + 1e-9

# ---- (B) where can the hypothesis of Montgomery's inequality fail? ----
P = primes_upto(2 * 3000 + 2)
Pset = set(P)
bad = []
for a in range(1, 3001):            # a = floor W'
    sp = []
    for b in range(a, 2 * a + 2):   # b = floor W, W <= 2W' < 2a+2
        if b > a and b in Pset:
            sp.append(b)            # sp = primes in (W', W]
        for p in sp:                # primes not in the support miss class 0
            if len(sp) < p:
                break               # sp is increasing, so no larger p can be covered
            if len({x % p for x in sp}) == p:
                bad.append((a, b, p, sp))
print(f"(B) (floor W', floor W) with floor W' <= 3000 where some prime has all classes hit: "
      f"{[(a, b, p, sp) for a, b, p, sp in bad]}")
print("    (W' >= W/2 with W >= 3 and floor W' = 1 means W' in [1.5, 2), W in [3, 4): support {2, 3}, p = 2)")

# ---- (C) the degenerate case ----
nu = ups = 1 / 18
q = 1
Rc = 1 / math.sqrt((nu + ups) * q)
Wp, W = 1.5, 3
sp = [2, 3]
lhs539 = abs(S(0, sp)) ** 2
rs = [r for r in range(1, int(Rc + 1e-12) + 1) if factor(r) is not None and math.gcd(r, q) == 1]
norm = sum(1 / phi_sqf(factor(r)) for r in rs)
tot = sum(abs(S(a / r, sp)) ** 2 for r in rs for a in range(1, r + 1) if math.gcd(a, r) == 1)
e540 = tot / norm
minfac = min(1, 2 * q / 1 / math.log(1 / (q * (nu + ups))))
rhs539 = minfac * (W - Wp + 1 / nu) * sum(math.log(p) ** 2 for p in sp)
r2 = abs(S(0, sp)) ** 2 / 1 - abs(S(0.5, sp)) ** 2
print(f"(C) q=1, k=1, alpha=0, nu=upsilon=1/18 (R={Rc:.4f}), W'=1.5, W=3, support {sp}:")
print(f"    LHS(5.39) = {lhs539:.4f};  (5.40) = {e540:.4f};  RHS(5.39) = {rhs539:.4f} (min factor {minfac:.4f})")
print(f"    r=2: |S(0)|^2/phi(2) - |S(1/2)|^2 = {r2:.4f} > 0, so Montgomery's inequality fails for r = 2")
degenerate_gap = lhs539 > e540 and lhs539 <= rhs539
only_degenerate = all(a == 1 and b == 3 and p == 2 for a, b, p, _ in bad) and len(bad) == 1

if example_step_holds:
    print("NOT CONFIRMED: Montgomery's inequality needs only a free residue class mod each p | r, not R <= W'; "
          "in the claim's own example (W'=10, W=20, R=100) the step holds, and "
          + ("the step fails only when the primes in (W',W] are {2,3} (W' in [1.5,2), W in [3,4)), q odd, R >= 2, "
             "where (5.39) itself still holds." if degenerate_gap and only_degenerate
             else "no degenerate failure was reproduced."))
else:
    print("CONFIRMED: in the claim's example the Montgomery step fails for some r <= R with R > W'.")
