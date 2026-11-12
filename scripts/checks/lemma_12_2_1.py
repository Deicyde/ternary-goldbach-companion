"""Check of [H, Lemma 12.2.1] (lem:suspiro, prod_{p|q or p<=m} p/(p-1) <= e^gamma(log(m+log q)+0.65771)).

Claim: two harmless slips in the proof. (a) It says t -> a + b/t is increasing
for t >= sqrt(b/a); that function is decreasing, the one used is t -> at + b/t.
(b) The chain n/phi(n) <= F(n) <= F(x) "for x >= n >= 27"
(F(t) = e^gamma loglog t + 2.50637/loglog t) is applied to n = P under the
condition q e^m >= 27, which does not give P >= 27; such pairs with
m + log q >= 8.53 exist and are covered by neither the chain nor the finite
check, though the lemma holds for them (P/phi(P) <= 3).  The lemma, 8.53 and
the worst case m = 1, q = 6 are correct.

Book inputs (l2normls.tex:433-461): the statement (12.18), epsilon_0 = 0.001102,
the [RS62 (3.42)] bound with 2.50637, "for all x >= n >= 27 (since ... t -> a+b/t
is increasing on t for t >= sqrt(b/a))", "if q e^m >= 27", the threshold 8.53,
and "the worst case is that of m = 1, q = 6".
Method: (a) evaluate a + b/t and at + b/t around sqrt(b/a); (b) the example
m = 1, q = 4096 (P = 2), and all squarefree P < 27 against the RHS at 8.53;
the 8.53 threshold; a brute force over m in {1} U primes <= 8.53 and
q <= e^8.53 for the worst case.  Confirms if (a) a+b/t decreases while at+b/t
increases past sqrt(b/a), (b) the example satisfies q e^m >= 27,
m + log q >= 8.53, P < 27, and the lemma holds there, and the worst case is
m = 1, q = 6 with value <= 0.65771.

Run: python3 -I lemma_12_2_1.py

Ported from a 2026-11-06 check script.
"""
import math

g = 0.5772156649015329
a, b = math.exp(g), 2.50637
t0 = math.sqrt(b / a)
print(f"sqrt(b/a) = {t0:.5f}; loglog n >= sqrt(b/a) iff n >= {math.exp(math.exp(t0)):.2f}")
f1 = lambda t: a + b / t
f2 = lambda t: a * t + b / t
dec = all(f1(t0 + 0.1 * k) > f1(t0 + 0.1 * (k + 1)) for k in range(50))
inc = all(f2(t0 + 0.1 * k) < f2(t0 + 0.1 * (k + 1)) for k in range(50))
print(f"(a) a+b/t decreasing past sqrt(b/a): {dec}; at+b/t increasing: {inc}")

def primes_of(n):
    ps, d = [], 2
    while d * d <= n:
        if n % d == 0:
            ps.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        ps.append(n)
    return ps

def ratio(ps):
    r = 1.0
    for p in ps:
        r *= p / (p - 1)
    return r

rhs = lambda m, q: a * (math.log(m + math.log(q)) + 0.65771)
m, q = 1, 4096
P = 2
ex = (q * math.e ** m >= 27, m + math.log(q) >= 8.53, P < 27, ratio([2]) <= rhs(m, q))
print(f"(b) m=1, q=4096: q e^m = {q*math.e:.0f}, m+log q = {1+math.log(q):.3f}, P = {P}, "
      f"P/phi(P) = 2 <= RHS = {rhs(m, q):.3f}: {ex}")
smallP = max(ratio(primes_of(n)) for n in range(2, 27))
print(f"max over P < 27 of P/phi(P) = {smallP:.3f}; RHS at m+log q = 8.53: {a*(math.log(8.53)+0.65771):.4f}")
thr = 0.001102 + (b / a) / math.log(8.53)
print(f"eps0 + (b/e^gamma)/log 8.53 = {thr:.7f} <= 0.65771: {thr <= 0.65771}")
best = (-1, None)
for m in (1, 2, 3, 5, 7):
    small = [p for p in (2, 3, 5, 7) if p <= m]
    for q in range(1, int(math.exp(8.53 - m)) + 1):
        if m + math.log(q) > 8.53:
            continue
        v = ratio(set(small) | set(primes_of(q))) / a - math.log(m + math.log(q))
        if v > best[0]:
            best = (v, (m, q))
print(f"finite region worst case: m, q = {best[1]}, value {best[0]:.7f}")
if dec and inc and all(ex) and smallP < a * (math.log(8.53) + 0.65771) and thr <= 0.65771 \
        and best[1] == (1, 6) and best[0] <= 0.65771:
    print("CONFIRMED: a+b/t is decreasing (at+b/t is the increasing one), and m=1, q=4096 meets 'q e^m >= 27' and m+log q >= 8.53 with P = 2 < 27, so the chain does not cover it, while the lemma holds there and its worst case m=1, q=6 is correct.")
else:
    print("NOT CONFIRMED: some computed value does not match the claim.")
