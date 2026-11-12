"""Check of [H, (A.41)] (|eta_+(t)/t|_oo <= 1.08754396 + 1.70181609 (1 + (4/pi) log H)/H).

Claim: (A.41) is proved through (A.39) and the l_oo form of (A.36), which is false (|(h - h_H)/t|_oo = oo), so the printed proof fails; the bound holds for H >= 25 via |eta_+/t|_oo <= |eta_o/t|_oo + |h - h_H|_oo with |h - h_H|_oo <= 64e^{3/2}/(pi H^3).

Book inputs (normsapp.tex):
  - l.8-19   h(t) = t^2 (2-t)^3 e^{t-1/2} on [0,2], eta_o(t) = h(t) t e^{-t^2/2},
             eta_+(t) = h_H(t) t e^{-t^2/2}.
  - l.21-39  h_H = h *_M F_H and (A.5): Mh_H(i tau) = Mh(i tau) for |tau| < H,
             0 for |tau| > H.
  - l.577-582 (A.36); l.589-591 (A.37) |h'|_oo <= 2.805820379671.
  - l.603-631 (A.39), |eta_o(t)/t|_oo <= 1.08754396, |eta_diamond|_oo = e^{-1/2},
             (A.41); eta_diamond(t) = t e^{-t^2/2}.
  - Uses: expform.tex Prop 9.5.1 assumes H >= 25; Sec. 14 takes H = 200.

Method: (1) h_H(t) = (1/pi) Re int_0^H Mh(i tau) t^{-i tau} d tau, with Mh from
its exact series Mh(s) = 6e^{-1/2} sum_n 2^{s+n+5}/(n!(s+n+2)(s+n+3)(s+n+4)(s+n+5)),
shows |(h - h_H)/t| exceeds (A.36) and grows as t -> 0+. (2) Each series term
has |i tau + k| >= tau, so |Mh(i tau)| <= 192 e^{3/2}/tau^4 (checked on a grid)
and |h - h_H|_oo <= (1/pi) int_H^oo |Mh| <= 64 e^{3/2}/(pi H^3) (checked against
a grid sup). (3) The corrected bound replaces |(h-h_H)/t|_oo |w t|_oo by
|h - h_H|_oo |w|_oo; its excess over the main term decreases faster in H than
the book's, so checking H = 25 covers all H >= 25.

Confirms if: (1) holds at H = 25 and 200, the bounds in (2) hold, and the
corrected bound is below the book's right side at H = 25 and H = 200.

Run: python3 -I eq_a_41.py

Ported from a 2026-11-06 check script.
"""

import math

E, PI = math.e, math.pi
H1 = 2.805820379671  # (A.37), |h'|_oo

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
def hH(t, H):
    """h_H(t) = (1/pi) Re int_0^H Mh(i tau) t^{-i tau} d tau, by (A.5)."""
    panels = int(max(100, 3 * H))
    if H not in NODES:
        hw, pts = H / panels, []
        for p in range(panels):
            c = (p + 0.5) * hw
            for x, w in zip(X, W):
                tau = c + 0.5 * hw * x
                pts.append((tau, w * 0.5 * hw * Mh(1j * tau)))
        NODES[H] = pts
    L = math.log(1 / t)
    return sum((m * complex(math.cos(tau * L), math.sin(tau * L))).real for tau, m in NODES[H]) / PI

def gridmax(f, a, b, n=200000):
    best = (-1.0, a)
    for i in range(n + 1):
        t = a + (b - a) * i / n
        v = abs(f(t))
        if v > best[0]:
            best = (v, t)
    return best

ok = True
# (1) the norm |(h - h_H)/t|_oo that the proof bounds by (A.36) is not bounded by it
for H in (25.0, 200.0):
    rhs = H1 * (1 + 4 / PI * math.log(H)) / H
    r = [abs(h(t) - hH(t, H)) / t for t in (1e-8, 1e-10, 1e-12)]
    print("H = %g: (A.36) right side %.5f; |h - h_H|/t at t = 1e-8, 1e-10, 1e-12: %.4g, %.4g, %.4g"
          % (H, rhs, r[0], r[1], r[2]))
    ok &= r[0] > rhs and r[2] > r[1] > r[0]

# (2) |Mh(i tau)| <= 192 e^{3/2}/tau^4 (each term of the series has |i tau + k| >= tau),
#     so |h - h_H|_oo <= (1/pi) int_H^oo |Mh| <= 64 e^{3/2}/(pi H^3)
worst = max(abs(Mh(1j * tau)) * tau**4 / (192 * E**1.5) for tau in [0.5 * k for k in range(1, 2001)])
print("max over tau in (0,1000] of |Mh(i tau)| tau^4/(192 e^{3/2}) = %.6f" % worst)
ok &= worst <= 1
B = lambda H: 64 * E**1.5 / (PI * H**3)
for H in (25.0, 200.0):
    sup = max(abs(h(t) - hH(t, H)) for t in [50 * (2e-8) ** (i / 6000) for i in range(6001)])
    print("H = %g: sup |h - h_H| on a log grid of [1e-6, 50] = %.5g <= 64e^{3/2}/(pi H^3) = %.5g" % (H, sup, B(H)))
    ok &= sup <= B(H)

# (3) corrected bound: |eta_+/t|_oo <= |eta_o/t|_oo + |h - h_H|_oo |e^{-t^2/2}|_oo
eot = gridmax(lambda t: h(t) * math.exp(-t * t / 2), 0, 2)[0]
print("|eta_o(t)/t|_oo = %.9f (book <= 1.08754396); book constant 2.805820379671 e^{-1/2} = %.9f (book 1.70181609)" % (eot, H1 * E**-0.5))
book = lambda H: 1.08754396 + 1.70181609 * (1 + 4 / PI * math.log(H)) / H
corr = lambda H: eot + 1e-8 + B(H) * 1.0
for H in (25.0, 200.0):
    print("H = %g: corrected bound %.7f, book's (A.41) %.7f" % (H, corr(H), book(H)))
ok &= eot <= 1.08754396 and corr(25.0) < book(25.0) and corr(200.0) < book(200.0)
if ok:
    print("CONFIRMED: |(h - h_H)/t|_oo is not bounded by (A.36) (it grows without bound as t -> 0+), so the printed proof of (A.41) fails, but the corrected route gives |eta_+/t|_oo <= %.6f < %.6f at H = 25 and the bound holds for all H >= 25." % (corr(25.0), book(25.0)))
else:
    print("NOT CONFIRMED: the computation does not match the claim.")
