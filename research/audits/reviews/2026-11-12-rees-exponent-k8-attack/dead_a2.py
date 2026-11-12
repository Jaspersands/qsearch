#!/opt/anaconda3/bin/python
"""Largest dead bank in F_41^2 for (P_8 u 0)-weights (exact DFS, finite; NODE cap reported).
Dead = no nonzero x in (P_8 u 0)^n with sum x_i lambda_i = 0.  Columns up to P_8-scaling (336 classes);
WLOG the bank contains e1 (GL_2 is transitive on nonzero vectors and preserves deadness), class index 0.
Multisets enumerated as non-decreasing class sequences starting with class 0."""
import numpy as np, sys, time
p, k = 41, 8
P = sorted({pow(x, k, p) for x in range(1, p)})
reps, seen = [], set()
def canon(v):
    return min(((q * v[0]) % p, (q * v[1]) % p) for q in P)
order = [(1, 0)] + [(x, y) for x in range(p) for y in range(p) if (x, y) not in ((0, 0), (1, 0))]
for v in order:
    c = canon(v)
    if c not in seen:
        seen.add(c); reps.append(v)
assert len(reps) == 336 and canon(reps[0]) == canon((1, 0))
CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
nodes = [0]; best = [0, None]; t0 = time.time()
cnt_by_size = {}
def shifts(A, v):
    out = np.zeros_like(A)
    for q in P:
        out |= np.roll(A, ((q * v[0]) % p, (q * v[1]) % p), axis=(0, 1))
    return out
def dfs(start, A, Zn, bank):
    nodes[0] += 1
    if nodes[0] > CAP:
        raise RuntimeError('cap')
    n = len(bank)
    cnt_by_size[n] = cnt_by_size.get(n, 0) + 1
    if n > best[0]:
        best[0], best[1] = n, list(bank)
    for idx in range(start, 336):
        v = reps[idx]
        # dead after adding v iff -q v not in A for all q in P  (A = all sums incl. 0)
        if any(A[(-q * v[0]) % p, (-q * v[1]) % p] for q in P):
            continue
        S = shifts(A, v)
        dfs(idx, A | S, Zn | S, bank + [v])
A0 = np.zeros((p, p), dtype=bool); A0[0, 0] = True
try:
    dfs(0, A0, np.zeros((p, p), dtype=bool), [])
    status = 'COMPLETE'
except RuntimeError:
    status = 'CAPPED at %d nodes (lower bound only)' % CAP
print(status, 'nodes', nodes[0], 'time %.0fs' % (time.time() - t0))
print('max dead bank size containing e1:', best[0], 'example:', best[1])
print('dead banks visited by size:', dict(sorted(cnt_by_size.items())))
if status == 'COMPLETE':
    print('=> N(8,2,41) = %d' % (best[0] + 1))
