"""Sampled check of Lemma J at p = 5: if X has k >= 2 independent dependencies, >= 4 genuine
D(X)-classes and a full-support codeword delta that is not constant, then some delta' in D(X)
gives >= 4 distinct joint labels (delta_i, delta'_i).  Exhaustive over delta' for each sampled D(X)."""
import itertools, numpy as np
from verify_gadget import rank_mod
rng = np.random.default_rng(7)
p = 5
checked = fails = 0
for k in (2, 3, 4):
    for c in range(k + 2, k + 6):
        for _ in range(3000):
            D = rng.integers(0, p, size=(k, c)).astype(np.int64)
            cols = [tuple(D[:, j]) for j in range(c)]
            if len(set(cols)) < c or any(not any(v) for v in cols) or rank_mod(D, p) < k:
                continue
            codewords = [(np.array(x) @ D) % p for x in itertools.product(range(p), repeat=k) if any(x)]
            fulls = [d for d in codewords if d.all() and len(set(d.tolist())) >= 2]
            for delta in fulls[:5]:
                checked += 1
                ok = any(rank_mod(np.vstack([delta, d2]), p) == 2 and len({(int(a), int(b)) for a, b in zip(delta, d2)}) >= 4
                         for d2 in codewords)
                if not ok:
                    fails += 1
                    print('COUNTEREXAMPLE', D, delta)
print(f'Lemma J sampled check at p=5: {checked} (D(X), delta) pairs with >= 4 classes, failures {fails}')
