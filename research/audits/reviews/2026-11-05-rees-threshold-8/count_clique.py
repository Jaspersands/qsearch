"""Count ALL transversal cliques (y_1 = g fixed by Q_0-scaling) at given (kappa, p).
Usage: python count_clique.py K p [p ...]   Prints count, normalised count, mu_P model."""
import sys, math
sys.setrecursionlimit(10000)
from clique import setup, masks, rot
def count(p, k):
    g, cls = setup(p, k)
    full = (1 << p) - 1
    C = masks(p, k, cls); Q0 = C[0]
    rem0 = {i: C[i] & rot(Q0, g, p, full) for i in range(2, k)}
    tot = 0
    def dfs(rem):
        nonlocal tot
        if not rem:
            tot += 1; return
        i = min(rem, key=lambda t: rem[t].bit_count())
        cand = rem[i]
        while cand:
            low = cand & -cand; y = low.bit_length() - 1; cand ^= low
            N = rot(Q0, y, p, full); new = {}
            for t, M in rem.items():
                if t == i: continue
                M2 = M & N
                if M2 == 0: break
                new[t] = M2
            else:
                dfs(new)
    dfs(rem0)
    return tot
k = int(sys.argv[1])
for p in map(int, sys.argv[2:]):
    c = count(p, k)
    mu = (k-2)*math.log(p) + (1 - k*(k-1)/2)*math.log(k)
    print(f"k={k} p={p} transversal_cliques(y1=g)={c} mu_P_model={math.exp(mu):.3g}", flush=True)
