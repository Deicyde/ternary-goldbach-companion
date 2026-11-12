"""Proposition 5.2.4 of [H] (arXiv:1501.05438v2): proof gaps in (5.54) and (5.56).

Claim: the proof of Prop. 5.2.4 has gaps: (5.54) inherits a gap from (5.51), and (5.56)
inherits from Lemma 5.2.1 a missing hypothesis under which Montgomery's inequality applies;
the printed bounds themselves stay true.

Book inputs (typeII.tex):
  - Prop. 5.2.4 hypotheses x >= W >= 1, W' >= W/2, U' >= x/2W, Q >= 3.5W,
    |delta/x| <= 1/qQ, q <= Q (l. 1193-1199); S_2 as in (5.38) (l. 860-864), m odd for v = 2;
    (5.54) (l. 1212-1218); (5.56) (l. 1228-1235).
  - Lemma 5.2.1 (l. 887-935): (5.40) (l. 916-921) is claimed for every squarefree r <= R,
    (r,q) = 1, with R = 1/sqrt((nu+upsilon) q); proof of (5.56) takes upsilon = (x/4W)|delta|/x,
    nu = |delta q|/x (l. 1289-1291).
  - Lemma 5.2.2 proof (l. 1003-1112): weights (W/2 + (3/2)(1/qrR - 1/Q)^-1)^-1 (l. 1025),
    (5.47)/(5.48) (l. 1029-1042), sigma = 1/(2 e^{0.50136}) (l. 1057), the chain with
    1/Q <= 1/(3.5W) (l. 1060-1069), the R = 2 case for odd q in (W/13.5, W/2] (l. 1096-1112),
    which checks q < W' but not 2 <= W' (Montgomery for r = 2 needs it).
  - (5.51) is obtained "proceeding again as before" (l. 1178); (5.54) is (5.51) with
    A_0 = U', A_1 = x/W (l. 1255-1262).

What is computed:
  (a) R = 2 step of Lemma 5.2.2 at W = 3, W' = 1.5, q = 1, Q = 3.5W, beta = 0:
      (5.47) > (5.48), i.e. the Montgomery step fails (support primes {2,3}).
  (b) (5.56) example x = 1000, W = 3, W' = 1.5, U' = x/2W, q = 1, a = 0, delta = 1, Q = 1000:
      all hypotheses hold, R = 3.44 > W', and the left side of Lemma 5.2.1 exceeds (5.40).
  (c) (5.54) and (5.56) themselves hold at these points (so: proof gap, not false).
  (d) The claim's other mechanism (weighted sieve applied with N = W/2 while the support can
      span W/2 + 1/2 integers): the literal-N threshold W >= sigma/(1-c)^2 = 10478.007, and the
      check that with the N - 1 form of the weighted sieve (Cohen's dilation of [MV, (1.6)])
      N - 1 = floor(W) - floor(W') - 1 < W/2 always, so this mechanism is not a real gap.

Confirms: (a) and (b) show failing steps while (c) holds.

Run: python3 -I proposition_5_2_4.py

Ported from a 2026-11-06 check script.
"""
import cmath
import math
from decimal import Decimal as D, getcontext

getcontext().prec = 50
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


ok = {}

# ---------------- (a) R = 2 case of Lemma 5.2.2 at W = 3, W' = 1.5 -----------------
print("(a) Lemma 5.2.2, R = 2 case, W = 3, W' = 1.5, q = 1, Q = 3.5W = 10.5, angle beta = 0")
W, Wp, q, Q, R = 3.0, 1.5, 1, 10.5, 2
pr = primes_in(Wp, W)
print("   support primes:", pr, "; q odd, W/13.5 < q <= W/2:", W / 13.5 < q <= W / 2, "; q < W':", q < Wp)
w = {r: 1 / (W / 2 + 1.5 / (1 / (q * r * R) - 1 / Q)) for r in (1, 2)}
lhs547 = sum(w[r] / phi(r) * abs(S(0, pr)) ** 2 for r in (1, 2))
rhs548 = sum(w[r] * sum(abs(S(a / r, pr)) ** 2 for a in range(1, r + 1) if math.gcd(a, r) == 1) for r in (1, 2))
print(f"   w_1 = {w[1]:.6f}, w_2 = {w[2]:.6f}")
print(f"   (5.47) = {lhs547:.6f}   (5.48) = {rhs548:.6f}   (5.47) <= (5.48): {lhs547 <= rhs548}")
print(f"   Montgomery r=2: |S(0)|^2/phi(2) = {abs(S(0, pr))**2:.6f} vs |S(1/2)|^2 = {abs(S(0.5, pr))**2:.6f}")
ok["a_step_fails"] = lhs547 > rhs548

# ---------------- (b) (5.56) example -----------------
print("\n(b) (5.56) example x=1000, W=3, W'=1.5, U'=x/2W, q=1, a=0, delta=1, Q=1000")
x, W, Wp, q, dl, Q = 1000.0, 3.0, 1.5, 1, 1.0, 1000.0
hyp = [x >= W >= 1, Wp >= W / 2, Q >= 3.5 * W, abs(dl / x) <= 1 / (q * Q) + 1e-15, q <= Q,
       x / (4 * W) + q <= x / (abs(dl) * q)]
print("   hypotheses of Prop 5.2.4 and of (5.56) hold:", all(hyp))
nu, ups = abs(dl) * q / x, (x / (4 * W)) * abs(dl) / x
Rb = 1 / math.sqrt((nu + ups) * q)
print(f"   nu = {nu}, upsilon = {ups:.6f}, R = {Rb:.6f} > W' = {Wp}: {Rb > Wp}")
pr = primes_in(Wp, W)
rs = [r for r in range(1, int(Rb) + 1) if sqfree(r) and math.gcd(r, q) == 1]
lsq = sum(LOG(p) ** 2 for p in pr)
best = None
for alpha in (0.0005, 0.5005):  # 2 alpha = 0/1 + 1/1000
    ms = [m for m in range(1, int(x / W) + 1) if m % 2 == 1 and x / (2 * W) < m <= x / W]
    lhs = sum(abs(S(alpha * m, pr)) ** 2 for m in ms)
    inner = sum(abs(S(alpha * m + a / r, pr)) ** 2 for m in ms for r in rs
                for a in range(1, r + 1) if math.gcd(a, r) == 1)
    msum = sum(1 / phi(r) for r in rs)
    b540 = inner / msum
    ls_bound = (W - Wp + 1 / nu) * lsq
    L = (x / (abs(dl) * q)) / (q + x / (4 * W))
    fac = min(1.0, 2 * q / phi(q) / LOG(L))
    rhs556 = fac * (x / abs(dl * q) + W / 2) * lsq
    print(f"   alpha={alpha}: #m={len(ms)}, r in {rs}, sum mu^2/phi = {msum}")
    print(f"     S_2 = {lhs:.4f};  (5.40) = {b540:.4f};  S_2 <= (5.40): {lhs <= b540}")
    print(f"     large-sieve step {inner:.2f} <= (W-W'+1/nu) sum log^2 p = {ls_bound:.2f}: {inner <= ls_bound}")
    print(f"     Lambda = {L:.6f}, min(1, 2/log Lambda) = {fac:.6f}; (5.56) RHS = {rhs556:.4f}; holds: {lhs <= rhs556}")
    if alpha == 0.0005:
        ok["b_540_false"] = lhs > b540
        vals = (lhs, b540)
        ok["c_556_holds"] = lhs <= rhs556
print(f"   |delta| q W = {abs(dl)*q*W} < 16, and R^2 = {Rb**2:.4f} <= 4W/(|delta|q) = {4*W/(abs(dl)*q)}")

# (c) (5.54) at the same x, W, W' with q = 1 (needs q < W/2): trivial bound vs RHS
q = 1
ms = [m for m in range(1, int(x / W) + 1) if m % 2 == 1 and x / (2 * W) < m <= x / W]
triv = len(ms) * (LOG(2) + LOG(3)) ** 2
rhs554 = (x / (4 * phi(q) * LOG(W / (2 * q))) + q / phi(q) * W / LOG(W / (2 * q))) * lsq
print(f"\n(c) (5.54) at x=1000, W=3, W'=1.5, q=1: trivial S_2 <= {triv:.2f} <= RHS {rhs554:.2f}: {triv <= rhs554}")
ok["c_554_holds"] = triv <= rhs554

# ---------------- (d) literal-N mechanism -----------------
print("\n(d) weighted sieve with N = W/2 (book) versus the integer count of (W', W]")
sig = 1 / (2 * D("0.50136").exp())
c = 3 * sig / (1 - sig / D("3.5"))
thr = sig / (1 - c) ** 2
print(f"   sigma = {float(sig):.7f}, 3sigma/(1-sigma/3.5) = {float(c):.7f}, slack = {float(1-c):.7f}")
print(f"   literal N = W/2 + 1/2: r = 1 step needs W >= sigma/(1-c)^2 = {float(thr):.3f} (q = 1)")
Wl = D(37)
Rl = (sig * Wl).sqrt()
lhs = 19 + D("1.5") / (1 / Rl - 1 / (D("3.5") * Wl))
rhs = Wl / 2 * (1 + 1 / Rl)
print(f"   W = 37, W' = 18.5 (primes 19..37 span 19 integers): N + 1.5(1/R-1/Q)^-1 = {float(lhs):.4f} > (W/2)(1+1/R) = {float(rhs):.4f}")
worst = max((math.floor(Wv) - math.floor(Wv / 2) - 1) - Wv / 2
            for Wv in [k / 8 for k in range(8, 8 * 20000)])
print(f"   N - 1 - W/2 <= {worst:.4f} < 0 on W in [1, 20000] (step 1/8), W' = W/2: the N-1 form of the")
print("   weighted sieve (Cohen's dilation) is dominated by the book's weight W/2 for every W;")
print("   so the W >= 10478 restriction is a citation looseness, not a gap.")
ok["d_literal_threshold"] = abs(float(thr) - 10478.007) < 0.01

print("\nflags:", ok)
if ok["a_step_fails"] and ok["b_540_false"] and ok["c_556_holds"] and ok["c_554_holds"]:
    print("CONFIRMED: at W = 3, W' = 1.5 the Montgomery steps behind (5.51)/(5.54) and (5.56) fail "
          f"((5.47) {lhs547:.4f} > (5.48) {rhs548:.4f}; S_2 {vals[0]:.2f} > (5.40) {vals[1]:.2f}) while (5.54) and (5.56) hold, "
          "so the proof has gaps; the literal-N mechanism (W >= 10478) is not one, since N - 1 < W/2.")
else:
    print("NOT CONFIRMED: the Montgomery steps do not fail at the test points as claimed.")
