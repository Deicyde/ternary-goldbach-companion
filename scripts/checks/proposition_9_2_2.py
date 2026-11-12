"""Check of [H, Proposition 9.2.2] (Gaussian eta(t) = e^{-t^2/2}, proof).

Claim: the proof evaluates Lemma 9.1.1's factor |eta'|_2 + 2 pi |delta| |eta|_2
as 0.942 + 4.183|delta| <= 1 + 5|delta| with the two L^2 norms swapped; the
true value 0.6657 + 5.9150|delta| exceeds 1 + 5|delta| for |delta| > 0.3654, so
the x^{-3/2} term should be (log q + 6)(1 + 6|delta|).  The printed bound
still follows from slack in the x^{-1} term once sqrt x >= 8.50 + 1.401 log q;
Thm 7.1.1 (x >= 10^8) is unaffected.

Book inputs:
  - expform.tex:113-115  Lemma 9.1.1 error (log q + 6.01)(|eta'|_2 +
    2 pi |delta| |eta|_2) x^{-1/2}.
  - expform.tex:929-931  |eta|_2^2 = sqrt(pi)/2, |eta'|_2^2 = sqrt(pi)/4.
  - expform.tex:976-980  err: (3 log q + 14|delta| + 17) x^{-1} +
    (log q + 6)(1 + 5|delta|) x^{-3/2}.
  - expform.tex:1007-1014  |R| <= 3 log q + 13.347|delta| + 16.695;
    "|eta'|_2 + 2 pi |delta| |eta|_2 <= 0.942 + 4.183|delta| <= 1 + 5|delta|";
    (6.01-6)(1+5|delta|) + 13.347|delta| + 16.695 < 14|delta| + 17.

Confirms if 0.942 and 4.183 match |eta|_2 and 2 pi |eta'|_2 (swapped), the
true factor exceeds 1 + 5|delta| at some delta, 1 + 6|delta| closes the
proof's last inequality, and the x^{-1} slack absorbs the deficit for
sqrt x >= 8.50 + 1.401 log q.

Run: python3 -I proposition_9_2_2.py

Ported from a 2026-11-06 check script.
"""
import math

n2 = math.sqrt(math.sqrt(math.pi) / 2)    # |eta|_2
nd2 = math.sqrt(math.sqrt(math.pi) / 4)   # |eta'|_2
print("|eta|_2 = %.7f   |eta'|_2 = %.7f" % (n2, nd2))
print("2pi|eta|_2 = %.7f   2pi|eta'|_2 = %.7f" % (2 * math.pi * n2, 2 * math.pi * nd2))
print("printed: 0.942 + 4.183|d|; correct |eta'|_2 + 2pi|d||eta|_2 = %.6f + %.6f|d|" % (nd2, 2 * math.pi * n2))
swapped = abs(0.942 - n2) < 1e-3 and abs(4.183 - 2 * math.pi * nd2) < 1e-3
d_cross = (1 - nd2) / (2 * math.pi * n2 - 5)
print("true factor > 1+5|d| for |d| > %.4f; at |d|=1: %.4f > 6" % (d_cross, nd2 + 2 * math.pi * n2))
fails = nd2 + 2 * math.pi * n2 > 6
fix_factor = nd2 <= 1 and 2 * math.pi * n2 <= 6
lhs_fix = lambda d: 0.01 * (1 + 6 * d) + 13.347 * d + 16.695
fix_closes = all(lhs_fix(d) < 14 * d + 17 for d in [k / 10 for k in range(0, 10001)])
print("with (1+6|d|): factor bounded:", fix_factor, "; 0.01(1+6|d|)+13.347|d|+16.695 < 14|d|+17 on [0,1000]:", fix_closes)

# printed form via x^{-1} slack: need deficit * x^{-3/2} <= slack * x^{-1}
def thresh(logq):
    best = 0.0
    for k in range(1, 200001):
        d = k / 1000.0
        defi = (logq + 6.01) * (nd2 + 2 * math.pi * n2 * d) - (logq + 6) * (1 + 5 * d)
        slack = 0.653 * d + 0.305
        best = max(best, defi / slack)
    lim = ((logq + 6.01) * 2 * math.pi * n2 - 5 * (logq + 6)) / 0.653
    return max(best, lim)
ok_thr = True
for q in (3, 3 * 10**5):
    L = math.log(q)
    t = thresh(L)
    print("q=%-7d sqrt(x) threshold = %.4f  (8.50 + 1.401 log q = %.4f)  x >= %.1f" % (q, t, 8.50 + 1.401 * L, t * t))
    ok_thr &= abs(t - (8.4976 + 1.40117 * L)) < 0.01
print("Thm 7.1.1 range x >= 1e8 lies above the threshold:", thresh(math.log(3e5)) ** 2 < 1e8)
if swapped and fails and fix_factor and fix_closes and ok_thr:
    print("CONFIRMED: the proof of Prop 9.2.2 uses 0.942 + 4.183|delta| = |eta|_2 + 2pi|eta'|_2|delta| (norms swapped); the true 0.6657 + 5.9150|delta| exceeds 1 + 5|delta| for |delta| > 0.3654, and (1 + 6|delta|) or the x^{-1} slack repairs the proof.")
else:
    print("NOT CONFIRMED: the norms in the proof of Prop 9.2.2 are not swapped as claimed, or the repair fails.")
