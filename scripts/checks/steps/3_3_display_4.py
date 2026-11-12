# (3.11): sum_n Lambda(n) e(an) eta(n/x) - sum_{(n,v)=1} ... = sum over n with (n,v)>1, not n|v.
import math, sys
def Lam(n):
    for p in range(2, n+1):
        if n % p == 0:
            m = n
            while m % p == 0: m //= p
            return math.log(p) if m == 1 else 0.0
    return 0.0
v, X = 2, 20
true_rem = sum(Lam(n) for n in range(1, X+1) if math.gcd(n, v) > 1)
printed = sum(Lam(n) for n in range(1, X+1) if v % n == 0)
print("eta = 1_[0,1], x=20, alpha=0: remainder =", true_rem, " printed S_{0,v} =", printed)
sys.exit(0 if abs(true_rem - printed) > 1e-9 else 1)
