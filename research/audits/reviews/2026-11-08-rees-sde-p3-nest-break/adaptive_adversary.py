"""Stage-adaptive adversary against WNEST (proof variant), strict asserts on.

The algorithm is deterministic and the pool at each stage is the first N(q) unconsumed columns.
An adaptive adversary therefore controls the FRESH columns of every pool (the returned columns
are fixed by the past).  At each stage we hill-climb the fresh columns to maximise the piece cost
|X| = wt (never letting the stage terminate early with a zero-sum set, which would end the game),
commit the piece, and continue.  The resulting m_needed is compared with guarantee(n), the exact
value of the proof's recursion; m_needed > guarantee(n) would refute Theorem A's accounting (a
per-piece cap would have to fail, which the asserts would catch first).  Every final witness is
verified by summation.
"""
import math, sys, time
import numpy as np
from multiprocessing import Pool
from strict_wnest import StrictRun, Fail, guarantee, closed_form, pool_size, piece_cap, rank, kernel, \
    peel_strict, pick_codeword_strict

def stage_cost(n, vecs_prefix, fresh, gens, pool_idx):
    """Simulate one WNEST stage on pool = pool_idx (indices into vecs_prefix+fresh).  Returns
    (wt, terminated) where terminated means a zero-sum finish would happen."""
    vecs = vecs_prefix + fresh
    q = n - len(gens)
    P = kernel(np.array(gens, dtype=np.int64)) if gens else np.eye(n, dtype=np.int64)
    M = (P @ np.array([vecs[i] for i in pool_idx]).T) % 3
    if any(not np.any(M[:, j]) for j in range(M.shape[1])):
        return -1, True
    stats = {}
    idx, B, trace = peel_strict(M, stats)
    delta, wt, var27 = pick_codeword_strict(B)
    Xloc = np.nonzero(delta)[0]
    MX = M[:, [idx[j] for j in Xloc]]
    BX = kernel(MX)
    dl = delta[Xloc]
    dp = next(row for row in BX if rank(np.vstack([dl, row])) == 2)
    X = [pool_idx[idx[j]] for j in Xloc]
    cls = {}
    for i, col in enumerate(X):
        cls.setdefault((int(dl[i]), int(dp[i])), []).append(col)
    from strict_wnest import UNIONS
    S = lambda sel: (np.sum([vecs[i] for i in sel], axis=0) % 3) if sel else np.zeros(n, dtype=np.int64)
    h1 = S([c for ab in UNIONS[(1, 0)] for c in cls.get(ab, [])])
    h2 = S([c for ab in UNIONS[(0, 1)] for c in cls.get(ab, [])])
    if rank((P @ np.vstack([h1, h2]).T) % 3) < 2:
        return wt, True
    return wt, False

def adaptive(args):
    n, steps_per_stage, seed = args
    rng = np.random.default_rng(seed)
    vecs = []                       # committed columns
    R = StrictRun(n, [], "proof", brute_var=False)
    # we drive the StrictRun manually: feed columns stage by stage
    costs = []
    while True:
        q = n - len(R.gens)
        if q < 4:
            break
        N = pool_size(q)
        pool_fixed = list(R.pool)
        need = N - len(pool_fixed)
        assert need >= 0
        fresh = [rng.integers(0, 3, n) for _ in range(need)]
        base_len = len(vecs)
        pool_idx = pool_fixed + list(range(base_len, base_len + need))
        best = None
        for s in range(steps_per_stage + 1):
            if s == 0:
                cand = fresh
            else:
                cand = [f.copy() for f in fresh]
                k = rng.integers(0, 5)
                j = int(rng.integers(0, need)) if need else 0
                if need == 0:
                    break
                if k == 0: cand[j][int(rng.integers(0, n))] = int(rng.integers(0, 3))
                elif k == 1: cand[j] = rng.integers(0, 3, n)
                elif k == 2:
                    i = int(rng.integers(0, len(pool_idx)))
                    src = (vecs + cand)[pool_idx[i]]; cand[j] = (src * int(rng.integers(1, 3))) % 3
                elif k == 3:
                    i1, i2 = rng.integers(0, len(pool_idx), 2); allv = vecs + cand
                    cand[j] = (int(rng.integers(1, 3)) * allv[pool_idx[i1]] + int(rng.integers(1, 3)) * allv[pool_idx[i2]]) % 3
                else:
                    cand[j] = np.zeros(n, dtype=np.int64); cand[j][int(rng.integers(0, n))] = int(rng.integers(1, 3))
            try:
                wt, term = stage_cost(n, vecs, cand, R.gens, pool_idx)
            except AssertionError as e:
                np.save(f"FAIL_adaptive_n{n}_{seed}.npy", np.array(vecs + cand))
                return dict(n=n, status="ASSERT " + str(e)[:200])
            score = -1 if term else wt
            if best is None or score > best[0]:
                best = (score, cand); fresh = cand
        if best[0] < 0:
            # every tried pool terminates: accept (the adversary cannot avoid it); run one and stop
            pass
        vecs = vecs + fresh
        R.vecs = [np.asarray(v, dtype=np.int64) % 3 for v in vecs]
        P = R.P()
        res = R.wnest_round(q, P)
        costs.append((q, R.costs[-1][2] if R.costs[-1][1] == 2 else R.costs[-1][1], piece_cap(N)))
        if res is not None:
            return dict(n=n, status="finished early", needed=R.m_needed, guar=guarantee(n), costs=costs)
    # finish with KOW rounds on adversarial-ish fresh columns (random)
    extra = [rng.integers(0, 3, n) for _ in range(20)]
    R.vecs = [np.asarray(v, dtype=np.int64) % 3 for v in vecs + extra]
    try:
        sol = R.run()
    except Fail as e:
        return dict(n=n, status="EXHAUSTED " + str(e), needed=R.m_needed, guar=guarantee(n), costs=costs)
    assert R.m_needed <= guarantee(n), ("RECURSION EXCEEDED", R.m_needed, guarantee(n))
    return dict(n=n, status="ok", needed=R.m_needed, guar=guarantee(n), closed=math.ceil(closed_form(n)),
                costs=costs, at_cap=sum(1 for c in costs if c[1] == c[2]), stages=len(costs))

if __name__ == "__main__":
    NS = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [6, 8, 10, 12, 14, 16, 20, 24, 30, 40]
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    t0 = time.time()
    print(f"adaptive adversary, {steps} climb steps per stage; costs = (q, |X|, cap)")
    with Pool(workers) as P:
        for r in P.imap_unordered(adaptive, [(n, steps, 11 * n) for n in NS]):
            print(r); sys.stdout.flush()
    print("total", round(time.time() - t0), "s")
