"""Eq (5.56) of [H] (arXiv:1501.05438v2): Lemma 5.2.1 is applied with R > W'.

Claim: (5.56) is Lemma 5.2.1 with R = (q(nu+upsilon))^{-1/2} = sqrt(Lambda); the lemma's proof
applies Montgomery's inequality for every squarefree r <= R without a hypothesis that makes it
valid, and in the example x = 1000, W = 3, W' = 1.5, q = 1, a = 0, delta = 1, Q = 1000 that step
fails, while (5.56) itself still holds.

Book inputs (typeII.tex):
  - Lemma 5.2.1 (l. 887-935): statement for any W, W' >= 1, W' >= W/2; (5.40) (l. 916-921)
    for all squarefree r <= R, (r,q) = 1, R = 1/sqrt((nu+upsilon) q) (l. 927).
  - Prop. 5.2.4 hypotheses (l. 1193-1199); S_2 as in (5.38) (l. 860-864), m odd;
    (5.56) (l. 1228-1235) with hypothesis x/4W + q <= x/|delta| q;
    its proof: upsilon = (x/4W)|delta|/x, nu = |delta q|/x (l. 1289-1291).

Computed: hypotheses, R, the Montgomery inequality at r = 2 and r = 3, S_2 versus the
right side of (5.40), the large-sieve step, and (5.56). Also a second point with R > W'
(W = 7, W' = 3.5) where the Montgomery step and (5.40) hold, which shows that R > W' alone
does not break the proof (the failure needs the support to be {2,3}).

Confirms: hypotheses hold, R > W', S_2 > (5.40) and S_2 <= RHS of (5.56).

Run: python3 -I eq_5_56.py

Ported from a 2026-11-06 check script.
"""
import cmath
import math

LOG = math.log


def S(beta, primes):
    return sum(LOG(p) * cmath.exp(2j * math.pi * beta * p) for p in primes)


def phi(n):
    r, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            r -= r // p
        p += 1
    if m > 1:
        r -= r // m
    return r


def sqfree(n):
    return all(n % (p * p) for p in range(2, int(n ** 0.5) + 1))


def primes_in(lo, hi):
    return [p for p in range(2, int(hi) + 1) if lo < p <= hi and all(p % d for d in range(2, int(p ** 0.5) + 1))]


def case(x, W, Wp, q, a, dl, Q, label):
    print(f"== {label}: x={x}, W={W}, W'={Wp}, U'=x/2W, q={q}, a={a}, delta={dl}, Q={Q}")
    hyp = [x >= W >= 1, Wp >= W / 2, Q >= 3.5 * W, abs(dl / x) <= 1 / (q * Q) + 1e-15, q <= Q,
           math.gcd(a, q) == 1, x / (4 * W) + q <= x / (abs(dl) * q)]
    nu, ups = abs(dl) * q / x, (x / (4 * W)) * abs(dl) / x
    R = 1 / math.sqrt((nu + ups) * q)
    L = (x / (abs(dl) * q)) / (q + x / (4 * W))
    fac = min(1.0, 2 * q / phi(q) / LOG(L))
    pr = primes_in(Wp, W)
    lsq = sum(LOG(p) ** 2 for p in pr)
    rs = [r for r in range(1, int(R) + 1) if sqfree(r) and math.gcd(r, q) == 1]
    msum = sum(1 / phi(r) for r in rs)
    alpha = (a / q + dl / x) / 2
    ms = [m for m in range(1, int(x / W) + 1) if m % 2 == 1 and x / (2 * W) < m <= x / W]
    s2 = sum(abs(S(alpha * m, pr)) ** 2 for m in ms)
    inner = sum(abs(S(alpha * m + b / r, pr)) ** 2 for m in ms for r in rs
                for b in range(1, r + 1) if math.gcd(b, r) == 1)
    b540 = inner / msum
    rhs556 = fac * (x / abs(dl * q) + W / 2) * lsq
    print(f"   hypotheses hold: {all(hyp)};  x/4W+q = {x/(4*W)+q:.4f} <= x/|delta|q = {x/(abs(dl)*q)}")
    print(f"   Lambda = {L:.6f}, R = sqrt(Lambda) = {R:.6f}, W' = {Wp}, R > W': {R > Wp}; |delta|qW = {abs(dl)*q*W}")
    print(f"   min(1, 2q/phi(q)/log Lambda) = {fac:.6f}; support primes {pr}; r used: {rs}")
    mont = {}
    for r in rs[1:]:
        worst = min(sum(abs(S(alpha * m + b / r, pr)) ** 2 for b in range(1, r + 1) if math.gcd(b, r) == 1)
                    / (abs(S(alpha * m, pr)) ** 2 / phi(r)) for m in ms)
        mont[r] = worst
        print(f"   Montgomery at r={r}: min over m of sum_b |S(am+b/r)|^2 / (|S(am)|^2/phi(r)) = {worst:.6f} (>= 1 needed)")
    print(f"   #m = {len(ms)}; S_2 = {s2:.4f}; (5.40) = {b540:.4f}; S_2 <= (5.40): {s2 <= b540}")
    print(f"   large-sieve step: {inner:.2f} <= (W-W'+1/nu) sum log^2 p = {(W - Wp + 1/nu) * lsq:.2f}")
    print(f"   (5.56): S_2 = {s2:.4f} <= {rhs556:.4f}: {s2 <= rhs556}")
    return dict(hyp=all(hyp), R_gt=R > Wp, s2=s2, b540=b540, rhs=rhs556, mont=mont)


A = case(1000.0, 3.0, 1.5, 1, 0, 1.0, 1000.0, "claim's example")
print("   with a_p = log p: |S(0)|^2 =", round(abs(S(0, [2, 3])) ** 2, 6), " phi(2)|S(1/2)|^2 =", round(abs(S(0.5, [2, 3])) ** 2, 6))
B = case(7000.0, 7.0, 3.5, 1, 0, 1.0, 7000.0, "control point with R > W' and support {5,7}")

print()
if A["hyp"] and A["R_gt"] and A["s2"] > A["b540"] and A["s2"] <= A["rhs"]:
    tail = ("; at W = 7, W' = 3.5 (R > W' too) the step is valid, so R > W' alone does not break it"
            if B["R_gt"] and B["s2"] <= B["b540"] else "")
    print(f"CONFIRMED: in the example R = 3.44 > W' and the Montgomery step fails at r = 2, so (5.40) is false "
          f"(S_2 = {A['s2']:.2f} > {A['b540']:.2f}) while (5.56) holds ({A['s2']:.2f} <= {A['rhs']:.2f}){tail}.")
else:
    print("NOT CONFIRMED: the example does not exhibit a failing step of the proof of (5.56).")
