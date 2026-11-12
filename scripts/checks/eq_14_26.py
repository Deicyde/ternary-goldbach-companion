"""Check of [H, Eq (14.26)] (eq:margot, the major-arc integral with error term).

Claim: the 1.7316e-6/kappa term in the display before (14.26) rests on two wrong
inputs: E_{eta_*,r,8} <= 1.33805e-8/kappa from (14.17), whose expression is
1.33805e-7/kappa, and 2.3922e-8 for E_{eta_+,r,8}, where (14.2) gives 2.3992e-8.
Corrected, the term is 2.7937e-6/kappa and (14.26) holds with
O*(3.9625e-5 x^2/kappa) = O*(8.0867e-7 x^2), not 3.85628e-5/kappa and 7.86996e-7.

Book inputs:
  - conclusion.tex:43-49   (14.2) 1.3482e-14 sqrt(300000) + 1.617e-10/sqrt(2)
                           + (499900 + 52 sqrt(300000))/sqrt(x_+) <= 2.3992e-8, x_+ = 4.9e26
  - conclusion.tex:282-290 (14.17) (1/kappa)(2.485e-19 + (381500 + 76 sqrt(300000))/sqrt(10^25))
                           <= 1.33805e-8/kappa
  - conclusion.tex:429-436 1.33805e-8/kappa*8.7806 + 2.3922e-8*1.6812*(sqrt(8.7806)
                           + 1.6812*0.80014)*sqrt(1.77082/kappa) <= 1.7316e-6/kappa, kappa = 49
  - conclusion.tex:455-463 (14.26): O*(2.9387e-5 sqrt(pi/2)/kappa x^2 + 1.7316e-6/kappa x^2
                           + 43 (log x)^2 x) = O*(3.85628e-5 x^2/kappa) = O*(7.86996e-7 x^2)
Confirms if the printed inputs reproduce 1.7316e-6, the two inputs are wrong as
stated, and the corrected total exceeds the printed 3.85628e-5/kappa.

Run: python3 -I eq_14_26.py

Ported from a 2026-11-06 check script.
"""
import math

kap, xp = 49, 4.9e26
s3 = math.sqrt(300000)
Estar = 2.485e-19 + (381500 + 76 * s3) / math.sqrt(1e25)
Eplus = 1.3482e-14 * s3 + 1.617e-10 / math.sqrt(2) + (499900 + 52 * s3) / math.sqrt(xp)
print(f"(14.17) expression: {Estar:.6e}/kappa (book uses 1.33805e-8/kappa)")
print(f"(14.2) expression: {Eplus:.6e} (printed <= 2.3992e-8; the display uses 2.3922e-8)")


def term(es, ep):
    return es * 8.7806 + ep * 1.6812 * (math.sqrt(8.7806) + 1.6812 * 0.80014) * math.sqrt(1.77082 / kap) * kap


tp = term(1.33805e-8, 2.3922e-8)
tc = term(1.33805e-7, 2.3992e-8)
print(f"display before (14.26), times kappa: printed inputs {tp:.6e} (printed 1.7316e-6); corrected {tc:.6e}")
x = xp
logterm = 43 * math.log(x) ** 2 * x / x ** 2 * kap  # 43(log x)^2 x as a multiple of x^2/kappa
main = 2.9387e-5 * math.sqrt(math.pi / 2)
tot_p = main + tp + logterm
tot_c = main + tc + logterm
print(f"43(log x)^2 x at x_+ as multiple of x^2/kappa: {logterm:.3e}")
print(f"(14.26) total, times kappa: printed inputs {tot_p:.6e} (printed 3.85628e-5); corrected {tot_c:.6e}; /49 = {tot_c / kap:.6e} (printed 7.86996e-7)")
ok = (abs(tp - 1.7316e-6) < 1e-9 and Estar > 1.33805e-8 and Eplus > 2.3922e-8 and Eplus <= 2.3992e-8
      and tot_c > 3.85628e-5 and tot_c / kap > 7.86996e-7)
if ok:
    print(f"CONFIRMED: with (14.17)'s value 1.33805e-7 and (14.2)'s 2.3992e-8 the term before (14.26) is {tc:.5e}/kappa (printed 1.7316e-6/kappa) and (14.26)'s error is {tot_c:.5e} x^2/kappa = {tot_c / kap:.5e} x^2 (printed 3.85628e-5/kappa = 7.86996e-7 x^2).")
else:
    print("NOT CONFIRMED: the display before (14.26) and (14.26) follow from the book's inputs.")
