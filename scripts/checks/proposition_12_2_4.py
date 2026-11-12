"""Check of [H, Proposition 12.2.4] (prop:espagn, G_q(Q0/sq)/G_q(Q/sq) <= (log Q0 + c+)/(log Q + c_E)).

Claim: step (12.29) covers small R by Lemma 12.2.3 with sigma = c+ = 1.36, but
that lemma bounds the quotient by (log Q0 + sigma)/(log Q + 1.312), weaker than
(12.23)'s denominator log Q + c_E.  Applying the lemma as stated needs
sigma <= 1.36 - omega(rho)(c_E - 1.312) ~ 1.34709; then c(c+) = 0.911808 drops
to ~0.908613 and the printed comparison varpi_0(3.3e9) >= 477.465 >
lambda(3.3e9) <= 475.513 (210 does not divide q) fails.  A repair that
re-derives the lemma against log Q + c_E gives c ~ 0.909181, and both printed
comparisons then still hold.

Book inputs (l2normls.tex):
  - 369-371  c_E = 1.3325822;
  - 514-524  Lemma 12.2.3, (12.21) with denominator log Q + 1.312 and
             c(sigma) = exp(e^-gamma (sigma - sigma^2/5.248 - 1.172));
  - 527-561  its proof (RHS of (12.22) >= (1-rho)(log Q0+sigma) + 1.312 rho^2);
  - 572-578  Prop 12.2.4, (12.23), c+ = 1.36, Q0,min = 10^5, rho <= 0.6;
  - 607-613  omega(rho); 783 omega(rho) <= 0.627312;
  - 660-665  (12.29) and "all smaller R are covered by that Lemma";
  - 675-690  varpi_0(q), tau = (1-rho) e^-gamma;
  - 864-870  varpi_0(2.2e10) >= 846.765 > lambda <= 838.227;
  - 902-903  varpi_0(3.3e9) >= 477.465 > lambda <= 475.513.
Confirms if (i) the lemma's bound exceeds (12.23)'s at Q0 = 10^5, rho = 0.6,
(ii) the printed varpi_0 values are reproduced with c(1.36), (iii) with the
largest admissible sigma the 3.3e9 comparison fails, and (iv) the re-derived
constant keeps both comparisons.

Run: PYTHONPATH=<mpmath dir> python3 -s proposition_12_2_4.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
cE, cp = mp.mpf('1.3325822'), mp.mpf('1.36')
eg = mp.exp(-mp.euler)
c = lambda s: mp.exp(eg * (s - s ** 2 / mp.mpf('5.248') - mp.mpf('1.172')))
rho = mp.mpf('0.6')
tau = (1 - rho) * eg
def varpi0(q, cc):
    A = cc * q ** tau - mp.log(q)
    return (cc * q ** tau - mp.log(q) / A ** (tau / (1 - tau))) ** (1 / (1 - tau))
l = mp.log(10 ** 5); L = l / rho
lem = (l + cp) / (L + mp.mpf('1.312')); need = (l + cp) / (L + cE)
print(f"(i) Q0=1e5, rho=0.6: lemma bound {mp.nstr(lem,7)}, (12.23) needs {mp.nstr(need,7)}")
om = mp.mpf('0.627312')
sig = cp - om * (cE - mp.mpf('1.312'))
print(f"largest sigma valid for all admissible (Q0,Q): {mp.nstr(sig,8)}")
print(f"c(1.36) = {mp.nstr(c(cp),7)}, c(sigma) = {mp.nstr(c(sig),7)}")
# (iv) re-derived lemma: (L-l+1.312)(l+c+)/(L+cE) = (1-rho)(l+c+) + theta(1.312-(1-rho)cE), theta >= rho
for (l_, L_) in [(11.5, 30.0), (20.0, 45.0), (13.0, 21.0)]:
    l_, L_ = mp.mpf(l_), mp.mpf(L_); r_ = l_ / L_; th = (l_ + cp) / (L_ + cE)
    lhs = (L_ - l_ + mp.mpf('1.312')) * (l_ + cp) / (L_ + cE)
    rhs = (1 - r_) * (l_ + cp) + th * (mp.mpf('1.312') - (1 - r_) * cE)
    assert abs(lhs - rhs) < mp.mpf(10) ** -20
f = lambda r: (1 - r) * cp + mp.mpf('1.312') * r - r * (1 - r) * cE - mp.mpf('1.172')
grid = [mp.mpf(k) / 10000 for k in range(1, 6001)]
rmin = min(grid, key=f)
crep = mp.exp(eg * f(rmin))
print(f"re-derived: min over rho in (0,0.6] = {mp.nstr(f(rmin),7)} at rho = {mp.nstr(rmin,4)}, c = {mp.nstr(crep,7)}")
rows = []
for name, cc in [("book c(1.36)", c(cp)), ("lemma as stated", c(sig)), ("re-derived", crep)]:
    a, b_ = varpi0(mp.mpf('2.2e10'), cc), varpi0(mp.mpf('3.3e9'), cc)
    rows.append((a, b_))
    print(f"{name:16s}: varpi0(2.2e10) = {mp.nstr(a,7)} (vs 838.227), varpi0(3.3e9) = {mp.nstr(b_,7)} (vs 475.513)")
ok = (lem > need and abs(rows[0][0] - mp.mpf('846.765')) < 0.01 and abs(rows[0][1] - mp.mpf('477.465')) < 0.01
      and rows[1][1] < mp.mpf('475.513') and rows[2][0] > mp.mpf('838.227') and rows[2][1] > mp.mpf('475.513'))
if ok:
    print(f"CONFIRMED: Lemma 12.2.3 as stated only gives (12.23) with sigma <= {mp.nstr(sig,7)}, which lowers varpi_0(3.3e9) to {mp.nstr(rows[1][1],6)} < 475.513, while a lemma re-derived against log Q + c_E (c = {mp.nstr(crep,6)}) keeps both printed comparisons.")
else:
    print("NOT CONFIRMED: the computed values do not match the claim.")
