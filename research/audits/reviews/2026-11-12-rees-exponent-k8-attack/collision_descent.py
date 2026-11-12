#!/opt/anaconda3/bin/python
"""Exact check of the half-degree collision descent at kappa = 8, p = 41 (finite; can only falsify).

Algorithm HCD (2026-11-12-rees-exponent-k8-attack.md, Theorem HC):
  * D-solver (D = kappa/2 = 4): the two-level construction of appendix-schedule2
    (lem:app-s2-tensor + lem:app-s2-witness) with the kappa=4 contraction at p = 41,
    xi = 6, alpha = (10,7,21,24), beta = (0,1,10,9) (found by union_step.py 41 4 1).
    Input: any (a+1)(3a+1) columns in F_41^a.  Output: nonzero x in (P_4 u {0})^M with sum x_b v_b = 0.
  * Stage (collision): objects = vectors v with r disjoint nonempty P_8-reps.  Run the D-solver on
    the vectors of A_4(a) objects; since -1 is not in P_8 but is in P_4 = P_8 u (-P_8), split
    eta into I (eta in P_8) and J (eta in -P_8): u = sum_I eta v = sum_J (-eta) v, which gives
    u with 2r disjoint reps.
  * Finish: after 2 stages every object has 4 reps; 4D = F_41 (D = P_8 u {0}), so a plain
    Gaussian dependency of a+1 objects lifts to a P_8-weighted zero sum.
  Total arity ((a+1)(3a+1))^2 (a+1): degree 5 in a.
Every output is verified: x in (P_8 u {0})^M, x != 0, sum x_b lambda_b = 0 over F_41.
"""
import random, sys, itertools

p, K8, K4 = 41, 8, 4
XI = 6
P8 = {pow(x, 8, p) for x in range(1, p)}
P4 = {pow(x, 4, p) for x in range(1, p)}
D8 = P8 | {0}
IND4 = {}
x = 1
for e in range(p - 1):
    IND4[x] = e % 4
    x = x * XI % p
Z4 = [pow(XI, m, p) for m in range(4)]
ALPHA = [10, 7, 21, 24]
BETA = [0, 1, 10, 9]
C4 = [[Z4[i] * Z4[j] * (ALPHA[j] + BETA[i]) % p for j in range(4)] for i in range(4)]
assert all(c == 0 or c in P4 for row in C4 for c in row) and C4[0][0] != 0
# 4-fold sumset table of D8: value -> (d1,d2,d3,d4)
SUM4 = {}
for t in itertools.product(sorted(D8), repeat=4):
    v = sum(t) % p
    if v not in SUM4 or (SUM4[v] == (0, 0, 0, 0) and any(t)):
        SUM4[v] = t
assert len(SUM4) == p
inv = lambda y: pow(y, p - 2, p)


def nullvec(vecs, dim):
    """Nonzero dependency of the given vectors (len(vecs) > rank), exact Gaussian elimination."""
    n = len(vecs)
    # matrix dim x n ; find kernel vector
    M = [[vecs[j][i] % p for j in range(n)] for i in range(dim)]
    piv = []
    r = 0
    for c in range(n):
        pr = next((i for i in range(r, dim) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = inv(M[r][c])
        M[r] = [y * iv % p for y in M[r]]
        for i in range(dim):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(y - f * z) % p for y, z in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == dim:
            break
    free = next(c for c in range(n) if c not in piv)
    xv = [0] * n
    xv[free] = 1
    for i, c in enumerate(piv):
        xv[c] = (-M[i][free]) % p
    return xv


def solver4(vecs, a):
    """Two-level kappa=4 construction; len(vecs) == (a+1)(3a+1). Returns x in (P4 u 0)^M."""
    B, N = a + 1, 3 * a + 1
    assert len(vecs) == B * N
    blocks = []
    for nu in range(N):
        idx = list(range(nu * B, (nu + 1) * B))
        c = nullvec([vecs[b] for b in idx], a)
        bs = next(b for b in range(B) if c[b])
        c = [y * inv(c[bs]) % p for y in c]
        cells = {}
        for t, b in enumerate(idx):
            if c[t]:
                i = IND4[c[t]]
                w = c[t] * inv(Z4[i]) % p
                assert w in P4
                cells.setdefault(i, []).append((b, w))
        T = []
        for i in range(4):
            v = [0] * a
            for b, w in cells.get(i, []):
                v = [(y + w * z) % p for y, z in zip(v, vecs[b])]
            T.append(v)
        blocks.append((cells, T))
    V = [sum((blocks[nu][1][i] for i in range(1, 4)), []) for nu in range(N)]
    eta = nullvec(V, 3 * a)
    ns = next(n for n in range(N) if eta[n])
    eta = [y * inv(eta[ns]) % p for y in eta]
    xv = [0] * len(vecs)
    for nu in range(N):
        if not eta[nu]:
            continue
        j = IND4[eta[nu]]
        vp = eta[nu] * inv(Z4[j]) % p
        for i, lst in blocks[nu][0].items():
            for b, w in lst:
                xv[b] = C4[i][j] * vp * w % p
    assert any(xv), 'solver4 returned zero'
    assert all(y == 0 or y in P4 for y in xv)
    assert all(sum(xv[b] * vecs[b][i] for b in range(len(vecs))) % p == 0 for i in range(a))
    return xv


class Obj:
    """vector v in F_p^a with disjoint P8-reps: list of dict col -> coef, sum coef*lambda = v."""
    def __init__(self, v, reps):
        self.v, self.reps = v, reps


PATH = []


class Found(Exception):
    def __init__(self, x):
        self.x = x


def stage(objs, a):
    vecs = [o.v for o in objs]
    eta = solver4(vecs, a)
    I = [n for n in range(len(objs)) if eta[n] and eta[n] in P8]
    J = [n for n in range(len(objs)) if eta[n] and eta[n] not in P8]
    for n in J:
        assert (-eta[n]) % p in P8
    r = len(objs[0].reps)
    def side(S, sign):
        out = []
        for k in range(r):
            rep = {}
            for n in S:
                cf = eta[n] * sign % p
                for col, c in objs[n].reps[k].items():
                    rep[col] = cf * c % p
            out.append(rep)
        return out
    if not I or not J:
        S = I or J
        PATH.append('early@stage')
        raise Found(side(S, 1 if I else p - 1)[0])
    u = [0] * a
    for n in I:
        u = [(y + eta[n] * z) % p for y, z in zip(u, objs[n].v)]
    return Obj(u, side(I, 1) + side(J, p - 1))


def hcd(lams, a):
    A4 = (a + 1) * (3 * a + 1)
    need = A4 * A4 * (a + 1)
    assert len(lams) == need
    objs = [Obj(list(l), [{b: 1}]) for b, l in enumerate(lams)]
    try:
        for _ in range(2):
            objs = [stage(objs[i * A4:(i + 1) * A4], a) for i in range(len(objs) // A4)]
        # every object now has 4 reps; zero-vector object => any rep is a zero sum
        for o in objs:
            if not any(o.v):
                PATH.append('zero-object')
                raise Found(o.reps[0])
        assert len(objs) == a + 1 and all(len(o.reps) == 4 for o in objs)
        eta = nullvec([o.v for o in objs], a)
        x = {}
        for n, o in enumerate(objs):
            if eta[n]:
                for k, dk in enumerate(SUM4[eta[n]]):
                    if dk:
                        for col, c in o.reps[k].items():
                            x[col] = dk * c % p
        PATH.append('full: 2 stages + GE')
        raise Found(x)
    except Found as F:
        xv = [0] * len(lams)
        for col, c in F.x.items():
            xv[col] = c
        return xv


def verify(xv, lams, a):
    return (any(xv) and all(y in D8 for y in xv)
            and all(sum(xv[b] * lams[b][i] for b in range(len(lams))) % p == 0 for i in range(a)))


def banks(a, n, rng):
    yield 'uniform', [[rng.randrange(p) for _ in range(a)] for _ in range(n)]
    yield 'all-e1', [[1] + [0] * (a - 1) for _ in range(n)]
    yield 'dead-blocks+uniform', [([0] * (b % a) + [rng.choice([1, 3])] + [0] * (a - 1 - b % a)) if b % 5 else
                                  [rng.randrange(p) for _ in range(a)] for b in range(n)]
    yield 'few-values', (lambda S: [rng.choice(S) for _ in range(n)])([[rng.randrange(p) for _ in range(a)] for _ in range(3)])
    yield 'zeros-mixed', [[0] * a if rng.random() < 0.3 else [rng.randrange(p) for _ in range(a)] for _ in range(n)]
    yield 'class-cosets', [[rng.choice([1, 6, 36, 11]) * (i == b % a) for i in range(a)] for b in range(n)]


if __name__ == '__main__':
    rng = random.Random(20261112)
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    tot = ok = 0
    for a in (1, 2, 3):
        A4 = (a + 1) * (3 * a + 1)
        n = A4 * A4 * (a + 1)
        for r in range(reps):
            for name, lams in banks(a, n, rng):
                PATH.clear()
                xv = hcd(lams, a)
                good = verify(xv, lams, a)
                tot += 1; ok += good
                print(f'a={a} M={n} bank={name:20s} support={sum(1 for y in xv if y):5d} path={PATH[-1]:22s} verified={good}')
    print(f'TOTAL {ok}/{tot} verified')
