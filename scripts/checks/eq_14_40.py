"""Check of [H, Eq (14.40)] (eq:golrof, f(t) <= 0.019562618 for all t > 0).

Claim: to extend (14.40) beyond t = 30000 the text says f(t) < (5/2)(log t)/t
whenever t > (log t)^2, "by c > 20/3".  This is false: f(t) ~ 10 (log t)/t.
The same reasoning gives f(t) < 10 (log t)/t (equivalent to
c t > (20/3)(log t)^2 - 20 b log t with b = log(12*2^(1/3)/2.004)), and
10 log(30000)/30000 = 0.0034 < 0.019562618, so (14.40) survives.

Book inputs:
  - conclusion.tex:661     c = 4 log(12*2^(1/3)/2.004) - log 3
  - conclusion.tex:663-664 f(t) = ((4/3) log t - c) / ((2/15) t - (2/3) log t + 2 log(12*2^(1/3)/2.004))
  - conclusion.tex:665-671 (14.40) f(t) <= 0.019562618 on [180, 30000] (bisection);
                           f(t) < (5/2)(log t)/t for t > (log t)^2, "by c > 20/3"
Confirms if f(t) > (5/2) log t/t at points t > 30000 (so the stated inequality
fails), while f(t) < 10 log t/t on a grid of t in [30000, 1e15] and the max of f
on [180, 30000] is <= 0.019562618.

Run: python3 -I eq_14_40.py

Ported from a 2026-11-06 check script.
"""
import math

b = math.log(12 * 2 ** (1 / 3) / 2.004)
c = 4 * b - math.log(3)


def f(t):
    L = math.log(t)
    return (4 / 3 * L - c) / (2 / 15 * t - 2 / 3 * L + 2 * b)


print(f"c = {c:.6f} (> 20/3 = {20 / 3:.6f}: {c > 20 / 3})")
fails = []
for t in (3e4, 1e5, 1e9):
    v, w, w10 = f(t), 2.5 * math.log(t) / t, 10 * math.log(t) / t
    print(f"t = {t:.0e}: f = {v:.4e}, (5/2)log t/t = {w:.4e}, 10 log t/t = {w10:.4e}, t > (log t)^2: {t > math.log(t) ** 2}")
    fails.append(v > w)
print(f"t*f(t)/log t at t = 1e12: {f(1e12) * 1e12 / math.log(1e12):.5f} (-> 10)")
# f < 10 log t/t on [30000, 1e15] (geometric grid) via the equivalent form
good = True
t = 3e4
while t <= 1e15:
    L = math.log(t)
    good &= c * t > 20 / 3 * L * L - 20 * b * L and f(t) < 10 * L / t
    t *= 1.001
print(f"f(t) < 10 log t/t on [3e4, 1e15]: {good}; 10 log(3e4)/3e4 = {10 * math.log(3e4) / 3e4:.5f}")
# max of f on [180, 30000]: grid + golden section refinement
best = max((f(180 * (30000 / 180) ** (k / 200000)), 180 * (30000 / 180) ** (k / 200000)) for k in range(200001))
lo, hi = best[1] * 0.999, best[1] * 1.001
g = (math.sqrt(5) - 1) / 2
for _ in range(200):
    a1, a2 = hi - g * (hi - lo), lo + g * (hi - lo)
    if f(a1) > f(a2):
        hi = a2
    else:
        lo = a1
fm = f((lo + hi) / 2)
print(f"max f on [180, 30000] = {fm:.10f} at t = {(lo + hi) / 2:.3f}; f(t) < 0 for t < 180: {f(179.9) < 0}")
ok = all(fails) and good and fm <= 0.019562618 and 10 * math.log(3e4) / 3e4 < 0.019562618
if ok:
    print(f"CONFIRMED: f(t) > (5/2)(log t)/t for t = 3e4, 1e5, 1e9 (f ~ 10 log t/t), so the text's extension step is false, but f(t) < 10 log t/t <= 0.0035 for t >= 30000 and max f on [180, 30000] = {fm:.10f}, so (14.40) holds.")
else:
    print("NOT CONFIRMED: the computation does not show the (5/2)(log t)/t step failing with (14.40) surviving.")
