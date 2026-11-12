"""Check of [H, Proposition 9.5.1] (the bound (9.73) for sum Lambda(n) log n eta_+^2(n/x)).

Claim: the proof does not establish the e^{-pi T1/4} part of (9.73).  The tail
step (9.90) loses a factor 2 (Lemma 9.1.3 counts only Im(rho) > T0, f bounds one
zero, no pairing) and uses Lemma 9.1.3's false decreasing clause (missing the
boundary term f(T0)g(T0), g(T0) = 0.5 log T0 + 17.7).  With both repaired the
tail is about 17.5 times the first line of (9.73) at H = 200, T0 = 450 and about
37 times at H = 25, T0 = 200; the factor 2 alone already exceeds it at H = 25,
T0 = 200 (x1.24); even the exact zero sum of f over both half-planes exceeds it
at H = 200, T0 = 450 (x1.07).  The 8.39 of (9.91) is harmless; the E2 form of
Prop 7.1.5 ((9.95), (9.96)) is unaffected.

Book inputs (expform.tex):
  - l.1712-1731 Prop 9.5.1: H >= 25, x >= 10^8, T0 >= max(2H+25, 200); (9.73).
  - l.528-543, 583-595 Lemma 9.1.3 (9.24) and its decreasing clause.
  - l.1960-1972 (9.89): f(T) = 8.45 (log x + (1/2)log T)(T/2 - H) e^{-pi(T-2H)/4}.
  - l.1978-1984 (9.90); l.1985-1995 (9.91) with 8.39/(4 pi).
  - l.2277-2290 (9.93): H = 200, T0 = 450, x >= 10^12, 5.123e-15;
    l.2327-2338 (9.95)-(9.96): 1.95e-6 and 5.3e-7 absorbed into 2e-6.
The tail sum sum_{|Im rho|>T0}|M eta(rho)| must be at most (first line of (9.73)) * log x.
Zeros of zeta from mpmath.zetazero.

Confirms if: 2*RHS(9.90) exceeds first line*log x at H = 25, T0 = 200 for all
tested x; the repaired bound exceeds it at both parameter sets by > 10; the
two-sided zero sum of f exceeds it at H = 200, T0 = 450, x = 1e12; and the E2
total stays <= 2e-6.

Run: PYTHONPATH=<mpmath dir> python3 -s proposition_9_5_1.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 25
pi = mp.pi


def f_book(T, x, H):
    return 8.45 * (mp.log(x) + mp.log(T) / 2) * (T / 2 - H) * mp.exp(-pi * (T - 2 * H) / 4)


def dens(T):
    return mp.log(T / (2 * pi)) / (2 * pi) + 1 / (4 * T)


def g(T):
    return mp.log(T) / 2 + mp.mpf("17.7")


def rhs990(x, H, T0):
    return mp.quad(lambda T: f_book(T, x, H) * dens(T), [T0, T0 + 20, T0 + 60, T0 + 200, mp.inf])


def FL(x, H, T0):  # first line of (9.73) times log x
    T1 = T0 - 2 * H
    L = mp.log(x)
    l1 = mp.log(T1)
    return ((0.462 * l1 ** 2 / L + 0.909 * l1) * T1 + 1.71 * (1 + l1 / L) * H) * mp.exp(-pi * T1 / 4) * L


ok = True
print("factor-2 and repaired tail versus the first line of (9.73):")
res = {}
for (H, T0) in ((25, 200), (200, 450)):
    for e in (8, 12, 27, 100):
        x = mp.mpf(10) ** e
        R = rhs990(x, H, T0)
        F = FL(x, H, T0)
        rep = 2 * (R + f_book(T0, x, H) * g(T0))
        r2, rr = 2 * R / F, rep / F
        res[(H, T0, e)] = (r2, rr)
        print("  H=%d T0=%d x=1e%d: RHS(9.90)/FL=%s  2RHS/FL=%s  2(RHS+f(T0)g(T0))/FL=%s"
              % (H, T0, e, mp.nstr(R / F, 5), mp.nstr(r2, 5), mp.nstr(rr, 5)))
        if H == 25 and r2 <= 1:
            ok = False
        if rr <= 10:
            ok = False

# actual zeros above 450, both half-planes (conjugate symmetry for zeta)
H, T0 = 200, 450
n0 = 235
assert mp.im(mp.zetazero(n0)) < T0 < mp.im(mp.zetazero(n0 + 1))
zs, k = [], n0 + 1
while True:
    t = mp.im(mp.zetazero(k))
    if t > T0 + 80:
        break
    zs.append(t)
    k += 1
x = mp.mpf(10) ** 12
two = 2 * mp.fsum(f_book(z, x, H) for z in zs)
rz = two / FL(x, H, T0)
print("H=200 T0=450 x=1e12: 2*sum_{gamma>450} f(gamma) / (first line*log x) = %s  (%d zeros up to %s)"
      % (mp.nstr(rz, 5), len(zs), mp.nstr(zs[-1], 6)))
ok = ok and rz > 1

# 8.39 in (9.91): pointwise 8.45*dens(T) <= (8.39/2pi) log T on [200, e^258]
def gap(lt):
    T = mp.e ** lt
    return 8.45 * dens(T) - 8.39 / (2 * pi) * lt
cross = mp.findroot(gap, 258)
pw = all(gap(mp.log(T)) < 0 for T in (200, 450, 10 ** 4, 10 ** 50)) and gap(mp.log(200)) < 0
print("8.45*dens(T) <= (8.39/2pi) log T for 200 <= T <= e^%s: %s" % (mp.nstr(cross, 6), pw))

# E2 form: (9.95)-(9.96) with the repaired tail at x = 1e12
L = mp.log(10 ** 12)
rep450 = 2 * (rhs990(x, 200, 450) + f_book(450, x, 200) * g(450)) / L
tot = mp.mpf("1.95e-6") + mp.mpf("5.3e-7") / L + rep450
print("repaired (9.93) first part per log x = %s (printed 5.123e-15); E2 total %s <= 2e-6: %s"
      % (mp.nstr(rep450, 4), mp.nstr(tot, 6), tot <= 2e-6))
ok = ok and pw and tot <= 2e-6 and rep450 > mp.mpf("5.123e-15")

if ok:
    print("CONFIRMED: repairing (9.90) makes the tail %s x the e^{-pi T1/4} part of (9.73) at H=200, T0=450 and %s x at H=25, T0=200 (factor 2 alone: %s x), and the two-sided zero sum of f is already %s x it, so (9.73) and 5.123e-15 are not established while the E2 form survives."
          % (mp.nstr(res[(200, 450, 12)][1], 3), mp.nstr(res[(25, 200, 8)][1], 3), mp.nstr(res[(25, 200, 8)][0], 3), mp.nstr(rz, 3)))
else:
    print("NOT CONFIRMED: the repaired tail does not exceed the first line of (9.73) as claimed.")
