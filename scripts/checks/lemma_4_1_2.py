"""Lemma 4.1.2 ([H], arXiv:1501.05438v2): the first display of the proof.

Claim: the proof's first display sums the integer-distance terms min(A, C/sin^2(pi r/q)) up
to r = q/2, but only r <= (q-1)/2 occur.  For even q this adds the term r = q/2, and the next
bound C*N(q), N(q) = csc^2(pi/2q) + csc^2(pi/q) + (q/pi)(cot(pi/q) + cot(3pi/2q)), is false
for the printed display at q = 2, 4, 6 (where the display even exceeds 20Cq^2/(3pi^2)); for
every even q the cited midpoint-convexity step gives N(q) + (q/pi) tan(pi/2q) > 20q^2/(3pi^2).
With upper limit (q-1)/2 the chain display <= C N(q) <= (20/3pi^2) C q^2 holds.

Book inputs (book/src/typeI.tex):
  - statement (4.4), lines 188-199: sum over y1 < n <= y2, q not dividing n, of
    min(A, C/|sin(pi alpha n)|^2) <= min((20/3pi^2) C q^2, 2A + (4q/pi) sqrt(AC));
  - first display of the proof, lines 208-213 (both sums to r = q/2);
  - the bound C N(q) for q >= 2, lines 216-220, and N(q) <= (20/3pi^2) q^2, lines 236-241.

Take A >= C/sin^2(pi/2q), so every min is its C-term (C = 1).  Confirmed if: the printed
display exceeds N(q) exactly for even q in {2, 4, 6} among 2 <= q <= 2000 and exceeds
20q^2/(3pi^2) at q = 2, 4, 6; N(q) + (q/pi)tan(pi/2q) > 20q^2/(3pi^2) for all even q <= 2000;
and with limit (q-1)/2 the display is <= N(q) <= 20q^2/(3pi^2) for all 2 <= q <= 2000.  A brute
evaluation of the lemma's left side (alpha = a/q + 1/(qQ), y2 = Q/2, y2 - y1 = q) checks that
the lemma itself holds for q <= 60.

Run: python3 -I lemma_4_1_2.py
Ported from a 2026-11-06 check script.
"""
import math

PI = math.pi


def csc2(t):
    return 1.0 / math.sin(t) ** 2


def N(q):
    return (csc2(PI / (2 * q)) + csc2(PI / q)
            + (q / PI) * (1 / math.tan(PI / q) + 1 / math.tan(3 * PI / (2 * q))))


def display(q, int_upper):
    half = sum(csc2(PI * (r - 0.5) / q) for r in range(1, q // 2 + 1))
    integ = sum(csc2(PI * r / q) for r in range(1, int_upper + 1))
    return half + integ


def main():
    bound = lambda q: 20 * q * q / (3 * PI * PI)
    fails = [q for q in range(2, 2001, 2) if display(q, q // 2) > N(q) * (1 + 1e-12)]
    for q in (2, 4, 6):
        print(f"q={q}: printed display/C = {display(q, q // 2):.6f}, N(q) = {N(q):.6f}, "
              f"20q^2/(3pi^2) = {bound(q):.6f}, corrected display/C = {display(q, (q - 1) // 2):.6f}")
    print(f"even q <= 2000 with printed display > N(q): {fails}")
    above = all(display(q, q // 2) > bound(q) for q in (2, 4, 6))
    mid = [q for q in range(2, 2001, 2) if N(q) + (q / PI) * math.tan(PI / (2 * q)) <= bound(q)]
    print(f"even q <= 2000 with N(q) + (q/pi)tan(pi/2q) <= 20q^2/(3pi^2): {len(mid)}")
    print(f"slack 20q^2/(3pi^2) - N(q): q=2 {bound(2) - N(2):.4f}, q=10 {bound(10) - N(10):.4f}, "
          f"q=2000 {bound(2000) - N(2000):.4f}")
    corr_bad = [q for q in range(2, 2001)
                if not (display(q, (q - 1) // 2) <= N(q) * (1 + 1e-12) <= bound(q) * (1 + 1e-12))]
    print(f"2 <= q <= 2000 where corrected display <= N(q) <= 20q^2/(3pi^2) fails: {corr_bad}")
    # brute check of the lemma's left side (A = infinity, C = 1)
    worst = 0.0
    for q in range(2, 61):
        Q = 10 ** 6 * q
        for a in range(1, q + 1):
            if math.gcd(a, q) != 1:
                continue
            for beta in (1.0, -1.0, 1e-9, -1e-9):
                y2 = Q // 2
                s = 0.0
                for n in range(y2 - q + 1, y2 + 1):
                    if n % q == 0:
                        continue
                    frac = (a * n % q) / q + n * beta / (q * Q)
                    s += csc2(PI * frac)
                worst = max(worst, s / bound(q))
    print(f"brute max of lemma LHS / (20 C q^2/(3 pi^2)), q <= 60: {worst:.6f}")
    ok = (fails == [2, 4, 6] and above and not mid and not corr_bad and worst <= 1.0)
    if ok:
        print("CONFIRMED: for even q the printed display includes the extra term r = q/2; it "
              "exceeds C N(q) at q = 2, 4, 6, the midpoint step overshoots 20Cq^2/(3pi^2) for every "
              "even q, and with limit (q-1)/2 the proof works.")
    else:
        print("NOT CONFIRMED: the computation does not reproduce the claimed gap.")


if __name__ == "__main__":
    main()
