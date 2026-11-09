"""Where do the (C1) configurations of a spike prime come from?  Bucket statistics for uniform S.
For S a uniform k-subset of F_p (as in mc_classes.py), the S-buckets are the classes of points
x not in S with equal S-profile ind(s_j - x) mod k modulo the diagonal; a bucket of size b gives
C(b, k) configurations.  With Poisson(lambda) bucket sizes the k-th factorial moment is lambda^k/k!
per bucket and the share of configurations from buckets of size b is e^-lambda lambda^(b-k)/(b-k)!.
Prints: configurations per S against the Poisson value M lambda^k/k!, the occupancy histogram of the
buckets against Poisson, the share of configurations by bucket size against Poisson, how
concentrated the configurations are on few S (share from the top 0.1% / 1% of S), and the S with the
largest bucket.
Usage: python bucket_stats.py k p nS [--seed s] [--top m]"""
import sys, math, argparse
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot

ap = argparse.ArgumentParser()
ap.add_argument('k', type=int); ap.add_argument('p', type=int); ap.add_argument('nS', type=int)
ap.add_argument('--seed', type=int, default=1); ap.add_argument('--top', type=int, default=5)
a = ap.parse_args(); k, p = a.k, a.p
g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
for e in range(p - 1):
    ind[x] = e; x = x * g % p
chi = ind % k; chi[0] = -1
xs = np.arange(p); kp = k ** np.arange(k - 1); M = k ** (k - 1); lam = p / M
rng = np.random.default_rng(a.seed)
bmax_cap = 40
occ = np.zeros(bmax_cap + 1)            # number of buckets of each size (sizes >= cap pooled)
conf_by_b = np.zeros(bmax_cap + 1)      # configurations from buckets of each size
NT = np.zeros(a.nS)
top = []                                 # (largest bucket size, N_T, S, bucket points)
for i in range(a.nS):
    S = rng.choice(p, k, replace=False)
    D = (S[None, :] - xs[:, None]) % p
    prof = chi[D]; inS = (D == 0).any(1)
    key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp
    bc = np.bincount(key[~inS], minlength=M)
    h = np.bincount(np.minimum(bc, bmax_cap), minlength=bmax_cap + 1)
    occ += h
    full = bc[bc >= k]
    if len(full):
        cb = np.array([math.comb(int(b), k) for b in full], dtype=float)
        NT[i] = cb.sum()
        np.add.at(conf_by_b, np.minimum(full, bmax_cap), cb)
        bm = int(full.max())
        if len(top) < a.top or bm > top[-1][0]:
            Bk = int(np.flatnonzero(bc == bm)[0])
            top.append((bm, NT[i], sorted(int(s) for s in S), sorted(int(t) for t in np.flatnonzero((key == Bk) & ~inS))))
            top.sort(key=lambda t: -t[0]); top = top[:a.top]
tot = NT.sum(); ETp = M * lam ** k / math.factorial(k)
print('k=%d p=%d lambda=%.3f  nS=%d  configurations %d  per S %.5f  Poisson %.5f  ratio %.2f' % (
    k, p, lam, a.nS, tot, tot / a.nS, ETp, tot / a.nS / ETp))
nb = occ.sum(); mean = (occ * np.arange(bmax_cap + 1)).sum() / nb
var = (occ * np.arange(bmax_cap + 1) ** 2).sum() / nb - mean ** 2
print('  bucket occupancy: mean %.4f (lambda %.4f, the M buckets include S-excluded points), var/mean %.3f' % (mean, lam, var / mean))
pois = lambda b: math.exp(-mean) * mean ** b / math.factorial(b)
print('  occupancy P(b) observed / Poisson(mean):  ' + '  '.join(
    'b=%d %.3g/%.3g' % (b, occ[b] / nb, pois(b)) for b in range(0, min(bmax_cap, 12)) if occ[b] > 0 or b <= k + 2))
print('  share of configurations by bucket size (Poisson e^-l l^(b-k)/(b-k)!):  ' + '  '.join(
    'b=%d %.3f (%.3f)' % (b, conf_by_b[b] / tot, math.exp(-mean) * mean ** (b - k) / math.factorial(b - k))
    for b in range(k, bmax_cap + 1) if conf_by_b[b] > 0))
srt = np.sort(NT)[::-1]
for f in (0.001, 0.01):
    m = max(1, int(f * a.nS)); print('  share of configurations from the top %.1f%% of S: %.3f' % (100 * f, srt[:m].sum() / tot))
print('  S with the largest buckets (size, configurations, S, bucket):')
for bm, nt, S, T in top:
    print('    b=%d  N_T=%d  S=%s  bucket=%s' % (bm, nt, S, T))
