"""v2: independent end-to-end executor of Lemmas T_l and W_l (fragment-v2.tex) with the l-level
tables of 2026-11-13-rees-k9-below-21 (read-only).  Written from the lemma statements; shares no code
with that folder's tensor_exec.py.  No early exit: the full level-l object is always built; dependences are random elements of the
null space, and in 'uniform' runs sub-objects with vanishing off-zero part are discarded, so the
table is exercised on every cell with T_y != 0 (counted in the output).  Output check: x_b = C_y w_b, x != 0, every nonzero
x_b a kappa-th power, sum_b x_b lambda_b = 0 (exact, mod p).  Finite falsifier only.
Usage: nice -n 19 python v2/ell_exec.py"""
import json, os, sys, itertools, random
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from certs import prim_root
SRC = os.path.join(HERE, '..', '..', '2026-11-13-rees-k9-below-21')
RNG = random.Random(2026)

def nullvec(V, p):
    """V: n x m int array (n > m rows = vectors); returns nonzero theta (len n) with theta V = 0 mod p."""
    n, m = V.shape
    A = np.concatenate([V.T % p, np.zeros((m, 0), dtype=np.int64)], axis=1)   # m x n, columns = vectors
    A = A.astype(np.int64); piv = []; r = 0
    for c in range(n):
        if r == m: break
        rows = np.nonzero(A[r:, c])[0]
        if len(rows) == 0: continue
        i = r + rows[0]; A[[r, i]] = A[[i, r]]
        A[r] = A[r] * pow(int(A[r, c]), p - 2, p) % p
        f = A[:, c].copy(); f[r] = 0
        A = (A - np.outer(f, A[r])) % p
        piv.append(c); r += 1
    frees = [c for c in range(n) if c not in piv]
    th = np.zeros(n, dtype=np.int64)
    for c in frees:                      # random element of the null space (any nonzero one is allowed)
        t = RNG.randrange(p)
        th[c] = (th[c] + t) % p
        for i, pc in enumerate(piv): th[pc] = (th[pc] - t * A[i, c]) % p
    if not th.any():
        c = frees[0]; th[c] = 1
        for i, pc in enumerate(piv): th[pc] = (-A[i, c]) % p
    return th

class Obj:   # level-t object: cells[y] = list of (b, w_b); T[y] = sum w_b lambda_b
    __slots__ = ('cells', 'T')

def build(src, a, k, l, p, ind, z, forced):
    """Lemma T_l on columns drawn from src (src.take(n) -> list of indices into src.lam); returns an Obj.
    forced: sub-objects whose off-zero vector (T_y, y without zero coordinate) vanishes are discarded and
    replaced by new ones on fresh columns, so that the level-l object has T != 0 and the table is used."""
    if l == 1:
        idx = src.take(a + 1); lam = src.lam
        th = nullvec(lam[idx], p) if a > 0 else np.array([1] + [0] * (len(idx) - 1))
        s = next(i for i in range(len(th)) if th[i]); th = th * pow(int(th[s]), p - 2, p) % p
        o = Obj(); o.cells = {(m,): [] for m in range(k)}; o.T = {(m,): np.zeros(a, dtype=np.int64) for m in range(k)}
        for i, c in enumerate(th):
            c = int(c)
            if not c: continue
            m = ind[c]; w = c * pow(z[m], p - 2, p) % p
            o.cells[(m,)].append((idx[i], w)); o.T[(m,)] = (o.T[(m,)] + w * lam[idx[i]]) % p
        return o
    N = (k - 1) ** (l - 1) * a + 1
    offz = list(itertools.product(range(1, k), repeat=l - 1))
    lam = src.lam
    objs = []
    while len(objs) < N:
        o1 = build(src, a, k, l - 1, p, ind, z, forced)
        if forced and not any(o1.T[y].any() for y in offz): src.discarded += 1; continue
        objs.append(o1)
    V = np.array([np.concatenate([o.T[y] for y in offz]) if a > 0 else np.zeros(0, dtype=np.int64) for o in objs], dtype=np.int64)
    th = nullvec(V, p) if a > 0 else np.array([1] + [0] * (N - 1))
    s = next(i for i in range(N) if th[i]); th = th * pow(int(th[s]), p - 2, p) % p
    o = Obj(); keys = list(itertools.product(range(k), repeat=l))
    o.cells = {y: [] for y in keys}; o.T = {y: np.zeros(a, dtype=np.int64) for y in keys}
    for t, mu in enumerate(objs):
        c = int(th[t])
        if not c: continue
        j = ind[c]; wp = c * pow(z[j], p - 2, p) % p
        for y in mu.cells:
            Y = y + (j,)
            o.cells[Y].extend((b, wp * w % p) for b, w in mu.cells[y])
            o.T[Y] = (o.T[Y] + wp * mu.T[y]) % p
    # assert every axis relation
    for r in range(l):
        for rest in itertools.product(range(k), repeat=l - 1):
            acc = np.zeros(a, dtype=np.int64)
            for m in range(k):
                y = rest[:r] + (m,) + rest[r:]
                acc = (acc + z[m] * o.T[y]) % p
            assert not acc.any(), ('axis relation fails', l, r)
    return o

def run(p, k, tabfile, a, rng, kind='uniform'):
    tab = json.load(open(os.path.join(SRC, tabfile))); l = len(next(iter(tab)))
    g = prim_root(p); z = [pow(g, m, p) for m in range(k)]
    ind = {}
    x = 1
    for e in range(p - 1):
        ind[x] = e % k; x = x * g % p
    M = 1
    for t in range(l): M *= (k - 1) ** t * a + 1
    class Src:
        def __init__(self):
            self.n = 0; self.discarded = 0; self.base = np.array([rng.randrange(p) for _ in range(a)], dtype=np.int64)
            self.lam = np.zeros((1024, a), dtype=np.int64); self.rs = np.random.default_rng(rng.randrange(2 ** 32))
        def take(self, m):
            while self.n + m > len(self.lam):
                self.lam = np.concatenate([self.lam, np.zeros_like(self.lam)])
            if kind == 'uniform': blk = self.rs.integers(0, p, size=(m, a))
            else: blk = np.where(self.rs.random((m, 1)) < .5, self.base[None, :], 0)
            self.lam[self.n:self.n + m] = blk
            i0 = self.n; self.n += m
            return list(range(i0, i0 + m))
    src = Src()
    o = build(src, a, k, l, p, ind, z, forced=(kind == 'uniform'))
    lam = src.lam; M = src.n
    x = {}
    for key, bval in tab.items():
        y = tuple(int(c) for c in key); C = pow(g, sum(y), p) * int(bval) % p
        for b, w in o.cells[y]:
            if C * w % p: x[b] = C * w % p
    tot = np.zeros(a, dtype=np.int64)
    for b, v in x.items(): tot = (tot + v * lam[b]) % p
    ok = bool(x) and not tot.any() and all(pow(v, (p - 1) // k, p) == 1 for v in x.values())
    used = sum(1 for y in o.cells if o.T[y].any())
    return ok, len(x), M, used, src.discarded

if __name__ == '__main__':
    rng = random.Random(11)
    plan = [(13, 4, 'B3_13_4.json', (1, 2, 3)), (13, 6, 'B3_13_6.json', (1, 2, 3)),
            (19, 9, 'B4_19.json', (1,)), (37, 9, 'B4_37.json', (1,)), (73, 9, 'B4_73.json', (1,))]
    for p, k, f, As in plan:
        for a in As:
            for kind in ('uniform', 'degenerate'):
                res = [run(p, k, f, a, rng, kind) for _ in range(2 if k == 9 else 5)]
                print(f'{f} p={p} k={k} a={a} {kind}: ok {sum(r[0] for r in res)}/{len(res)}; columns {[r[2] for r in res]}, '
                      f'support {[r[1] for r in res]}, cells with T!=0 {[r[3] for r in res]}, discarded {[r[4] for r in res]}', flush=True)
    print('negative controls (perturbed tables; uniform banks):')
    for p, k, f, a in [(13, 4, 'B3_13_4_perturbed.json', 2), (13, 6, 'B3_13_6_perturbed.json', 2), (37, 9, 'B4_37_perturbed.json', 1)]:
        res = [run(p, k, f, a, rng) for _ in range(3 if k < 9 else 2)]
        print(f'  {f}: ok {sum(r[0] for r in res)}/{len(res)} (must be 0)', flush=True)
