"""Eq 5.51 of [H] (H. A. Helfgott, The ternary Goldbach problem, arXiv:1501.05438v2).

Claim: the proof of (5.51) ("proceed again as before", i.e. the proof of (5.43)) has gaps:
(i) the weighted large sieve is used with W/2 in place of N although the primes in (W', W]
can span (W+1)/2 integers, so that the per-r weight step would fail for W < 168; (ii) in the
R = 2 branch the proof checks q < W' where R <= W' is needed, and R = 2 > W' is possible for
2 < W < 4; (iii) the same branch asserts qR^2 < W, false for q >= W/4. The statement holds.

Book inputs (book/src/typeII.tex):
  - Montgomery's inequality (5.46) "for each square-free r <= W'" (lines 1017-1023);
  - weights (W/2 + (3/2)(1/(qrR) - 1/Q)^(-1))^(-1), MV73 (1.6) (lines 1024-1047);
  - case q <= W/13.5: R = (sigma W/q)^(1/2), sigma = 1/(2 e^(2*0.25068)), per-r bound
    W/2 + (3/2)(1/qrR - 1/Q)^(-1) < (W/2)(1 + r/R) (lines 1053-1069);
  - case W/13.5 < q < W/2, q odd: "set R=2; clearly qR^2 < W <= Q and q < W/2 <= W', and so
    this choice of R is valid" (lines 1098-1101);
  - (5.50) and (5.51) of Lemma 5.2.3 (lines 1146-1159); (5.51) proof (lines 1178-1180).
  MV73 (1.6) with N, and its dilated form: applying (1.6) to b_{2n} = a_n at the points
  (x_r + j)/2, j = 0, 1, gives weights (N - 1/2 + (3/2) delta_r^-1)^-1.

What this computes: (A) per-r margin (W/2)(1+r/R) - [N + (3/2)(1/qrR - 1/Q)^-1] with
N = floor(W) - floor(W/2) (the integer count) is negative at W = 167, q = 2, r = 5, but
N - 1/2 <= W/2 always, so with the dilated form the book's W/2 is valid and point (i) is not
a gap; (B) at W = 3, W' = 1.5, q = 1, Q = 10.5 (R = 2 branch), (5.46) with r = 2 fails and the
step (5.47) <= (5.48) fails, while (5.51) still follows from (5.50) for 2 < W <= 4;
(C) W = 10, q = 3: qR^2 = 12 > W but < 3.5W <= Q.
Confirms the claim (as a proof gap in the R = 2 branch) if (B) and (C) hold.

Run: python3 -I eq_5_51.py
Ported from a 2026-11-06 check script.
"""
import math


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def squarefree(n):
    return all(n % (d * d) for d in range(2, math.isqrt(n) + 1))


sigma = 1 / (2 * math.exp(2 * 0.25068))
print(f"sigma = {sigma:.7f}")

print("=== A: per-r weight step, N form vs book's W/2 (Q = 3.5W) ===")


def margin(W, q, r, Neff):
    Q = 3.5 * W
    R = math.sqrt(sigma * W / q)
    return (W / 2) * (1 + r / R) - (Neff + 1.5 / (1 / (q * r * R) - 1 / Q))


W, q, r = 167, 2, 5
Nint = math.floor(W) - math.floor(W / 2)
print(f"W={W}, q={q}, r={r}: N=floor(W)-floor(W/2)={Nint}; margin with N: {margin(W, q, r, Nint):.5f}; "
      f"with W/2: {margin(W, q, r, W / 2):.5f}")
last_fail = None
min_book = 1e9
for i in range(28, 801):
    W = i / 2
    for q in range(1, int(W / 13.5) + 1):
        R = math.sqrt(sigma * W / q)
        for r in range(1, int(R) + 1):
            if math.gcd(r, q) != 1 or not squarefree(r):
                continue
            Nint = math.floor(W) - math.floor(W / 2)
            if margin(W, q, r, Nint) < 0:
                last_fail = (W, q, r)
            min_book = min(min_book, margin(W, q, r, W / 2))
print(f"scan W in [14,400]: last failure of the N form at (W,q,r)={last_fail}; "
      f"min margin of book form = {min_book:.4f}")
excess = max(math.floor(i / 8) - math.floor(i / 16) - 0.5 - i / 16 for i in range(8, 400001))
print(f"max over W in [1, 50000] (step 1/8) of N - 1/2 - W/2 = {excess}")
point_i_gap = excess > 0 or min_book <= 0
print(f"point (i) is a gap: {point_i_gap}")

print("\n=== B: R = 2 branch at W = 3, W' = 1.5, q = 1, Q = 10.5 ===")
W, Wp, q, Q, R = 3.0, 1.5, 1, 10.5, 2
branch = (W / 13.5 < q < W / 2) and q % 2 == 1 and Q >= 3.5 * W and Wp >= W / 2
ps = [p for p in range(math.floor(Wp) + 1, math.floor(W) + 1) if is_prime(p)]
print(f"in R=2 branch: {branch}; primes in (W',W]: {ps}; R={R} > W'={Wp}: {R > Wp}")
S0 = sum(math.log(p) for p in ps)                      # S(beta) at beta = 0
Sh = sum(math.log(p) * math.cos(math.pi * p) for p in ps)  # S(beta + 1/2), real here
lhs546, rhs546 = S0 ** 2 / 1, Sh ** 2                  # (1/phi(2))|S(0)|^2 vs |S(1/2)|^2
print(f"(5.46), r=2, beta=0: (1/phi(2))|S(0)|^2 = {lhs546:.4f} vs |S(1/2)|^2 = {rhs546:.4f}")
w1 = 1 / (W / 2 + 1.5 / (1 / (q * 1 * R) - 1 / Q))
w2 = 1 / (W / 2 + 1.5 / (1 / (q * 2 * R) - 1 / Q))
v547 = (w1 + w2 / 1) * S0 ** 2
v548 = w1 * S0 ** 2 + w2 * Sh ** 2
logsq = sum(math.log(p) ** 2 for p in ps)
print(f"weights w1={w1:.5f}, w2={w2:.5f}; (5.47) = {v547:.4f}, (5.48) = {v548:.4f}, "
      f"sum (log p)^2 = {logsq:.4f}")
step_fails = branch and R > Wp and lhs546 > rhs546 and v547 > v548
# (5.51) from (5.50) on 2 < W <= 4 (here q = 1 is forced): W - W' + 2q <= W/2 + 2 < W/log(W/2)
survives = all((W / 2 + 2) < W / math.log(W / 2) for W in (2 + k / 1000 for k in range(1, 2001)))
print(f"(5.50) gives (5.51) on (2,4]: W/2+2 < W/log(W/2) everywhere: {survives}")

print("\n=== C: 'qR^2 < W' in the R = 2 branch ===")
W, q = 10, 3
inbranch = W / 13.5 < q < W / 2 and q % 2 == 1
print(f"W={W}, q={q} (in branch: {inbranch}): qR^2 = {q * 4} > W: {q * 4 > W}; "
      f"qR^2 < 3.5W: {q * 4 < 3.5 * W}")
c_ok = inbranch and q * 4 > W and q * 4 < 3.5 * W

if step_fails and survives and c_ok:
    msg = ("CONFIRMED: the R=2 branch of the proof of (5.51) is invalid for 2<W<4 (W=3: R=2>W'=1.5, "
           "(5.46) fails 3.21>0.16) and misstates qR^2<W, though (5.51) still holds")
    msg += ("; the N vs W/2 point is not a gap, since the dilated MV sieve has N-1/2 <= W/2."
            if not point_i_gap else "; the N vs W/2 point is also a gap.")
    print(msg)
else:
    print("NOT CONFIRMED: the R=2 branch checks did not reproduce the claimed failure.")
