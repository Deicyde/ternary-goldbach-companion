# f_2: r1=(3/8)y^{4/15}; printed first line has x^{4/15}. Check 0.05699 = log(3/8)+(4/15)log 49 (i.e. uses x=49y).
from math import log, sqrt, e
euler = 0.5772156649015329
mpf = float
a = log(mpf(3)/8) + mpf(4)/15*log(49)
print("log(3/8) =", log(mpf(3)/8))
print("log(3/8)+(4/15)log49 =", a, "(printed 0.05699)")
y = mpf(10)**25; r0 = mpf(150000)
pre = mpf('3.2')*(log(y)/2)**(mpf(1)/6)/y**(mpf(1)/6)
f2y = pre*log(mpf(3)/8*y**(mpf(4)/15)/r0)
f2x = pre*log(mpf(3)/8*(49*y)**(mpf(4)/15)/r0)
print("f2 with r1=(3/8)y^{4/15} at y=1e25:", f2y)
print("f2 with (3/8)x^{4/15}  at y=1e25:", f2x, "(printed <= 0.001332)")
# confirms typo claim: x^{4/15} differs from r1, the second line is a valid upper bound for the y-version
ok = abs(a - mpf('0.05699')) < 1e-5 and f2y < f2x <= mpf('0.001332')
raise SystemExit(0 if ok else 1)
