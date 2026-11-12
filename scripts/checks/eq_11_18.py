"""Check of [H, Eq (11.18)] (eq:kroz, S_{eta_*}(alpha,x) <= g_{x,phi}(max(1,|delta|/8) q) |phi|_1 x).

Claim: (11.18) omits the w < 1/K part of the Mellin integral (11.9), which the
proof bounds by C_{phi,0,K} x but which no term of g_{x,phi} (11.19) absorbs;
the bound is false for phi with mass at tiny scales.  Counterexample:
x = 10^25, K = 2, 2alpha = 1/10^5 (a = 1, q = 10^5, delta = 0), phi a tent of
half-width 1% centred at w = 14/x: |S_{eta_*}(alpha,x)| ~ 1.043 |phi|_1 x
while g_{x,phi}(10^5) ~ 0.0494.  In Ch. 13 (phi = t^2 e^{-t^2/2},
K = (log y)/2) the missing term C_{phi,0,K}/|phi|_1 is ~1.2*10^-5 at y = 10^25.

Book inputs (optcoor.tex):
  - 194-200   (11.9) S_{eta_2 *_M phi}(alpha,x) = int_0^inf S_{eta_2}(alpha,wx) phi(w) dw/w;
  - 215-217   (11.10) eta_2(t) = 4 max(log 2 - |log 2t|, 0);
  - 237-247   (11.12)-(11.13) R_{x,t}, L_t;
  - 377-404   Prop 11.2.3: hypotheses, (11.18), (11.19) g_{x,phi}, R_{x,K,phi,t},
              (11.20) C_{phi,2,K}, (11.21) C_{phi,0,K} = 1.04488 int_0^{1/K} phi;
  - 586 / conclusion.tex:598  digamma(r) = e^gamma loglog r + 2.50637/loglog r.
  S_eta(alpha,x) = sum_n Lambda(n) e(alpha n) eta(n/x).
Method: with u = wx, S_{eta_*}(alpha,x) = int S_{eta_2}(alpha,u) tent(u) du/u,
computed by quadrature between the breakpoints of eta_2(n/u) (n <= 14);
C_{phi,2,K} = 0 since phi vanishes on [1/K,1], so R_{x,K,phi,t} = R_{x,t}.
Confirms if every hypothesis holds and |S_{eta_*}| (and Re S_{eta_*}) exceeds
g_{x,phi}(10^5) |phi|_1 x.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_11_18.py

Ported from a 2026-11-06 check script.
"""
import math
import mpmath as mp

mp.mp.dps = 30
x, K, q, a, delta = mp.mpf(10) ** 25, mp.mpf(2), 10 ** 5, 1, 0
alpha = mp.mpf(a) / q / 2
Q = mp.mpf(3) / 4 * x ** (mp.mpf(2) / 3)
hyp = (x >= K * mp.mpf('2.16e20'), q <= Q, math.gcd(a, q) == 1, abs(delta / x) <= 1 / (q * Q),
       q <= mp.cbrt(x / K) / 6)
print(f"hypotheses of Prop 11.2.3 hold: {all(hyp)} (q <= (x/K)^(1/3)/6 = {mp.nstr(mp.cbrt(x/K)/6,4)})")
Lam = {2: mp.log(2), 3: mp.log(3), 4: mp.log(2), 5: mp.log(5), 7: mp.log(7), 8: mp.log(2),
       9: mp.log(3), 11: mp.log(11), 13: mp.log(13)}
eta2 = lambda t: 4 * max(mp.log(2) - abs(mp.log(2 * t)), 0) if t > 0 else mp.mpf(0)
S2 = lambda u: sum(L * mp.expjpi(2 * alpha * n) * eta2(n / u) for n, L in Lam.items())
u0, hw = mp.mpf(14), mp.mpf('0.14')            # tent centre wx = 14, half-width 1%
tent = lambda u: max(0, 1 - abs(u - u0) / hw)
phi1x = hw                                      # |phi|_1 x = (0.01*14/x) x
brk = sorted(set([u0 - hw, u0, u0 + hw] + [mp.mpf(n) / c for n in Lam for c in (mp.mpf(1)/4, mp.mpf(1)/2, 1)
                                           if u0 - hw < mp.mpf(n) / c < u0 + hw]))
S = mp.quad(lambda u: S2(u) * tent(u) / u, brk)
ratio = S / phi1x
print(f"S_eta*(alpha,x)/(|phi|_1 x) = {mp.nstr(ratio.real,6)} + {mp.nstr(ratio.imag,3)}i, |.| = {mp.nstr(abs(ratio),6)}")
eg = mp.exp(mp.euler)
dg = lambda r: eg * mp.log(mp.log(r)) + mp.mpf('2.50637') / mp.log(mp.log(r))
Rx = lambda X, t: mp.mpf('0.27125') * mp.log(1 + mp.log(4 * t) / (2 * mp.log(9 * mp.cbrt(X) / (mp.mpf('2.004') * t)))) + mp.mpf('0.41415')
Lt = lambda t: dg(t / 2) * (mp.mpf(13) / 4 * mp.log(t) + mp.mpf('7.82')) + mp.mpf('13.66') * mp.log(t) + mp.mpf('37.55')
def g(r):
    r = mp.mpf(r)
    return ((Rx(x, 2 * r) * mp.log(2 * r) + mp.mpf('0.5')) * mp.sqrt(dg(r)) + mp.mpf('2.5')) / mp.sqrt(2 * r) \
        + Lt(2 * r) / r + mp.mpf('3.36') * K ** (mp.mpf(1) / 6) * x ** (-mp.mpf(1) / 6)
gv = g(max(1, abs(delta) / 8) * q)
print(f"g_x,phi(10^5) = {mp.nstr(gv,6)}; violation factor {mp.nstr(abs(ratio)/gv,4)}")
# Ch. 13 size of the missing term
for y in (mp.mpf(10) ** 25, mp.mpf(10) ** 27):
    Ky = mp.log(y) / 2
    c3 = mp.mpf('1.04488') * mp.quad(lambda t: t ** 2 * mp.exp(-t ** 2 / 2), [0, 1 / Ky]) / mp.sqrt(mp.pi / 2)
    print(f"phi = t^2 e^(-t^2/2), y = {mp.nstr(y,2)}: C_phi,0,K/|phi|_1 = {mp.nstr(c3,4)}")
if all(hyp) and ratio.real > gv and abs(ratio) > gv:
    print(f"CONFIRMED: at x = 10^25, K = 2, 2alpha = 1/10^5 with phi a 1% tent at w = 14/x, S_eta*(alpha,x) = {mp.nstr(ratio.real,5)} |phi|_1 x exceeds the (11.18) bound {mp.nstr(gv,4)} |phi|_1 x.")
else:
    print("NOT CONFIRMED: the counterexample does not violate (11.18).")
