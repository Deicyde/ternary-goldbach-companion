"""Check of [H, Eq (13.34)] (eq:cymba, the definition of f_1(r_0)).

Claim: f_1's last term must bound int_{r_0}^inf L_{2r} r^-2 dr, with
L_{2r} = F(r)(13/4 log 2r + 7.82) + 13.66 log 2r + 37.55 (F = digamma).  The
book's own bounds for int F/r^2 and int F log r/r^2 (both via J_{r_0}) give the
constants 13/4 log 2 + 7.82 = 10.073 and 13.66 log 2 + 37.55 = 47.018; the book
prints 11.07 and 37.55, dropping 13.66 log 2.  At r_0 = 1.5e5 the printed term
(3.40353e-3) is below the integral (3.41256e-3).  With the derived constants
f_1 = 0.0169333 (printed 0.0169073), but the exact integral of all f_1 pieces is
0.0168732 < 0.0169073, so the printed value still bounds what it must.

Book inputs:
  - optcoor.tex:237-247    (11.13) g_x(r) = ((R log 2r + 0.5) sqrt(F(r)) + 2.5)/sqrt(2r) + L_{2r}/r + ...;
                           L_t = F(t/2)(13/4 log t + 7.82) + 13.66 log t + 37.55
  - conclusion.tex:598     F(r) = e^gamma log log r + 2.50637/log log r
  - intminarc.tex:523-526  F(r) <= e^gamma log log r + c_gamma, c_gamma = 1.025742, r >= 1e5
  - intminarc.tex:579-585  int F/r^2 <= J/r_0, int F log r/r^2 <= J log(e r_0)/r_0
                           (J = e^gamma(log log r_0 + 1/log r_0) + c_gamma)
  - intminarc.tex:773-786, 817  (13.34) f_1(r_0) = sqrt(F(log r_0))/sqrt(2r_0)(1 + e^gamma/(F(log r_0) log r_0))
                           + 5/sqrt(2r_0) + (1/r_0)((13/4 log e r_0 + 11.07) J_{r_0} + 13.66 log e r_0 + 37.55),
                           J_r = F(log r) + e^gamma/log r, F(t) = e^gamma log t + c_gamma
  - conclusion.tex:778-779 f_1(150000) = 0.0169073...
Confirms if the printed last term is below the quadrature of int_{r_0}^inf L_{2r}/r^2
at r_0 = 1.5e5 while the term with the derived constants is above it, and the
printed f_1 still exceeds the exact integral of all the f_1 pieces.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_13_34.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
eg = mp.exp(mp.euler)
cg = mp.mpf("1.025742")
r0 = mp.mpf(150000)


def Dg(r):
    ll = mp.log(mp.log(r))
    return eg * ll + mp.mpf("2.50637") / ll


F = lambda t: eg * mp.log(t) + cg
lr0 = mp.log(r0)
J = F(lr0) + eg / lr0
print(f"J_r0 = {mp.nstr(J, 6)}")
c1, c2 = 13 * mp.log(2) / 4 + mp.mpf("7.82"), mp.mpf("13.66") * mp.log(2) + mp.mpf("37.55")
print(f"derived constants: 13/4 log 2 + 7.82 = {mp.nstr(c1, 6)} (printed 11.07); 13.66 log 2 + 37.55 = {mp.nstr(c2, 6)} (printed 37.55)")
lere = mp.log(mp.e * r0)
last_p = ((13 * lere / 4 + mp.mpf("11.07")) * J + mp.mpf("13.66") * lere + mp.mpf("37.55")) / r0
last_d = ((13 * lere / 4 + c1) * J + mp.mpf("13.66") * lere + c2) / r0
L2r = lambda r: Dg(r) * (13 * mp.log(2 * r) / 4 + mp.mpf("7.82")) + mp.mpf("13.66") * mp.log(2 * r) + mp.mpf("37.55")
# substitute r = r0 e^u
integ = mp.quad(lambda u: L2r(r0 * mp.exp(u)) / (r0 * mp.exp(u)), [0, 1, 5, 20, 80, mp.inf])
print(f"int_r0^inf L_2r/r^2 dr = {mp.nstr(integ, 6)}; printed term {mp.nstr(last_p, 6)}; derived term {mp.nstr(last_d, 6)}")
head = mp.sqrt(F(lr0)) / mp.sqrt(2 * r0) * (1 + eg / (F(lr0) * lr0)) + 5 / mp.sqrt(2 * r0)
f1p, f1d = head + last_p, head + last_d
print(f"f_1 printed formula = {mp.nstr(f1p, 7)} (book 0.0169073); with derived constants = {mp.nstr(f1d, 7)}")
# exact integral of all the f_1 pieces: int_r0^inf ((0.5 sqrt(F) + 2.5)/sqrt(2r) + L_2r/r) dr/r
ex = mp.quad(lambda u: ((mp.mpf("0.5") * mp.sqrt(Dg(r0 * mp.exp(u))) + mp.mpf("2.5")) / mp.sqrt(2 * r0 * mp.exp(u))
                        + L2r(r0 * mp.exp(u)) / (r0 * mp.exp(u))), [0, 1, 5, 20, 80, mp.inf])
print(f"exact integral of the f_1 pieces = {mp.nstr(ex, 7)}")
ok = last_p < integ < last_d and f1d > mp.mpf("0.0169073") and ex < mp.mpf("0.0169073") and abs(f1p - mp.mpf("0.0169073")) < 1e-7
if ok:
    print(f"CONFIRMED: f_1's last term with the printed 11.07, 37.55 is {mp.nstr(last_p, 6)} < int L_2r/r^2 = {mp.nstr(integ, 6)} (13.66 log 2 is dropped; the derived constants 10.073, 47.018 give f_1 = {mp.nstr(f1d, 6)}), but the printed f_1 = 0.0169073 still exceeds the exact {mp.nstr(ex, 6)}.")
else:
    print("NOT CONFIRMED: the printed last term of f_1 bounds int L_2r/r^2, or the printed f_1 fails.")
