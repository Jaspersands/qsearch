"""Are spike primes driven by structured (C1) families?  For divisors d of p-1 (2k <= d <= dmax),
draw random k-subsets S of the d-th roots of unity mu_d (multiplication is in PGL_2, so cosets
c*mu_d are equivalent) and count the (C1) configurations they give (k-subsets T of full S-buckets
over all of F_p, as in mc_classes.py), and how many of those have T inside mu_d.  Compare with the
uniform-S rate (configurations per S) of the Monte Carlo run at the same p.
Usage: python struct_c1.py k p [nS_per_d] [dmax]"""
import sys, math, itertools
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
k, p = int(sys.argv[1]), int(sys.argv[2])
nS = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
dmax = int(sys.argv[4]) if len(sys.argv) > 4 else 400
g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
for e in range(p - 1):
    ind[x] = e; x = x * g % p
chi = ind % k; chi[0] = -1
xs = np.arange(p); kp = k ** np.arange(k - 1); M = k ** (k - 1)
def confs(S):
    D = (S[None, :] - xs[:, None]) % p
    prof = chi[D]; inS = (D == 0).any(1)
    key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp; key[inS] = -1
    bc = np.bincount(key[~inS], minlength=M)
    out = []
    for Bk in np.flatnonzero(bc >= k):
        pts = np.flatnonzero(key == Bk)
        out.extend(itertools.combinations(pts, k))
    return out
rng = np.random.default_rng(5)
# uniform baseline
tot = sum(len(confs(rng.choice(p, k, replace=False))) for _ in range(nS))
print('k=%d p=%d lambda=%.3f  uniform S: %.4f configurations per S (%d draws)' % (k, p, p / k ** (k - 1), tot / nS, nS))
divs = [d for d in range(2 * k, min(dmax, p - 1) + 1) if (p - 1) % d == 0]
for d in divs:
    mu = np.array(sorted({pow(g, (p - 1) // d * i, p) for i in range(d)}))
    muset = set(mu.tolist())
    n_draw = min(nS, math.comb(d, k)); c = 0; inside = 0
    for _ in range(n_draw):
        S = rng.choice(mu, k, replace=False)
        cs = confs(S); c += len(cs); inside += sum(1 for T in cs if all(t in muset for t in T))
    print('  d=%4d: %.4f configurations per S (%.1fx uniform), %.4f with T inside mu_d' % (
        d, c / n_draw, (c / n_draw) / max(tot / nS, 1e-12), inside / n_draw))
