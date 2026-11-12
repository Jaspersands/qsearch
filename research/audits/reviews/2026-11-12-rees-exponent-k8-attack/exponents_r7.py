#!/opt/anaconda3/bin/python
"""Rule R7 = R5 + multi-representation descent with general two-class stages (finite exact computation).

Stage options at (p, kappa) (Theorem HC and Proposition HC' of 2026-11-12-rees-exponent-k8-attack.md):
  half : even kappa, a law-free (kappa/2)-solver on the objects' vectors; cost R7(kappa/2, p);
         eps = -omega^{-1}, omega of class kappa/2.
  u{m} : a two-level union step RC(kappa; Z_kappa -> {0, m}) on the objects' vectors (exists: exhaustive
         search); cost 2; eps = -(xi^m)^{-1}.
Each stage doubles the rep multiset: R_{s+1} = R_s u eps R_s.  Finishes F0/F1/F2/F3 as in exponents_hcd.py.
R7(kappa,p) = min(R5, min over multisets of <= 4 stages and finishes).  Applied only where R5 >= 5.
"""
import sys, os, math, functools, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import exponents_hcd as H
X = H.X
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30000


def sumset(A, B, p):
    return {(x + y) % p for x in A for y in B}


@functools.lru_cache(None)
def stage_options(k, p):
    g, ind = H.classes(p, k)
    opts = []
    if k % 2 == 0:
        omega = next(x for x, e in ind.items() if e == k // 2)
        opts.append(('half', None, (-pow(omega, p - 2, p)) % p))
    for m in range(1, k):
        if H.union_step_exists(p, k, (0, m)):
            zm = pow(g, m, p)
            opts.append(('u', m, (-pow(zm, p - 2, p)) % p))
    return tuple(opts)


@functools.lru_cache(None)
def r7(k, p, detail=False):
    base = H.r5(k, p)
    best, plan = base, ('R5',)
    if base < 5 or k == 1:
        return (best, plan) if detail else best
    g, ind = H.classes(p, k)
    P = frozenset(x for x, e in ind.items() if e == 0)
    opts = stage_options(k, p)
    def cost(o):
        return r7(k // 2, p) if o[0] == 'half' else 2
    for s in range(1, 5):
        for seq in itertools.combinations_with_replacement(range(len(opts)), s):
            c0 = sum(cost(opts[i]) for i in seq)
            if c0 + 0 >= best:
                continue
            T, Tn = set(P) | {0}, set(P)
            for i in seq:
                e = opts[i][2]
                eT, eTn = {e * y % p for y in T}, {e * y % p for y in Tn}
                T, Tn = sumset(T, eT, p), sumset(Tn, eT, p) | sumset(T, eTn, p)
            stages = tuple(opts[i][:2] for i in seq)
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
                            cands.append((c0 + r7(Dp, p), stages + (('F2', Dp, c),)))
                            break
            if c0 + 2 < best:
                for c in sorted(C):
                    Kt = tuple(sorted({(m - c) % k for m in C}))
                    if H.union_step_exists(p, k, Kt):
                        cands.append((c0 + 2, stages + (('F3', Kt, c),)))
                        break
            for v, pl in cands:
                if v < best:
                    best, plan = v, pl
    return (best, plan) if detail else best


def E(f, c, p):
    return 1 + sum(f(math.gcd(d, p - 1), p) for d in range(2, c + 1))


if __name__ == '__main__':
    P = [q for q in X.primes_upto(PMAX) if q > 2]
    print('primes 3..%d.  Per-(kappa,p) values where R5 >= 5:' % PMAX)
    for k in range(2, 10):
        for p in P:
            if (p - 1) % k == 0 and H.r5(k, p) >= 5:
                v, pl = r7(k, p, True)
                print(f'  kappa={k} p={p}: R5={H.r5(k, p)} R6={H.r6(k, p)} R7={v} plan={pl}  stage options={[o[:2] for o in stage_options(k, p)]}', flush=True)
    for name, f in (('R5', H.r5), ('R6', H.r6), ('R7', r7)):
        row = []
        for c in range(2, 10):
            best, arg = max((E(f, c, p), p) for p in P if p > c)
            row.append(f'{best}(p={arg})')
        print(f'{name:3s}', ' '.join(row))
    # with the shorter chainless lists of rem:app-s2-chains-scope (chains exist elsewhere; degree not
    # recorded there, so this row only shows which primes would remain binding if those chains have degree <= 4)
    vals = sorted(((E(r7, 9, p), p) for p in P if p > 9), reverse=True)[:14]
    print('c=9 R7 top primes:', vals)
    print('union-step searches abandoned at NODE_CAP (treated as non-existent):', H.UNDECIDED)
    for p in (37, 73, 19, 41, 433, 29, 71):
        print(f'c=9 p={p}: e_d(R7) =', [r7(math.gcd(d, p - 1), p) for d in range(2, 10)],
              'kappa_d =', [math.gcd(d, p - 1) for d in range(2, 10)], 'E =', E(r7, 9, p))
