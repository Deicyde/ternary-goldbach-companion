"""Eq (6.2) of [H] (arXiv:1501.05438v2): the printed value of |eta''_{2,rho}|_1.

Claim: the middle expression printed for |eta''_{2,rho}|_1 in (6.2) is 1/4 of the true value
(as if eta_2 lacked its factor 4) and, for e^2 < rho < 4e^2, also misses the interior turning
points of eta'_{2,rho}; the final bound |eta''_{2,rho}|_1 < 48 log rho is nevertheless true.

Book inputs:
  - eta_2(t) = 4 max(log 2 - |log 2t|, 0) (intromin.tex l. 124-125);
  - (6.1): |eta_2''|_1 = 48 (minarctotals.tex l. 39-41), so point masses of eta'' count;
  - (6.2): eta_{2,rho}(t) = log(rho t) eta_2(t), rho >= 4, and the printed line
    |eta''_{2,rho}|_1 = 4log(rho/4) + |2log rho - 4log(rho/4)| + |4log2 - 4log rho|
                       + |log rho - 4log2| + |log rho| < 48 log rho  (minarctotals.tex l. 43-51).

Computed: |eta''_{2,rho}|_1 = total variation of eta'_{2,rho}, by (i) jumps plus exact
integrals of |eta''| with turning points, and (ii) brute-force total variation of a sampled
derivative; the sanity value |eta_2''|_1 = 48; the printed expression; the ratio; and
max of true/(48 log rho) on a grid rho in [4, 10^30]. Lines 1-2 of (6.2) at rho = 4 as well.

Confirms: true/printed = 4 for rho outside (e^2, 4e^2), > 4 inside, and true < 48 log rho.

Run: python3 -I eq_6_2.py

Ported from a 2026-11-06 check script.
"""
import math

L2 = math.log(2)


def eta2(t):
    return 4 * max(L2 - abs(math.log(2 * t)), 0.0) if t > 0 else 0.0


def deta(t, rho):
    """eta'_{2,rho} on the open pieces; 0 outside [1/4, 1]."""
    if 0.25 < t < 0.5:
        return 4 / t * math.log(4 * rho * t * t)
    if 0.5 < t < 1:
        return -4 / t * math.log(rho * t * t)
    return 0.0


def tv_exact(rho):
    """jumps of eta' + integral of |eta''| on each piece (eta' piecewise monotone between turning points)."""
    jumps = 16 * math.log(rho / 4) + 16 * math.log(rho / 2) + 4 * math.log(rho)
    pts1 = [0.25, 0.5]
    t0 = math.e / (2 * math.sqrt(rho))
    if 0.25 < t0 < 0.5:
        pts1 = [0.25, t0, 0.5]
    pts2 = [0.5, 1.0]
    t1 = math.e / math.sqrt(rho)
    if 0.5 < t1 < 1:
        pts2 = [0.5, t1, 1.0]
    f1 = lambda t: 4 / t * math.log(4 * rho * t * t)
    f2 = lambda t: -4 / t * math.log(rho * t * t)
    smooth = sum(abs(f1(b) - f1(a)) for a, b in zip(pts1, pts1[1:])) + sum(abs(f2(b) - f2(a)) for a, b in zip(pts2, pts2[1:]))
    return jumps + smooth


def tv_brute(rho, n=200000):
    """total variation of eta' sampled on a fine grid of [0.2, 1.05] (jumps captured by the grid)."""
    ts = [0.2 + 0.85 * k / n for k in range(n + 1)]
    vals = []
    for t in ts:
        if abs(t - 0.25) < 1e-12 or abs(t - 0.5) < 1e-12 or abs(t - 1) < 1e-12:
            t += 1e-9
        vals.append(deta(t, rho))
    return sum(abs(b - a) for a, b in zip(vals, vals[1:]))


def printed(rho):
    l = math.log(rho)
    return 4 * math.log(rho / 4) + abs(2 * l - 4 * math.log(rho / 4)) + abs(4 * L2 - 4 * l) + abs(l - 4 * L2) + abs(l)


# sanity: |eta_2''|_1 = 48 with the same convention
def deta2(t):
    if 0.25 < t < 0.5:
        return 4 / t
    if 0.5 < t < 1:
        return -4 / t
    return 0.0


n = 200000
ts = [0.2 + 0.85 * k / n + 1e-9 for k in range(n + 1)]
v = [deta2(t) for t in ts]
print("sanity |eta_2''|_1 (sampled TV of eta_2') =", round(sum(abs(b - a) for a, b in zip(v, v[1:])), 4), "(book (6.1): 48)")

print(f"{'rho':>10} {'printed':>12} {'true(exact)':>12} {'true(brute)':>12} {'ratio':>8} {'48log':>10}")
rows = []
for rho in [4, math.e ** 2, 10, 16, 20, 4 * math.e ** 2, 100, 1e6]:
    p, te, tb = printed(rho), tv_exact(rho), tv_brute(rho)
    rows.append((rho, p, te, tb))
    print(f"{rho:10.4f} {p:12.6f} {te:12.6f} {tb:12.6f} {te/p:8.4f} {48*math.log(rho):10.4f}")

brute_ok = all(abs(te - tb) < 1e-3 * te for _, _, te, tb in rows)
grid = [4 * (1.001 ** k) for k in range(0, 66000) if 4 * (1.001 ** k) <= 1e30]
ratios = [(tv_exact(r) / printed(r), r) for r in grid]
out = [x for x, r in ratios if not (math.e ** 2 < r < 4 * math.e ** 2)]
ins = [x for x, r in ratios if math.e ** 2 + 1e-6 < r < 4 * math.e ** 2 - 1e-6]
mx = max((tv_exact(r) / (48 * math.log(r)), r) for r in grid)
print(f"grid of {len(grid)} rho in [4, 1e30]: ratio outside (e^2,4e^2) in [{min(out):.6f}, {max(out):.6f}]; "
      f"inside: min {min(ins):.6f}, max {max(ins):.6f}")
print(f"max true/(48 log rho) = {mx[0]:.6f} at rho = {mx[1]:.4g}")
print(f"turning points at rho = 16: t0 = e/(2 sqrt rho) = {math.e/8:.6f}, t1 = e/sqrt rho = {math.e/4:.6f}")

# lines 1-2 of (6.2) at rho = 4
rho = 4.0
N = 200000
l1 = sum(abs(math.log(rho * t) * eta2(t)) for t in [0.25 + 0.75 * (k + 0.5) / N for k in range(N)]) * 0.75 / N
print(f"rho = 4: |eta_2,rho|_1 = {l1:.6f} < log rho = {math.log(rho):.6f};  2 eta_2,rho(1/2) = {2*math.log(rho/2)*eta2(0.5):.6f} = 8 (log 2)^2 = {8*L2*L2:.6f}")

four_out = abs(min(out) - 4) < 1e-6 and abs(max(out) - 4) < 1e-6
if brute_ok and four_out and min(ins) > 4 and mx[0] < 1:
    print("CONFIRMED: the printed middle expression of (6.2) is exactly 1/4 of |eta''_{2,rho}|_1 for rho outside "
          f"(e^2, 4e^2) and less than 1/4 inside (ratio up to {max(ins):.4f}), e.g. {rows[0][1]:.3f} vs {rows[0][2]:.3f} at rho = 4; "
          "the final bound < 48 log rho still holds.")
else:
    print("NOT CONFIRMED: the printed expression does not differ from the true value as claimed.")
