# Count transversal cliques (y_m in Q_m, m=1..k-1, all differences in Q_0), y_1 fixed (Q_0-scaling).
import sys
from common import setup
k = int(sys.argv[1])
for p in map(int, sys.argv[2:]):
    ind, g = setup(p, k)
    assert ind[p-1] == 0
    Q = [[x for x in range(1, p) if ind[x] == m] for m in range(k)]
    cnt = 0
    def rec(m, ys):
        global cnt
        if m == k: cnt += 1; return
        for y in Q[m]:
            if all(ind[(y - z) % p] == 0 for z in ys): rec(m + 1, ys + [y])
    rec(2, [Q[1][0]])
    print(f"k={k} p={p} transversal cliques (y_1 fixed) = {cnt}")
