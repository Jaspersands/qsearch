"""Tier B: chains with union targets (Lemma R of the fragment) at selected primes.
BFS over nodes (D, K), D | kappa, 0 in K subset Z_D, |K| <= KMAX; start nodes (1,{0}) of degree 1 and
(D,{0}) of degree e(D) (Tier A degree of a D-solver, D | kappa, 2 <= D < kappa); an edge
(D,K) -> (D2,K2) (D | D2 | kappa) exists if an RC(D2; lift(K) -> K2) contraction is found (and checked),
and costs +1.  Produces for each (p, kappa): NODE0 (degree of a chain to (kappa,{0})), TWO ((m, degree)
for chains to (kappa, K) with K subset {0,m}), FK (K -> degree for chains to (kappa, K)).
Not finding a contraction is NOT a proof of non-existence; the rule then simply does not use it.
usage: tierB.py p1 p2 ...   (merges into tierB.json)"""
import json, os, sys, itertools
from certs import find_rc, prim_root
import rule
HERE = os.path.dirname(os.path.abspath(__file__))
KMAX = 3; LMAX = 3


def lift(K, D, D2):
    return frozenset(x for x in range(D2) if x % D in K)


def bfs(p, kappa, eA, log):
    divs = [D for D in range(1, kappa + 1) if kappa % D == 0]
    best = {}
    frontier = {(1, frozenset([0])): 1}
    for D in divs:
        if 2 <= D < kappa: frontier[(D, frozenset([0]))] = min(frontier.get((D, frozenset([0])), 99), eA[D][0])
    best.update(frontier)
    cache = {}
    for L in range(LMAX):
        new = {}
        for (D, K), dg in frontier.items():
            for D2 in divs:
                if D2 < 2 or D2 % D: continue
                R = lift(K, D, D2)
                if len(R) < 2: continue
                for size in range(1, KMAX + 1):
                    for rest in itertools.combinations(range(1, D2), size - 1):
                        K2 = frozenset((0,) + rest)
                        if D2 < kappa and K2 != frozenset([0]) and size > 1 and D2 != kappa:
                            pass
                        key = (D2, R, K2)
                        if key not in cache:
                            w = find_rc(p, D2, sorted(R), sorted(K2), trials=200)
                            cache[key] = None if (w is None or w[0] == 'undecided') else w
                            if cache[key]:
                                log.append({'p': p, 'D': D2, 'R': sorted(R), 'K': sorted(K2), 'g': prim_root(p),
                                            'alpha': w[0], 'beta': {str(i): v for i, v in w[1].items()}})
                        if cache[key]:
                            node = (D2, K2)
                            if dg + 1 < best.get(node, 99) and dg + 1 < new.get(node, 99):
                                new[node] = dg + 1
        frontier = {k: v for k, v in new.items() if v < best.get(k, 99)}
        best.update(frontier)
        if not frontier: break
    out = {'NODE0': [], 'TWO': [], 'FK': {}}
    for (D, K), dg in best.items():
        if D != kappa: continue
        if K == frozenset([0]): out['NODE0'].append((dg, 'chain{0}'))
        elif len(K) == 2: out['TWO'].append((max(K), dg, f'chain{{0,{max(K)}}}'))
        out['FK'][','.join(map(str, sorted(K)))] = min(dg, out['FK'].get(','.join(map(str, sorted(K))), 99))
    return out


def main(primes):
    path = os.path.join(HERE, 'tierB.json'); lpath = os.path.join(HERE, 'tierB_witnesses.json')
    data = json.load(open(path)) if os.path.exists(path) else {}
    wl = json.load(open(lpath)) if os.path.exists(lpath) else []
    rule.CERTS = rule.load_certs()
    for p in primes:
        eA = rule.degrees(p, tierB=False)
        for kappa in sorted(eA):
            if kappa < 4: continue
            log = []
            o = bfs(p, kappa, eA, log)
            wl.extend(log)
            for kind in ('NODE0', 'TWO', 'FK'):
                data[f'{p}|{kappa}|{kind}'] = o[kind]
            print(p, kappa, 'TierA', eA[kappa], 'NODE0', o['NODE0'], 'TWO', o['TWO'], 'FK', o['FK'], flush=True)
    json.dump(data, open(path, 'w')); json.dump(wl, open(lpath, 'w'))


if __name__ == '__main__':
    main([int(x) for x in sys.argv[1:]])
