"""Check of [H, Eq (8.3)] (Theorem 8.0.1, good-sign case sgn(delta) = sgn(tau)).

Claim: the bound (8.3) is false when rho = 4|tau|/ell^2 is small (for large ell,
for every rho below about 0.81), including the range |tau| >= 20 used by
Corollary 8.0.2.  The proof's L_3 step uses the Gaussian tail bound
int_{-oo}^{-ell} e^{-t^2/2} dt <= sqrt(pi/2) e^{-ell^2/2} [AS64, 7.1.13], which
needs ell >= 0, while in this case ell < 0.  A valid version is
|x0|^{-sigma}|Gamma(s)|e^{pi|tau|/2}((1+pi/2^{5/2})e^{-ell^2/2}e^{-pi|tau|/4}
+ e^{-pi|tau|}).

Book inputs (mellintran.tex):
  - l.26-29: f_delta(t) = e^{-t^2/2} e(delta t), F_delta its Mellin transform,
    s = sigma + i tau, sigma >= 0, ell = -2 pi delta (e(x) = e^{2 pi i x},
    notprem.tex l.34; Mellin kernel t^{s-1}, notprem.tex l.222).
  - l.60-65: (8.3) |F| <= |x0|^{-sigma} e^{-ell^2/2}|Gamma(s)| e^{pi|tau|/2}
    ((1+pi/2^{3/2}) e^{-pi|tau|/4} + (1/2) e^{-pi|tau|}).
  - l.66-70: (8.4) lower bounds 0.51729 sqrt(tau), 0.84473|tau|/|ell| for x0.
  - l.498 (8.21) and l.748: x0 = Re u_{0,+} = (|ell|/2) sqrt((j-1)/2),
    j = sqrt(1+rho^2), rho = 4 tau/ell^2.
  - l.1187-1198: the L_3 step with the tail bound.
F_delta(s) is computed two independent ways: the exact series
F = (1/2) sum_n (2 pi i delta)^n/n! 2^{(n+s)/2} Gamma((n+s)/2) (termwise
integration of the definition), and the parabolic-cylinder closed form
F = e^{-pi^2 delta^2} Gamma(s) U(s-1/2, -2 pi i delta) (mpmath pcfu); at s=1+i
also by quadrature of the definition on a rotated ray.

Confirms if: at points with sgn(delta) = sgn(tau) the computed |F| exceeds the
(8.3) right side (also with x0 replaced by its (8.4) lower bound), including a
point with |tau| >= 20 and rho <= 3/2; the L_3 Gaussian integral exceeds the
claimed sqrt(pi/2)e^{-ell^2/2}; on a grid every violation has rho < 0.82 and
there is none for rho >= 1; and the corrected form holds at every grid point.

Run: PYTHONPATH=<dir containing mpmath> python3 -s eq_8_3.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp
from mpmath import mpf, mpc, pi, exp, sqrt, gamma, fabs

mp.mp.dps = 40


def params(tau, delta):
    ell = -2 * pi * mpf(delta)
    rho = 4 * fabs(tau) / ell ** 2
    j = sqrt(1 + rho ** 2)
    x0 = fabs(ell) / 2 * sqrt((j - 1) / 2)
    return ell, rho, x0


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


def F_pcfu(sigma, tau, delta):
    with mp.workdps(60):
        s = mpc(sigma, tau)
        r = exp((pi * 1j * delta) ** 2) * gamma(s) * mp.pcfu(s - mpf(1) / 2, -2j * pi * delta)
    return +r


def F_ray(sigma, tau, delta, theta):
    """Definition integrated along t = r e^{i theta}; valid by Cauchy for |theta| < pi/4."""
    s = mpc(sigma, tau)
    w = exp(1j * mpf(theta))
    g = lambda r: exp(-(r * w) ** 2 / 2 + 2j * pi * delta * r * w) * r ** (s - 1)
    return w ** s * mp.quad(g, mp.linspace(0, 12, 60) + [mp.inf])


def rhs83(sigma, tau, delta, x0):
    ell = -2 * pi * mpf(delta)
    s = mpc(sigma, tau)
    return (x0 ** (-sigma) * exp(-ell ** 2 / 2) * fabs(gamma(s)) * exp(pi / 2 * fabs(tau))
            * ((1 + pi / mpf(2) ** mpf(1.5)) * exp(-pi / 4 * fabs(tau)) + exp(-pi * fabs(tau)) / 2))


def corrected(sigma, tau, delta, x0):
    ell = -2 * pi * mpf(delta)
    s = mpc(sigma, tau)
    return (x0 ** (-sigma) * fabs(gamma(s)) * exp(pi / 2 * fabs(tau))
            * ((1 + pi / mpf(2) ** mpf(2.5)) * exp(-ell ** 2 / 2) * exp(-pi / 4 * fabs(tau))
               + exp(-pi * fabs(tau))))


def x0_low(tau, delta):
    ell, rho, _ = params(tau, delta)
    lows = [mpf('0.51729') * sqrt(fabs(tau))]
    if rho <= 1.5:
        lows.append(mpf('0.84473') * fabs(tau) / fabs(ell))
    return min(lows)   # smallest admissible x0 gives the largest right side


ok = True
print("Point checks (tau > 0, delta > 0, so ell < 0 and sgn(delta) = sgn(tau)):")
big_tau_fail = False
for sigma, tau, delta in [(1, 1, 1), (mpf('0.5'), 1, 1), (1, 20, 2), (1, 20, 3)]:
    ell, rho, x0 = params(tau, delta)
    A = F_series(sigma, tau, delta)
    B = F_pcfu(sigma, tau, delta)
    agree = fabs(A - B) <= mpf(10) ** -20 * fabs(A)
    extra = ""
    if tau == 1 and sigma == 1:
        C = F_ray(sigma, tau, delta, mpf('0.5'))
        agree = agree and fabs(A - C) <= mpf(10) ** -12 * fabs(A)
        extra = " ray(0.5)=%s" % mp.nstr(fabs(C), 15)
    R = rhs83(sigma, tau, delta, x0)
    Rl = rhs83(sigma, tau, delta, x0_low(tau, delta))
    viol = fabs(A) > R and fabs(A) > Rl
    if tau >= 20 and rho <= 1.5 and viol:
        big_tau_fail = True
    ok = ok and agree and viol
    print("  s=%s+%si delta=%s rho=%.5f x0=%.6f: |F| series=%s pcfu=%s%s" % (
        sigma, tau, delta, float(rho), float(x0), mp.nstr(fabs(A), 15), mp.nstr(fabs(B), 15), extra))
    print("      RHS(8.3) exact x0 = %s ; with (8.4) lower bound for x0 = %s ; violated: %s" % (
        mp.nstr(R, 6), mp.nstr(Rl, 6), viol))

print("\nFaulty L_3 step: int_{-oo}^{-x0} e^{-(y-ell)^2/2} dy versus the claimed sqrt(pi/2) e^{-ell^2/2}:")
step_bad = True
for tau, delta in [(1, 1), (20, 2)]:
    ell, rho, x0 = params(tau, delta)
    I = mp.quad(lambda y: exp(-(y - ell) ** 2 / 2), [-mp.inf, ell, -x0])
    cl = sqrt(pi / 2) * exp(-ell ** 2 / 2)
    step_bad = step_bad and I > cl
    print("  ell=%.5f x0=%.5f: integral=%s claimed bound=%s" % (float(ell), float(x0), mp.nstr(I, 8), mp.nstr(cl, 4)))

print("\nGrid: rho in {0.1,...,5}, tau in {2,5,10,20,40}, sigma in {0.25,1,3}:")
rhos = [mpf(r) for r in ('0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.82', '0.9',
                         '1', '1.2', '1.5', '2', '3', '5')]
nviol = npts = 0
max_rho_viol = mpf(0)
viol_ge1 = 0
max_corr = mpf(0)
for rho in rhos:
    for tau in (2, 5, 10, 20, 40):
        delta = sqrt(4 * mpf(tau) / rho) / (2 * pi)
        _, _, x0 = params(tau, delta)
        for sigma in (mpf('0.25'), mpf(1), mpf(3)):
            F = fabs(F_pcfu(sigma, tau, delta))
            npts += 1
            if F > rhs83(sigma, tau, delta, x0):
                nviol += 1
                max_rho_viol = max(max_rho_viol, rho)
                if rho >= 1:
                    viol_ge1 += 1
            max_corr = max(max_corr, F / corrected(sigma, tau, delta, x0))
print("  %d of %d points violate (8.3); largest violating rho = %s; violations with rho >= 1: %d" % (
    nviol, npts, mp.nstr(max_rho_viol, 4), viol_ge1))
print("  corrected form: max |F|/bound = %s" % mp.nstr(max_corr, 6))
print("  coefficient: (pi^{3/2}/4)/sqrt(2 pi) = %s = pi/2^{5/2} = %s; printed pi/2^{3/2} = %s" % (
    mp.nstr(pi ** 1.5 / 4 / sqrt(2 * pi), 8), mp.nstr(pi / mpf(2) ** 2.5, 8), mp.nstr(pi / mpf(2) ** 1.5, 8)))

grid_ok = nviol > 0 and max_rho_viol < mpf('0.82') and viol_ge1 == 0 and max_corr < 1
if ok and big_tau_fail and step_bad and grid_ok:
    print("CONFIRMED: (8.3) fails at points with sgn(delta)=sgn(tau) and small rho (e.g. s=1+i, delta=1: |F|=0.01747 against 4.2e-8; s=1+20i, delta=2: 1.29e-28 against 1.18e-40), because the L_3 tail bound is applied with ell<0, while the corrected form holds on the grid.")
else:
    print("NOT CONFIRMED: points ok=%s, |tau|>=20 failure=%s, faulty step=%s, grid pattern=%s." % (
        ok, big_tau_fail, step_bad, grid_ok))
