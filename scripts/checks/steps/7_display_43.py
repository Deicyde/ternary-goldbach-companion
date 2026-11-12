# Check numerator 13.6164 vs log(150001)+c^+ with c^+=2.3912, and the resulting bound vs 8.805x.
from math import log, sqrt, e
euler = 0.5772156649015329
mpf = float
L1 = log(150001)
print("log 150001 =", L1)
print("log150001 + 2.3912 =", L1 + mpf('2.3912'))
print("log150001 + 1.698  =", L1 + mpf('1.698'), "(printed 13.6164)")
print("log 2 + 1.698 =", log(2) + mpf('1.698'))
def chain(num, lx):
    return num/(lx/2 + mpf('0.6294'))*(mpf('0.640209')*lx - mpf('0.021095')) - mpf('8.6297')
lx0 = log(mpf('4.9e26'))
for num in (mpf('13.6164'), L1 + mpf('2.3912')):
    sup = 2*num*mpf('0.640209') - mpf('8.6297')
    print("num", num, ": value at x=4.9e26:", chain(num, lx0), " sup (x->inf):", sup)
    for lx in (lx0, 100, 1000, 10**6):
        assert chain(num, lx) <= sup  # increasing in log x towards sup
sup_correct = 2*(L1 + mpf('2.3912'))*mpf('0.640209') - mpf('8.6297')
print("corrected roussel:", mpf('0.041061')*sup_correct)
sys_exit = 0 if sup_correct > mpf('8.805') else 1
raise SystemExit(sys_exit)
