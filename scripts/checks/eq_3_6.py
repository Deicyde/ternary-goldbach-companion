"""Eq 3.6: Vaughan's identity as printed, with +mu_{<=U}*Lambda_{<=V}*1.

Claim: (3.6) as printed is false; with the sign of the second term changed to -, it holds (a typo).

Book inputs (intromin.tex):
  - l.207-209: Lambda = mu_{<=U}*log + mu_{<=U}*Lambda_{<=V}*1 + mu_{>U}*Lambda_{>V}*1 + Lambda_{<=V}.
  - l.211-215: f_{<=z}(n) = f(n) for n <= z, 0 otherwise; f_{>z} = f - f_{<=z}; 1 the constant function.

Both sides are computed for n <= 200 and U, V in {1, ..., 6}, as sums of log p with integer
coefficients over the primes p <= 200 (exact), and compared.

Confirms if: the printed identity fails (at n = 2, U = V = 2 its right side is 3 log 2 against
Lambda(2) = log 2), and the identity with - holds for every n and U, V tested.

Run: python3 -I eq_3_6.py
"""
from collections import Counter

N = 200
PRIMES = [p for p in range(2, N + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def factor(n):
    f = Counter()
    for p in PRIMES:
        while n % p == 0:
            f[p] += 1
            n //= p
    return f


def mu(n):
    f = factor(n)
    return 0 if any(e > 1 for e in f.values()) else (-1) ** len(f)


# a value is a Counter p -> integer coefficient of log p
def Lam(n):
    f = factor(n)
    return Counter({next(iter(f)): 1}) if len(f) == 1 else Counter()


def log(n):
    return Counter(factor(n))


def scale(c, v):
    return Counter({p: c * e for p, e in v.items()})


def add(*vs):
    out = Counter()
    for v in vs:
        for p, e in v.items():
            out[p] += e
    return Counter({p: e for p, e in out.items() if e})


def conv(a, b, n):
    """(a * b)(n) for an integer function a and a log-valued function b."""
    return add(*[scale(a(d), b(n // d)) for d in range(1, n + 1) if n % d == 0])


def rhs(n, U, V, sign):
    muU = lambda d: mu(d) if d <= U else 0
    muGU = lambda d: mu(d) if d > U else 0
    LamV = lambda m: Lam(m) if m <= V else Counter()
    LamGV = lambda m: Lam(m) if m > V else Counter()
    LamV1 = lambda m: add(*[LamV(d) for d in range(1, m + 1) if m % d == 0])     # Lambda_{<=V} * 1
    LamGV1 = lambda m: add(*[LamGV(d) for d in range(1, m + 1) if m % d == 0])   # Lambda_{>V} * 1
    return add(conv(muU, log, n), scale(sign, conv(muU, LamV1, n)), conv(muGU, LamGV1, n), LamV(n))


def main():
    printed_fails, corrected_fails = [], []
    for U in range(1, 7):
        for V in range(1, 7):
            for n in range(1, N + 1):
                if rhs(n, U, V, +1) != Lam(n):
                    printed_fails.append((n, U, V))
                if rhs(n, U, V, -1) != Lam(n):
                    corrected_fails.append((n, U, V))
    at = rhs(2, 2, 2, +1)
    print(f'printed: {len(printed_fails)} failures, first {printed_fails[:3]}; at n = 2, U = V = 2 the right side is '
          f'{at.get(2, 0)} log 2 against Lambda(2) = log 2')
    print(f'with -: {len(corrected_fails)} failures')
    if printed_fails and not corrected_fails and dict(at) == {2: 3}:
        print("CONFIRMED: (3.6) as printed fails (n = 2, U = V = 2: right side 3 log 2, Lambda(2) = log 2), "
              "and with -mu_{<=U}*Lambda_{<=V}*1 it holds for all n <= 200, U, V <= 6: a sign typo.")
    else:
        print('NOT CONFIRMED: the printed and corrected identities do not behave as claimed.')


main()
