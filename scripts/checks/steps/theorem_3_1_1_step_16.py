# Thm 3.1.1 constant: AM-GM constant term vs printed 0.49911
import math, sys
rho=3.397962; s=math.sqrt(rho)
printed=(math.log(2)/s+s/2*0.67506)/2
correct=math.log(2)/(2*s)+s/2*0.67506
print("printed formula (1/2)(log2/sqrt(rho)+sqrt(rho)/2*0.67506) =",printed)
print("correct log2/(2sqrt rho)+(sqrt rho/2)*0.67506 =",correct)
print("log coeff 1/(4sqrt rho)+sqrt(rho)*0.30214/2 =",1/(4*s)+s*0.30214/2)
sys.exit(0 if correct>0.49911+0.1 else 1)
