"""Rank-1 rate of involution-symmetric index blocks, against the heuristic.  For iota: x -> -x, random a, b, x, y in
F_p^* (all of +-a, +-b, +-x, +-y distinct), the 4x4 block M[s, t] = ind(s - t) mod k over rows (a, -a, b, -b) and
columns (x, -x, y, -y) is rank-1 (M = alpha_s + beta_t) with heuristic probability e_k k^-5 (e_k = 2 for even k,
1 for odd), against k^-9 for a generic block.  Prints observed/heuristic per prime with its Poisson se.
Usage: python block_rate.py k nsamp p [p ...]"""
import sys
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot

k, ns = int(sys.argv[1]), int(sys.argv[2]); e = 2 if k % 2 == 0 else 1
print('  p     lam    4x4 rate/heur (se)   (k=%d, %d samples)' % (k, ns))
for p in [int(v) for v in sys.argv[3:]]:
    g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
    for t in range(p - 1):
        ind[x] = t; x = x * g % p
    rng = np.random.default_rng(3)
    a, b, xx, yy = (rng.integers(1, p, ns) for _ in range(4))
    rows = np.stack([a, -a % p, b, -b % p], 1); cols = np.stack([xx, -xx % p, yy, -yy % p], 1)
    allpts = np.concatenate([rows, cols], 1)
    srt = np.sort(allpts, 1); ok = (np.diff(srt, axis=1) != 0).all(1)
    Mx = ind[(rows[:, :, None] - cols[:, None, :]) % p] % k
    def rank1(M):
        d = (M - M[:, :1, :] - M[:, :, :1] + M[:, :1, :1]) % k
        return (d == 0).all((1, 2))
    r4 = rank1(Mx) & ok; n = ok.sum()
    h4 = e * float(k) ** -5
    f4 = r4.sum() / n / h4
    print('%6d  %.3f   %6.3f (%.3f)' % (p, p / k ** (k - 1), f4, f4 / np.sqrt(max(r4.sum(), 1))))
