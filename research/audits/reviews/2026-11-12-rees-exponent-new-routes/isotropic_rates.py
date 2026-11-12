"""Stage-2 multi-output rate on random labels (finite checks only).
For uniform labels lambda_1..lambda_M in F_p^a compute
  r_max = max dim of a subspace W of F_p^M totally isotropic for
          q(w) = sum_i w_i^2 lambda_i   (multi-output merge, Theorem MO2),
  r_dec = max number of pairwise disjoint supports of isotropic vectors
          (= best set of disjoint single-output merges),
  ub    = floor((M + z)/2), z = min_{mu != 0} #{i : mu.lambda_i = 0}
          (Witt bound applied to the single form sum_i (mu.lambda_i) w_i^2)."""
import itertools, sys
import numpy as np
from lie import rank_mod

rng = np.random.default_rng(7)

def analyse(p, a, M, lam):
    vecs = np.array(list(itertools.product(range(p), repeat=M)), dtype=np.int64)
    qv = ((vecs ** 2) @ lam) % p
    iso = vecs[np.all(qv == 0, axis=1) & vecs.any(axis=1)]
    reps = {}
    for w in iso:
        nz = int(w[np.nonzero(w)[0][0]])
        wn = tuple(int(x) for x in (w * pow(nz, -1, p)) % p)
        reps[wn] = True
    reps = [np.array(w) for w in reps]
    # r_dec: set packing of supports
    supp = set()
    for w in reps:
        supp.add(frozenset(np.nonzero(w)[0].tolist()))
    best = {frozenset(): 0}
    # DP over used-coordinate sets
    from functools import lru_cache
    supps = sorted(supp, key=len)
    @lru_cache(None)
    def pack(used):
        b = 0
        for s in supps:
            if not (s & used):
                b = max(b, 1 + pack(used | s))
        return b
    r_dec = pack(frozenset())
    # ub (Witt bound, Lemma W)
    z = M
    for mu in itertools.product(range(p), repeat=a):
        if any(mu):
            z = min(z, int(np.sum((lam @ np.array(mu)) % p == 0)))
    ub = (M + z) // 2
    # r_max via DFS (stops early once the Witt bound is reached)
    B = lambda x, y: ((x * y) @ lam) % p
    r_max = 0
    stop = min(ub, M)
    def dfs(basis, cands):
        nonlocal r_max
        r_max = max(r_max, len(basis))
        if r_max >= stop:
            return
        for k, w in enumerate(cands):
            if basis and rank_mod(np.vstack(basis + [w]), p) <= len(basis):
                continue
            nb = basis + [w]
            nc = [u for u in cands[k + 1:] if not B(u, w).any()]
            dfs(nb, nc)
            if r_max >= stop:
                return
    dfs([], reps)
    return r_max, r_dec, ub

if __name__ == "__main__":
    cases = [(5, 1, 5), (7, 1, 5), (5, 2, 5), (5, 2, 6), (7, 2, 6), (5, 2, 7), (11, 2, 5), (5, 3, 7), (7, 3, 7)]
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    for (p, a, M) in cases:
        hist = {}; viol = 0; gain = 0
        for t in range(trials):
            lam = rng.integers(0, p, size=(M, a))
            r_max, r_dec, ub = analyse(p, a, M, lam)
            hist[(r_max, r_dec)] = hist.get((r_max, r_dec), 0) + 1
            viol += r_max > ub
            gain += r_max > r_dec
        print(f"p={p} a={a} M={M} trials={trials}: (r_max,r_dec) histogram {dict(sorted(hist.items()))}; "
              f"r_max>r_dec in {gain}; Witt-bound violations {viol}")
