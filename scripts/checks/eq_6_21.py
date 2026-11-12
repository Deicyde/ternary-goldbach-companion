"""Eq (6.21) of [H] (arXiv:1501.05438v2): (5.54) used without its hypothesis Q >= 3.5W.

Claim: (5.54) holds only under Prop. 5.2.4's Q >= 3.5W; (6.21) needs it for all W <= x/U, i.e. Q >= 3.5x/U, which Ch. 6 never checks; section 6.3.2 sets Q = x/U, so it fails for W > x/(3.5U); harmless in section 6.3.1.

Book inputs:
  - Prop. 5.2.4: "Let Q >= 3.5W" (typeII.tex l. 1193-1196); (5.51): "If q < W/2 and Q >= 3.5W"
    (l. 1152-1153); its proof follows Lemma 5.2.2, which uses 1/Q <= 1/(3.5W) and needs
    3 sigma/(1 - sigma/3.5) < 1, sigma = 1/(2 e^0.50136) (l. 1057-1069); (5.54) is (5.51) with
    A_0 = U', A_1 = x/W (l. 1255-1262).
  - (6.21): 'We use (garn1a)' = (5.54) for W in [W_0, x/U] (minarctotals.tex l. 598-614).
  - Ch. 6 assumes only Q >= max(16, 2 sqrt x) and Q >= max(2U, x/U) (minarctotals.tex l. 16-17).
  - first choice (6.49): Q = (3/4) x^(2/3), U = x^(2/3)/(9 sqrt(q delta_0)) (l. 1286-1298);
    second choice (6.65): U = 500 sqrt6 x^(1/3), Q = x/U (l. 1825-1826); case (a) with theta = 4
    applies (6.38) (hence Eq (6.21)) for y < q <= x/8U (l. 1976-1981).

Computed: the chain coefficient 3 sigma/(1 - sigma W/Q) at W/Q = 1/3.5 and W/Q = 1, the
smallest Q/W the step allows, and Q/(3.5 x/U) for both parameter choices at x0 = 2.16e20.

Confirms: the chain fails at W = Q, the second choice has Q < 3.5W on (x/3.5U, x/U] inside
the integration range, and the first choice satisfies Q >= 3.5x/U.

Run: python3 -I eq_6_21.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as D, getcontext
getcontext().prec = 50

def sigma_chain():
    """Lemma 5.2.2 proof (typeII.tex l. 1057-1069): weight bound needs 3 sigma/(1 - sigma W/Q) < 1."""
    s = 1 / (2 * D("0.50136").exp())
    c35 = 3 * s / (1 - s / D("3.5"))
    c1 = 3 * s / (1 - s)
    need = s / (1 - 3 * s)
    print(f"sigma = {float(s):.7f}; chain coefficient 3s/(1 - s W/Q): W/Q = 1/3.5 -> {float(c35):.6f}, "
          f"W/Q = 1 -> {float(c1):.6f}; the step needs Q/W >= s/(1-3s) = {float(need):.5f}")
    return c35 < 1, c1 > 1


def params_report():
    x = D("2.16e20")
    x13 = x ** (D(1) / 3)
    # first choice (6.49): Q = (3/4) x^{2/3}, U = x^{2/3}/(9 sqrt(q delta_0)), q delta_0 <= 2y = x^{1/3}/3
    r1 = D("0.75") * D(3).sqrt() / D("31.5") * x ** (D(1) / 6)
    print(f"first choice (6.49) at x0: Q/(3.5 x/U) >= 0.75 sqrt3/31.5 x^(1/6) = {float(r1):.3f}")
    # second choice (6.65): U = 500 sqrt6 x^{1/3}, Q = x/U; theta = 4, case (a) y < q <= x/8U, W in [8q, x/U]
    U = 500 * D(6).sqrt() * x13
    Q = x / U
    y = x13 / 6
    print(f"second choice (6.65) at x0: U = {float(U):.5g}, Q = x/U = {float(Q):.5g}, Q/(3.5 x/U) = {float(Q/(D('3.5')*x/U)):.4f}")
    print(f"   Q >= 3.5W fails for W in (x/3.5U, x/U] = ({float(x/(D('3.5')*U)):.5g}, {float(x/U):.5g}];"
          f" case (a) q in ({float(y):.4g}, {float(x/(8*U)):.5g}], W_0 = 8q;"
          f" for q > x/28U = {float(x/(28*U)):.4g} all of [W_0, x/U] violates it")
    return r1 >= 100, Q < D("3.5") * (x / U), D(8) * y < x / U

ok35, fail1 = sigma_chain()
r1ok, viol, nonempty = params_report()
if ok35 and fail1 and viol and nonempty and r1ok:
    print("CONFIRMED: Eq (6.21) applies (5.54) up to W = x/U, but with Q = x/U ((6.65)) Q >= 3.5W fails on "
          "(x/3.5U, x/U], where Lemma 5.2.2's chain breaks (3 sigma/(1 - sigma) = 1.303 > 1 at W = Q); "
          "the first choice satisfies Q >= 3.5x/U (ratio >= 101).")
else:
    print("NOT CONFIRMED: the hypothesis Q >= 3.5W is not violated, or its violation does not break the step.")
