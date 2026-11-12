"""Check of [H, Eq (9.94)] (eq:kokord, bound for int eta_+^2 log xt).

Claim: the printed derivation does not give the O* constants of (9.94): the
expansion carries 2*int (eta_+ - eta_o) eta_o log xt but only one copy of its
bound is used, and rounding the main-term constant -0.021094778698867 to
-0.021095 costs 2.21e-7, which is not budgeted; even with one copy the
constant term needs 7.41e-7 > 5.3e-7 on the stated range x >= 10^12.

Book inputs:
  - optcoor.tex:70-74   eta_o(t) = t^3 (2-t)^3 e^{-(t-1)^2/2} on [0,2].
  - expform.tex:2282    x >= 10^12; H = 200.
  - expform.tex:2301-2303  expansion with the factor 2 on the cross term.
  - expform.tex:2306-2308  main term (0.64020599736635) log x - 0.021094778698867.
  - expform.tex:2312-2318  one cross copy <= 274.86/H^{7/2} (0.80013 log x + 0.214).
  - expform.tex:2322-2325  square term <= (274.86/H^{7/2})^2 log x + 27428/H^7.
  - expform.tex:2327-2331  conclusion (0.640206 + O*(1.95e-6)) log x - 0.021095 + O*(5.3e-7).
  - normsapp.tex:290-293   |eta_+ - eta_o|_2 <= 274.856893/H^{7/2}.

Recomputes the eta_o integrals (to check the book's main-term values and the
norms 0.80013, 0.214), then sums the book's own error terms with one and with
two cross copies plus the rounding of the main term, and finds the least
log x at which the printed form a log x + b (a = 1.95e-6, b = 5.3e-7) holds.
Confirms if, with one copy, that least log x exceeds log 10^12 (so the
derivation fails on the book's range) and with two copies the log x
coefficient alone exceeds 1.95e-6.  This concerns the derivation only; it does
not claim (9.94) is false.

Run: PYTHONPATH=<mpmath dir> python3 -s eq_9_94.py

Ported from a 2026-11-06 check script.
"""
import mpmath as mp

mp.mp.dps = 30

eo2 = lambda t: (t ** 3 * (2 - t) ** 3) ** 2 * mp.exp(-(t - 1) ** 2)
A0 = mp.quad(eo2, [0, 1, 2])
B0 = mp.quad(lambda t: eo2(t) * mp.log(t), [0, 1, 2])
N2 = mp.quad(lambda t: eo2(t) * mp.log(t) ** 2, [0, 1, 2])
print("int eta_o^2         = %s  (book 0.64020599736635)" % mp.nstr(A0, 18))
print("int eta_o^2 log t   = %s  (book -0.021094778698867)" % mp.nstr(B0, 18))
print("|eta_o|_2           = %s  (book <= 0.80013)" % mp.nstr(mp.sqrt(A0), 12))
print("|eta_o log|_2       = %s  (book <= 0.214)" % mp.nstr(mp.sqrt(N2), 12))
main_ok = abs(A0 - mp.mpf("0.64020599736635")) < 1e-14 and abs(B0 - mp.mpf("-0.021094778698867")) < 1e-15

H = mp.mpf(200)
e = mp.mpf("274.86") / H ** mp.mpf(3.5)
cross_l, cross_c = e * mp.mpf("0.80013"), e * mp.mpf("0.214")
sq_l, sq_c = e ** 2, mp.mpf(27428) / H ** 7
rnd_l = abs(mp.mpf("0.640206") - mp.mpf("0.64020599736635")) + mp.mpf("1e-14")
rnd_c = abs(mp.mpf("-0.021094778698867") - mp.mpf("-0.021095")) + mp.mpf("1e-15")
print("one cross copy  : %s log x + %s" % (mp.nstr(cross_l, 6), mp.nstr(cross_c, 6)))
print("square term     : %s log x + %s" % (mp.nstr(sq_l, 6), mp.nstr(sq_c, 6)))
print("main-term rounding: %s log x + %s" % (mp.nstr(rnd_l, 6), mp.nstr(rnd_c, 6)))

a, b = mp.mpf("1.95e-6"), mp.mpf("5.3e-7")
L12 = mp.log(mp.mpf(10) ** 12)
need = {}
for k in (1, 2):
    tl = k * cross_l + sq_l + rnd_l
    tc = k * cross_c + sq_c + rnd_c
    print("%d cop%s: total %s log x + %s   (printed 1.95e-6 log x + 5.3e-7)"
          % (k, "y " if k == 1 else "ies", mp.nstr(tl, 6), mp.nstr(tc, 6)))
    if tl >= a:
        need[k] = mp.inf
        print("   log x coefficient alone exceeds 1.95e-6")
    else:
        need[k] = max(mp.mpf(0), (tc - b) / (a - tl))
        print("   holds only for log x >= %s (x >= %s); log 10^12 = %s"
              % (mp.nstr(need[k], 6), mp.nstr(mp.exp(need[k]), 4), mp.nstr(L12, 6)))

if main_ok and need[1] > L12 and need[2] == mp.inf:
    print("CONFIRMED: the book's own error terms give %s log x + %s with one cross copy (valid only for log x >= %s > log 10^12) and a log x coefficient %s > 1.95e-6 with the two copies the expansion requires, so the printed O* constants of (9.94) do not follow from its derivation."
          % (mp.nstr(cross_l + sq_l + rnd_l, 5), mp.nstr(cross_c + sq_c + rnd_c, 4), mp.nstr(need[1], 4), mp.nstr(2 * cross_l + sq_l + rnd_l, 4)))
else:
    print("NOT CONFIRMED: the book's error terms fit the printed O* constants of (9.94) on x >= 10^12 (or the main-term values differ).")
