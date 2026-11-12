"""Check of [H, Eq (8.47)] (and (8.3) of Thm 8.0.1), case sgn(delta) = sgn(tau), delta != 0.

Claim: (8.47) and (8.3) are false as printed. In the L_3 estimate (ell < 0) the book uses
int_{-oo}^{-ell} e^{-t^2/2} dt <= sqrt(pi/2) e^{-ell^2/2} ([AS64, 7.1.13]), valid only
for ell >= 0; for ell < 0 the integral is >= sqrt(pi/2), so the e^{-tau pi/2} term loses
its factor e^{-ell^2/2}.

Book inputs (mellintran.tex):
  - l.26-29: f_delta(t) = e^{-t^2/2} e(delta t), F_delta its Mellin transform, ell = -2 pi delta.
  - l.60-65 (8.3): |F| <= |x0|^{-sigma} e^{-ell^2/2} |Gamma(s)| e^{pi|tau|/2}
        ((1 + pi/2^{3/2}) e^{-pi|tau|/4} + (1/2) e^{-pi|tau|}).
  - l.401-405 (8.11): F = e^{-2pi^2 delta^2} Gamma(s)/(sqrt(2pi) i) int e^{2pi i delta u + u^2/2} u^{-s} du.
  - l.498-502 (damherr): x0 = Re u_{0,+} = (|ell|/2) sqrt((j(rho)-1)/2), j = sqrt(1+rho^2), rho = 4tau/ell^2.
  - l.1187-1198: L_3 bound and the use of [AS64, 7.1.13].
  - l.1236-1244 (8.47): for ell < 0, tau >= 0,
        |F| <= |x0|^{-sigma} ((1 + pi/2^{3/2}) e^{-Re phi(u0+)} + (1/2) e^{-tau pi/2}) e^{-ell^2/2} |Gamma(s)|,
    with l.1246-1248: -Re phi(u0+) = (ell^2/4)(1 - upsilon) + (tau/2) arccos(1/upsilon).

F_delta(s) is computed two independent ways: quadrature of the Mellin integral on a rotated
ray t = r e^{i theta}, and the closed form e^{(pi i delta)^2} Gamma(s) U(s - 1/2, -2 pi i delta)
(parabolic cylinder function). u_{0,+} is also recomputed directly as the saddle of phi.

Confirms if: at delta > 0, tau > 0 (so ell < 0), the two evaluations of |F| agree and |F|
exceeds the right sides of both (8.47) and (8.3), and the L_3 Gaussian integral exceeds the
book's bound sqrt(pi/2) e^{-ell^2/2}; also reports that the bound without e^{-ell^2/2} on the
L_3 term holds at the test points.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_8_47.py   (mpmath 1.3.0; -E would drop PYTHONPATH)

Ported from a 2026-11-06 check script.
"""
import mpmath as mp
from mpmath import mpf, mpc, pi, exp, sqrt, gamma, quad, inf, acos

mp.mp.dps = 40


def F_ray(delta, s, theta):
    e = exp(1j * theta)
    f = lambda r: exp(-(r * e) ** 2 / 2 + 2j * pi * delta * r * e) * (r * e) ** (s - 1) * e
    return quad(f, [0, mpf('0.01'), mpf('0.1'), mpf('0.5'), 1, 2, 3, 4, 6, 9, 14, inf])


def F_pcfu(delta, s):
    return exp((pi * 1j * delta) ** 2) * gamma(s) * mp.pcfu(s - mpf(1) / 2, -2j * pi * delta)


def book_quantities(delta, s):
    sigma, tau = s.real, s.imag
    ell = -2 * pi * delta
    rho = 4 * tau / ell ** 2
    j = sqrt(1 + rho ** 2)
    ups = sqrt((1 + j) / 2)
    x0 = abs(ell) / 2 * sqrt((j - 1) / 2)
    mrephi = ell ** 2 / 4 * (1 - ups) + tau / 2 * acos(1 / ups)
    # direct saddle: phi(u) = -u^2/2 + i ell u + i tau log u, phi'(u) = 0 <=> u^2 - i ell u - i tau = 0
    r = mp.polyroots([1, -1j * ell, -1j * tau])
    u0 = [u for u in r if mp.re(u) > 0][0]
    phi = lambda u: -u ** 2 / 2 + 1j * ell * u + 1j * tau * mp.log(u)
    return ell, rho, x0, mrephi, u0, -mp.re(phi(u0))


def main():
    c = 1 + pi / mpf(2) ** mpf('1.5')
    cases = [(mpf(1), mpc('0.5', 1)), (mpf('0.6'), mpc('0.5', 1)), (mpf('1.6'), mpc('0.5', 1)),
             (mpf(1), mpc(1, 1)), (mpf(1), mpc('0.5', 3))]
    allfail = True
    l3fail = True
    corr_ok = True
    for delta, s in cases:
        sigma, tau = s.real, s.imag
        ell, rho, x0, mrephi, u0, mrephi_direct = book_quantities(delta, s)
        Fa = F_ray(delta, s, mpf('0.3'))
        Fb = F_ray(delta, s, mpf('0.6'))
        Fc = F_pcfu(delta, s)
        agree = max(abs(Fa - Fc), abs(Fb - Fc)) / abs(Fc)
        G = abs(gamma(s))
        r847 = x0 ** (-sigma) * (c * exp(mrephi) + exp(-tau * pi / 2) / 2) * exp(-ell ** 2 / 2) * G
        r83 = x0 ** (-sigma) * exp(-ell ** 2 / 2) * G * exp(pi / 2 * tau) * (
            c * exp(-pi / 4 * tau) + exp(-pi * tau) / 2)
        gaussL3 = quad(lambda y: exp(-(y - ell) ** 2 / 2), [-inf, ell, -x0])
        bookL3 = sqrt(pi / 2) * exp(-ell ** 2 / 2)
        corr = x0 ** (-sigma) * (c * exp(mrephi) * exp(-ell ** 2 / 2) + exp(-tau * pi / 2)) * G
        F = abs(Fc)
        print("delta=%s s=%s ell=%s rho=%s" % (delta, mp.nstr(s, 4), mp.nstr(ell, 8), mp.nstr(rho, 6)))
        print("  x0=%s (direct Re u0+ = %s); -Re phi(u0+) book=%s direct=%s"
              % (mp.nstr(x0, 10), mp.nstr(mp.re(u0), 10), mp.nstr(mrephi, 10), mp.nstr(mrephi_direct, 10)))
        print("  |F| pcfu=%s ray0.3=%s ray0.6=%s rel.diff=%s"
              % (mp.nstr(F, 12), mp.nstr(abs(Fa), 12), mp.nstr(abs(Fb), 12), mp.nstr(agree, 3)))
        print("  RHS(8.47)=%s RHS(8.3)=%s" % (mp.nstr(r847, 6), mp.nstr(r83, 6)))
        print("  L3 Gaussian integral=%s vs book bound sqrt(pi/2)e^{-ell^2/2}=%s"
              % (mp.nstr(gaussL3, 10), mp.nstr(bookL3, 6)))
        print("  bound without e^{-ell^2/2} on L3 term = %s, holds: %s" % (mp.nstr(corr, 8), F <= corr))
        sane = agree < mpf('1e-15') and abs(x0 - mp.re(u0)) < mpf('1e-20') and abs(mrephi - mrephi_direct) < mpf('1e-20')
        if not sane:
            print("  WARNING: evaluations disagree")
        allfail = allfail and sane and F > r847 and F > r83
        l3fail = l3fail and gaussL3 > bookL3
        corr_ok = corr_ok and F <= corr
    print("delta=0 control: |F_0(1/2+i)| =", mp.nstr(abs(F_ray(0, mpc('0.5', 1), mpf('0.3'))), 10))
    if allfail and l3fail:
        print("CONFIRMED: at every test point with ell<0, tau>0, |F_delta(s)| (two methods agreeing) exceeds "
              "the right sides of (8.47) and (8.3), because the L_3 Gaussian integral exceeds the book's bound "
              "sqrt(pi/2)e^{-ell^2/2}; dropping e^{-ell^2/2} from the L_3 term %s." %
              ("restores the bound at all test points" if corr_ok else "does not restore it everywhere"))
    else:
        print("NOT CONFIRMED: (8.47)/(8.3) were not violated at every test point.")


main()
