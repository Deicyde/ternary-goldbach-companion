"""Check of [H, Lemma 9.1.1] (explicit formula, eq. (9.1)-(9.2)).

Claim: for q > 1, chi even and eta(0) != 0, Lemma 9.1.1 is false as printed:
the residue at s = 0 of (L'/L)(s,chi) G_delta(s) x^s is a double-pole residue
b*eta(0) + c_0 + eta(0) log x, while (9.2) gives the x-independent
R = eta(0)(log(2pi/q) + gamma - L'(1,chi)/L(1,chi)) + O*(c_0).  Secondary slip:
the constant 226.844 is the integral over |tau| <= 10^5 only; over R it is
226.8499, and sqrt(226.8499/2pi) <= 6.01 still holds.

Book inputs:
  - expform.tex:98-132  Lemma 9.1.1: (9.1) error O*((log q + 6.01)(|eta'|_2 +
    2 pi |delta| |eta|_2)) x^{-1/2}; (9.2) R as above; (9.3) c_0.
  - expform.tex:219-227  (9.7) integrand -(L'/L) G_delta x^s, but
    "R = Res_{s=0} L'/L G_delta(s)" (no x^s).
  - expform.tex:363-367  integral of (1/2 log(tau^2+9/4) + 4.1396 + log pi)^2
    /(1/4 + tau^2) bounded by 226.844; footnote: integrated over [-1e5, 1e5].
  - expform.tex:930-944  Gaussian norms |eta'|_2^2 = sqrt(pi)/4,
    |eta/sqrt t|_1-type norms 1.03045, 1.07791.
Test case: eta(t) = exp(-t^2/2) (eta(0) = 1), delta = 0, chi = (./5) (even,
primitive, q = 5); G_0(s) = 2^{s/2-1} Gamma(s/2).

Confirms if: (a) the residue of (L'/L) G x^s at 0 (contour integral) equals
b + c_0 + log x and varies with x, while the book's R does not; (b) end to
end, LHS + sum_rho G(rho) x^rho + b violates the printed bound
|.| <= c_0-bound + E x^{-1/2} for some x >= 100, while the corrected identity
holds to high accuracy.

Run: PYTHONPATH=<mpmath dir> python3 -s lemma_9_1_1.py

Ported from a 2026-11-06 check script.
"""
import math
import mpmath as mp

mp.mp.dps = 20
chi = [0, 1, -1, -1, 1]
q = 5
L = lambda s: mp.dirichlet(s, chi)
dL = lambda s: mp.dirichlet(s, chi, 1)
F = lambda s: mp.power(2, s / 2 - 1) * mp.gamma(s / 2)  # Mellin of exp(-t^2/2)
b = mp.log(2 * mp.pi / q) + mp.euler - dL(1) / L(1)    # book bracket in (9.2)
c0 = (mp.log(2) - mp.euler) / 2                         # true Laurent constant of F at 0
print("chi(-1) =", chi[4], " L(0,chi) =", mp.nstr(L(0), 5))
print("book bracket b = log(2pi/q)+gamma-L'/L(1) =", mp.nstr(b, 12))
print("true c_0 of G_0 =", mp.nstr(c0, 12))

# (a) residue by contour integral on |s| = 1/2
def res0(fun):
    r = mp.mpf("0.5")
    g = lambda th: fun(r * mp.expj(th)) * r * mp.expj(th)
    return mp.quad(g, [0, mp.pi / 2, mp.pi, 3 * mp.pi / 2, 2 * mp.pi]) / (2 * mp.pi)

LL = lambda s: dL(s) / L(s)
ok_a = True
R_book = b + c0
print("\n(a) residues at s=0")
print("Res (L'/L)G (no x^s, the book's R) =", mp.nstr(mp.re(res0(lambda s: LL(s) * F(s))), 12))
for x in [10, 10**3, 10**6]:
    r = mp.re(res0(lambda s: LL(s) * F(s) * mp.power(x, s)))
    pred = b + c0 + mp.log(x)
    print("x=%-8d Res (L'/L)G x^s = %s   b+c0+log x = %s   book R = %s" %
          (x, mp.nstr(r, 12), mp.nstr(pred, 12), mp.nstr(R_book, 12)))
    if abs(r - pred) > 1e-8 or abs(r - R_book) < 1:
        ok_a = False

# (b) end-to-end test of (9.1)
def Z(t):
    s = mp.mpf(0.5) + 1j * t
    th = mp.im(mp.loggamma(s / 2)) + t / 2 * mp.log(mp.mpf(q) / mp.pi)
    return mp.expj(th) * L(s)

TMAX, step = 70, mp.mpf("0.04")
zs = []
t_prev = mp.mpf("0.001"); z_prev = Z(t_prev).real
t = t_prev + step
while t <= TMAX:
    zt = Z(t).real
    if zt == 0 or (zt > 0) != (z_prev > 0):
        zs.append(mp.findroot(lambda u: Z(u).real, (t_prev, t), solver="anderson"))
    t_prev, z_prev = t, zt
    t += step
print("\n(b) %d zeros with 0<gamma<=%d; first: %s" % (len(zs), TMAX, [mp.nstr(z, 10) for z in zs[:3]]))

def zerosum(x):  # real chi: zeros symmetric under conjugation
    x = mp.mpf(x)
    return 2 * sum(mp.re(F(mp.mpf(0.5) + 1j * g) * mp.power(x, mp.mpf(0.5) + 1j * g)) for g in zs)

def LLm(tau):  # L'/L at -1/2+i tau via the functional equation (kappa = 0, chibar = chi)
    s = mp.mpf(-0.5) + 1j * tau
    return mp.log(mp.pi / q) - mp.digamma(s / 2) / 2 - mp.digamma((1 - s) / 2) / 2 - dL(1 - s) / L(1 - s)

def I(x):
    x = mp.mpf(x)
    g = lambda tau: mp.re(LLm(tau) * F(mp.mpf(-0.5) + 1j * tau) * mp.power(x, mp.mpf(-0.5) + 1j * tau))
    return mp.quad(g, [0, 2, 5, 10, 20, 40, 70]) / mp.pi

def lhs(x):
    N = int(9 * x) + 10
    sv = bytearray([1]) * (N + 1); sv[0:2] = b"\x00\x00"
    for p in range(2, int(N ** 0.5) + 1):
        if sv[p]:
            sv[p * p::p] = bytearray(len(range(p * p, N + 1, p)))
    terms = []
    for p in range(2, N + 1):
        if sv[p] and chi[p % 5] != 0:
            lp = math.log(p); pk = p; ck = chi[p % 5]
            while pk <= N:
                terms.append(ck * lp * math.exp(-0.5 * (pk / x) ** 2))
                pk *= p; ck *= chi[p % 5]
    return mp.mpf(math.fsum(terms))

c0bound = mp.mpf(2) / 3 * (mp.mpf("1.03045") + mp.mpf("1.07791"))  # (9.3), delta = 0
E = (mp.log(q) + mp.mpf("6.01")) * mp.sqrt(mp.sqrt(mp.pi) / 4)
print("printed: |LHS + sum_rho + b| <= %s + %s x^-1/2" % (mp.nstr(c0bound, 8), mp.nstr(E, 8)))
print("%8s %12s %12s %12s %12s" % ("x", "bound", "|D+b|", "log x+c0", "corr.resid"))
fails = 0; ok_corr = True
for x in [10, 100, 1000, 10**4, 10**5]:
    D = lhs(x) + zerosum(x)
    bound = c0bound + E / mp.sqrt(x)
    resid = D + b + c0 + mp.log(x) + I(x)
    print("%8d %12s %12s %12s %12s" % (x, mp.nstr(bound, 6), mp.nstr(abs(D + b), 8),
                                       mp.nstr(mp.log(x) + c0, 8), mp.nstr(resid, 3)))
    if x >= 100 and abs(D + b) > bound:
        fails += 1
    if abs(resid) > 1e-8:
        ok_corr = False

# (c) the constant 226.844
mp.mp.dps = 25
C = mp.mpf("4.1396") + mp.log(mp.pi)
f = lambda t: (mp.log(t * t + mp.mpf(9) / 4) / 2 + C) ** 2 / (mp.mpf(1) / 4 + t * t)
pts = [0, 1, 10, 100, 1000, 10**4, 10**5]
I1 = 2 * mp.quad(f, pts)
I2 = I1 + 2 * mp.quad(f, [10**5, 10**6, 10**8, mp.inf])
print("\n(c) integral on [-1e5,1e5] = %s ; on R = %s" % (mp.nstr(I1, 10), mp.nstr(I2, 10)))
print("sqrt(226.844/2pi) = %s ; sqrt(I_R/2pi) = %s" %
      (mp.nstr(mp.sqrt(mp.mpf("226.844") / (2 * mp.pi)), 8), mp.nstr(mp.sqrt(I2 / (2 * mp.pi)), 8)))
ok_c = I1 <= mp.mpf("226.844") < I2 and mp.sqrt(I2 / (2 * mp.pi)) <= mp.mpf("6.01")

print("\nresidue check ok:", ok_a, "; printed bound fails at", fails, "of 4 x>=100 ; corrected identity ok:", ok_corr,
      "; 226.844 covers |tau|<=1e5 only, 6.01 survives:", ok_c)
if ok_a and fails > 0 and ok_corr:
    print("CONFIRMED: for chi=(./5), eta=exp(-t^2/2) the residue at s=0 is b+c_0+log x, so (9.1)-(9.2) fail for x>=100 by about log x, while the corrected identity holds.")
else:
    print("NOT CONFIRMED: the residue/end-to-end computation does not show the missing eta(0) log x term.")
