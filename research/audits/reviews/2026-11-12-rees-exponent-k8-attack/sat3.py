#!/opt/anaconda3/bin/python
"""SAT encoding of a THREE-level union-target contraction at (p, kappa, K) (finite exact search).

Object (IS Lemma 12 with l = 3, then a contraction): functions F1, F2, F3 : Z_k^2 -> F_p with
  B(i,j,l) = F1(j,l) + F2(i,l) + F3(i,j)  in  {0} u U_{m in K} Q_{m-i-j-l}   for all (i,j,l),
  B(0,0,0) != 0,
where Q_m = g^m P_kappa (g = least primitive root).  Then C(i,j,l) = z_i z_j z_l B(i,j,l) annihilates
W^{(x)3} and has classes in K, so (with the 3-level tensor of arity (a+1)((k-1)a+1)((k-1)^2 a+1)) it gives a
law-free degree-3 node (K = (0,)) or a degree-3 two-class stage (|K| = 2).
Gauge fixed: F2(0,l) = 0, F3(0,j) = 0, F3(i,0) = 0 (B is invariant under the 3 slice shifts).
Usage: sat3.py p k K1,K2,... out.cnf      ;  sat3.py --check p k K model.txt  (decode and verify a model)
"""
import sys, itertools
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
ARGV = sys.argv[:]
sys.argv = sys.argv[:1]   # exponents.py parses argv at import
import exponents_hcd as H
sys.argv = ARGV


def build(p, k, K):
    g, ind = H.classes(p, k)
    nv = [0]
    def new():
        nv[0] += 1
        return nv[0]
    F = {}
    for t in (1, 2, 3):
        for a in range(k):
            for b in range(k):
                F[(t, a, b)] = [new() for _ in range(p)]
    clauses = []
    def onehot(vs):
        clauses.append(list(vs))
        for x, y in itertools.combinations(vs, 2):
            clauses.append([-x, -y])
    fixed = set()
    for l in range(k):
        fixed.add((2, 0, l))
    for j in range(k):
        fixed.add((3, 0, j))
    for i in range(k):
        fixed.add((3, i, 0))
    for key, vs in F.items():
        if key in fixed:
            clauses.append([vs[0]])
            for v in vs[1:]:
                clauses.append([-v])
        else:
            onehot(vs)
    for i, j, l in itertools.product(range(k), repeat=3):
        allowed = {0} if (i, j, l) != (0, 0, 0) else set()
        allowed |= {x for x, e in ind.items() if e in {(m - i - j - l) % k for m in K}}
        A, Bv, Cv = F[(1, j, l)], F[(2, i, l)], F[(3, i, j)]
        S = [new() for _ in range(p)]          # S = F1 + F2
        for u in range(p):
            for v in range(p):
                clauses.append([-A[u], -Bv[v], S[(u + v) % p]])
        for w in range(p):
            for t in range(p):
                if (w + t) % p not in allowed:
                    clauses.append([-S[w], -Cv[t]])
    return nv[0], clauses, F


def decode_check(p, k, K, model_file):
    nvars, clauses, F = build(p, k, K)
    true = set()
    for line in open(model_file):
        if line.startswith('v'):
            true |= {int(x) for x in line.split()[1:] if int(x) > 0}
    val = {key: next(u for u, v in enumerate(vs) if v in true) for key, vs in F.items()}
    g, ind = H.classes(p, k)
    ok = True
    for i, j, l in itertools.product(range(k), repeat=3):
        b = (val[(1, j, l)] + val[(2, i, l)] + val[(3, i, j)]) % p
        if (i, j, l) == (0, 0, 0) and b == 0:
            ok = False
        if b and ind[b] not in {(m - i - j - l) % k for m in K}:
            ok = False
    # independent check of the annihilation property on random elements of W^{(x)3}
    import random
    z = [pow(g, m, p) for m in range(k)]
    C = {(i, j, l): z[i] * z[j] * z[l] * ((val[(1, j, l)] + val[(2, i, l)] + val[(3, i, j)]) % p) % p
         for i, j, l in itertools.product(range(k), repeat=3)}
    rng = random.Random(1)
    def rand_w():
        w = [rng.randrange(p) for _ in range(k - 1)]
        s = sum(z[m + 1] * w[m] for m in range(k - 1)) % p
        return [(-s) % p] + w      # z_0 = 1
    for _ in range(50):
        w1, w2, w3 = rand_w(), rand_w(), rand_w()
        if sum(C[(i, j, l)] * w1[i] * w2[j] * w3[l] for i, j, l in C) % p:
            ok = False
    return ok, val


if __name__ == '__main__':
    if sys.argv[1] == '--check':
        p, k = int(sys.argv[2]), int(sys.argv[3]); K = tuple(int(x) for x in sys.argv[4].split(','))
        ok, val = decode_check(p, k, K, sys.argv[5])
        print('model verified (class conditions, B(0)!=0, annihilation on 50 random W^3 elements):', ok)
        print('F values:', {kk: v for kk, v in sorted(val.items())})
    else:
        p, k = int(sys.argv[1]), int(sys.argv[2]); K = tuple(int(x) for x in sys.argv[3].split(','))
        nvars, clauses, _ = build(p, k, K)
        with open(sys.argv[4], 'w') as f:
            f.write('p cnf %d %d\n' % (nvars, len(clauses)))
            for c in clauses:
                f.write(' '.join(map(str, c)) + ' 0\n')
        print('vars', nvars, 'clauses', len(clauses))
