"""Check of [H, (A.32)] (|eta_+'|_2 <= 10.845789).

Claim: the proof of (A.32) uses (A.18), |f|_1 = |(r+i)Mh(ir)|_1 <= 27.8622803,
which is false (27.8622803 is the bracket that (A.18)'s text says to double).
With the factor 2 the argument gives only 21.69, and 14.28 with the true norm;
even the norm of f truncated to [-H,H] exceeds 27.8622803 for H >= 7.889, so
the argument fails for every H >= 25, where the bound is used. The printed
bound is still true there: a direct estimate gives |eta_+'|_2 <= 1.979 at H = 25.

Book inputs (normsapp.tex):
  - l.8-19   h, eta_o(t) = h(t) t e^{-t^2/2} = t^3(2-t)^3 e^{-(t-1)^2/2},
             eta_+(t) = h_H(t) t e^{-t^2/2}.
  - l.35-39  (A.5): Mh_H(i tau) = Mh(i tau) for |tau| < H, 0 for |tau| > H.
  - l.100-212 printed C_0..C_4 (C_4 = 2013.18185012); l.243-260 (A.18).
  - l.423-461 (A.31) convolution over [-H,H], Young, |g|_2^2 = 3 pi^{3/2}/4,
             and (A.32) = (2pi)^{-1/2} (3/2pi) 27.8622803 sqrt(3pi^{3/2}/4).
  - expform.tex Props 9.4.2, 9.5.1 assume H >= 25.

Method: (1) the factor K = (2pi)^{-1/2}(3/2pi)sqrt(3pi^{3/2}/4) times the
printed bracket, twice the bracket, and the true norm (Mh(it) from its exact
series, Gauss-Legendre); the truncated norm 2 int_0^H |t+i||Mh(it)| dt at
H = 7.88, 7.889, 25. (2) Direct estimate: with G(u) = h(e^u) and D = G_H - G,
eta_+' - eta_o' = D'(log t) e^{-t^2/2} + D(log t)(1-t^2) e^{-t^2/2}, and by
Plancherel |D'|_2 <= |G''|_2/H, |D|_2 <= |G''|_2/H^2, so
|eta_+'|_2 <= |eta_o'|_2 + (2e)^{-1/4}|G''|_2/H + max|1-t^2|sqrt(t)e^{-t^2/2} |G''|_2/H^2,
with |G''|_2^2 = int_0^2 (x^2 h'' + x h')^2 dx/x.

Confirms if: K*27.8622803 = 10.845789, K*(2 bracket) and K*(true norm) exceed
10.845789, the truncated norm at H = 25 exceeds 27.8622803, and the direct
bound is <= 10.845789 at H = 25 (it decreases in H).

Run: python3 -I eq_a_32.py

Ported from a 2026-11-06 check script.
"""
import math

E, PI = math.e, math.pi
C0 = 92 * E**-0.5 - 12 * E**1.5
C1 = 2 * math.sqrt(E)
C2, C3, C4 = 10.79195821037, 75.1295251672, 2013.18185012
F = lambda t: math.sqrt(t * t + 1) + math.log((math.sqrt(t * t + 1) - 1) / t)
r = C1 / C0
bracket = (C0 / 2 * (math.sqrt(r**4 + r**2) + math.asinh(r)) + C1 * (F(C2 / C1) - F(C1 / C0))
           + C2 * math.log(C3 * C1 / C2**2) + C3 * (C2 / C3 - C3 / C4) + C4 / 2 * C3**2 / C4**2)

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
def integ(f, a, b, panels):
    h, tot = (b - a) / panels, 0.0
    for p in range(panels):
        c = a + (p + 0.5) * h
        tot += sum(w * f(c + 0.5 * h * x) for x, w in zip(X, W)) * 0.5 * h
    return tot

K = (2 * PI) ** -0.5 * 3 / (2 * PI) * math.sqrt(3 * PI**1.5 / 4)
g = lambda t: math.hypot(t, 1) * abs(Mh(1j * t))
trunc = {H: 2 * integ(g, 0, H, int(8 * H) + 8) for H in (7.88, 7.889, 25.0)}
T = 2000.0
norm = 2 * (integ(g, 0, 100, 400) + integ(g, 100, T, 1900))
tail = 2 * C4 * (1 / (2 * T * T) + 1 / (3 * T**3))
print("K = %.9f" % K)
print("K * 27.8622803          = %.7f (book 10.845789)" % (K * 27.8622803))
print("K * 2*bracket (%.7f) = %.4f" % (2 * bracket, K * 2 * bracket))
print("true |f|_1 in [%.5f, %.5f]; K * |f|_1 = %.4f" % (norm, norm + tail, K * norm))
for H, v in trunc.items():
    print("truncated 2 int_0^H |t+i||Mh(it)| dt at H = %g: %.6f" % (H, v))

# direct estimate
def Hpolys():
    H0 = [0, 0, 8, -12, 6, -1]  # x^2 (2-x)^3
    out = [H0]
    for _ in range(2):
        p = out[-1]
        d = [i * p[i] for i in range(1, len(p))] + [0]
        out.append([a + b for a, b in zip(p, d)])
    return out
HP = Hpolys()
ev = lambda p, x: sum(c * x**i for i, c in enumerate(p))
hk = lambda k, x: ev(HP[k], x) * math.exp(x - 0.5)
G2sq = integ(lambda x: (x * x * hk(2, x) + x * hk(1, x))**2 / x, 0, 2, 200)
def eta_o_der(t):
    # eta_o = h(t) t e^{-t^2/2}
    return (hk(1, t) * t + hk(0, t) * (1 - t * t)) * math.exp(-t * t / 2)
eo = math.sqrt(integ(lambda t: eta_o_der(t)**2, 0, 2, 200))
m2 = max(abs(1 - t * t) * math.sqrt(t) * math.exp(-t * t / 2) for t in [i * 1e-4 for i in range(1, 100000)])
m2 += 1e-6  # grid safety margin
c1 = (2 * E) ** -0.25 * math.sqrt(G2sq)
c2 = m2 * math.sqrt(G2sq)
bound = lambda H: eo + c1 / H + c2 / H**2
print("|G''|_2^2 = %.6f, |eta_o'|_2 = %.7f, max|1-t^2|sqrt(t)e^{-t^2/2} <= %.7f" % (G2sq, eo, m2))
print("direct bound: |eta_+'|_2 <= %.6f + %.5f/H + %.5f/H^2 = %.6f (H=25), %.6f (H=200)"
      % (eo, c1, c2, bound(25), bound(200)))

ok = (abs(K * 27.8622803 - 10.845789) < 1e-6 and K * 2 * bracket > 10.845789 and K * norm > 10.845789
      and trunc[25.0] > 27.8622803 and trunc[7.889] > 27.8622803 > trunc[7.88] and bound(25) <= 10.845789)
if ok:
    print("CONFIRMED: the (A.32) route needs |f|_1 <= 27.8622803 but gives %.4f with the factor 2 and %.4f with the true norm (truncated norm %.4f > 27.8622803 at H = 25); the bound itself holds for H >= 25 since |eta_+'|_2 <= %.4f there."
          % (K * 2 * bracket, K * norm, trunc[25.0], bound(25)))
else:
    print("NOT CONFIRMED: the computed quantities do not match the claim.")
