"""Check of [H, Eq (8.39)] and the display after it (bound for |u_o| on L_2).

Claim: the display after (8.39) asserts that the square
S(j, beta) = (sqrt((j-1)/2) cos b + (1 + sqrt((j+1)/2)) sin b)^2 is at least
P = j/2 + (7/2) sin^2 b - (1/2) cos^2 b + (j/2) sin^2 b; this fails as j -> 1
(small rho), although the next line |u_o| >= (l/2) sqrt((j/2)(1 + sin^2 b)) still
holds for b in [pi/8, pi/4]. Separately, "arg u_0 = arg u_{0,+} - beta" before
(8.39) should read arg u_o = beta.

Book inputs (mellintran.tex):
  - l.495-502 (8.27)-(8.28): j = sqrt(1 + rho^2), rho = 4 tau/l^2,
    Re u_{0,+} = (l/2) sqrt((j-1)/2), Im u_{0,+} = (l/2)(1 + sqrt((j+1)/2)) (l > 0).
  - l.866 "Since arg u_0 = arg u_{0,+} - beta"; l.867-873 (8.39)
    |u_o| = (l/2)(sqrt((j-1)/2) cos b + (1 + sqrt((j+1)/2)) sin b).
  - l.874-883 the display "the square ... is at least j/2 + 7/2 sin^2 b
    - 1/2 cos^2 b + j/2 sin^2 b"; l.884-888 beta >= pi/8, next line
    |u_o| >= (l/2) sqrt((j/2)(1 + sin^2 b)).
  - l.941-944 L_2 runs from u_{0,+} to x_1 = x_0 + y_0 tan b
    (u - u_{0,+} = y_0 (tan b - i) at u = x_1).

Confirms if: (a) S < P at j = 1 (and a range j < j*) for beta = pi/8, with tau > 0;
(b) S >= (j/2)(1 + sin^2 b) on a grid of beta in [pi/8, pi/4], j in [1, 1e8];
(c) in a concrete geometry, the foot u_o of the normal from 0 to L_2 has
arg u_o = beta, not arg u_{0,+} - beta, and |u_o| equals (8.39).

Run: python3 -I eq_8_39.py

Ported from a 2026-11-06 check script.
"""
import cmath
import math


def S(j, b):
    return (math.sqrt((j - 1) / 2) * math.cos(b)
            + (1 + math.sqrt((j + 1) / 2)) * math.sin(b)) ** 2


def P(j, b):
    s2, c2 = math.sin(b) ** 2, math.cos(b) ** 2
    return j / 2 + 3.5 * s2 - 0.5 * c2 + (j / 2) * s2


def T(j, b):  # what the next line needs
    return (j / 2) * (1 + math.sin(b) ** 2)


b8 = math.pi / 8
print("beta = pi/8: at j = 1, S = %.12f, printed bound P = %.12f" % (S(1, b8), P(1, b8)))
fails_j1 = S(1, b8) < P(1, b8)

# threshold j* where S - P changes sign (beta = pi/8)
lo, hi = 1.0, 2.0
assert S(lo, b8) - P(lo, b8) < 0 < S(hi, b8) - P(hi, b8)
for _ in range(200):
    mid = (lo + hi) / 2
    if S(mid, b8) - P(mid, b8) < 0:
        lo = mid
    else:
        hi = mid
jstar = lo
rhostar = math.sqrt(jstar ** 2 - 1)
print("printed display fails for 1 <= j < %.10f, i.e. rho < %.9f" % (jstar, rhostar))
# check a strictly admissible case tau > 0
rho = 0.05
j = math.sqrt(1 + rho ** 2)
fails_pos = S(j, b8) < P(j, b8)
print("rho = 0.05 (tau > 0): S = %.6f, P = %.6f, fails: %s" % (S(j, b8), P(j, b8), fails_pos))
for name, b in (("pi/6", math.pi / 6), ("pi/5", math.pi / 5), ("pi/4", math.pi / 4)):
    lo, hi = 1.0, 3.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if S(mid, b) - P(mid, b) < 0:
            lo = mid
        else:
            hi = mid
    print("  beta = %s: fails for rho < %.6f" % (name, math.sqrt(lo ** 2 - 1)))

# (b) the next line S >= (j/2)(1 + sin^2 b) on beta in [pi/8, pi/4], j in [1, 1e8]
worst = (1e9, None, None)
NB, NJ = 400, 2000
for ib in range(NB + 1):
    b = math.pi / 8 + (math.pi / 8) * ib / NB
    for ij in range(NJ + 1):
        j = 1 + (10 ** (-12 + 20 * ij / NJ) if ij > 0 else 0.0)
        d = S(j, b) - T(j, b)
        if d < worst[0]:
            worst = (d, b, j)
next_ok = worst[0] >= 0
print("min over grid of S - (j/2)(1+sin^2 b): %.10f at beta = %.6f, j = %.6g"
      % worst)
print("  (7/2) sin^2(pi/8) - 1/2 = %.10f" % (3.5 * math.sin(b8) ** 2 - 0.5))
tb = 0.37  # tan(0.37) > 1/sqrt7, the book's stated sufficient condition
print("beta = 0.37 (tan = %.5f > 1/sqrt7 = %.5f): S - (j/2)(1+sin^2) at j=1 = %.5f"
      % (math.tan(tb), 1 / math.sqrt(7), S(1, tb) - T(1, tb)))

# (c) geometry: l = 3, tau = 2, beta = pi/8
l, tau, b = 3.0, 2.0, b8
rho = 4 * tau / l ** 2
j = math.sqrt(1 + rho ** 2)
x0 = (l / 2) * math.sqrt((j - 1) / 2)
y0 = (l / 2) * (1 + math.sqrt((j + 1) / 2))
u0 = complex(x0, y0)
res = abs(u0 * u0 - 1j * l * u0 - 1j * tau)
x1 = x0 + y0 * math.tan(b)
d = complex(x1, 0) - u0           # direction of L_2
t = -(u0.real * d.real + u0.imag * d.imag) / abs(d) ** 2
uo = u0 + t * d                    # foot of normal from origin
arg_uo = cmath.phase(uo)
emp = (l / 2) * math.sqrt(S(j, b))
print("geometry l=3, tau=2: saddle residual %.1e, u_o on L_2 at t = %.4f (0..1)" % (res, t))
print("  arg u_o = %.6f, beta = %.6f, arg u_{0,+} - beta = %.6f" % (arg_uo, b, cmath.phase(u0) - b))
print("  |u_o| = %.10f, (8.39) = %.10f" % (abs(uo), emp))
geo_ok = (abs(arg_uo - b) < 1e-12 and abs(cmath.phase(u0) - b - arg_uo) > 0.1
          and abs(abs(uo) - emp) < 1e-12 and 0 <= t <= 1)

if fails_j1 and fails_pos and next_ok and geo_ok:
    print("CONFIRMED: the display after (8.39) fails for small rho (beta = pi/8: S = %.6f < "
          "%.6f at j = 1, failing for rho < %.6f) while |u_o| >= (l/2)sqrt((j/2)(1+sin^2 beta)) "
          "holds for beta in [pi/8, pi/4], and arg u_o = beta, not arg u_{0,+} - beta."
          % (S(1, b8), P(1, b8), rhostar))
else:
    print("NOT CONFIRMED: fails_j1=%s fails_pos=%s next_ok=%s geo_ok=%s"
          % (fails_j1, fails_pos, next_ok, geo_ok))
