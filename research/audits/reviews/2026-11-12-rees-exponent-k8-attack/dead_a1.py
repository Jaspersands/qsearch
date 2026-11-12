#!/opt/anaconda3/bin/python
"""Exact N(8,1,41): the least n such that every n columns in F_41 have a nonzero (P_8 u 0)-weighted zero sum.
Columns matter only up to P_8-scaling, i.e. by their class in Z_8 (zero columns are never dead).
Exhaustive over class multisets (counts n_0..n_7, total <= 9); dead test by exact DP over F_41."""
import itertools
p, k, g = 41, 8, 6
P = sorted({pow(x, k, p) for x in range(1, p)})
z = [pow(g, m, p) for m in range(k)]
def dead(cols):
    A = {0}      # all sums (incl. trivial)
    Zn = set()   # nontrivial sums
    for c in cols:
        Pc = {y * c % p for y in P}
        Zn = Zn | {(a + q) % p for a in A for q in Pc}
        A = A | Zn
        if 0 in Zn:
            return False
    return True
best = {}
for n in range(1, 10):
    found = []
    for combo in itertools.combinations_with_replacement(range(k), n):
        if dead([z[m] for m in combo]):
            found.append(combo)
    print(f'n={n}: dead class multisets: {len(found)}', ('e.g. ' + str(found[:6])) if found else '')
    if not found:
        print(f'=> N(8,1,41) = {n}  (every {n} columns have a solution; max dead size {n-1})')
        break
