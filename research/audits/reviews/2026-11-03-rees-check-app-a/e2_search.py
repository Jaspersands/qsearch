"""Exact search for two-level contractions (Definition before lem:app-s2-witness).

A contraction is (alpha, beta) with beta_0 = 0 (WLOG), alpha_0 in Q_0, and
alpha_j + beta_i in Q_{-(i+j)} u {0} for all i, j (Lemma lem:app-s2-normal).
mode 'zero'   : entries in Q_0 u {0}, the appendix's definition of E_2;
mode 'strict' : every entry in Q_0 (what Propositions TW/TA and Phase 0 produce).
Depth-first search over beta_1..beta_{k-1} with bitmask candidate sets for each
column alpha_j; exhaustive when no contraction exists.
Usage: python -I e2_search.py KAPPA PMAX [MODE] [PMIN]
"""
import json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sympy import primerange, primitive_root
from ffcommon import coset_table, masks, rot

sys.setrecursionlimit(10000)


def find_contraction(p, k, mode='zero', xi=None, rng=None):
    ind, xi = coset_table(p, k, xi)
    full = (1 << p) - 1
    mz = masks(p, k, ind, with_zero=(mode == 'zero'))
    mstrict = masks(p, k, ind, with_zero=False)
    start = [mstrict[0]] + [mz[(-j) % k] for j in range(1, k)]
    order = list(range(p))
    if rng is not None:
        rng.shuffle(order)
    beta = [0] * k

    def dfs(i, cols):
        if i == k:
            return True
        for b in order:
            new = []
            for j in range(k):
                c = cols[j] & rot(mz[(-(i + j)) % k], b, p, full)
                if not c:
                    break
                new.append(c)
            else:
                beta[i] = b
                if dfs(i + 1, new):
                    return True
        return False

    if not all(start):
        return None, xi
    if dfs(1, start):
        # rebuild alpha and verify every coset condition directly
        alpha = []
        for j in range(k):
            ok = [x for x in range(p) if (j > 0 or x != 0) and all(
                ((x + beta[i]) % p == 0 and mode == 'zero' and not (i == 0 and j == 0)) or
                ((x + beta[i]) % p != 0 and ind[(x + beta[i]) % p] == (-(i + j)) % k) for i in range(k))]
            assert ok, (p, k, beta, j)
            alpha.append(ok[0])
        C = [[(pow(xi, i, p) * pow(xi, j, p) * (alpha[j] + beta[i])) % p for j in range(k)] for i in range(k)]
        assert C[0][0] != 0
        for row in C:
            for e in row:
                assert e == 0 and mode == 'zero' or (e != 0 and ind[e] == 0)
        return (alpha, beta, C), xi
    return None, xi


def exceptional(k, pmax, mode, pmin=3, seed=1):
    rng = random.Random(seed)
    E = []
    for p in primerange(max(pmin, k + 1), pmax):
        if (p - 1) % k:
            continue
        res, _ = find_contraction(p, k, mode, rng=rng)
        if res is None:
            E.append(p)
    return E


if __name__ == '__main__':
    k = int(sys.argv[1]); pmax = int(sys.argv[2])
    mode = sys.argv[3] if len(sys.argv) > 3 else 'zero'
    pmin = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    t = time.time()
    E = exceptional(k, pmax, mode, pmin)
    print(json.dumps(dict(kappa=k, pmin=pmin, pmax=pmax, mode=mode, E=E, n=len(E),
                          seconds=round(time.time() - t, 1))))
