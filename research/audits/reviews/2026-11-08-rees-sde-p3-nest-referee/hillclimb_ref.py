"""Hill climb over whole instances (m = ceil(theorem bound)) maximizing columns pulled by WNEST."""
import math, sys
import numpy as np
from wnest_ref import WNEST, Fail, theorem_bound, guarantee
rng = np.random.default_rng(5)
def score(vecs):
    W = WNEST(vecs)
    S = W.run()       # Fail would propagate: a refutation
    assert not np.any(sum((vecs[i] for i in S), np.zeros(len(vecs[0]), dtype=np.int64)) % 3)
    return W.pulled
print(" n   m   guarantee  start            best pulled  steps")
for n in [int(x) for x in sys.argv[1:]] or [6, 7, 8, 10]:
    m = math.ceil(theorem_bound(n)); g = guarantee(n)
    for start in ("random", "dup"):
        vecs = [rng.integers(0, 3, n) for _ in range(m)]
        if start == "dup":
            vecs = [vecs[i // 2] for i in range(m)]
        best = score(vecs); steps = 1500
        for it in range(steps):
            cand = list(vecs)
            for _ in range(int(rng.integers(1, 4))):
                i = int(rng.integers(0, best + 1)) if best < m else int(rng.integers(0, m))
                i = min(i, m - 1); r = rng.random()
                if r < 0.4:
                    cand[i] = rng.integers(0, 3, n)
                elif r < 0.7:
                    j, k = rng.integers(0, m, 2); cand[i] = (cand[j] + cand[k]) % 3
                else:
                    j = int(rng.integers(0, m)); cand[i] = (int(rng.integers(1, 3)) * cand[j]) % 3
                if not np.any(cand[i]):
                    cand[i] = rng.integers(0, 3, n)
            s = score(cand)
            if s >= best:
                best, vecs = s, cand
        assert best <= g
        print(f"{n:2d} {m:4d}  {g:6d}     {start:8s}        {best:6d}     {steps}"); sys.stdout.flush()
print("no failure; every witness verified")
