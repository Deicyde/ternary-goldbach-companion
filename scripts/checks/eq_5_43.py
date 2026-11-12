"""Eq 5.43 (proof of Lemma 5.2.2, typeII.tex:1003-1112).

Claim: in Case B (q odd, W/13.5 < q < W/2, R = 2, typeII.tex:1099-1101) the
text's "clearly qR^2 < W" is false for q >= W/4 (only qR^2 < Q is needed, and
it holds since Q >= 3.5W), and the inference "q < W/2 <= W', so R = 2 is valid"
misses that validity needs R <= W' (typeII.tex:1023, 1028), which fails for
q = 1, W' < 2 <= W, where Montgomery's inequality (5.46) with r = 2 is false;
Case A (typeII.tex:1058-1069) prints rW/R for r/R and 'q < W'' for R <= W'
(true); (5.43) itself survives.

Book inputs: Lemma 5.2.2 hypotheses W >= 1, W' >= W/2, q < W/2, Q >= 3.5W
(typeII.tex:954-962); (5.43) (typeII.tex:963-967); (5.46) for square-free
r <= W' (typeII.tex:1017-1023); Case A: R = (sigma W/q)^(1/2),
sigma = 1/(2 e^(2*0.25068)) (typeII.tex:1053-1069); Case B inequality for
2 <= t <= 13.5 (typeII.tex:1102-1112).

Confirming output: a Case B instance with qR^2 >= W but < 3.5W; the Case B
edge q = 1, W = 3, W' = 1.5 with R = 2 > W' where (5.46) fails at r = 2 and
alpha = 0, while (5.43) holds there by the trivial bound; Case A's expression
equals (W/2)(1 + c r/R) with c = 3 sigma/(1 - sigma/3.5) < 1, not (W/2)(1 + c rW/R),
and R <= W/2 <= W' there; the Case B final inequality holds on [2, 13.5].

Run: python3 -I eq_5_43.py
Ported from a 2026-11-06 check script.
"""
from math import log, exp, pi, cos, sin, sqrt

ok = True

# Case B: qR^2 < W
W, q, R = 100.0, 41, 2
print("Case B: W=100, q=41 (odd, W/13.5 < q < W/2): qR^2 =", q * R * R, "> W:", q * R * R > W,
      "; < 3.5W <= Q:", q * R * R < 3.5 * W)
ok &= (q * R * R >= W) and (q * R * R < 3.5 * W) and (W / 13.5 < q < W / 2)
# in general for W/4 <= q < W/2: 4q in [W, 2W) < 3.5W


def S2(alpha, P):
    re = sum(log(p) * cos(2 * pi * alpha * p) for p in P)
    im = sum(log(p) * sin(2 * pi * alpha * p) for p in P)
    return re * re + im * im


# Case B edge: q = 1, W = 3, W' = 1.5
q, W, Wp, R = 1, 3.0, 1.5, 2
assert W >= 1 and Wp >= W / 2 and q < W / 2 and W / 13.5 < q and q % 2 == 1
P = [2, 3]   # primes in (1.5, 3]
lhs = S2(0.0, P) / 1          # (1/phi(2)) |S(0)|^2
rhs = S2(0.5, P)              # sum over a' = 1 mod 2
print("Case B edge q=1, W=3, W'=1.5: R=2 > W':", R > Wp, "; (5.46) at r=2, alpha=0: %.6f <= %.6f ? %s"
      % (lhs, rhs, lhs <= rhs))
ok &= (R > Wp) and (lhs > rhs)
# fraction of alpha where (5.46) at r=2 fails
N = 10000
frac = sum(S2(k / N, P) > S2(k / N + 0.5, P) for k in range(N)) / N
print("    (5.46) at r=2 fails for a fraction %.3f of alpha in [0,1)" % frac)
# trivial bound: LHS <= #m * #P * sum(log p)^2 with #P <= 2 and #m <= ceil(A1-A0);
# (5.43) RHS (q=1) = ceil(A1-A0) * W/log(W/2) * sum(log p)^2; W/log(W/2) decreases on (2, 2e)
mn = min(Wt / log(Wt / 2) for Wt in [2 + k * 2 / 100000 for k in range(1, 100001)])
print("    min of W/log(W/2) on (2,4] = %.5f > 2 = max #primes in (W',W]: (5.43) holds trivially" % mn)
ok &= mn > 2

# Case A
sigma = 1 / (2 * exp(2 * 0.25068))
c = 3 * sigma / (1 - sigma / 3.5)
print("Case A: sigma = %.6f, 3 sigma/(1-sigma/3.5) = %.5f" % (sigma, c))
okA = c < 1
worst_rel = 0.0
for W in [13.5, 20.0, 100.0, 1000.0, 1e5]:
    for q in [1, 2, 3, 5, int(W / 13.5)]:
        if q < 1 or q > W / 13.5:
            continue
        R = sqrt(sigma * W / q)
        okA &= R >= 2 and q * R * R < 3.5 * W and R <= W / 2   # R <= W/2 <= W'
        for r in range(1, int(R) + 1):
            direct = W / 2 + 1.5 * q * r * R / (1 - sigma / 3.5)
            good = W / 2 * (1 + c * r / R)
            printed = W / 2 * (1 + c * r * W / R)
            worst_rel = max(worst_rel, abs(direct - good) / direct)
            if (W, q, r) == (1000.0, 3, 2):
                print("    W=1000, q=3, r=2: W/2+(3/2)qrR/(1-sigma/3.5) = %.5f, (W/2)(1+c r/R) = %.5f, printed (W/2)(1+c rW/R) = %.2f"
                      % (direct, good, printed))
okA &= worst_rel < 1e-12
print("    identity with r/R holds (max rel. diff %.1e); R >= 2, qR^2 < 3.5W, R <= W/2 <= W' on samples: %s" % (worst_rel, okA))
ok &= okA


# Case B final inequality
def f(t):
    return 1 / (0.5 + 1.5 / (t / 2 - 1 / 3.5)) + 1 / (0.5 + 1.5 / (t / 4 - 1 / 3.5)) - log(t / 2)


m = min((f(2 + k * 11.5 / 200000), 2 + k * 11.5 / 200000) for k in range(200001))
print("Case B inequality: min over t in [2,13.5] of LHS - log(t/2) = %.6f at t = %.4f" % m)
ok &= m[0] > 0

if ok:
    print("CONFIRMED: In Case B 'qR^2 < W' fails for q >= W/4 (qR^2 < 3.5W <= Q holds) and R = 2 > W' at q=1, W=3, W'=1.5 "
          "where (5.46) fails at r=2; Case A's rW/R should be r/R; (5.43) still holds.")
else:
    print("NOT CONFIRMED: one of the Case A/Case B checks did not come out as claimed.")
