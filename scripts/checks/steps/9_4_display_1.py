# Lemma 9.1.3 / 9.4.1: for complex chi the zeros of L(s,chi) are not symmetric under gamma -> -gamma,
# so N^+(T,chi) = N(T,chi)/2 and "sum_{|Im rho|>T0} = sum_{Im rho>T0} (|G(rho)|+|G(1-rho)|)" fail.
from mpmath import mp, mpf, mpc, dirichlet, findroot, re, im
import sys
mp.dps = 20
chi = [0, 1, 1j, -1j, -1]          # chi mod 5 with chi(2) = i (complex, primitive)
L = lambda s: dirichlet(s, chi)
def first_zero(sign):
    ts = [sign*mpf(k)/10 for k in range(1, 200)]
    vals = [abs(L(mpf(1)/2 + 1j*t)) for t in ts]
    for i in range(1, len(ts)-1):
        if vals[i] < vals[i-1] and vals[i] < vals[i+1] and vals[i] < 0.3:
            return findroot(L, mpc(0.5, ts[i]))
z_pos, z_neg = first_zero(1), first_zero(-1)
print("lowest zero with gamma>0:", z_pos, " lowest with gamma<0:", z_neg)
T = (im(z_pos) + abs(im(z_neg)))/2
print("at T =", T, ": N^+(T) and N^-(T) differ (one is 0, the other >= 1)")
sys.exit(0 if abs(im(z_pos) + im(z_neg)) > 0.1 else 1)
