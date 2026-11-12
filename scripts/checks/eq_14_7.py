"""Check of [H, Eq (14.7)] (eq:celine, the l2 norm of S_{eta_+} over the major arcs).

Claim: the term 5.19*delta_0*r*ET*(|eta_+|_1 + ET/2), printed <= 0.075272, is
0.075457 with the book's own inputs (ET <= 1.1405e-8, |eta_+|_1 <= 1.062319);
so the printed O*(0.0754), the lower end 8.6298x and the upper end 8.7806x of
(14.7) do not follow (the corrected chain gives [8.62971x, 8.78077x], i.e.
(8.7052 + O*(0.0756))x <= 8.7808x).  The next term, printed <= 1.00393e-8, is
1.0093e-8 (harmless).

Book inputs:
  - conclusion.tex:22-24   r = 150000, x_+ = 4.9e26; delta_0 = 8 (line 35)
  - conclusion.tex:37-40   (14.1) ET = 4.772e-11 + 251400/sqrt(x_+) <= 1.1405e-8
  - conclusion.tex:43-49   (14.2) E_{eta_+,r,delta_0} <= 2.3992e-8
  - conclusion.tex:65      (14.3) |eta_+|_1 <= 1.062319
  - conclusion.tex:80-83   K_{r,2} <= 9.71e-21 x
  - conclusion.tex:86-92   5.19 delta_0 r ET(|eta_+|_1 + ET/2) <= 0.075272;
                           delta_0 r log(2e^2 r)(E^2 + K_{r,2}/x) <= 1.00393e-8
  - conclusion.tex:130-136 8.70517 <= L_{r,delta_0} <= 8.70531
  - conclusion.tex:140-144 (14.7) (8.70524 + O*(0.00007))x + O*(0.075273)x
                           = (8.7052 + O*(0.0754))x <= 8.7806x
Confirms if the 5.19-term exceeds 0.075272 (and 0.075273) with the printed ET
bound, and the resulting interval [L_lo - err, L_hi + err] is not contained in
[8.6298, 8.7806] (so neither O*(0.0754) nor the endpoints follow).

Run: python3 -I eq_14_7.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as D, getcontext
import math

getcontext().prec = 40
r, d0, xp = D(150000), D(8), D("4.9e26")
ET_exact = D("4.772e-11") + D(251400) / xp.sqrt()
ET = D("1.1405e-8")
eta1 = D("1.062319")
E = D("2.3992e-8")
Kx = D("9.71e-21")
print(f"ET exact = {ET_exact:.8e} (printed bound 1.1405e-8)")
T1 = D("5.19") * d0 * r * ET * (eta1 + ET / 2)
T1e = D("5.19") * d0 * r * ET_exact * (eta1 + ET_exact / 2)
print(f"5.19-term with ET = 1.1405e-8: {T1:.7f}; with exact ET: {T1e:.7f}; printed <= 0.075272")
T1_2013 = D("5.19") * d0 * r * D("1.1377e-8") * (eta1 + D("1.1377e-8") / 2)
print(f"  (same term with the 2013 bound ET <= 1.1377e-8: {T1_2013:.7f})")
logterm = d0 * r * D(math.log(2 * math.e ** 2 * 150000))
T2 = logterm * (E * E + Kx)
print(f"second term = {T2:.5e}; printed <= 1.00393e-8")
Llo, Lhi = D("8.70517"), D("8.70531")
err = T1 + T2
lo, hi = Llo - err, Lhi + err
print(f"corrected range: [{lo:.6f}, {hi:.6f}]  vs printed [8.6298, 8.7806]")
half = max(D("8.7052") - lo, hi - D("8.7052"))
print(f"half-width around 8.7052: {half:.6f} (printed O*(0.0754))")
plo, phi_ = Llo - D("0.075273"), Lhi + D("0.075273")
print(f"printed chain with 0.075273: [{plo:.6f}, {phi_:.6f}]")
ok = T1 > D("0.075273") and lo < D("8.6298") and hi > D("8.7806") and half > D("0.0754")
if ok:
    print(f"CONFIRMED: with the book's ET <= 1.1405e-8 and |eta_+|_1 <= 1.062319 the 5.19-term is {T1:.6f} > 0.075272, giving [{lo:.5f}x, {hi:.5f}x], so (14.7)'s O*(0.0754), 8.6298x and 8.7806x do not follow (8.7808x does).")
else:
    print("NOT CONFIRMED: the printed 0.075272 and the range [8.6298, 8.7806] follow from the book's inputs.")
