"""Check of [H, Eq (12.12)] (eq:malito, Ramare's asymptotic for G_d(R)).

Claim: the proof in [Ram95] of the lemma quoted as (12.12) ends with
(3.9): prod_p (1 + (p^(1/3)+p^(2/3))/(p(p-1))) <= 8, giving the constant
7.284 = 0.9105*8 (0.9105 the constant of [Ram95, Lemma 3.3]).  The product is
in fact ~8.0836 > 8, so that argument gives ~7.36, not 7.284; (12.12) as
stated is nevertheless true.

Book inputs:
  - l2normls.tex:358-367  (12.12) with constant 7.284 and f_1(d), whose local
                          factor contains (1 + (p^(1/3)+p^(2/3))/(p(p-1)))^(-1).
  - [Ram95] (3.9) and Lemma 3.3 (0.9105) are from the cited paper, not the book.
Method: every factor exceeds 1, so the partial product over p <= X = 10^7 is
a lower bound for the full product (float error ~1e-12, far below the
margin).  The tail over p > 10^7 is
bounded above crudely by a sum over all integers and estimated by the
prime-number-theorem integral int_X^inf (t^(-4/3)+t^(-5/3))/log t dt.
Confirms if the partial product exceeds 8 (reporting the first prime where it
does) and 0.9105 * (estimate of the full product) > 7.284.
The truth of (12.12) itself is not re-checked here.

Run: python3 -I eq_12_12.py

Ported from a 2026-11-06 check script.
"""
import math

X = 10 ** 7
s = bytearray([1]) * (X + 1); s[0] = s[1] = 0
for i in range(2, int(X ** 0.5) + 1):
    if s[i]:
        s[i * i::i] = bytearray(len(s[i * i::i]))
logP = 0.0
first = None
for p in range(2, X + 1):
    if s[p]:
        logP += math.log1p((p ** (1 / 3) + p ** (2 / 3)) / (p * (p - 1)))
        if first is None and logP > math.log(8):
            first = (p, math.exp(logP))
P = math.exp(logP)
# tail: sum_{p>X} log(1+f) <= sum_{p>X} (p^-4/3 + p^-5/3) * p/(p-1); upper bound via all n > X
tail_up = 1.0000001 * (3 * X ** (-1 / 3) + 1.5 * X ** (-2 / 3))
# prime-density estimate of the tail: int_X^inf (t^-4/3 + t^-5/3)/log t dt,
# with t = X e^u, computed by the midpoint rule
L = math.log(X); h = 1e-3
tail_est = sum((X ** (-1 / 3) * math.exp(-(k + .5) * h / 3) + X ** (-2 / 3) * math.exp(-2 * (k + .5) * h / 3))
               / (L + (k + .5) * h) * h for k in range(200000))
print(f"product first exceeds 8 at p = {first[0]} (value {first[1]:.7f})")
print(f"product over p <= 10^7 = {P:.6f}")
print(f"full product in [{P:.6f}, {P*math.exp(tail_up):.6f}], estimate {P*math.exp(tail_est):.5f}")
print(f"0.9105 * 8 = {0.9105*8:.4f}; 0.9105 * product >= {0.9105*P:.4f}; with tail estimate {0.9105*P*math.exp(tail_est):.4f}")
if first is not None and P > 8 and abs(0.9105 * 8 - 7.284) < 1e-9 and 0.9105 * P > 7.284:
    print(f"CONFIRMED: the product in [Ram95] (3.9) is about {P*math.exp(tail_est):.4f} > 8 (it passes 8 at p = {first[0]}), so the argument behind 7.284 = 0.9105*8 gives about {0.9105*P*math.exp(tail_est):.2f}.")
else:
    print("NOT CONFIRMED: the product does not exceed 8.")
