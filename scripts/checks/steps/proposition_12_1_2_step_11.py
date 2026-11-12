# Prop 12.1.2: 2/(q q') >= 1/(2qQ) + 1/(2Qq')  <=>  q + q' <= 4Q; holds for even q,q' <= 2Q.
import sys
Q = 50
ok = all(2/(q*r) >= 1/(2*q*Q) + 1/(2*Q*r) - 1e-15 for q in range(2, 2*Q+1, 2) for r in range(2, 2*Q+1, 2))
odd_even = all(1/(q*r) >= 1/(4*q*Q) + 1/(2*Q*r) - 1e-15 for q in range(1, Q+1, 2) for r in range(2, 2*Q+1, 2))
print("both even, q,q'<=2Q:", ok, "; odd q<=Q, even q'<=2Q:", odd_even)
sys.exit(0 if ok and odd_even else 1)
