# Sec 6.3: (x/y)(2/3+0.1573) with y=x^(1/3)/6, coefficient of x^(2/3) log x
import sys
c=6*(2/3+0.1573); half=3*(2/3+0.1573)
print("x/y*(2/3+0.1573) coefficient =",c,"; with x/(2y):",half,"; printed 2.4719")
sys.exit(0 if c>2.4719 and abs(half-2.4719)<1e-3 else 1)
