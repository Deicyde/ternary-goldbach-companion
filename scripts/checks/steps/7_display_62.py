# R_{y,r0} vs R_{y,2r0} at y=1e150 (and 2y/log y); effect on 0.10426.
from math import log, sqrt, e
euler = 0.5772156649015329
mpf = float
def R(z, t):
    return mpf('0.27125')*log(1 + log(4*t)/(2*log(9*z**(mpf(1)/3)/(mpf('2.004')*t)))) + mpf('0.41415')
r0 = mpf(150000); y = mpf(10)**150
P2 = lambda t: t**2 + 4*t + 8
q = P2(log(2*r0))/sqrt(r0)
z2 = 2*y/log(y)
for name, z in (("y", y), ("2y/log y", z2)):
    print(name, " R_{z,r0} =", R(z, r0), " R_{z,2r0} =", R(z, 2*r0))
print("P2(log 2r0)/sqrt r0 =", q)
print("0.43086^2*q =", mpf('0.43086')**2*q, " R_{y,2r0}^2*q =", R(y, 2*r0)**2*q)
print("0.43113^2*q =", mpf('0.43113')**2*q, " R_{2y/logy,2r0}^2*q =", R(z2, 2*r0)**2*q)
d = mpf(4)/15*log(y) - log(800000)
j = mpf('0.97781')*sqrt(R(y,2*r0)**2*q + mpf('0.49214')/d) + mpf('0.02219')*sqrt(R(z2,2*r0)**2*q + mpf('0.49584')/d)
print("jijona with corrected R at y=1e150:", j, "(printed <= 0.33247; needed <= 0.4153461)")
raise SystemExit(0 if R(y, 2*r0)**2*q > mpf('0.10426') else 1)
