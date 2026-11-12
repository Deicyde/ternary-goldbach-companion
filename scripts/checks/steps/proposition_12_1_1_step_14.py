# l2normls.tex 136-145: for chi primitive mod q, r coprime to q, a_n supported on primes > sqrt x:
#   sum_{b<=qr,(b,qr)=1} conj(chi)(b) S(b/qr + alpha) = conj(chi)(r) tau(conj chi) mu(r) sum a_n e(alpha n) chi(n),
# so |RHS|^2 = mu(r)^2 q |sum a_n e(alpha n) chi(n)|^2, and the printed equality (no mu^2(r)) fails for r=4.
# Exit 0 if printed equality fails for non-squarefree r and holds for squarefree r (claim confirmed).
import cmath, math
e = lambda t: cmath.exp(2j*math.pi*t)
q = 3
chi = lambda n: [0, 1, -1][n % 3]          # primitive character mod 3 (real)
P = [29, 31, 37, 41, 43, 47, 53]   # primes > r (n coprime to r)
a = {p: 1 + 0.1*i for i, p in enumerate(P)}
alpha = 0.1234
S = lambda t: sum(a[p]*e(t*p) for p in P)
lhs = q*abs(sum(a[p]*e(alpha*p)*chi(p) for p in P))**2
ok = True
for r in (1, 2, 4, 5, 8, 10):
    if math.gcd(r, q) != 1: continue
    rhs = abs(sum(chi(b)*S(b/(q*r)+alpha) for b in range(1, q*r+1) if math.gcd(b, q*r) == 1))**2
    sqf = all(r % (p*p) for p in range(2, r+1))
    print("r=%d squarefree=%s: q|..|^2 = %.6f, |sum_b ...|^2 = %.6f" % (r, sqf, lhs, rhs))
    if sqf != (abs(lhs-rhs) < 1e-6*lhs): ok = False
raise SystemExit(0 if ok else 1)
