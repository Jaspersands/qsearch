#!/opt/anaconda3/bin/python
"""Streaming writer of the sat3.py CNF (same variables, same clauses, same order; low memory for large p).

Writes exactly the file `sat3.py p k K out.cnf` writes (checked by sha256 at (37,9,{0}): c00a76cec23e16d2),
but streams clauses to disk instead of holding them in a list.  The model check is still `sat3.py --check`.
usage: sat3_stream.py p k K1,K2,.. out.cnf
"""
import sys, itertools
sys.path.insert(0, '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-12-rees-exponent-k8-attack')
ARGV = sys.argv[:]
sys.argv = sys.argv[:1]
import exponents_hcd as H
sys.argv = ARGV


def gen(p, k, K, emit):
    g, ind = H.classes(p, k)
    nv = 0
    F = {}
    for t in (1, 2, 3):
        for a in range(k):
            for b in range(k):
                F[(t, a, b)] = list(range(nv + 1, nv + p + 1))
                nv += p
    fixed = {(2, 0, l) for l in range(k)} | {(3, 0, j) for j in range(k)} | {(3, i, 0) for i in range(k)}
    for key, vs in F.items():
        if key in fixed:
            emit([vs[0]])
            for v in vs[1:]:
                emit([-v])
        else:
            emit(list(vs))
            for x, y in itertools.combinations(vs, 2):
                emit([-x, -y])
    for i, j, l in itertools.product(range(k), repeat=3):
        allowed = {0} if (i, j, l) != (0, 0, 0) else set()
        allowed |= {x for x, e in ind.items() if e in {(m - i - j - l) % k for m in K}}
        A, Bv, Cv = F[(1, j, l)], F[(2, i, l)], F[(3, i, j)]
        S = list(range(nv + 1, nv + p + 1))
        nv += p
        for u in range(p):
            for v in range(p):
                emit([-A[u], -Bv[v], S[(u + v) % p]])
        for w in range(p):
            for t in range(p):
                if (w + t) % p not in allowed:
                    emit([-S[w], -Cv[t]])
    return nv


if __name__ == '__main__':
    p, k = int(sys.argv[1]), int(sys.argv[2]); K = tuple(int(x) for x in sys.argv[3].split(','))
    cnt = [0]
    def count(c):
        cnt[0] += 1
    nv = gen(p, k, K, count)
    with open(sys.argv[4], 'w', buffering=1 << 20) as f:
        f.write('p cnf %d %d\n' % (nv, cnt[0]))
        gen(p, k, K, lambda c: f.write(' '.join(map(str, c)) + ' 0\n'))
    print('vars', nv, 'clauses', cnt[0])
