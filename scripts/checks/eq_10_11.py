"""Check of [H, Eq (10.11)] (eq:joko, error term of the triple product).

Claim: the bound (10.11) on |S_1 S_2 S_3 e(-N alpha) - (10.10)| does not
follow from (10.8): writing S_j = M_j + E_j (M_j the character-sum term of
(10.8), |E_j| <= eps_j), the cross terms eps_i eps_j |S_k| and eps_1 eps_2 eps_3
are dropped.  The printed inequality fails for admissible weights; the
correct bound is (10.11) + sum_{i<j} eps_i eps_j |S_k| + eps_1 eps_2 eps_3.

Book inputs:
  - intmajarc.tex:3-9     S_eta(alpha,x) = sum Lambda(n) e(alpha n) eta(n/x),
                          eta: R -> C of fast decay.
  - intmajarc.tex:197-206 (10.8) S_eta = (1/phi(q)) sum_chi chi(a) tau(chibar)
                          S_{eta,chi*}(delta/x,x) + O*(2 sum_{p|q} log p
                          sum_{k>=1} eta(p^k/x)), and (10.9).
  - intmajarc.tex:225-237 (10.10) and (10.11).
  alpha = a/q + delta/x.

Example: q = 2, a = 1, delta = 0, x = 10, N = 101, eta_1 = eta_2 = eta_3 = eta,
a C^infinity nonnegative compactly supported sum of bumps with eta(0.2) = 1,
eta(0.3) = log 2/log 3, eta(m/10) = 0 for every other integer m >= 1.
The Gauss sums, (10.8) main term, (10.10) and (10.11) are computed literally.
Confirms if (10.8) holds, |LHS| > (10.11), and the corrected bound holds.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_10_11.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 40


def Lam(n):
    for p in range(2, n + 1):
        if n % p == 0:
            m = n
            while m % p == 0:
                m //= p
            return mp.log(p) if m == 1 else mp.mpf(0)
    return mp.mpf(0)


def bump(u):
    return mp.exp(1 - 1 / (1 - u * u)) if abs(u) < 1 else mp.mpf(0)


W = mp.mpf("0.04")
centres = [(mp.mpf("0.2"), mp.mpf(1)), (mp.mpf("0.3"), mp.log(2) / mp.log(3))]
eta = lambda t: sum(c * bump((t - t0) / W) for t0, c in centres)

q, a, delta, x, N = 2, 1, 0, 10, 101
alpha = mp.mpf(a) / q + mp.mpf(delta) / x
e = lambda y: mp.expjpi(2 * y)
NMAX = 40  # eta(n/x) = 0 for n > 3.2

# characters mod 2: only chi_0 (chi_0(1)=1), induced by the trivial character mod 1
chars = [({1: 1}, lambda n: 1)]  # (values on units mod q, primitive character)
phi = 1


def S(beta, chistar):
    return sum(Lam(n) * chistar(n) * e(beta * n) * eta(mp.mpf(n) / x) for n in range(1, NMAX))


S_eta = S(alpha, lambda n: 1)
terms = []
for vals, chistar in chars:
    tau = sum(mp.conj(vals[b]) * e(mp.mpf(b) / q) for b in vals)  # tau(chibar)
    terms.append((vals[a % q] * tau, S(mp.mpf(delta) / x, chistar)))
M = sum(c * s for c, s in terms) / phi
eps = 2 * sum(mp.log(p) * sum(eta(mp.mpf(p) ** k / x) for k in range(1, 30)) for p in (2,))
print("S_eta(alpha,x)   =", mp.nstr(S_eta, 15))
print("(10.8) main term =", mp.nstr(M, 15), " (-2 log 2 =", mp.nstr(-2 * mp.log(2), 15), ")")
print("eps (10.8)       =", mp.nstr(eps, 15))
ok108 = abs(S_eta - M) <= eps + mp.mpf(10) ** -30

# (10.10) as the literal triple character sum (eta_1 = eta_2 = eta_3)
T = mp.mpf(0)
for c1, s1 in terms:
    for c2, s2 in terms:
        for c3, s3 in terms:
            T += c1 * c2 * c3 * s1 * s2 * s3
T = T / phi ** 3 * e(-mp.mpf(N) * a / q) * e(-mp.mpf(delta) * N / x)
LHS = abs(S_eta ** 3 * e(-N * alpha) - T)
B1011 = 3 * abs(S_eta) ** 2 * eps
Bcorr = B1011 + 3 * eps ** 2 * abs(S_eta) + eps ** 3
print("|S^3 e(-N alpha) - (10.10)| =", mp.nstr(LHS, 15), " (8 (log 2)^3 =", mp.nstr(8 * mp.log(2) ** 3, 15), ")")
print("(10.11)                     =", mp.nstr(B1011, 5))
print("corrected bound             =", mp.nstr(Bcorr, 15))

if ok108 and LHS > B1011 + mp.mpf("1e-10") and LHS <= Bcorr + mp.mpf(10) ** -25:
    print("CONFIRMED: for q=2, alpha=1/2, x=10 and an admissible smooth eta >= 0 satisfying (10.8), |S^3 e(-N alpha) - (10.10)| = %s while (10.11) = %s, so (10.11) drops the cross terms; the corrected bound %s holds." % (mp.nstr(LHS, 8), mp.nstr(B1011, 3), mp.nstr(Bcorr, 8)))
else:
    print("NOT CONFIRMED: the example does not violate (10.11) or does not satisfy (10.8).")
