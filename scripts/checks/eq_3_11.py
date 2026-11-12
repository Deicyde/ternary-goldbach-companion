"""Eq 3.11 ([H], arXiv:1501.05438v2): check of the decomposition (3.11).

Claim: with the printed S_{0,v} = sum_{n|v} Lambda(n) e(alpha n) eta(n/x), the identity
(3.11) S_eta(alpha,x) = S_{I,1} - S_{I,2} + S_{II} + S_{0,infty} + S_{0,v} is false; the
correct remainder is the sum over (n,v) > 1, which also contains the prime powers p^k,
k >= 2, p | v.  For eta = eta_2 and v = 2 the dropped terms total 4 (log 2)^2 at alpha = 0.

Book inputs (book/src/intromin.tex):
  - S_eta(alpha,x) = sum_n Lambda(n) e(alpha n) eta(n/x), (3.1), line 8-9;
  - eta_2(t) = 4 max(log 2 - |log 2t|, 0), (3.3), line 125;
  - (3.9) and the sums S_{I,1}, S_{I,2}, S_{II}, S_{0,infty} of (3.8), lines 247-262;
  - f(n) = 1 if gcd(n,v) = 1, else 0, (3.10), lines 264-266, with v = 2;
  - (3.11) and the printed S_{0,v} = sum_{n|v}, lines 266-270.

Each sum is evaluated directly in double precision at small x (errors ~1e-12).  The claim
is confirmed if, at every test point, S_eta minus the right side of (3.11) with the printed
S_{0,v} is far from 0 (> 1e-3), while the same difference with the remainder
sum_{(n,v)>1} Lambda(n) e(alpha n) eta(n/x) is < 1e-9.  The script also evaluates the dropped
terms n = 2^66, 2^67 at x = 2.16e20, alpha = 0 (they give 4 (log 2)^2).

Run: python3 -I eq_3_11.py
Ported from a 2026-11-06 check script.
"""
import cmath
import math

LOG2 = math.log(2.0)


def eta2(t):
    if t <= 0.25 or t >= 1.0:
        return 0.0
    return 4.0 * max(LOG2 - abs(math.log(2.0 * t)), 0.0)


def e(t):
    return cmath.exp(2j * math.pi * (t - math.floor(t)))


def sieve(N):
    spf = list(range(N + 1))
    for p in range(2, int(N ** 0.5) + 1):
        if spf[p] == p:
            for k in range(p * p, N + 1, p):
                if spf[k] == k:
                    spf[k] = p
    lam = [0.0] * (N + 1)
    mu = [0] * (N + 1)
    if N >= 1:
        mu[1] = 1
    for n in range(2, N + 1):
        p = spf[n]
        m = n // p
        mu[n] = 0 if m % p == 0 else -mu[m]
        k = n
        while k % p == 0:
            k //= p
        if k == 1:
            lam[n] = math.log(p)
    return lam, mu


def check(x, alpha, U, V, v):
    N = int(x)
    lam, mu = sieve(N + 1)
    f = lambda n: 1 if math.gcd(n, v) == 1 else 0
    S = sum(lam[n] * e(alpha * n) * eta2(n / x) for n in range(1, N + 1))
    SI1 = 0j
    for m in range(1, int(U) + 1):
        if mu[m] and f(m):
            for n in range(1, N // m + 1):
                if f(n):
                    SI1 += mu[m] * math.log(n) * e(alpha * m * n) * eta2(m * n / x)
    SI2 = 0j
    for d in range(1, int(V) + 1):
        if lam[d] and f(d):
            for m in range(1, int(U) + 1):
                if mu[m] and f(m):
                    for n in range(1, N // (d * m) + 1):
                        if f(n):
                            SI2 += lam[d] * mu[m] * e(alpha * d * m * n) * eta2(d * m * n / x)
    cm = [0] * (N + 1)
    for d in range(int(U) + 1, N + 1):
        if mu[d]:
            for m in range(d, N + 1, d):
                cm[m] += mu[d]
    SII = 0j
    for m in range(int(U) + 1, N + 1):
        if not f(m):
            continue
        c = cm[m]
        if c == 0:
            continue
        for n in range(int(V) + 1, N // m + 1):
            if lam[n] and f(n):
                SII += c * lam[n] * e(alpha * m * n) * eta2(m * n / x)
    S0inf = sum(lam[n] * e(alpha * n) * f(n) * eta2(n / x) for n in range(1, int(V) + 1))
    S0v_printed = sum(lam[n] * e(alpha * n) * eta2(n / x) for n in range(1, v + 1) if v % n == 0)
    S0v_full = sum(lam[n] * e(alpha * n) * eta2(n / x) for n in range(1, N + 1)
                   if math.gcd(n, v) > 1)
    core = SI1 - SI2 + SII + S0inf
    gap_printed = abs(S - core - S0v_printed)
    gap_full = abs(S - core - S0v_full)
    return S, core, S0v_printed, S0v_full, gap_printed, gap_full


def main():
    v = 2
    ok = True
    for (x, alpha, U, V) in [(100, 0.0, 5, 7), (100, 0.1234, 5, 7), (1000, 0.3, 10, 10),
                             (5000, 0.01, 20, 20)]:
        S, core, p, full, gp, gf = check(x, alpha, U, V, v)
        print(f"x={x} alpha={alpha} U={U} V={V}: S_eta={S.real:.10f}{S.imag:+.10f}i")
        print(f"   core S_I1-S_I2+S_II+S_0inf = {core.real:.10f}{core.imag:+.10f}i")
        print(f"   printed S_0,2 = {p.real:.3e}, |S - core - printed S_0,2| = {gp:.6f}")
        print(f"   sum over (n,2)>1 = {full.real:.6f}{full.imag:+.6f}i, "
              f"|S - core - that| = {gf:.2e}")
        ok = ok and gp > 1e-3 and gf < 1e-9
    x = 2.16e20
    big = sum(LOG2 * eta2(2.0 ** k / x) for k in range(1, 80))
    printed_big = LOG2 * eta2(2.0 / x)
    print(f"x=2.16e20, alpha=0: sum_k log2*eta2(2^k/x) = {big:.6f} "
          f"(4(log 2)^2 = {4 * LOG2 ** 2:.6f}); printed S_0,2 = {printed_big}")
    ok = ok and abs(big - 4 * LOG2 ** 2) < 1e-9 and printed_big == 0.0
    if ok:
        print("CONFIRMED: with the printed S_{0,v} = sum_{n|v}, (3.11) misses the prime powers "
              "2^k, k >= 2 (e.g. 4(log 2)^2 = 1.9218 at alpha = 0), and holds with the sum over "
              "(n,v) > 1.")
    else:
        print("NOT CONFIRMED: the computed gaps do not match the claimed error in (3.11).")


if __name__ == "__main__":
    main()
