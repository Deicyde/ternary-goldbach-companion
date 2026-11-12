"""Eq 5.39 (Lemma 5.2.1, typeII.tex:887-934).

Claim: the log-gain branch min(1, (2q/phi(q))/log((q(nu+upsilon))^-1)) of (5.39)
is established only when R = (q(nu+upsilon))^(-1/2) <= W', because Montgomery's
inequality fails for r sharing a prime with the support (W', W].

Book inputs: Lemma 5.2.1 hypotheses (typeII.tex:887-894: W, W' >= 1, W' >= W/2,
nu+upsilon <= 1/q); (5.39) (typeII.tex:895-900); the Montgomery step (5.40)
with weight mu(r)^2/phi(r) for all r <= R, (r,q)=1 (typeII.tex:912-921), citing
Montgomery's inequality in the form of [IK, Lemma 7.15] (any excluded classes).

Test: Montgomery's inequality |S(alpha)|^2/phi(r) <= sum_{a' mod r}^* |S(alpha+a'/r)|^2
is checked for every squarefree r <= 100 in the claim's own example
(q=1, nu+upsilon=1e-4, R=100, W'=10, W=20), and (5.40) is checked against the
left side of (5.39) on random admissible data with R > W' and a support other
than {2,3}. The claim (failure whenever R > W' and r shares a prime with the
support) is confirmed only if a failure is found there; the {2,3} corner is
reported separately (see eq_5_40.py).

Run: python3 -I eq_5_39.py
Ported from a 2026-11-06 check script.
"""
from math import gcd, log, pi, cos, sin, sqrt, floor
import random


def isprime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def phi(n):
    return sum(1 for a in range(1, n + 1) if gcd(a, n) == 1)


def mu2(n):
    d = 2
    while d * d <= n:
        if n % (d * d) == 0:
            return 0
        d += 1
    return 1


def S2(alpha, P):
    re = sum(log(p) * cos(2 * pi * alpha * p) for p in P)
    im = sum(log(p) * sin(2 * pi * alpha * p) for p in P)
    return re * re + im * im


# (1) claim's example
Wp, W, R = 10, 20, 100
P = [p for p in range(2, W + 1) if isprime(p) and p > Wp]
omegas = {l: l - len({p % l for p in P}) for l in range(2, R + 1) if isprime(l)}
print("(1) claim's example q=1, R=100, W'=10, W=20, support", P)
print("    min over primes l <= 100 of omega(l) (classes missed) =", min(omegas.values()),
      "; omega(11), omega(13), omega(17), omega(19) =", [omegas[l] for l in (11, 13, 17, 19)])
fails1 = 0
worst1 = 0.0
shared = 0
for r in range(1, R + 1):
    if not mu2(r):
        continue
    if any(r % p == 0 for p in P):
        shared += 1
    for k in range(201):
        al = k / 201
        lhs = S2(al, P) / phi(r)
        rhs = sum(S2(al + a / r, P) for a in range(r) if gcd(a, r) == 1)
        worst1 = max(worst1, lhs / rhs)
        fails1 += lhs > rhs * (1 + 1e-9)
print("    squarefree r <= 100 sharing a prime with the support:", shared,
      "; Montgomery failures over 201 alphas each:", fails1, "; max ratio %.4f" % worst1)

# (2) random admissible data with R > W', support != {2,3}
rnd = random.Random(12345)
fails2 = trials2 = hit2 = 0
worst2 = 0.0
corner_fail = corner_trials = 0
corner_worst539 = 0.0
for _ in range(4000):
    Wp = rnd.choice([1.0, 1.5, 1.7, 1.9, 2.0, 2.5, 3.0, 3.5, 4.0, 5.5, 6.5, 7.0, 10.0])
    W = rnd.uniform(Wp, 2 * Wp)
    if rnd.random() < 0.3:
        W = 2 * Wp
    q = rnd.choice([1, 1, 1, 2, 3, 5])
    s = rnd.uniform(1 / (q * 150), 1 / q)
    nu = rnd.uniform(0.05, 0.95) * s
    ups = s - nu
    P = [p for p in range(2, int(floor(W)) + 1) if isprime(p) and p > Wp]
    R = 1 / sqrt(q * s)
    if not P or R <= Wp:
        continue
    c = rnd.uniform(-1, 1)
    al = []
    for a in range(q):
        pts = []
        for _ in range(rnd.randint(0, int(ups / nu) + 1)):
            t = rnd.uniform(c, c + ups)
            if all(abs(t - u) > nu for u in pts):
                pts.append(t)
        al += [a / q + t for t in pts]
    if not al:
        continue
    rs = [r for r in range(1, int(floor(R + 1e-12)) + 1) if gcd(r, q) == 1 and mu2(r)]
    norm = sum(1 / phi(r) for r in rs)
    lhs = sum(S2(a, P) for a in al)
    toy = sum(S2(a + ap / r, P) for r in rs for ap in range(r) if gcd(ap, r) == 1 for a in al) / norm
    lsq = sum(log(p) ** 2 for p in P)
    g = min(1.0, 2 * q / phi(q) / log(1 / (q * s)))
    rhs539 = g * (W - Wp + 1 / nu) * lsq
    if P == [2, 3]:
        corner_trials += 1
        corner_fail += lhs > toy * (1 + 1e-9)
        corner_worst539 = max(corner_worst539, lhs / rhs539)
        continue
    trials2 += 1
    hit2 += any(r % p == 0 for r in rs for p in P)
    fails2 += lhs > toy * (1 + 1e-9)
    worst2 = max(worst2, lhs / toy)
print("(2) random admissible data, R > W', support != {2,3}: trials", trials2,
      "(with some r <= R divisible by a support prime:", hit2, "); (5.40) failures:", fails2,
      "; max LHS/(5.40) %.6f" % worst2)
print("    support {2,3}, R > W': trials", corner_trials, "; (5.40) failures:", corner_fail,
      "; max LHS/RHS(5.39) %.4f" % corner_worst539)

if fails1 or fails2:
    print("CONFIRMED: Montgomery's step (5.40) fails for R > W' with a support other than {2,3}, "
          "so the log-gain branch of (5.39) is unproved for R > W'.")
else:
    print("NOT CONFIRMED: For R > W' Montgomery's step (5.40) held for all %d squarefree r <= 100 sharing a support prime in the claim's own example "
          "and all %d random admissible cases with support other than {2,3}; the only failure is the support {2,3} "
          "(Eq 5.40), where (5.39) itself still holds." % (shared, trials2))
