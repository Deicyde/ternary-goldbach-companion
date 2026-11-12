# (hutterite), Lemma 9.1.1: printed (2/3)(t^{-1/2}+t^{1/2}) <= |log t| for all t>0;
# intended |log t| <= (2/3)(t^{-1/2}+t^{1/2}). With t=e^u: (4/3)cosh(u/2) vs |u|.
# Exit 0 if printed fails and reversed holds for all t (confirms the typo claim), else 1.
import math, sys
f=lambda u:(4/3)*math.cosh(u/2)-abs(u)
us=[k/10000 for k in range(-400000,400001)]
m=min(us,key=f)
print("printed at t=1: %.4f <= 0 ? %s"%(4/3, 4/3<=0))
print("min over u in [-40,40] of (4/3)cosh(u/2)-|u| = %.6f at |u|=%.4f"%(f(m),abs(m)))
sys.exit(0 if f(m)>0 else 1)
