"""Check of [H, Lemma B.2.3] (|hat(eta_(y)'')|_oo < 31.521 log y for y >= 4).

Claim: two steps of the proof fail: (i) the bound |16 log 2 k - hat h| <=
48 log 2 + 25 = 58.27 is followed by max(31.521 log y, 58.27) = 31.521 log y,
which is false for 4 <= y < 6.35; (ii) the decay bound covers |t| >= 2252.51
but the numerics stop at t = 2252.21. The lemma is still true:
|eta_(4)''|_1 = 48 log 2 gives |hat(eta_(y)'')| <= 48 log 2 + 31.521 (log y -
log 4) < 31.521 log y.

Book inputs:
  - intromin.tex l.124-125: eta_2(t) = 4 max(log 2 - |log 2t|, 0).
  - normfour.tex l.60-66 Lemma B.2.1 (|hat(eta_2'')|_oo <= 31.521); l.69-79
    eta_2'' = 4(4 delta_{1/4} - 4 delta_{1/2} + delta_1) + f; l.167-173 the
    lemma, eta_(y)(t) = log(yt) eta_2(t); l.176-191 eta_(y)'' and h(x);
    l.193-203 (B.13), the threshold 2252.51 and "0 <= t <= 2252.21";
    l.205 I = [0.3, 2252.21] minus [3.25, 3.65]; l.215-220 the max step.

Method: arithmetic for (i) and (ii); for the repair, |eta_(4)''|_1 is the total
mass of the measure eta_2'' log 4 + 4 log x (4 delta_{1/4} - 4 delta_{1/2} +
delta_1) + h (point masses plus Gauss-Legendre for the density), and
eta_(y) = eta_(4) + log(y/4) eta_2 with Lemma B.2.1.

Confirms if: 48 log 2 + 25 > 31.521 log 4, 2252.21 < the computed threshold,
and |eta_(4)''|_1 = 48 log 2 < 31.521 log 4.

Run: python3 -I lemma_b_2_3.py

Ported from a 2026-11-06 check script.
"""
import math

L2 = math.log(2)
lhs = 48 * L2 + 25
print("48 log 2 + 25 = %.4f; 31.521 log 4 = %.4f; max(...) = 31.521 log y only for y >= e^{%.4f/31.521} = %.4f"
      % (lhs, 31.521 * math.log(4), lhs, math.exp(lhs / 31.521)))
thr = (80 + 160 * (1 + L2) / math.log(4)) / (math.pi * 0.03892)
print("decay threshold (80 + 160(1 + log 2)/log 4)/(pi 0.03892) = %.4f; numerics cover t <= 2252.21" % thr)

# eta_(4)'' as a measure on [1/4, 1]
def dens(x):  # absolutely continuous part: log 4 * f(x) + h(x)
    if 0.25 <= x < 0.5:
        return math.log(4) * (-4 / x**2) + 4 / x**2 * (2 - 2 * math.log(2 * x))
    if 0.5 <= x < 1:
        return math.log(4) * (4 / x**2) + 4 / x**2 * (-2 + 2 * math.log(x))
    return 0.0
atoms = {x: 4 * m * (math.log(4) + math.log(x)) for x, m in [(0.25, 4), (0.5, -4), (1.0, 1)]}

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
X, W = gl(30)
def integ(f, a, b, panels=50):
    hw, tot = (b - a) / panels, 0.0
    for p in range(panels):
        c = a + (p + 0.5) * hw
        tot += sum(w * f(c + 0.5 * hw * x) for x, w in zip(X, W)) * 0.5 * hw
    return tot
# the density is 8(1 - log 4x)/x^2 > 0 on [1/4,1/2) and 8(log 2x - 1)/x^2 < 0 on [1/2,1)
cont = integ(lambda x: abs(dens(x)), 0.25, 0.5) + integ(lambda x: abs(dens(x)), 0.5, 1.0)
mass = cont + sum(abs(v) for v in atoms.values())
print("point masses of eta_(4)'':", {k: round(v / L2, 10) for k, v in atoms.items()}, "(in units of log 2)")
print("|density|_1 = %.10f = %.10f log 2; total |eta_(4)''|_1 = %.10f = %.10f log 2" % (cont, cont / L2, mass, mass / L2))
print("repair: 48 log 2 = %.4f < 31.521 log 4 = %.4f (margin %.4f)" % (48 * L2, 31.521 * math.log(4), 31.521 * math.log(4) - 48 * L2))

ok = lhs > 31.521 * math.log(4) and thr > 2252.21 and abs(mass - 48 * L2) < 1e-9 and mass < 31.521 * math.log(4)
if ok:
    print("CONFIRMED: 48 log 2 + 25 = %.3f > 31.521 log 4 = %.3f (the max step fails for 4 <= y < %.3f) and the decay range starts at %.3f > 2252.21, while |eta_(4)''|_1 = 48 log 2 < 31.521 log 4 repairs the lemma."
          % (lhs, 31.521 * math.log(4), math.exp(lhs / 31.521), thr))
else:
    print("NOT CONFIRMED: the computed values do not match the claim.")
