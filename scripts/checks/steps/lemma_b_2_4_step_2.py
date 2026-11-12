# Lemma B.2.4: f = log(t)*eta2(t), eta2 = 4log(4t) on [1/4,1/2], 4log(1/t) on [1/2,1].
from mpmath import mp, mpf, log, diff, quad
import sys
mp.dps = 30
def f(t):
    if mpf(1)/4 <= t <= mpf(1)/2: return 4*log(t)*log(4*t)
    if mpf(1)/2 <= t <= 1: return -4*log(t)**2
    return mpf(0)
def fp(t):
    if mpf(1)/4 < t < mpf(1)/2: return 4*log(4*t*t)/t
    if mpf(1)/2 < t < 1: return -8*log(t)/t
    return mpf(0)
pts1 = [mpf(1)/4 + k*mpf(1)/400 for k in range(1, 100)]
pts2 = [mpf(1)/2 + k*mpf(1)/200 for k in range(1, 100)]
f_neg_dec_1 = all(f(t) < 0 for t in pts1) and all(f(pts1[i+1]) < f(pts1[i]) for i in range(98))
f_neg_inc_2 = all(f(t) < 0 for t in pts2) and all(f(pts2[i+1]) > f(pts2[i]) for i in range(98))
print("f negative & decreasing on (1/4,1/2):", f_neg_dec_1, "; f negative & increasing on (1/2,1):", f_neg_inc_2)
fp_ok = all(fp(t) < 0 for t in pts1) and all(fp(pts1[i+1]) > fp(pts1[i]) for i in range(98)) \
    and all(fp(t) > 0 for t in pts2) and all(fp(pts2[i+1]) < fp(pts2[i]) for i in range(98))
print("f' negative increasing on (1/4,1/2), positive decreasing on (1/2,1):", fp_ok)
a, b = fp(mpf(1)/4 + mpf(10)**-25), fp(mpf(1)/2 + mpf(10)**-25)
print("f'(1/4+) / log2 =", a/log(2), " f'(1/2+) / log2 =", b/log(2))
# total variation of f' (= |f''|_1 as a measure, jumps included)
TV = abs(a) + quad(lambda t: abs(diff(fp, t)), [mpf(1)/4, mpf(1)/2]) + abs(b - fp(mpf(1)/2 - mpf(10)**-25)) \
     + quad(lambda t: abs(diff(fp, t)), [mpf(1)/2, 1])
print("|f''|_1 / log 2 =", TV/log(2), "(f'' has point masses at 1/4, 1/2, so |f''|_inf is infinite)")
sys.exit(0 if f_neg_dec_1 and f_neg_inc_2 and fp_ok and abs(TV/log(2) - 96) < 1e-6 else 1)
