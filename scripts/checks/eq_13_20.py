"""Check of [H, Eq (13.20)] (eq:lili, the jump coefficient of H(r) at r_1).

Claim: in 7/15 + (-2.14938 + (8/15) log kappa)/(log x + 2c^-) the constant
should be -2(log(3/8) + c^+ - (8/15)c^-) = -1.46271 for the book's c^+ = 2.0532,
c^- = 0.6394 (-2.14938 comes from c^+ = 2.3912, c^- = 0.6294).  At kappa = 49,
x = 4.9e26 the true jump 0.476437 exceeds the printed bound 0.465491, so the
display understates the bound.

Book inputs:
  - intminarc.tex:382-386  H(r) = (log(r+1) + c^+)/(log sqrt(x) + c^-) for r < r_1, 1 for r >= r_1;
                           c^+ = 2.0532, c^- = 0.6394
  - intminarc.tex:391-401  r_1 = (3/8) y^(4/15), y = x/kappa; the jump
                           1 - (log((3/8)(x/kappa)^(4/15) + 1) + c^+)/(log sqrt(x) + c^-)
                           <= 7/15 + (-2.14938 + (8/15) log kappa)/(log x + 2c^-)
  - intminarc.tex:415-421  (13.20) uses the same coefficient times g(r_1)
  - conclusion.tex:24, 274 kappa = 49, x >= x_+ = 4.9e26
Confirms if the constant implied by the book's own algebra (second line of the
display) with c^+ = 2.0532, c^- = 0.6394 differs from -2.14938, and at kappa = 49,
x = 4.9e26 the exact jump exceeds the printed bound.  (Only this coefficient is
checked; the downstream minor-arc total is not recomputed here.)

Run: python3 -I eq_13_20.py

Ported from a 2026-11-06 check script.
"""
import math

cp, cm = 2.0532, 0.6394
const = -2 * (math.log(3 / 8) + cp - 8 / 15 * cm)
const2013 = -2 * (math.log(3 / 8) + 2.3912 - 8 / 15 * 0.6294)
print(f"-2(log(3/8) + c+ - (8/15)c-) with c+ = 2.0532, c- = 0.6394: {const:.6f} (printed -2.14938)")
print(f"same with c+ = 2.3912, c- = 0.6294: {const2013:.6f}")
kap, x = 49, 4.9e26
lx = math.log(x)
y = x / kap
jump = 1 - (math.log(3 / 8 * y ** (4 / 15) + 1) + cp) / (lx / 2 + cm)
printed = 7 / 15 + (-2.14938 + 8 / 15 * math.log(kap)) / (lx + 2 * cm)
corr = 7 / 15 + (const + 8 / 15 * math.log(kap)) / (lx + 2 * cm)
print(f"kappa = 49, x = 4.9e26: exact jump {jump:.7f}, printed bound {printed:.7f}, corrected bound {corr:.7f}")
# the corrected bound is exactly the jump with the +1 dropped (so it is >= the jump):
# check this identity for x = 10^27..10^300
okr = all(abs((1 - (math.log(3 / 8) + 4 / 15 * (e * math.log(10) - math.log(kap)) + cp) / (e * math.log(10) / 2 + cm))
              - (7 / 15 + (const + 8 / 15 * math.log(kap)) / (e * math.log(10) + 2 * cm))) < 1e-12 for e in range(27, 301))
print(f"corrected bound = jump without the +1 (an upper bound for it), x = 10^27..10^300: {okr}")
ok = abs(const - (-2.14938)) > 0.1 and abs(const2013 + 2.14938) < 1e-5 and jump > printed and corr >= jump and okr
if ok:
    print(f"CONFIRMED: with c+ = 2.0532, c- = 0.6394 the constant is {const:.5f}, not -2.14938 (the value for c+ = 2.3912, c- = 0.6294), and at kappa = 49, x = 4.9e26 the jump {jump:.6f} exceeds the printed bound {printed:.6f}.")
else:
    print("NOT CONFIRMED: the printed constant -2.14938 is consistent with the book's c+ and c-.")
