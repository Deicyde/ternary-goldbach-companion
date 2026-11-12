# Lemma 4.2.1: D<=(Q+1)/2 => M=min(Q/2,D) >= floor(D)? Q integer.
import sys, math
cex=[]
for Q in range(1,40):
    for k in range(1,200):
        D=k/4
        if D<=(Q+1)/2 and min(Q/2,D)<math.floor(D): cex.append((Q,D))
print("counterexamples (Q,D):",cex[:6])
print("all have D==(Q+1)/2 with Q odd:",all(D==(Q+1)/2 and Q%2 for Q,D in cex))
sys.exit(0 if cex else 1)
