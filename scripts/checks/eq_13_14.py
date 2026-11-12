"""Check of [H, Eq (13.14)] (eq:gropa, case 1 q <= r of the proof of Thm 13.2.1).

Claim (proof gap, harmless): (13.14) cites Prop 11.2.3's first case (11.18),
whose statement omits the w < 1/K term C_{phi,0,K} y = C_{phi,3}(K)|phi|_1 y that
its own proof adds, so (13.14) lacks it (harmless: (13.17) adds C_{phi,3}((log y)/2)).
Also g_{y,phi}(|delta| q/8) <= g_{y,phi}(r) needs monotonicity up to
|delta| q/8 <= y/(8Q) = y^(1/3)/6, while Lemma 11.2.4 is stated only for
r <= (y/K)^(1/3)/6; numerically g_{y,phi} is decreasing on [r_1, y^(1/3)/6].
What is computed here is the numerical content: the size of the omitted term,
the gap between the two ranges, and the monotonicity that makes it harmless.

Book inputs:
  - optcoor.tex:237-247    R_{x,t}, L_t, digamma; optcoor.tex:254 h(x)
  - optcoor.tex:384-417    Prop 11.2.3, (11.18)-(11.19): g_{x,phi}, R_{x,K,phi,t},
                           C_{phi,2,K} = -int_{1/K}^1 phi log w, C_{phi,0,K} = 1.04488 int_0^{1/K} phi
  - optcoor.tex:426-432    proof: int_0^{1/K} contributes <= 1.04488 x int_0^{1/K} phi for every q
  - optcoor.tex:497-498    Lemma 11.2.4: g_{x,phi} decreasing for 670 <= r <= (x/K)^(1/3)/6
  - intminarc.tex:240-271  proof of Thm 13.2.1: Q = (3/4) y^(2/3), |delta|/y <= 1/(qQ), case 1 (13.14);
                           intminarc.tex:290, 296: K = (log y)/2, r_1 = (3/8) y^(4/15)
  - conclusion.tex:20, 263 phi(t) = t^2 e^(-t^2/2), |phi|_1 = sqrt(pi/2); conclusion.tex:598 digamma
Confirms if at y = 10^25 the bound y/(8Q) on |delta| q/8 equals y^(1/3)/6 and exceeds
(y/K)^(1/3)/6, C_{phi,0,K} > 0, and for y = 10^25..10^300 g_{y,phi} strictly decreases
on a 4000-point geometric grid of [r_1, y^(1/3)/6].

Run: PYTHONPATH=<mpmath dir> python3 -s eq_13_14.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
eg = mp.exp(mp.euler)
phi = lambda w: w * w * mp.exp(-w * w / 2)
phi1 = mp.sqrt(mp.pi / 2)


def R(lz, lt):  # R_{z,t}, from log z and log t
    return mp.mpf("0.27125") * mp.log(1 + (mp.log(4) + lt) / (2 * (mp.log(9) + lz / 3 - mp.log("2.004") - lt))) + mp.mpf("0.41415")


def h(lx):
    return mp.mpf("0.276") * mp.exp(-lx / 6) * lx ** 1.5 + 1234 * mp.exp(-lx / 3) * lx


class Y:
    def __init__(self, ly):
        self.ly = ly
        self.K = ly / 2
        self.lK = mp.log(self.K)
        self.c = -mp.quad(lambda w: phi(w) * mp.log(w), [1 / self.K, 1]) / phi1 / self.lK
        self.C0 = mp.mpf("1.04488") * mp.quad(phi, [0, 1 / self.K])
        self.t3 = mp.mpf("3.36") * self.K ** (mp.mpf(1) / 6) * mp.exp(-ly / 6)

    def g(self, lr):  # g_{y,phi}(r), from log r
        l2r = mp.log(2) + lr
        Ry, RyK = R(self.ly, l2r), R(self.ly - self.lK, l2r)
        RK = Ry + (RyK - Ry) * self.c
        ll = mp.log(lr)
        dg = eg * ll + mp.mpf("2.50637") / ll
        L = dg * (mp.mpf(13) / 4 * l2r + mp.mpf("7.82")) + mp.mpf("13.66") * l2r + mp.mpf("37.55")
        return ((RK * l2r + mp.mpf("0.5")) * mp.sqrt(dg) + mp.mpf("2.5")) / mp.exp(l2r / 2) + L / mp.exp(lr) + self.t3

    lr1 = property(lambda s: mp.log(mp.mpf(3) / 8) + mp.mpf(4) / 15 * s.ly)
    ltop = property(lambda s: s.ly / 3 - mp.log(6))
    ltopK = property(lambda s: (s.ly - s.lK) / 3 - mp.log(6))


S = Y(25 * mp.log(10))
y = mp.mpf(10) ** 25
Q = mp.mpf(3) / 4 * y ** (mp.mpf(2) / 3)
print(f"y = 1e25: K = {mp.nstr(S.K, 5)}, r_1 = {mp.nstr(mp.exp(S.lr1), 4)}, (y/K)^(1/3)/6 = {mp.nstr(mp.exp(S.ltopK), 4)}, "
      f"y^(1/3)/6 = {mp.nstr(mp.exp(S.ltop), 4)}, y/(8Q) = {mp.nstr(y / (8 * Q), 4)}")
print(f"  omitted C_(phi,0,K) = {mp.nstr(S.C0, 4)} (times y); |phi|_1 g_(y,phi)(150000) = {mp.nstr(phi1 * S.g(mp.log(150000)), 4)} (times y)")
gap = mp.exp(S.ltopK) < mp.exp(S.ltop) and abs(y / (8 * Q) - mp.exp(S.ltop)) < 1e-6 * mp.exp(S.ltop) and S.C0 > 0
allok = True
for e in (25, 30, 40, 50, 75, 100, 150, 200, 250, 300):
    T = Y(e * mp.log(10))
    n, lo, hi = 4000, T.lr1, T.ltop
    prev, dec = None, True
    for i in range(n + 1):
        v = T.g(lo + (hi - lo) * i / n)
        if prev is not None and not v < prev:
            dec = False
        prev = v
    allok &= dec
    print(f"y = 1e{e}: g_(y,phi) decreasing on [r_1, y^(1/3)/6] = [{mp.nstr(mp.exp(lo), 3)}, {mp.nstr(mp.exp(hi), 3)}]: {dec}")
if gap and allok:
    print("CONFIRMED: at y = 1e25 the argument |delta|q/8 of g_(y,phi) in (13.14) can reach y/(8Q) = y^(1/3)/6 = 3.59e7, beyond Lemma 11.2.4's range (y/K)^(1/3)/6 = 1.17e7, and the omitted C_(phi,0,K) = 1.46e-5 is positive; harmless, since g_(y,phi) decreases on [r_1, y^(1/3)/6] for y = 1e25..1e300.")
else:
    print("NOT CONFIRMED: the range gap or the monotonicity that makes it harmless does not hold as claimed.")
