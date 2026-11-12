"""Check of [H, Eq (9.41)] (eq:milstei, proof of Lemma 9.2.1).

Claim: the proof of (9.41) applies (9.40), stated for y >= e, at
y = T0/(pi|delta|); under the lemma's hypothesis T0 >= 50 this can be < e
(for |delta| > T0/(pi e)) and then (9.40) itself fails, so the term-by-term
bound breaks. The combined inequality (9.41) still holds, since its first two
terms sum to (|delta|/2) log(qT0/2pi)/(2c'y) and qT0/2pi >= e.

Book inputs (expform.tex):
  - l.775: hypothesis T0 >= 50 (the 2013 hypothesis T0 >= max(4pi^2|delta|,100)
    is commented out at l.776).
  - l.884-888 (9.40): int_y^oo (log t) e^{-ct^2} dt <= (log y)/(2cy) e^{-cy^2}, for y >= e.
  - l.889-897 (9.41) with c' = 0.1065 (l.898).
Test: q = 1, T0 = 50, delta = 10, 30, 100 (mpmath quadrature).

Confirms if: (9.40) fails at y = T0/(pi|delta|) for some admissible delta,
while (9.41) as a whole holds there.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_9_41.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30
cp = mp.mpf("0.1065")
q, T0 = 1, mp.mpf(50)
fails_940, holds_941 = [], []
for d in [mp.mpf(10), mp.mpf(30), mp.mpf(100)]:
    y = T0 / (mp.pi * d)
    lhs40 = mp.quad(lambda t: mp.log(t) * mp.e ** (-cp * t ** 2), [y, 1, 10, mp.inf])
    rhs40 = mp.log(y) / (2 * cp * y) * mp.e ** (-cp * y ** 2)
    lhs41 = mp.quad(lambda T: mp.e ** (-cp * (T / (mp.pi * d)) ** 2)
                    * (mp.log(q * T / (2 * mp.pi)) / (2 * mp.pi) + 1 / (4 * T)), [T0, T0 * 4, mp.inf])
    rhs41 = ((d / 2 * mp.log(T0 / (mp.pi * d))) / (2 * cp * y) + (d / 2 * mp.log(q * d / 2)) / (2 * cp * y)
             + 1 / (8 * cp * y ** 2)) * mp.e ** (-cp * y ** 2)
    print("delta = %s: y = %s; (9.40): %s vs bound %s; (9.41): %s vs bound %s"
          % (d, mp.nstr(y, 6), mp.nstr(lhs40, 6), mp.nstr(rhs40, 6), mp.nstr(lhs41, 6), mp.nstr(rhs41, 6)))
    fails_940.append(lhs40 > rhs40)
    holds_941.append(lhs41 <= rhs41)

if any(fails_940) and all(holds_941):
    print("CONFIRMED: at q = 1, T0 = 50, (9.40) fails at y = T0/(pi|delta|) for delta = 10 (y < e), "
          "but the combined (9.41) holds for delta = 10, 30, 100.")
else:
    print("NOT CONFIRMED: (9.40) held at every tested y, or (9.41) failed.")
