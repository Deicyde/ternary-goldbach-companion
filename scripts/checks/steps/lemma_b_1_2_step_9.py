# Lemma B.1.2: is 31.52065 the max of |4g+fhat| (claim: yes) rather than of |fhat|?
import cmath, math, sys
def e(x): return cmath.exp(2j*math.pi*x)
def g(t): return 4*e(-t/4)-4*e(-t/2)+e(-t)
def simpson(fn,a,b,n):
    h=(b-a)/n; s=fn(a)+fn(b)
    for k in range(1,n): s+=(4 if k%2 else 2)*fn(a+k*h)
    return s*h/3
def fhat(t):
    n=400+40*int(abs(t))
    return simpson(lambda x:-4/x**2*e(-x*t),0.25,0.5,n)+simpson(lambda x:4/x**2*e(-x*t),0.5,1.0,n)
best=(0,0); bestf=(0,0)
t=0.0
while t<=60:
    F=fhat(t); v=abs(4*g(t)+F)
    if v>best[0]: best=(v,t)
    if abs(F)>bestf[0]: bestf=(abs(F),t)
    t+=0.01
# refine
a=best[1]
for step in (1e-3,1e-4,1e-5):
    cands=[a+k*step for k in range(-20,21)]
    a=max(cands,key=lambda s:abs(4*g(s)+fhat(s)))
print("max |4g+fhat| on [0,60] ~ %.6f at t=%.5f"%(abs(4*g(a)+fhat(a)),a))
print("max |fhat| on [0,60] ~ %.6f at t=%.2f (and |fhat|<=80/(pi t) beyond)"%bestf)
ok = abs(abs(4*g(a)+fhat(a))-31.52065)<1e-3 and bestf[0]<31
sys.exit(0 if ok else 1)
