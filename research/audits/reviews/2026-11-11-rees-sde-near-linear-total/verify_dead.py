"""Independent brute-force check of a claimed dead bank: enumerate all x in P0^n (no kernel code).
Usage: /opt/anaconda3/bin/python -I verify_dead.py p kappa '<cols as python list>'"""
import ast, itertools, sys
p, kap = int(sys.argv[1]), int(sys.argv[2])
cols = ast.literal_eval(sys.argv[3])
d, n = len(cols[0]), len(cols)
P0 = sorted({pow(y, kap, p) for y in range(p)})
# rank by brute Gaussian elimination
M = [list(c) for c in cols]
r = 0
A = [[cols[j][i] % p for j in range(n)] for i in range(d)]
for c in range(n):
    piv = next((i for i in range(r, d) if A[i][c]), None)
    if piv is None: continue
    A[r], A[piv] = A[piv], A[r]
    inv = pow(A[r][c], p - 2, p)
    A[r] = [x * inv % p for x in A[r]]
    for i in range(d):
        if i != r and A[i][c]:
            f = A[i][c]; A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
    r += 1
nsol = 0
for x in itertools.product(P0, repeat=n):
    if any(x) and all(sum(x[j] * cols[j][i] for j in range(n)) % p == 0 for i in range(d)):
        nsol += 1
print(f"p={p} kappa={kap} d={d} n={n} rank={r} |P0|={len(P0)} nonzero_solutions={nsol}")
