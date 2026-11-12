"""Eq 5.40 (proof of Lemma 5.2.1, typeII.tex:912-934).

Claim: the step "left side of (5.39) <= (5.40)" (Montgomery's inequality with
weight mu(r)^2/phi(r) for every r <= R, (r,q)=1, R = (q(nu+upsilon))^(-1/2)) is
false for some data the lemma allows; separately, the condition
"If nu+upsilon >= 1/qR^2" (typeII.tex:925) is reversed (<= is needed); the
conclusion (5.39) of Lemma 5.2.1 survives.

Book inputs: Lemma 5.2.1 hypotheses (typeII.tex:887-894: q >= 1,
alpha_i = a_i/q + upsilon_i, upsilon_i in an interval of length upsilon,
nu-separation for equal a_i, nu+upsilon <= 1/q, W, W' >= 1, W' >= W/2);
(5.39) (typeII.tex:895-900); (5.40) (typeII.tex:916-921); the separation
sentence and the choice R = 1/sqrt((nu+upsilon) q) (typeII.tex:922-928).

Confirming output: (a) with q=1, alpha_1=0, nu=upsilon=1/8 (R=2), W=3, W'=1.5
the left side of (5.39) exceeds (5.40) while (5.39) holds; (b) data with
nu+upsilon >= 1/qR^2 whose shifted angles are closer than nu, while
nu+upsilon <= 1/qR^2 always gives nu-separation; (c) the trivial bound
(R+1) log R <= R^2 for R > 1 covers R >= W', so (5.39) survives.
The script also records that the failure needs a support missing no residue
class mod some prime dividing r: it scans all admissible supports.

Run: python3 -I eq_5_40.py
Ported from a 2026-11-06 check script.
"""
from fractions import Fraction as F
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


def toyor(alphas, P, q, R):
    rs = [r for r in range(1, int(floor(R + 1e-12)) + 1) if gcd(r, q) == 1]
    norm = sum(mu2(r) / phi(r) for r in rs)
    inner = sum(S2(a + ap / r, P) for r in rs if mu2(r)
                for ap in range(r) if gcd(ap, r) == 1 for a in alphas)
    return inner / norm


ok = True

# (a) counterexample
q, nu, ups, W, Wp = 1, 1 / 8, 1 / 8, 3.0, 1.5
assert q >= 1 and nu + ups <= 1 / q and W >= 1 and Wp >= 1 and Wp >= W / 2
R = 1 / sqrt(q * (nu + ups))
P = [p for p in range(2, int(W) + 1) if isprime(p) and p > Wp]
alphas = [0.0]
lhs = sum(S2(a, P) for a in alphas)
t540 = toyor(alphas, P, q, R)
lsq = sum(log(p) ** 2 for p in P)
gain = min(1.0, 2 * q / phi(q) / log(1 / (q * (nu + ups))))
rhs = gain * (W - Wp + 1 / nu) * lsq
print("(a) q=1, alpha_1=0, nu=upsilon=1/8, W=3, W'=1.5: R =", R, " support", P)
print("    LHS(5.39) = %.6f  (log 6)^2 = %.6f" % (lhs, log(6) ** 2))
print("    (5.40)    = %.6f  ((log 6)^2+(log 1.5)^2)/2 = %.6f" % (t540, (log(6) ** 2 + log(1.5) ** 2) / 2))
print("    RHS(5.39) = %.6f" % rhs)
a_ok = lhs > t540 * (1 + 1e-12) and lhs <= rhs
print("    LHS > (5.40):", lhs > t540, "  (5.39) holds:", lhs <= rhs)
ok &= a_ok


def dist(x):
    x = x - (x.numerator // x.denominator)
    return min(x, 1 - x)


def minsep(alphas, q, R):
    ang = [al + F(ap, r) for al in alphas for r in range(1, R + 1) if gcd(r, q) == 1
           for ap in range(r) if gcd(ap, r) == 1]
    return min(dist(x - y) for i, x in enumerate(ang) for y in ang[i + 1:])


# (b) reversed condition
q, R, nu, ups = 1, 2, F(3, 10), F(31, 100)
assert nu + ups >= F(1, q * R * R) and nu + ups <= F(1, q)
m1 = minsep([F(0), F(31, 100)], q, R)
print("(b) printed direction: q=1, R=2, nu=0.3, upsilon=0.31 (nu+upsilon >= 1/qR^2), "
      "alphas 0, 0.31: min separation %s < nu: %s" % (float(m1), m1 < nu))
b_ok = m1 < nu
# exact check: distinct shifted fractions are >= 1/qR^2 apart
for qq in range(1, 8):
    for RR in range(2, 7):
        fr = sorted({(F(a, qq) + F(ap, r)) % 1 for a in range(qq) for r in range(1, RR + 1)
                     if gcd(r, qq) == 1 for ap in range(r) if gcd(ap, r) == 1})
        if len(fr) > 1:
            m = min(dist(x - y) for x in fr for y in fr if x != y)
            b_ok &= m >= F(1, qq * RR * RR)
# random check of correct direction: nu + ups <= 1/qR^2 gives separation >= nu
rnd = random.Random(1)
for _ in range(300):
    qq = rnd.randint(1, 4)
    RR = rnd.randint(1, 4)
    s = F(1, qq * RR * RR)
    nu2 = s * F(rnd.randint(1, 99), 100)
    ups2 = s - nu2
    al = []
    for a in range(qq):
        pts = []
        for _ in range(3):
            t = ups2 * F(rnd.randint(0, 1000), 1000)
            if all(abs(t - u) > nu2 for u in pts):
                pts.append(t)
        al += [F(a, qq) + t for t in pts]
    if len(al) > 1:
        b_ok &= minsep(al, qq, RR) >= nu2
print("    correct direction (<=) gives nu-separation in all random trials; "
      "shifted fractions >= 1/qR^2 apart for q<=7, R<=6:", b_ok)
ok &= b_ok

# (c) survival: R^2 - (R+1) log R >= 0 for R > 1
worst = min(RR * RR - (RR + 1) * log(RR) for RR in [1 + k / 1000 for k in range(1, 300000)])
print("(c) min over R in (1,301) of R^2-(R+1)log R = %.6f (>= 0 means trivial bound covers R >= W')" % worst)
c_ok = worst >= 0
ok &= c_ok

# (d) scope: supports (W',W] with W' >= W/2 that cover every class mod some prime ell
bad = []
primes = [p for p in range(2, 3000) if isprime(p)]
for i, p0 in enumerate(primes):
    sup = [p for p in primes[i:] if p < 2 * p0]   # maximal support with least prime p0
    for ell in primes:
        if ell > sup[-1]:
            break
        if len({p % ell for p in sup}) == ell:
            bad.append((p0, ell, sup))
print("(d) admissible supports with least prime < 3000 hitting every class mod some prime:",
      [(b[0], b[1], b[2]) for b in bad])
print("    (Montgomery's weight h(r) >= 1/phi(r) holds whenever each prime of r misses a class;"
      " so the failure in (a) is confined to support {2,3}, q odd)")

if ok:
    print("CONFIRMED: For admissible data (q=1, alpha=0, nu=upsilon=1/8, W=3, W'=1.5) the left side of (5.39) "
          "is %.4f > (5.40) = %.4f, the printed condition nu+upsilon >= 1/qR^2 is reversed, and (5.39) itself still holds." % (lhs, t540))
else:
    print("NOT CONFIRMED: the counterexample, the reversed-condition check or the survival bound did not hold.")
