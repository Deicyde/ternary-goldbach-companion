"""Check of [H, Proposition 7.1.5] (the E_2 form), via the derivation of (9.94).

Claim: the derivation of (9.94) splits int eta_+^2 log(xt) into a main term,
a cross term 2 int (eta_+ - eta_o) eta_o log(xt) and a square term, but adds the
Cauchy-Schwarz bound of the cross integral only once. With the factor 2 the same
argument gives only about 3.89e-6 log x + 1.26e-6, hence |E_2| <~ 3.94e-6 +
366.91/sqrt(x) at x = 1e12, not 2e-6 + 366.91/sqrt(x). The printed statement is
nevertheless true, because the true cross term is far smaller (Mellin-Parseval).

Book inputs:
  - intromaj.tex:146-162  h(t) = t^2 (2-t)^3 e^{t-1/2} on [0,2]; h_H = h *_M F_H,
    so M h_H(i tau) = M h(i tau) 1_{|tau|<H}; H = 200; eta_+ = h_H(t) t e^{-t^2/2},
    eta_o = h(t) t e^{-t^2/2}.
  - intromaj.tex:219-235  Prop 7.1.5: x >= 1e12, |E_1| <= 5.123e-15 + 366.91/sqrt x,
    |E_2| <= 2e-6 + 366.91/sqrt x.
  - expform.tex:2300-2304  the split, with the explicit factor 2 on the cross term.
  - expform.tex:2305-2311  main term 0.64020599736635 log x - 0.021094778698867.
  - expform.tex:2313-2318  cross integral <= (274.86/H^{7/2})(0.80013 log x + 0.214)
    <= 1.944e-6 log x + 5.2e-7 (no factor 2).
  - expform.tex:2322-2325  square term <= (274.86/H^{7/2})^2 log x + 27428/H^7.
  - expform.tex:2327-2331  (9.94): (0.640206 + O*(1.95e-6)) log x - 0.021095 + O*(5.3e-7).
  - normsapp.tex:290-293  |eta_+ - eta_o|_2 <= 274.856893/H^{7/2}.

Confirms if: (a) the printed 1.95e-6 matches one copy of the cross-term bound but
not two; (b) with the factor 2 the same bounds give a log x coefficient > 2e-6, so
the argument cannot give |E_2| <= 2e-6 + 366.91/sqrt x at any x >= 1e12; and
(c) a Mellin-Parseval computation of the true cross integrals puts
int eta_+^2 log(xt) inside the printed (9.94), so the statement holds.

Run: python3 -I proposition_7_1_5.py

Ported from a 2026-11-06 check script.
"""
import cmath
import math

H = 200.0
LX = math.log(1e12)

# ---------------- (a), (b): the book's own chain ----------------
n2 = 274.86 / H ** 3.5             # |eta_+ - eta_o|_2 bound, normsapp.tex:290
cross1 = n2 * 0.80013               # log x coefficient of one cross integral
cross0 = n2 * 0.214
sq1 = n2 ** 2
sq0 = 27428 / H ** 7
rnd1 = 0.640206 - 0.64020599736635  # rounding of the main-term coefficient
rnd0 = abs(-0.021094778698867 + 0.021095)
print("274.86/H^3.5 = %.6e; x0.80013 = %.6e (book 1.944e-6); x0.214 = %.6e (book 5.2e-7)"
      % (n2, cross1, cross0))
print("square term: %.4e log x + %.4e (book 5.903e-12, 2.143e-12)" % (sq1, sq0))
one1 = cross1 + sq1 + rnd1
two1 = 2 * cross1 + sq1 + rnd1
one0 = cross0 + sq0 + rnd0
two0 = 2 * cross0 + sq0 + rnd0
print("log x coefficient: one cross term %.6e, two cross terms %.6e (printed 1.95e-6)"
      % (one1, two1))
print("constant:          one cross term %.6e, two cross terms %.6e (printed 5.3e-7)"
      % (one0, two0))
E1c = 5.123e-15
e2_two = two1 + two0 / LX + E1c
e2_one = one1 + one0 / LX + E1c
e2_printed = 1.95e-6 + 5.3e-7 / LX + E1c
print("|E_2| - 366.91/sqrt x at x = 1e12: factor 2 -> %.6e, factor 1 -> %.6e, "
      "printed (9.94) -> %.6e (needed <= 2e-6)" % (e2_two, e2_one, e2_printed))
a_ok = one1 <= 1.95e-6 < two1
b_ok = two1 > 2e-6 and e2_printed <= 2e-6
print("note: even with one cross term the constant %.3e exceeds the printed 5.3e-7 "
      "(rounding of -0.021094778698867 omitted)" % one0)

# ---------------- (c): true cross term via Mellin-Parseval ----------------
# G(t) = h(t) t^3 e^{-t^2}, so (eta_+ - eta_o) eta_o = (h_H - h) G / t, and
#  X_A = int (eta_+-eta_o) eta_o dt       = -(1/pi) int_H^inf Re[Mh conj MG](i tau) dtau
#  X_B = int (eta_+-eta_o) eta_o log t dt = -(1/pi) int_H^inf Re[Mh conj MG'](i tau) dtau
E12 = math.exp(-0.5)
LOG2 = math.log(2.0)
NT = 70


def beta_term(p):
    # int_0^2 t^{p-1} (2-t)^3 dt
    return 6 * cmath.exp((p + 3) * LOG2) / (p * (p + 1) * (p + 2) * (p + 3))


def dlog_beta(p):
    return LOG2 - 1 / p - 1 / (p + 1) - 1 / (p + 2) - 1 / (p + 3)


ch = [1.0]
for n in range(1, NT):
    ch.append(ch[-1] / n)
cg = [1.0, 1.0]                     # e^{t - t^2} = sum cg_k t^k
for k in range(1, NT):
    cg.append((cg[k] - 2 * cg[k - 1]) / (k + 1))


def Mh(s):
    return E12 * sum(c * beta_term(s + n + 2) for n, c in enumerate(ch))


def MG(s):
    return E12 * sum(c * beta_term(s + k + 5) for k, c in enumerate(cg))


def MG_d(s):
    return E12 * sum(c * beta_term(s + k + 5) * dlog_beta(s + k + 5)
                     for k, c in enumerate(cg))


def gauss_legendre(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        p0, p1 = 1.0, x
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1)
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


GX, GW = gauss_legendre(30)


def integ(f, edges):
    s = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m, r = (lo + hi) / 2, (hi - lo) / 2
        s += r * sum(w * f(m + r * x) for x, w in zip(GX, GW))
    return s


def h(t):
    return t * t * (2 - t) ** 3 * math.exp(t - 0.5) if 0 <= t <= 2 else 0.0


# direct quadrature of the eta_o integrals (support [0,2])
fine = [2.0 * i / 200 for i in range(201)]
logedges = [0.0] + [2.0 * 2.0 ** -j for j in range(40, 0, -1)] + [1.25, 1.5, 1.75, 2.0]
A0 = integ(lambda t: (h(t) * t) ** 2 * math.exp(-t * t), fine)
B0 = integ(lambda t: (h(t) * t) ** 2 * math.exp(-t * t) * math.log(t) if t > 0 else 0.0, logedges)
L2log = math.sqrt(integ(lambda t: (h(t) * t) ** 2 * math.exp(-t * t) * math.log(t) ** 2
                        if t > 0 else 0.0, logedges))
print("direct: int eta_o^2 = %.14f (book 0.64020599736635), int eta_o^2 log t = %.14f "
      "(book -0.021094778698867)" % (A0, B0))
print("|eta_o|_2 = %.7f (book 0.80013), |eta_o log|_2 = %.7f (book 0.214)"
      % (math.sqrt(A0), L2log))
inputs_ok = math.sqrt(A0) <= 0.80013 and L2log <= 0.214

fA = lambda tau: (Mh(1j * tau) * MG(1j * tau).conjugate()).real
fB = lambda tau: (Mh(1j * tau) * MG_d(1j * tau).conjugate()).real
fN = lambda tau: abs(Mh(1j * tau)) ** 2
low_edges = [0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60, 80,
             100, 125, 150, 175, 200]


def tail(f):
    g = lambda u: f(H / u) * H / (u * u) if u > 0 else 0.0
    return integ(g, [0, 0.25, 0.5, 0.75, 1.0])


A_low, A_tail = integ(fA, low_edges), tail(fA)
B_low, B_tail = integ(fB, low_edges), tail(fB)
recA = (A_low + A_tail) / math.pi
recB = (B_low + B_tail) / math.pi
print("Parseval reconstruction: int eta_o^2 = %.14f, int eta_o^2 log t = %.14f"
      % (recA, recB))
valid = abs(recA - A0) < 1e-12 and abs(recB - B0) < 1e-12
XA = -A_tail / math.pi
XB = -B_tail / math.pi
Nh = tail(fN) / math.pi                      # int |h_H - h|^2 dt/t
SqA = (1.5) ** 1.5 * math.exp(-1.5) * Nh     # >= |eta_+ - eta_o|_2^2
SqB = 0.14882234545 * Nh                     # >= |int (eta_+-eta_o)^2 log t|
print("true cross integrals: X_A = %.4e, X_B = %.4e; int|h_H-h|^2 dt/t = %.4e"
      % (XA, XB, Nh))
print("Cauchy-Schwarz bound of one cross integral at x = 1e12: %.4e" % (cross1 * LX + cross0))
dA = 2 * abs(XA) + SqA
dB = 2 * abs(XB) + SqB
devA = max(abs(A0 - 0.640206 - dA), abs(A0 - 0.640206 + dA))
devB = max(abs(B0 + 0.021095 - dB), abs(B0 + 0.021095 + dB))
print("int eta_+^2 log(xt) - (0.640206 log x - 0.021095) = %.4e log x + %.4e at most "
      "(printed (9.94): 1.95e-6 log x + 5.3e-7)" % (devA, devB))
c_ok = valid and devA <= 1.95e-6 and devB <= 5.3e-7

print("(a) one copy only: %s; (b) factor 2 breaks 2e-6: %s; (c) (9.94) true: %s; "
      "book norms ok: %s" % (a_ok, b_ok, c_ok, inputs_ok))
if a_ok and b_ok and c_ok and inputs_ok:
    print("CONFIRMED: the derivation of (9.94) drops the factor 2 on the cross term; with it "
          "the argument gives %.3e log x + %.3e and only |E_2| <= %.3e + 366.91/sqrt(x) at "
          "x = 1e12, but the true cross term is %.1e, so (9.94) and Prop 7.1.5 hold."
          % (two1, two0, e2_two, XA))
else:
    print("NOT CONFIRMED: one-copy=%s, factor-2 breaks bound=%s, (9.94) true=%s, norms=%s."
          % (a_ok, b_ok, c_ok, inputs_ok))
