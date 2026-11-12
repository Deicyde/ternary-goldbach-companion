"""Check of [H, (9.54)] (proof of Lemma 9.3.1, Gaussian part of the zero sum).

Claim: the final '<= 1.578 T0 log(qT0/2pi)' of (9.54) needs
2.566(1 + 1/log(T0/(pi|delta|)))|delta|/T0 <= 0.091, which holds for
T0 >= 4 pi^2 |delta| (the 2013 hypothesis still cited after (9.54)) but not
under the lemma's hypothesis T0 >= max(10 pi |delta|, 50).  Counterexample:
q = 1, |delta| = 5, T0 = 50 pi.  Harmless downstream (Sec. 9.6 has
T0/|delta| >= 83).

Book inputs (expform.tex):
  - l.1044-1050  Lemma 9.3.1: hypothesis T0 >= max(10 pi |delta|, 50); bound
    1.578 e^{-0.1065 T0^2/(pi delta)^2} for the Gaussian part.
  - l.1081-1091  (9.48): Gaussian part (kappa_{2,0}/4)(T/(pi delta))^2
    e^{-0.1065 (T/(pi delta))^2} for |T| < (3/2)(pi delta)^2, kappa_{2,0} = 7.96.
  - l.1098-1103  (9.49): weight (1/2pi) log(qT/2pi) + 1/(4T).
  - l.1171-1175  |delta| > 20/(3 pi) when the Gaussian term is present.
  - l.1228-1236  (9.54): first line
    (1.487 T0 + 2.194|delta|) log(q|delta|/2) + 1.487 T0 log(T0/(pi|delta|))
    + 2.566|delta| log(e T0/(pi|delta|)), middle line
    (1.487 + 2.566(1 + 1/log(T0/pi|delta|))/(T0/|delta|)) T0 log(qT0/2pi),
    final line 1.578 T0 log(qT0/2pi).
  - l.1237-1238  "using several times the assumption that T0 >= 4 pi^2 |delta|".

Confirms if: at the admissible point q = 1, |delta| = 5, T0 = 50 pi (where the
Gaussian term is present) the first line of (9.54) exceeds
1.578 T0 log(qT0/2pi), the middle coefficient exceeds 1.578 at
T0/|delta| = 10 pi but not at 4 pi^2, and the exact integral (9.53) (with
log(qT/2pi), as in (9.49)) also exceeds 1.578 there.

Run: python3 -I eq_9_54.py

Ported from a 2026-11-06 check script.
"""
import math

PI = math.pi
c = 0.1065
k20 = 7.96


def first_line(q, d, T0):
    return ((1.487 * T0 + 2.194 * d) * math.log(q * d / 2)
            + 1.487 * T0 * math.log(T0 / (PI * d))
            + 2.566 * d * math.log(math.e * T0 / (PI * d)))


def middle_coef(T0, d):
    u = T0 / d
    return 1.487 + 2.566 * (1 + 1 / math.log(T0 / (PI * d))) / u


def denom(q, T0):
    return T0 * math.log(q * T0 / (2 * PI))


def gl_nodes(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(PI * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


GLX, GLW = gl_nodes(30)


def integrate(fn, a, b, pieces):
    h = (b - a) / pieces
    s = 0.0
    for j in range(pieces):
        mid = a + (j + 0.5) * h
        for x, w in zip(GLX, GLW):
            s += w * fn(mid + h / 2 * x)
    return s * h / 2


def gauss_ratio(q, d, T0, pieces, cutoff=False):
    """Exact (9.53) with log(qT/2pi), divided by e^{-c y^2} T0 log(qT0/2pi)."""
    pd = PI * d
    y = T0 / pd

    def g(T):
        t = T / pd
        return (k20 / 4) * t * t * math.exp(-c * (t * t - y * y)) * (
            math.log(q * T / (2 * PI)) / (2 * PI) + 1 / (4 * T))
    U = 1.5 * pd * pd if cutoff else T0 + 30 * pd
    return integrate(g, T0, U, pieces) / denom(q, T0)


q, d, T0 = 1, 5.0, 50 * PI
print("Admissibility of q=1, |delta|=5, T0=50 pi:")
adm = T0 >= max(10 * PI * d, 50) - 1e-9 and d > 20 / (3 * PI) and T0 < 1.5 * (PI * d) ** 2
print(f"  T0 = {T0:.4f} >= max(10 pi|d|,50) = {max(10*PI*d,50):.4f}; |d| > 20/(3pi) = {20/(3*PI):.4f};"
      f" T0 < (3/2)(pi d)^2 = {1.5*(PI*d)**2:.2f}: {adm}")
t1 = (1.487 * T0 + 2.194 * d) * math.log(q * d / 2)
t2 = 1.487 * T0 * math.log(T0 / (PI * d))
t3 = 2.566 * d * math.log(math.e * T0 / (PI * d))
L1 = first_line(q, d, T0)
Lm = middle_coef(T0, d) * denom(q, T0)
Lf = 1.578 * denom(q, T0)
print(f"  first line = {t1:.4f} + {t2:.4f} + {t3:.4f} = {L1:.4f}")
print(f"  middle line = {Lm:.4f} (coefficient {middle_coef(T0, d):.6f})")
print(f"  final 1.578 T0 log(qT0/2pi) = {Lf:.4f}; first/(T0 log) = {L1/denom(q,T0):.6f}")
fail_first = L1 > Lf
print(f"  first <= middle: {L1 <= Lm}; middle <= final: {Lm <= Lf}; first <= final: {not fail_first}")

M10 = 1.487 + 2.566 * (1 + 1 / math.log(10)) / (10 * PI)
M4pi = 1.487 + 2.566 * (1 + 1 / math.log(4 * PI)) / (4 * PI * PI)
print(f"Middle coefficient: at T0/|d| = 10 pi: {M10:.6f}; at T0/|d| = 4 pi^2: {M4pi:.6f}")
lo, hi = 10.0, 4 * PI
for _ in range(100):
    m = (lo + hi) / 2
    if 1.487 + 2.566 * (1 + 1 / math.log(m)) / (PI * m) > 1.578:
        lo = m
    else:
        hi = m
print(f"  middle coefficient <= 1.578 iff T0/|d| >= {PI*hi:.4f} (4 pi^2 = {4*PI*PI:.4f}, 10 pi = {10*PI:.4f})")
M83 = 1.487 + 2.566 * (1 + 1 / math.log(1000 / (12 * PI))) / (1000 / 12)
print(f"  at Sec. 9.6's T0/(pi|d|) >= 1000/(12 pi): {M83:.6f}")

r_a = gauss_ratio(q, d, T0, 300)
r_b = gauss_ratio(q, d, T0, 600)
print(f"Exact (9.53) ratio at q=1,|d|=5,T0=50pi: {r_a:.7f} (300 panels), {r_b:.7f} (600 panels)")
print(f"  with cutoff at (3/2)(pi d)^2: {gauss_ratio(q, d, T0, 600, cutoff=True):.7f}")

ok = adm and fail_first and M10 > 1.578 and M4pi <= 1.578 and min(r_a, r_b) > 1.578 and M83 <= 1.578
if ok:
    print(f"CONFIRMED: at the admissible point q=1, |delta|=5, T0=50pi the first line of (9.54) is {L1/denom(q,T0):.4f} T0 log(qT0/2pi) and the exact integral {r_b:.4f}, both above 1.578, which needs T0 >= 39.35|delta| (true under 4pi^2|delta|, not 10pi|delta|).")
else:
    print("NOT CONFIRMED: the computation does not show (9.54) failing at an admissible point under T0 >= 10pi|delta|.")
