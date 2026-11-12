"""Check of [H, Eq (9.33)] (eq:gargara, proof of Lemma 9.2.1).

Claim: the identity before (9.33), sum_{|Im rho|>T0}|F(rho)| =
sum_{Im rho>T0}(|F(rho)| + |F(1-rho)|), assumes the zeros of L(s,chi) come in
pairs rho, 1-rho. The functional equation sends a zero of L(s,chi) to a zero
1-rho of L(s,chi-bar); zeros of L(s,chi) are only symmetric under rho -> 1-conj(rho).
So for complex chi the identity fails.

Book inputs (expform.tex):
  - l.803-812: the identity and "the functional equation (which implies that
    non-trivial zeros come in pairs rho, 1-rho)"; l.813-817 (9.33).
  - l.771-775: chi any primitive character mod q, zeros with |Im rho| <= T0 on
    Re s = 1/2 (GRH to height T0).
Test: chi mod 5 with chi(2) = i (chi(1,2,3,4) = 1, i, -i, -1; odd, complex,
primitive). L via mpmath.dirichlet. Zeros on Re s = 1/2 located by sign changes
of the real function Z(t) = eps^{-1/2} (5/pi)^{s/2} Gamma((s+1)/2) L(s,chi) / |Gamma|,
eps the root number (computed numerically), on 50 < |t| < 90, refined by findroot.

Confirms if: the ordinates in (50,55) and the negatives of those in (-55,-50)
differ, |L(1-rho, chi)| is far from 0 at the zero rho with smallest t > 50,
and the counts above and below differ.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_9_33.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 20
chi = [0, 1, 1j, -1j, -1]
chib = [0, 1, -1j, 1j, -1]
q = 5


def Lam(s, c):
    return (mp.mpf(q) / mp.pi) ** (s / 2) * mp.gamma((s + 1) / 2) * mp.dirichlet(s, c)


s0 = mp.mpf("0.3") + 2j
eps = Lam(s0, chi) / Lam(1 - s0, chib)
s1 = mp.mpf("0.7") + 5j
eps1 = Lam(s1, chi) / Lam(1 - s1, chib)
print("root number eps =", mp.nstr(eps, 12), " |eps| =", mp.nstr(abs(eps), 12),
      " (check at second point:", mp.nstr(eps1, 12), ")")
rot = 1 / mp.sqrt(eps)


def Zc(t):
    s = mp.mpf(0.5) + 1j * t
    return rot * Lam(s, chi) / abs(mp.gamma((s + 1) / 2))


maxim = 0
def zeros_in(a, b, h=mp.mpf("0.02")):
    global maxim
    out = []
    t = mp.mpf(a)
    zprev = Zc(t)
    while t < b:
        t2 = t + h
        z2 = Zc(t2)
        maxim = max(maxim, abs(mp.im(z2)) / (abs(z2) + 1e-30) if abs(z2) > 1e-6 else 0)
        if mp.re(zprev) * mp.re(z2) < 0:
            r = mp.findroot(lambda u: mp.re(Zc(u)), (t, t2), solver="anderson")
            out.append(r)
        t, zprev = t2, z2
    return out


up = zeros_in(50, 90)
down = [-r for r in zeros_in(-90, -50)]
print("max |Im Z|/|Z| on the grid (should be ~0):", mp.nstr(maxim, 3))
up55 = [r for r in up if r < 55]
down55 = sorted(r for r in down if r < 55)
print("zeros 1/2+it, 50 < t < 55:", [mp.nstr(r, 9) for r in up55])
print("zeros 1/2-it, 50 < t < 55:", [mp.nstr(r, 9) for r in down55])
print("counts in 50 < |t| < 90: above", len(up), " below", len(down))
rho = mp.mpf(0.5) + 1j * up[0]
a = abs(mp.dirichlet(rho, chi))
b = abs(mp.dirichlet(1 - rho, chi))
c = abs(mp.dirichlet(1 - rho, chib))
print("rho = 1/2 + %si: |L(rho,chi)| = %s, |L(1-rho,chi)| = %s, |L(1-rho,chibar)| = %s"
      % (mp.nstr(up[0], 9), mp.nstr(a, 3), mp.nstr(b, 6), mp.nstr(c, 3)))
mismatch = min(abs(u - d) for u in up55 for d in down55) > 0.01

if mismatch and a < 1e-8 and b > 0.5 and c < 1e-8:
    print("CONFIRMED: for chi mod 5 with chi(2) = i the zeros are not symmetric under rho -> 1-rho: "
          "1/2+%si is a zero but |L(1-rho,chi)| = %s (1-rho is a zero of L(s,chi-bar))."
          % (mp.nstr(up[0], 7), mp.nstr(b, 4)))
else:
    print("NOT CONFIRMED: zeros of L(s,chi) looked symmetric under rho -> 1-rho in the tested range.")
