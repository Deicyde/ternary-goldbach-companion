# Lemma 12.2.1: a+b/t is decreasing; a t + b/t is increasing for t >= sqrt(b/a).
# Used with a=e^gamma, b=2.50637, t=log log n, n>=27.
import math, sys
g = 0.5772156649015329
a, b = math.exp(g), 2.50637
f1 = lambda t: a + b/t
f2 = lambda t: a*t + b/t
t0 = math.sqrt(b/a)
print("sqrt(b/a) =", t0, " loglog 27 =", math.log(math.log(27)))
ts = [t0 + 0.1*k for k in range(1, 30)]
dec1 = all(f1(ts[i+1]) < f1(ts[i]) for i in range(len(ts)-1))
inc2 = all(f2(ts[i+1]) > f2(ts[i]) for i in range(len(ts)-1))
print("a+b/t decreasing:", dec1, " at+b/t increasing:", inc2)
sys.exit(0 if dec1 and inc2 and math.log(math.log(27)) >= t0 else 1)
