"""Check of [H, Eq (9.49)] (proof of Lemma 9.3.1).

Claim: (9.49), sum_{Im rho > T0} f(Im rho) <= int_{T0}^oo f(T)((1/2pi) log(qT/2pi)
+ 1/(4T)) dT, is false as printed: it rests on Lemma 9.1.3's decreasing-f
clause, which drops f(T0) g_chi(T0) (g_chi(T) = 0.5 log qT + 17.7); it fails
whenever T0 lies just below a zero.

Book inputs (expform.tex):
  - l.1050: hypothesis T0 >= max(10 pi |delta|, 50).
  - l.1081-1090 (9.48): for |tau| >= (3/2)(pi delta)^2, f(tau) = kappa_{2,1}|tau|e^{-0.1598|tau|},
    kappa_{2,1} = 5.13 (l.1091). With delta = 0 this is f for every tau.
  - l.1099-1103 (9.49); l.536-538 (9.25) g_chi.
Test case: zeta (q = 1), delta = 0, T0 = 52.97 (admissible); zeros from
mpmath.zetazero up to height 400.

Confirms if: at T0 = 52.97 the left side exceeds the right side, while the
right side plus f(T0)g(T0) is larger than the left side.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_9_49.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 25
q, c, k21 = 1, mp.mpf("0.1598"), mp.mpf("5.13")
HMAX = 400
f = lambda T: k21 * T * mp.e ** (-c * T)
g = lambda T: 0.5 * mp.log(q * T) + 17.7

zeros = []
n = 1
while True:
    t = mp.zetazero(n).imag
    if t > HMAX:
        break
    zeros.append(t)
    n += 1
T0 = mp.mpf("52.97")
L = mp.fsum(f(t) for t in zeros if t > T0)
R = mp.quad(lambda T: f(T) * (mp.log(q * T / (2 * mp.pi)) / (2 * mp.pi) + 1 / (4 * T)), [T0, HMAX, mp.inf])
first = [t for t in zeros if t > T0][:6]
print("zeros above T0 (first six):", [mp.nstr(t, 7) for t in first])
print("their contribution:", mp.nstr(mp.fsum(f(t) for t in first), 8))
print("T0 = 52.97: LHS =", mp.nstr(L, 8), " RHS(9.49) =", mp.nstr(R, 8))
B = f(T0) * g(T0)
print("boundary term f(T0)g(T0) =", mp.nstr(B, 6), " RHS + boundary =", mp.nstr(R + B, 6))
L50 = mp.fsum(f(t) for t in zeros if t > 50)
R50 = mp.quad(lambda T: f(T) * (mp.log(q * T / (2 * mp.pi)) / (2 * mp.pi) + 1 / (4 * T)), [50, HMAX, mp.inf])
print("control T0 = 50: LHS =", mp.nstr(L50, 6), " RHS =", mp.nstr(R50, 6))

if L > R and L <= R + B:
    print("CONFIRMED: for zeta at T0 = 52.97 the left side of (9.49) is %s > %s, the right side; adding "
          "f(T0)g(T0) gives %s, which holds." % (mp.nstr(L, 5), mp.nstr(R, 5), mp.nstr(R + B, 4)))
else:
    print("NOT CONFIRMED: (9.49) held at T0 = 52.97 or the repaired bound failed.")
