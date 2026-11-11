"""Attack SPARSE2 at m = guarantee(n) exactly; every returned x is re-summed over the original
columns (S5.unwind asserts x != 0, x in S^m, lam x = 0).  Families: random; simplex blocks
(dependency code of each block = simplex code S_r, r = 2, 3, the worst case for the averaging
step); series classes; weight-2 signed; few-distinct columns; low rank + random; and a
consumption-maximising hill climb at small n.  /opt/anaconda3/bin/python -I test_sparse2.py
"""
import itertools, os, sys, time
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import sparse2 as SP   # noqa: E402
S5 = SP.S5
p = 5
rng = np.random.default_rng(2026_11_11)


def rand_gl(n):
    while True:
        A = rng.integers(0, p, size=(n, n))
        if S5.nullspace(A).shape[0] == 0:
            return A


def simplex_block(r):
    """columns v_1..v_N (N = 5^r - 1) in F_5^(N-r) whose dependency code is the simplex code:
    the generator G (r x N, all nonzero columns) spans D; columns = basis of the dual's dual."""
    G = np.array([v for v in itertools.product(range(p), repeat=r) if any(v)], dtype=np.int64).T
    Vt = S5.nullspace(G)            # (N-r) x N, rows span G-perp; columns v_i: Vt[:, i]
    assert Vt.shape[0] == G.shape[1] - r
    return Vt


def fam_random(n, M):
    return rng.integers(0, p, size=(n, M))


def fam_simplex(n, M, r):
    cols = []; c0 = 0
    B = simplex_block(r); k = B.shape[0]
    while len(cols) < M and c0 + k <= n:
        perm = rng.permutation(B.shape[1])
        for i in perm:
            v = np.zeros(n, dtype=np.int64); v[c0:c0 + k] = B[:, i]; cols.append(v)
        c0 += k
    while len(cols) < M:
        cols.append(rng.integers(0, p, size=n))
    lam = np.array(cols[:M]).T % p
    return (rand_gl(n) @ lam) % p


def fam_simplex_mixed(n, M, r):
    """simplex blocks laid over overlapping random coordinates (not a direct sum)."""
    B = simplex_block(r); k = B.shape[0]
    cols = []
    while len(cols) < M:
        if k <= n:
            E = rng.integers(0, p, size=(n, k))      # random embedding F_5^k -> F_5^n
            for i in rng.permutation(B.shape[1]):
                cols.append((E @ B[:, i]) % p)
        else:
            cols.append(rng.integers(0, p, size=n))
    return np.array(cols[:M]).T % p


def fam_series(n, M, size=4):
    cols = []; c0 = 0
    while len(cols) < M:
        if c0 + size - 1 <= n:
            sc = rng.integers(1, p, size=size)
            vs = [np.zeros(n, dtype=np.int64) for _ in range(size)]
            for j in range(size - 1):
                vs[j][c0 + j] = 1
            vs[-1][c0:c0 + size - 1] = 1
            for j in range(size):
                vs[j] = (vs[j] * sc[j]) % p
            cols.extend(vs); c0 += size - 1
        else:
            cols.append(rng.integers(0, p, size=n))
    lam = np.array(cols[:M]).T % p
    return (rand_gl(n) @ lam) % p


def fam_weight2(n, M):
    cols = []
    for _ in range(M):
        v = np.zeros(n, dtype=np.int64)
        i, j = rng.choice(n, 2, replace=False)
        v[i] = rng.integers(1, p); v[j] = rng.integers(1, p)
        cols.append(v)
    return np.array(cols).T % p


def fam_fewdistinct(n, M):
    base = rng.integers(0, p, size=(n, max(2, n // 2)))
    return np.array([(rng.integers(1, p) * base[:, rng.integers(base.shape[1])]) % p for _ in range(M)]).T


def fam_lowrank(n, M):
    k = max(2, n // 3)
    E = rng.integers(0, p, size=(n, k))
    a = [(E @ rng.integers(0, p, size=k)) % p for _ in range(M // 2)]
    b = [rng.integers(0, p, size=n) for _ in range(M - M // 2)]
    cols = a + b
    rng.shuffle(cols)
    return np.array(cols).T % p


def run(lam):
    log = []
    x = SP.solve(lam, log=log)
    return x, log


def main():
    t0 = time.time()
    fams = {'random': fam_random,
            'simplex2': lambda n, M: fam_simplex(n, M, 2),
            'simplex3': lambda n, M: fam_simplex(n, M, 3),
            'simplex2mix': lambda n, M: fam_simplex_mixed(n, M, 2),
            'simplex3mix': lambda n, M: fam_simplex_mixed(n, M, 3),
            'series4': fam_series, 'weight2': fam_weight2,
            'fewdistinct': fam_fewdistinct, 'lowrank': fam_lowrank}
    print('A. families at m = guarantee(n) exactly (failures would print FAIL)')
    fails = 0; runs = 0; ratios = []
    for n in (6, 9, 12, 16, 20, 25, 30, 40, 50):
        m = SP.guarantee(n)
        line = []
        for name, f in fams.items():
            for rep in range(2 if n >= 40 else 3):
                lam = f(n, m) % p
                x, log = run(lam)
                runs += 1
                if x is None:
                    fails += 1; line.append(name + ':FAIL')
                    continue
                used = sum(c for _, _, c, _ in log)
                for q, r, c, cb in log:
                    if q >= 20:
                        ratios.append((q, r, c, cb))
                line.append('%s:%d' % (name, used))
        print('n=%d m=%d (B\' %d) consumed ' % (n, m, S5.guarantee_simple(n)) + ' '.join(line), flush=True)
    print('runs', runs, 'failures', fails)
    if ratios:
        ar = np.array([c / q for q, r, c, cb in ratios]); slack = [cb - c for q, r, c, cb in ratios]
        print('pieces with q>=20: %d, cost/q mean %.4f max %.4f, min slack to bound %d (q,r,c,bound worst: %s)'
              % (len(ratios), ar.mean(), ar.max(), min(slack), max(ratios, key=lambda t: t[2] - t[3])))

    print('B. simplex-block piece costs: the first piece of a pure simplex3 instance at q = 121')
    lam = (rand_gl(121) @ simplex_block(3)) % p
    lam = np.concatenate([lam, rng.integers(0, p, size=(121, SP.guarantee(121) - lam.shape[1]))], axis=1)
    log = []
    x = SP.solve(lam, log=log)
    print('  solved:', x is not None, ' first stages (q, r, |Y|, bound):', log[:3])

    print('C. hill climb (maximise consumed columns), n = 8, 10, 12 at m = guarantee(n)')
    for n in (8, 10, 12):
        m = SP.guarantee(n)
        best = None
        for start in range(4):
            lam = fam_random(n, m)
            x, log = run(lam); assert x is not None
            score = sum(c for _, _, c, _ in log)
            for it in range(150):
                lam2 = lam.copy()
                for _ in range(rng.integers(1, 4)):
                    lam2[:, rng.integers(m)] = rng.integers(0, p, size=n)
                x2, log2 = run(lam2)
                if x2 is None:
                    print('  FAIL at n=%d' % n); fails += 1; break
                s2 = sum(c for _, _, c, _ in log2)
                if s2 >= score:
                    lam, score = lam2, s2
            best = score if best is None else max(best, score)
        print('  n=%d m=%d max consumed by pieces %d (pool needs m-1=%d at most)' % (n, m, best, m - 1), flush=True)
    print('total failures', fails, 'time %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
