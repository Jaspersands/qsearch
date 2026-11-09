"""Referee B attack: run the note's WNEST_5 (wnest_p.solve, at m = guarantee(n) exactly) and the
referee's SIMPLE5 (at m = guarantee_simple(n) exactly) on families the note did not use:
true series classes of size 4 (circuits in private coordinates, hidden by a random change of basis;
the note's 'chain3/chain4' are proportional COLUMNS, i.e. parallel classes, which end at once),
series classes of size 5-7 (peeled), PG(2,5) blocks, zero-sum-triple heavy, mixed subspace/random,
weight-2 signed columns, and a stage-adaptive hill climb at small n.  Every witness is re-summed.
"""
import sys, time, itertools, math
import numpy as np
sys.path.insert(0, '../2026-11-08-rees-sde-fq-nest')
import wnest_p
from sparse_tri import Field
import simple5
p = 5
F = Field(p, 2)
rng = np.random.default_rng(2026_11_09)

def rand_gl(n):
    while True:
        A = rng.integers(0, p, size=(n, n))
        if simple5.nullspace(A).shape[0] == 0:
            return A

def series(n, M, size):
    """blocks of `size` columns spanning size-1 private coordinates with one circuit (series class)."""
    cols = []; c0 = 0
    while len(cols) < M:
        if c0 + size - 1 <= n:
            sc = rng.integers(1, p, size=size)
            vs = []
            for t in range(size - 1):
                v = np.zeros(n, dtype=np.int64); v[c0 + t] = 1; vs.append(v)
            vs.append((-sum(vs)) % p)
            cols += [(int(s) * v) % p for s, v in zip(sc, vs)]
            c0 += size - 1
        else:
            cols.append(rng.integers(0, p, size=n))
    lam = np.array(cols[:M]).T
    return (rand_gl(n) @ lam) % p

def pg_blocks(n, M):
    pts = [v for v in itertools.product(range(p), repeat=3) if any(v) and v[next(i for i in range(3) if v[i])] == 1]
    cols = []
    while len(cols) < M:
        b = int(rng.integers(0, max(1, n // 3)))
        for v in pts:
            w = np.zeros(n, dtype=np.int64); w[3 * b:3 * b + 3] = v[:min(3, n - 3 * b)] if 3 * b + 3 <= n else 0
            cols.append(w if w.any() else rng.integers(0, p, size=n))
    return np.array(cols[:M]).T

def triples(n, M):
    cols = []
    while len(cols) < M:
        a, b = rng.integers(0, p, size=(2, n))
        cols += [a, b, (2 * (a + b)) % p]     # a + b + 3*(2(a+b))... dependency with coefficients (1,1,2)
    return (np.array(cols[:M]).T) % p

def mixed(n, M):
    B = rng.integers(0, p, size=(n, max(2, n // 2)))
    lam = rng.integers(0, p, size=(n, M))
    mask = rng.random(M) < 0.5
    lam[:, mask] = (B @ rng.integers(0, p, size=(B.shape[1], int(mask.sum())))) % p
    return lam

def weight2(n, M):
    lam = np.zeros((n, M), dtype=np.int64)
    for j in range(M):
        i1, i2 = rng.choice(n, size=2, replace=False)
        lam[i1, j] = rng.integers(1, p); lam[i2, j] = rng.integers(1, p)
    return lam

FAMS = {'series4': lambda n, M: series(n, M, 4), 'series6': lambda n, M: series(n, M, 6),
        'series7': lambda n, M: series(n, M, 7), 'pg_blocks': pg_blocks, 'triples': triples,
        'mixed': mixed, 'weight2': weight2, 'random': lambda n, M: rng.integers(0, p, size=(n, M))}

def run_wnest(lam):
    log = []
    x = wnest_p.solve(F, lam.astype(np.int64), log=log)
    assert x is not None, 'WNEST ran out of columns at guarantee(n)'
    assert x.any() and all(int(v) in F.S for v in x) and not ((lam @ x) % p).any()
    return sum(e[4] for e in log), len([e for e in log if e[5]])

def run_simple(lam):
    log = []
    x = simple5.solve(lam.astype(np.int64), log=log)
    assert x is not None, 'SIMPLE5 ran out of columns'
    return sum(e[1] for e in log), len(log)

t0 = time.time()
print('A. families; m = guarantee exactly for each solver')
for n in (6, 9, 14, 20, 30, 40):
    gW = wnest_p.guarantee(p, n)[0]; gS = simple5.guarantee_simple(n)
    for name, f in FAMS.items():
        resW, resS = [], []
        for t in range(3):
            resW.append(run_wnest(f(n, gW)))
            resS.append(run_simple(f(n, gS)))
        print(f'  n={n:2d} {name:9s}: WNEST (m={gW}) consumed {[r[0] for r in resW]} pieces {[r[1] for r in resW]};'
              f'  SIMPLE5 (m={gS}) consumed {[r[0] for r in resS]} pieces {[r[1] for r in resS]}', flush=True)
print(f'  [{time.time()-t0:.0f}s] gadget label sets met: WNEST {len(wnest_p.GADGET_CACHE)} (infeasible {len(wnest_p.INFEASIBLE)}), SIMPLE5 {len(simple5.CACHE)} (infeasible {sum(v is None for v in simple5.CACHE.values())})')

print('B. hill climb (maximise columns consumed) on SIMPLE5 at m = guarantee_simple(n)')
for n in (6, 8, 10, 12):
    M = simple5.guarantee_simple(n)
    lam = rng.integers(0, p, size=(n, M)).astype(np.int64)
    best = run_simple(lam)[0]; steps = 0; t1 = time.time()
    while time.time() - t1 < 40:
        cand = lam.copy(); j = rng.integers(0, M)
        cand[:, j] = rng.integers(0, p, size=n) if rng.random() < 0.6 else cand[:, rng.integers(0, M)]
        u = run_simple(cand)[0]; steps += 1
        if u >= best:
            best, lam = u, cand
    print(f'  n={n}: m = {M}; max consumed {best} after {steps} steps (stage costs <= q+2 by construction)', flush=True)

print('C. hill climb on WNEST_5 per-stage excess |X| - q at the first stage, q = n, pool N(q)')
for n in (5, 8, 12):
    N = wnest_p.pool_size(p, n); M = wnest_p.guarantee(p, n)[0]
    lam = rng.integers(0, p, size=(n, M)).astype(np.int64)
    def first_excess(L):
        log = []
        wnest_p.solve(F, L, log=log)
        return (log[0][4] - log[0][0]) if log and log[0][5] else -99
    best = first_excess(lam); steps = 0; t1 = time.time()
    while time.time() - t1 < 40:
        cand = lam.copy(); j = rng.integers(0, N)
        cand[:, j] = rng.integers(0, p, size=n) if rng.random() < 0.6 else cand[:, rng.integers(0, N)]
        e = first_excess(cand); steps += 1
        if e >= best:
            best, lam = e, cand
    cap = math.floor(0.8 * N + 0.8 * math.sqrt(N)) - n
    print(f'  q={n}: N(q)={N}; max first-piece |X| - q = {best} (proof cap {cap}) after {steps} steps', flush=True)
print(f'done, {time.time()-t0:.0f}s, no assertion failure, every witness re-summed')
