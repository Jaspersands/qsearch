"""Existence of an admissible chain (threshold-7 Definition 2.1) at a prime p, by exhaustive search
over the finite graph of nodes (D, K), D | kappa, 0 in K subset Z_D.  An edge (D, K) -> (D', K'),
D | D', exists iff RC(D'; pi^{-1}(K) -> K') is feasible (complete DFS of rcdfs.c, witnesses
re-checked with pow).  Taking R_t = pi^{-1}(K_{t-1}) is no loss: fewer rows are easier.
Best-first on |K| with domination pruning: a reached (D, K0) dominates (D, K) for K0 subset K.
Usage: reach.py kappa p1 p2 ...   or   reach.py kappa E2   (all primes of E_2(kappa) for kappa<=7)
"""
import sys, itertools, heapq
from rc import feasible, is_prime

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]

def reach(kap, p):
    cache = {}
    def edge(D, K, D2, K2):
        rows = sorted(x for x in range(D2) if (x % D) in K)
        key = (D2, tuple(rows), K2)
        if key not in cache:
            st, a, b, n = feasible(p, D2, rows, list(K2))
            assert st in (0, 1)
            cache[key] = st
        return cache[key]
    nodes = {}
    for D in divisors(kap):
        if D == 1: continue
        nodes[D] = [tuple(sorted({0} | set(s))) for r in range(D) for s in itertools.combinations(range(1, D), r)]
    start = (1, (0,))
    reached = {start: None}
    heap = [(1, 1, (0,))]
    def dominated(D, K):
        return any(D0 == D and set(K0) <= set(K) and K0 != K for (D0, K0) in reached)
    while heap:
        _, D, K = heapq.heappop(heap)
        if dominated(D, K): continue
        for D2 in divisors(kap):
            if D2 == 1 or D2 % D: continue
            for K2 in sorted(nodes[D2], key=len):
                if (D2, K2) in reached or dominated(D2, K2): continue
                if edge(D, K, D2, K2):
                    reached[(D2, K2)] = (D, K)
                    if (D2, K2) == (kap, (0,)):
                        path, x = [], (kap, (0,))
                        while x is not None: path.append(x); x = reached[x]
                        return True, path[::-1], len(cache)
                    heapq.heappush(heap, (len(K2), D2, K2))
    return False, None, len(cache)

if __name__ == "__main__":
    kap = int(sys.argv[1])
    if sys.argv[2] == 'E2':
        from e2lists import E2
        ps = E2[kap]
    else:
        ps = [int(x) for x in sys.argv[2:]]
    for p in ps:
        assert is_prime(p) and p % kap == 1
        ok, path, ncalls = reach(kap, p)
        print("kappa=%d p=%d chain exists: %s  (edge tests %d)  %s" % (kap, p, ok, ncalls,
              " -> ".join("(%d,%s)" % (D, set(K)) for D, K in path) if ok else ""), flush=True)
