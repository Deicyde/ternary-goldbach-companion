"""Check of [H, Lemma 9.1.3] (lem:garmola), closing clause for real decreasing f.

Claim: for real decreasing f the book says the error term (second line of
(9.24)) is O*((1/4) int_y^oo f(T)/T dT); this is false, because
f(y)g(y) - int_y^oo f'(T)g(T)dT = 2f(y)g(y) + int_y^oo f g' (not 0.5 int f/T),
so the error is only O*(f(y)g(y) + (1/4) int f/T). Also (9.24) itself fails for
piecewise C^1 f with jumps (jumps are not counted in int |f'| g).

Book inputs (expform.tex):
  - l.522-543: Lemma 9.1.3, (9.24) main term (1/2pi) int_y^oo f(T) log(qT/2pi) dT,
    error (1/2) O*(|f(y)|g(y) + int |f'| g), g_chi(T) = 0.5 log qT + 17.7 (9.25),
    decreasing clause O*((1/4) int f/T).
  - l.585-594: the proof's identity f(y)g(y) - int f'g = 0.5 int f/T.
Test case: zeta (q = 1, chi trivial), zeros from mpmath.zetazero.
  (a) y = 14.13, f(t) = exp(-10(t - 14.13)): real, decreasing, C^1.
  (b) f = 1 on [14,15], 0 elsewhere (piecewise C^1 with jumps), y = 1.

Confirms if: in (a) |sum - main| exceeds (1/4) int f/T while it is within
the general bound (1/2)(f(y)g(y) + int |f'|g), and the proof's identity is
numerically false; and in (b) |sum - main| exceeds the (9.24) error term.

Run: PYTHONPATH=<mpmath dir> python3 -s lemma_9_1_3.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
q = 1
g = lambda T: 0.5 * mp.log(q * T) + 17.7
main = lambda f, a, b: mp.quad(lambda T: f(T) * mp.log(q * T / (2 * mp.pi)), [a, b]) / (2 * mp.pi)

zeros = []
n = 1
while True:
    t = mp.zetazero(n).imag
    zeros.append(t)
    if t > 30:
        break
    n += 1

# (a) decreasing f
y = mp.mpf("14.13")
f = lambda t: mp.e ** (-10 * (t - y))
fp = lambda t: -10 * mp.e ** (-10 * (t - y))
S = mp.fsum(f(t) for t in zeros if t > y)
M = main(f, y, mp.inf)
err = abs(S - M)
quarter = mp.quad(lambda T: f(T) / T, [y, mp.inf]) / 4
general = (abs(f(y)) * g(y) + mp.quad(lambda T: abs(fp(T)) * g(T), [y, mp.inf])) / 2
lhs_id = f(y) * g(y) - mp.quad(lambda T: fp(T) * g(T), [y, mp.inf])
rhs_id_book = 0.5 * mp.quad(lambda T: f(T) / T, [y, mp.inf])
rhs_id_true = 2 * f(y) * g(y) + mp.quad(lambda T: f(T) * 0.5 / T, [y, mp.inf])
print("(a) zeta, y = 14.13, f(t) = exp(-10(t-14.13))")
print("    sum_{gamma>y} f(gamma)          =", mp.nstr(S, 8))
print("    main term (1/2pi) int f log    =", mp.nstr(M, 8))
print("    |sum - main|                   =", mp.nstr(err, 8))
print("    book decreasing clause (1/4)int f/T =", mp.nstr(quarter, 8))
print("    general bound (1/2)(f g + int|f'|g)  =", mp.nstr(general, 8))
print("    proof identity: f(y)g(y) - int f'g =", mp.nstr(lhs_id, 10),
      " book says", mp.nstr(rhs_id_book, 8), " true 2fg + int f g' =", mp.nstr(rhs_id_true, 10))
a_ok = err > quarter and err <= general and abs(lhs_id - rhs_id_book) > 1 and abs(lhs_id - rhs_id_true) < 1e-15

# (b) f with jumps
yb = 1
Sb = sum(1 for t in zeros if 14 <= t <= 15)
Mb = main(lambda T: 1, 14, 15)
err_b = abs(Sb - Mb)
bound_b = 0  # f(y) = 0 and f' = 0 off the jumps
print("(b) zeta, y = 1, f = 1_[14,15]")
print("    sum =", Sb, " main =", mp.nstr(Mb, 6), " |sum-main| =", mp.nstr(err_b, 6),
      " (9.24) error term =", bound_b)
b_ok = err_b > bound_b + 0.5

if a_ok and b_ok:
    print("CONFIRMED: for zeta with f(t)=exp(-10(t-14.13)), |sum-main| = %s exceeds the decreasing-f bound %s "
          "(the proof drops 2f(y)g(y)), and for f = 1 on [14,15] (9.24) predicts error 0 but the error is %s."
          % (mp.nstr(err, 4), mp.nstr(quarter, 3), mp.nstr(err_b, 4)))
else:
    print("NOT CONFIRMED: the decreasing-f clause or (9.24) with jumps held in the tested cases.")
