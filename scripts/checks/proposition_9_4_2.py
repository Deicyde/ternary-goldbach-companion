"""Check of [H, Prop 9.4.2] (first line of err_{eta+,chi}, (9.70), and its Sec. 9.6 value).

Claim: the first line of (9.70) is Lemma 9.4.1's bound, whose proof does not
establish it for any H: (9.66) drops Lemma 9.1.3's boundary term
f(T0) g_chi(T0); restoring it raises 11.308 to about 28 at Sec. 9.6's heights,
so Sec. 9.6's q-independent constant 1.3482e-14 becomes about 3.5e-14. Even
with the book's (9.66), 11.308 is not justified at H = 25, T0 = 75 (11.37
needed). (The complex-chi pairing and the misprint x^{1/2} for x^{-1/2} in
(9.70) are not numerical.)

Book inputs (expform.tex):
  - 528-543  Lemma 9.1.3, g_chi(T) = 0.5 log qT + 17.7.
  - 1515-1544 g(tau) with kappa_{1,1} = 4.017, kappa_{1,0} = 4.903,
             |Mh(ir)|_1 <= 16.193918, f(tau) = |Mh|_1/(2pi) g(tau - H), (9.66).
  - 1608-1634 Prop 9.4.2, (9.70) first line with 11.308 and 16.147.
  - 2190-2244 Sec. 9.6: H = 200, T0 - H = 250 r/q >= 250,
             (T0-H)/(pi|delta|) >= 19.89436, qT0 <= 1.35e8,
             11.308 sqrt(T0-H)e^{-0.1598(T0-H)} <= 7.9854e-16, first line
             <= log(1.35e8/2pi)(7.9854e-16 + 9.5777e-12/q) <= 1.3482e-14 + ...
Test of the missing term: zeta zeros (mpmath.zetazero) at H = 200,
T0 = 450 (q = 1, delta -> 0, admissible), and the boundary term evaluated
with the book's f at Sec. 9.6's worst case.

Confirms if: the zeta zero sum exceeds (9.66)'s right side at H = 200 (the
boundary term is needed at the book's H); the restored constant is >= 15.49
> 11.308 for every q, H, T0; and Sec. 9.6's q-independent first-line
constant with the term restored is well above 1.3482e-14.

Run: PYTHONPATH=<mpmath dir> python3 -s proposition_9_4_2.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 20
PI = mp.pi
c = mp.mpf("0.1598")
cg = mp.mpf("0.1065")
Mh = mp.mpf("16.193918")
K = mp.mpf("4.017") * Mh / (2 * PI)   # 10.3532
K0 = mp.mpf("4.903") * Mh / (2 * PI)  # 12.6368
g = lambda q, T: mp.mpf("0.5") * mp.log(q * T) + mp.mpf("17.7")

# (a) zeta at H = 200, T0 = 450, delta -> 0
H, T0 = mp.mpf(200), mp.mpf(450)
f = lambda T: K * mp.sqrt(T - H) * mp.exp(-c * (T - H))
n = 1
lo, hi = 1, 400
while lo < hi:  # first zero above 450
    mid = (lo + hi) // 2
    if mp.zetazero(mid).imag > T0:
        hi = mid
    else:
        lo = mid + 1
n = lo
print("N(450) =", n - 1, "; first zeros above 450:", [mp.nstr(mp.zetazero(k).imag, 9) for k in range(n, n + 4)])
S = mp.mpf(0)
while True:
    gam = mp.zetazero(n).imag
    S += f(gam)
    n += 1
    if gam > 650:
        break
rhs = mp.quad(lambda T: f(T) * (mp.log(T / (2 * PI)) / (2 * PI) + 1 / (4 * T)), [T0, T0 + 20, T0 + 100, mp.inf])
bt = f(T0) * g(1, T0)
print("sum_{gamma>450} f(gamma) =", mp.nstr(S, 7), "; right side of (9.66) =", mp.nstr(rhs, 7),
      "; ratio", mp.nstr(S / rhs, 5), "; f(450)g(450) =", mp.nstr(bt, 5))
ok_a = S > rhs and S <= rhs + bt

# (b) universal lower bound for the restored constant, in units sqrt(T0-H)log(qT0/2pi)e^{-c(T0-H)}:
#   first line >= K/(2 pi c) (int_y^oo sqrt(u)e^{-cu} >= sqrt(y)e^{-cy}/c, log(qT/2pi) >= log(qT0/2pi)),
#   boundary = K (0.5 log qT0 + 17.7)/log(qT0/2pi) >= K/2.
lb = K / (2 * PI * c) + K / 2
print("restored constant >= K/(2 pi c) + K/2 =", mp.nstr(lb, 6), "(vs 11.308)")
ok_b = lb > 11.308

# (c) Sec. 9.6, general q: T0 - H >= 250, u0 = (T0-H)/(pi|delta|) >= 250/(4 pi), qT0 <= 1.35e8
book_exp = mp.mpf("11.308") * mp.sqrt(250) * mp.exp(-c * 250)
book_first = mp.log(mp.mpf("1.35e8") / (2 * PI)) * mp.mpf("7.9854e-16")
gmax = mp.mpf("0.5") * mp.log(mp.mpf("1.35e8")) + mp.mpf("17.7")
u0 = mp.mpf(250) / (4 * PI)
add_exp = K * mp.sqrt(250) * mp.exp(-c * 250) * gmax          # sqrt(u)e^{-cu} decreasing for u >= 3.13
add_gau = K0 * (u0 / 2) * mp.exp(-cg * u0 ** 2) * gmax          # u e^{-cg u^2} decreasing for u >= 2.17
print("Sec 9.6: 11.308 sqrt(250) e^{-0.1598*250} =", mp.nstr(book_exp, 6), "(book 7.9854e-16)")
print("Sec 9.6: q-independent first-line constant =", mp.nstr(book_first, 6), "(book 1.3482e-14)")
print("missing f(T0)g_chi(T0): exponential part", mp.nstr(add_exp, 4), "+ Gaussian part", mp.nstr(add_gau, 3))
tot = book_first + add_exp + add_gau
print("restored q-independent constant <=", mp.nstr(tot, 4))
need = (K / (2 * PI) * mp.quad(lambda u: mp.sqrt(u) * mp.exp(-c * u) * mp.log(mp.mpf("1.35e8") / (2 * PI)), [250, 300, mp.inf]) + add_exp) \
    / (mp.sqrt(250) * mp.exp(-c * 250) * mp.log(mp.mpf("1.35e8") / (2 * PI)))
print("restored constant in place of 11.308 at T0-H=250, qT0=1.35e8 (approx.):", mp.nstr(need, 5))
ok_c = add_exp > book_first and tot > 2 * book_first

if ok_a and ok_b and ok_c:
    print("CONFIRMED: for zeta at H=200, T0=450 the zero sum is %s times (9.66)'s right side, the restored constant is >= %s > 11.308 for all q, H, T0, and at Sec. 9.6 the missing term adds %s to the q-independent 1.3482e-14 (total %s)."
          % (mp.nstr(S / rhs, 4), mp.nstr(lb, 4), mp.nstr(add_exp + add_gau, 3), mp.nstr(tot, 3)))
else:
    print("NOT CONFIRMED: the boundary-term computation does not show that the first line of (9.70) is unproved.")
