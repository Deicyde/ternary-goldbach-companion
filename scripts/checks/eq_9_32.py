"""Check of [H, Eq (9.32)] (eq:datora, proof of Lemma 9.1.4).

Claim: the justification after (9.32), "f(sigma+i tau) = f(sigma-i tau) (because
eta is real-valued)", is false for delta != 0: conj G_delta(s) = G_{-delta}(conj s),
so |G_delta(1/2-i tau)| = |G_{-delta}(1/2+i tau)| differs from |G_delta(1/2+i tau)|.
Hence the sum over 1<|gamma|<=T0 of |G_delta(rho)| is not sum f(|gamma|), and the
next step, (1/pi) int_1^{T0} |f|^2 <= |eta|_2^2, fails.

Book inputs (expform.tex):
  - l.616-626: Lemma 9.1.4, eta real, G_delta = Mellin transform of eta(t)e(delta t),
    e(x) = exp(2 pi i x); T0 >= 1.
  - l.670-673: f(t) = |G_delta(1/2+it)| for t <= T0, 0 for t > T0.
  - l.674-681 (9.32) and the symmetry sentence; l.689-695: (1/pi) int_1^{T0}|f|^2 <= |eta|_2^2.
Test function eta(t) = t^2 e^{-t^2/2} (one of the book's uses), |eta|_2^2 = 3 sqrt(pi)/8.
G_delta(s) is computed by quadrature on two rotated rays t = r e^{i theta}
(they must agree), and checked at delta = 0 against 2^{s/2} Gamma(s/2+1).

Confirms if: |G_delta(1/2+5i)| and |G_delta(1/2-5i)| differ greatly at delta = 1,
the latter equals |G_{-delta}(1/2+5i)|, and (1/pi) int_1^{40} |G_{-2}(1/2+iT)|^2 dT
exceeds |eta|_2^2.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_9_32.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 20


def G(delta, s, theta=None):
    if theta is None:
        theta = 0.5 if delta >= 0 else -0.5
    w = mp.e ** (1j * theta)
    h = lambda r: (r * w) ** (s + 1) * mp.e ** (-(r * w) ** 2 / 2 + 2j * mp.pi * delta * r * w) * w
    return mp.quad(h, [0, 1, 3, 6, 12, mp.inf])


s0 = mp.mpf(0.5) + 3j
print("delta=0 check: quad", mp.nstr(G(0, s0), 12), " closed form", mp.nstr(2 ** (s0 / 2) * mp.gamma(s0 / 2 + 1), 12))
d = 1
sp, sm = mp.mpf(0.5) + 5j, mp.mpf(0.5) - 5j
gp, gp2 = G(d, sp), G(d, sp, 0.3)
gm, gm2 = G(d, sm), G(d, sm, 0.3)
gneg = G(-d, sp)
print("delta=1: |G(1/2+5i)| = %s (theta 0.5) / %s (theta 0.3)" % (mp.nstr(abs(gp), 6), mp.nstr(abs(gp2), 6)))
print("         |G(1/2-5i)| = %s (theta 0.5) / %s (theta 0.3)" % (mp.nstr(abs(gm), 6), mp.nstr(abs(gm2), 6)))
print("         |G_{-1}(1/2+5i)| = %s" % mp.nstr(abs(gneg), 6))
ok1 = abs(gm) > 1e5 * abs(gp) and abs(abs(gm) - abs(gneg)) < 1e-10 and abs(gp - gp2) < 1e-12 and abs(gm - gm2) < 1e-10

d, T0 = -2, 40
eta2 = 3 * mp.sqrt(mp.pi) / 8
I = mp.quad(lambda T: abs(G(d, mp.mpf(0.5) + 1j * T)) ** 2, mp.linspace(1, T0, 14)) / mp.pi
jump = abs(G(d, mp.mpf(0.5) + 10j))
print("delta=-2: (1/pi) int_1^40 |G(1/2+iT)|^2 dT = %s vs |eta|_2^2 = %s" % (mp.nstr(I, 6), mp.nstr(eta2, 6)))
print("delta=-2: f(T0) at T0=10 (jump of f to 0) = %s" % mp.nstr(jump, 6))
ok2 = I > eta2

if ok1 and ok2:
    print("CONFIRMED: for eta = t^2 e^{-t^2/2}, |G_1(1/2+5i)| = %s but |G_1(1/2-5i)| = %s = |G_{-1}(1/2+5i)|, and at "
          "delta = -2 (1/pi) int_1^40 |f|^2 = %s > |eta|_2^2 = %s." % (mp.nstr(abs(gp), 3), mp.nstr(abs(gm), 4),
                                                                       mp.nstr(I, 4), mp.nstr(eta2, 4)))
else:
    print("NOT CONFIRMED: the symmetry held or the Plancherel step held in the tested cases.")
