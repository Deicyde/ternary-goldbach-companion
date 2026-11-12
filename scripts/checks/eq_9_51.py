"""Check of [H, (9.51)] (proof of Lemma 9.3.1).

Claim: (9.51) is false as printed for every T0 >= 50 and every q.  Its left
side contains (1/(4T)) * T e^{-cT} = (1/4) e^{-cT}, a constant times e^{-cT},
but the right side comes from (9.50) with the term c1/t, c1 = pi/2, i.e. it
treats that piece as (pi/2)/T * e^{-cT}/(2 pi).  With the constant c1 the
method gives a = (log T0/c + 1/c + pi/2)/(log T0/c - 1/(c^2 T0)) = 1.3634 at
T0 = 50 instead of a <= 1.299.

Book inputs (expform.tex):
  - l.1099-1103 (9.49): weight (1/2pi) log(qT/2pi) + 1/(4T).
  - l.1106-1116 (9.50) and its a = (log y/c + 1/c + c1/y)/(log y/c - 1/(c^2 y)).
  - l.1117 "c = 0.1598, c1 = pi/2, y = T0 >= 50".
  - l.1119-1126 (9.51): LHS int_{T0}^oo ((1/2pi)log(qT/2pi) + 1/(4T)) T e^{-cT} dT
    <= (1/2pi)(log(q/2pi)(T0/c + 1/c^2) + (T0/c + a/c^2) log T0) e^{-cT0}.
  - l.1128-1129: a = (log T0/0.1598 + 1/0.1598 + (pi/2)/T0)/(...) <= 1.299.

Method: the LHS is evaluated twice, by a closed form with E_1 (continued
fraction) and by composite Gauss-Legendre quadrature of the printed
integrand, for several q and T0; the q-dependent parts of both sides are
identical, so the comparison is also made in the normalized form
J + pi/(2c) <= (T0/c + a/c^2) log T0, J = e^{cT0} int T log T e^{-cT}.

Confirms if: LHS > RHS of (9.51) with the book's a (and with a = 1.299 at
T0 = 50) at every tested (q, T0), T0 in [50, 10^4], the two LHS evaluations
agree, and the RHS with the constant-c1 value of a is >= LHS.

Run: python3 -I eq_9_51.py

Ported from a 2026-11-06 check script.
"""
import math

PI = math.pi
c = 0.1598


def eE1(z):
    """e^z E_1(z), z > 1, continued fraction (modified Lentz)."""
    tiny = 1e-300
    b = z + 1.0
    C = 1.0 / tiny
    D = 1.0 / b
    h = D
    for i in range(1, 100000):
        an = -float(i * i)
        b += 2.0
        D = an * D + b
        D = tiny if D == 0 else D
        C = b + an / C
        C = tiny if C == 0 else C
        D = 1.0 / D
        de = C * D
        h *= de
        if abs(de - 1.0) < 1e-16:
            break
    return h


def legendre(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(PI * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return list(zip(xs, ws))


GL = legendre(20)


def a_book(T0):
    L = math.log(T0)
    return (L / c + 1 / c + (PI / 2) / T0) / (L / c - 1 / (c * c * T0))


def a_const(T0):
    L = math.log(T0)
    return (L / c + 1 / c + PI / 2) / (L / c - 1 / (c * c * T0))


def lhs_closed(T0, q):
    """Printed LHS of (9.51), times e^{cT0}."""
    IT = T0 / c + 1 / c ** 2
    J = (T0 / c + 1 / c ** 2) * math.log(T0) + 1 / c ** 2 + eE1(c * T0) / c ** 2
    return (math.log(q / (2 * PI)) * IT + J) / (2 * PI) + 1 / (4 * c)


def lhs_quad(T0, q):
    """Printed integrand integrated numerically (substitution T = T0 + u), times e^{cT0}."""
    f = lambda u: (math.log(q * (T0 + u) / (2 * PI)) / (2 * PI) + 1 / (4 * (T0 + u))) * (T0 + u) * math.exp(-c * u)
    s, h = 0.0, 1.0
    for j in range(600):
        m = (j + 0.5) * h
        s += sum(w * f(m + 0.5 * h * x) for x, w in GL) * 0.5 * h
    return s


def rhs(T0, q, a):
    """RHS of (9.51), times e^{cT0}."""
    return (math.log(q / (2 * PI)) * (T0 / c + 1 / c ** 2) + (T0 / c + a / c ** 2) * math.log(T0)) / (2 * PI)


print("a_book(50) = %.6f (book: <= 1.299); a_const(50) = %.6f" % (a_book(50), a_const(50)))
print("pi/(2c) = %.6f" % (PI / (2 * c)))
print()
print("%8s %8s %14s %14s %14s %10s %14s" % ("q", "T0", "LHS(closed)", "LHS(quad)", "RHS(a_book)", "LHS/RHS", "RHS(a_const)"))
all_fail = True
agree = True
const_ok = True
for q in [1, 3, 1000, 10 ** 6]:
    for T0 in [50, 60, 83, 100, 200, 1000, 10000]:
        L1 = lhs_closed(T0, q)
        L2 = lhs_quad(T0, q) if T0 <= 1000 else L1
        R = rhs(T0, q, a_book(T0))
        Rc = rhs(T0, q, a_const(T0))
        print("%8d %8d %14.6f %14.6f %14.6f %10.6f %14.6f" % (q, T0, L1, L2, R, L1 / R, Rc))
        all_fail &= L1 > R
        agree &= abs(L1 - L2) < 1e-9 * abs(L1)
        const_ok &= Rc >= L1

# with a = 1.299 (the printed bound on a) at T0 = 50
L50, R50 = lhs_closed(50, 1), rhs(50, 1, 1.299)
print()
print("q=1, T0=50: LHS*e^{cT0} = %.6f, RHS with a=1.299: %.6f, ratio %.6f" % (L50, R50, L50 / R50))
# normalized gap 2pi e^{cT0}(LHS - RHS) is q-independent
for T0 in [50, 100, 1000]:
    g = 2 * PI * (lhs_closed(T0, 1) - rhs(T0, 1, a_book(T0)))
    print("normalized gap at T0=%d: %.5f (J+pi/(2c) - (T0/c+a/c^2)log T0)" % (T0, g))
# scan of the normalized gap on [50, 1e4]
mn = min(2 * PI * (lhs_closed(T, 1) - rhs(T, 1, a_book(T))) for T in [50 * 1.01 ** k for k in range(540)])
print("min normalized gap on T0 in [50, 1.07e4] (540-point geometric grid): %.5f" % mn)

ok = all_fail and agree and const_ok and L50 > R50 and mn > 0
if ok:
    print("CONFIRMED: the printed (9.51) fails at every tested q and T0 >= 50 (LHS/RHS = %.5f at q=1, T0=50; the normalized gap is >= %.3f), because the 1/(4T) weight times T is the constant 1/4, and with that constant a = %.4f at T0=50 restores the inequality." % (lhs_closed(50, 1) / rhs(50, 1, a_book(50)), mn, a_const(50)))
else:
    print("NOT CONFIRMED: the printed (9.51) holds at some tested point, or the two LHS evaluations disagree.")
