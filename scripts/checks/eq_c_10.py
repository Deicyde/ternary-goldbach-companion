"""Check of [H, (C.10)] (the constants of [Ram95] 7.284, 4.899 and c_E).

Claim: (i) [Ram95, Lemma 3.4], cited for both lines of (C.10), is proved there
with (3.9), prod_p (1 + (p^{1/3} + p^{2/3})/(p(p-1))) <= 8, and 7.284 =
0.9105 * 8; the product is in fact about 8.0836, so the cited argument gives
about 7.36, not 7.284 (the lemma itself holds). (ii) c_E = gamma + sum_p
log p/(p(p-1)) = 1.33258227573..., outside the printed 1.332582275 + O*(10^{-9}/3).

Book inputs (sumlaphi.tex):
  - l.179-187 (C.10) with 7.284 and 4.899, cited to [Ram95, Lemma 3.4].
  - l.188 c_E = gamma + sum_p log p/(p(p-1)) = 1.332582275 + O*(10^{-9}/3).
  Not in the book (from [Ram95], as quoted in the claim): D = 0.9105 and
  (3.9). Only the numerical content (the product exceeds 8; 0.9105 * 8 = 7.284)
  is checked here.

Method: (i) the factors all exceed 1, so the product is increasing; sieve the
primes up to 2*10^6 and report where the partial product passes 8.
(ii) Since 1/(p(p-1)) = sum_{k>=2} p^{-k} and sum_p log p p^{-s} = -P'(s) with
P'(s) = sum_m mu(m) zeta'(ms)/zeta(ms), one gets sum_p log p/(p(p-1)) =
sum_{n>=2} mu(n) zeta'(n)/zeta(n); evaluated with mpmath, cross-checked
against the numerical derivative of mpmath's primezeta and against the direct
prime sum to 2*10^6 (with tail bound).

Confirms if: the partial product exceeds 8 (so 0.9105 * product > 7.284), and
c_E lies outside [1.332582275 - 10^{-9}/3, 1.332582275 + 10^{-9}/3].

Run: PYTHONPATH=<mpmath dir> python3 -s eq_c_10.py

Ported from a 2026-11-06 check script.
"""
import math
from mpmath import mp, mpf, zeta, euler, diff, primezeta

N = 2 * 10**6
sieve = bytearray([1]) * (N + 1)
sieve[0] = sieve[1] = 0
for i in range(2, int(N**0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = bytearray(len(range(i * i, N + 1, i)))
primes = [i for i in range(N + 1) if sieve[i]]

logprod, cross = 0.0, None
for p in primes:
    logprod += math.log1p((p ** (1 / 3) + p ** (2 / 3)) / (p * (p - 1)))
    if cross is None and logprod > math.log(8):
        cross = p
prod = math.exp(logprod)
print("product over p <= %d: %.6f; first exceeds 8 at p = %s" % (N, prod, cross))
print("0.9105 * 8 = %.4f; 0.9105 * (partial product) = %.4f" % (0.9105 * 8, 0.9105 * prod))

mp.dps = 30
def mobius(n):
    r, m, d = 1, n, 2
    while d * d <= m:
        if m % d == 0:
            m //= d
            if m % d == 0:
                return 0
            r = -r
        d += 1
    return -r if m > 1 else r
S = sum(mobius(n) * zeta(n, derivative=1) / zeta(n) for n in range(2, 150))
S2 = sum(-diff(primezeta, kk) for kk in range(2, 120))
direct = sum(math.log(p) / (p * (p - 1)) for p in primes)
tail = (math.log(N) + 1) / N  # >= sum_{n>N} log n/(n(n-1))
cE = euler + S
print("sum_p log p/(p(p-1)): mobius/zeta formula %s, primezeta formula %s" % (mp.nstr(S, 20), mp.nstr(S2, 20)))
print("direct prime sum p <= %d: %.12f (true value in [this, this + %.1e])" % (N, direct, tail))
print("c_E = %s; printed interval [%s, %s]" % (mp.nstr(cE, 16), mp.nstr(mpf("1.332582275") - mpf(10)**-9 / 3, 13),
                                               mp.nstr(mpf("1.332582275") + mpf(10)**-9 / 3, 13)))

ok = (cross is not None and 0.9105 * prod > 7.284 and abs(S - S2) < mpf(10)**-20
      and direct <= S <= direct + tail and abs(cE - mpf("1.332582275")) > mpf(10)**-9 / 3)
if ok:
    print("CONFIRMED: the product in [Ram95, (3.9)] already exceeds 8 at p = %d (%.5f for p <= 2*10^6, so 0.9105 times it is > %.3f > 7.284), and c_E = %s lies outside 1.332582275 + O*(10^-9/3)."
          % (cross, prod, 0.9105 * prod, mp.nstr(cE, 13)))
else:
    print("NOT CONFIRMED: the computed values do not match the claim.")
