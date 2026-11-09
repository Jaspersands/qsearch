"""Adversarial instances for WNEST over F_5 (wnest_p.solve): structured families and a hill climb.
Every invariant used by the proof is asserted inside wnest_p (wt >= r*+3, |wt - mu N*| <= sigma,
dim D(X) >= 3, >= 4 labels, gadget exists); every witness is re-summed here."""
import sys, math, itertools, time
import numpy as np
from wnest_p import solve, guarantee, GADGET_CACHE, INFEASIBLE
from sparse_tri import Field

rng = np.random.default_rng(55)
p = 5
F = Field(p, 2)


def fam(name, n, M):
    if name == 'random':
        return rng.integers(0, p, size=(n, M))
    if name == 'chain3':        # series classes of size 3: blocks of 3 columns proportional mod the rest
        base = rng.integers(0, p, size=(n, M))
        for j in range(0, M - 2, 3):
            base[:, j + 1] = (2 * base[:, j]) % p
            base[:, j + 2] = (3 * base[:, j]) % p
        return base
    if name == 'chain4':
        base = rng.integers(0, p, size=(n, M))
        for j in range(0, M - 3, 4):
            for t in range(1, 4):
                base[:, j + t] = ((t + 1) * base[:, j]) % p
        return base
    if name == 'dup':           # every column duplicated
        half = rng.integers(0, p, size=(n, (M + 1) // 2))
        return np.repeat(half, 2, axis=1)[:, :M]
    if name == 'blocks3':       # three blocks whose sums are proportional (the k = 2 degenerate structure)
        lam = rng.integers(0, p, size=(n, M))
        u = rng.integers(0, p, size=n)
        for b, mult in zip(range(3), (1, 1, 3)):
            cols = range(b, M, 3)
            s = lam[:, list(cols)[:-1]].sum(axis=1) % p
            lam[:, list(cols)[-1]] = (mult * u - s) % p
        return lam
    if name == 'two_values':    # columns from {u, 2u} + small noise subspace: dependencies take few values
        B = rng.integers(0, p, size=(n, 3))
        return (B @ rng.integers(0, p, size=(3, M))) % p
    if name == 'lowrank':
        B = rng.integers(0, p, size=(n, max(2, n // 3)))
        return (B @ rng.integers(0, p, size=(B.shape[1], M))) % p
    if name == 'sparse':
        return (rng.integers(0, p, size=(n, M)) * (rng.random((n, M)) < 0.1)) % p
    if name == 'proj':          # projective columns: first nonzero entry 1
        lam = rng.integers(0, p, size=(n, M))
        for j in range(M):
            nz = np.nonzero(lam[:, j])[0]
            if len(nz):
                lam[:, j] = (lam[:, j] * pow(int(lam[nz[0], j]), -1, p)) % p
        return lam
    if name == 'signed_blocks': # columns +-e_i and +-(e_i + e_j)
        cols = []
        for j in range(M):
            v = np.zeros(n, dtype=np.int64)
            i1, i2 = rng.integers(0, n, size=2)
            v[i1] = rng.choice([1, 4]); v[i2] = (v[i2] + rng.choice([0, 1, 4])) % p
            cols.append(v)
        return np.array(cols).T
    if name == 'weightgap':     # block-diagonal pools
        lam = np.zeros((n, M), dtype=np.int64)
        for j in range(M):
            b = j % 3
            lo, hi = b * n // 3, (b + 1) * n // 3
            lam[lo:hi, j] = rng.integers(0, p, size=hi - lo)
        return lam
    raise ValueError(name)


def run_instance(lam):
    log = []
    x = solve(F, lam.astype(np.int64), log=log)
    assert x is not None
    assert x.any() and all(int(v) in F.S for v in x) and not ((lam @ x) % p).any()
    return sum(e[4] for e in log), max((e[4] - e[0] for e in log if e[5]), default=0)


print('A. structured families at n = 30, M = guarantee(30) =', guarantee(p, 30)[0])
fams = ['random', 'chain3', 'chain4', 'dup', 'blocks3', 'two_values', 'lowrank', 'sparse', 'proj', 'signed_blocks', 'weightgap']
for name in fams:
    M = guarantee(p, 30)[0]
    used, excess = [], []
    for t in range(4):
        u, e = run_instance(fam(name, 30, M))
        used.append(u); excess.append(e)
    print(f'  {name:14s}: columns consumed {min(used)}..{max(used)}; max per-piece |X| - q = {max(excess)}; infeasible label sets so far {len(INFEASIBLE)}', flush=True)

print('B. hill climb on the columns consumed, n = 8..14, M = guarantee(n)')
for n in (8, 10, 12, 14):
    M = guarantee(p, n)[0]
    lam = rng.integers(0, p, size=(n, M)).astype(np.int64)
    best, _ = run_instance(lam)
    t0 = time.time()
    steps = 0
    while time.time() - t0 < 60:
        cand = lam.copy()
        j = rng.integers(0, M)
        if rng.random() < 0.5:
            cand[:, j] = rng.integers(0, p, size=n)
        else:
            cand[:, j] = cand[:, rng.integers(0, M)]
        try:
            u, _ = run_instance(cand)
        except AssertionError as ex:
            print('  ASSERTION FAILURE (proof invariant violated):', ex)
            raise
        steps += 1
        if u >= best:
            best, lam = u, cand
    print(f'  n={n}: guarantee {M}; max columns consumed after {steps} climb steps: {best}; infeasible label sets {len(INFEASIBLE)}', flush=True)
print('gadget cache size', len(GADGET_CACHE), 'infeasible', INFEASIBLE[:3])
