"""N(kappa,a,p): largest bank in F_p^a (a = 1, 2) with no nonzero x in (P u {0})^M,
sum x_i lambda_i = 0 (rem:sde-worst-case(a)).  Exhaustive DFS.

a = 2 reduction: GL_2 acts; every bank either lies in a line (then it is a
1-dim bank, size <= N(kappa,1,p)) or, up to GL_2, contains e_1 and e_2.  Columns
matter only up to scaling by P.  Remaining columns: sorted multiset of P-classes.
Reach set R = {sum x_i lambda_i : x in (P u {0})^k} (contains 0).  Adding column
lam keeps the bank unsolvable iff lam != 0 and (-P*lam) cap R is empty.
"""
import sys, time
import numpy as np
import sympy

def powers(p, kappa):
    return sorted({pow(x, kappa, p) for x in range(1, p)})

def N1(p, kappa):
    P = powers(p, kappa)
    Po = [0] + P
    # classes of F_p^* modulo P
    seen, reps = set(), []
    for x in range(1, p):
        if x not in seen:
            reps.append(x)
            for q in P:
                seen.add(x * q % p)
    best = [0]
    def dfs(start, R, size):
        best[0] = max(best[0], size)
        for ci in range(start, len(reps)):
            lam = reps[ci]
            if any(R[(-q * lam) % p] for q in P):
                continue
            R2 = np.zeros(p, dtype=bool)
            for c in Po:
                R2 |= np.roll(R, c * lam % p)
            dfs(ci, R2, size + 1)
    R0 = np.zeros(p, dtype=bool); R0[0] = True
    dfs(0, R0, 0)
    return best[0]

def N2(p, kappa, cap=10**7):
    P = powers(p, kappa)
    Po = [0] + P
    seen, reps = set(), []
    for x in range(p):
        for y in range(p):
            if (x, y) == (0, 0) or (x, y) in seen:
                continue
            reps.append((x, y))
            for q in P:
                seen.add((x * q % p, y * q % p))
    negP = [[((-q * x) % p, (-q * y) % p) for q in P] for (x, y) in reps]
    def add(R, lam):
        R2 = np.zeros((p, p), dtype=bool)
        for c in Po:
            R2 |= np.roll(np.roll(R, c * lam[0] % p, axis=0), c * lam[1] % p, axis=1)
        return R2
    R = np.zeros((p, p), dtype=bool); R[0, 0] = True
    R = add(R, (1, 0))
    if any(R[(-q) % p, 0] for q in P) is True:
        pass
    # adding e_2 to {e_1}: need (-P e_2) cap R empty: R is on the x-axis only, fine
    R = add(R, (0, 1))
    best = [2, None]
    nodes = [0]
    def dfs(start, R, size, chosen):
        nodes[0] += 1
        if size > best[0]:
            best[0], best[1] = size, list(chosen)
        if nodes[0] > cap:
            return
        for ci in range(start, len(reps)):
            if any(R[a, b] for (a, b) in negP[ci]):
                continue
            dfs(ci, add(R, reps[ci]), size + 1, chosen + [reps[ci]])
    dfs(0, R, 2, [(1, 0), (0, 1)])
    return best[0], best[1], nodes[0]

def G2star(p, kappa):
    # least |Good| with two distinct offsets (classes may be equal)
    g = sympy.primitive_root(p)
    cos = [None] * p
    x = 1
    for e in range(p - 1):
        cos[x] = e % kappa; x = x * g % p
    A = [[y == 0 or cos[y] == (-c) % kappa for y in range(p)] for c in range(kappa)]
    best = None
    for c1 in range(kappa):
        for c2 in range(kappa):
            cnt = sum(1 for s in range(p) if A[c1][s] and A[c2][(s + 1) % p])
            best = cnt if best is None else min(best, cnt)
    return best

if __name__ == "__main__":
    t0 = time.time()
    for kappa, p in [(3, 7), (3, 13), (3, 19), (3, 31), (4, 17)]:
        n1 = N1(p, kappa)
        g2 = G2star(p, kappa)
        n2, wit, nodes = N2(p, kappa)
        n2 = max(n2, n1)
        print(f"kappa={kappa} p={p}: N(kappa,1,p)={n1}  G*_2(p)={g2}  N(kappa,2,p)={n2}  witness={wit}  nodes={nodes}  [{time.time()-t0:.1f}s]")
        sys.stdout.flush()
