"""Check of [H, (5.31)] (bound 0.36393 / 0.37273 on the triple sum for S >= 100000).

Item: Eq 5.31 (eq:corto, typeII.tex:777-782; proof typeII.tex:715-775).

Claim: in the proof, the term coming from the bound c_{v,5}/sqrt(x), x >= 10^10,
is printed and used as (2-sqrt2) c_{v,5}/10^5 for both v; for v = 1 the sum
runs over all s < S/10^10 and sum_{s<X} s^{-1/2} -> 2 sqrt X, so the term should
be 2(2-sqrt2) c_{1,5}/10^5, raising the v = 1 total to 0.3639231 <= 0.36393;
for v = 2 (odd s) sum_{s odd < X} s^{-1/2} <= sqrt X and the printed term is
valid; and the '=' between sum_{s<S/10^10} 1/(s log^2(S/2s)) and
int_0^{2/10^10} dt/(t log^2 t) should be '<='.  (5.31) survives.

Book inputs: g_v(x) = sum_{r1,r2<=x, (r1,r2)=1, (r1 r2,v)=1}
mu(r1)mu(r2)/(sigma(r1)sigma(r2)) (Lemma 5.1.2, typeII.tex:393-399); the
constants c_{v,0..5} (typeII.tex:711-722); the decomposition and error terms
(typeII.tex:723-760); C_0 = 10000 and the printed values 0.0006506, 0.009525,
0.00009923, 0.000853636, 0.362482, 0.360576, 6204066.5, 15911340.1,
0.00006931, 0.00017328 (typeII.tex:762-775).  Lemma 5.1.2's constants are
taken as printed.

Computation: g_v(m) for m <= 10^4 (float, exact incremental formula), the
main term and the c_{v,0} sum; the c_{v,5} term (2-sqrt2) c_{v,5} S^{-1/2}
sum_{s<X,(s,v)=1} s^{-1/2} for X = S/10^10 up to 10^6 and its supremum; the
totals at S = 10^5 with the printed and with the corrected term; the Riemann
sum against the integral.

Confirms the claim if: the v=1 c_5 term exceeds the printed value for large X
and tends to twice it, the v=2 one stays below the printed value, the
corrected v=1 total is still <= 0.36393, the v=2 total is <= 0.37273, and the
sum is strictly below the integral.

Run: python3 -I eq_5_31.py

Ported from a 2026-11-06 check script.
"""
import math

N = 10000
# sieve mu, sigma
mu = [1] * (N + 1)
mu[0] = 0
comp = [False] * (N + 1)
primes = []
for i in range(2, N + 1):
    if not comp[i]:
        primes.append(i)
        mu[i] = -1
    for p in primes:
        if i * p > N:
            break
        comp[i * p] = True
        if i % p == 0:
            mu[i * p] = 0
            break
        mu[i * p] = -mu[i]
sig = [0] * (N + 1)
for d in range(1, N + 1):
    for k in range(d, N + 1, d):
        sig[k] += d
sqdivs = [[] for _ in range(N + 1)]
for d in range(1, N + 1):
    if mu[d]:
        for k in range(d, N + 1, d):
            sqdivs[k].append(d)


def gvals(v):
    """g_v(m), m <= N.  g(m) - g(m-1) = 2 b_m sum_{r<m,(r,m)=1} b_r + [m=1] b_1^2,
    with b_r = mu(r)/sigma(r) for (r,v)=1; the coprime sum is sum_{d|m} mu(d) B[d]."""
    b = [0.0] * (N + 1)
    for r in range(1, N + 1):
        if mu[r] and math.gcd(r, v) == 1:
            b[r] = mu[r] / sig[r]
    B = [0.0] * (N + 1)
    g = [0.0] * (N + 1)
    cur = 0.0
    for m in range(1, N + 1):
        if b[m]:
            for d in sqdivs[m]:
                cur += mu[d] * (2 * B[d] * b[m] + b[m] * b[m])
                B[d] += b[m]
        g[m] = cur
    return g


def brute_g(v, x):
    return sum(mu[a] * mu[c] / (sig[a] * sig[c]) for a in range(1, x + 1) for c in range(1, x + 1)
               if math.gcd(a, c) == 1 and math.gcd(a * c, v) == 1)


c = {1: dict(c0=1 / 6, c1=1.0, c2=55.768, c3=111.536, c4=0.0044325, c5=0.1079),
     2: dict(c0=1 / 3, c1=2.5, c2=817.168, c3=1634.34, c4=0.038128, c5=0.2046)}
printed_mid = {1: 0.0006506, 2: 0.009525}
bound = {1: 0.36393, 2: 0.37273}
C0 = 10000
S = 1e5
k = 2 - math.sqrt(2)

ok = True
for v in (1, 2):
    g = gvals(v)
    for x in (1, 2, 3, 6, 10, 30):
        assert abs(g[x] - brute_g(v, x)) < 1e-12
    cv = c[v]
    phi_v = 1 if v == 1 else 1
    main = phi_v / (2 * v) * sum(g[m] * math.log1p(1 / m) for m in range(1, C0 + 1))
    c0sum = cv['c0'] * sum(abs(g[m]) * (5 * m * m + 2 * m + 1) for m in range(1, C0 + 1))
    t1 = cv['c1'] * math.log(2) / C0
    mid_no5 = math.log(2) / 1e6 * (cv['c3'] + cv['c2'] * (1 + math.log(1e6)))
    t5_printed = k * cv['c5'] / 1e5
    t4 = cv['c4'] / 2 / math.log(1e10 / 2)
    # c_5 term: k c5 S^{-1/2} sum_{s<X,(s,v)=1} s^{-1/2}, S = 10^10 X; coefficient of c5/10^5 is
    # k X^{-1/2} sum_{s<X} s^{-1/2}.  The sum is constant on (n, n+1], so the sup over X in (n, n+1]
    # of this coefficient is approached at X -> n+ (sum over s <= n).
    acc, worst, worstX = 0.0, 0.0, None
    samples = {}
    for n in range(1, 10**6 + 1):
        if v == 1 or n % 2 == 1:
            acc += n ** -0.5
        coef = k * acc / math.sqrt(n)
        if coef > worst:
            worst, worstX = coef, n
        if n in (10, 100, 10**4, 10**5, 10**6):
            samples[n] = coef
    limit = 2 * k if v == 1 else k
    t5_needed = worst * cv['c5'] / 1e5           # sup over X <= 10^6
    t5_limit = limit * cv['c5'] / 1e5            # sup over all X (limit; sums stay below it)
    t5_use = max(t5_needed, t5_limit, t5_printed) if v == 1 else max(t5_needed, t5_printed)
    total_printed = main + c0sum / S**2 + t1 + mid_no5 + t5_printed + t4
    total_corr = main + c0sum / S**2 + t1 + mid_no5 + t5_use + t4
    print(f"v={v}: main={main:.7f}  c_v0 sum={c0sum:.1f}  c1 term={t1:.8f}  c4 term={t4:.8f}")
    print(f"      mid term with printed c5 piece = {mid_no5 + t5_printed:.7f} (book prints {printed_mid[v]})")
    print(f"      c5 piece coefficient k X^-1/2 sum_(s<X,(s,v)=1) s^-1/2 at X=" +
          ", ".join(f"{n}: {samples[n]:.5f}" for n in sorted(samples)) +
          f"; sup on X<=1e6 = {worst:.5f} at X={worstX}; printed coefficient {k:.5f}; limit {limit:.5f}")
    print(f"      c5 piece: printed {t5_printed:.4e}, needed (sup) {t5_use:.4e}")
    print(f"      total at S=1e5: printed term {total_printed:.7f}; corrected {total_corr:.7f}; bound {bound[v]}")
    if v == 1:
        ok &= samples[10**6] > k and abs(samples[10**6] - 2 * k) < 0.01 and total_corr <= bound[1]
        ok &= abs((mid_no5 + t5_use) - 0.0006513) < 5e-8
    else:
        ok &= worst <= k and total_corr <= bound[2]

# Riemann sum vs integral: sum_{s<X} 1/(s log^2(S/2s)) vs 1/log(10^10/2), S = 10^10 X
integral = 1 / math.log(1e10 / 2)
for X in (10, 1000, 10**5):
    Sb = 1e10 * X
    rs = sum(1 / (s * math.log(Sb / (2 * s)) ** 2) for s in range(1, X))
    print(f"X={X}: sum_(s<X) 1/(s log^2(S/2s)) = {rs:.10e}  integral = {integral:.10e}  strict '<': {rs < integral}")
    ok &= rs < integral

if ok:
    print("CONFIRMED: for v=1 the x>=10^10 term in the proof of (5.31) must be 2(2-sqrt2)c_{1,5}/10^5, not the printed "
          "(2-sqrt2)c_{1,5}/10^5, which raises the v=1 total to 0.3639231 <= 0.36393; the v=2 term is valid, the "
          "sum-integral '=' is a '<=', and (5.31) survives for both v.")
else:
    print("NOT CONFIRMED: the recomputed terms do not match the claim.")
