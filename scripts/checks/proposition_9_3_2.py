"""Check of [H, Prop 9.3.2] (first line of (9.57), constants 6.11 and 1.578).

Claim: the proof (via Lemma 9.3.1) does not establish (9.57) for q = 1 in two
corners once x is large: (i) T0 < ~52.4 with small |delta| (e.g. delta = 0),
because (9.50)-(9.51) treat the weight's 1/(4T) term as c1/t although
f(T) ~ T e^{-0.1598T} makes it the constant 1/4 (exact majorant 6.169 > 6.11
at T0 = 50); (ii) 2.9 <~ |delta| <~ 6 with T0 near 10 pi |delta|, because the
last step of (9.54) uses the 2013 hypothesis y = T0/(pi|delta|) >= 4 pi while
only y >= 10 is assumed (bracket 1.6042 at y = 10).  The printed statement
is not shown false; 6.19 and 1.605 would work.

Book inputs (expform.tex):
  - l.1044-1050 Lemma 9.3.1, T0 >= max(10 pi |delta|, 50); l.1283 same in Prop 9.3.2.
  - l.1081-1091 (9.48): f = 5.13 T e^{-0.1598T} + (7.96/4)(T/(pi delta))^2
    e^{-0.1065 (T/(pi delta))^2} for T < (3/2)(pi delta)^2.
  - l.1099-1103 (9.49): weight (1/2pi) log(qT/2pi) + 1/(4T).
  - l.1106-1129 (9.50)-(9.51) with c1 = pi/2 as c1/t; l.1140-1142 (9.52) 6.11.
  - l.1228-1239 (9.54): bracket 1.487 + 2.566(1+1/log y)/(pi y) <= 1.578, using T0 >= 4 pi^2 |delta|.
  - l.1294-1303 (9.57) err; l.1313-1323 proof: Lemma 9.1.4 term
    (1.22 sqrt T0 log qT0 + 5.056 sqrt T0 + 1.423 log q + 37.188) sqrt x,
    Lemma 9.1.1 term (log q + 6.01)(|eta'|_2 + 2 pi |delta| |eta|_2) x^{-1/2}.
  - l.264-266: R = 0 for q = 1 when eta(0) = 0.
  - l.616-637 (9.31) Lemma 9.1.4 and l.1260-1273 (9.56) norms of eta.

Method: the first line of the proof's bound is computed exactly (closed form
for the exponential part, Gauss-Legendre for the Gaussian part, cut off at
(3/2)(pi delta)^2) and compared with the printed first line; the remaining
lines of the proof's bound (with exact norms, which is smaller than the
proof's rounded constants) are added and compared with the printed (9.57) as
x grows.

Confirms if: at q = 1 the exact first line exceeds the printed one at
(T0 = 50, delta = 0) and at (|delta| = 3.35, T0 = 10 pi |delta|), the full
proof bound exceeds (9.57) for all x beyond 2e3 resp. 3e6, while the
first line with 6.19 and 1.605 is not exceeded on the scanned region.

Run: python3 -I proposition_9_3_2.py

Ported from a 2026-11-06 check script.
"""
import math

PI = math.pi
c, cp, k21, k20 = 0.1598, 0.1065, 5.13, 7.96


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


GL = legendre(20)


def gl(f, a, b, m):
    h = (b - a) / m
    s = 0.0
    for j in range(m):
        mid = a + (j + 0.5) * h
        s += sum(w * f(mid + 0.5 * h * x) for x, w in GL)
    return s * h / 2


def wt(T, q):
    return math.log(q * T / (2 * PI)) / (2 * PI) + 1 / (4 * T)


def exp_exact(T0, q):
    """5.13 int_{T0}^oo T e^{-cT} wt(T) dT, closed form."""
    e = math.exp(-c * T0)
    IT = (T0 / c + 1 / c ** 2) * e
    ITlog = ((T0 / c + 1 / c ** 2) * math.log(T0) + 1 / c ** 2 + eE1(c * T0) / c ** 2) * e
    return k21 * ((math.log(q / (2 * PI)) * IT + ITlog) / (2 * PI) + e / (4 * c))


def exp_quad(T0, q):
    return gl(lambda T: k21 * T * math.exp(-c * T) * wt(T, q), T0, T0 + 500, 500)


def gauss_exact(T0, d, q, m=120):
    d = abs(d)
    if d == 0:
        return 0.0
    U = 1.5 * (PI * d) ** 2
    if T0 >= U:
        return 0.0
    f = lambda T: (k20 / 4) * (T / (PI * d)) ** 2 * math.exp(-cp * (T / (PI * d)) ** 2) * wt(T, q)
    return gl(f, T0, min(U, T0 + 40 * PI * d), m)


def N1(T0, q):
    return T0 * math.log(q * T0 / (2 * PI)) * math.exp(-c * T0)


def N2(T0, d, q):
    return T0 * math.log(q * T0 / (2 * PI)) * math.exp(-cp * (T0 / (PI * d)) ** 2) if d else 0.0


def line1(T0, d, q, A=6.11, B=1.578):
    return A * N1(T0, q) + B * N2(T0, d, q)


def exact1(T0, d, q):
    return exp_exact(T0, q) + gauss_exact(T0, d, q)


def a951(T0, c1_const):
    L = math.log(T0)
    t = PI / 2 if c1_const else (PI / 2) / T0
    return (L / c + 1 / c + t) / (L / c - 1 / (c * c * T0))


def chain951(T0, q, a):  # 5.13 * RHS(9.51) / N1
    r = (math.log(q / (2 * PI)) * (T0 / c + 1 / c ** 2) + (T0 / c + a / c ** 2) * math.log(T0)) * math.exp(-c * T0) / (2 * PI)
    return k21 * r / N1(T0, q)


# exact norms of eta = t^2 e^{-t^2/2} ((9.56))
g = 0.5772156649015329
sp = math.sqrt(PI)
eta2 = math.sqrt(3 / 8 * sp)
etad2 = math.sqrt(7 / 16 * sp)
etalog2 = math.sqrt(sp / 64 * (8 * (3 * g - 8) * math.log(2) + 3 * PI ** 2 + 6 * g ** 2 + 24 * math.log(2) ** 2 + 16 - 32 * g))
eos = 2 ** 0.25 * math.gamma(0.25) / 4


def H914(T0, q):  # Lemma 9.1.4 (9.31) with exact norms
    return (eta2 + etalog2) * math.sqrt(T0) * math.log(q * T0) + (17.21 * etalog2 - math.log(2 * PI * math.sqrt(math.e)) * eta2) * math.sqrt(T0) + eos * (1.32 * math.log(q) + 34.5)


def proof_bound(x, T0, d, q):  # q = 1 only: R = 0
    return exact1(T0, d, q) + H914(T0, q) * x ** -0.5 + (math.log(q) + 6.01) * (etad2 + 2 * PI * abs(d) * eta2) * x ** -1.5


def printed(x, T0, d, q):
    return line1(T0, d, q) + (1.22 * math.sqrt(T0) * math.log(q * T0) + 5.056 * math.sqrt(T0) + 1.423 * math.log(q) + 37.19) * x ** -0.5 \
        + (3 + 11 * abs(d)) / x + (math.log(q) + 6) * (1 + 6 * abs(d)) * x ** -1.5


def threshold(T0, d):
    """Smallest x (bisection in log x) beyond which proof_bound > printed, assuming one crossing."""
    lo, hi = 1.0, 1e15
    if proof_bound(hi, T0, d, 1) <= printed(hi, T0, d, 1):
        return None
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if proof_bound(mid, T0, d, 1) > printed(mid, T0, d, 1):
            hi = mid
        else:
            lo = mid
    return hi


print("norms: |eta|_2=%.6f |eta'|_2=%.6f |eta log|_2=%.6f |eta/sqrt t|_1=%.6f" % (eta2, etad2, etalog2, eos))
print("Lemma 9.1.4 coefficients (exact norms): %.6f %.6f %.6f (book 1.22, 5.056, 37.188)"
      % (eta2 + etalog2, 17.21 * etalog2 - math.log(2 * PI * math.sqrt(math.e)) * eta2, 34.5 * eos))
print()
print("(i) exponential part, q = 1, in units of T0 log(T0/2pi) e^{-0.1598 T0}")
for T0 in [50, 51, 52, 52.4, 53, 60]:
    print("  T0=%5.1f exact %.6f (quad %.6f) | (9.51) chain with c1/y: a=%.5f -> %.5f | with constant c1: a=%.5f -> %.5f"
          % (T0, exp_exact(T0, 1) / N1(T0, 1), exp_quad(T0, 1) / N1(T0, 1), a951(T0, False), chain951(T0, 1, a951(T0, False)),
             a951(T0, True), chain951(T0, 1, a951(T0, True))))
lo, hi = 50.0, 60.0
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if exp_exact(mid, 1) / N1(mid, 1) > 6.11 else (lo, mid)
cross = lo
print("  exact exponential constant crosses 6.11 at T0 = %.4f" % cross)
r_i = exp_exact(50, 1) / N1(50, 1)
print()
print("(ii) (9.54) bracket 1.487 + 2.566(1+1/log y)/(pi y): y=10 -> %.5f, y=4pi -> %.5f"
      % (1.487 + 2.566 * (1 + 1 / math.log(10)) / (PI * 10), 1.487 + 2.566 * (1 + 1 / math.log(4 * PI)) / (4 * PI ** 2)))
d = 3.0
print("    exact cut-off Gaussian majorant at q=1, |delta|=3, T0=30pi: %.5f" % (gauss_exact(30 * PI, d, 1, 400) / N2(30 * PI, d, 1)))
print()
print("(iii) exact first line / printed first line, q = 1, T0 = 10 pi |delta|")
bad = []
mx = (0, 0)
for k in range(213, 1201, 2):
    d = k / 100
    T0 = max(10 * PI * d, 50)
    r = exact1(T0, d, 1) / line1(T0, d, 1)
    if r > 1:
        bad.append(d)
    if r > mx[0]:
        mx = (r, d)
print("    ratio > 1 for |delta| in [%.2f, %.2f] (grid step 0.02); max %.6f at |delta| = %.2f" % (min(bad), max(bad), mx[0], mx[1]))
mq = max(exact1(max(10 * PI * k / 10, 50), k / 10, q) / line1(max(10 * PI * k / 10, 50), k / 10, q) for q in [3, 4, 5] for k in range(22, 121, 2))
print("    max ratio for q in {3,4,5}, |delta| in [2.2,12]: %.6f" % mq)
# corrected constants 6.19, 1.605
mc = 0.0
for k in range(0, 1201, 4):
    d = k / 100
    for T0 in [50, 52, 55, 60, 10 * PI * d, 10.5 * PI * d, 12 * PI * d]:
        if T0 < max(10 * PI * d, 50):
            continue
        mc = max(mc, exact1(T0, d, 1) / line1(T0, d, 1, 6.19, 1.605))
print("    with 6.19 and 1.605: max ratio %.6f over the scan" % mc)
print()
print("(iv) full proof bound vs printed (9.57), q = 1 (R = 0, exact norms)")
t1 = threshold(50, 0.0)
d = 3.35
t2 = threshold(10 * PI * d, d)
print("    delta=0, T0=50: proof bound > (9.57) for x > %.4g; first-line excess %.4e" % (t1, exact1(50, 0, 1) - line1(50, 0, 1)))
print("    |delta|=3.35, T0=10pi|delta|: proof bound > (9.57) for x > %.4g; first-line excess %.4e" % (t2, exact1(10 * PI * d, d, 1) - line1(10 * PI * d, d, 1)))
for x in [1e4, 1e8, 1e12]:
    print("      x=%.0e: delta=0 bound/printed %.6f ; |delta|=3.35 %.6f" % (x, proof_bound(x, 50, 0, 1) / printed(x, 50, 0, 1),
                                                                     proof_bound(x, 10 * PI * d, d, 1) / printed(x, 10 * PI * d, d, 1)))

ok = (r_i > 6.11 and 52.0 < cross < 52.6 and mx[0] > 1 and min(bad) < 3.0 and max(bad) > 5.5 and mq < 1
      and mc < 1 and t1 is not None and t1 <= 2e3 and t2 is not None and t2 <= 3e6)
if ok:
    print("CONFIRMED: for q=1 the exact first-line majorant exceeds 6.11/1.578 (6.169 at T0=50, delta=0, above 6.11 until T0=%.2f; up to %.3f%% at T0=10pi|delta| for |delta| in [%.2f,%.2f]), so the proof's bound exceeds (9.57) for x > %.3g resp. %.3g, while 6.19 and 1.605 suffice for the first line on the scan." % (cross, 100 * (mx[0] - 1), min(bad), max(bad), t1, t2))
else:
    print("NOT CONFIRMED: the exact first-line majorant or the x thresholds do not match the claim.")
