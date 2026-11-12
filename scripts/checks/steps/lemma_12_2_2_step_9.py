# Check (charpy) lower bound G(R) >= log R + 1.312 on [182,184]; so Q/Q0 >= 182 suffices.
import math
N=200
phi=list(range(N+1)); 
for p in range(2,N+1):
    if phi[p]==p:
        for k in range(p,N+1,p): phi[k]-=phi[k]//p
def sqf(n):
    d=2
    while d*d<=n:
        if n%(d*d)==0: return False
        d+=1
    return True
G=0.0; ok=True; worst=1e9
for r in range(1,185):
    if sqf(r): G+=1.0/phi[r]
    # G constant on [r, r+1); worst at right end r+1 (sup), check for R in [182,184]
    if 182<=r<=184:
        Rend=min(r+1,184)
        m=G-math.log(Rend)
        worst=min(worst,m); print("R in [%d,%d): G-logR >= %.5f"%(r,r+1,m))
print("min of G(R)-log R on [182,184]: %.5f (need >= 1.312)"%worst)
raise SystemExit(0 if worst>=1.312 else 1)
