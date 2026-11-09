"""Lemma 6.1 of 2026-11-08-rees-sde-p3.md assumes the fraction rho of coordinates of F' whose
functional on A is proportional to another one is o(1) on random pools.  For KOW's own space
A = D(F), |F| = q + r, r = ceil(log_3(q+1)), the coordinate functionals are q + r vectors in
F_3^r, i.e. at most (3^r - 1)/2 projective classes, so rho is bounded below by a constant.
Also: the spread of weights over all of A, min vs mean."""
import math, itertools
import numpy as np
from nested_sampler import kernel

rng = np.random.default_rng(1)
for q in (20, 60, 120, 240):
    r = max(1, math.ceil(math.log(q + 1, 3) - 1e-12))
    rhos = []; gaps = []
    for _ in range(10):
        M = rng.integers(0, 3, (q, q + r))
        B = kernel(M)                         # rows = basis of D(F), dim >= r
        rows = B.T % 3                        # coordinate functionals
        def canon(v):
            v = tuple(int(x) for x in v)
            if not any(v): return None
            f = next(x for x in v if x); return tuple((x * f) % 3 for x in v)  # scale so first nonzero = 1
        cl = {}
        for i, v in enumerate(rows):
            c = canon(v)
            if c is not None: cl.setdefault(c, []).append(i)
        prop = sum(len(v) for v in cl.values() if len(v) > 1)
        nzc = sum(len(v) for v in cl.values())
        rhos.append(prop / nzc)
        k = B.shape[0]
        W = [int(np.count_nonzero((np.array(c) @ B) % 3)) for c in itertools.product(range(3), repeat=k) if any(c)]
        gaps.append((np.mean(W) - min(W)) / math.sqrt(q))
    print(f"q={q:4d} r={r}: fraction of nonzero coordinates proportional to another: mean {np.mean(rhos):.3f}; "
          f"(mean weight - min weight)/sqrt(q) over all of A: mean {np.mean(gaps):.2f}")
print("(log2 3 - 1)/3 =", (math.log2(3) - 1) / 3)
