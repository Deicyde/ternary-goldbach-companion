# kappa_6 = 0.60428 = 4*0.15107 rests on (5.36): int_1^T H_2(S) dS/S <= 0.15107 log T, where
# H_2 = (4/pi^2) G_2(S) for 1<=S<16, 0.15107 for S>=16, and
# G_2(S) = sum_{s<=S, s odd} (1/s) int_{1/2}^1 g_2(uS/s) du,
# g_2(x) = sum_{r1,r2<=x, (r1,r2)=1, r1 r2 odd} mu(r1)mu(r2)/(sigma(r1)sigma(r2)).
# Computes sup_T (int_1^T H_2/S - 0.15107 log T). Exit 0 if positive (claim confirmed), 1 otherwise.
import math, sys
from fractions import Fraction as F
def mu(n):
    r=1; d=2
    while d*d<=n:
        if n%d==0:
            n//=d
            if n%d==0: return 0
            r=-r
        d+=1
    return -r if n>1 else r
def sigma(n): return sum(d for d in range(1,n+1) if n%d==0)
N=16
g=[F(0)]*(N+1)
for x in range(1,N+1):
    t=F(0)
    for r1 in range(1,x+1,2):
        for r2 in range(1,x+1,2):
            if math.gcd(r1,r2)==1 and mu(r1) and mu(r2):
                t+=F(mu(r1)*mu(r2),sigma(r1)*sigma(r2))
    g[x]=t
def G2(S):
    tot=0.0; s=1
    while s<=S:
        # int_{1/2}^1 g(floor(uS/s)) du, breakpoints at u=m s/S
        a=0.5; val=0.0
        while a<1-1e-15:
            m=math.floor(a*S/s+1e-12)
            b=min(1.0,(m+1)*s/S)
            val+=(b-a)*float(g[m]) if m>=1 else 0.0
            a=b
        tot+=val/s; s+=2
    return tot
c=4/math.pi**2
# integrate in log S with fine steps, midpoint rule on S in [1,16]
h=1e-4; I=0.0; best=(-1,1); S=1.0
while S<16:
    Sm=S+h/2; I+=c*G2(Sm)/Sm*h; S+=h
    d=I-0.15107*math.log(S)
    if d>best[0]: best=(d,S)
J4=0.0; S=1.0
while S<4:
    Sm=S+h/2; J4+=G2(Sm)/Sm*h; S+=h
print("int_1^4 G_2/S = %.5f vs 0.37273 log 4 = %.5f"%(J4,0.37273*math.log(4)))
print("sup_T (int_1^T H_2/S - 0.15107 log T) = %.6f at T = %.3f"%best)
sys.exit(0 if best[0]>1e-4 else 1)
