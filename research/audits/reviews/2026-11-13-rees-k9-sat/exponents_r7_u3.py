#!/opt/anaconda3/bin/python
"""R7 with additional THREE-level two-class union stages (finite exact computation; CONDITIONAL like R7).

Same rule as exponents_r7.py (2026-11-12-rees-exponent-k8-attack), copied, with one change: at the (p, kappa, m)
listed in U3 (three-level union steps RC3(kappa; Z_kappa^3 -> {0, m}) found by sat3.py + kissat and verified by
sat3.py --check), a stage option ('u3', m) of cost 3 is added, eps = -(g^m)^{-1} exactly as for the two-level
stage (Lemma S only uses that the node's nonzero output classes lie in {0, m}).
Finishes are unchanged (F0/F1/F2/F3 with TWO-level union steps).
usage: exponents_r7_u3.py PMAX "p:k:m,p:k:m,..."
"""
import sys, os, math, functools, itertools
K8 = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-12-rees-exponent-k8-attack'
sys.path.insert(0, K8)
ARGV = sys.argv[:]
sys.argv = sys.argv[:1]
import exponents_hcd as H
import exponents_r7 as R7old
sys.argv = ARGV
X = H.X
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
U3 = set()
if len(sys.argv) > 2 and sys.argv[2]:
    for t in sys.argv[2].split(','):
        p_, k_, m_ = map(int, t.split(':'))
        U3.add((p_, k_, m_))


def sumset(A, B, p):
    return {(x + y) % p for x in A for y in B}


@functools.lru_cache(None)
def stage_options(k, p):
    g, ind = H.classes(p, k)
    opts = list(R7old.stage_options(k, p))
    for m in range(1, k):
        if (p, k, m) in U3:
            zm = pow(g, m, p)
            opts.append(('u3', m, (-pow(zm, p - 2, p)) % p))
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
        return r7(k // 2, p) if o[0] == 'half' else (3 if o[0] == 'u3' else 2)
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
    print('U3 =', sorted(U3))
    for (p, k, m) in sorted(U3):
        v, pl = r7(k, p, True)
        print(f'  kappa={k} p={p}: old R7={R7old.r7(k, p)} new R7={v} plan={pl}')
    P = [q for q in X.primes_upto(PMAX) if q > 2]
    for name, f in (('R7old', R7old.r7), ('R7new', r7)):
        row = []
        for c in range(2, 10):
            best, arg = max((E(f, c, p), p) for p in P if p > c)
            row.append(f'{best}(p={arg})')
        print(f'{name:5s}', ' '.join(row))
    vals = sorted(((E(r7, 9, p), p) for p in P if p > 9), reverse=True)[:14]
    print('c=9 new R7 top primes:', vals)
    for p in (19, 37, 73):
        print(f'c=9 p={p}: e_d(new R7) =', [r7(math.gcd(d, p - 1), p) for d in range(2, 10)], 'E =', E(r7, 9, p),
              ' (old E =', E(R7old.r7, 9, p), ')')
