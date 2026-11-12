"""Check of [H, Eq (14.17)] (eq:fabienne, the bound on E_{eta_*,r,8}).

Claim: the bracket (1/kappa)(2.485e-19 + (381500 + 76 sqrt(300000))/sqrt(10^25))
equals 1.33805e-7/kappa, not the printed 1.33805e-8/kappa (exponent slip); the
2.485e-19 term also lacks its sqrt(q*) factor (negligible).  Carried forward,
the display before (14.26) becomes ~2.79e-6/kappa (printed 1.7316e-6/kappa),
(14.26) becomes ~3.962e-5/kappa = 8.086e-7 x^2 (printed 3.85628e-5/kappa,
7.86996e-7 x^2), and (14.27)'s 1.058259 still holds only via the unrounded
1.3203236*(0.8023792 - 0.000834).

Book inputs:
  - intromaj.tex:115-131   Cor 7.1.3: |E| <= 2.485e-19 + (381500/sqrt(q) + 76)/sqrt(x)
  - conclusion.tex:282-295 (14.17): the bracket above, "<= 1.33805e-8/kappa";
                           max over q <= 300000 of sqrt(q*)|err|
  - conclusion.tex:274     x/kappa >= 10^25, kappa = 49
  - conclusion.tex:429-433 1.33805e-8/kappa*8.7806 + 2.3922e-8*1.6812*(sqrt(8.7806)
                           + 1.6812*0.80014)*sqrt(1.77082/kappa) <= 1.7316e-6/kappa
  - conclusion.tex:455-463 (14.26): 2.9387e-5 sqrt(pi/2)/kappa + 1.7316e-6/kappa + ...
                           = 3.85628e-5/kappa = 7.86996e-7
  - conclusion.tex:470-478 1.3203236(...) >= 1.0594003 - 0.001102 >= 1.058298 -> 1.058259;
                           conclusion.tex:263-264 |phi|_1|eta_o|_2^2 = 0.80237...,
                           conclusion.tex:96 |eta_o|_2 >= 0.8001287
Confirms if the bracket lies in (1.33805e-8, 1.33805e-7], and the propagated
values exceed the printed ones while 1.058259 still follows from the unrounded chain.

Run: python3 -I eq_14_17.py

Ported from a 2026-11-06 check script.
"""
import math

kap = 49
s3 = math.sqrt(300000)
br = 2.485e-19 + (381500 + 76 * s3) / math.sqrt(1e25)
br_q = 2.485e-19 * s3 + (381500 + 76 * s3) / math.sqrt(1e25)
print(f"bracket as printed = {br:.7e} (printed bound 1.33805e-8)")
print(f"bracket with sqrt(q*) on the constant term = {br_q:.8e}")
# display before (14.26), with (14.17) corrected and other printed inputs kept
second = 2.3922e-8 * 1.6812 * (math.sqrt(8.7806) + 1.6812 * 0.80014) * math.sqrt(1.77082 / kap) * kap
pre_printed = 1.33805e-8 * 8.7806 + second
pre_corr = 1.33805e-7 * 8.7806 + second
print(f"display before (14.26) (times kappa): printed inputs {pre_printed:.5e}, corrected {pre_corr:.5e} (printed 1.7316e-6)")
tot = 2.9387e-5 * math.sqrt(math.pi / 2) + pre_corr
print(f"(14.26) error (times kappa): {tot:.5e} (printed 3.85628e-5); /49 = {tot / kap:.5e} (printed 7.86996e-7)")
main_unr = 1.3203236 * (math.sqrt(math.pi / 2) * 0.8001287 ** 2 - 0.000834)
print(f"unrounded 1.3203236*(|phi|_1*0.8001287^2 - 0.000834) = {main_unr:.8f}")
print(f"  minus corrected error: {main_unr - tot:.8f} ; rounded 1.058298 - error = {1.058298 - tot:.8f} (target 1.058259)")
ok = (1.33805e-8 < br <= 1.33805e-7 and br_q <= 1.33805e-7 and pre_corr > 1.7316e-6
      and tot > 3.85628e-5 and main_unr - tot >= 1.058259 and 1.058298 - tot < 1.058259)
if ok:
    print(f"CONFIRMED: the (14.17) bracket is {br:.6e}, so the bound is 1.33805e-7/kappa, not 1.33805e-8/kappa; propagated, (14.26) becomes {tot:.4e}/kappa = {tot / kap:.4e} x^2, and 1.058259 survives only through the unrounded {main_unr:.7f}.")
else:
    print("NOT CONFIRMED: the (14.17) bracket and its propagation do not behave as claimed.")
