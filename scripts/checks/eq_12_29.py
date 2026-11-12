"""Check of [H, Eq (12.29)] (eq:joho, and "all smaller R are covered by that Lemma").

Claim: the sentence after (12.29), that every R failing (12.29) is covered by
Lemma 12.2.3 with sigma = c+ = 1.36, is not justified: the lemma's (12.21) has
denominator log Q + 1.312, while (12.23) needs log Q + c_E; the largest sigma
for which the lemma does give (12.23) is 1.36 - 0.627312(c_E - 1.312) ~ 1.347089,
which changes c(c+) from 0.911808 to ~0.90861.

Book inputs (l2normls.tex): 369-371 c_E = 1.3325822; 514-524 Lemma 12.2.3
((12.21), its hypotheses Q >= 200 Q0, rho <= 2/3, sigma >= 1.312 rho, and
c(sigma)); 572-578 (12.23), c+ = 1.36, Q >= 20000 Q0, Q0 >= 10^5, rho <= 0.6;
660-665 (12.29) and the "covered by that Lemma" sentence; 783 omega <= 0.627312.
Method: an admissible case with R below the (12.29) threshold: q = 2^9 5^9,
s = 1, Q0 = 3*10^9 (R = Q0/(sq) = 3), rho = 0.6 (Q = Q0^(5/3)).  Check the
Prop.'s and lemma's hypotheses, that (12.29) fails there (so the proof relies on
the lemma), and compare the lemma's bound with what (12.23) requires.
Confirms if the case is admissible, (12.29) fails, and the lemma's bound
exceeds (12.23)'s; also prints the largest admissible sigma and c(sigma).

Run: PYTHONPATH=<mpmath dir> python3 -s eq_12_29.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
cE, cp, Q0min = mp.mpf('1.3325822'), mp.mpf('1.36'), mp.mpf(10) ** 5
eg = mp.exp(-mp.euler)
c = lambda s: mp.exp(eg * (s - s ** 2 / mp.mpf('5.248') - mp.mpf('1.172')))
q, s, Q0, rho = mp.mpf(2) ** 9 * mp.mpf(5) ** 9, 1, mp.mpf(3) * 10 ** 9, mp.mpf('0.6')
Q = Q0 ** (1 / rho)
R = Q0 / (s * q)
tau = (1 - rho) * eg
adm = (Q >= 20000 * Q0, Q0 >= Q0min, rho <= mp.mpf("0.6"), q <= Q0, 1 <= s <= Q0 / q,  # Prop 12.2.4
       Q >= 200 * Q0, rho <= mp.mpf(2) / 3, cp >= mp.mpf('1.312') * rho)       # Lemma 12.2.3
thr = c(cp) * max(R * q, Q0min) ** tau - mp.log(q)
print(f"q = 2^9 5^9, s = 1, Q0 = 3e9, rho = 0.6: R = {mp.nstr(R,5)}, Q/Q0 = {mp.nstr(Q/Q0,5)}; hypotheses hold: {all(adm)}")
print(f"(12.29) needs R > {mp.nstr(thr,6)}: fails, so R is left to the lemma: {R <= thr}")
lem = (mp.log(Q0) + cp) / (mp.log(Q) + mp.mpf('1.312'))
need = (mp.log(Q0) + cp) / (mp.log(Q) + cE)
print(f"Lemma 12.2.3 (sigma = 1.36) gives {mp.nstr(lem,7)}; (12.23) needs {mp.nstr(need,7)}")
sig = cp - mp.mpf('0.627312') * (cE - mp.mpf('1.312'))
print(f"largest sigma giving (12.23) for all admissible (Q0,Q): {mp.nstr(sig,7)}; c(1.36) = {mp.nstr(c(cp),7)}, c(sigma) = {mp.nstr(c(sig),7)}")
if all(adm) and R <= thr and lem > need:
    print(f"CONFIRMED: in the admissible case q = 2^9 5^9, s = 1, Q0 = 3e9, rho = 0.6, R = 3 fails (12.29), and Lemma 12.2.3 gives only {mp.nstr(lem,6)} where (12.23) needs {mp.nstr(need,6)}, so 'covered by that Lemma' does not follow.")
else:
    print("NOT CONFIRMED: the example is not admissible or the lemma suffices.")
