# Lemma 4.2.4 (eq:prok): (UV+(19/18)Q0) <= x/5.6 gives 2/9+3/2+log(D'+19/18 q) <= log x
# iff e^{2/9+3/2} <= 5.6. Check also that "<= x" is not what feeds the 9/8 (2c2)^{3/2} sqrt x log x term.
import math, sys
c = math.exp(2/9 + 3/2)
print("e^(2/9+3/2) =", c, "<= 5.6:", c <= 5.6)
# constant check: (10/3)(3/4 + 9/8) = 25/4
k = (10/3)*(3/4 + 9/8)
print("(10/3)(3/4+9/8) =", k)
# 3/2 D'q log D' + 9/8 q^2(...) expansion check vs direct integral at sample points
def lhs(D, q):
    F = lambda t: t*t/2*math.log(t/math.sqrt(math.e))
    return F(D + 1.5*q) - F(q)
def rhs(D, q):
    return 0.5*D*D*math.log(D/math.sqrt(math.e)) + 1.5*D*q*math.log(D) + 9/8*q*q*(2/9 + 1.5 + math.log(D + 19/18*q))
ok = True
for D, q in [(1e6, 1e3), (1e8, 1e4), (5e3, 1e4), (1e4, 2e4)]:
    print(D, q, lhs(D, q) <= rhs(D, q), lhs(D, q), rhs(D, q))
    ok &= lhs(D, q) <= rhs(D, q)
sys.exit(0 if (c <= 5.6 and abs(k - 6.25) < 1e-12 and ok) else 1)
