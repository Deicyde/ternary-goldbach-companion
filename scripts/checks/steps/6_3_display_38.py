# Book Sec. 6.3 (minarctotals.tex l.2127-2143), case x/8U < q <= Q.
# E(t): the unsimplified expression (l.2127-2133); D(t): the simplified display (l.2138-2142).
# kappa_2 <= 1.93768, kappa_9 <= 3.9086, c' = 500 sqrt 6, t >= t0 = log(2.16e20).
# Checks: D(t) <= 0.10327 (as printed)?  D(t) <= 0.10327 t^{3/2}?  E(t) <= 0.10327 t^{3/2}?
# Exit 0 if the printed display is false (confirms the claim that it is wrong as printed), else 1.
import math, sys
k2,k9=1.93768,3.9086; c=500*math.sqrt(6)
def E(t):
    a=2*t/3-math.log(c); b=t/3-math.log(3)
    return ((k2*math.sqrt(2*a)+k9)*math.sqrt(3)+k2*math.sqrt(a)/math.sqrt(c)
            +2*k2/3*(a**1.5-b**1.5)*(math.sqrt(c)/(2*math.sqrt(2))*math.exp(-t/6)+1/math.sqrt(c)))
def D(t):
    return ((2*k2+math.sqrt(3)*k9)*math.sqrt(t)+k2/math.sqrt(c)*math.sqrt(2/3)*math.sqrt(t)
            +2*k2/3*(2**1.5-1)/3**1.5*t**1.5*(math.sqrt(c)/(2*math.sqrt(2))*math.exp(-t/6)+1/math.sqrt(c)))
t0=math.log(2.16e20)
ts=[t0+k*0.01 for k in range(0,200000)]
print("D(t0) = %.6f vs printed bound 0.10327"%D(t0))
print("max D(t)/t^1.5 on [t0,t0+2000] = %.6f (at t0)"%max(D(t)/t**1.5 for t in ts))
print("max E(t)/t^1.5 on [t0,t0+2000] = %.6f (at t0)"%max(E(t)/t**1.5 for t in ts))
sys.exit(0 if D(t0)>0.10327 else 1)
