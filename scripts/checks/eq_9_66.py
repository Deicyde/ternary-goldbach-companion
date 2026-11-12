"""Check of [H, (9.66)] (proof of Lemma 9.4.1, via the last clause of Lemma 9.1.3).

Claim: (9.66) is obtained from the decreasing-f clause of Lemma 9.1.3, which is
false: its proof sets f(y)g_chi(y) - int_y^oo f' g_chi equal to 0.5 int f/T,
but integration by parts gives 2 f(y) g_chi(y) + 0.5 int f/T, so the right
side of (9.66) lacks f(T0) g_chi(T0); the step already fails for zeta.

Book inputs (expform.tex):
  - 528-543  Lemma 9.1.3, (9.24) and g_chi(T) = 0.5 log qT + 17.7 (9.25);
             decreasing-f clause: error O*((1/4) int_y^oo f(T)/T dT).
  - 583-589  the identity f(y)g(y) - int f'g = 0.5 int f/T.
  - 1473-1481 Lemma 9.4.1 hypotheses: H >= 25, T0 >= H + max(10 pi|delta|, 50).
  - 1515-1533 g(tau) = kappa_{1,1} sqrt|tau| e^{-0.1598|tau|} + Gaussian term
             (kappa_{1,1} = 4.017), f(tau) = |Mh(ir)|_1/(2 pi) g(tau - H),
             |Mh(ir)|_1 <= 16.193918.
  - 1536-1544 (9.66): sum_{Im rho > T0} f(Im rho) <=
             int_{T0}^oo f(T) ((1/2pi) log(qT/2pi) + 1/(4T)) dT.
Test case: zeta (q = 1), H = 25, T0 = 75, delta -> 0 (the Gaussian term of g
vanishes), so f(T) = 10.35318 sqrt(T-25) e^{-0.1598 (T-25)}, decreasing on
[75, oo). Zeros of zeta from mpmath.zetazero (all on the line, as required).

Confirms if: (a) numerically f(y)g(y) - int f'g = 2 f(y)g(y) + 0.5 int f/T,
not 0.5 int f/T; (b) sum_{gamma > 75} f(gamma) exceeds the right side of
(9.66), while adding f(75) g_chi(75) restores the inequality.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_9_66.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 20
PI = mp.pi
c = mp.mpf("0.1598")
H = mp.mpf(25)
T0 = mp.mpf(75)
q = 1
C = mp.mpf("4.017") * mp.mpf("16.193918") / (2 * PI)
print("constant |Mh|_1 kappa_{1,1}/(2pi) =", mp.nstr(C, 9), "(book: 10.3532)")

f = lambda T: C * mp.sqrt(T - H) * mp.exp(-c * (T - H))
fp = lambda T: mp.diff(f, T)
g = lambda T: mp.mpf("0.5") * mp.log(q * T) + mp.mpf("17.7")

# (a) the identity in the proof of Lemma 9.1.3
lhs_id = f(T0) * g(T0) - mp.quad(lambda T: fp(T) * g(T), [T0, 100, 200, mp.inf])
intf_T = mp.quad(lambda T: f(T) / T, [T0, 100, 200, mp.inf])
print("f(y)g(y) - int f'g          =", mp.nstr(lhs_id, 10))
print("book's value 0.5 int f/T    =", mp.nstr(intf_T / 2, 10))
print("2 f(y)g(y) + 0.5 int f/T    =", mp.nstr(2 * f(T0) * g(T0) + intf_T / 2, 10))
ok_a = abs(lhs_id - (2 * f(T0) * g(T0) + intf_T / 2)) < mp.mpf(10) ** -8 and lhs_id > 100 * intf_T

# (b) zeta zeros above 75
n = 1
while mp.zetazero(n).imag < T0:
    n += 1
print("N(75) =", n - 1)
zs = []
while True:
    gam = mp.zetazero(n).imag
    zs.append(gam)
    n += 1
    if gam > 330:
        break
print("first zeros above 75:", [mp.nstr(z, 10) for z in zs[:6]])
S = mp.fsum(f(z) for z in zs)
# tail beyond the last zero: N(T) - N(330) <= T log T, f tiny
tail = mp.quad(lambda T: -fp(T) * T * mp.log(T), [zs[-1], mp.inf])
print("sum_{75<gamma<=%s} f(gamma) =" % mp.nstr(zs[-1], 6), mp.nstr(S, 8), " tail bound", mp.nstr(tail, 3))
main = mp.quad(lambda T: f(T) * mp.log(q * T / (2 * PI)) / (2 * PI), [T0, 100, 200, mp.inf])
quart = intf_T / 4
rhs = main + quart
bnd = f(T0) * g(T0)
print("main term =", mp.nstr(main, 8), " (1/4) int f/T =", mp.nstr(quart, 6))
print("right side of (9.66) =", mp.nstr(rhs, 8), "; ratio sum/RHS =", mp.nstr(S / rhs, 5))
print("f(75) g_chi(75) =", mp.nstr(f(T0), 6), "*", mp.nstr(g(T0), 8), "=", mp.nstr(bnd, 6))
print("RHS + f(75) g_chi(75) =", mp.nstr(rhs + bnd, 8))
ok_b = S > rhs and S + tail <= rhs + bnd

if ok_a and ok_b:
    print("CONFIRMED: f(y)g(y) - int f'g = 2f(y)g(y) + 0.5 int f/T (%s, not %s), and for zeta at H=25, T0=75, delta->0 the zero sum %s exceeds the right side %s of (9.66), restored by adding f(75)g_chi(75) = %s."
          % (mp.nstr(lhs_id, 6), mp.nstr(intf_T / 2, 4), mp.nstr(S, 5), mp.nstr(rhs, 5), mp.nstr(bnd, 4)))
else:
    print("NOT CONFIRMED: the identity check or the zeta zero sum does not show the missing boundary term in (9.66).")
