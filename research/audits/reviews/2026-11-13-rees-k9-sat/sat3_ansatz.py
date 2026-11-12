#!/opt/anaconda3/bin/python
"""Symmetric ansatz for the three-level union-target contraction (finite exact search; SAT only is informative).

The sat3.py problem is invariant under permuting the three coordinates (the class condition depends on i+j+l).
Ansatz C3 (cyclic):  B(i,j,l) = F(j,l) + F(l,i) + F(i,j)   (one F : Z_k^2 -> F_p; B is cyclically symmetric).
   Gauge F -> F + h(x) - h(y) leaves B unchanged; fixed by F(0,y) = 0 for y != 0.
Ansatz S3 (symmetric): as C3 with F symmetric, F(x,y) = F(y,x) (B fully symmetric; no gauge).
Every ansatz solution is a sat3.py solution (F1 = F, F2(i,l) = F(l,i), F3 = F), so SAT here => SAT there
(the --dump option writes a model of the sat3.py CNF, to be checked by sat3.py --check / verify_model.py).
UNSAT here says nothing about the full problem.
usage: sat3_ansatz.py C3|S3 p k K out.cnf          ;  sat3_ansatz.py --dump C3|S3 p k K model.txt full_model.txt
"""
import sys, itertools
sys.path.insert(0, '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-12-rees-exponent-k8-attack')
ARGV = sys.argv[:]
sys.argv = sys.argv[:1]
import exponents_hcd as H
sys.argv = ARGV


def key(mode, x, y):
    return (min(x, y), max(x, y)) if mode == 'S3' else (x, y)


def build(mode, p, k, K):
    g, ind = H.classes(p, k)
    nv = [0]
    def new():
        nv[0] += 1
        return nv[0]
    F = {}
    for x in range(k):
        for y in range(k):
            kk = key(mode, x, y)
            if kk not in F:
                F[kk] = [new() for _ in range(p)]
    cl = []
    for kk, vs in F.items():
        if mode == 'C3' and kk[0] == 0 and kk[1] != 0:
            cl.append([vs[0]])
            cl.extend([-v] for v in vs[1:])
        else:
            cl.append(list(vs))
            cl.extend([-a, -b] for a, b in itertools.combinations(vs, 2))
    seen = set()
    for i, j, l in itertools.product(range(k), repeat=3):
        rep = tuple(sorted((i, j, l))) if mode == 'S3' else min([(i, j, l), (j, l, i), (l, i, j)])
        if rep in seen:
            continue
        seen.add(rep)
        allowed = {0} if (i, j, l) != (0, 0, 0) else set()
        allowed |= {x for x, e in ind.items() if e in {(m - i - j - l) % k for m in K}}
        A, Bv, Cv = F[key(mode, j, l)], F[key(mode, l, i)], F[key(mode, i, j)]
        S = [new() for _ in range(p)]
        for u in range(p):
            for v in range(p):
                cl.append([-A[u], -Bv[v], S[(u + v) % p]])
        for w in range(p):
            for t in range(p):
                if (w + t) % p not in allowed:
                    cl.append([-S[w], -Cv[t]])
    return nv[0], cl, F


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == '--dump':
        mode, p, k, K = a[1], int(a[2]), int(a[3]), tuple(int(x) for x in a[4].split(','))
        _, _, F = build(mode, p, k, K)
        true = set()
        for line in open(a[5]):
            if line.startswith('v'):
                true |= {int(x) for x in line.split()[1:] if int(x) > 0}
        val = {kk: next(u for u, v in enumerate(vs) if v in true) for kk, vs in F.items()}
        Fv = lambda x, y: val[key(mode, x, y)]
        # sat3.py layout: t = 1,2,3; a, b in range(k); p value vars each. F1(j,l)=F(j,l), F2(i,l)=F(l,i), F3(i,j)=F(i,j)
        lits, base = [], 0
        for t in (1, 2, 3):
            for x in range(k):
                for y in range(k):
                    u = Fv(x, y) if t != 2 else Fv(y, x)
                    lits.append(base + 1 + u)
                    base += p
        with open(a[6], 'w') as f:
            f.write('s SATISFIABLE\nv ' + ' '.join(map(str, lits)) + ' 0\n')
        print('wrote full-layout model (NOT gauge-fixed: check with verify_model.py, not sat3.py --check)')
    else:
        mode, p, k, K = a[0], int(a[1]), int(a[2]), tuple(int(x) for x in a[3].split(','))
        nv, cl, _ = build(mode, p, k, K)
        with open(a[4], 'w') as f:
            f.write('p cnf %d %d\n' % (nv, len(cl)))
            for c in cl:
                f.write(' '.join(map(str, c)) + ' 0\n')
        print('vars', nv, 'clauses', len(cl))
