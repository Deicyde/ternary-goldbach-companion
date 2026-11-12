"""Eq 1.11: the remark after (1.12) that eta^(-delta) "is just sqrt(2 pi) e^{-2 pi^2 delta^2}".

Claim: with the book's one-sided Gaussian (the transform that the main term of (1.11) actually
is), eta^(-delta) = sqrt(pi/2) e^{-2 pi^2 delta^2} + i sqrt(2) D(sqrt(2) pi delta), D = Dawson's
integral, so the remark's value sqrt(2 pi) e^{-2 pi^2 delta^2} is false; read with the two-sided
value instead, (1.11)-(1.12) fail at q = 1, delta = 0 for large x.

Book inputs:
  - introductionp.tex:866-885: eta(t) = e^{-t^2/2}, x >= 10^8, (1.11) main term
    I_{q=1} eta^(-delta) x, (1.12) |E| <= 4.306e-22 + (650400/sqrt(q) + 112)/sqrt(x), and the
    remark "eta^(-delta) is just sqrt(2 pi) e^{-2 pi^2 delta^2}".
  - expform.tex:926-927: "we set eta_heart(t) = 0 for t < 0" (one-sided Gaussian).
  - expform.tex:228-230: G_delta(1) = int_0^infty eta(t) e(delta t) dt = eta^(-delta).

Confirms if: (a) the one-sided transform (by quadrature and by the Dawson closed form) has real
part exactly half the remark's value and a nonzero imaginary part at delta = 0.1 and 2;
(b) (1/x) sum_n Lambda(n) e^{-(n/x)^2/2} at x = 10^6, 3*10^6 is near sqrt(pi/2), not sqrt(2 pi);
(c) with the two-sided main term, |E| -> sqrt(2pi) - sqrt(pi/2) exceeds the (1.12) bound for
x beyond (650512/(sqrt(pi/2) - 4.306e-22))^2 ~ 2.694e11.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_1_11.py

Ported from a 2026-11-06 check script.
"""
import math
import mpmath as mp

mp.mp.dps = 40


def remark(d):
    return mp.sqrt(2 * mp.pi) * mp.exp(-2 * mp.pi ** 2 * d ** 2)


def one_sided_closed(d):
    z = mp.sqrt(2) * mp.pi * d
    dawson = mp.sqrt(mp.pi) / 2 * mp.exp(-z * z) * mp.erfi(z)
    return mp.mpc(mp.sqrt(mp.pi / 2) * mp.exp(-2 * mp.pi ** 2 * d ** 2), mp.sqrt(2) * dawson)


def one_sided_quad(d):
    # int_0^inf e^{-t^2/2} e(delta t) dt, e(u) = exp(2 pi i u)
    f = lambda t: mp.exp(-t * t / 2) * mp.expjpi(2 * d * t)
    pts = [0] + [k for k in range(1, 41)]
    return mp.quad(f, pts)


ok = True
print("(a) one-sided transform vs the remark")
for ds in ["0", "0.1", "2"]:
    d = mp.mpf(ds)
    r, c, q = remark(d), one_sided_closed(d), one_sided_quad(d)
    agree = abs(c - q) < mp.mpf("1e-25")
    ratio = c.real / r
    print("  delta=%-4s remark=%s  one-sided closed=%s  quad=%s  Re/remark=%s  closed==quad:%s"
          % (ds, mp.nstr(r, 12), mp.nstr(c, 12), mp.nstr(q, 12), mp.nstr(ratio, 15), agree))
    ok &= agree and abs(ratio - mp.mpf("0.5")) < mp.mpf("1e-30")
    if d != 0:
        ok &= abs(c.imag) > mp.mpf("0.05")


def primes_upto(N):
    s = bytearray([1]) * (N + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(N) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(range(i * i, N + 1, i)))
    return [i for i in range(N + 1) if s[i]]


print("(b) (1/x) sum Lambda(n) e^{-(n/x)^2/2}")
PR = primes_upto(int(9 * 3e6))
s1, s2 = math.sqrt(math.pi / 2), math.sqrt(2 * math.pi)
for x in (1e6, 3e6):
    N = int(9 * x)
    c = 1.0 / (2 * x * x)
    terms = []
    for p in PR:
        if p > N:
            break
        lp = math.log(p)
        pk = p
        while pk <= N:
            terms.append(lp * math.exp(-pk * pk * c))
            pk *= p
    v = math.fsum(terms) / x
    print("  x=%.0e  S/x=%.9f  minus sqrt(pi/2)=%+.3e  minus sqrt(2pi)=%+.6f" % (x, v, v - s1, v - s2))
    ok &= abs(v - s1) < 1e-5 and abs(v - s2) > 1.2

print("(c) two-sided reading at q=1, delta=0")
gap = s2 - s1
thr = (650512 / (s1 - 4.306e-22)) ** 2
print("  |E| -> sqrt(2pi)-sqrt(pi/2) = %.7f ; bound 4.306e-22+650512/sqrt(x) < that for x > %.6e" % (gap, thr))
print("  bound at x=1e8: %.4f" % (4.306e-22 + 650512 / 1e4))
ok &= 2.69e11 < thr < 2.70e11

if ok:
    print("CONFIRMED: the book's one-sided transform is sqrt(pi/2)e^{-2pi^2 d^2} + i sqrt2 D(sqrt2 pi d), "
          "half the remark's real value plus an imaginary part, and with the remark's two-sided value "
          "(1.11)-(1.12) fail at q=1, delta=0 for x > 2.694e11.")
else:
    print("NOT CONFIRMED: the computed transform or prime sum does not match the claim.")
