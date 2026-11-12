"""Eq 1.33: the constant 0.5 in R_{x,delta_0 q} log delta_0 q + 0.5.

Claim: in the AM-GM step (6.76)->(6.77) the constant term log2/(2 sqrt rho) + (sqrt rho/2)*0.67506
= 0.8102 is printed as (1/2)(log2/sqrt rho + (sqrt rho/2)*0.67506) = 0.49911 (rounded to 0.5);
with 0.5, (1.33) does not follow from the book's own (6.63), with 0.8102 it does.

Book inputs:
  - introductionp.tex:1503-1518: (1.33) with R_{x,t} = 0.27125 C_{x,t} + 0.41415,
    L_{x,t,q} = (q/phi(q))(13/4 log t + 7.82) + 13.66 log t + 37.55, 2.5, 3.36 x^{5/6}.
  - minarctotals.tex:1774-1786: (6.63) with sqrt(C(log t + 0.002) + log(4t)/2)
    * sqrt(0.30214 log t + 0.67506), 2.49157, 7.81811, 13.6516, 37.5415, 3.35531.
  - minarctotals.tex:2257-2288: AM-GM display, C_{x,t} = log(1 + log 4t / (2 log(9x^{1/3}/(2.004t)))),
    rho at x_1 = 10^25, q_0 = 2*10^5, and (6.77) with constant 0.49911.

Confirms if: the printed (6.77) constant evaluates to 0.49911 while the AM-GM constant is
0.8102; at x = 10^25, delta_0 q = 4*10^5 (where AM-GM is an equality) the printed (6.77) is
below (6.76); (6.63)/(1.33) > 1 at x = 10^25, delta_0 = 2, q = 95003, and with 0.8102 in place
of 0.5 the ratio is < 1 there and on a grid.

Run: python3 -I eq_1_33.py

Ported from a 2026-11-06 check script.
"""
from math import log, sqrt


def C(x, t):
    return log(1 + log(4 * t) / (2 * log(9 * x ** (1 / 3) / (2.004 * t))))


def rhs663(x, q, ph, d0):
    t = d0 * q
    A = C(x, t) * (log(t) + 0.002) + log(4 * t) / 2
    B = 0.30214 * log(t) + 0.67506
    return (x / sqrt(d0 * ph) * sqrt(A) * sqrt(B) + 2.49157 * x / sqrt(t)
            + 2 * x / (d0 * ph) * (13 / 4 * log(t) + 7.81811)
            + 2 * x / t * (13.6516 * log(t) + 37.5415) + 3.35531 * x ** (5 / 6))


def rhs133(x, q, ph, d0, const=0.5):
    t = d0 * q
    R = 0.27125 * C(x, t) + 0.41415
    L = q / ph * (13 / 4 * log(t) + 7.82) + 13.66 * log(t) + 37.55
    return (R * log(t) + const) / sqrt(d0 * ph) * x + 2.5 * x / sqrt(t) + 2 * x / t * L + 3.36 * x ** (5 / 6)


def phi(n):
    r, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            r -= r // p
        p += 1
    if m > 1:
        r -= r // m
    return r


ok = True
x1, q0 = 1e25, 2e5
t1 = 2 * q0
rho = (C(x1, t1) * (log(t1) + 0.002) + log(8 * q0) / 2) / (0.30214 * log(t1) + 0.67506)
sr = sqrt(rho)
printed = 0.5 * (log(2) / sr + sr / 2 * 0.67506)
correct = log(2) / (2 * sr) + sr / 2 * 0.67506
print("rho = %.7f (book 3.397962...), sqrt(rho) = %.7f" % (rho, sr))
print("1/(2 sqrt rho) = %.6f (book 0.27125); 1/(4 sqrt rho) + 0.30214 sqrt(rho)/2 = %.6f (book 0.4141)"
      % (1 / (2 * sr), 1 / (4 * sr) + 0.30214 * sr / 2))
print("printed (6.77) constant (1/2)(log2/sqrt rho + sqrt(rho)/2*0.67506) = %.6f (book 0.49911)" % printed)
print("AM-GM constant log2/(2 sqrt rho) + sqrt(rho)/2*0.67506          = %.6f" % correct)
ok &= abs(printed - 0.49911) < 5e-6 and abs(correct - 0.8102) < 5e-5

A = C(x1, t1) * (log(t1) + 0.002) + log(4 * t1) / 2
B = 0.30214 * log(t1) + 0.67506
lhs676 = sqrt(A * B)
amgm = A / (2 * sr) + sr / 2 * B
p677 = 0.27125 * C(x1, t1) * (log(t1) + 0.002) + 0.4141 * log(t1) + 0.49911
print("at x=1e25, t=4e5: (6.76) = %.6f, exact AM-GM bound = %.6f, printed (6.77) = %.6f" % (lhs676, amgm, p677))
ok &= p677 < lhs676

x, q = 1e25, 95003
r05 = rhs663(x, q, q - 1, 2) / rhs133(x, q, q - 1, 2)
r81 = rhs663(x, q, q - 1, 2) / rhs133(x, q, q - 1, 2, 0.8102)
print("x=1e25, delta0=2, q=95003 (prime): (6.63)/(1.33) = %.6f; with 0.8102: %.6f" % (r05, r81))
ok &= r05 > 1.02 and r81 < 1

worst = (0, None)
for e in [20.3345, 21, 22, 23, 24, 25, 26, 28, 30, 35, 40]:
    xx = max(10 ** e, 2.16e20)
    for k in range(1, 600):
        qq = int(10 ** (k * 0.0125))
        if qq > xx ** (1 / 3) / 6:
            break
        for qv in {qq, qq + 1}:
            ph = phi(qv)
            for d0 in (2, 3, 5, 10, 100, 1000):
                if d0 * qv > xx ** (1 / 3) / 3:
                    continue
                r = rhs663(xx, qv, ph, d0) / rhs133(xx, qv, ph, d0, 0.8102)
                if r > worst[0]:
                    worst = (r, (e, qv, d0))
print("grid max of (6.63)/(1.33 with 0.8102) = %.6f at (log10 x, q, delta0) = %s" % worst)
ok &= worst[0] < 1

if ok:
    print("CONFIRMED: the AM-GM constant in (6.77) is %.4f, not the printed %.5f, and with 0.5 the book's "
          "(6.63) exceeds (1.33) (ratio %.4f at x=1e25, q=95003, delta0=2) while with 0.8102 it does not."
          % (correct, printed, r05))
else:
    print("NOT CONFIRMED: the recomputed constants or ratios do not match the claim.")
