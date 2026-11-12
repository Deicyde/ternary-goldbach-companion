"""Eq 4.11 (Lemma 4.2.1, case (a)): the last step x/Q -> x/Q0 needs floor(x/|delta q|) >= Q0.

Claim: with Q = floor(x/|delta q|), the proof's chain (4.16)[M = Q/2] + (4.19) carries x/Q, and
for non-integer Q0 (allowed by the lemma) Q < Q0 can happen and the chain then exceeds (4.11);
the closing sentence's bound log+ D/((Q+1)/2) <= log+ 2D/(x/|delta|q + 1) runs the wrong way,
while the log+ 2D/(x/|delta|q) printed in (4.11) is valid; the bound (4.11) survives via
2x/(Q+1) <= 2x/Q0 and q' >= (eps/(1+eps)) x/|delta q|.

Book inputs (typeI.tex): hypotheses and c1 = 1 + |eta'|_1/(2x/D), c2, varpi_eps, (4.11)
(lines 602-649); Q = floor(x/|delta q|) (656); (4.16) final form (5c0c2/6pi^2)M + (35c0c2/6pi^2)q
(781-796); (4.19) (863-869); (4.20) (873-880); closing sentence (898-899). c0 = 31.521 and
|eta'|_1 = 8 log 2 (eta_2, as in Ch. 6).

Confirms if: at admissible points with non-integer Q0 and Q < Q0 the printed chain exceeds (4.11),
the repaired chain does not, an integer-Q0 control does not fail, and the closing log+ bound is
reversed while the printed log+ in (4.11) dominates.

Run: python3 -I eq_4_11.py

Ported from a 2026-11-06 check script.
"""
from decimal import Decimal as Dm, getcontext

getcontext().prec = 60


def machin_pi():
    def atan_inv(n):
        x = Dm(1) / n
        x2, s, t, k = x * x, x, x, 1
        while True:
            t = -t * x2
            k += 2
            if abs(t / k) < Dm(10) ** -65:
                return s
            s += t / k
    return 16 * atan_inv(5) - 4 * atan_inv(239)


PI = machin_pi()


def logp(v):
    v = Dm(v)
    return max(v.ln(), Dm(0)) if v > 0 else Dm(0)


def floor(v):
    return Dm(int(Dm(v).to_integral_value(rounding="ROUND_FLOOR")))


def run(label, c0, eta1, q, Q0, x, D, x_over_delta, eps):
    c0, q, Q0, x, D, eps = map(Dm, (c0, q, Q0, x, D, eps))
    xd = Dm(x_over_delta)
    delta = x / xd
    y = xd / q                     # x/(|delta| q)
    Q = floor(y)
    c1 = 1 + eta1 / (2 * x / D)
    c2 = (3 * PI / (5 * c0.sqrt())) * (1 + (Dm(13) / 3).sqrt())
    varpi = (3 + 2 * eps).sqrt() + ((1 + (Dm(13) / 3).sqrt()) / 4 - 1) / (2 * (1 + eps))
    A = 2 * (c0 * c1).sqrt() / PI
    hyp = (delta / x <= 1 / (q * Q0) and q <= Q0 and Q0 >= 16 and 1 <= D <= x
           and delta >= 1 / (2 * c2) and 0 < eps <= 1 and D > (Q + 1) / 2)
    jenuf = 5 * c0 * c2 / (6 * PI**2) * (Q / 2) + 35 * c0 * c2 / (6 * PI**2) * q
    L = logp(D / ((Q + 1) / 2))
    sauna = A * (D + ((1 + eps) * (3 + 2 * eps).sqrt() - Dm(1) / 2) * (Q + 1)
                 + ((1 + eps) * Q + 1) / 2 * L) + 3 * c1 * (2 + (1 + eps) / eps * L) * x / Q
    chain = jenuf + sauna
    kull = (A * (D + (1 + eps) * (Q + 1) * (varpi + L / 2))
            + 3 * c1 * (2 + (1 + eps) / eps * L) * x / Q + 35 * c0 * c2 / (6 * PI**2) * q)
    L2 = logp(2 * D / y)
    kall = (A * (D + (1 + eps) * min(floor(y) + 1, 2 * D) * (varpi + L2 / 2))
            + 3 * c1 * (2 + (1 + eps) / eps * L2) * x / Q0 + 35 * c0 * c2 / (6 * PI**2) * q)
    sauna_rep = (A * (D + ((1 + eps) * (3 + 2 * eps).sqrt() - Dm(1) / 2) * (Q + 1)
                      + ((1 + eps) * Q + 1) / 2 * L)
                 + 3 * c1 * (2 * x / (Q + 1) + (1 + eps) / eps * L * x / y))
    chain_rep = jenuf + sauna_rep
    Lw = logp(2 * D / (y + 1))
    print(f"{label}\n  hypotheses hold: {hyp}; |delta|={delta:.6f}, Q={Q}, Q0={Q0}, c1={c1:.8f}")
    print(f"  chain (4.16)+(4.19) = {chain:.4f}; (4.20) = {kull:.4f}; (4.11) = {kall:.4f}; "
          f"chain-(4.11) = {chain-kall:.4f}; repaired chain = {chain_rep:.4f}")
    print(f"  log+(D/((Q+1)/2)) = {L:.6f}; closing-sentence bound log+(2D/(x/|dq|+1)) = {Lw:.6f}; "
          f"printed log+(2D/(x/|dq|)) = {L2:.6f}")
    return dict(hyp=hyp, Q=Q, Q0=Q0, chain=chain, kall=kall, rep=chain_rep, L=L, Lw=Lw, L2=L2)


c0 = "31.521"
eta1 = 8 * Dm(2).ln()
fail_cases = [
    run("Ex1: q=1, Q0=16.5, x=D=1000, x/|delta|=16.6, eps=0.1", c0, eta1, 1, "16.5", 1000, 1000, "16.6", "0.1"),
    run("Ex1b: same, eps=1", c0, eta1, 1, "16.5", 1000, 1000, "16.6", "1"),
    run("Ex2: q=3, Q0=100.9, x/|delta q|=100.95, x=1e6, D=1e5, eps=0.5", c0, eta1, 3, "100.9", 10**6, 10**5,
        Dm("100.95") * 3, "0.5"),
]
ex3 = run("Ex3: q=1, Q0=16.01, x/|delta|=16.99, x=D=1000, eps=1", c0, eta1, 1, "16.01", 1000, 1000, "16.99", "1")
ctrl = run("Control: integer Q0=16, x/|delta|=16.6, x=D=1000, eps=0.1", c0, eta1, 1, "16", 1000, 1000, "16.6", "0.1")

ok = all(r["hyp"] and r["Q"] < r["Q0"] and r["chain"] > r["kall"] and r["rep"] <= r["kall"] for r in fail_cases)
ok = ok and ex3["hyp"] and ex3["rep"] <= ex3["kall"]
ok = ok and ctrl["hyp"] and ctrl["chain"] <= ctrl["kall"]
logs = all(r["Lw"] < r["L"] <= r["L2"] for r in fail_cases + [ex3])
print("chain > (4.11) at non-integer Q0, repair holds, integer control holds:", ok)
print("closing log+ bound reversed, printed log+ in (4.11) valid:", logs)
if ok and logs:
    print("CONFIRMED: for non-integer Q0 with floor(x/|delta q|) < Q0 the printed chain exceeds (4.11) and the closing log+ bound is reversed, while the repaired chain stays below (4.11).")
else:
    print("NOT CONFIRMED: the printed chain did not exceed (4.11), or the repair or log+ comparison failed.")
