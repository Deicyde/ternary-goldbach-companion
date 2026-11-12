"""Check of [H, Eq (14.45)] (eq:jijona, the f_0 bracket <= 0.33239 for y >= 10^150).

Claim: the crude bound needs R_{z,2r_0}^2 P_2(log 2r_0)/sqrt(r_0), but the text
bounds R_{y,r_0} <= 0.43086 and R_{y/K,r_0} <= 0.43113 (computed with log 4r_0
and 2.004 r_0, i.e. t = r_0).  With R_{z,2r_0} the crude bound at y = 10^150 is
0.33306 > 0.33239.  The printed inequality itself survives: the exact left side
(from (13.35)) is 0.33221 at 10^150 and decreases.

Book inputs:
  - intminarc.tex:616-620  R_{z,t} = 0.27125 log(1 + log 4t / (2 log(9 z^(1/3)/(2.004 t)))) + 0.41415
  - intminarc.tex:507, 690 P_2(t) = t^2+4t+8, P_3(t) = t^3+6t^2+24t+48, P_2^- = 2t^2+16t+48
  - intminarc.tex:773-777  (13.34) f_0 uses (1-c_phi) sqrt(I_{0,r_0,r_1,y}) + c_phi sqrt(I_{0,r_0,r_1,2y/log y})
  - intminarc.tex:802-808  (13.35) definition of I_{0,r_0,r_1,z}
  - conclusion.tex:629     r_1 = (3/8) y^(4/15); r_0 = 150000; K = (log y)/2
  - conclusion.tex:794-795, 880  c_phi <= 0.07455/log((log y)/2) <= 0.02219
  - conclusion.tex:807-812 crude bound I_0 <= R_{z,2r_0}^2 P_2(log 2r_0)/sqrt(r_0)
                           + (R_{z,2r_1}^2 - 0.41415^2)/log(r_1/r_0) * P_2^-(log 2r_0)/sqrt(r_0)
  - conclusion.tex:814     R_{y,2r_1} <= 0.71215, R_{y/K,2r_1} <= 0.71392
  - conclusion.tex:815-875 R_{y,r_0} <= 0.43086 (formula with log 4r_0, 2.004 r_0),
                           R_{y/K,r_0} <= 0.43113; 0.10426, 0.10439; (14.45) <= 0.33239
Confirms if the printed R's are R_{z,r_0} (not R_{z,2r_0}), the crude bound with
R_{z,2r_0} exceeds 0.33239 at y = 10^150, and the exact left side is <= 0.33239
on y in [10^150, 10^4000] (geometric grid) and in the limit.

Run: python3 -I eq_14_45.py

Ported from a 2026-11-06 check script.
"""
import math

r0 = 150000.0
L10 = math.log(10)


def R(logz, t, logt=None):
    lt = math.log(t) if logt is None else logt
    return 0.27125 * math.log(1 + (math.log(4) + lt) / (2 * (math.log(9) + logz / 3 - math.log(2.004) - lt))) + 0.41415


P2 = lambda t: t * t + 4 * t + 8
P3 = lambda t: t ** 3 + 6 * t * t + 24 * t + 48
P2m = lambda t: 2 * t * t + 16 * t + 48
A = P2(math.log(2 * r0)) / math.sqrt(r0)
Am = P2m(math.log(2 * r0)) / math.sqrt(r0)
ly = 150 * L10
lyK = ly - math.log(ly / 2)
print(f"y = 10^150: R_(y,r0) = {R(ly, r0):.6f}, R_(y,2r0) = {R(ly, 2 * r0):.6f}, "
      f"R_(y/K,r0) = {R(lyK, r0):.6f}, R_(y/K,2r0) = {R(lyK, 2 * r0):.6f}")
print(f"P_2(log 2r0)/sqrt(r0) = {A:.6f}; R_(y,2r0)^2*that = {R(ly, 2 * r0) ** 2 * A:.6f} (printed 0.10426), "
      f"R_(y/K,2r0)^2*that = {R(lyK, 2 * r0) ** 2 * A:.6f} (printed 0.10439)")
n1 = (0.71215 ** 2 - 0.41415 ** 2) * Am
n2 = (0.71392 ** 2 - 0.41415 ** 2) * Am
print(f"numerators: {n1:.5f} (printed 0.49214), {n2:.5f} (printed 0.49584)")
den = 4 / 15 * ly - math.log(400000)
crude_printed = 0.97781 * math.sqrt(0.10426 + 0.49214 / den) + 0.02219 * math.sqrt(0.10439 + 0.49584 / den)
crude_2r0 = (0.97781 * math.sqrt(R(ly, 2 * r0) ** 2 * A + n1 / den)
             + 0.02219 * math.sqrt(R(lyK, 2 * r0) ** 2 * A + n2 / den))
print(f"crude bound at 10^150: printed inputs {crude_printed:.6f}; with R_(z,2r0) {crude_2r0:.6f}; printed <= 0.33239")


def I0(logz, logy):
    lr1 = math.log(3 / 8) + 4 / 15 * logy
    l2r0, l2r1 = math.log(2 * r0), math.log(2) + lr1
    Ra, Rb = R(logz, 2 * r0), R(logz, 0, math.log(2) + lr1)
    isr1 = math.exp(-lr1 / 2)
    t1 = Ra ** 2 * (P2(l2r0) / math.sqrt(r0) - P2(l2r1) * isr1)
    t2 = (Rb ** 2 - Ra ** 2) / (lr1 - math.log(r0)) * (P2m(l2r0) / math.sqrt(r0) - (P3(l2r1) - l2r0 * P2(l2r1)) * isr1)
    return t1 + t2


def lhs(e):
    logy = e * L10
    c = 0.07455 / math.log(logy / 2)
    return (1 - c) * math.sqrt(I0(logy, logy)) + c * math.sqrt(I0(logy - math.log(logy / 2), logy))


vals = []
e = 150.0
while e <= 4000:
    vals.append((lhs(e), e))
    e *= 1.002
mx = max(vals)
print(f"exact LHS: 10^150 {lhs(150):.6f}, 10^160 {lhs(160):.6f}, 10^1000 {lhs(1000):.6f}; max on grid {mx[0]:.6f} at 10^{mx[1]:.1f}")
# as y -> inf: c_phi -> 0, R_(z,2r0) -> 0.41415, and the second term of I_0 -> 0
# (R_(z,2r1) stays bounded while log(r1/r0) -> inf), so the left side -> 0.41415 sqrt(P_2/sqrt(r0))
lim = 0.41415 * math.sqrt(A)
print(f"limit y -> inf: 0.41415*sqrt(P_2(log 2r0)/sqrt(r0)) = {lim:.4f}")
ok = (abs(R(ly, r0) - 0.43086) < 5e-6 and R(ly, 2 * r0) > 0.43086 and crude_2r0 > 0.33239
      and mx[0] <= 0.33239 and lim <= 0.33239)
if ok:
    print(f"CONFIRMED: the printed 0.43086 is R_(y,r0); with R_(z,2r0), which the crude bound requires, (14.45)'s bound at y = 10^150 is {crude_2r0:.5f} > 0.33239, though the exact left side ({lhs(150):.5f} at 10^150, max {mx[0]:.5f} on the grid) stays below 0.33239.")
else:
    print("NOT CONFIRMED: the crude bound of (14.45) is consistent with R_(z,2r0), or the exact left side exceeds 0.33239.")
