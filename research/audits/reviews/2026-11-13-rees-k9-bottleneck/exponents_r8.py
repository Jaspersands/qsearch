#!/opt/anaconda3/bin/python
"""Rule R8 = R7 + flexible-line-chain nodes inside the descent calculus (finite exact computation; CONDITIONAL like R7).

R7 is exponents_r7.py of 2026-11-12-rees-exponent-k8-attack (imported read-only).  Changes, only at the (kappa, p)
whose chain data are in chains_all.json (all pairs with R5 >= 5 at p <= 30000):
  * base: min(R5, deg[{0}]) where deg[{0}] is the least L+1 of a chain ending at {0} (thm:app-s2-chain);
  * stage option ('ch', m) of cost deg[{0,m}] (a chain ending at kappa-classes in {0,m} is a {0,m}-node; Lemma S);
  * finish F3': cost deg[C - c] for c in C (a chain K-node, Lemma F), in addition to F0/F1/F2/F3 of R7.
Everything else (stage sumsets, F2 recursion, <= 4 stages) is as in R7.  The u3 stage of 2026-11-13-rees-k9-sat
(conditional on IS Lemma 12 at l = 3) is NOT used.
usage: exponents_r8.py [PMAX]
"""
import sys, os, math, functools, itertools, json
K8 = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-12-rees-exponent-k8-attack'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, K8)
ARGV = sys.argv[:]
sys.argv = sys.argv[:1]
import exponents_hcd as H
import exponents_r7 as R7old
sys.argv = ARGV
X = H.X
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
CH = json.load(open(os.path.join(HERE, 'chains_all.json')))


def deg(k, p, K):
    d = CH.get(f'{k}:{p}')
    if d is None:
        return None
    return d['deg'].get(','.join(map(str, sorted(K))))


def sumset(A, B, p):
    return {(x + y) % p for x in A for y in B}


@functools.lru_cache(None)
def stage_options(k, p):
    g, ind = H.classes(p, k)
    opts = [o + (r8(k // 2, p) if o[0] == 'half' else 2,) for o in R7old.stage_options(k, p)]
    for m in range(1, k):
        dm = deg(k, p, (0, m))
        if dm is not None:
            zm = pow(g, m, p)
            opts.append(('ch', m, (-pow(zm, p - 2, p)) % p, dm))
    return tuple(opts)


@functools.lru_cache(None)
def r8(k, p, detail=False):
    base = H.r5(k, p)
    best, plan = base, ('R5',)
    if base < 5 or k == 1:
        return (best, plan) if detail else best
    d0 = deg(k, p, (0,))
    if d0 is not None and d0 < best:
        best, plan = d0, ('chain{0}',)
    g, ind = H.classes(p, k)
    P = frozenset(x for x, e in ind.items() if e == 0)
    opts = stage_options(k, p)
    for s in range(1, 5):
        for seq in itertools.combinations_with_replacement(range(len(opts)), s):
            c0 = sum(opts[i][3] for i in seq)
            if c0 >= best:
                continue
            T, Tn = set(P) | {0}, set(P)
            for i in seq:
                e = opts[i][2]
                eT, eTn = {e * y % p for y in T}, {e * y % p for y in Tn}
                T, Tn = sumset(T, eT, p), sumset(Tn, eT, p) | sumset(T, eTn, p)
            stages = tuple(opts[i][:2] + (opts[i][3],) for i in seq)
            cands = []
            if 0 in Tn:
                cands.append((c0, stages + (('F0',),)))
            if len(Tn - {0}) == p - 1:
                cands.append((c0 + 1, stages + (('F1',),)))
            C = {ind[x] for x in Tn if x}
            for Dp in range(2, k):
                if k % Dp == 0:
                    cp = {(m * Dp) % k for m in range(k // Dp)}
                    for c in range(k):
                        if {(c + m) % k for m in cp} <= C:
                            cands.append((c0 + r8(Dp, p), stages + (('F2', Dp, c),)))
                            break
            for c in sorted(C):
                Kt = tuple(sorted({(m - c) % k for m in C}))
                dK = deg(k, p, Kt)
                if dK is not None:
                    cands.append((c0 + dK, stages + (('F3chain', Kt, c, dK),)))
                elif c0 + 2 < best and H.union_step_exists(p, k, Kt):
                    cands.append((c0 + 2, stages + (('F3', Kt, c),)))
            for v, pl in cands:
                if v < best:
                    best, plan = v, pl
    return (best, plan) if detail else best


def E(f, c, p):
    return 1 + sum(f(math.gcd(d, p - 1), p) for d in range(2, c + 1))


if __name__ == '__main__':
    P = [q for q in X.primes_upto(PMAX) if q > 2]
    print('primes 3..%d.  Per-(kappa,p) values where R5 >= 5 (R7 -> R8):' % PMAX)
    for k in range(2, 10):
        for p in P:
            if (p - 1) % k == 0 and H.r5(k, p) >= 5:
                v, pl = r8(k, p, True)
                print(f'  kappa={k} p={p}: R5={H.r5(k, p)} R7={R7old.r7(k, p)} R8={v} plan={pl}'
                      + ('' if f'{k}:{p}' in CH else '   [no chain data]'), flush=True)
    for name, f in (('R7', R7old.r7), ('R8', r8)):
        row = []
        for c in range(2, 10):
            best, arg = max((E(f, c, p), p) for p in P if p > c)
            row.append(f'{best}(p={arg})')
        print(f'{name:3s}', ' '.join(row))
    for c in range(2, 10):
        vals = sorted(((E(r8, c, p), p) for p in P if p > c), reverse=True)
        top = vals[0][0]
        print(f'c={c} R8 max {top} attained at', sorted(q for v, q in vals if v == top), ' next:', next(((v, q) for v, q in vals if v < top), None))
    vals = sorted(((E(r8, 9, p), p) for p in P if p > 9), reverse=True)[:16]
    print('c=9 R8 top primes:', vals)
    for p in (37, 73, 127, 181, 433, 19, 29, 13, 71, 31):
        print(f'c=9 p={p}: e_d(R8) =', [r8(math.gcd(d, p - 1), p) for d in range(2, 10)],
              'kappa_d =', [math.gcd(d, p - 1) for d in range(2, 10)], 'E8 =', E(r8, 9, p), ' E7 =', E(R7old.r7, 9, p))
