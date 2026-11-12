"""Check of [H, eq. (9.90)] (tail of the zero sum in the proof of Prop 9.5.1).

Claim: the step (9.90) has two gaps.  (i) It uses the decreasing-f clause of
Lemma 9.1.3, which is false: for decreasing f, f(y)g(y) - int_y^oo f'g equals
2f(y)g(y) + int f g', not 0.5 int f/T, so the error term lacks f(T0)g(T0),
g(T0) = 0.5 log T0 + 17.7.  (ii) Lemma 9.1.3 counts only zeros with
Im(rho) > T0, while (9.90) sums over |Im(rho)| > T0 with f bounding a single
zero (no pairing), so a factor 2 is lost.  Repaired, the tail at H = 200,
T0 = 450 is about 17 times the first line of (9.73).

Book inputs (expform.tex):
  - l.528-543   Lemma 9.1.3 (9.24): sum over Im(rho) > y; g_chi = 0.5 log qT + 17.7;
                decreasing clause O*((1/4) int f/T).
  - l.583-595   the clause's proof: f(y)g(y) - int f'g = 0.5 int f/T.
  - l.1954-1972 (9.89): f(T) = 8.45 (log x + (1/2) log T)(T/2 - H) e^{-pi(T-2H)/4},
                bounding |M eta_{+,2}(rho)| for a single zero with |tau| >= T0.
  - l.1978-1984 (9.90): sum_{|Im rho|>T0} |M eta(rho)| <= int_{T0}^oo f(T)((1/2pi)log(T/2pi)+1/4T) dT.
  - l.1712-1731 (9.73) first line; l.2277-2290: H = 200, T0 = 450, x >= 10^12.
Zeros of zeta are computed with mpmath.zetazero (q = 1, so the zero set is
symmetric under conjugation and sum_{|gamma|>T0} f(|gamma|) = 2 sum_{gamma>T0} f(gamma)).

Confirms if: (a) the integration-by-parts identity gives 2f(y)g(y)+0.5 int f/T
for the book's f, not 0.5 int f/T; (b) sum over actual zeros gamma > 450 of f
exceeds the right side of (9.90) (one half-plane already) and the two-sided sum
exceeds it further; (c) the repaired bound 2(RHS + f(T0)g(T0)) exceeds the
(9.73) first line times log x by a factor > 10 at H = 200, T0 = 450.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_9_90.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
pi = mp.pi


def f_book(T, x, H):
    return 8.45 * (mp.log(x) + mp.log(T) / 2) * (T / 2 - H) * mp.exp(-pi * (T - 2 * H) / 4)


def fprime(T, x, H):
    return mp.diff(lambda t: f_book(t, x, H), T)


def dens(T):
    return mp.log(T / (2 * pi)) / (2 * pi) + 1 / (4 * T)


def g(T):
    return mp.log(T) / 2 + mp.mpf("17.7")


def rhs990(x, H, T0):
    return mp.quad(lambda T: f_book(T, x, H) * dens(T), [T0, T0 + 20, T0 + 60, T0 + 200, mp.inf])


def first_line_times_logx(x, H, T0):
    T1 = T0 - 2 * H
    L = mp.log(x)
    l1 = mp.log(T1)
    return ((0.462 * l1 ** 2 / L + 0.909 * l1) * T1 + 1.71 * (1 + l1 / L) * H) * mp.exp(-pi * T1 / 4) * L


H, T0 = 200, 450
x = mp.mpf(10) ** 12

# (a) integration by parts for the book's f (decreasing on [T0, oo))
fy = f_book(T0, x, H)
lhs = fy * g(T0) - mp.quad(lambda T: fprime(T, x, H) * g(T), [T0, T0 + 20, T0 + 60, T0 + 200])
half = mp.quad(lambda T: f_book(T, x, H) / T, [T0, T0 + 20, T0 + 60, T0 + 200, mp.inf]) / 2
print("(a) f(y)g(y) - int f'g = %s ; book's 0.5 int f/T = %s ; 2f(y)g(y)+0.5 int f/T = %s"
      % (mp.nstr(lhs, 8), mp.nstr(half, 8), mp.nstr(2 * fy * g(T0) + half, 8)))
ok_a = abs(lhs - (2 * fy * g(T0) + half)) < 1e-6 * lhs and lhs > 100 * half

# (b) zeros of zeta above 450
# locate the first zero above T0 (N(450) = 235)
n0 = 230
while mp.im(mp.zetazero(n0)) > T0:
    n0 -= 5
while mp.im(mp.zetazero(n0 + 1)) <= T0:
    n0 += 1
zs = []
k = n0 + 1
while True:
    t = mp.im(mp.zetazero(k))
    if t > T0 + 80:
        break
    zs.append(t)
    k += 1
print("N(450) =", n0, "; first zeros above 450:", [mp.nstr(z, 10) for z in zs[:4]], "; used", len(zs), "zeros up to", mp.nstr(zs[-1], 8))
ok_b = True
for xx in (mp.mpf(10) ** 8, mp.mpf(10) ** 12, mp.mpf(10) ** 27):
    S1 = mp.fsum(f_book(z, xx, H) for z in zs)
    R = rhs990(xx, H, T0)
    FL = first_line_times_logx(xx, H, T0)
    rep = 2 * (R + f_book(T0, xx, H) * g(T0))
    print("x=1e%d: sum_{gamma>450} f = %s, RHS(9.90) = %s, ratio %s; two-sided sum / RHS = %s"
          % (int(mp.nint(mp.log10(xx))), mp.nstr(S1, 6), mp.nstr(R, 6), mp.nstr(S1 / R, 5), mp.nstr(2 * S1 / R, 5)))
    print("        (9.73) first line * log x = %s; 2*sum/that = %s; 2*RHS/that = %s; repaired 2(RHS+f(T0)g(T0)) = %s, /that = %s"
          % (mp.nstr(FL, 6), mp.nstr(2 * S1 / FL, 5), mp.nstr(2 * R / FL, 5), mp.nstr(rep, 6), mp.nstr(rep / FL, 5)))
    if xx == mp.mpf(10) ** 12:
        ok_b = S1 > R
        ratio_rep = rep / FL
        ratio_two = 2 * S1 / FL
ok_c = ratio_rep > 10

print("checks: identity %s, zero sum exceeds RHS %s, repaired/first-line %s" % (ok_a, ok_b, mp.nstr(ratio_rep, 4)))
if ok_a and ok_b and ok_c:
    print("CONFIRMED: Lemma 9.1.3's decreasing clause drops f(T0)g(T0) and (9.90) loses the conjugate zeros: at H=200, T0=450, x=1e12 the actual zeta zeros above 450 give sum f = %s x RHS(9.90), and the repaired bound is %s x the (9.73) first line."
          % (mp.nstr(S1_ratio := (mp.fsum(f_book(z, x, H) for z in zs) / rhs990(x, H, T0)), 4), mp.nstr(ratio_rep, 4)))
else:
    print("NOT CONFIRMED: the identity, zero-sum or repaired-bound computation does not show the gaps in (9.90).")
