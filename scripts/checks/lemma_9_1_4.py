"""Check of [H, Lemma 9.1.4] (lem:hausierer), Cauchy-Schwarz step for int |f'| g_chi.

Claim: the Cauchy-Schwarz bound int_1^oo |f'| g_chi <= sqrt((1/2pi) int_R |f'|^2)
* sqrt((1/pi) int_1^{T0} g_chi^2) is wrong: with (1/2pi) int_R |G'|^2 = |eta log|_2^2
(the book prints |eta log|_2, missing a square) it gives |eta log|_2 sqrt((1/pi) int g^2),
which needs int_1^{T0} |f'|^2 <= |eta log|_2^2 / pi; the summing step uses
|eta log|_2 sqrt(int g^2), needing int_1^{T0}|f'|^2 <= |eta log|_2^2. Both fail.
Also sqrt((log(qT0/2pi e))^2 + 1) <= log(qT0/2pi e) + 1/2 needs qT0 >= 2 pi e^{7/4} = 36.2.

Book inputs (expform.tex):
  - l.670-673: f(t) = |G_delta(1/2+it)| for t <= T0, else 0.
  - l.536-538 (9.25): g_chi(T) = 0.5 log qT + 17.7.
  - l.708-718: the Cauchy-Schwarz display and (1/2pi) int |f'|^2 = |eta(t) log t|_2.
  - l.726-736: the summing step with (log(qT0/2pi e) + 1/2)|eta|_2 + (log(qT0)/2 + 17.21)|eta log|_2.
Test: eta(t) = t^2 e^{-t^2/2}, delta = 0, q = 1, T0 = 10. Then
G_0(s) = 2^{s/2} Gamma(s/2+1), G_0'(s) = G_0(s)(log 2 + psi(s/2+1))/2, and
|eta log|_2^2 = int_0^oo t^4 e^{-t^2} (log t)^2 dt.

Confirms if: int_1^{T0}|f'| g exceeds the displayed bound, int_1^{T0}|f'|^2
exceeds |eta log|_2^2, Plancherel gives (1/2pi) int_R |G'|^2 = |eta log|_2^2,
and the sqrt(x^2+1) <= x + 1/2 step fails for some qT0 < 36.2.

Run: PYTHONPATH=<mpmath dir> python3 -s lemma_9_1_4.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 20
q, T0 = 1, mp.mpf(10)
G = lambda s: 2 ** (s / 2) * mp.gamma(s / 2 + 1)
Gp = lambda s: G(s) * (mp.log(2) + mp.digamma(s / 2 + 1)) / 2
g = lambda T: 0.5 * mp.log(q * T) + 17.7


def fprime(T):  # d/dT |G(1/2+iT)|
    s = mp.mpf(0.5) + 1j * T
    gv = G(s)
    return mp.re(mp.conj(gv) * 1j * Gp(s)) / abs(gv)


etalog2 = mp.quad(lambda t: t ** 4 * mp.e ** (-t ** 2) * mp.log(t) ** 2, [0, 1, mp.inf])
planch = mp.quad(lambda T: abs(Gp(mp.mpf(0.5) + 1j * T)) ** 2, [-mp.inf, -10, 0, 10, mp.inf]) / (2 * mp.pi)
nodes = mp.linspace(1, T0, 10)
A = mp.quad(lambda T: abs(fprime(T)) * g(T), nodes)
B = mp.quad(lambda T: fprime(T) ** 2, nodes)
g2 = mp.quad(lambda T: g(T) ** 2, [1, T0])
disp = mp.sqrt(etalog2) * mp.sqrt(g2 / mp.pi)
summ = mp.sqrt(etalog2) * mp.sqrt(g2)
print("|eta log|_2^2 =", mp.nstr(etalog2, 8), "; Plancherel (1/2pi) int_R |G'(1/2+iT)|^2 dT =", mp.nstr(planch, 8))
print("int_1^T0 |f'| g      =", mp.nstr(A, 6))
print("displayed bound |eta log|_2 sqrt((1/pi) int g^2) =", mp.nstr(disp, 6))
print("summing-step bound |eta log|_2 sqrt(int g^2)     =", mp.nstr(summ, 6))
print("int_1^T0 |f'|^2 =", mp.nstr(B, 6), " vs |eta log|_2^2 =", mp.nstr(etalog2, 6),
      " and pi |eta log|_2^2 =", mp.nstr(mp.pi * etalog2, 6))
x = lambda Q: mp.log(Q / (2 * mp.pi * mp.e))
thr = 2 * mp.pi * mp.e ** mp.mpf(1.75)
Qt = mp.mpf(30)
print("sqrt(x^2+1) <= x+1/2 with x = log(qT0/2pi e): threshold qT0 =", mp.nstr(thr, 6),
      "; at qT0 = 30:", mp.nstr(mp.sqrt(x(Qt) ** 2 + 1), 6), "vs", mp.nstr(x(Qt) + 0.5, 6))

ok = (A > disp and B > etalog2 and abs(planch - etalog2) < 1e-10
      and mp.sqrt(x(Qt) ** 2 + 1) > x(Qt) + 0.5)
if ok:
    print("CONFIRMED: for eta = t^2 e^{-t^2/2}, q = 1, T0 = 10, int_1^T0 |f'| g_chi = %s exceeds the displayed "
          "Cauchy-Schwarz bound %s, and int_1^T0 |f'|^2 = %s > |eta log|_2^2 = %s." % (
              mp.nstr(A, 4), mp.nstr(disp, 4), mp.nstr(B, 3), mp.nstr(etalog2, 4)))
else:
    print("NOT CONFIRMED: the Cauchy-Schwarz step of Lemma 9.1.4 held in the tested case.")
