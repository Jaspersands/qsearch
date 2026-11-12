#!/opt/anaconda3/bin/python
"""Independent re-encoding of the three-level union-target contraction problem (cross-check of sat3.py).

Same mathematical problem as sat3.py, written from the definition without reusing its code:
  exists F1, F2, F3 : Z_k^2 -> F_p,  B(i,j,l) = F1(j,l) + F2(i,l) + F3(i,j),
  B(i,j,l) in {0} u {x != 0 : dlog_g(x) mod k in K - (i+j+l)}  for all (i,j,l),  B(0,0,0) != 0,
g = least primitive root mod p.
Differences from sat3.py: NO gauge fixing (option --gauge adds it, to compare); the auxiliary sum is
T = F2 + F3 (sat3.py uses F1 + F2), with T encoded by equivalence T[w] <-> OR_{u+v=w}(F2=u & F3=v)
(sat3.py uses implications only); the cell constraint is written as clauses (-T[w] v -F1[t]) for
forbidden w + t; at-most-one by a sequential (ladder) encoding instead of pairwise.
usage: indep_cnf.py p k K1,K2,.. out.cnf [--gauge]
"""
import sys, itertools


def main():
    p, k = int(sys.argv[1]), int(sys.argv[2])
    K = {int(x) % k for x in sys.argv[3].split(',')}
    out = sys.argv[4]
    gauge = '--gauge' in sys.argv
    g = next(h for h in range(2, p) if all(pow(h, (p - 1) // q, p) != 1
                                           for q in range(2, p) if (p - 1) % q == 0 and
                                           all(q % r for r in range(2, q))))
    dlog = {}
    x = 1
    for e in range(p - 1):
        dlog[x] = e
        x = x * g % p
    n = [0]
    cls = []

    def var():
        n[0] += 1
        return n[0]

    def exactly_one(xs):
        cls.append(list(xs))
        s = [var() for _ in xs[:-1]]          # ladder: s[r] = some of xs[0..r] true
        for r, xv in enumerate(xs[:-1]):
            cls.append([-xv, s[r]])
            if r > 0:
                cls.append([-s[r - 1], s[r]])
                cls.append([-xv, -s[r - 1]])
        cls.append([-xs[-1], -s[-1]])

    F = {(t, a, b): [var() for _ in range(p)] for t in (1, 2, 3) for a in range(k) for b in range(k)}
    for key, xs in F.items():
        exactly_one(xs)
    if gauge:
        for key in [(2, 0, l) for l in range(k)] + [(3, 0, j) for j in range(k)] + [(3, i, 0) for i in range(k)]:
            cls.append([F[key][0]])
    for i, j, l in itertools.product(range(k), repeat=3):
        ok = set() if (i, j, l) == (0, 0, 0) else {0}
        ok |= {y for y in range(1, p) if (dlog[y] + i + j + l) % k in K}
        F1, F2, F3 = F[(1, j, l)], F[(2, i, l)], F[(3, i, j)]
        T = [var() for _ in range(p)]
        for w in range(p):
            pairs = []
            for u in range(p):
                v = (w - u) % p
                a = var()                       # a <-> F2=u & F3=v
                cls.append([-a, F2[u]]); cls.append([-a, F3[v]]); cls.append([a, -F2[u], -F3[v]])
                pairs.append(a)
            cls.append([-T[w]] + pairs)
            for a in pairs:
                cls.append([T[w], -a])
        for w in range(p):
            for t in range(p):
                if (w + t) % p not in ok:
                    cls.append([-T[w], -F1[t]])
    with open(out, 'w') as f:
        f.write(f'p cnf {n[0]} {len(cls)}\n')
        for c in cls:
            f.write(' '.join(map(str, c)) + ' 0\n')
    print('vars', n[0], 'clauses', len(cls), 'gauge', gauge)


main()
