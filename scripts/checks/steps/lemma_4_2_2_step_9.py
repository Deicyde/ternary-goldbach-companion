# Lemma 4.2.2: is sum_{m<=N, m odd} m = (N+1)^2/4 for real N=M/q? (claim: only <=)
import sys, math
def S(N): return sum(m for m in range(1,int(math.floor(N))+1,2))
bad=[]; ok_le=True
for k in range(1,400):
    N=k/7
    if S(N)>(N+1)**2/4+1e-12: ok_le=False
    if abs(S(N)-(N+1)**2/4)>1e-12: bad.append(N)
print("N=2: sum =",S(2),"(N+1)^2/4 =",9/4)
print("equality fails for",len(bad),"of 399 sampled N; '<=' holds:",ok_le)
sys.exit(0 if bad and ok_le else 1)
