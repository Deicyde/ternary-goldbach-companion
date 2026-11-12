"""Check of [H, Eq (14.27)] (eq:juventud, the total major-arc lower bound 1.058259 x^2/kappa).

Claim: two slips in the derivation; the bound survives.  (i) 1.3203236 |phi|_1
0.8001287^2 = 1.0594001, not the printed 1.0594003.  (ii) With (14.26)'s error
corrected to 3.9625e-5/kappa (inherited from (14.17)), the printed rounded chain
gives 1.058298 - 0.0000396 = 1.0582584 < 1.058259; only the unrounded
1.3203236(0.8023792 - 0.000834) = 1.0582990 gives 1.0582594 >= 1.058259.

Book inputs:
  - conclusion.tex:96      (14.5) 0.8001287 <= |eta_o|_2
  - conclusion.tex:155-156 (14.9) C_0 >= 1.3203236
  - conclusion.tex:260-264 C_{eta_o,eta_*} >= (|phi|_1 |eta_o|_2^2 - 0.000834)/kappa,
                           |phi|_1 = sqrt(pi/2)
  - conclusion.tex:470-478 C_0 C >= 1.0594003/kappa - 0.001102/kappa >= 1.058298/49,
                           hence (14.27) >= 1.058259 x^2/kappa
  - conclusion.tex:282-290, 43-49, 429-433, 455-463: inputs of the corrected
                           (14.26) error (recomputed here): (14.17) bracket, (14.2),
                           display before (14.26), 2.9387e-5 sqrt(pi/2)
Confirms if 1.3203236 sqrt(pi/2) 0.8001287^2 < 1.0594003, and with the corrected
(14.26) error the rounded chain falls below 1.058259 while the unrounded one does not.

Run: python3 -I eq_14_27.py

Ported from a 2026-11-06 check script.
"""
import math

kap = 49
phi1 = math.sqrt(math.pi / 2)
a = 1.3203236 * phi1 * 0.8001287 ** 2
b = 1.3203236 * 0.000834
print(f"1.3203236*|phi|_1*0.8001287^2 = {a:.9f} (printed 1.0594003)")
print(f"1.3203236*0.000834 = {b:.9f} (printed 0.001102)")
print(f"unrounded C_0 C * kappa >= {a - b:.9f} (printed 1.058298)")
s3 = math.sqrt(300000)
Estar = 2.485e-19 + (381500 + 76 * s3) / math.sqrt(1e25)
Eplus = 1.3482e-14 * s3 + 1.617e-10 / math.sqrt(2) + (499900 + 52 * s3) / math.sqrt(4.9e26)
Estar_r = 1.33805e-7  # the (14.17) value, correctly rounded up
Eplus_r = 2.3992e-8   # (14.2)
assert Estar <= Estar_r and Eplus <= Eplus_r
pre = Estar_r * 8.7806 + Eplus_r * 1.6812 * (math.sqrt(8.7806) + 1.6812 * 0.80014) * math.sqrt(1.77082 / kap) * kap
err = 2.9387e-5 * phi1 + pre + 43 * math.log(4.9e26) ** 2 / 4.9e26 * kap
print(f"corrected (14.26) error, times kappa: {err:.6e} (printed 3.85628e-5)")
print(f"book: 1.058298 - 3.85628e-5 = {1.058298 - 3.85628e-5:.8f}")
r1 = 1.058298 - err
r2 = a - b - err
print(f"corrected, rounded chain: 1.058298 - err = {r1:.8f}; unrounded: {r2:.8f}; target 1.058259")
ok = a < 1.0594003 and r1 < 1.058259 <= r2
if ok:
    print(f"CONFIRMED: 1.3203236*sqrt(pi/2)*0.8001287^2 = {a:.7f} < 1.0594003, and with the corrected (14.26) error the rounded chain gives {r1:.7f} < 1.058259 while the unrounded {a - b:.7f} gives {r2:.7f} >= 1.058259.")
else:
    print("NOT CONFIRMED: the derivation of (14.27) does not show the claimed slips.")
