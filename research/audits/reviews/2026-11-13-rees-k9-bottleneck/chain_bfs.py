#!/opt/anaconda3/bin/python
"""Shortest flexible-line chains (thm:app-s2-chain) to EVERY target (D, K) at kappa = 9 (finite exact search).

A chain of length L ending at (D_L, K_L) gives, by the induction in the proof of thm:app-s2-chain
(procedure P_L with U = 0, m = a), a law-free node of arity binom(a+L+1, L+1) (degree L+1) whose
nonzero weights have D_L-class in K_L, i.e. 9-class in lift(K_L) = {x in Z_9 : x mod D_L in K_L}.
Edges (D,K) -> (D2,K2), D | D2, D2 >= 2: RC(D2; lift_{D2}(K) -> K2) feasible (complete DFS, rcdfs.c copied
from 2026-11-05-rees-threshold-7-check; witnesses re-checked by pow in rc.check).
Output: for every K subset Z_9 with 0 in K, deg9[K] = least L+1 over chains whose final 9-class set is
contained in K (monotone closure); "None" = no chain of length <= LMAX.
Usage: chain_bfs.py LMAX p1 p2 ...
"""
import sys, itertools, json
from rc import feasible

KAP = 9
DIVS = [3, 9]
LIMIT = 10**9


def subsets(D):
    return [tuple(sorted({0} | set(s))) for r in range(D) for s in itertools.combinations(range(1, D), r)]


def lift(D, K, D2):
    return tuple(x for x in range(D2) if (x % D) in K)


def run(p, LMAX):
    cache, und = {}, []
    def edge(D, K, D2, K2):
        rows = lift(D, K, D2)
        key = (D2, rows, K2)
        if key not in cache:
            st, a, b, n = feasible(p, D2, list(rows), list(K2), limit=LIMIT)
            if st == -1:
                und.append(key)
            cache[key] = (st, a, b)
        return cache[key][0] == 1
    # frontier[L] = antichain (per D) of minimal K reached by chains of length exactly <= L
    reached = {(1, (0,)): 0}
    best = {}   # (D,K) -> (L, parent)
    front = [(1, (0,))]
    best[(1, (0,))] = (0, None)
    for L in range(1, LMAX + 1):
        new = []
        for (D, K) in front:
            for D2 in DIVS:
                if D2 % D:
                    continue
                found = []
                for K2 in sorted(subsets(D2), key=len):
                    if any(set(f) <= set(K2) for f in found):
                        continue
                    # skip K2 already dominated by something reached with length < L at same D2
                    if any(D0 == D2 and set(K0) <= set(K2) and best[(D0, K0)][0] < L for (D0, K0) in best):
                        continue
                    if edge(D, K, D2, K2):
                        found.append(K2)
                        if (D2, K2) not in best:
                            best[(D2, K2)] = (L, (D, K))
                            new.append((D2, K2))
        # keep only minimal new nodes
        front = [x for x in new if not any(y[0] == x[0] and set(y[1]) < set(x[1]) for y in new + list(best))]
        if not front:
            break
    deg9 = {}
    for K in subsets(KAP):
        ds = [best[(D, K0)][0] + 1 for (D, K0) in best if D > 1 and set(lift(D, K0, KAP)) <= set(K)]
        deg9[K] = min(ds) if ds else None
    return best, deg9, cache, und


def path(best, node):
    out = []
    while node is not None:
        out.append(node)
        node = best[node][1]
    return out[::-1]


if __name__ == '__main__':
    LMAX = int(sys.argv[1])
    res = {}
    for p in map(int, sys.argv[2:]):
        best, deg9, cache, und = run(p, LMAX)
        print(f'p={p}: edge tests {len(cache)}, undecided {und}', flush=True)
        for D in DIVS:
            for (D0, K0), (L, par) in sorted(best.items(), key=lambda t: (t[1][0], t[0])):
                if D0 == D:
                    print(f'   reached ({D},{set(K0)}) at length {L}: ' + ' -> '.join(f'({a},{set(b)})' for a, b in path(best, (D0, K0))))
        two = {K: d for K, d in deg9.items() if len(K) <= 2}
        print('   deg of K-nodes |K|<=2:', {str(K): d for K, d in two.items()})
        res[p] = {'deg9': {','.join(map(str, K)): d for K, d in deg9.items()},
                  'witnesses': {f'{k[0]}|{k[1]}|{k[2]}': [v[0], v[1], {str(i): b for i, b in (v[2] or {}).items()}] for k, v in cache.items() if v[0] == 1},
                  'undecided': [list(map(str, u)) for u in und]}
    json.dump(res, open(f'chain_bfs_L{LMAX}_' + '_'.join(sys.argv[2:]) + '.json', 'w'), indent=0)
