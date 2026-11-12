# 1312.7748 Lemma 4.2 (lem:merkel): is F(r)=e^g loglog r + 2.50637/loglog r > e^g*2.50637 for all r>e?
import math, sys
g=0.57721566490153286
a=math.exp(g); b=2.50637
F=lambda r: a*math.log(math.log(r))+b/math.log(math.log(r))
tmin=math.sqrt(b/a); rmin=math.exp(math.exp(tmin))
print("e^gamma*2.50637 =", a*b)
print("min F = 2 sqrt(ab) =", 2*math.sqrt(a*b), "at r =", rmin, "; F(rmin)=", F(rmin))
print("min F > 3:", 2*math.sqrt(a*b)>3)
sys.exit(0 if F(rmin) < a*b and 2*math.sqrt(a*b)>3 else 1)
