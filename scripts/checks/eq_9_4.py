"""Check of [H, Eq (9.4)] (proof of Lemma 9.1.1, exchange of sum and integral).

Claim: the swap of sum_n and the integral on Re s = 3/2 in (9.4) is justified
only by "G_delta bounded on Re s = 3/2 and sum Lambda(n) n^{-3/2} finite"; this
does not give absolute integrability, and under the lemma's hypotheses G_delta
need not be in L^1 on Re s = 3/2.  Counterexample:
eta(t) = psi0(t) t^{-1.6} sin(sqrt t), psi0 smooth, 0 on [0,1], 1 on [2,oo),
delta = 0, for which |G_0(3/2+i tau)| ~ 2^{-1.2} sqrt(4 pi) tau^{-0.7}.

Book inputs:
  - expform.tex:98-107  hypotheses of Lemma 9.1.1: eta in C^1; eta, eta' in
    L^2; eta t^{sigma-1}, eta' t^{sigma-1} in L^1 for sigma in an open interval
    containing [1/2, 3/2].  (Example: |eta| <= t^{-1.6}, eta' = O(t^{-2.1}),
    so sigma in (0, 1.6) works.)
  - expform.tex:143-157  the stated justification and the swap (9.4).
  - notprem.tex:221-223  Mellin convention M f(s) = int_0^oo f(x) x^{s-1} dx.
Tonelli needs x^{3/2} sum Lambda(n) n^{-3/2} * int |G_0(3/2+i tau)| d tau < oo.

Confirms if tau^{0.7} |G_0(3/2+i tau)| computed by quadrature is within 1e-3
of 2^{-1.2} sqrt(4 pi) = 1.54301 at tau = 100, 400, 1600 (and agrees with the
closed form 2 Gamma(w) sin(pi w/2), w = 2s - 3.2, of the uncut transform), so
|G_0| >= 1.5 tau^{-0.7} for large tau and int |G_0| = oo.  The check concerns
only the printed justification; it does not claim (9.4) is false.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_9_4.py

Ported from a 2026-11-06 check script.
"""
import math, cmath
import mpmath as mp


def S(x):  # smooth step: 0 for x <= 0, 1 for x >= 1
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    a, b = math.exp(-1 / x), math.exp(-1 / (1 - x))
    return a / (a + b)


def simpson(tau, V, steps_per_rad=6.0):
    # G_0(3/2+i tau) = int psi0(t) t^{-1.1+i tau} sin(sqrt t) dt; t = u^2, u = e^v:
    # = int_0^V 2 S(u^2-1) u^{-0.2} sin(u) e^{2 i tau v} dv
    rate = 2 * tau + math.exp(V)
    n = int(V * rate * steps_per_rad) + 1
    n += n % 2
    h = V / n
    f = lambda v: 2 * S(math.exp(2 * v) - 1) * math.exp(-0.2 * v) * math.sin(math.exp(v)) * cmath.exp(2j * tau * v)
    s = f(0.0) + f(V)
    for k in range(1, n):
        s += (4 if k % 2 else 2) * f(k * h)
    return s * h / 3


def tail_ibp(tau, U):
    # int_U^oo 2 u^{-1.2} sin(u) u^{2 i tau} du by repeated integration by parts
    total = 0j
    for sg in (1, -1):
        php = lambda u, sg=sg: sg + 2 * tau / u
        b0 = lambda u, sg=sg: u ** -1.2 / (1j * sg)
        def nxt(bk, php=php):
            qf = lambda u: bk(u) / (1j * php(u))
            def d(u):
                h = 1e-3 * u
                return (-qf(u + 2 * h) + 8 * qf(u + h) - 8 * qf(u - h) + qf(u - 2 * h)) / (12 * h)
            return d
        val = 0j; bk = b0
        for k in range(4):
            val += (-1) ** k * (-bk(U) / (1j * php(U)))
            bk = nxt(bk)
        total += val * cmath.exp(1j * (sg * U + 2 * tau * math.log(U)))
    return total


C = 2 ** -1.2 * math.sqrt(4 * math.pi)
print("predicted constant 2^-1.2 sqrt(4 pi) = %.7f" % C)
ok = True
for tau in (100.0, 400.0, 1600.0):
    U = 40 * tau
    g = simpson(tau, math.log(U)) + tail_ibp(tau, U)
    s = mp.mpc(1.5, tau)
    w = 2 * s - mp.mpf("3.2")
    gcl = 2 * mp.gamma(w) * mp.sin(mp.pi * w / 2)  # Mellin of t^{-1.6} sin sqrt t (no cutoff)
    a, acl = tau ** 0.7 * abs(g), float(tau ** 0.7 * abs(gcl))
    print("tau=%6.0f  tau^0.7|G_0| quadrature = %.7f   closed form (no cutoff) = %.7f" % (tau, a, acl))
    if abs(a - C) > 1e-3 or abs(a - acl) > 1e-3:
        ok = False
# lower bound for the integral up to T, using |G_0| >= 1.5 tau^-0.7 on [100, T]
for T in (1e4, 1e8):
    print("int_100^%g 1.5 tau^-0.7 d tau = %.1f" % (T, 1.5 / 0.3 * (T ** 0.3 - 100 ** 0.3)))
if ok:
    print("CONFIRMED: for eta = psi0(t) t^-1.6 sin(sqrt t), which satisfies Lemma 9.1.1's hypotheses, tau^0.7 |G_0(3/2+i tau)| -> 1.54301, so G_0 is not integrable on Re s = 3/2 and the printed justification of the swap in (9.4) fails.")
else:
    print("NOT CONFIRMED: the computed |G_0(3/2+i tau)| does not follow 1.54301 tau^-0.7.")
