# Lemma 4.1.1: needed arcsin x + x sqrt(1-x^2) <= 2x with x = sqrt(C/A);
# A arcsin sqrt(C/A) + C sqrt(A/C - 1) = A(arcsin x + x sqrt(1-x^2)).
import math, sys
xs = [k/1000 for k in range(1, 1000)]
good = all(math.asin(x) + x*math.sqrt(1-x*x) <= 2*x + 1e-15 for x in xs)
printed = all(math.asin(x) + x*(1-x*x) <= 2*x + 1e-15 for x in xs)
idok = True
for A, C in [(10, 1), (5, 3), (100, 0.5)]:
    x = math.sqrt(C/A)
    l = A*math.asin(x) + C*math.sqrt(A/C - 1); r = A*(math.asin(x) + x*math.sqrt(1-x*x))
    idok &= abs(l - r) < 1e-9
    # printed substitution x=C/A does not give the needed form
    y = C/A
    print(A, C, "needed form", l, "<= 2sqrt(AC)", 2*math.sqrt(A*C), "; with x=C/A, A(asin y + y(1-y^2)) =", A*(math.asin(y)+y*(1-y*y)))
print("corrected inequality holds:", good, "; printed inequality (true but not what is needed):", printed, "; identity:", idok)
sys.exit(0 if good and idok else 1)
