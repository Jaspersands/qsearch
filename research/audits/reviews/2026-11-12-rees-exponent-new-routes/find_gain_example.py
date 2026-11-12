"""Find and print one explicit instance (p=7, a=2, M=6, all labels nonzero and
pairwise non-proportional) where a totally isotropic 2-plane exists but no two
disjoint supports carry isotropic vectors (r_max = 2 > r_dec = 1). Exact."""
import itertools, numpy as np
from isotropic_rates import analyse
from lie import rank_mod
rng = np.random.default_rng(11)
p, a, M = 7, 2, 6
for t in range(3000):
    lam = rng.integers(0, p, size=(M, a))
    if any(not l.any() for l in lam):
        continue
    if any((lam[i][0]*lam[j][1]-lam[i][1]*lam[j][0]) % p == 0 for i, j in itertools.combinations(range(M), 2)):
        continue
    r_max, r_dec, ub = analyse(p, a, M, lam)
    if r_max > r_dec:
        vecs = np.array(list(itertools.product(range(p), repeat=M)))
        iso = vecs[np.all(((vecs**2) @ lam) % p == 0, axis=1) & vecs.any(axis=1)]
        for w1, w2 in itertools.combinations(iso, 2):
            if not (((w1*w2) @ lam) % p).any() and rank_mod(np.stack([w1, w2]), p) == 2:
                print("labels (rows):", lam.tolist()); print("w1 =", w1.tolist(), " w2 =", w2.tolist())
                print("r_max =", r_max, " r_dec =", r_dec, " Witt bound =", ub, " trial", t)
                break
        break
