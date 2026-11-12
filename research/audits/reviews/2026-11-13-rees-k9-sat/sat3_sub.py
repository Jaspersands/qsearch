#!/opt/anaconda3/bin/python
"""Sub-box restriction of the sat3.py problem (finite exact search; sufficient test for UNSAT).

Same problem as sat3.py (three-level union-target contraction at (p, kappa, K)), but the cell set is
restricted to S x S x S for an index set S containing 0 (F1, F2, F3 restricted to S x S).  Any solution of
the full problem restricts to a solution of the sub-box problem, so sub-box UNSAT => full UNSAT.
(A sub-box SAT says nothing.)  Gauge fixing F2(0,.) = F3(0,.) = F3(.,0) = 0 on S: the same three slice shifts
as in sat3.py, restricted to S, so it loses no solutions.
Option 'one': add F1(0,0) = 1 (case B(0,0,0) in Q_0; with K = {0,m} the case B(0,0,0) in Q_m is the case
'one' of K = {0,-m} after scaling by g^{-m}, so the 8 cases ('one', K = {0,m}), m = 1..8, cover all m).
Option sym: add F1(0,0) in {1, g^m : m in K \\ {0}} (scaling by an element of P_kappa preserves classes and the
gauge zeros, and P_kappa acts transitively on each class; B(0,0,0) = F1(0,0) under the gauge).
usage: sat3_sub.py p k K S out.cnf [sym]       e.g.  sat3_sub.py 37 9 0,1 0,1,2,3,4 x.cnf
       sat3_sub.py --check p k K S model        (decode and verify the restricted conditions)
"""
import sys, itertools, os
sys.path.insert(0, '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-12-rees-exponent-k8-attack')
ARGV = sys.argv[:]
sys.argv = sys.argv[:1]
import exponents_hcd as H
sys.argv = ARGV


def build(p, k, K, S, sym=False):
    assert 0 in S
    g, ind = H.classes(p, k)
    nv = [0]
    def new():
        nv[0] += 1
        return nv[0]
    F = {(t, a, b): [new() for _ in range(p)] for t in (1, 2, 3) for a in S for b in S}
    clauses = []
    fixed = {(2, 0, l) for l in S} | {(3, 0, j) for j in S} | {(3, i, 0) for i in S}
    for key, vs in F.items():
        if key in fixed:
            clauses.append([vs[0]])
            clauses.extend([-v] for v in vs[1:])
        else:
            clauses.append(list(vs))
            clauses.extend([-x, -y] for x, y in itertools.combinations(vs, 2))
    if sym == 'sym':
        clauses.append([F[(1, 0, 0)][pow(g, m, p)] for m in sorted(set(K) | {0})])
    elif sym == 'one':
        clauses.append([F[(1, 0, 0)][1]])
    for i, j, l in itertools.product(S, repeat=3):
        allowed = {0} if (i, j, l) != (0, 0, 0) else set()
        allowed |= {x for x, e in ind.items() if e in {(m - i - j - l) % k for m in K}}
        A, Bv, Cv = F[(1, j, l)], F[(2, i, l)], F[(3, i, j)]
        T = [new() for _ in range(p)]
        for u in range(p):
            for v in range(p):
                clauses.append([-A[u], -Bv[v], T[(u + v) % p]])
        for w in range(p):
            for t in range(p):
                if (w + t) % p not in allowed:
                    clauses.append([-T[w], -Cv[t]])
    return nv[0], clauses, F


def check(p, k, K, S, model):
    _, _, F = build(p, k, K, S)
    true = set()
    for line in open(model):
        if line.startswith('v'):
            true |= {int(x) for x in line.split()[1:] if int(x) > 0}
    val = {key: next(u for u, v in enumerate(vs) if v in true) for key, vs in F.items()}
    g, ind = H.classes(p, k)
    ok = True
    for i, j, l in itertools.product(S, repeat=3):
        b = (val[(1, j, l)] + val[(2, i, l)] + val[(3, i, j)]) % p
        if (i, j, l) == (0, 0, 0) and b == 0:
            ok = False
        if b and ind[b] not in {(m - i - j - l) % k for m in K}:
            ok = False
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == '--check':
        p, k = int(a[1]), int(a[2]); K = tuple(int(x) for x in a[3].split(',')); S = tuple(int(x) for x in a[4].split(','))
        print('sub-box model verified:', check(p, k, K, S, a[5]))
    else:
        p, k = int(a[0]), int(a[1]); K = tuple(int(x) for x in a[2].split(',')); S = tuple(int(x) for x in a[3].split(','))
        nv, cl, _ = build(p, k, K, S, sym=a[5] if len(a) > 5 else False)
        with open(a[4], 'w') as f:
            f.write('p cnf %d %d\n' % (nv, len(cl)))
            for c in cl:
                f.write(' '.join(map(str, c)) + ' 0\n')
        print('vars', nv, 'clauses', len(cl))
