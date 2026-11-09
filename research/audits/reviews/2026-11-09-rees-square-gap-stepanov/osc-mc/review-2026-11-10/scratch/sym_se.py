"""Referee scratch: sampling error of sym_rate.py's symR (same estimator, other seed, batch se), and the rate of
S symmetric under a NON-split involution x -> eps/x (eps a non-square), which sym_rate.py's share f omits.
Usage: python sym_se.py k nS nbatch seed p [p ...]   (run from osc-mc)"""
import sys, math
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot

k, nS, nb, seed = (int(v) for v in sys.argv[1:5])
for p in [int(v) for v in sys.argv[5:]]:
    g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p - 1):
        ind[x] = e; x = x * g % p
    chi = ind % k; chi[0] = -1
    xs = np.arange(p); kp = k ** np.arange(k - 1); M = k ** (k - 1); lam = p / M
    ETp = M * lam ** k / math.factorial(k)
    eps = next(e for e in range(2, p) if pow(e, (p - 1) // 2, p) == p - 1)
    invm = np.zeros(p, dtype=np.int64); invm[1:] = [pow(int(t), p - 2, p) for t in range(1, p)]
    res = {}
    for kind in ('split', 'nonsplit'):
        rng = np.random.default_rng(seed)
        img = (-xs) % p if kind == 'split' else (eps * invm) % p      # the involution on F_p^* (0 <-> inf for nonsplit)
        tot = np.zeros(nb); fixed = 0.0; done = 0
        n_this = nS if kind == 'split' else nS // 2
        while done < n_this:
            r = rng.integers(1, p, k // 2)
            S = np.concatenate([r, img[r]] + ([np.array([0])] if k % 2 else []))
            if len(set(S.tolist())) < k: continue
            bidx = done * nb // n_this; done += 1
            D = (S[None, :] - xs[:, None]) % p
            prof = chi[D]; inS = (D == 0).any(1)
            key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp; key[inS] = -1
            bc = np.bincount(key[~inS], minlength=M)
            for Bk in np.flatnonzero(bc >= k):
                X = np.flatnonzero(key == Bk); c = math.comb(len(X), k); tot[bidx] += c
                Xs = set(X.tolist())
                if Xs == set(int(img[t]) if t != 0 else -1 for t in X) or (kind == 'split' and Xs == set(((-X) % p).tolist())): fixed += c
        rate = tot / (n_this / nb) / ETp
        res[kind] = (rate.mean(), rate.std(ddof=1) / math.sqrt(nb), fixed / max(tot.sum(), 1))
    print('p=%d lam=%.3f  split symR %.2f (batch se %.2f, %d S, fixed-bucket share %.3f)   nonsplit rate %.2f (se %.2f, %d S, fixed share %.3f)' % (
        p, lam, res['split'][0], res['split'][1], nS, res['split'][2], res['nonsplit'][0], res['nonsplit'][1], nS // 2, res['nonsplit'][2]), flush=True)
