# Lemma 9.3.1 (expform.tex 1199-1239): hypotheses T0>=max(10 pi|d|,50), Gaussian term only when |d|>20/(3pi).
# Checks: y=T0/(pi|d|)>=4pi? c1=1/(2|d|)<=3/16? T0>=4pi^2|d|? and the effect on the constant 1.578.
from math import pi, log, e
import sys
c = 0.1065
dmin = 20/(3*pi)
print("y lower bound from hyp: 10 ; 4pi =", 4*pi)
print("c1 sup = 1/(2*dmin) =", 1/(2*dmin), "; 3/16 =", 3/16)
# counterexample: d=3, T0=10*pi*3 (>=50, and < 1.5 (pi d)^2 so Gaussian term present)
d = 3.0; T0 = 10*pi*d
print("d=3,T0=%.3f: T0>=50:%s, T0<1.5(pi d)^2=%.3f:%s, 4pi^2 d=%.3f" % (T0, T0>=50, 1.5*(pi*d)**2, T0<1.5*(pi*d)**2, 4*pi**2*d))
def a_of(y, c1):
    return (c1*y + log(e*y)/(2*c))/(y*log(e*y)/(2*c) - 1/(4*c*c*y))
print("a(y=10, c1=3pi/40) =", a_of(10, 3*pi/40), "(text: <=0.117)")
# constant: R = 1.487 + 2.566(1+1/log(T0/pi d))/(T0/d), text's first inequality in (caplor)
for r, name in [(10*pi, "T0/d=10pi"), (4*pi**2, "T0/d=4pi^2")]:
    print(name, "->", 1.487 + 2.566*(1+1/log(r/pi))/r)
# direct ratio of (caplor) line 1 to T0 log(qT0/2pi), q=1, over the admissible region
worst = 0
for i in range(1, 400):
    dd = dmin*(1+i*0.01)
    y = 10.0
    if y >= 1.5*pi*dd: continue
    T = pi*dd*y
    if T < 50: continue
    for q in (1, 2, 3, 10):
        num = (1.487*T + 2.194*dd)*log(q*dd/2) + 1.487*T*log(T/(pi*dd)) + 2.566*dd*log(e*T/(pi*dd))
        R = num/(T*log(q*T/(2*pi)))
        worst = max(worst, R)
print("max ratio (caplor line1)/(T0 log(qT0/2pi)) at y=10:", worst, "(text: 1.578)")
ok = (10 < 4*pi) and (1/(2*dmin) > 3/16) and (10*pi*d < 4*pi**2*d) and worst > 1.578
sys.exit(0 if ok else 1)
