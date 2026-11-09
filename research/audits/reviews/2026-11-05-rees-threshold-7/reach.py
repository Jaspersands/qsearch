"""Reachability over ALL union chains at modulus kappa (report Section 4.4).

Nodes: class sets K subset Z_kappa with 0 in K.  Edge R -> K (R != K) iff an RC(kappa; R -> K)
contraction exists (complete DFS of rectu.c, ALLOWDUP=1 unless K = {0}; witnesses re-checked).
A union chain of any length exists iff {0} is reachable from Z_kappa.  Monotonicity used to prune:
if R -> K is feasible then R' -> K' is feasible for R' subset R, K' superset K (restrict rows /
enlarge target), so we only query edges not already implied.
Usage: python reach.py kappa p [p ...]
"""
import sys, itertools
from union_exact import decide

def subsets_with0(kappa):
    out = []
    for r in range(0, kappa):
        for rest in itertools.combinations(range(1, kappa), r):
            out.append(frozenset((0,) + rest))
    return out

def reach(kappa, p):
    nodes = subsets_with0(kappa)
    full = frozenset(range(kappa)); zero = frozenset([0])
    feas, infeas = [], []   # known feasible (R,K) and infeasible (R,K)
    calls = 0
    def edge(R, K):
        nonlocal calls
        for (R2, K2) in feas:
            if R <= R2 and K >= K2: return True
        for (R2, K2) in infeas:
            if R >= R2 and K <= K2: return False
        calls += 1
        ok = decide(p, kappa, sorted(R), sorted(K))
        (feas if ok else infeas).append((R, K))
        return ok
    seen = {full}; frontier = [full]; parent = {full: None}
    while frontier:
        R = frontier.pop()
        for K in sorted(nodes, key=len):
            if K == R or K in seen: continue
            if edge(R, K):
                seen.add(K); frontier.append(K); parent[K] = R
    path = []
    if zero in seen:
        x = zero
        while x is not None: path.append(tuple(sorted(x))); x = parent[x]
        path.reverse()
    return zero in seen, sorted((tuple(sorted(s)) for s in seen), key=len), calls, path

if __name__ == "__main__" and sys.argv[1] != "general":
    kappa = int(sys.argv[1])
    for p in map(int, sys.argv[2:]):
        ok, seen, calls, path = reach(kappa, p)
        small = [s for s in seen if len(s) <= 2]
        print("kappa=%d p=%d: {0} reachable from Z_kappa: %s; reachable sets of size <= 2: %s; DFS calls %d; a chain: %s" % (
            kappa, p, ok, small, calls, path), flush=True)

# ---------------------------------------------------------------------------------------------
# General admissible chains (report Definition 2.1): nodes (D, K), D | kappa, 0 in K subset Z_D,
# start (1, {0}); an edge (D, K) -> (D', K') with D | D' needs RC(D'; pi^{-1}(K) -> K'),
# pi: Z_D' -> Z_D.  Goal (kappa, {0}).
def divisors(n): return [d for d in range(1, n+1) if n % d == 0]

def reach_general(kappa, p):
    nodes = [(D, S) for D in divisors(kappa) if D > 1 for S in subsets_with0(D)]
    known = {}   # D' -> (feas list, infeas list)
    calls = 0
    def edge(Dp, R, K):
        nonlocal calls
        fe, inf = known.setdefault(Dp, ([], []))
        for (R2, K2) in fe:
            if R <= R2 and K >= K2: return True
        for (R2, K2) in inf:
            if R >= R2 and K <= K2: return False
        calls += 1
        ok = decide(p, Dp, sorted(R), sorted(K))
        (fe if ok else inf).append((R, K))
        return ok
    start = (1, frozenset([0])); goal = (kappa, frozenset([0]))
    seen = {start}; parent = {start: None}; frontier = [start]
    while frontier:
        D, K = frontier.pop()
        for (Dp, Kp) in sorted(nodes, key=lambda n: (-n[0], len(n[1]))):
            if Dp % D or (Dp, Kp) in seen: continue
            R = frozenset(x for x in range(Dp) if (x % D) in K)
            if R == Kp: continue
            if edge(Dp, R, Kp):
                seen.add((Dp, Kp)); parent[(Dp, Kp)] = (D, K); frontier.append((Dp, Kp))
        if goal in seen: break
    path = []
    if goal in seen:
        x = goal
        while x is not None: path.append((x[0], tuple(sorted(x[1])))); x = parent[x]
        path.reverse()
    return goal in seen, path, calls

if __name__ == "__main__" and sys.argv[1] == "general":
    kappa = int(sys.argv[2])
    for p in map(int, sys.argv[3:]):
        ok, path, calls = reach_general(kappa, p)
        print("kappa=%d p=%d: some admissible chain exists: %s; DFS calls %d; chain (D, K): %s" % (kappa, p, ok, calls, path), flush=True)
