"""Check of [H, (A.18)] (|(t+i) Mh(it)|_1 <= 27.8622803).

Claim: the text says the norm is at most two times a bracketed sum, but
27.8622803 is the bracket itself, so the argument gives only <= 55.7245604;
the true norm is about 36.677, so (A.18) is false.

Book inputs (normsapp.tex):
  - l.8-10   h(t) = t^2 (2-t)^3 e^{t-1/2} on [0,2]; l.61 Mellin transform.
  - l.82-87  (A.8): |Mh(it)| <= C_4/(|t||t+i||t+2i||t+3i|).
  - l.100, 121-128, 145-152, 180-182, 209-212: printed C_0 = 92e^{-1/2} -
             12e^{3/2}, C_1 = 2 sqrt(e), C_2 = 10.79195821037,
             C_3 = 75.1295251672, C_4 = 2013.18185012.
  - l.228-241 (A.17) with its factor 2, printed 16.1939176 (control).
  - l.243-260 "at most two times" the bracket, its closed form, (A.18).
  - notprem.tex l.35: |f|_r is the L_r norm on the whole line.

Method: evaluate the printed closed form of the bracket and of (A.17). Compute
Mh(it) from the series Mh(s) = 6e^{-1/2} sum_n 2^{s+n+5}/(n!(s+n+2)(s+n+3)
(s+n+4)(s+n+5)) (expand e^x and use the Beta integral), checked against direct
quadrature, and integrate |t+i||Mh(it)| over [-T,T] by Gauss-Legendre; the
tail is at most 2 C_4 (1/(2T^2) + 1/(3T^3)) by (A.8).

Confirms if: the bracket reproduces 27.8622803 (and (A.17) reproduces
16.1939176 with its factor 2), and the true norm (lower bound: the integral
over [-T,T]) exceeds 27.8622803.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_a_18.py

Ported from a 2026-11-06 check script.
"""
import math
from mpmath import mp, mpf, mpc, quad as mquad, exp as mexp, log as mlog, linspace

E = math.e
C0 = 92 * E**-0.5 - 12 * E**1.5
C1 = 2 * math.sqrt(E)
C2, C3, C4 = 10.79195821037, 75.1295251672, 2013.18185012

a17 = 2 * (C1 + C1 * math.log(C2 * C0 / C1**2) + C2 * (C1 / C2 - C2 / C3)
           + C3 / 2 * (C2**2 / C3**2 - C3**2 / C4**2) + C4 / 3 * C3**3 / C4**3)
F = lambda t: math.sqrt(t * t + 1) + math.log((math.sqrt(t * t + 1) - 1) / t)
r = C1 / C0
bracket = (C0 / 2 * (math.sqrt(r**4 + r**2) + math.asinh(r)) + C1 * (F(C2 / C1) - F(C1 / C0))
           + C2 * math.log(C3 * C1 / C2**2) + C3 * (C2 / C3 - C3 / C4) + C4 / 2 * C3**2 / C4**2)
print("(A.17) expression (with factor 2): %.9f  book 16.1939176" % a17)
print("(A.18) bracket closed form:        %.9f  book prints 27.8622803" % bracket)
print("two times the bracket:             %.9f" % (2 * bracket))

def Mh(s):
    tot, fact = 0j, 1.0
    for n in range(80):
        tot += 2.0**(s + n + 5) / (fact * (s + n + 2) * (s + n + 3) * (s + n + 4) * (s + n + 5))
        fact *= n + 1
    return 6 * E**-0.5 * tot

mp.dps = 25
maxerr = 0
for t in [0, 0.5, 3, 30, 200]:
    # Mh(it) = int h(e^u) e^{itu} du, u = log x, split into many panels
    hh = lambda x: x**2 * (2 - x)**3 * mexp(x - mpf(1) / 2)
    direct = mquad(lambda u: hh(mexp(u)) * mexp(1j * t * u), linspace(-60, mlog(2), 400))
    maxerr = max(maxerr, abs(complex(direct) - Mh(1j * t)))
print("max |series - quadrature| for Mh(it), t in {0,0.5,3,30,200}: %.2e" % maxerr)

def gl(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x); ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws

X, W = gl(16)
def integ(f, a, b, panels):
    h, tot = (b - a) / panels, 0.0
    for p in range(panels):
        c = a + (p + 0.5) * h
        tot += sum(w * f(c + 0.5 * h * x) for x, w in zip(X, W)) * 0.5 * h
    return tot

g = lambda t: math.hypot(t, 1) * abs(Mh(1j * t))
# |Mh(-it)| = |Mh(it)| (h real), so the full-line integral is twice [0,T]
I10 = 2 * integ(g, 0, 10, 40)
T = 2000.0
IT = 2 * (integ(g, 0, 10, 40) + integ(g, 10, 100, 180) + integ(g, 100, T, 1900))
tail = 2 * C4 * (1 / (2 * T * T) + 1 / (3 * T**3))
print("int_{-10}^{10} |t+i||Mh(it)| dt = %.6f" % I10)
print("int_{-%g}^{%g} |t+i||Mh(it)| dt = %.6f, tail <= %.2e, so the norm is in [%.5f, %.5f]"
      % (T, T, IT, tail, IT, IT + tail))

ok = (abs(bracket - 27.8622803) < 1e-6 and abs(a17 - 16.1939176) < 1e-6 and maxerr < 1e-12
      and I10 > 27.8622803)
if ok:
    print("CONFIRMED: 27.8622803 is the bracket itself (twice it is %.7f), and the true |(t+i)Mh(it)|_1 is %.4f > 27.8622803, so (A.18) is false."
          % (2 * bracket, IT))
else:
    print("NOT CONFIRMED: the computation does not show (A.18) false as claimed.")
