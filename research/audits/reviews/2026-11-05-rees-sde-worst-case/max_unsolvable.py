"""Exact N(kappa, a, p) for a = 1, 2: the maximal length of a column sequence in F_p^a with
NO nonzero x in (P u {0})^M with sum x_i lam_i = 0.  Chevalley-Warning: N <= kappa*a.
Lower bound 2a: (e_j, -u e_j) with -u not in P.
a = 2 search: WLOG the bank contains e1 and e2 (rank 1 banks are a = 1 instances; GL_2 is
transitive on ordered bases), columns are taken up to scaling by P (which preserves
solvability), the rest in nondecreasing class order; DFS keeps only unsolvable prefixes
(supersets of solvable banks are solvable).  Usage: max_unsolvable.py kappa p"""
import sys


def run(k, p):
    P = sorted({pow(y, k, p) for y in range(1, p)})
    # a = 1
    def solv1(cs):
        R1 = set()
        for c in cs:
            new = {(w * c) % p for w in P} | {(r + w * c) % p for r in R1 for w in P}
            R1 |= new
            if 0 in R1:
                return True
        return False
    import itertools
    reps1 = []
    seen = set()
    for y in range(1, p):
        if y in seen:
            continue
        reps1.append(y)
        seen |= {(y * w) % p for w in P}
    N1 = 0
    for n in range(1, k + 2):
        if any(not solv1(cs) for cs in itertools.combinations_with_replacement(reps1, n)):
            N1 = n
    # a = 2
    reps, seen = [], set()
    for x in range(p):
        for y in range(p):
            if (x, y) == (0, 0) or (x, y) in seen:
                continue
            reps.append((x, y))
            seen |= {((w * x) % p, (w * y) % p) for w in P}

    def add(R1, v):
        out = set(R1)
        for w in P:
            a0, a1 = (w * v[0]) % p, (w * v[1]) % p
            out.add((a0, a1))
            for (r0, r1) in R1:
                out.add(((r0 + a0) % p, (r1 + a1) % p))
        return out

    base = add(add(set(), (1, 0)), (0, 1))
    best = [2, None]
    count = [0]

    def dfs(R1, start, chosen):
        L = 2 + len(chosen)
        if L > best[0]:
            best[0], best[1] = L, list(chosen)
        if L >= k * 2:          # CW: length kappa*a + 1 is always solvable
            return
        for j in range(start, len(reps)):
            R = add(R1, reps[j])
            count[0] += 1
            if (0, 0) not in R:
                dfs(R, j, chosen + [reps[j]])

    if (0, 0) not in base:
        dfs(base, 0, [])
    return N1, best[0], best[1], count[0]


k, p = int(sys.argv[1]), int(sys.argv[2])
N1, N2, ex, nodes = run(k, p)
print("kappa=%d p=%d  N(a=1)=%d  N(a=2)=%d  CW bound a=2: %d  example (with e1,e2): %s  nodes=%d"
      % (k, p, N1, N2, 2 * k, ex, nodes), flush=True)
