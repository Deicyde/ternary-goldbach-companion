# Lemma 5.2.2: sigma=e^{-2*0.25068}/2; 3 sigma/(1-sigma/3.5) < 1; identity (3r/(2(1-s/3.5)R))*2s*W/2 = (W/2)(3s/(1-s/3.5))(r/R)
import math, random
s=math.exp(-2*0.25068)/2; k=3*s/(1-s/3.5); print("sigma=%.6f factor=%.6f"%(s,k))
ok=True
for _ in range(100):
    W=random.uniform(1e4,1e6); r=random.uniform(1,50); R=random.uniform(r,100)
    lhs=3*r/(2*(1-s/3.5)*R)*2*s*W/2; rhsR=W/2*k*r/R; rhsW=W/2*k*r*W/R
    ok &= abs(lhs-rhsR)<1e-9*lhs and abs(lhs-rhsW)>1e-3*lhs
raise SystemExit(0 if ok and k<1 else 1)
