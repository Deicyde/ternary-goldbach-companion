"""Lemma 4.1.3 ([H], arXiv:1501.05438v2): the small-C case of the proof of (4.6).

Claim: the proof bounds the left side of (4.6) by
X = 2 sum_{r <= q/2} min(B/sin(pi(r-1/2)/q), C/sin^2(pi(r-1/2)/q)); for small C, X itself
exceeds the right side (2Bq/pi) max(2, log(C e^3 q/(B pi))), worst at C = B sin(pi/2q) (ratio
up to 1.0696); and the printed relaxation to C = B sin(pi/q) for C < B sin(pi/q) gives the
factor 3 + log((q/pi) sin(pi/q)) >= 2.548 (and pi/(q sin(pi/2q)) + cos(pi/q) >= 2.221 before the
last simplification), which never meets max(2, log(C e^3 q/(B pi))) there.  The main range
B sin(pi/q) <= C <= B is unaffected.

Book inputs (book/src/typeI.tex):
  - statement (4.6), lines 391-402;
  - the majorant X, lines 404-410;
  - the case B sin(pi/q) <= C <= B and its final bound B (q/pi) log(C e^3 q/(B pi)), lines 411-449;
  - the relaxation "If C < B sin pi/q ... relax the input to C = B sin pi/q", lines 455-456.

B = 1.  For 2 <= q <= 400 the script maximizes X / RHS over C on a fine grid plus the point
C = sin(pi/2q); it evaluates the relaxed factors for 2 <= q <= 2000; it checks that on
sin(pi/q) <= C <= 1 X stays below RHS; and, as a sanity check that the lemma itself holds, it
evaluates the lemma's left side directly (alpha = a/q + beta/(qQ), y2 = Q/2, y2 - y1 = q) for
q <= 40.  Confirmed if X > RHS at C = sin(pi/2q) for every q <= 400 except q = 3, both relaxed
factors exceed 2 for every q (so the factor-2 range C <= B pi/(e q) is not covered), X <= RHS
on the main range, and the direct left side stays below RHS.

Run: python3 -I lemma_4_1_3.py
Ported from a 2026-11-06 check script.
"""
import math

PI = math.pi


def X(q, C):
    s = 0.0
    for r in range(1, q // 2 + 1):
        t = math.sin(PI * (r - 0.5) / q)
        s += min(1.0 / t, C / (t * t))
    return 2 * s


def rhs(q, C):
    return 2 * q / PI * max(2.0, math.log(C * math.e ** 3 * q / PI))


def main():
    over = []
    ratios = {}
    for q in range(2, 401):
        c0 = math.sin(PI / (2 * q))
        ratios[q] = X(q, c0) / rhs(q, c0)
        if ratios[q] > 1:
            over.append(q)
    notover = [q for q in range(2, 401) if q not in over]
    for q in (2, 3, 4, 5, 10, 140, 400):
        print(f"q={q}: X/RHS at C = sin(pi/2q): {ratios[q]:.6f}")
    print(f"q in [2,400] with X/RHS <= 1 at C = sin(pi/2q): {notover}")
    # sup over a C-grid is attained at C = sin(pi/2q) (check for a few q)
    for q in (4, 10, 140):
        grid = [math.sin(PI / q) * k / 4000 for k in range(1, 4001)]
        g = max(X(q, C) / rhs(q, C) for C in grid)
        print(f"q={q}: max X/RHS over C in (0, sin(pi/q)] grid = {g:.6f}")
    relax = min(3 + math.log(q / PI * math.sin(PI / q)) for q in range(2, 2001))
    pre = min(PI / (q * math.sin(PI / (2 * q))) + math.cos(PI / q) for q in range(2, 2001))
    print(f"min over 2<=q<=2000 of 3 + log((q/pi) sin(pi/q)) = {relax:.4f}")
    print(f"min over 2<=q<=2000 of pi/(q sin(pi/2q)) + cos(pi/q) = {pre:.4f}")
    cover = all(math.pi / (math.e * q) < math.sin(PI / q) for q in range(2, 2001))
    print(f"B pi/(e q) < B sin(pi/q) for all 2<=q<=2000: {cover}")
    main_max = 0.0
    for q in range(2, 401):
        lo = math.sin(PI / q)
        for k in range(0, 401):
            C = lo + (1 - lo) * k / 400
            main_max = max(main_max, X(q, C) / rhs(q, C))
    print(f"max X/RHS on sin(pi/q) <= C <= 1, q <= 400: {main_max:.6f}")
    # direct evaluation of the lemma's left side
    direct = 0.0
    for q in range(2, 41):
        Q = 10 ** 6 * q
        y2 = Q // 2
        Cs = [math.sin(PI / (2 * q)) * f for f in (0.25, 0.5, 1.0, 1.5, 2.0, 3.0)] + [0.5, 1.0]
        for a in range(1, q + 1):
            if math.gcd(a, q) != 1:
                continue
            for beta in (1.0, -1.0, 1e-9, -1e-9):
                ts = []
                for n in range(y2 - q + 1, y2 + 1):
                    if n % q:
                        fr = (a * n % q) / q + n * beta / (q * Q)
                        ts.append(abs(math.sin(PI * fr)))
                for C in Cs:
                    s = sum(min(1 / t, C / t ** 2) for t in ts)
                    direct = max(direct, s / rhs(q, C))
    print(f"max direct LHS/RHS of (4.6), q <= 40: {direct:.6f}")
    ok = (notover == [3] and relax > 2 and pre > 2 and cover and main_max <= 1
          and direct <= 1)
    if ok:
        print("CONFIRMED: for C near B sin(pi/2q) the proof's majorant X exceeds the right side "
              "of (4.6) (ratio up to 1.0696), and the relaxation to C = B sin(pi/q) gives a factor "
              ">= 2.221 > 2, so the small-C range is not proved; the main range holds.")
    else:
        print("NOT CONFIRMED: the computation does not reproduce the claimed gap.")


if __name__ == "__main__":
    main()
