"""Matroid profile of a bank: for each subset, rank; report max n_U - 2u over proper flats
(classifies: dense / tight / strictly sub-critical) and the coset classes of the columns.
Usage: /opt/anaconda3/bin/python -I analyze_bank.py p kappa '<cols>'"""
import ast, itertools, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdecore import rank_mod, coset_table
p, kap = int(sys.argv[1]), int(sys.argv[2])
cols = ast.literal_eval(sys.argv[3]); n, d = len(cols), len(cols[0])
flats = {}
for r in range(1, n + 1):
    for T in itertools.combinations(range(n), r):
        rk = rank_mod([cols[i] for i in T], p)
        if rk < d:
            # closure
            cl = tuple(i for i in range(n) if rank_mod([cols[j] for j in T] + [cols[i]], p) == rk)
            flats[cl] = rk
prof = {}
for F, rk in flats.items():
    prof.setdefault(rk, []).append(len(F))
for rk in sorted(prof):
    print(f"rank {rk}: max columns in a flat = {max(prof[rk])}, #flats with 2*rk cols = {sum(1 for c in prof[rk] if c >= 2*rk)}, with >=2rk-1: {sum(1 for c in prof[rk] if c >= 2*rk-1)}")
worst = max(len(F) - 2 * rk for F, rk in flats.items())
print("max over proper flats of (n_U - 2u):", worst, "->", "dense" if worst > 0 else "tight" if worst == 0 else "strictly sub-critical")
