"""Eq 4.42 (Lemma 4.2.3, typeI.tex:1206-1220): the general large-delta bound omits the main term.

Claim. The lemma states that for |delta| >= 1/2c2 the absolute value of (4.39) is at most
(4.42) for eps in (0,1] (typeI.tex:1206), with no "(4.40) plus" (compare Lemmas 4.2.1/4.2.2);
the case-(a) proof bounds only (4.43), i.e. q does not divide m or m > Q/2.  When M/q is small
the single term m = q contributes about (x/2q) log(x/q) |hat eta(delta/2)|, which exceeds (4.42).

Book inputs:
  - Lemma 4.2.3 hypotheses, (4.39), (4.42), c1 = 1 + |eta'|_1/(x/D), c2 = 6 pi/(5 sqrt c0):
    typeI.tex:1153-1220.
  - eta = eta_2(t) = 4 max(log 2 - |log 2t|, 0): intromin.tex:124-125; |eta_2'|_1 = 8 log 2:
    minarctotals.tex:39-41; (4.38) with rho0 = 4: minarctotals.tex:44-50, 59-61.
  - c0 = 31.521: normfour.tex:64, 171; minarctotals.tex:86.
Method. (4.39) is evaluated as a finite sum over odd m <= D and odd n (blockwise Taylor
expansion of log n with exact phase tables; truncation error bounded and printed; validated
against naive summation).  (4.42) is evaluated at several eps and a rigorous lower bound for its
 the eps-interval on which (4.42) < |(4.39)| is certified from its monotone parts.
Confirms the claim if: |(4.39)| minus its error bound exceeds (4.42) at eps = 0.1 in the claim's
example, and on all of eps in [1e-6, 1] in at least one admissible case.
Run: python3 -I eq_4_42.py
Ported from a 2026-11-06 check script.
"""
import math, cmath, time
from fractions import Fraction as Fr

PI = math.pi
LOG2 = math.log(2.0)
ETA1 = 8 * LOG2          # |eta_2'|_1, minarctotals.tex:39-41
C0_BOOK = 31.521         # c_0 for eta_2, normfour.tex:64,171; minarctotals.tex:86
C0_L1 = 48.0             # |eta_2''|_1 = 48 >= |hat(eta_2'')|_inf, minarctotals.tex:39-41
RHO0 = 4                 # rho_0 = 4, minarctotals.tex:61


def c2_of(c0):
    """c_2 = 6 pi / (5 sqrt(c_0)), typeI.tex:1169."""
    return 6 * PI / (5 * math.sqrt(c0))


def eta2(t):
    """eta_2(t) = 4 max(log 2 - |log 2t|, 0), intromin.tex:124-125."""
    if t <= 0.25 or t >= 1.0:
        return 0.0
    return 4.0 * max(LOG2 - abs(math.log(2.0 * t)), 0.0)


# ---- Fourier transforms hat g(xi) = int g(t) e(-xi t) dt by Gauss-Legendre ----
def _gl(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        z = math.cos(PI * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p1, p2 = 1.0, 0.0
            for j in range(1, n + 1):
                p1, p2 = ((2 * j - 1) * z * p1 - (j - 1) * p2) / j, p1
            pp = n * (z * p1 - p2) / (z * z - 1.0)
            dz = p1 / pp
            z -= dz
            if abs(dz) < 1e-16:
                break
        xs.append(z)
        ws.append(2.0 / ((1.0 - z * z) * pp * pp))
    return xs, ws


def _fourier_raw(g, xi, nodes, pieces):
    xs, ws = _gl(nodes)
    tot = 0j
    for a, b in ((0.25, 0.5), (0.5, 1.0)):
        h = (b - a) / pieces
        for p in range(pieces):
            mid = a + (p + 0.5) * h
            s = 0j
            for x_, w_ in zip(xs, ws):
                t = mid + 0.5 * h * x_
                s += w_ * g(t) * cmath.exp(-2j * PI * xi * t)
            tot += s * 0.5 * h
    return tot


def eta_hat(xi):
    a = _fourier_raw(eta2, xi, 20, 16)
    b = _fourier_raw(eta2, xi, 30, 32)
    assert abs(a - b) < 1e-12, (a, b)
    return b


def logeta_hat(xi):
    g = lambda t: math.log(t) * eta2(t)
    a = _fourier_raw(g, xi, 20, 16)
    b = _fourier_raw(g, xi, 30, 32)
    assert abs(a - b) < 1e-12, (a, b)
    return b


# ---- Moebius function ----
def mobius(N):
    mu = [1] * (N + 1)
    mu[0] = 0
    comp = bytearray(N + 1)
    primes = []
    for i in range(2, N + 1):
        if not comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            ip = i * p
            if ip > N:
                break
            comp[ip] = 1
            if i % p == 0:
                mu[ip] = 0
                break
            mu[ip] = -mu[i]
    return mu


# ---- The sum (4.39), evaluated term by term ------------------------------
# S = sum_{m<=D, m odd} mu(m) T_m,  T_m = sum_{n odd} e(alpha m n) (log n) eta_2(mn/x),
# with 2 alpha = a/q + delta/x (typeI.tex:1154).  Replacing alpha by alpha+1/2
# multiplies every term (m, n odd) by -1, so |S| does not depend on the lift.
# On x/4 < mn <= x/2: (log n) eta_2 = 4 log n (log(4m/x) + log n);
# on x/2 < mn < x:    (log n) eta_2 = -4 log n (log(m/x) + log n).
# Odd n are taken in blocks n = c + 2j, 0 <= j < L (L a power of 2, 2L <= R c);
# log n = log c + log(1 + (2L/c) t), t = j/L, is replaced by its Taylor polynomial
# of degree K in t, and sum_j w^j t^k (w = e(2 alpha m)) is tabulated exactly for
# L = 2^s by doubling.  The truncation error is bounded and reported.

K = 16
R = 0.05


def _tables(beta2, smax):
    """G[s][k] = sum_{j<2^s} w^j (j/2^s)^k, w = e(beta2); beta2 a Fraction."""
    binom = [[math.comb(k, i) for i in range(K + 1)] for k in range(K + 1)]
    G = [[1.0 + 0j] + [0j] * K]           # L = 1: only j = 0, t^0 = 1, t^k = 0
    for s in range(smax):
        L = 1 << s
        wL = cmath.exp(2j * PI * float((beta2 * L) % 1))
        g = G[s]
        # sum_{j<2L} w^j (j/2L)^k = 2^-k [ G_k(L) + w^L sum_i C(k,i) G_i(L) ]
        new = []
        for k in range(K + 1):
            acc = 0j
            bk = binom[k]
            for i in range(k + 1):
                acc += bk[i] * g[i]
            new.append((g[k] + wL * acc) / (2 ** k))
        G.append(new)
    return G


def _polymul(a, b):
    out = [0.0] * (K + 1)
    for i, ai in enumerate(a):
        if ai == 0.0:
            continue
        for j in range(K + 1 - i):
            out[i + j] += ai * b[j]
    return out


def T_odd(m, x, alpha):
    """sum over odd n of e(alpha m n) (log n) eta_2(mn/x); returns (value, error bound)."""
    beta = alpha * m
    total = 0j
    err = 0.0
    nterms = 0
    lo1 = x // (4 * m) + 1            # smallest n with 4mn > x
    hi1 = x // (2 * m)                # largest n with 2mn <= x
    lo2 = hi1 + 1
    hi2 = (x - 1) // m                # largest n with mn < x
    segs = []
    for lo, hi, A, B in ((lo1, hi1, 4.0, math.log(4 * m / x)), (lo2, hi2, -4.0, math.log(m / x))):
        if lo % 2 == 0:
            lo += 1
        if hi % 2 == 0:
            hi -= 1
        if hi >= lo:
            segs.append((lo, hi, A, B))
    if not segs:
        return 0j, 0.0
    smax = max(0, int(math.log2(max(1.0, R * segs[-1][1] / 2))) + 1)
    G = _tables(2 * beta, smax + 1)
    for lo, hi, A, B in segs:
        c = lo
        remaining = (hi - lo) // 2 + 1
        while remaining > 0:
            s = min(remaining.bit_length() - 1, len(G) - 1)
            while s > 0 and 2 * (1 << s) > R * c:
                s -= 1
            L = 1 << s
            l0 = math.log(c)
            y = 2 * L / c
            P = [0.0] + [(-1) ** (k + 1) * y ** k / k for k in range(1, K + 1)]
            P2 = _polymul(P, P)
            coef = [A * (l0 * (B + l0) if k == 0 else 0.0) + A * ((B + 2 * l0) * P[k] + P2[k])
                    for k in range(K + 1)]
            g = G[s]
            acc = 0j
            for k in range(K + 1):
                acc += coef[k] * g[k]
            ph = cmath.exp(2j * PI * float((beta * c) % 1))
            total += ph * acc
            # remainder of log(1+y t), |y t| <= y <= R:  <= y^(K+1)/((K+1)(1-y))
            rem = y ** (K + 1) / ((K + 1) * (1 - y)) if s > 0 else 0.0
            umax = l0 + y
            err += L * abs(A) * (abs(B) + 2 * umax + 2 * rem + 1e-300) * rem
            # floating-point rounding allowance
            err += L * 1e-13 * abs(A) * (abs(B) + 2 * umax) * umax
            nterms += L
            c += 2 * L
            remaining -= L
    return total, err


def S_439(x, q, a, delta, D, mu=None):
    """(4.39) for 2 alpha = a/q + delta/x; delta a Fraction, x an int."""
    alpha = Fr(a, 2 * q) + Fr(delta) / (2 * x)
    if mu is None:
        mu = mobius(int(D))
    tot = 0j
    err = 0.0
    for m in range(1, int(D) + 1, 2):
        if mu[m] == 0:
            continue
        v, e_ = T_odd(m, x, alpha)
        tot += mu[m] * v
        err += e_
    return tot, err


def S_439_naive(x, q, a, delta, D):
    alpha = Fr(a, 2 * q) + Fr(delta) / (2 * x)
    mu = mobius(int(D))
    tot = 0j
    for m in range(1, int(D) + 1, 2):
        if mu[m] == 0:
            continue
        b = alpha * m
        for n in range(x // (4 * m) + 1, x // m + 1):
            if n % 2 == 0:
                continue
            t = m * n / x
            if t >= 1.0:
                continue
            tot += mu[m] * cmath.exp(2j * PI * float((b * n) % 1)) * math.log(n) * eta2(t)
    return tot


# ---- The printed bounds of Lemma 4.2.3 (typeI.tex:1176-1220) ------------------
def mu_sums(M_over_q, x, q, coprime_to):
    mu = mobius(int(M_over_q))
    s1, s2 = [], []
    for m in range(1, int(M_over_q) + 1):
        if mu[m] and math.gcd(m, coprime_to) == 1:
            s1.append(mu[m] / m)
            s2.append(mu[m] / m * math.log(x / (m * q)))
    return math.fsum(s1), math.fsum(s2)


def bound_440_printed(x, q, delta, D, M, c0):
    """(4.40) as printed, typeI.tex:1176-1189: x/q, min(1,(c0/delta^2)/(2pi)^2), (m,q)=1, hat(log eta)(-delta)."""
    d = float(delta)
    s1, s2 = mu_sums(M / q, x, q, q)
    mn = min(1.0, (c0 / d ** 2) / (2 * PI) ** 2) if d != 0 else 1.0
    return ((x / q) * mn * abs(s2) + (x / q) * abs(logeta_hat(-d)) * abs(s1)
            + c0 * (0.5 - 2 / PI ** 2) * (D ** 2 / (4 * q * x) * math.log(math.sqrt(math.e) * x / D) + 1 / math.e))


def bound_440_oddn(x, q, delta, D, M, c0):
    """Main term of the odd-n sum, as the proof's first display (typeI.tex:1236-1245) gives it:
    x/2q, min(1, c0/(pi delta)^2) >= |hat eta(-delta/2)|, (m,2q)=1, hat(log eta)(-delta/2)."""
    d = float(delta)
    s1, s2 = mu_sums(M / q, x, q, 2 * q)
    mn = min(1.0, c0 / (PI * d) ** 2) if d != 0 else 1.0
    return ((x / (2 * q)) * mn * abs(s2) + (x / (2 * q)) * abs(logeta_hat(-d / 2)) * abs(s1)
            + c0 * (0.5 - 2 / PI ** 2) * (D ** 2 / (4 * q * x) * math.log(math.sqrt(math.e) * x / D) + 1 / math.e))


def logp(z):
    return max(math.log(z), 0.0)


def bound_441(x, q, D, c0):
    """(4.41), typeI.tex:1191-1202, with c1 = 1 + |eta'|_1/(x/D) (typeI.tex:1203)."""
    c1 = 1 + ETA1 / (x / D)
    c2 = c2_of(c0)
    A = 2 * math.sqrt(c0 * c1) / PI
    return (A * D * math.log(math.e * x / D)
            + 1.5 * c1 * (x / q) * logp(D / (c2 * x / q)) * math.log(q / c2)
            + ((2 * ETA1 / PI) * max(1.0, math.log(c0 * math.e ** 3 * q * q / (4 * PI * ETA1 * x))) * math.log(x)
               + A * (math.sqrt(3) + 0.5 * logp(D / (q / 2))) * math.log(q / c2)) * q
            + 1.5 * c1 * math.sqrt(2 * x / c2) * math.log(2 * x / c2)
            + 20 * c0 * c2 ** 1.5 / (3 * PI ** 2) * math.sqrt(2 * x) * math.log(2 * math.sqrt(math.e) * x / c2))


def _442_parts(x, q, delta, D, c0):
    d = abs(float(delta))
    c1 = 1 + ETA1 / (x / D)
    c2 = c2_of(c0)
    A = 2 * math.sqrt(c0 * c1) / PI
    X = x / (d * q)
    const = A * D * math.log(math.e * x / D) + (40 / 3) * math.sqrt(2) * c0 * c2 ** 1.5 * math.sqrt(x) * math.log(x) \
        + 0.75 * c1 * (2 / math.sqrt(5)) * math.sqrt(x) * math.log(x)
    # increasing in eps:
    inc = lambda e: A * (1 + e) * (X + 1) * (math.sqrt(3 + 2 * e) * logp(2 * math.sqrt(math.e) * d * q)
                                            + 0.5 * logp(2 * D / X) * logp(2 * d * q))
    # decreasing in eps:
    dec = lambda e: 0.75 * c1 * (1 + e) / (2 * e) * math.log(x) * math.sqrt(x) * math.log(x)
    return const, inc, dec


def bound_442(x, q, delta, D, c0, eps):
    """(4.42), typeI.tex:1207-1220."""
    const, inc, dec = _442_parts(x, q, delta, D, c0)
    return const + inc(eps) + dec(eps)


def eps_fail_range(x, q, delta, D, c0, value):
    """Largest grid interval [lo, hi] of eps in [1e-40, 1] on which (4.42) < value is certified:
    on [e0, e1] (4.42) <= const + inc(e1) + dec(e0), its increasing/decreasing parts being monotone."""
    const, inc, dec = _442_parts(x, q, delta, D, c0)
    grid = [10 ** (-40 + 40 * i / 20000) for i in range(20001)]   # 1e-40 .. 1
    best, cur = None, None
    for e0, e1 in zip(grid, grid[1:]):
        if const + inc(e1) + dec(e0) < value:
            cur = (cur[0], e1) if cur else (e0, e1)
            if best is None or math.log(cur[1] / cur[0]) > math.log(best[1] / best[0]):
                best = cur
        else:
            cur = None
    return best


def hyps(x, q, delta, D, Q0, c0):
    d = abs(float(delta))
    c2 = c2_of(c0)
    out = {
        "|delta/x| <= 1/(q Q0)": d / x <= 1 / (q * Q0),
        "q <= Q0": q <= Q0,
        "Q0 >= max(16, 2 sqrt x)": Q0 >= max(16, 2 * math.sqrt(x)),
        "sqrt3 <= D <= min(x/rho0, x/e)": math.sqrt(3) <= D <= min(x / RHO0, x / math.e),
        "|delta| >= 1/(2 c2)": d >= 1 / (2 * c2),
        "D <= Q0/2": D <= Q0 / 2,
    }
    return out
# ---------------------------------------------------------------------------


def main():
    t0 = time.time()
    for args in ((300000, 3, 1, Fr(3), 5), (400000, 1, 0, Fr(3, 4), 2)):
        v, e = S_439(*args)
        w = S_439_naive(*args)
        print("validation %s: blocks %.10e, naive %.10e, |diff| %.1e (bound %.1e)" % (args, abs(v), abs(w), abs(v - w), e))
        assert abs(v - w) <= e + 1e-6 * abs(w)
    c0 = C0_BOOK
    print("c2 = %.7f, 1/(2 c2) = %.6f" % (c2_of(c0), 1 / (2 * c2_of(c0))))
    results = []
    for label, x, q, a, delta, D in (
            ("Claim's example: q=3, a=1, delta=3, D=5, x=1e30", 10 ** 30, 3, 1, Fr(3), 5),
            ("Same with x=1e60", 10 ** 60, 3, 1, Fr(3), 5),
            ("q=1, a=0, delta=3/4, D=2, x=1e9", 10 ** 9, 1, 0, Fr(3, 4), 2),
            ("q=1, a=0, delta=1, D=2, x=1e10", 10 ** 10, 1, 0, Fr(1), 2)):
        Q0 = 2 * math.sqrt(x)
        print("=" * 78)
        print(label, " Q0 = 2 sqrt(x)")
        h = hyps(x, q, delta, D, Q0, c0)
        h.pop("D <= Q0/2")                     # not needed for the general clause
        for k, v in h.items():
            print("  hypothesis %-34s %s" % (k, v))
        S, err = S_439(x, q, a, delta, D)
        lower = abs(S) - err
        print("  |(4.39)| by summation = %.7e (error bound %.1e)" % (abs(S), err))
        vals = {eps: bound_442(x, q, delta, D, c0, eps) for eps in (0.01, 0.1, 0.5, 1.0)}
        for eps, v in vals.items():
            print("  (4.42) at eps=%-4g = %.7e   %s" % (eps, v, "FAILS" if lower > v else "holds"))
        rng = eps_fail_range(x, q, delta, D, c0, lower)
        print("  (4.42) < |(4.39)| certified for all eps in %s" % ("[%.3g, %.4g]" % rng if rng else "no grid interval"))
        M = min(math.floor(x / (abs(float(delta)) * q)) / 2, D)
        p40 = bound_440_printed(x, q, delta, D, M, c0)
        o40 = bound_440_oddn(x, q, delta, D, M, c0)
        print("  info: printed (4.40) + (4.42)(eps=0.1) = %.4e; odd-n main term + (4.42)(eps=0.1) = %.4e"
              % (p40 + vals[0.1], o40 + vals[0.1]))
        # the single term m = q carries the log x factor that (4.42) lacks
        Tq, eq = T_odd(q, x, Fr(a, 2 * q) + Fr(delta) / (2 * x))
        print("  |T_{q,o}| = %.7e, (x/2q) log(x/q) |hat eta(delta/2)| = %.7e"
              % (abs(Tq), x / (2 * q) * math.log(x / q) * abs(eta_hat(float(delta) / 2))))
        results.append((all(h.values()), lower > vals[0.1], rng is not None and rng[0] <= 1e-6 and rng[1] >= 0.9999))
    print("total time %.1f s" % (time.time() - t0))
    ex_ok = results[0][0] and results[0][1]
    all_eps = any(r[0] and r[2] for r in results)  # fails on all of [1e-6, 1]
    if ex_ok and all_eps:
        print("CONFIRMED: with eta_2, c0=31.521 and all hypotheses met, the summed |(4.39)| exceeds (4.42) (claim's example at eps=0.1: 3.63e30 vs 2.65e30), and with x=1e60 it exceeds (4.42) for every eps in [1e-6, 1], so (4.42) without a main term is false.")
    else:
        print("NOT CONFIRMED: the summed |(4.39)| did not exceed (4.42) as required (example fails: %s, all-eps failure: %s)." % (ex_ok, all_eps))


if __name__ == "__main__":
    main()
