"""Table 3.1 of [H] (HH column) against Theorem 3.1.1, (3.2).

Claim: the HH column of Table 3.1 does not follow from Theorem 3.1.1 as printed. At
x = 10^27, |delta| <= 8 (so delta_0 = 2), five entries lie below (3.2) evaluated at an
admissible q >= q0 with exact phi(q), and the book's own worst-case form g_x(r) of (3.2)
(q/phi(q) replaced by digamma(r), r = q0) is 2.6-4.9% above all seven entries.

Book inputs:
- (3.2) and R_{x,t}, L_{x,t,q}: intromin.tex:84-111 (constants 0.27125, 0.41415, 0.5,
  2.5, 13/4, 7.82, 13.66, 37.55, 3.36; delta_0 = max(2, |delta|/4)).
- Table 3.1 entries and caption (q >= q0, |delta| <= 8, x = 10^27): intromin.tex:180-196.
- g_x(r) with digamma(r) = e^gamma loglog r + 2.50637/loglog r: optcoor.tex:236-246,
  conclusion.tex:598.

Confirms if (a) with exact phi, (3.2)/x exceeds the printed entry at some q >= q0 for
exactly the five rows q0 = 1.5e5, 5e5, 7.5e5, 1e6, 1e7 (at q = 150150, 510510, 750750,
1021020, 10210200), and (b) the digamma recipe exceeds all seven entries by 2.6-4.9%.

Run: python3 -I table_3_1.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as D, getcontext

getcontext().prec = 50
GAMMA = D("0.57721566490153286060651209008240243104215933593992")
EG = GAMMA.exp()
X13 = D(10) ** 9            # x^{1/3} for x = 10^27
XM16 = D(10) ** D("-4.5")   # x^{-1/6}


def ln(v):
    return D(v).ln()


def digamma(r):
    ll = ln(ln(D(r)))
    return EG * ll + D("2.50637") / ll


def R(t):
    return D("0.27125") * ln(1 + ln(4 * t) / (2 * ln(9 * X13 / (D("2.004") * t)))) + D("0.41415")


def bound32(q, qphi, d0=D(2)):
    """(3.2) divided by x; qphi = q/phi(q)."""
    q = D(q)
    t = d0 * q
    phi = q / qphi
    main = (R(t) * ln(t) + D("0.5")) / (d0 * phi).sqrt()
    sec = D("2.5") / t.sqrt()
    L = qphi * (D(13) / 4 * ln(t) + D("7.82")) + D("13.66") * ln(t) + D("37.55")
    return main + sec + 2 / t * L + D("3.36") * XM16


def qphi_exact(n):
    r = D(1)
    m, p = n, 2
    while p * p <= m:
        if m % p == 0:
            r *= D(p) / D(p - 1)
            while m % p == 0:
                m //= p
        p += 1
    if m > 1:
        r *= D(m) / D(m - 1)
    return r


Q0 = [100000, 150000, 250000, 500000, 750000, 1000000, 10000000]
BOOK = [D(s) for s in ("0.04661", "0.03883", "0.03098", "0.02297", "0.01934", "0.01756", "0.00690")]
# admissible worst-type q >= q0 (multiples of small primorials)
WORST = {150000: 150150, 500000: 510510, 750000: 750750, 1000000: 1021020, 10000000: 10210200}

print("x = 1e27, delta_0 = 2 (|delta| <= 8)")
print(f"{'q0':>9} {'printed':>8} | {'g_x(q0)':>8} {'excess%':>8} | {'q':>9} {'exact(3.2)':>10} {'excess%':>8}")
recipe_ok = True
fails = []
for q0, b in zip(Q0, BOOK):
    v = bound32(q0, digamma(q0))
    pr = float((v / b - 1) * 100)
    if not (2.5 <= pr <= 5.0):
        recipe_ok = False
    s = f"{q0:9d} {float(b):8.5f} | {float(v):8.5f} {pr:8.2f} |"
    if q0 in WORST:
        q = WORST[q0]
        assert q >= q0
        ve = bound32(q, qphi_exact(q))
        pe = float((ve / b - 1) * 100)
        if ve > b:
            fails.append(q0)
        s += f" {q:9d} {float(ve):10.6f} {pe:8.2f}"
    print(s)

print("rows where exact-phi (3.2) at an admissible q exceeds the printed entry:", fails)
print("digamma recipe 2.5-5% above every row:", recipe_ok)
if recipe_ok and fails == list(WORST):
    print("CONFIRMED: at x = 1e27, delta_0 = 2, Theorem 3.1.1 as printed exceeds five Table 3.1 "
          "HH entries at admissible q and its worst-case form g_x(q0) is 2.6-4.9% above all seven.")
else:
    print("NOT CONFIRMED: the HH column of Table 3.1 is consistent with Theorem 3.1.1 at the tested points.")
