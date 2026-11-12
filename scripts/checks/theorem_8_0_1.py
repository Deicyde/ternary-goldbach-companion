"""Check of [H, Theorem 8.0.1] (Mellin transform of the twisted Gaussian).

Claim: (i) the good-sign bound (8.3) is false when rho = 4|tau|/ell^2 is small;
for large ell it fails for every rho below about 0.81 (the claim gives the
approximate root 0.8137 of rho^2 + 6 pi rho = 16), because the L_3 step applies
a Gaussian tail bound that needs ell >= 0 while ell < 0; (ii) the first case
of (8.4), |x0| >= 0.51729 sqrt(tau) "for rho arbitrary", holds only for
rho >= 3/2 (up to rounding of 0.51729); (iii) for tau < 0, tau, ell and rho in
(8.1) need absolute values, as the proof says after (8.42).

Book inputs (mellintran.tex):
  - l.26-29: f_delta(t) = e^{-t^2/2} e(delta t), s = sigma + i tau, sigma >= 0,
    tau != 0, ell = -2 pi delta (e(x) = e^{2 pi i x}, notprem.tex l.34).
  - l.29-36: (8.1) for sgn(delta) != sgn(tau): |F| <= |Gamma(s)| e^{pi tau/2}
    e^{-E(rho) tau} c_1/tau^{sigma/2} (rho arbitrary), c_2/ell^sigma (rho <= 3/2).
  - l.37-58: (8.2) E(rho), c_1, c_2, upsilon(rho), rho = 4 tau/ell^2.
  - l.59-70: (8.3) and (8.4).
  - l.498 (8.21), l.748: x0 = Re u_{0,+} = (|ell|/2) sqrt((j-1)/2), j = sqrt(1+rho^2).
  - l.997-1000: "put absolute values around tau and ell" (after (8.42)).
  - l.1187-1198: L_3 step with int_{-oo}^{-ell} e^{-t^2/2} <= sqrt(pi/2) e^{-ell^2/2}.
F_delta(s) is computed from the exact series (1/2) sum_n (2 pi i delta)^n/n!
2^{(n+s)/2} Gamma((n+s)/2) and from e^{-pi^2 delta^2} Gamma(s) U(s-1/2, -2 pi i delta).

Confirms if: (i) |F| exceeds the (8.3) right side at s=1+i, delta=1 and at
s=1+20i, delta=2, 3, the L_3 Gaussian integral exceeds the claimed bound, and
at tau = 400 the bound fails at rho = 0.813 but holds at rho = 0.82;
(ii) x0/sqrt(tau) < 0.51729 at rho = 0.5 and 1.4; (iii) at s = 1-20i, delta = 1
(sgn differ, so (8.1) applies) the literal (8.1) gives a bound below |F| or a
negative one, while (8.1) with absolute values holds.

Run: PYTHONPATH=<dir containing mpmath> python3 -s theorem_8_0_1.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp
from mpmath import mpf, mpc, pi, exp, sqrt, gamma, fabs, acos, sin, tan, cos, sec

mp.mp.dps = 40


def F_series(sigma, tau, delta):
    z = 2j * pi * mpf(delta)
    dps = int(40 + float((2 * pi * delta) ** 2 / 2) / 2.3 + 2 * abs(float(tau)))
    with mp.workdps(dps):
        s = mpc(sigma, tau)
        tot, pre, n, mx = mpc(0), mpc(1), 0, mpf(0)
        while True:
            t = pre * mpf(2) ** ((n + s) / 2) * gamma((n + s) / 2)
            tot += t
            a = fabs(t)
            mx = max(mx, a)
            if n > 10 and n > 2 * fabs(z) ** 2 and a < mx * mpf(10) ** (-dps):
                break
            n += 1
            pre *= z / n
        r = tot / 2
    return +r


def F_pcfu(sigma, tau, delta, dps=60):
    with mp.workdps(dps):
        s = mpc(sigma, tau)
        r = exp((pi * 1j * delta) ** 2) * gamma(s) * mp.pcfu(s - mpf(1) / 2, -2j * pi * delta)
    return +r


def x0_of(tau, delta):
    ell = -2 * pi * mpf(delta)
    rho = 4 * fabs(tau) / ell ** 2
    j = sqrt(1 + rho ** 2)
    return fabs(ell) / 2 * sqrt((j - 1) / 2), rho


def rhs83(sigma, tau, delta):
    ell = -2 * pi * mpf(delta)
    x0, _ = x0_of(tau, delta)
    s = mpc(sigma, tau)
    return (x0 ** (-sigma) * exp(-ell ** 2 / 2) * fabs(gamma(s)) * exp(pi / 2 * fabs(tau))
            * ((1 + pi / mpf(2) ** mpf(1.5)) * exp(-pi / 4 * fabs(tau)) + exp(-pi * fabs(tau)) / 2))


def bound81(sigma, tau, ell):
    """(8.1) exactly as printed, with the given (possibly negative) tau and ell.
    tau^{sigma/2} is read as |tau|^{sigma/2} (the only real reading)."""
    s = mpc(sigma, tau)
    rho = 4 * tau / ell ** 2
    ups = sqrt((1 + sqrt(rho ** 2 + 1)) / 2)
    E = (acos(1 / ups) - 2 * (ups - 1) / rho) / 2
    c1 = (1 + mpf(2) ** 0.25 * (2 / (1 + sin(pi / 8) ** 2)) ** (sigma / 2)
          + exp(-(sqrt(2) - 1) / 2 * tau) / tan(pi / 8) ** sigma) / 2
    c2 = (1 + min(mpf(2) ** (sigma + 0.5), sqrt(sec(2 * pi / 5)) / sin(pi / 5) ** sigma)
          + exp(-tau / 6) / (1 / sqrt(3)) ** sigma) / 2
    pre = fabs(gamma(s)) * exp(pi / 2 * tau) * exp(-E * tau)
    b1 = pre * c1 / fabs(tau) ** (sigma / 2)
    b2 = pre * c2 / ell ** sigma if rho <= 1.5 else None
    return rho, b1, b2


# (i)
print("(i) (8.3) at good-sign points (tau > 0, delta > 0):")
i_ok = True
for sigma, tau, delta in [(1, 1, 1), (1, 20, 2), (1, 20, 3)]:
    A, B = F_series(sigma, tau, delta), F_pcfu(sigma, tau, delta)
    R = rhs83(sigma, tau, delta)
    _, rho = x0_of(tau, delta)
    agree = fabs(A - B) <= mpf(10) ** -20 * fabs(A)
    i_ok = i_ok and agree and fabs(A) > R
    print("  s=%d+%di delta=%d rho=%.5f |F|=%s (series), %s (pcfu); RHS(8.3)=%s" % (
        sigma, tau, delta, float(rho), mp.nstr(fabs(A), 12), mp.nstr(fabs(B), 12), mp.nstr(R, 6)))
ell = -2 * pi
x0, _ = x0_of(1, 1)
I = mp.quad(lambda y: exp(-(y - ell) ** 2 / 2), [-mp.inf, ell, -x0])
print("  L_3 step at ell=-2pi: integral = %s, claimed bound sqrt(pi/2)e^{-ell^2/2} = %s" % (
    mp.nstr(I, 8), mp.nstr(sqrt(pi / 2) * exp(-ell ** 2 / 2), 4)))
i_ok = i_ok and I > sqrt(pi / 2) * exp(-ell ** 2 / 2)
print("  large ell, tau = 400, sigma = 1: log10(|F|/RHS(8.3)):")
lr = {}
for r in ('0.813', '0.82'):
    rho = mpf(r)
    delta = sqrt(4 * mpf(400) / rho) / (2 * pi)
    F1, F2 = F_pcfu(1, 400, delta, 60), F_pcfu(1, 400, delta, 90)
    lr[r] = mp.log10(fabs(F2) / rhs83(1, 400, delta))
    i_ok = i_ok and fabs(F1 - F2) <= mpf(10) ** -20 * fabs(F2)
    print("    rho=%s: %s" % (r, mp.nstr(lr[r], 6)))
i_ok = i_ok and lr['0.813'] > 0 and lr['0.82'] < 0
print("  root of rho^2 + 6 pi rho = 16:", mp.nstr(mp.findroot(lambda r: r ** 2 + 6 * pi * r - 16, 0.8), 7))

# (ii)
print("\n(ii) x0/sqrt(tau) = sqrt((j(rho)-1)/(2 rho)):")
ratio = lambda rho: sqrt((sqrt(1 + rho ** 2) - 1) / (2 * rho))
for r in ('0.1', '0.5', '1', '1.4', '1.5', '2'):
    print("  rho=%s: %s" % (r, mp.nstr(ratio(mpf(r)), 7)))
rstar = mp.findroot(lambda r: ratio(r) - mpf('0.51729'), 1.5)
print("  equals 0.51729 at rho* = %s" % mp.nstr(rstar, 9))
ii_ok = ratio(mpf('0.5')) < mpf('0.51729') and ratio(mpf('1.4')) < mpf('0.51729') and rstar > 1.49

# (iii)
print("\n(iii) s = 1-20i, delta = 1 (sgn(delta) != sgn(tau), so (8.1) applies):")
A = F_series(1, -20, 1)
B = F_pcfu(1, -20, 1)
Cc = mp.conj(F_series(1, 20, -1))  # F_delta(conj s) = conj F_{-delta}(s)
print("  |F| = %s (series), %s (pcfu), %s (conj of F_{-1}(1+20i))" % (
    mp.nstr(fabs(A), 12), mp.nstr(fabs(B), 12), mp.nstr(fabs(Cc), 12)))
rho, b1, b2 = bound81(1, mpf(-20), -2 * pi)
print("  literal (8.1): rho=%s, case 1 = %s, case 2 = %s" % (mp.nstr(rho, 5), mp.nstr(b1, 6), mp.nstr(b2, 6)))
rhoa, b1a, b2a = bound81(1, mpf(20), 2 * pi)
print("  (8.1) with |tau|, |ell|: rho=%s, case 1 = %s, case 2 = %s" % (mp.nstr(rhoa, 5), mp.nstr(b1a, 6), mp.nstr(b2a, 6)))
lit_fails = fabs(A) > b1 and (b2 is None or b2 < 0 or fabs(A) > b2)
abs_holds = fabs(A) <= b1a and (b2a is None or fabs(A) <= b2a)
iii_ok = lit_fails and abs_holds and fabs(A - B) <= mpf(10) ** -20 * fabs(A)

print("\nparts: (i) %s, (ii) %s, (iii) %s" % (i_ok, ii_ok, iii_ok))
if i_ok and ii_ok and iii_ok:
    print("CONFIRMED: (8.3) is false for small rho (|F(1+i)|=0.01747 with delta=1 against 4.2e-8; at tau=400 it fails at rho=0.813 and holds at rho=0.82), the first case of (8.4) fails for rho<1.49997, and (8.1) holds for tau<0 only with absolute values.")
else:
    print("NOT CONFIRMED: (i)=%s (ii)=%s (iii)=%s." % (i_ok, ii_ok, iii_ok))
