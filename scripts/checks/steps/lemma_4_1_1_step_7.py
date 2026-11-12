# typeI.tex 83: "x -> 1/sin(x)^2 is convex-up on (0,inf)" -- test midpoint convexity across pi.
# Exit 0 if convexity on (0,inf) fails (claim confirmed).
import math
f = lambda x: 1/math.sin(x)**2
a, b = 2.0, 4.0     # midpoint 3.0 (< pi); try also a pair straddling pi
for (a, b) in ((2.0, 4.0), (3.0, 3.3), (1.0, 5.0)):
    m = (a+b)/2
    print("f(%.2f)=%.4f, (f(%.2f)+f(%.2f))/2=%.4f, convex-midpoint holds: %s" % (m, f(m), a, b, (f(a)+f(b))/2, f(m) <= (f(a)+f(b))/2))
viol = f(3.15) > (f(3.0)+f(3.3))/2
print("violation at midpoint 3.15 of [3.0,3.3]:", viol)
raise SystemExit(0 if viol else 1)
