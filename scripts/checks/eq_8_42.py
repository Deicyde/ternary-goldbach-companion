"""Check of [H, Eq (8.42)] (definition of c_{2,sigma,tau}, the rho <= 3/2 case).

Claim: for rho <= 3/2 the book bounds I_2 by the smaller of its beta = pi/6 and
beta = pi/5 bounds, but always adds the beta = pi/6 I_3 term e^{-tau/6}/(1/sqrt3)^sigma,
although one contour (one beta) must serve I_1, I_2, I_3. For sigma > 1.48748 the min
picks beta = pi/5, whose I_3 term by the book's own estimate is
e^{-0.11803 tau}/0.72654^sigma, larger when tau > 4.7262 sigma. So the printed c_2 does
not follow from the written argument there (proof gap); the sharper estimate y_0 >= l,
l^2 = 4 tau/rho >= 8 tau/3 makes the printed c_2 valid.

Book inputs (mellintran.tex):
  - l.894-910: beta = pi/8, or for rho <= 3/2 beta = pi/6 or pi/5 (arg u_{0,+} >= 1.28842);
    I_2 <= e^{-Re phi(u0+)} min(sqrt((pi/2)/cos(2pi/5)) |l sin(pi/5)|^{-sigma},
    sqrt(pi)|l/2|^{-sigma}).
  - l.915-938: (1/2)(1 - tan^2 b) y_0^2 >= (1 - tan^2 b) tau/4;
    I_3 <= |x_1|^{-sigma} sqrt(pi/2) e^{-(1-tan^2 b) tau/4} e^{-Re phi(u0+)},
    x_1 = x_0 + y_0 tan b >= tan b max(sqrt tau, l).
  - l.947-956 and (8.42) l.984-996: c_2 = (1/2)(1 + min(2^{sigma+1/2},
    sqrt(sec 2pi/5)/sin^sigma(pi/5)) + e^{-tau/6}/(1/sqrt3)^sigma).
  - l.498-502 (8.28): x_0 = (l/2) sqrt((j-1)/2), y_0 = (l/2)(1 + upsilon), j = sqrt(1+rho^2);
    l.781-783 (8.30): Re phi(x+iy) = (y^2-x^2)/2 - l y - tau arg(x+iy).
  - l.1400-1445 (proof of Cor 8.0.2): c_2 <= 3.15692, 5.02186 at |tau| >= 20 and
    kappa_{1,0} <= 4.903, kappa_{2,0} <= 7.96 with factors 2.53596, 2.5881, sqrt(3/8).
All terms are normalised by sqrt(pi/2) l^{-sigma} e^{-Re phi(u0+)}.

Confirms if: the beta = pi/5 I_3 term exceeds the printed one exactly when
tau > 4.7262 sigma; at tau = 20 every single admissible beta (beta <= arg u0+/2) with
the book's I_3 estimate gives c_2 above the printed 3.15692 (sigma = 2); and the repaired
I_3 term is <= the printed term for all tau, sigma >= 0, with the exact exponent gain
Re phi(x_1) - Re phi(u0+) at beta = pi/5 at least the repaired 0.6295 tau for rho <= 3/2.

Run: python3 -I eq_8_42.py

Ported from a 2026-11-06 check script.
"""
import math

PI = math.pi
s5, t5, t6 = math.sin(PI / 5), math.tan(PI / 5), math.tan(PI / 6)
A6 = lambda sg: 2 ** (sg + 0.5)                                 # I_2 term, beta = pi/6
A5 = lambda sg: math.sqrt(1 / math.cos(2 * PI / 5)) / s5 ** sg  # I_2 term, beta = pi/5
g = lambda b: (1 - math.tan(b) ** 2) / 4


def I3(b, sg, tau, gain=None):      # book's I_3 term for angle b, normalised by l^{-sigma}
    gg = g(b) if gain is None else gain
    return math.exp(-gg * tau) / math.tan(b) ** sg


def A(b, sg):                       # I_2 term for general b, using |u_o| >= l sin b
    return math.sqrt(1 / math.cos(2 * b)) / math.sin(b) ** sg


printed = lambda sg, tau: (1 + min(A6(sg), A5(sg)) + I3(PI / 6, sg, tau)) / 2
print("printed I_3 term: (1-tan^2(pi/6))/4 = %.10f (=1/6), 1/tan(pi/6) = %.8f (=sqrt3)"
      % (g(PI / 6), 1 / t6))
sstar = math.log(math.sqrt(1 / math.cos(2 * PI / 5)) / math.sqrt(2)) / math.log(2 * s5)
thr = math.log(t6 / t5) / (g(PI / 5) - g(PI / 6))
print("min(2^{s+1/2}, sqrt(sec 2pi/5)/sin^s(pi/5)) switches to beta=pi/5 at sigma* = %.8f" % sstar)
print("beta = pi/5 I_3 term e^{-%.8f tau}/%.8f^sigma exceeds the printed one iff tau > %.7f sigma"
      % (g(PI / 5), t5, thr))
# verify the threshold numerically on a grid
thr_ok = True
for sg10 in range(1, 31):
    sg = sg10 / 10
    for tau in (thr * sg * 0.99, thr * sg * 1.01):
        thr_ok &= ((I3(PI / 5, sg, tau) > I3(PI / 6, sg, tau)) == (tau > thr * sg))

tau = 20.0
vals = {}
for sg in (1, 2, 3):
    p = printed(sg, tau)
    c5 = (1 + A5(sg) + I3(PI / 5, sg, tau)) / 2
    c6 = (1 + A6(sg) + I3(PI / 6, sg, tau)) / 2
    vals[sg] = (p, min(c5, c6))
    print("tau = 20, sigma = %d: printed c_2 = %.7f; one contour: beta=pi/6 %.7f, beta=pi/5 %.7f"
          % (sg, p, c6, c5))

# best single admissible beta: beta <= (arg u0+)/2, arg u0+ >= (1/2)arccos(-1/upsilon(3/2))
ups = math.sqrt((1 + math.sqrt(1 + 2.25)) / 2)
argmin = 0.5 * math.acos(-1 / ups)
bmax = argmin / 2
print("rho <= 3/2: upsilon <= %.6f, arg u0+ >= %.7f, so beta <= %.7f" % (ups, argmin, bmax))
best = {}
for sg in (2, 3):
    bb = min(((1 + A(b, sg) + I3(b, sg, tau)) / 2, b)
             for b in [0.2 + (bmax - 0.2) * k / 20000 for k in range(20001)])
    best[sg] = bb
    print("  sigma = %d: best single beta (book's I_3 estimate) c_2 = %.6f at beta = %.5f (printed %.6f)"
          % (sg, bb[0], bb[1], vals[sg][0]))
gap = best[2][0] > vals[2][0] and vals[3][1] > vals[3][0] and thr_ok
k1 = (4e-7 + vals[2][1]) * 2.53596 * math.sqrt(3 / 8)
k2 = (4e-7 + vals[3][1]) * 2.5881 * math.sqrt(3 / 8)
print("propagated (pi/5 or pi/6 contour): kappa_{1,0} = %.5f (printed <= 4.903), kappa_{2,0} = %.5f (<= 7.96)"
      % (k1, k2))

# repair: (1/2)(1-tan^2 b) y_0^2 >= (1/2)(1-tan^2 b) l^2 >= (4/3)(1-tan^2 b) tau
grep = (4 / 3) * (1 - t5 ** 2)
rep_grid = all(I3(PI / 5, sg / 10, tt, grep) <= I3(PI / 6, sg / 10, tt)
               for sg in range(0, 61) for tt in range(0, 401))
rep_c2 = [(1 + A5(sg) + I3(PI / 5, sg, tau, grep)) / 2 for sg in (2, 3)]
print("repair: gain >= %.7f tau; repaired I_3 <= printed I_3 on grid sigma in [0,6], tau in [0,400]: %s"
      % (grep, rep_grid))
print("  repaired single-beta c_2 at tau = 20: %.6f (sigma=2), %.6f (sigma=3)" % tuple(rep_c2))


def rephi(x, y, l, tau):
    return (y * y - x * x) / 2 - l * y - tau * math.atan2(y, x)


# exact gain Re phi(x_1) - Re phi(u0+) at beta = pi/5 for rho in (0, 3/2]
mingain = 1e9
for k in range(1, 1501):
    rho = 1.5 * k / 1500
    for tau_ in (1.0, 20.0, 100.0):
        l = math.sqrt(4 * tau_ / rho)
        j = math.sqrt(1 + rho * rho)
        x0 = (l / 2) * math.sqrt((j - 1) / 2)
        y0 = (l / 2) * (1 + math.sqrt((j + 1) / 2))
        assert abs(complex(x0, y0) ** 2 - 1j * l * complex(x0, y0) - 1j * tau_) < 1e-8 * l * l
        x1 = x0 + y0 * t5
        gain = (rephi(x1, 0.0, l, tau_) - rephi(x0, y0, l, tau_)) / tau_
        mingain = min(mingain, gain)
print("exact (Re phi(x_1) - Re phi(u0+))/tau at beta = pi/5, rho <= 3/2: min %.5f "
      "(book's estimate %.5f, repair %.5f)" % (mingain, g(PI / 5), grep))
rep_ok = rep_grid and all(r <= vals[sg][0] for r, sg in zip(rep_c2, (2, 3))) and mingain >= grep

if gap and rep_ok:
    print("CONFIRMED: for sigma > %.5f and tau > %.4f sigma the printed c_2 in (8.42) uses the beta=pi/6 "
          "I_3 term with the beta=pi/5 I_2 term (one contour gives c_2 = %.5f, %.5f at tau=20, sigma=2, 3, "
          "against printed %.5f, %.5f), and y_0 >= l restores the printed c_2."
          % (sstar, thr, vals[2][1], vals[3][1], vals[2][0], vals[3][0]))
else:
    print("NOT CONFIRMED: gap=%s rep_ok=%s" % (gap, rep_ok))
