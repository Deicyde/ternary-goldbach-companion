import math, sys
a = 0.5*math.exp(2*0.25068); b = 0.5*math.exp(-2*0.25068)
print("1/2 e^{+0.50136} =", a, " 1/2 e^{-0.50136} =", b)
sys.exit(0 if abs(b - 0.30285) < 1e-5 and abs(a - 0.30285) > 0.1 else 1)
