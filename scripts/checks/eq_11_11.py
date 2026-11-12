"""Check of [H, Eq (11.11)] (the '+0.5' in g_x, inherited from Thm 3.1.1 via (6.77)).

Claim: (11.11) rests on Theorem 3.1.1, whose '+0.5' comes from the constant
0.49911 in (6.77); there the AM-GM constant is log2/(2 sqrt rho) +
(sqrt rho/2) 0.67506 = 0.81020, but [H] prints
(1/2)(log2/sqrt rho + (sqrt rho/2) 0.67506) = 0.49911, halving the 0.67506 term
twice.  So [H] gives no valid proof of (11.11) with 0.5.

Book inputs:
  - minarctotals.tex:2251-2311 (6.76) sqrt(C_{x,t}(log t + 0.002) + log(4t)/2)
      * sqrt(0.30214 log t + 0.67506), t = delta0 q; AM-GM with parameter rho;
      C_{x,t} = log(1 + log(4t)/(2 log(9x^{1/3}/(2.004 t))));
      rho = A/B at x1 = 1e25, t = 2 q0 = 4e5 (= 3.397962); (6.77) RHS
      0.27125 C (log t + 0.002) + 0.4141 log t + 0.49911;
      R_{x,t} = 0.27125 C_{x,t} + 0.41415.
  - intromin.tex:84-104 Thm 3.1.1 with 'R log delta0 q + 0.5'.
  - optcoor.tex:223-239 (11.11), (11.12): obtained from Thm 3.1.1.

Computes rho, the correct and printed AM-GM constants, the minimum over rho of
the correct constant, and (6.76) against the (6.77) RHS and R log t + 0.5 at
x = 1e25, t = 4e5.  Confirms if the correct constant is 0.81020, the printed
formula gives 0.49911, and (6.76) exceeds both (6.77) and R log t + 0.5 there.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_11_11.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
C = lambda x, t: mp.log(1 + mp.log(4 * t) / (2 * mp.log(9 * mp.cbrt(x) / (mp.mpf("2.004") * t))))
Aa = lambda x, t: C(x, t) * (mp.log(t) + mp.mpf("0.002")) + mp.log(4 * t) / 2
Bb = lambda t: mp.mpf("0.30214") * mp.log(t) + mp.mpf("0.67506")

x1, t1 = mp.mpf(10) ** 25, mp.mpf(4) * 10 ** 5
rho = Aa(x1, t1) / Bb(t1)
sr = mp.sqrt(rho)
print("rho = %s (book 3.397962)" % mp.nstr(rho, 10))
print("1/(2 sqrt rho) = %s (book 0.27125); log t coefficient 1/(4 sqrt rho) + sqrt(rho) 0.30214/2 = %s (book 0.4141)"
      % (mp.nstr(1 / (2 * sr), 7), mp.nstr(1 / (4 * sr) + sr * mp.mpf("0.30214") / 2, 7)))
c_true = mp.log(2) / (2 * sr) + sr / 2 * mp.mpf("0.67506")
c_print = (mp.log(2) / sr + sr / 2 * mp.mpf("0.67506")) / 2
c_min = mp.sqrt(mp.mpf("0.67506") * mp.log(2))
print("constant: correct log2/(2 sqrt rho) + (sqrt rho/2)0.67506 = %s ; printed formula = %s (book 0.49911); min over rho = %s"
      % (mp.nstr(c_true, 6), mp.nstr(c_print, 6), mp.nstr(c_min, 6)))

lhs = mp.sqrt(Aa(x1, t1)) * mp.sqrt(Bb(t1))
rhs = mp.mpf("0.27125") * C(x1, t1) * (mp.log(t1) + mp.mpf("0.002")) + mp.mpf("0.4141") * mp.log(t1) + mp.mpf("0.49911")
R = (mp.mpf("0.27125") * C(x1, t1) + mp.mpf("0.41415")) * mp.log(t1) + mp.mpf("0.5")
print("x = 1e25, t = 4e5: (6.76) = %s ; (6.77) RHS = %s ; R log t + 0.5 = %s" % (mp.nstr(lhs, 8), mp.nstr(rhs, 8), mp.nstr(R, 8)))

if abs(c_true - mp.mpf("0.81020")) < 1e-5 and abs(c_print - mp.mpf("0.49911")) < 1e-5 and lhs > rhs and lhs > R and c_min > mp.mpf("0.5"):
    print("CONFIRMED: the AM-GM constant in (6.77) is %s, not the printed 0.49911 (no rho gives below %s), and at x = 1e25, delta0 q = 4e5 (6.76) = %s exceeds both (6.77) and R log t + 0.5 = %s, so [H] does not prove the '+0.5' that (11.11) inherits." % (mp.nstr(c_true, 6), mp.nstr(c_min, 4), mp.nstr(lhs, 6), mp.nstr(R, 6)))
else:
    print("NOT CONFIRMED: the AM-GM constant or the failure of (6.77) did not reproduce.")
