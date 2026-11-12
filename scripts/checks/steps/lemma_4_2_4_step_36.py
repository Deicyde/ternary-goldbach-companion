# Lemma 4.2.4 case (b): bound (2|eta'|_1/pi) q max(1,log(...)) log(q/2) at q=1 vs empty sum 0
import math, sys
eta1=8*math.log(2); c0=31.521
for x in (1e20,1e25):
    q=1
    b=2*eta1/math.pi*q*max(1,math.log(c0*math.e**3*q*q/(4*math.pi*eta1*x)))*math.log(q/2)
    print("x=%g q=1 bound=%.4f (sum over m<=1/2 is empty = 0)"%(x,b))
sys.exit(0 if b<0 else 1)
