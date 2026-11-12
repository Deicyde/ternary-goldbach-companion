# Lemma 4.2.4 case (b) display (typeI.tex l.1762): bound (2|eta'|_1/pi) q max(1, log(c0 e^3 q^2/(4pi|eta'|_1 x))) log(q/2)
# for sum_{m<=q/2} (log m)|T_m|. At q=1 (allowed: lem:bogus only assumes q<=Q0) the sum is empty (=0)
# but log(1/2)<0 and the other factors are positive. Sample eta'_1, c0, x values.
# Exit 0 if the bound is negative (printed statement false at q=1), else 1.
import math, sys
vals=[]
for e1 in (0.5,1.0,2.0,5.0):
    for c0 in (1.0,10.0,31.0):
        for x in (1e3,1e10,1e25):
            q=1
            b=2*e1/math.pi*q*max(1,math.log(c0*math.e**3*q*q/(4*math.pi*e1*x)))*math.log(q/2)
            vals.append(b)
print("max of bound at q=1 over samples: %.6g (sum is 0)"%max(vals))
sys.exit(0 if max(vals)<0 else 1)
