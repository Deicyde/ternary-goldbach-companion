"""Check of [H, Eq (9.68)] (Gaussian part in the proof of Lemma 9.4.1).

Claim: the chain (9.68) can fail. Its second inequality multiplies the
correction term (pi/2 + 1/(2*0.1065*y))/y by log(qT0/2pi)/log(T0/(pi|delta|)),
which is < 1 when q|delta| < 2, whereas the book's own integral bound (with
kappa = H/(pi|delta|), kappa_1 = pi/2, plus the separate log(q|delta|/2) term)
needs factor 1. The first inequality replaces (pi/2)/(pi|delta|u + H) by
(pi/2)/u, which is not valid pointwise when pi|delta| < 1. The concluding
constant 16.147 still holds.

Book inputs (expform.tex):
  - 1473-1494  Lemma 9.4.1: H >= 25, q >= 1, T0 >= H + max(10 pi|delta|, 50).
  - 1528-1533  f = |Mh(ir)|_1/(2pi) g(tau-H), |Mh(ir)|_1 <= 16.193918;
               kappa_{1,0} = 4.903.
  - 1580-1586  integral bound int_y^oo (t log(t+k) + k1) e^{-ct^2} dt
               <= (1 + (k1 + 1/(2cy))/(y log(y+k))) log(y+k) e^{-cy^2}/(2c).
  - 1589-1602  (9.68), its three lines, and "at most 16.147 |delta| log(qT0/2pi)".
  - normsapp.tex:228-241  |Mh(it)|_1 <= 16.1939176, "far from tight";
               h(x) = x^2 (2-x)^3 e^{x-1/2} on [0,2].
All lines are in units of e^{-0.1065((T0-H)/(pi delta))^2}.
L1 is line 1 with the actual |Mh(ir)|_1; L1b is line 1 with |Mh(ir)|_1
replaced by its bound 16.193918 (prefactor 12.6368 as in line 2).
The rigorous upper bound |Mh(ir)|_1 <= 2 pi (|phi|_2 |phi'|_2)^{1/2},
phi(u) = h(e^u), follows from Cauchy-Schwarz and Plancherel.

Confirms if: L2 > L3 at admissible points with q|delta| < 2 (the printed
second inequality fails), never with q|delta| >= 2 on the grid; and the
final 16.147 bound dominates L1, L2 and the corrected line 3 on the grid.
Also reported: whether L1 <= L2 (first inequality) holds as printed, and
whether L1b > L2 (the substitution in isolation loses).

Run: python3 -I eq_9_68.py

Ported from a 2026-11-06 check script.
"""
import math

pi = math.pi
c = 0.1065
K = 12.6368


def simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i & 1 else 2) * f(a + i * h)
    return s * h / 3


# rigorous upper bound for |Mh(ir)|_1
def h(x):
    return x * x * (2 - x) ** 3 * math.exp(x - 0.5)


def hp(x):
    return (2 * x * (2 - x) ** 3 - 3 * x * x * (2 - x) ** 2 + x * x * (2 - x) ** 3) * math.exp(x - 0.5)


phi2 = simpson(lambda x: h(x) ** 2 / x if x > 0 else 0.0, 0.0, 2.0, 20000)
dphi2 = simpson(lambda x: x * hp(x) ** 2, 0.0, 2.0, 20000)
norm_ub = 2 * pi * (phi2 * dphi2) ** 0.25
print("|phi|_2^2 = %.6f, |phi'|_2^2 = %.6f, |Mh(ir)|_1 <= %.4f (book bound 16.193918)" % (phi2, dphi2, norm_ub))
Kact = 4.903 * norm_ub / (2 * pi)
print("4.903*16.193918/2pi = %.6f <= 12.6368; with the rigorous norm bound: %.4f" % (4.903 * 16.193918 / (2 * pi), Kact))


def chain(q, H, T0, d, n=20000):
    P = pi * abs(d)
    y = (T0 - H) / P
    kap = H / P
    ub = math.sqrt(y * y + 70 / c)
    E = lambda u: math.exp(-c * (u - y) * (u + y))
    g1 = lambda u: (math.log(q * (P * u + H) / (2 * pi)) / (2 * pi) + 1 / (4 * (P * u + H))) * (u / 2) * P * E(u)
    g2 = lambda u: (math.log(u + kap) + math.log(q * abs(d) / 2) + (pi / 2) / u) * u * E(u)
    I1 = simpson(g1, y, ub, n)
    L2 = K * abs(d) / 4 * simpson(g2, y, ub, n)
    lg = math.log(q * T0 / (2 * pi))
    corr = (pi / 2 + P / (2 * c * (T0 - H))) / y
    L3 = K * abs(d) / (8 * c) * (1 + corr / math.log(T0 / P)) * lg
    L3c = K * abs(d) / (8 * c) * (lg + corr)
    B = 16.147 * abs(d) * lg
    return Kact * I1, K * I1, L2, L3, L3c, B


print("\nq H T0 delta: L1(actual norm, upper) L1b(norm bound) L2 L3 L3corrected 16.147-bound")
examples = [(1, 25, 75, 0.1), (1, 25, 75, 0.3), (1, 25, 75, 1.0), (1, 200, 250, 0.1), (3, 25, 75, 1.0)]
for (q, H, T0, d) in examples:
    r = chain(q, H, T0, d)
    print(q, H, T0, d, " ".join("%.6f" % v for v in r))

# grid scan over admissible parameters
n_adm = n_fail2 = n_fail2_big = n_fail1 = n_sub = n_finfail = 0
maxr = 0.0
for q in (1, 2, 3, 5, 10):
    for H in (25, 50, 200):
        for dT in (50, 60, 80, 120):
            for k in range(25):
                d = 0.01 * (1.25 ** k)
                T0 = H + dT
                if T0 < H + max(10 * pi * d, 50):
                    continue
                n_adm += 1
                L1, L1b, L2, L3, L3c, B = chain(q, H, T0, d, 4000)
                if L2 > L3:
                    n_fail2 += 1
                    maxr = max(maxr, L2 / L3)
                    if q * d >= 2:
                        n_fail2_big += 1
                if L1 > L2:
                    n_fail1 += 1
                if L1b > L2:
                    n_sub += 1
                if max(L1, L2, L3c) > B:
                    n_finfail += 1
print("\nadmissible grid points: %d" % n_adm)
print("second <= fails (L2 > L3): %d (max ratio %.5f); of these with q|delta| >= 2: %d" % (n_fail2, maxr, n_fail2_big))
print("first <= fails as printed (L1 actual > L2): %d" % n_fail1)
print("substitution alone loses (L1 with norm bound > L2): %d" % n_sub)
print("16.147 bound exceeded by L1, L2 or corrected L3: %d" % n_finfail)
print("corrected-L3 constant at y=10, T0=75, q=1: %.4f" % (K / (8 * c) * (1 + (pi / 2 + 1 / (20 * c)) / (10 * math.log(75 / (2 * pi))))))

if n_fail2 > 0 and n_fail2_big == 0 and n_finfail == 0:
    first = ("the first inequality holds as printed (true norm <= %.3f) though its substitution alone loses at %d points"
             % (norm_ub, n_sub)) if n_fail1 == 0 else "the first inequality also fails at %d points" % n_fail1
    print("CONFIRMED: the second inequality of (9.68) fails at %d admissible points, all with q|delta| < 2 "
          "(max ratio %.4f); %s; the final 16.147 bound holds." % (n_fail2, maxr, first))
else:
    print("NOT CONFIRMED: the second inequality of (9.68) does not fail as described, or 16.147 is exceeded.")
