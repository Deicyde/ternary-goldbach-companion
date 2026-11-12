"""Check of [H, Eq (14.3)] (eq:sazar, the sup-norm line |eta_+|_inf <= 1.079955).

Claim: the sup-norm line of (14.3) is App. A's (A.38) at H = 200, whose proof
uses (A.36), |h_H(t) - h(t)|/t < |h'|_inf (1 + (4/pi) log H)/H for all t; this is
false for small t (in the w < 0 half of the integration by parts the weight is
e^(-w/H) = e^(|w|/H), up to 2/t, not e^(-|w|/H)).  The printed bound
|eta_+|_inf <= 1.079955 is nevertheless true (numerically |eta_+|_inf = 1.00000007, at t = 1).

Book inputs:
  - intromaj.tex:148-151, 158-170  h(t) = t^2 (2-t)^3 e^(t-1/2) on [0,2], 0 elsewhere;
                           h_H = h *_M F_H, whose Mellin transform on the imaginary axis is
                           Mh truncated to [-iH, iH]
  - normsapp.tex:19, 29-40 eta_+(t) = h_H(t) t e^(-t^2/2); Mh_H(i tau) = Mh(i tau) for |tau| < H
  - normsapp.tex:531-582   (A.35)-(A.36): the integration by parts and
                           |h_H(t) - h(t)|/t < |h'|_inf (1 + (4/pi) log H)/H
  - normsapp.tex:589-597   |h'|_inf <= 2.805820379671; (A.38) |eta_+|_inf < 1 + 2.06440727 (1 + (4/pi) log H)/H
  - conclusion.tex:63-71   (14.3) with H = 200: |eta_+|_inf <= 1.079955
Method: Mellin inversion h_H(t) = (1/pi) Re int_0^H Mh(i tau) t^(-i tau) d tau, with
Mh(s) = e^(-1/2) sum_k 2^(k+s+5) B(k+s+2, 4)/k! exact, by composite Gauss-Legendre
(two resolutions, which must agree).  Confirms if |h_H(t) - h(t)|/t exceeds the (A.36)
bound at t = 1e-8 and 1e-10, while max |eta_+| on a grid of (0, 8] is <= 1.079955.

Run: python3 -I eq_14_3.py

Ported from a 2026-11-06 check script.
"""
import cmath
import math

H = 200.0


def gl_nodes(n):
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
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


def Mh(s):
    tot, fact = 0j, 1.0
    for k in range(60):
        a = k + s + 2
        tot += cmath.exp((k + s + 5) * math.log(2)) * 6 / (a * (a + 1) * (a + 2) * (a + 3)) / fact
        fact *= k + 1
    return math.exp(-0.5) * tot


def table(m, n):  # m panels on [0, H], n nodes each
    xs, ws = gl_nodes(n)
    taus, wts = [], []
    hw = H / m / 2
    for j in range(m):
        c = (2 * j + 1) * hw
        for x, w in zip(xs, ws):
            taus.append(c + hw * x)
            wts.append(hw * w)
    return [(tau, w * Mh(1j * tau)) for tau, w in zip(taus, wts)]


TA = table(400, 20)
TB = table(600, 24)


def hH(t, T=TA):
    lt = math.log(t)
    return sum((wm * cmath.exp(-1j * tau * lt)).real for tau, wm in T) / math.pi


h = lambda t: t * t * (2 - t) ** 3 * math.exp(t - 0.5) if 0 <= t <= 2 else 0.0
print(f"|Mh(200 i)| = {abs(Mh(200j)):.4e}")
print(f"h_H(1) = {hH(1.0):.10f} vs h(1) = {h(1.0):.10f}")
bound = 2.805820379671 * (1 + 4 / math.pi * math.log(H)) / H
print(f"(A.36) bound |h'|_inf (1 + (4/pi) log H)/H = {bound:.5f}")
viol = True
for t in (1e-6, 1e-8, 1e-10):
    a, b = hH(t), hH(t, TB)
    r = abs(a - h(t)) / t
    print(f"t = {t:.0e}: h_H(t) = {a:.4e} (finer rule {b:.4e}), |h_H - h|/t = {r:.4f}")
    if t < 1e-7:
        viol &= r > bound and abs(a - b) < 1e-3 * abs(a)
# sup of eta_+ : log grid on [1e-12, 0.5], linear grid on [0.5, 8], refine near the max
grid = [10 ** (-12 + 11.7 * i / 1500) for i in range(1501)] + [0.5 + 7.5 * i / 1500 for i in range(1501)]
eta = lambda t: abs(hH(t) * t * math.exp(-t * t / 2))
vals = [(eta(t), t) for t in grid]
m, tm = max(vals)
for _ in range(3):
    loc = [tm + (k - 20) * 5e-4 for k in range(41)]
    m, tm = max((eta(t), t) for t in loc)
print(f"max |eta_+| on the grid = {m:.9f} at t = {tm:.4f}; printed bound 1.079955")
ok = viol and m <= 1.079955 and abs(hH(1.0) - h(1.0)) < 1e-4
if ok:
    print(f"CONFIRMED: (A.36) fails for small t (|h_H - h|/t at t = 1e-10 is {abs(hH(1e-10)) / 1e-10:.2f} > {bound:.4f}), so the proof of |eta_+|_inf <= 1.079955 is invalid, though the bound holds numerically (max |eta_+| = {m:.8f}).")
else:
    print("NOT CONFIRMED: (A.36) is not violated at small t, or |eta_+|_inf exceeds 1.079955.")
