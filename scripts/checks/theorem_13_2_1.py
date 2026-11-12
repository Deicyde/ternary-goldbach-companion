"""Check of [H, Theorem 13.2.1] (thm:ostop, the minor-arc bound for Z_{r0}).

Claim: (1) scale mix-up: the l^infty input (13.14)-(13.17) is derived only off
M_{8,r}(y), y = x/kappa, while Prop 13.1.2 needs it off the arcs of the l^2
input H(r), which comes from (12.42) at scale x (as do Z_{r0}, J);
M_{8,r}(y) = M_{392,r}(x) is 49 times wider and no bound g(r) is shown on the
gap (Prop 11.2.3 at scale y gives only g(r/kappa), ~6.8 g(r0) at kappa = 49,
r0 = 150000, y = 10^25).  (a) The jump constant -2.14938 is stale: the book's
c+ = 2.0532, c- = 0.6394 give -1.46271, so M is understated.  (b) Squaring
sqrt(I0 S) >= sqrt J - sqrt E needs J >= E, which the hypotheses do not give
(eta_+(t) = max(0, 1 - tx/3) makes M + T < 0); harmless in Ch. 14.
The scale mix-up itself is a logical gap; what is checked are its numbers.

Book inputs:
  - intmajarc.tex:34-40   M_{delta0,r} (arcs a/q +- delta0 r/(2qx), q odd; +- delta0 r/(qx), q even);
  - intminarc.tex:169-237 statement: x >= 10^25 kappa, eta_+, r_1, (13.12) g_{y,phi},
                          K = log(x/kappa)/2, Z_{r0}, J, E, (13.13) M, c+-, C_{eta_+,j};
  - intminarc.tex:240-262 proof: y = x/kappa, "y is used instead of x to define M_{8,r}",
                          (13.14) |S_eta*| <= g_{y,phi}((|delta|/8) q) |phi|_1 y;
  - intminarc.tex:400-422 H(r), "c- = 0.6394 < log(1/sqrt(2*8)) + log 2 + 1.3325822",
                          and the jump bound with -2.14938;
  - intminarc.tex:440-470 I_0 S >= (sqrt J - sqrt E)^2;
  - optcoor.tex:237-247, 391-404 R_{x,t}, L_t, R_{x,K,phi,t}, C_{phi,2,K};
    optcoor.tex:586 digamma; conclusion.tex:258-263 kappa = 49, |phi|_1 = sqrt(pi/2),
    phi(t) = t^2 e^{-t^2/2}; conclusion.tex:778 r0 = 150000.
Method: (1) c- against log(1/4) + log 2 + c_E at scale x and its scale-y
analogue; the alpha = 4 r0/x just outside M_{8,r0}(x) (q = 1) has, at scale y,
delta = 8 r0/kappa, so Prop 11.2.3 gives g_{y,phi}(r0/kappa); ratio to
g_{y,phi}(r0).  (a) the constant.  (b) the example: S = 0, J <= int|S_2|^2 =
(log 2/3)^2 < E.  Confirms if all three numerical points come out as claimed.

Run: PYTHONPATH=<mpmath dir> python3 -s theorem_13_2_1.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
cE, cp, cm = mp.mpf('1.3325822'), mp.mpf('2.0532'), mp.mpf('0.6394')
kap, r0, y = mp.mpf(49), mp.mpf(150000), mp.mpf(10) ** 25
cx = mp.log(1 / mp.sqrt(16)) + mp.log(2) + cE
cy = cx - mp.log(kap) / 2
print(f"(1) c- bound at scale x: {mp.nstr(cx,6)} (c- = 0.6394 fits); at scale y: {mp.nstr(cy,6)}")
K = mp.log(y) / 2
phi = lambda t: t ** 2 * mp.exp(-t ** 2 / 2)
phi1 = mp.sqrt(mp.pi / 2)
C2 = -mp.quad(lambda t: phi(t) * mp.log(t), [1 / K, 1])
eg = mp.exp(mp.euler)
dg = lambda r: eg * mp.log(mp.log(r)) + mp.mpf('2.50637') / mp.log(mp.log(r))
Rx = lambda X, t: mp.mpf('0.27125') * mp.log(1 + mp.log(4 * t) / (2 * mp.log(9 * mp.cbrt(X) / (mp.mpf('2.004') * t)))) + mp.mpf('0.41415')
Lt = lambda t: dg(t / 2) * (mp.mpf(13) / 4 * mp.log(t) + mp.mpf('7.82')) + mp.mpf('13.66') * mp.log(t) + mp.mpf('37.55')
def g(r):
    t = 2 * r
    R = Rx(y, t) + (Rx(y / K, t) - Rx(y, t)) * (C2 / phi1) / mp.log(K)
    return ((R * mp.log(t) + mp.mpf('0.5')) * mp.sqrt(dg(r)) + mp.mpf('2.5')) / mp.sqrt(t) + Lt(t) / r \
        + mp.mpf('3.36') * K ** (mp.mpf(1) / 6) * y ** (-mp.mpf(1) / 6)
x = y * kap
alpha = 4 * r0 / x                      # edge of the q = 1 arc of M_{8,r0}(x)
delta_y = 2 * alpha * y                 # 2 alpha = 0/1 + delta/y
r_alpha = max(1, delta_y / 8) * 1
ratio = g(r_alpha) / g(r0)
print(f"    alpha = 4 r0/x: delta_y = {mp.nstr(delta_y,6)}, Prop 11.2.3 gives g_y({mp.nstr(r_alpha,6)}); g(r0/kappa)/g(r0) = {mp.nstr(ratio,5)}")
ca = -2 * (mp.log(mp.mpf(3) / 8) + cp - mp.mpf(8) / 15 * cm)
print(f"(a) -2(log 3/8 + c+ - (8/15)c-) = {mp.nstr(ca,7)} (printed -2.14938)")
# (b) eta_+(t) = max(0, 1 - t x/3): only n = 2 contributes, n <= sqrt x, so S = 0
X = mp.mpf(10) ** 25 * kap
etap = lambda t: max(0, 1 - t * X / 3)
S2sq = (mp.log(2) * etap(2 / X)) ** 2   # int |S_2|^2 = sum Lambda(n)^2 eta_+(n/x)^2
C0 = mp.mpf('0.7131') * mp.quad(lambda t: (1 - t * X / 3) ** 2 / mp.sqrt(t), [0, 3 / X])
C1 = mp.mpf(0)                          # eta_+ vanishes on [1, inf)
Cc2 = mp.mpf('0.51942')
E = ((C0 + Cc2) * mp.log(X) + (2 * C0 + C1)) * mp.sqrt(X)
print(f"(b) eta_+ = max(0,1-tx/3), x = 4.9e26: S = 0, J <= int|S_2|^2 = {mp.nstr(S2sq,5)} < E = {mp.nstr(E,5)}, so (sqrt J - sqrt E)^2 >= {mp.nstr((mp.sqrt(S2sq)-mp.sqrt(E))**2,5)} > 0 and M + T < 0")
ok = abs(cm - cx) < 1e-4 and cm < cx and cy < 0 and ratio > 6 and abs(ca - mp.mpf('-1.46271')) < 1e-5 and S2sq < E
if ok:
    print(f"CONFIRMED: c- = 0.6394 is the scale-x constant (scale y would give {mp.nstr(cy,5)}), Prop 11.2.3 at scale y bounds alpha just outside M_(8,r0)(x) only by g(r0/kappa) = {mp.nstr(ratio,4)} g(r0), the jump constant should be {mp.nstr(ca,6)}, and eta_+ = max(0,1-tx/3) gives J < E, so M + T < 0.")
else:
    print("NOT CONFIRMED: some computed value does not match the claim.")
