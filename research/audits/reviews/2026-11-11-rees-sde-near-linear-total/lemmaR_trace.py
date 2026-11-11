"""Trace Lemma R's case analysis on a dead (2d+1)-bank to locate which lower-dimensional
hypothesis fails (consistency check of Lemma R). Usage: python -I lemmaR_trace.py p kappa '<cols>'"""
import ast, itertools, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdecore import coset_table, rank_mod, is_dead
p, kap = int(sys.argv[1]), int(sys.argv[2])
cols = ast.literal_eval(sys.argv[3]); n, d = len(cols), len(cols[0])
g, cos = coset_table(p, kap)
# dead triples in F_p^1
dead3 = [(a, b) for a in range(1, p) for b in range(a, p) if is_dead([[1], [a], [b]], p, cos)]
print("kappa", kap, "p", p, "-1 in P:", cos[p-1] == 0, " #dead triples (1,a,b) in F_p:", len(dead3), dead3[:5])
for r in range(1, n):
    for T in itertools.combinations(range(n), r):
        rk = rank_mod([cols[i] for i in T], p)
        if 1 <= rk < d and len(T) == 2 * rk:
            full = [i for i in range(n) if rank_mod([cols[j] for j in T] + [cols[i]], p) == rk]
            if len(full) != len(T):
                continue
            print("tight flat cols", T, "rank", rk, " D dead:", is_dead([cols[i] for i in T], p, cos))
