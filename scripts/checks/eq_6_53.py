"""Check of [H, Eq (6.53)] (first type I bound, |S_{I,1}|, first choice of parameters).

Claim: (6.53) as printed is false. It carries the all-n main term of (4.40)
((x/q) min(1, c_0'/delta^2), Mobius sums over (m,q)=1), but S_{I,1} sums over odd m
and odd n, whose main term is (x/2q)|eta^(-delta/2) S_log + (log eta)^(-delta/2) S_1|
with sums over (m,2q)=1. At x = 2.16e20, q = 101, a = 1, delta = 10.8 the printed
right-hand side is about 3.07e16, while |S_{I,1}| >= 5.88e16.

Book inputs:
  - minarctotals.tex:12-17  2 alpha = a/q + delta/x, (a,q)=1, |delta/x| <= 1/qQ.
  - intromin.tex:251-262  S_{I,1} = sum_{m<=U} mu(m) f(m) sum_n log n e(alpha m n) f(n)
    eta(mn/x), f = 1_{(n,v)=1}, v = 2.
  - minarctotals.tex:25-27 and introductionp.tex:1498  eta = eta_2 = eta_1 *_M eta_1,
    eta_1 = 2 * 1_[1/2,1], so eta_2(t) = 4 log 4t on [1/4,1/2], -4 log t on [1/2,1].
  - minarctotals.tex:1285-1300  y = x^{1/3}/6, Q = (3/4) x^{2/3},
    U = x^{2/3}/(9 sqrt(q delta_0)), delta_0 = max(2, |delta|/4); (6.52) x >= 2.16e20.
  - minarctotals.tex:86, 104, 137-144  c_0 = 31.521, c_0' = 0.798437, c_2 = 6pi/(5 sqrt c_0),
    c_{3,I} .. c_{10,I}.
  - minarctotals.tex:1371-1387  (6.53), evaluated term by term as printed.

Method: the q|m part of S_{I,1} is computed by Poisson summation over odd n (k = 0 mode
exactly, k != 0 modes bounded); the q !| m part is bounded by partial summation
(|sum_r g(r) e(beta r)| <= |g''|_1/(4 sin^2 pi beta)). The Mobius sums over
m <= N = floor(U/q), (m,2q) = 1, are computed exactly (in floating point) by the
Dirichlet-hyperbola recursion sum_{d<=y,(d,2q)=1} A(y/d)/d = 1, validated against a
direct sieve at smaller N. Fourier transforms by composite Gauss-Legendre.

Confirms if the rigorous lower bound main - (bounded remainders) for |S_{I,1}| exceeds
the printed RHS of (6.53) at an admissible point.

Run: python3 -I eq_6_53.py

Ported from a 2026-11-06 check script.
"""
import math, cmath
from math import log, sqrt, isqrt

TWOPI = 2 * math.pi


# ---------------- Fourier transforms of eta_2 (f^(t) = int f(u) e(-tu) du) -------------
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


GX, GW = gl(24)


def integ(f, a, b, pieces):
    h = (b - a) / pieces; s = 0j
    for j in range(pieces):
        mid = a + (j + 0.5) * h
        for x, w in zip(GX, GW):
            s += w * f(mid + x * h / 2)
    return s * h / 2


def ft(t, wt, pieces):
    f1 = lambda u: 4 * log(4 * u) * wt(u) * cmath.exp(-1j * TWOPI * t * u)
    f2 = lambda u: -4 * log(u) * wt(u) * cmath.exp(-1j * TWOPI * t * u)
    return integ(f1, 0.25, 0.5, pieces) + integ(f2, 0.5, 1.0, pieces)


def etahat(t, p=64): return ft(t, lambda u: 1.0, p)
def logetahat(t, p=64): return ft(t, log, p)


# ---------------- Mobius sums over (m, r) = 1 -------------------------------------------
EG = 0.57721566490153286060651209008240243
G1 = -0.07281584548367672486058637587490131   # Stieltjes gamma_1


def sieve_mu(L):
    mu = [1] * (L + 1); mu[0] = 0
    isp = bytearray([1]) * (L + 1)
    for p in range(2, L + 1):
        if isp[p]:
            isp[2 * p::p] = bytearray(len(range(2 * p, L + 1, p)))
            for k in range(p, L + 1, p): mu[k] = -mu[k]
            pp = p * p
            for k in range(pp, L + 1, pp): mu[k] = 0
    return mu


class MuSums:
    """A(y) = sum_{m<=y,(m,r)=1} mu(m)/m, B(y) = sum ... mu(m) log m / m, r squarefree."""

    def __init__(self, r, L):
        self.r = r; self.L = L
        self.divs = [(e, (-1) ** len([p for p in range(2, e + 1) if e % p == 0 and all(p % s for s in range(2, p))]))
                     for e in range(1, r + 1) if r % e == 0]
        mu = sieve_mu(L)
        self.Hs = [0.0] * (L + 1); self.Gs = [0.0] * (L + 1)
        self.As = [0.0] * (L + 1); self.Bs = [0.0] * (L + 1)
        h = g = a = b = 0.0
        for n in range(1, L + 1):
            ln = log(n)
            h += 1.0 / n; g += ln / n
            if mu[n] and math.gcd(n, r) == 1:
                a += mu[n] / n; b += mu[n] * ln / n
            self.Hs[n] = h; self.Gs[n] = g; self.As[n] = a; self.Bs[n] = b
        self.memo = {}

    def H(self, n):
        if n <= self.L: return self.Hs[n]
        return log(n) + EG + 1 / (2 * n) - 1 / (12 * n * n) + 1 / (120 * n ** 4)

    def G(self, n):
        if n <= self.L: return self.Gs[n]
        ln = log(n)
        # Euler-Maclaurin for f(t) = log t / t
        return ln * ln / 2 + G1 + ln / (2 * n) + (1 - ln) / (12 * n * n)

    def Hr(self, y):  # sum_{d<=y,(d,r)=1} 1/d
        return sum(s / e * self.H(y // e) for e, s in self.divs)

    def Gr(self, y):  # sum_{d<=y,(d,r)=1} log d / d
        return sum(s / e * (log(e) * self.H(y // e) + self.G(y // e)) for e, s in self.divs)

    def AB(self, y):
        if y <= self.L: return self.As[y], self.Bs[y]
        if y in self.memo: return self.memo[y]
        r = self.r
        sA = 0.0; sB = 0.0
        s = isqrt(y)
        for d in range(2, s + 1):
            if math.gcd(d, r) == 1:
                a, b = self.AB(y // d)
                sA += a / d; sB += b / d + log(d) / d * a
        # d > s grouped by v = y // d  (v <= y // (s+1))
        vmax = y // (s + 1)
        for v in range(1, vmax + 1):
            lo = max(y // (v + 1), s); hi = y // v
            if hi <= lo: continue
            a, b = self.AB(v)
            w1 = self.Hr(hi) - self.Hr(lo); w2 = self.Gr(hi) - self.Gr(lo)
            sA += a * w1; sB += b * w1 + a * w2
        res = (1.0 - sA, -sB)
        self.memo[y] = res
        return res

    def S1_SL(self, N):
        """S_1 = A(N), SL = sum mu(m)/m log(N/m) = log N A(N) - B(N)."""
        a, b = self.AB(N)
        return a, log(N) * a - b


# ---------------- book constants and printed (6.53) -------------------------------------
c0 = 31.521; c0p = 0.798437
c2 = 6 * math.pi / (5 * sqrt(c0))
c3, c4, c5, c6, c7, c8, c9, c10 = 2.11104, 1.00303, 3.57422, 2.23389, 6.19072, 3.53017, 19.1568, 9.37301


def logplus(z): return max(log(z), 0.0)


def printed653(x, q, d, rho):
    d0 = max(2.0, abs(d) / 4); y = x ** (1 / 3) / 6; s = sqrt(q * d0)
    lp = logplus((x ** (2 / 3) / 9) / (q ** 2.5 * d0 ** 0.5))
    mn = 1.0 if lp == 0 else min(0.8 * rho / lp, 1.0)
    first = (x / q) * min(1.0, c0p / d ** 2) * (mn * (log(9 * x ** (1 / 3) * s) + c3) + c4 * rho)
    rest = ((c7 * log(y / c2) + c8 * log(x)) * y
            + c10 * x ** (1 / 3) / (81 * 4 * q ** 1.5 * d0 ** 0.5) * log(9 * x ** (1 / 3) * sqrt(math.e * q * d0))
            + (c5 * log(2 * x ** (2 / 3) / (9 * c2 * s)) + c6 * log(x ** (5 / 3) / (9 * s))) * x ** (2 / 3) / (9 * s)
            + c9 * sqrt(x) * log(2 * sqrt(math.e) * x / c2) + c10 / math.e)
    return first, rest


def main():
    # Fourier data
    d = 10.8
    e64, e16 = etahat(-d / 2, 64), etahat(-d / 2, 16)
    l64, l16 = logetahat(-d / 2, 64), logetahat(-d / 2, 16)
    print("eta2^(0) = %.15f (should be 1); (log eta2)^(0) = %.12f (should be -(2-log4) = %.12f)"
          % (etahat(0.0).real, logetahat(0.0).real, -(2 - log(4))))
    print("eta2^(-5.4) = %s  |.| = %.10f  (16 vs 64 pieces diff %.1e)" % (e64, abs(e64), abs(e64 - e16)))
    print("(log eta2)^(-5.4) = %s  (diff %.1e)" % (l64, abs(l64 - l16)))
    print("|eta2^(-delta/2)| / (c0'/delta^2) = %.4f ; (2 pi 5.4)^2 |eta2^(5.4)| = %.4f vs c0 = %.3f"
          % (abs(e64) / (c0p / d ** 2), (TWOPI * 5.4) ** 2 * abs(e64), c0))

    # validate the Mobius recursion against a direct sieve
    q = 101; r = 2 * q
    Nt = 3_000_000
    mu = sieve_mu(Nt)
    dA = sum(mu[m] / m for m in range(1, Nt + 1) if mu[m] and math.gcd(m, r) == 1)
    dL = sum(mu[m] / m * log(Nt / m) for m in range(1, Nt + 1) if mu[m] and math.gcd(m, r) == 1)
    del mu
    tst = MuSums(r, 20000)
    tA, tL = tst.S1_SL(Nt)
    nb = 20000
    gerr = abs(tst.Gs[nb] - (log(nb) ** 2 / 2 + G1 + log(nb) / (2 * nb) + (1 - log(nb)) / (12 * nb * nb)))
    herr = abs(tst.Hs[nb] - (log(nb) + EG + 1 / (2 * nb) - 1 / (12 * nb * nb) + 1 / (120 * nb ** 4)))
    print("asymptotic H, G vs direct at n=%d: errors %.1e, %.1e" % (nb, herr, gerr))
    print("validation N=%d: direct S1=%.12e SL=%.12f ; recursion S1=%.12e SL=%.12f"
          % (Nt, dA, dL, tA, tL))
    ok_val = abs(dA - tA) < 1e-11 and abs(dL - tL) < 1e-10 and gerr < 1e-12 and herr < 1e-12

    x = 2.16e20
    d0 = max(2.0, d / 4)
    U = x ** (2 / 3) / (9 * sqrt(q * d0))
    Q = 0.75 * x ** (2 / 3); y = x ** (1 / 3) / 6; V = 4.5 * x ** (1 / 3)
    N = int(U // q)
    adm = (q <= y and abs(d) <= x / (q * Q) and U <= Q / 2 and x / U <= Q and U * V <= x
           and 2e6 <= V < x / 4 and Q >= 2 * sqrt(x))
    print("x=%.3e q=%d a=1 delta=%.1f: y=%.3e Q=%.3e U=%.6e V=%.3e N=%d x/(qQ)=%.1f admissible=%s"
          % (x, q, d, y, Q, U, V, N, x / (q * Q), adm))

    ms = MuSums(r, 3_000_000)
    S1, SL = ms.S1_SL(N)
    Slog = log(x / (q * N)) * S1 + SL
    print("S_1 = sum_{m<=N,(m,2q)=1} mu(m)/m = %.10e ; sum mu(m)/m log(N/m) = %.10f ; S_log = %.10f"
          % (S1, SL, Slog))
    mainT = x / (2 * q) * abs(e64 * Slog + l64 * S1)

    # remainders: |K''|_1 <= 48 log x + 160 for K(v) = (log(x/m) + log v) eta_2(v)
    Kpp = 48 * log(x) + 160
    eps = abs(d) * U / x
    # (i) q|m, Poisson modes k != 0: <= |K''|_1 m/(6x(1-eps)^2) each, sum m <= U^2/(2q) + U
    R1 = Kpp * (U * U / (2 * q) + U) / (6 * x * (1 - eps) ** 2)
    # (ii) q !| m: |T_m| <= (m/x)|K''|_1/(8 ||2 alpha m||^2), ||2 alpha m|| >= min(j,q-j)/q - eps
    per = sum(1.0 / (min(j, q - j) / q - eps) ** 2 for j in range(1, q))
    R2 = (U / x) * Kpp / 8 * per * (U / q + 1)
    lower = mainT - R1 - R2
    first, rest = printed653(x, q, d, q / (q - 1))
    RHS = first + rest
    print("main term (x/2q)|eta^ S_log + (log eta)^ S_1| = %.6e ; remainders <= %.3e + %.3e" % (mainT, R1, R2))
    print("lower bound |S_I1| >= %.6e" % lower)
    print("printed (6.53): first line %.6e + other terms %.4e = RHS %.6e ; lower/RHS = %.3f"
          % (first, rest, RHS, lower / RHS))

    if ok_val and adm and lower > RHS:
        print("CONFIRMED: at x = 2.16e20, q = 101, a = 1, delta = 10.8 the printed RHS of (6.53) is %.3e "
              "but |S_I1| >= %.3e, so (6.53) as printed is false." % (RHS, lower))
    else:
        print("NOT CONFIRMED: no violation of the printed (6.53) established (val=%s adm=%s lower=%.3e RHS=%.3e)."
              % (ok_val, adm, lower, RHS))


if __name__ == "__main__":
    main()
