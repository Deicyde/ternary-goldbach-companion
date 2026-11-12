"""Check of [H, Eq (8.43)] and the I_0 bound after it.

Claim: after (8.43) the book bounds I_0(t) = (1/pi) int_0^pi e^{t cos th} dth using
cos th = sqrt(1 - sin^2 th) < 1 - sin^2 th / 2 <= 1 - 2 th^2/pi^2, applied on all of
[0, pi]; both the "=" and the Jordan step "<=" fail for th in (pi/2, pi]. The needed
inequality cos th <= 1 - 2 th^2/pi^2 does hold on [0, pi], so
I_0(t) <= (sqrt(pi)/2^{3/2}) e^t / sqrt(t) stands.

Book inputs (mellintran.tex):
  - l.1062-1065 (8.43): I_2 <= x_0^{1-sigma} int_0^{pi/2} e^{-(...)} dalpha, and
    l.1078-1082: I_2 <= x_0^{-sigma} (pi/2) x_0 I_0(x_0^2/2), with
    I_0(t) = (1/pi) int_0^pi e^{t cos th} dth (th = 2 alpha runs over [0, pi]).
  - l.1085-1099: the chain cos th = sqrt(1-sin^2 th) < 1 - sin^2 th/2 <= 1 - 2th^2/pi^2
    and I_0(t) <= (1/pi) int_0^pi e^{t(1-2th^2/pi^2)} dth < sqrt(pi)/2^{3/2} e^t/sqrt t.

Confirms if: at th = 0.9 pi the "=" and the "<=" steps of the chain are false, and
f(th) = 1 - 2th^2/pi^2 - cos th >= 0 on a fine grid of [0, pi] (with f''' = -sin <= 0,
f(0) = f(pi) = 0, f''(0) > 0, f'(pi) < 0 proving it), and I_0(t) computed by
quadrature is below the printed bound at sample t.

Run: python3 -I eq_8_43.py

Ported from a 2026-11-06 check script.
"""
import math

PI = math.pi
th = 0.9 * PI
c = math.cos(th)
r = math.sqrt(1 - math.sin(th) ** 2)
m = 1 - math.sin(th) ** 2 / 2
jd = 1 - 2 * th ** 2 / PI ** 2
print("th = 0.9 pi: cos = %.10f, sqrt(1-sin^2) = %.10f, 1-sin^2/2 = %.10f, 1-2th^2/pi^2 = %.10f"
      % (c, r, m, jd))
eq_fails = abs(c - r) > 1e-6
jordan_fails = m > jd
print("  '=' step false: %s; '1-sin^2/2 <= 1-2th^2/pi^2' false: %s" % (eq_fails, jordan_fails))

# range on which the chain's steps fail
N = 4000
bad_eq = bad_j = 0
first_bad = None
fmin = 1e9
for i in range(N + 1):
    t = PI * i / N
    if abs(math.cos(t) - math.sqrt(max(0.0, 1 - math.sin(t) ** 2))) > 1e-12:
        bad_eq += 1
    if 1 - math.sin(t) ** 2 / 2 > 1 - 2 * t ** 2 / PI ** 2 + 1e-15:
        bad_j += 1
        if first_bad is None:
            first_bad = t / PI
    f = 1 - 2 * t ** 2 / PI ** 2 - math.cos(t)
    fmin = min(fmin, f)
print("grid of %d steps: '=' fails at %d points, Jordan step fails at %d points (first at th/pi = %.5f)"
      % (N, bad_eq, bad_j, first_bad))
print("min of f(th) = 1 - 2th^2/pi^2 - cos th on grid: %.3e" % fmin)
f2_0 = 1 - 4 / PI ** 2
f1_pi = math.sin(PI) - 4 * PI / PI ** 2
print("f(0) = 0, f(pi) = %.1e, f''(0) = 1 - 4/pi^2 = %.6f > 0, f'(pi) = -4/pi = %.6f < 0, f''' = -sin <= 0"
      % (1 - 2 - math.cos(PI), f2_0, f1_pi))
fix_ok = fmin >= -1e-15 and f2_0 > 0 and f1_pi < 0


def I0(t, n=20000):  # Simpson on (1/pi) int_0^pi e^{t cos th}
    h = PI / n
    s = math.exp(t) + math.exp(-t)
    for k in range(1, n):
        s += (4 if k % 2 else 2) * math.exp(t * math.cos(k * h))
    return s * h / 3 / PI


bound_ok = True
for t in (0.25, 0.79, 1.0, 5.0, 20.0, 100.0):
    v = I0(t)
    bnd = math.sqrt(PI) / 2 ** 1.5 * math.exp(t) / math.sqrt(t)
    print("t = %6.2f: I_0(t) = %.8e, bound sqrt(pi/8) e^t/sqrt(t) = %.8e, ratio %.6f"
          % (t, v, bnd, v / bnd))
    bound_ok &= v < bnd

if eq_fails and jordan_fails and bad_j > 0 and fix_ok and bound_ok:
    print("CONFIRMED: the chain cos th = sqrt(1-sin^2 th) < 1-sin^2 th/2 <= 1-2th^2/pi^2 after (8.43) "
          "is false on (pi/2, pi] (e.g. th = 0.9 pi), but cos th <= 1-2th^2/pi^2 holds on [0, pi], "
          "so I_0(t) <= sqrt(pi)/2^{3/2} e^t/sqrt(t) stands.")
else:
    print("NOT CONFIRMED: eq_fails=%s jordan_fails=%s fix_ok=%s bound_ok=%s"
          % (eq_fails, jordan_fails, fix_ok, bound_ok))
