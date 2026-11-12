"""Check of [H, Eq (14.29)] (eq:hexelor, S_{eta_*}(0,x) E <= 1.05315e-11 x^2/kappa).

Claim: the display before (14.29), S_{eta_*}(0,x) = (sqrt(pi/2) + O*(1.33805e-8)) x/kappa,
repeats (14.17)'s exponent slip: the error term from (14.17) is 1.338e-7, not
1.33805e-8 (and even the q = 1 case of Cor 7.1.3 gives 1.2067e-7).  (14.29)
itself still holds.

Book inputs:
  - intromaj.tex:115-131   Cor 7.1.3: |E| <= 2.485e-19 + (381500/sqrt(q) + 76)/sqrt(x)
  - conclusion.tex:282-290 (14.17) (1/kappa)(2.485e-19 + (381500 + 76 sqrt(300000))/sqrt(10^25))
  - conclusion.tex:274     x/kappa >= 10^25
  - conclusion.tex:509-514 (14.28) E <= 8.4029e-12 x
  - conclusion.tex:517-525 S_{eta_*}(0,x) = (sqrt(pi/2) + O*(1.33805e-8)) x/kappa;
                           (14.29) S_{eta_*}(0,x) E <= 1.05315e-11 x^2/kappa
Confirms if both the (14.17) expression and the q = 1 error exceed 1.33805e-8,
and (sqrt(pi/2) + 1.33805e-7) * 8.4029e-12 <= 1.05315e-11.

Run: python3 -I eq_14_29.py

Ported from a 2026-11-06 check script.
"""
import math

s3 = math.sqrt(300000)
e1417 = 2.485e-19 + (381500 + 76 * s3) / math.sqrt(1e25)
eq1 = 2.485e-19 + (381500 + 76) / math.sqrt(1e25)
print(f"(14.17) expression = {e1417:.6e}; q = 1 bound from Cor 7.1.3 = {eq1:.6e}; printed 1.33805e-8")
lhs = (math.sqrt(math.pi / 2) + 1.33805e-7) * 8.4029e-12
lhs8 = (math.sqrt(math.pi / 2) + 1.33805e-8) * 8.4029e-12
print(f"(sqrt(pi/2) + 1.33805e-7)*8.4029e-12 = {lhs:.8e}; with 1e-8: {lhs8:.8e}; printed <= 1.05315e-11")
ok = e1417 > 1.33805e-8 and eq1 > 1.33805e-8 and lhs <= 1.05315e-11
if ok:
    print(f"CONFIRMED: the error term in S_eta*(0,x) is {e1417:.4e} (q = 1: {eq1:.4e}), not 1.33805e-8, and (14.29) still holds since (sqrt(pi/2) + 1.33805e-7)*8.4029e-12 = {lhs:.6e} <= 1.05315e-11.")
else:
    print("NOT CONFIRMED: the display before (14.29) is consistent with the book's inputs, or (14.29) fails.")
