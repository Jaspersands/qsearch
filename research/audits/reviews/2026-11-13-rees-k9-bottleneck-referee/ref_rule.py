#!/opt/anaconda3/bin/python
"""Referee's own reimplementation of the descent rule with chain nodes (finite exact; CONDITIONAL like R7/R8).

Only input taken from earlier work: R5(kappa, p) = e_grade('R5', p, kappa) of
2026-11-12-rees-exponent-discharge/exponents.py (read-only import; the base grade, unchanged by R7 and R8).
Everything else is computed here with ref_common (own RC solver, own chain BFS run to a fixpoint, no length cap).

Node menu at (kappa, p) (classes mod kappa w.r.t. the least primitive root g):
  N0[K] (0 in K): least degree of a K-node in normal form: chain to (D_L,K_L) with lift(K_L) subset K -> L+1;
                  a D'-solver (1 < D' < kappa, D'Z_kappa subset K) -> r(D'); Gaussian elimination (K = Z_kappa) -> 1.
  N[K] = min_{c in K} N0[K - c]   (a K-node times g^c is a (K+c)-node).
r(kappa,p) = R5 if R5 < 5 (as in R7/R8); else min(R5, N0[{0}], plans), where a plan is a multiset of <= 4
stages {0,m} (cost N[{0,m}], eps = -g^{-m}; Lemma S) and a finish (Lemma F): 0 if 0 in Tn, else
min_{c in C} N0[C - c], C = classes of Tn \\ 0 (C = Z_kappa gives Gaussian elimination, F1).
E(c,p) = 1 + sum_{d=2}^{c} r(gcd(d,p-1), p).
usage: ref_rule.py PMAX
"""
import sys, os, math, functools, itertools, json, time
from ref_common import *

DIS = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-12-rees-exponent-discharge'
sys.path.insert(0, DIS)
_argv = sys.argv[:]
sys.argv = sys.argv[:1]
import exponents as X  # read-only: R5 base grade only
sys.argv = _argv
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
CAP = 20_000_000
t0 = time.time()


@functools.lru_cache(None)
def r5(k, p):
    return 1 if k == 1 else X.e_grade('R5', p, k)


CHAIN = {}


def chain_data(k, p):
    if (k, p) not in CHAIN:
        level, parent, tests, und = chain_bfs(k, p, LMAX=None, cap=CAP)
        from ref_common import _masks, _shifted
        _masks.cache_clear(); _shifted.cache_clear()
        CHAIN[(k, p)] = (chain_degrees(k, level), len(tests), und, level, parent)
        print(f'   [chains kappa={k} p={p}: tests={len(tests)} undecided={len(und)} '
              f'deg{{0}}={CHAIN[(k, p)][0][(0,)]} t={time.time() - t0:.0f}s]', flush=True)
    return CHAIN[(k, p)]


@functools.lru_cache(None)
def N0(k, p, K):
    K = tuple(sorted(K))
    if len(K) == k:
        return 1
    best = math.inf
    d = chain_data(k, p)[0].get(K)
    if d is not None:
        best = d
    for Dp in range(2, k):
        if k % Dp == 0 and set(range(0, k, Dp)) <= set(K):
            best = min(best, r(Dp, p))
    return best


def N(k, p, K):
    return min(N0(k, p, tuple(sorted((x - c) % k for x in K))) for c in K)


@functools.lru_cache(None)
def r(k, p, detail=False):
    if k == 1:
        return (1, 'GE') if detail else 1
    base = r5(k, p)
    if base < 5:
        return (base, 'R5') if detail else base
    best, plan = base, 'R5'
    if N0(k, p, (0,)) < best:
        best, plan = N0(k, p, (0,)), 'chain{0}'
    g, L = dlog(p)
    P = {x for x in range(1, p) if L[x] % k == 0}
    opts = []
    for m in range(1, k):
        cst = N(k, p, (0, m))
        if cst < math.inf:
            opts.append((m, cst, (-pow(pow(g, m, p), p - 2, p)) % p))
    for s in range(1, 5):
        for seq in itertools.combinations_with_replacement(range(len(opts)), s):
            c0 = sum(opts[i][1] for i in seq)
            if c0 >= best:
                continue
            T, Tn = P | {0}, set(P)
            for i in seq:
                e = opts[i][2]
                eT = {e * y % p for y in T}
                eTn = {e * y % p for y in Tn}
                Tn = {(x + y) % p for x in Tn for y in eT} | {(x + y) % p for x in T for y in eTn}
                T = {(x + y) % p for x in T for y in eT}
            if 0 in Tn:
                fin, fd = 0, 'F0'
            else:
                C = {L[x] % k for x in Tn if x}
                fin, fd = min((N0(k, p, tuple(sorted((x - c) % k for x in C))), ('K', c)) for c in C)
            if c0 + fin < best:
                best, plan = c0 + fin, ([(opts[i][0], opts[i][1]) for i in seq], fd, fin)
    return (best, plan) if detail else best


def E(c, p):
    return 1 + sum(r(math.gcd(d, p - 1), p) for d in range(2, c + 1))


if __name__ == '__main__':
    primes = [q for q in X.primes_upto(PMAX) if q > 2]
    print(f'primes 3..{PMAX}; pairs with R5 >= 5:')
    pairs = [(k, p) for k in range(2, 10) for p in primes if (p - 1) % k == 0 and r5(k, p) >= 5]
    for (k, p) in pairs:
        v, pl = r(k, p, True)
        print(f'  kappa={k} p={p}: R5={r5(k, p)} ref={v} plan={pl}', flush=True)
    und = {kp: d[2] for kp, d in CHAIN.items() if d[2]}
    print('undecided RC tests (treated as infeasible):', und)
    row = []
    res = {}
    for c in range(2, 10):
        vals = sorted(((E(c, p), p) for p in primes if p > c), reverse=True)
        top = vals[0][0]
        att = sorted(q for v, q in vals if v == top)
        res[c] = (top, att[:20])
        print(f'c={c}: max {top} attained at {att[:20]}{" ..." if len(att) > 20 else ""}; next {next(((v, q) for v, q in vals if v < top), None)}')
    print('maxima c=2..9:', [res[c][0] for c in range(2, 10)])
    for p in (13, 19, 37, 73, 127, 181, 433, 29, 43):
        print(f'c=9 p={p}: e_d =', [r(math.gcd(d, p - 1), p) for d in range(2, 10)], 'E =', E(9, p))
    print('chain deg{0,m} at kappa=9:', {p: [N0(9, p, (0, m)) for m in range(1, 9)] for (k, p) in pairs if k == 9})
    print('done %.0fs' % (time.time() - t0))
