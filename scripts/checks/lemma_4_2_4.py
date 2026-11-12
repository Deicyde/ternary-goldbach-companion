"""Check of [H, Lemma 4.2.4] (lem:bogus): the constant c_1 and the slips after (4.53).

Claim: the statement sets c_1 = 1 + |eta'|_1/(2x/D) (Lemma 4.2.1's all-n value),
but the proof bounds T_{m,o} by (4.36), whose first entry x/2m + |eta'|_1/2
needs c_1 = 1 + |eta'|_1/(x/D); Ch. 6 (Sec. 6.3.2) uses the printed form
(1.000189) where 1.000378 is needed. Also, after (4.53) the u-ranges
min(U, M/V) and min(U/q, M/Vq) should be min(U, M/v) and min(U/q, M/(vq)), and
the final '(v,q)=1' in the display bounding sum log p/(p^a/(q,p^a)) should be
'(v,q)>1'.

Book inputs:
  - typeI.tex:1538  c_1 = 1 + |eta'|_1/(2x/D), D = UV; typeI.tex:1507
    UV + (19/18)Q_0 <= x/5.6; typeI.tex:1499 Q_0 >= max(2e, 2 sqrt x).
  - typeI.tex:1114-1121  (4.36) first entry x/(2m) + |eta'|_1/2 and
    A = (x/2y_1)(1 + |eta'|_1/(x/y_1)); typeI.tex:1675 proof uses (4.36);
    the proof's coefficient 3c_1/2 x/(jq+R) is 3A with A = c_1 x/(2y_1).
  - minarctotals.tex:1825 V = x^{1/3}/3, U = 500 sqrt6 x^{1/3};
    minarctotals.tex:1314 x >= 2.16e20; minarctotals.tex:1936 c_1 = 1.000189;
    |eta_2'|_1 = 8 log 2.
  - typeI.tex:1585-1619  the two displays after (4.53) and the chain
    ending in '(v,q)=1'.

Confirms if: (a) A from (4.36) exceeds the printed c_1 x/(2y_1) for y_1 > D/2
at admissible D/x, and the Sec. 6.3.2 corrected c_1 exceeds 1.000189;
(b) in exact arithmetic the first display after (4.53) holds with M/v and
fails with the printed M/V at some test point, and the second display (with
M/(vq), M/p^a, mu inside the sum) equals the left side; (c) the chain's final
bound with '(v,q)=1' is false at some (q,V) while with '(v,q)>1' it holds and
adding the (v,2q)=1 sum gives exactly log q + sum_{v odd} Lambda(v)/v.

Run: python3 -I lemma_4_2_4.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as Dm, getcontext
from fractions import Fraction as Fr
import math

getcontext().prec = 50
E1 = 8 * Dm(2).ln()  # |eta_2'|_1
ok = True

# ---------------------------------------------------------------- (a) c_1
print("(a) c_1 with |eta'|_1 = 8 log 2")
for x in (Dm(10) ** 9, Dm(10) ** 30):
    D = x / Dm("5.6") - Dm(19) / 18 * 2 * x.sqrt()   # largest admissible D = UV
    c1p = 1 + E1 / (2 * x / D)
    c1c = 1 + E1 / (x / D)
    print(f"   x={float(x):.0e}: D/x={float(D/x):.10f}, printed c1={float(c1p):.7f}, (4.36) needs {float(c1c):.7f}")
    for frac in ("0.5", "0.75", "1"):
        y1 = Dm(frac) * D
        A = x / (2 * y1) + E1 / 2
        Ap = x / (2 * y1) * c1p
        print(f"      y1={frac}D: A(4.36)={float(A):.6f}, printed (x/2y1)c1={float(Ap):.6f}, covers: {Ap >= A}")
        if frac == "1":
            ok &= Ap < A
x13 = Dm(6) * Dm(10) ** 6        # (2.16e20)^(1/3)
UVx = 500 * Dm(6).sqrt() / (3 * x13)
p6 = 1 + E1 * UVx / 2
c6 = 1 + E1 * UVx
print(f"   Sec 6.3.2 at x=2.16e20: UV/x={float(UVx):.6e}; printed form {float(p6):.9f}"
      f" (< 1.000189: {p6 < Dm('1.000189')}); corrected {float(c6):.9f} (< 1.000378: {c6 < Dm('1.000378')})")
ok &= p6 < Dm("1.000189") < c6 < Dm("1.000378")


# ---------------------------------------------------------------- arithmetic
def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def mu(n):
    f = factor(n)
    return 0 if any(e > 1 for e in f.values()) else (-1) ** len(f)


def pp(n):
    """prime p if n = p^a (a >= 1), else None."""
    if n < 2:
        return None
    f = factor(n)
    return next(iter(f)) if len(f) == 1 else None


# exact linear forms sum_p c_p log p, stored as {p: Fraction}
def add(d, p, c):
    if c:
        d[p] = d.get(p, Fr(0)) + c


def same(a, b):
    keys = set(a) | set(b)
    return all(a.get(k, 0) == b.get(k, 0) for k in keys)


def val(d):
    return sum(float(c) * math.log(p) for p, c in d.items())


def musum(lim, cond):
    return sum(Fr(mu(u), u) for u in range(1, math.floor(lim) + 1) if cond(u))


def lhs(q, U, V, M):
    d = {}
    for a in range(1, M + 1):
        if a % 2 == 0 or a % q:
            continue
        for v in range(1, V + 1):
            p = pp(v)
            if p and a % v == 0 and Fr(a, U) <= v:
                add(d, p, Fr(mu(a // v), a))
    return d


def first_display(q, U, V, M, printed):
    d = {}
    for v in range(3, V + 1, 2):
        p = pp(v)
        if not p:
            continue
        lim = min(Fr(U), Fr(M, V) if printed else Fr(M, v))
        g = math.gcd(v, q)
        div = q if g == 1 else q // g
        add(d, p, Fr(1, v) * musum(lim, lambda u: u % 2 and u % div == 0))
    return d


def second_display(q, U, V, M):
    d = {}
    for v in range(3, V + 1, 2):
        p = pp(v)
        if not p:
            continue
        g = math.gcd(q, v)
        if g == 1:
            lim = min(Fr(U, q), Fr(M, v * q))
            add(d, p, Fr(mu(q), q) * Fr(1, v) * musum(lim, lambda u: math.gcd(u, 2 * q) == 1))
        else:
            dd = q // g
            lim = min(Fr(U, dd), Fr(M, v) / dd)
            add(d, p, Fr(mu(dd), q) * Fr(g, v) * musum(lim, lambda u: u % 2 and math.gcd(u, dd) == 1))
    return d


print("\n(b) identity after (4.53), exact")
fail_printed = 0
all_corr = True
for (q, U, V, M) in ((3, 40, 30, 300), (9, 40, 30, 300), (15, 60, 25, 400), (45, 100, 50, 900), (27, 200, 60, 2500)):
    L = lhs(q, U, V, M)
    Rc = first_display(q, U, V, M, False)
    Rp = first_display(q, U, V, M, True)
    R2 = second_display(q, U, V, M)
    ec, ep, e2 = same(L, Rc), same(L, Rp), same(L, R2)
    print(f"   q={q} U={U} V={V} M={M}: LHS={val(L):.9f} M/v:{val(Rc):.9f} ({ec})"
          f" printed M/V:{val(Rp):.9f} ({ep}) 2nd display corrected:{val(R2):.9f} ({e2})")
    all_corr &= ec and e2
    fail_printed += not ep
ok &= all_corr and fail_printed > 0


# ---------------------------------------------------------------- (c) chain ending in (v,q)=1
def Lam_over_v(v):
    p = pp(v)
    return math.log(p) / v if p else 0.0


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


print("\n(c) chain bounding S = sum_{p^a<=V, p odd, p|q} log p/(p^a/(q,p^a))")
printed_fails = 0
corr_ok = True
for (q, V) in ((105, 9), (3, 9), (15015, 169), (3 * 5 * 7 * 11 * 13, 2000)):
    S = sum(math.log(pp(n)) / (n / math.gcd(q, n)) for n in range(3, V + 1, 2) if pp(n) and q % pp(n) == 0)
    fin_p = math.log(q) + sum(Lam_over_v(v) for v in range(3, V + 1, 2) if math.gcd(v, q) == 1)
    fin_c = math.log(q) + sum(Lam_over_v(v) for v in range(3, V + 1, 2) if math.gcd(v, q) > 1)
    s2q = sum(Lam_over_v(v) for v in range(3, V + 1, 2) if math.gcd(v, q) == 1)
    nxt = math.log(q) + sum(Lam_over_v(v) for v in range(3, V + 1, 2))
    # the step before: log q + sum_p (log p) sum_beta 1/p^beta (single log)
    mid = math.log(q) + sum(math.log(p) * sum(p ** -b for b in range(1, 80) if p ** b <= V / p ** vp(q, p))
                            for p in factor(q) if p % 2)
    print(f"   q={q} V={V}: S={S:.4f} mid={mid:.4f} printed '(v,q)=1' bound={fin_p:.4f} (S<=: {S <= fin_p + 1e-12})"
          f" '(v,q)>1' bound={fin_c:.4f} (mid<=: {mid <= fin_c + 1e-12}); sum_(v,2q)=1 + '(v,q)>1' bound"
          f" = {s2q + fin_c:.6f} vs next line {nxt:.6f}")
    printed_fails += S > fin_p + 1e-12
    corr_ok &= S <= mid + 1e-12 and mid <= fin_c + 1e-12 and abs(s2q + fin_c - nxt) < 1e-9
ok &= printed_fails > 0 and corr_ok

if ok:
    print(f"CONFIRMED: (4.36) needs c_1 = 1+|eta'|_1/(x/D), not the printed 1+|eta'|_1/(2x/D) (Sec. 6.3.2: {float(c6):.7f} needed vs 1.000189 used), and the M/V ranges and the '(v,q)=1' after (4.53) are slips for M/v and '(v,q)>1'.")
else:
    print("NOT CONFIRMED: some part of the Lemma 4.2.4 claim did not reproduce.")
