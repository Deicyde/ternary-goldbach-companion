"""Eq 3.16 ([H], arXiv:1501.05438v2): the case list for F_{3,V} after (3.16).

Claim: for square-free n = p1 p2 p3 (p1 < p2 < p3) with V^3 < n, the book's case list for
F_{3,V}(n) swaps two values.  In fact F_{3,V}(n) = (12 - 6k) log p1 log p2 log p3 with
k = #{i : p_i > V}: it is 6 log p1 log p2 log p3 when p1 < p2 <= V < p3 (the book prints 0)
and 0 when p1 <= V < p2 < p3 (the book prints 6 log p1 log p2 log p3).

Book inputs (book/src/intromin.tex):
  - f_{<=z}, f_{>z} truncations, after (3.6), lines 209-215;
  - (3.15) Lambda log^2 = mu*log^3 - 3((Lambda log)*Lambda_{>V} + (mu*log^2)*Lambda_{<=V})
    + (-Lambda_{>V}*Lambda*Lambda + 2 Lambda_{<=V}*Lambda*Lambda), lines 343-348;
  - (3.16) F_{3,V} = -Lambda_{>V}*Lambda*Lambda + 2 Lambda_{<=V}*Lambda*Lambda, lines 351-353;
  - the printed case list, lines 356-360.

The script computes F_{3,V} by exact Dirichlet convolution (floats) for n <= 3000, checks
identity (3.15) to validate the implementation, and compares F_{3,V}(n) with the printed
case list for every square-free n = p1 p2 p3 with V^3 < n.  The claim is confirmed if
(3.15) holds, the printed list fails exactly in the two middle cases and (12 - 6k) fits all.

Run: python3 -I eq_3_16.py
Ported from a 2026-11-06 check script.
"""
import math

N = 3000


def sieve(N):
    spf = list(range(N + 1))
    for p in range(2, int(N ** 0.5) + 1):
        if spf[p] == p:
            for k in range(p * p, N + 1, p):
                if spf[k] == k:
                    spf[k] = p
    return spf


SPF = sieve(N)


def factor(n):
    out = []
    while n > 1:
        p = SPF[n]
        out.append(p)
        n //= p
    return out


lam = [0.0] * (N + 1)
mu = [0] * (N + 1)
mu[1] = 1
for n in range(2, N + 1):
    fs = factor(n)
    if len(set(fs)) == 1:
        lam[n] = math.log(fs[0])
    mu[n] = 0 if len(set(fs)) < len(fs) else (-1) ** len(fs)


def conv(a, b):
    c = [0.0] * (N + 1)
    for d in range(1, N + 1):
        if a[d]:
            for m in range(1, N // d + 1):
                c[d * m] += a[d] * b[m]
    return c


def main():
    bad_identity = 0.0
    mismatches = {}
    ratios = {}
    for V in (3, 10, 14):
        lle = [lam[n] if n <= V else 0.0 for n in range(N + 1)]
        lgt = [lam[n] if n > V else 0.0 for n in range(N + 1)]
        LL = conv(lam, lam)
        F3 = [-a + 2 * b for a, b in zip(conv(lgt, LL), conv(lle, LL))]
        # validate with (3.15)
        logk = lambda k: [math.log(n) ** k if n >= 1 else 0.0 for n in range(N + 1)]
        mu_f = [float(m) for m in mu]
        rhs1 = conv(mu_f, logk(3))
        lamlog = [lam[n] * math.log(n) if n >= 1 else 0.0 for n in range(N + 1)]
        mulog2 = conv(mu_f, logk(2))
        t2 = [a + b for a, b in zip(conv(lamlog, lgt), conv(mulog2, lle))]
        for n in range(2, N + 1):
            rhs = rhs1[n] - 3 * t2[n] + F3[n]
            bad_identity = max(bad_identity, abs(rhs - lam[n] * math.log(n) ** 2))
        for n in range(V ** 3 + 1, N + 1):
            fs = factor(n)
            if len(fs) != 3 or len(set(fs)) != 3:
                continue
            p1, p2, p3 = sorted(fs)
            L = math.log(p1) * math.log(p2) * math.log(p3)
            k = sum(1 for p in fs if p > V)
            if k == 3:
                printed, case = -6 * L, "all > V"
            elif p1 < p2 <= V < p3:
                printed, case = 0.0, "p1<p2<=V<p3"
            elif p1 <= V < p2 < p3:
                printed, case = 6 * L, "p1<=V<p2<p3"
            else:
                printed, case = 12 * L, "all <= V"
            ratios.setdefault(k, set()).add(round(F3[n] / L, 9))
            mism = abs(F3[n] - printed) > 1e-6
            ent = mismatches.setdefault(case, [0, 0])
            ent[0] += 1
            ent[1] += mism
            if V == 3 and n in (30, 70):
                print(f"V=3, n={n}={p1}*{p2}*{p3}: F_3V = {F3[n]:.4f}, printed {printed:.4f}")
    print(f"max error in identity (3.15), n <= {N}, V in (3,10,14): {bad_identity:.2e}")
    for k in sorted(ratios):
        print(f"k = {k} primes > V: F_3V / (log p1 log p2 log p3) in {sorted(ratios[k])}")
    for case, (cnt, bad) in mismatches.items():
        print(f"case {case}: {cnt} n, printed value wrong for {bad}")
    ok = (bad_identity < 1e-6
          and all(ratios[k] == {12.0 - 6 * k} for k in ratios)
          and mismatches["p1<p2<=V<p3"][1] == mismatches["p1<p2<=V<p3"][0] > 0
          and mismatches["p1<=V<p2<p3"][1] == mismatches["p1<=V<p2<p3"][0] > 0
          and mismatches["all > V"][1] == 0)
    if ok:
        print("CONFIRMED: F_{3,V}(p1p2p3) = (12-6k) log p1 log p2 log p3, so the printed case "
              "list swaps the values 0 and 6 log p1 log p2 log p3 of its two middle cases.")
    else:
        print("NOT CONFIRMED: the computed F_{3,V} does not show the claimed swap.")


if __name__ == "__main__":
    main()
