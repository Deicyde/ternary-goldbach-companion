"""Check of [H, Eq (14.49)] (eq:rozoj, the minor-arc total Z_{r_0} <= 1.00948 x^2/kappa).

Claim (proof gap): the book's argument does not establish 1.00948.  (1) It is
Thm 13.2.1 evaluated with g built on Thm 3.1.1's constant 0.5 (the "+0.5" in
R log 2r + 0.5), which the proof of Thm 3.1.1 does not give: in (6.77) the constant
is log 2/(2 sqrt(rho)) + (sqrt(rho)/2) 0.67506 = 0.81020 at rho = 3.397962, but [H]
writes (1/2)(log 2/sqrt(rho) + (sqrt(rho)/2) 0.67506) = 0.49911.  With 0.8102 the
section 14.3 chain gives about 1.0356.  (2) Thm 13.2.1's l-infinity input is proved
only off the arcs at scale y = x/kappa while its other inputs use scale-x arcs
(a scale mix-up).  The main theorem still holds, but not through the book's argument.
Only (1) is numerical and is checked here; (2) is not numerical.

Book inputs:
  - minarctotals.tex:2257-2288  (6.77): AM-GM with rho; the constant term of (moryo) is
                           (1/(2 sqrt rho)) (log 4)/2 + (sqrt rho/2) 0.67506; printed
                           (1/2)(log 2/sqrt rho + (sqrt rho/2) 0.67506), "<= ... + 0.49911";
                           rho = 3.397962 (line 2272)
  - optcoor.tex:237-239    (11.13) g_x(r) = ((R log 2r + 0.5) sqrt(F(r)) + 2.5)/sqrt(2r) + ...
  - conclusion.tex:597-612 g(r_0) with sqrt(5.42506), 2r_0 = 300000, <= 0.041568
  - conclusion.tex:623-626 (14.37) g(r_0) * 9.2598 x
  - conclusion.tex:680-760 g(r_1) chain: sqrt(F(r_1)) <= sqrt(e^g log log y) - 1.43644/(2 sqrt(e^g log log y)),
                           (14.43) (7/15) g(r_1) S, S <= (0.640209 log x - 0.021095) x, r_1 = (3/8) y^(4/15)
  - intminarc.tex:778-779  f_1's first term sqrt(F(log r_0))/sqrt(2r_0)(1 + e^g/(F(log r_0) log r_0))
                           comes from 0.5 sqrt(F)/sqrt(2r); F(t) = e^g log t + 1.025742
  - conclusion.tex:913-924 (14.45)-(14.47) factor 1.280418; M <= 0.80508 x
  - conclusion.tex:555-559, 523-525, 931-940 T <= 3.5776e-4 x, S_eta*(0,x)E <= 1.0532e-11, (14.49)
  - conclusion.tex:24, 274 kappa = 49, x >= 4.9e26, y >= 1e25; |phi|_1 = sqrt(pi/2)
Method: M is affine in the constant c of "R log 2r + c"; add (c - 0.5) times its
coefficient (from the three places c enters) to the printed M = 0.80508, then redo (14.49).
Confirms if (6.77)'s constant is 0.81020 (not 0.49911) and with it Z exceeds 1.00948.

Run: python3 -I eq_14_49.py

Ported from a 2026-11-06 check script.
"""
import math

rho = 3.397962
sr = math.sqrt(rho)
c_true = math.log(4) / (4 * sr) + sr / 2 * 0.67506
c_book = 0.5 * (math.log(2) / sr + sr / 2 * 0.67506)
print(f"(6.77) constant: log2/(2 sqrt rho) + (sqrt rho/2) 0.67506 = {c_true:.5f}; book's expression = {c_book:.5f} (printed 0.49911)")
eg = math.exp(0.5772156649015329)
y = 1e25
x = 49 * y
r0 = 150000
# coefficient of c in g(r_0) * 9.2598
a1 = 9.2598 * math.sqrt(5.42506) / math.sqrt(300000)
# coefficient of c in (7/15) g(r_1) S / x, maximised over y >= 1e25 on a grid
a2 = 0
for k in range(250, 3001):
    yy = 10 ** (k / 10)
    lly = math.log(math.log(yy))
    sF = math.sqrt(eg * lly) - 1.43644 / (2 * math.sqrt(eg * lly))
    a2 = max(a2, 7 / 15 * sF / math.sqrt(0.75 * yy ** (4 / 15)) * (0.640209 * math.log(49 * yy) - 0.021095))
# coefficient of c in 1.280418 * f_1 (first term is 0.5 * int sqrt(F)/(sqrt 2 r^(3/2)))
lr0 = math.log(r0)
F0 = eg * math.log(lr0) + 1.025742
a3 = 1.280418 * math.sqrt(F0) / math.sqrt(2 * r0) * (1 + eg / (F0 * lr0)) / 0.5
print(f"dM/dc = {a1:.6f} + {a2:.6f} + {a3:.6f} = {a1 + a2 + a3:.6f}")
phi1 = math.sqrt(math.pi / 2)
Z = lambda M: (math.sqrt(phi1 * (M + 3.5776e-4)) + math.sqrt(1.0532e-11)) ** 2
Mb = 0.80508
Mt = Mb + (c_true - 0.5) * (a1 + a2 + a3)
print(f"printed M = {Mb} -> Z = {Z(Mb):.5f} (printed 1.00948)")
print(f"with c = {c_true:.5f}: M = {Mt:.5f} -> Z = {Z(Mt):.5f}; major-arc bound 1.058259")
ok = abs(c_book - 0.49911) < 5e-6 and c_true > 0.81 and Z(Mt) > 1.00948 and Z(Mb) <= 1.00948
if ok:
    print(f"CONFIRMED: (6.77)'s constant is {c_true:.5f}, not 0.49911 (so not 0.5), and with it the section 14.3 chain gives Z = {Z(Mt):.4f} x^2/kappa > 1.00948 (still < 1.058259); the scale issue is not numerical and is not checked.")
else:
    print("NOT CONFIRMED: (6.77)'s constant 0.5 is consistent, or correcting it does not move Z above 1.00948.")
