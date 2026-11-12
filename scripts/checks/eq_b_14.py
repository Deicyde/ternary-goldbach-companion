"""Check of [H, (B.14)] (arg((4g + hat f)/(-16 log 2 k + hat h)) in (-pi/3, pi/3) on I).

Claim: the denominator has the wrong sign. With z1 = 4g + hat f and
z2 = -16 log 2 k + hat h, as printed arg(z1/z2) is near +-pi (|arg| >= 2.15 on
I), so (B.14) is false (and would not give |z1 log y + z2| <= max(|z1| log y,
|z2|)). The intended quantity is arg(z1/(-z2)); its maximum on I, 0.99134 at
t = 7.5, is exactly the value the book reports.

Book inputs:
  - notprem.tex l.34, l.100-102: e(x) = e^{2 pi i x}, hat f(t) = int e(-xt) f(x) dx.
  - intromin.tex l.124-125: eta_2(t) = 4 max(log 2 - |log 2t|, 0).
  - normfour.tex l.21-22 g; l.69-79 eta_2'' and f; l.176-191 eta_(y)'', h, k,
    (B.12); l.205-213 I = [0.3, 2252.21] minus [3.25, 3.65] and (B.14);
    l.216-219 the max step; l.257-260 the reported maximum 0.99134.

Method: z1, z2 by Gauss-Legendre (panels scaled with t). Check (B.12):
z1 = -(2 pi t)^2 hat(eta_2)(t) and z2 = -(2 pi t)^2 hat(log * eta_2)(t) at sample
t. Scan 0.005Z cap I up to t = 50, and a coarser grid (step 2.5) up to 2252.

Confirms if: (B.12) checks, |arg(z1/z2)| > pi/3 at every sampled t (so (B.14)
as printed is false), and max |arg(z1/(-z2))| on the fine grid is 0.99134 to
five digits.

Run: python3 -I eq_b_14.py

Ported from a 2026-11-06 check script.
"""
import cmath
import math

PI, L2 = math.pi, math.log(2)
e = lambda x: cmath.exp(2j * PI * x)
g = lambda t: 4 * e(-t / 4) - 4 * e(-t / 2) + e(-t)
k = lambda t: 2 * e(-t / 4) - e(-t / 2)

def f(x):
    return -4 / x**2 if x < 0.5 else 4 / x**2
def hh(x):
    return 4 / x**2 * (2 - 2 * math.log(2 * x)) if x < 0.5 else 4 / x**2 * (-2 + 2 * math.log(x))
def eta2(x):
    return 4 * max(L2 - abs(math.log(2 * x)), 0.0)

def gl(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for kk in range(2, n + 1):
                p0, p1 = p1, ((2 * kk - 1) * x * p1 - (kk - 1) * p0) / kk
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x); ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws
X, W = gl(16)

def ft(fun, t, pieces=((0.25, 0.5), (0.5, 1.0))):
    tot = 0j
    for a, b in pieces:
        panels = max(4, int(2 * t * (b - a)) + 4)
        hw = (b - a) / panels
        for p in range(panels):
            c = a + (p + 0.5) * hw
            for x, w in zip(X, W):
                u = c + 0.5 * hw * x
                tot += w * 0.5 * hw * fun(u) * cmath.exp(-2j * PI * u * t)
    return tot

z1 = lambda t: 4 * g(t) + ft(f, t)
z2 = lambda t: -16 * L2 * k(t) + ft(hh, t)

err = 0
for t in (0.7, 7.5, 40.3):
    a = -(2 * PI * t) ** 2 * ft(eta2, t)
    b = -(2 * PI * t) ** 2 * ft(lambda x: math.log(x) * eta2(x), t)
    err = max(err, abs(a - z1(t)), abs(b - z2(t)))
print("(B.12) check: max |z1 + (2 pi t)^2 hat eta_2|, |z2 + (2 pi t)^2 hat(log eta_2)| = %.2e" % err)
t = 7.5
print("t = 7.5: z1 = %s, z2 = %s, arg(z1/z2) = %.5f, arg(z1/(-z2)) = %.5f"
      % (z1(t), z2(t), cmath.phase(z1(t) / z2(t)), cmath.phase(z1(t) / -z2(t))))

inI = lambda t: not (3.25 <= t <= 3.65)
minp, maxc, tc = 10.0, 0.0, None
for i in range(60, 10001):  # 0.005 Z from 0.3 to 50
    t = 0.005 * i
    if not inI(t):
        continue
    a, b = z1(t), z2(t)
    minp = min(minp, abs(cmath.phase(a / b)))
    c = abs(cmath.phase(a / -b))
    if c > maxc:
        maxc, tc = c, t
print("fine grid 0.005Z cap I, t <= 50: min |arg(z1/z2)| = %.5f, max |arg(z1/(-z2))| = %.6f at t = %.3f" % (minp, maxc, tc))
minc = 10.0
for i in range(21, 902):  # 2.5 Z from 52.5 to 2252.5 (last point dropped)
    t = 2.5 * i
    if t > 2252.21:
        break
    minc = min(minc, abs(cmath.phase(z1(t) / z2(t))))
print("coarse grid 2.5Z, 52.5 <= t <= 2250: min |arg(z1/z2)| = %.5f" % minc)

ok = err < 1e-9 and min(minp, minc) > PI / 3 and abs(maxc - 0.99134) < 5e-6
if ok:
    print("CONFIRMED: as printed |arg(z1/z2)| >= %.4f > pi/3 at every sampled t in I, so (B.14) is false; with the denominator 16 log 2 k - hat h the maximum is %.5f at t = %.3f, the book's 0.99134."
          % (min(minp, minc), maxc, tc))
else:
    print("NOT CONFIRMED: the computed arguments do not match the claim.")
