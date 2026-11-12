"""Check of [H, (A.15)] (the constant C_4).

Claim: the integral of |h''''(x)| x^3 over (0,2) is 1035.5366451..., not the
printed 1152.69754862..., so C_4 = 1896.0209466..., not 2013.18185012...; the
printed value is an overestimate (harmless for upper bounds). The display
before (A.15) also prints the third interval as [alpha_{4,1}, 2^-] instead of
[alpha_{4,2}, 2^-].

Book inputs (normsapp.tex):
  - l.8-10   h(t) = t^2 (2-t)^3 e^{t-1/2} on [0,2], 0 elsewhere.
  - l.82-87  C_k = lim int_t^oo |h^(k)(x)| x^{k-1} dx.
  - l.126-128 H_{k+1} = H_k + H_k', h^(k) = H_k e^{x-1/2}.
  - l.140-213 roots alpha_{k,j}, printed C_2 = 10.79195821037, C_3 =
             75.1295251672, the closed-form line (K at alpha_{4,j} and
             -lim h'''(t) t^3), the value 1152.69754862 (l.201), the delta
             term 24 e^{3/2} 2^3 and C_4 = 2013.18185012 (l.211).

Method: exact polynomial arithmetic for H_k, roots by mpmath findroot, the
book's own closed form, and an independent Gauss-Legendre quadrature of
|H_4(x)| x^3 e^{x-1/2} split at the roots. C_2, C_3 and the roots are
recomputed as a control.

Confirms if: C_2, C_3 and the roots match the book, the closed form and the
quadrature agree on a value of the (0,2) integral that differs from 1152.6975
by more than 1, and C_4 computed from it is below the printed 2013.18185012.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_a_15.py

Ported from a 2026-11-06 check script.
"""
from mpmath import mp, mpf, exp, findroot, quad, polyval

mp.dps = 40

# polynomial coefficients, lowest degree first
def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]

def pder(a):
    return [i * a[i] for i in range(1, len(a))]

def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r

H = [pmul([0, 0, 1], [8, -12, 6, -1])]  # x^2 (2-x)^3
for k in range(4):
    H.append(padd(H[-1], pder(H[-1])))
print("H_4 coefficients (x^0..x^5):", H[4])

def ev(p, x):
    return polyval(list(reversed(p)), x)

def hk(k, x):
    return ev(H[k], x) * exp(x - mpf(1) / 2)

def roots(k, guesses):
    return [findroot(lambda x: ev(H[k], x), g) for g in guesses]

a2 = roots(2, [0.49, 1.49])
a3 = roots(3, [1.04, 1.81])
a4 = roots(4, [0.46, 1.55])
print("alpha_2:", [mp.nstr(r, 15) for r in a2], "book 0.48756597185712, 1.48777169309489")
print("alpha_3:", [mp.nstr(r, 15) for r in a3], "book 1.04294565694978, 1.80999654602916")
print("alpha_4:", [mp.nstr(r, 15) for r in a4], "book 0.45839599852663, 1.54626346975533")

C2 = 2 * sum((-1) ** (j + 1) * (hk(1, a) * a - hk(0, a)) for j, a in [(1, a2[0]), (2, a2[1])])
C3 = 2 * sum((-1) ** j * (hk(2, a) * a**2 - 2 * hk(1, a) * a + 2 * hk(0, a)) for j, a in [(1, a3[0]), (2, a3[1])])
print("C_2 =", mp.nstr(C2, 15), " book 10.79195821037")
print("C_3 =", mp.nstr(C3, 15), " book 75.1295251672")

def K(x):
    return hk(3, x) * x**3 - 3 * hk(2, x) * x**2 + 6 * hk(1, x) * x - 6 * hk(0, x)

h3_at_2 = hk(3, mpf(2))
print("lim h'''(t), t->2-: ", mp.nstr(h3_at_2, 15), " book -24 e^{3/2} =", mp.nstr(-24 * exp(mpf(3) / 2), 15))
closed = 2 * sum((-1) ** j * K(a) for j, a in [(1, a4[0]), (2, a4[1])]) - h3_at_2 * 8
print("K(alpha_41), K(alpha_42) =", mp.nstr(K(a4[0]), 12), mp.nstr(K(a4[1]), 12))
print("book's closed form for int_0^2 |h''''| x^3 :", mp.nstr(closed, 15))

f = lambda x: abs(hk(4, x)) * x**3
q = quad(f, [0, a4[0], a4[1], 2])
print("direct quadrature (split at roots)        :", mp.nstr(q, 15))
literal = (-quad(lambda x: hk(4, x) * x**3, [0, a4[0]]) + quad(lambda x: hk(4, x) * x**3, [a4[0], a4[1]])
           - quad(lambda x: hk(4, x) * x**3, [a4[0], 2]))
print("display read literally with [alpha_41, 2^-] :", mp.nstr(literal, 12))

delta = 24 * exp(mpf(3) / 2) * 8
C4 = q + delta
book_int, book_C4 = mpf("1152.69754862"), mpf("2013.18185012")
print("delta term 192 e^{3/2} =", mp.nstr(delta, 15), "; book C_4 - book integral =", mp.nstr(book_C4 - book_int, 12))
print("C_4 =", mp.nstr(C4, 15), " book 2013.18185012; book - true =", mp.nstr(book_C4 - C4, 12))

ok_ctrl = (abs(C2 - mpf("10.79195821037")) < 1e-10 and abs(C3 - mpf("75.1295251672")) < 1e-9
           and abs(a4[0] - mpf("0.45839599852663")) < 1e-13 and abs(a4[1] - mpf("1.54626346975533")) < 1e-13)
ok = ok_ctrl and abs(closed - q) < 1e-20 and abs(q - book_int) > 1 and C4 < book_C4
if ok:
    print("CONFIRMED: the (0,2) integral is %s (book's own closed form and quadrature agree), not 1152.69754862, so C_4 = %s < printed 2013.18185012."
          % (mp.nstr(q, 11), mp.nstr(C4, 11)))
else:
    print("NOT CONFIRMED: the recomputed integral or controls do not support the claim.")
