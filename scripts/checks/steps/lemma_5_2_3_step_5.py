# (zeromb) in Lemma 5.2.3 as printed (sum over ALL m in (A0,A1]) vs with m odd.
# Counterexample data: alpha = 1/101 so 2alpha = a/q with a=2, q=101, (a,q)=1, any Q>=q
# (take Q=1e9, rho=q/Q); varrho=1, A0=0, A1=2q (so A1-A0 <= 2 varrho q); W=100, W'=50.
# Exit 0 if the printed (all-m) inequality fails (confirms claim), 1 otherwise.
import cmath, math, sys
def primes(lo,hi):
    return [n for n in range(max(2,lo+1),hi+1) if all(n%d for d in range(2,int(n**0.5)+1))]
W,Wp,q,a=100,50,101,2
alpha=a/(2*q); Q=1e9; rho=q/Q; vr=1.0; A0,A1=0,2*q
P=primes(Wp,W); S2=sum(math.log(p)**2 for p in P)
def T(m): return abs(sum(math.log(p)*cmath.exp(2j*math.pi*alpha*m*p) for p in P))**2
allm=sum(T(m) for m in range(A0+1,A1+1)); odd=sum(T(m) for m in range(A0+1,A1+1) if m%2)
rhs=(W-Wp+q/(1-vr*rho))*S2
print("sum over all m: %.6g ; sum over odd m: %.6g ; RHS of (zeromb): %.6g"%(allm,odd,rhs))
print("all-m holds:",allm<=rhs," odd-m holds:",odd<=rhs)
sys.exit(0 if allm>rhs else 1)
