# Theorem 3.1.1 / (6.77): AM-GM constant.
from mpmath import mp, mpf, log, sqrt
import sys
mp.dps = 30
x1, q0 = mpf(10)**25, 2*mpf(10)**5
def C(x, t): return log(1 + log(4*t)/(2*log(9*x**(mpf(1)/3)/(mpf('2.004')*t))))
rho = (C(x1, 2*q0)*(log(2*q0) + mpf('0.002')) + log(8*q0)/2)/(mpf('0.30214')*log(2*q0) + mpf('0.67506'))
sr = sqrt(rho)
printed = (log(2)/sr + sr/2*mpf('0.67506'))/2
correct = log(2)/(2*sr) + sr/2*mpf('0.67506')
print("rho =", rho, " 1/(2sqrt rho) =", 1/(2*sr), " 1/(4 sqrt rho)+sqrt(rho)*0.30214/2 =", 1/(4*sr) + sr*mpf('0.30214')/2)
print("printed constant =", printed, " correct constant =", correct)
sys.exit(0 if abs(printed - mpf('0.49911')) < 1e-4 and correct > mpf('0.81') else 1)
