"""Check of [H, Cor 9.3.3] ((9.61), eta_* = eta_2 *_M eta).

Claim: (1) Cor 9.3.3 is stated for all x > 0, but its proof applies Prop 9.3.2
(which assumes x >= 1) at scale wx, w in [1/4, 1], so it covers only x >= 4;
for 0 < x < 4 the statement still holds by the trivial bound
|LHS| <= sum Lambda(n) eta_*(n/x) + |eta_*|_1 x <= 0.0785 (51.17 sqrt x + 6 + 18/sqrt x).
(2) Through (9.57) the w-independent first-line term 6.11 e^{-0.1598 T0} is
not justified for q = 1, T0 <~ 52.4: the eta_2-average of the proof's own
bounds at q = 1, delta = 0, T0 = 50 exceeds (9.61) for x >= 4e4; the 1.578
slip does not reach (9.61) (averaged Gaussian coefficient <= 0.0102 for
|delta| in [2.5, 8], T0 = 10 pi |delta|).

Book inputs (expform.tex):
  - l.1278 Prop 9.3.2 "x >= 1"; l.1363 Cor 9.3.3 "x in R^+"; l.1399 "[-1/4,1]".
  - l.1379-1389 (9.61) err_{eta_*}; l.1414-1419 (9.62) average over w in [1/4,1].
  - l.1421-1434 eta_2 formula, moments 1, 1.37259, 1.92182, 2.74517, and 0.006446.
  - l.1081-1103 (9.48)-(9.49): f and weight (1/2pi)log(qT/2pi) + 1/(4T).
  - l.1294-1323 (9.57) and its proof: Lemma 9.1.4 term, Lemma 9.1.1 term
    (log q + 6.01)(|eta'|_2 + 2 pi |delta| |eta|_2); l.264-266 R = 0 for q = 1.
  - l.616-637 (9.31) Lemma 9.1.4; l.1260-1273 (9.56) norms.

Method: Gauss-Legendre on [1/4,1/2] and [1/2,1] for the eta_2 averages;
eta_*(t) by the same quadrature; the exponential majorant in closed form.

Confirms if: (1) the eta_2 moments match, the trivial bound ratio on (0,4]
is < 1 (so the statement holds there although the proof needs x >= 4);
(2) the averaged proof bound at q = 1, delta = 0, T0 = 50 exceeds (9.61) for
every x beyond some x0 <= 4e4, and the averaged exact Gaussian coefficient
is <= 0.0102 on the |delta| scan.

Run: python3 -I corollary_9_3_3.py

Ported from a 2026-11-06 check script.
"""
import math

PI = math.pi
LN = math.log
c, cp, k21, k20 = 0.1598, 0.1065, 5.13, 7.96


def legendre(n):
    out = []
    for i in range(1, n + 1):
        x = math.cos(PI * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        out.append((x, 2 / ((1 - x * x) * dp * dp)))
    return out


GL20 = legendre(20)


def gl(f, a, b, m, nodes=GL20):
    h = (b - a) / m
    s = 0.0
    for j in range(m):
        mid = a + (j + 0.5) * h
        s += sum(w * f(mid + 0.5 * h * x) for x, w in nodes)
    return s * h / 2


def eta2(w):
    if 0.25 <= w <= 0.5:
        return 4 * LN(4 * w)
    if 0.5 < w <= 1.0:
        return 4 * LN(1 / w)
    return 0.0


def avg(g, m=4):
    return gl(lambda w: g(w) * eta2(w), 0.25, 0.5, m) + gl(lambda w: g(w) * eta2(w), 0.5, 1.0, m)


def eta(t):
    return t * t * math.exp(-t * t / 2) if t > 0 else 0.0


def eta_star(t):
    return avg(lambda w: eta(t / w) / w, 3)


def eE1(z):
    tiny = 1e-300
    b = z + 1.0
    C, D = 1.0 / tiny, 1.0 / b
    h = D
    for i in range(1, 100000):
        an = -float(i * i)
        b += 2.0
        D = an * D + b
        D = tiny if D == 0 else D
        C = b + an / C
        C = tiny if C == 0 else C
        D = 1.0 / D
        de = C * D
        h *= de
        if abs(de - 1.0) < 1e-16:
            break
    return h


def wt(T, q):
    return LN(q * T / (2 * PI)) / (2 * PI) + 1 / (4 * T)


def exp_exact(T0, q):
    e = math.exp(-c * T0)
    IT = (T0 / c + 1 / c ** 2) * e
    ITlog = ((T0 / c + 1 / c ** 2) * LN(T0) + 1 / c ** 2 + eE1(c * T0) / c ** 2) * e
    return k21 * ((LN(q / (2 * PI)) * IT + ITlog) / (2 * PI) + e / (4 * c))


def gauss_exact(T0, d, q, m=60):
    d = abs(d)
    if d == 0:
        return 0.0
    U = 1.5 * (PI * d) ** 2
    if T0 >= U:
        return 0.0
    f = lambda T: (k20 / 4) * (T / (PI * d)) ** 2 * math.exp(-cp * (T / (PI * d)) ** 2) * wt(T, q)
    return gl(f, T0, min(U, T0 + 40 * PI * d), m)


def N1(T0, q):
    return T0 * LN(q * T0 / (2 * PI)) * math.exp(-c * T0)


def N2(T0, d, q):
    return T0 * LN(q * T0 / (2 * PI)) * math.exp(-cp * (T0 / (PI * d)) ** 2)


# norms of eta (9.56), exact
g = 0.5772156649015329
sp = math.sqrt(PI)
n2 = math.sqrt(3 / 8 * sp)
nd2 = math.sqrt(7 / 16 * sp)
nlog2 = math.sqrt(sp / 64 * (8 * (3 * g - 8) * LN(2) + 3 * PI ** 2 + 6 * g ** 2 + 24 * LN(2) ** 2 + 16 - 32 * g))
nos = 2 ** 0.25 * math.gamma(0.25) / 4


def H914(T0, q):
    return (n2 + nlog2) * math.sqrt(T0) * LN(q * T0) + (17.21 * nlog2 - LN(2 * PI * math.sqrt(math.e)) * n2) * math.sqrt(T0) + nos * (1.32 * LN(q) + 34.5)


# ---- moments of eta_2 ----
m0 = avg(lambda w: 1.0, 20)
mh = avg(lambda w: w ** -0.5, 20)
m1 = avg(lambda w: 1 / w, 20)
m32 = avg(lambda w: w ** -1.5, 20)
mg = avg(lambda w: math.exp(-0.1065 * 100 * (1 / w ** 2 - 1)), 20)
print("eta_2 moments: %.7f %.7f %.7f %.7f (book 1, <=1.37259, 4(log2)^2=%.7f, <=2.74517); Gaussian %.7f (book <= 0.006446)"
      % (m0, mh, m1, m32, 4 * LN(2) ** 2, mg))
mom_ok = abs(m0 - 1) < 1e-9 and mh <= 1.37259 and m1 <= 1.92182 and m32 <= 2.74517 and mg <= 0.006446
print("eta_2(w) for w in [-1/4, 1/4): ", [eta2(w) for w in (-0.25, 0.0, 0.2)], " (support is [1/4,1])")

# ---- (1) small x ----
A = gl(eta_star, 0.0, 16.0, 64)
print("|eta_*|_1 = %.7f (sqrt(pi/2) = %.7f)" % (A, math.sqrt(PI / 2)))


def lam(n):
    for p in range(2, int(n ** 0.5) + 1):
        if n % p == 0:
            k = n
            while k % p == 0:
                k //= p
            return LN(p) if k == 1 else 0.0
    return LN(n) if n >= 2 else 0.0


LAM = [lam(n) for n in range(80)]


def S(x):
    return sum(LAM[n] * eta_star(n / x) for n in range(2, min(79, int(16 * x) + 2))) + A * x


best = (0.0, 0.0)
for i in range(1, 801):
    x = 4.0 * i / 800
    r = S(x) / (51.17 * math.sqrt(x) + 6 + 18 / math.sqrt(x))
    if r > best[0]:
        best = (r, x)
print("(1) 0 < x <= 4: max [sum Lambda(n) eta_*(n/x) + |eta_*|_1 x] / (51.17 sqrt x + 6 + 18/sqrt x) = %.5f at x = %.3f" % best)
print("    Prop 9.3.2 at scale wx needs wx >= 1 for all w in [1/4,1], i.e. x >= 4")

# ---- (2) averaged proof bound, q = 1, delta = 0, T0 = 50 ----
T0 = 50.0
first_proof = exp_exact(T0, 1)
first_print = 6.11 * N1(T0, 1)


def proof_avg(x):  # q = 1, delta = 0, R = 0
    return first_proof + mh * H914(T0, 1) * x ** -0.5 + m32 * 6.01 * nd2 * x ** -1.5


def printed(x):  # (9.61) at q = 1, delta = 0
    return first_print + (1.679 * math.sqrt(T0) * LN(T0) + 6.957 * math.sqrt(T0) + 51.17) * x ** -0.5 + 6 / x + 18 * x ** -1.5


print("(2) q=1, delta=0, T0=50: first line exact %.7f (=%.4f N1) vs printed %.7f; second-line coefficient %.4f vs %.4f"
      % (first_proof, first_proof / N1(T0, 1), first_print, mh * H914(T0, 1), 1.679 * math.sqrt(T0) * LN(T0) + 6.957 * math.sqrt(T0) + 51.17))
lo, hi = 4.0, 1e12
for _ in range(200):
    mid = math.sqrt(lo * hi)
    lo, hi = (lo, mid) if proof_avg(mid) > printed(mid) else (mid, hi)
x0 = hi
mono = all(proof_avg(x) > printed(x) for x in [x0 * 1.01, 4e4, 1e6, 1e10, 1e20])
print("    averaged proof bound > (9.61) for x > %.4g (checked at 4e4, 1e6, 1e10, 1e20: %s)" % (x0, mono))

# ---- Gaussian average ----
gmax = (0.0, 0.0)
for k in range(0, 23):
    d = 2.5 + 0.25 * k
    T = 10 * PI * d
    v = avg(lambda w: gauss_exact(T, d * w, 1), 3) / N2(T, d, 1)
    if v > gmax[0]:
        gmax = (v, d)
print("    averaged exact Gaussian coefficient, q=1, T0=10pi|delta|, |delta| in [2.5,8]: max %.6f at |delta| = %.2f (printed 0.0102)" % gmax)

ok = mom_ok and best[0] < 1 and x0 <= 4e4 and mono and gmax[0] <= 0.0102
if ok:
    print("CONFIRMED: the proof covers only x >= 4 (the case x < 4 holds trivially, ratio %.4f), and at q=1, delta=0, T0=50 the eta_2-average of the proof's bounds (first line %.4f N1 > 6.11 N1) exceeds (9.61) for x > %.3g, while the averaged Gaussian coefficient stays <= %.5f <= 0.0102." % (best[0], first_proof / N1(T0, 1), x0, gmax[0]))
else:
    print("NOT CONFIRMED: the small-x bound, the averaged first line, or the Gaussian average does not behave as claimed.")
