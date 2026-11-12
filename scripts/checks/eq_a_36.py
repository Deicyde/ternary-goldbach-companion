"""Check of [H, (A.36)] (|h_H(t) - h(t)|/t < |h'|_oo (1 + (4/pi) log H)/H).

Claim: (A.36) is false for small t, so |(h - h_H)/t|_oo = oo: on the w < 0 half
of the integration by parts the weight e^{-w/H} reaches 2/t, but the next
display bounds that half as if it were e^{-|w|/H}. Going down from t = 2 the
inequality first fails near t = 9.2e-8 (H = 200) and t = 1.08e-4 (H = 25), and
the ratio is unbounded as t -> 0+.

Book inputs (normsapp.tex):
  - l.8-10   h(t) = t^2 (2-t)^3 e^{t-1/2} on [0,2]; l.61 Mellin transform.
  - l.21-39  h_H = h *_M F_H, F_H(y) = sin(H log y)/(pi log y), and (A.5):
             Mh_H(i tau) = Mh(i tau) for |tau| < H, 0 for |tau| > H.
  - l.531-534 (A.35): h_H(t) = int_{-H log(2/t)}^oo h(t e^{-w/H}) sin w/(pi w) dw.
  - l.552-582 the bound and (A.36); l.589-591 (A.37) |h'|_oo <= 2.805820379671.

Method: h_H(t) = (1/pi) Re int_0^H Mh(i tau) t^{-i tau} d tau (Mellin inversion
of (A.5)), with Mh from its exact series Mh(s) = 6e^{-1/2} sum_n 2^{s+n+5}/
(n!(s+n+2)(s+n+3)(s+n+4)(s+n+5)); cross-checked at two points against direct
quadrature of the book's (A.35). Compare |h - h_H|/t with both forms of the
right side of (A.36).

Confirms if: the two computations of h_H agree, a log-grid scan downward from
t = 2 finds |h - h_H|/t above the right side of (A.36) for both H = 200 and
H = 25, and the ratio keeps growing as t decreases (down to t = 1e-12).

Run: python3 -I eq_a_36.py

Ported from a 2026-11-06 check script.
"""
import math

E, PI = math.e, math.pi
H1 = 2.805820379671  # (A.37)

def h(t):
    return t * t * (2 - t)**3 * math.exp(t - 0.5) if 0 <= t <= 2 else 0.0

def Mh(s):
    tot, fact = 0j, 1.0
    for n in range(80):
        tot += 2.0**(s + n + 5) / (fact * (s + n + 2) * (s + n + 3) * (s + n + 4) * (s + n + 5))
        fact *= n + 1
    return 6 * E**-0.5 * tot

def gl(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x); ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws

X, W = gl(16)
NODES = {}
def mh_nodes(H, panels):
    key = (H, panels)
    if key not in NODES:
        hw = H / panels
        pts = []
        for p in range(panels):
            c = (p + 0.5) * hw
            for x, w in zip(X, W):
                tau = c + 0.5 * hw * x
                pts.append((tau, w * 0.5 * hw * Mh(1j * tau)))
        NODES[key] = pts
    return NODES[key]

def hH(t, H, panels=None):
    panels = panels or int(max(100, 3 * H))
    L = math.log(1 / t)
    return sum((m * complex(math.cos(tau * L), math.sin(tau * L))).real for tau, m in mh_nodes(H, panels)) / PI

def integ(f, a, b, panels):
    hw, tot = (b - a) / panels, 0.0
    for p in range(panels):
        c = a + (p + 0.5) * hw
        tot += sum(w * f(c + 0.5 * hw * x) for x, w in zip(X, W)) * 0.5 * hw
    return tot

def hH_direct(t, H):  # book's (A.35)
    sinc = lambda w: math.sin(w) / (PI * w) if w != 0 else 1 / PI
    f = lambda w: h(t * math.exp(-w / H)) * sinc(w)
    a = -H * math.log(2 / t)
    return integ(f, a, 0, int(-a) + 10) + integ(f, 0, 60 * H, int(60 * H) + 10)

def rhs(H):
    return H1 * (1 - math.exp(-1 / H) + 4 / PI * math.log(H) / H), H1 * (1 + 4 / PI * math.log(H)) / H

ok = True
FIRST = {}
for t, H in [(1e-8, 200.0), (1e-5, 25.0), (0.5, 25.0)]:
    a, b = hH(t, H), hH_direct(t, H)
    print("h_H(%g), H=%g: Mellin inversion %.15e, book's (A.35) %.15e" % (t, H, a, b))
    ok &= abs(a - b) < 1e-12

for H, ts in [(200.0, [1.0, 1e-3, 1e-6, 1e-7, 1e-8, 1e-10, 1e-12]), (25.0, [1.0, 1e-2, 1e-4, 1e-5, 1e-6, 1e-8, 1e-12])]:
    mid, last = rhs(H)
    print("H = %g: (A.36) right side %.5f (middle form %.5f)" % (H, last, mid))
    prev = 0
    for t in ts:
        ratio = abs(h(t) - hH(t, H)) / t
        flag = "FAILS" if ratio > last else ""
        print("   t = %-8g |h - h_H|/t = %.6g %s" % (t, ratio, flag))
        if t <= (1e-8 if H == 200 else 1e-6):
            ok &= ratio > prev
        prev = ratio
    # scan a log grid from t = 2 down to 1e-9 for the first failure
    first, N = None, 6000
    for i in range(N + 1):
        t = 2 * (5e-10) ** (i / N)
        if abs(h(t) - hH(t, H)) / t > last:
            first = t
            break
    print("   first failure on a log grid (6000 points in [1e-9, 2]), going down from t = 2: t = %.4g" % first)
    ok &= first is not None and first < 1e-3
    FIRST[H] = first

R12 = abs(h(1e-12) - hH(1e-12, 200.0)) / 1e-12
if ok:
    print("CONFIRMED: |h - h_H|/t first exceeds the right side of (A.36) near t = %.3g (H = 200) and t = %.3g (H = 25) and grows without bound as t -> 0+ (%.4g at t = 1e-12, H = 200), so (A.36) is false for small t." % (FIRST[200.0], FIRST[25.0], R12))
else:
    print("NOT CONFIRMED: (A.36) was not found to fail as claimed.")
