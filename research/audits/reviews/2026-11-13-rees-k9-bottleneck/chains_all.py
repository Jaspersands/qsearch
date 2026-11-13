#!/opt/anaconda3/bin/python
"""Shortest flexible-line chains (thm:app-s2-chain) to every class target, for general kappa (finite exact search).

For kappa and p = 1 mod kappa, BFS over nodes (D, K), D | kappa, D >= 2, 0 in K subset Z_D, from (1,{0}).
Edge (D,K) -> (D2,K2), D | D2: RC(D2; lift_{D2}(K) -> K2) feasible (complete DFS, rcdfs.c; witnesses
re-checked by pow in rc.check).  A chain of length L ending at (D_L, K_L) is a law-free node of degree L+1
(arity binom(a+L+1, L+1)) with kappa-classes in lift_kappa(K_L).
deg[K] (K subset Z_kappa, 0 in K) = least L+1 over chains whose final kappa-class set is contained in K.
Writes chains_all.json: {"kappa:p": {"deg": {"0,1": 3, ...}, "paths": {...}, "undecided": [...]}}.
Usage: chains_all.py LMAX kappa:p kappa:p ...
"""
import sys, itertools, json, os
from rc import feasible

LIMIT = 10**9


def subsets(D):
    return [tuple(sorted({0} | set(s))) for r in range(D) for s in itertools.combinations(range(1, D), r)]


def lift(D, K, D2):
    return tuple(x for x in range(D2) if (x % D) in K)


def run(kap, p, LMAX):
    divs = [d for d in range(2, kap + 1) if kap % d == 0]
    cache, und = {}, []
    def edge(D, K, D2, K2):
        rows = lift(D, K, D2)
        key = (D2, rows, K2)
        if key not in cache:
            st, a, b, n = feasible(p, D2, list(rows), list(K2), limit=LIMIT)
            if st == -1:
                und.append(key)
            cache[key] = st
        return cache[key] == 1
    best = {(1, (0,)): (0, None)}
    front = [(1, (0,))]
    for L in range(1, LMAX + 1):
        new = []
        for (D, K) in front:
            for D2 in divs:
                if D2 % D:
                    continue
                found = []
                for K2 in sorted(subsets(D2), key=len):
                    if len(K2) == D2:
                        continue           # trivial target: never better than Gaussian elimination
                    if any(set(f) <= set(K2) for f in found):
                        continue
                    if any(D0 == D2 and set(K0) <= set(K2) and best[(D0, K0)][0] < L for (D0, K0) in best):
                        continue
                    if edge(D, K, D2, K2):
                        found.append(K2)
                        if (D2, K2) not in best:
                            best[(D2, K2)] = (L, (D, K))
                            new.append((D2, K2))
        front = [x for x in new if not any(y[0] == x[0] and set(y[1]) < set(x[1]) for y in list(best))]
        if not front:
            break
    deg = {}
    for K in subsets(kap):
        ds = [best[(D, K0)][0] + 1 for (D, K0) in best if D > 1 and set(lift(D, K0, kap)) <= set(K)]
        deg[K] = min(ds) if ds else None
    return best, deg, und, len(cache)


def path(best, node):
    out = []
    while node is not None:
        out.append(node)
        node = best[node][1]
    return out[::-1]


if __name__ == '__main__':
    LMAX = int(sys.argv[1])
    fn = 'chains_all.json'
    res = json.load(open(fn)) if os.path.exists(fn) else {}
    for t in sys.argv[2:]:
        kap, p = map(int, t.split(':'))
        best, deg, und, ne = run(kap, p, LMAX)
        small = {K: d for K, d in deg.items() if len(K) <= 2}
        print(f'kappa={kap} p={p} LMAX={LMAX}: edge tests {ne}, undecided {len(und)}; '
              f'deg{{0}}={deg[(0,)]}; two-class degs ' + ' '.join(f'{K[-1] if len(K)>1 else 0}:{d}' for K, d in small.items() if len(K) == 2), flush=True)
        for K in [(0,)] + [K for K in small if len(K) == 2]:
            cands = [(best[n][0], n) for n in best if n[0] > 1 and set(lift(n[0], n[1], kap)) <= set(K)]
            if cands:
                L, n = min(cands)
                print('     ', K, 'via', ' -> '.join(f'({a},{set(b)})' for a, b in path(best, n)))
        res[f'{kap}:{p}'] = {'LMAX': LMAX, 'deg': {','.join(map(str, K)): d for K, d in deg.items()},
                            'undecided': [str(u) for u in und]}
        json.dump(res, open(fn, 'w'), indent=0)
