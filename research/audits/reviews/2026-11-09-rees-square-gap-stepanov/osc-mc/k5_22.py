"""kappa = 5 (any odd kappa >= 5 in principle): test the pre-registered shape in k4/predictions_k5_22.txt.
For random S (|S| = k) and each involution iota swapping two disjoint pairs of S:
  - partial-fixed keys: full bucket keys K of points t whose profile on the four swapped points is carried by iota to
    the same normalized partial profile (P1 predicts exactly k^(k-3) of them: 25 at k = 5);
  - paired points: t with iota(t) in the same full bucket; every such bucket must be partial-fixed (P1);
  - paired fraction inside partial-fixed buckets (P2 predicts about 1/k);
  - mean iota-pairs in buckets, split against non-split iota (P3);
  - G = s/R22, s = sum_iota sum_K C(m_K, 2) C(b_K - 4, k - 4) / sum_K C(b_K, k), no overlap correction (P4).
Usage: python k5_22.py k p nS [--seed s]"""
import sys, math, itertools, argparse
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
from sym_confs_lib import mob_from

ap = argparse.ArgumentParser()
ap.add_argument('k', type=int); ap.add_argument('p', type=int); ap.add_argument('nS', type=int)
ap.add_argument('--seed', type=int, default=11)
a = ap.parse_args(); k, p = a.k, a.p
assert p % k == 1
g0 = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
for e in range(p - 1):
    ind[x] = e; x = x * g0 % p
chi = ind % k; chi[0] = -1
xs = np.arange(p); kp = k ** np.arange(k - 1); M = k ** (k - 1); lam = p / M
inv = np.zeros(p, dtype=np.int64); inv[1:] = [pow(i, p - 2, p) for i in range(1, p)]
mob_from.p = p
Ninv = math.comb(k, 2) * math.comb(k - 2, 2) // 2
PAIRS = [((i, j), (u, v)) for (i, j), (u, v) in itertools.combinations(itertools.combinations(range(k), 2), 2)
         if len({i, j, u, v}) == 4]
assert len(PAIRS) == Ninv


def apply(gm, t):
    A, B, C, D = gm
    den = (C * t + D) % p
    out = np.full(t.shape, -1, dtype=np.int64); ok = den != 0
    out[ok] = (A * t[ok] + B) % p * inv[den[ok]] % p
    return out


rng = np.random.default_rng(a.seed)
sumN1 = 0; sum22 = 0.0; npf_hist = {}; viol = 0; pf_pts = 0; pf_paired = 0
pairs_by = {True: [0, 0], False: [0, 0]}         # split?: [sum of iota-pairs in buckets, number of iota]
for _ in range(a.nS):
    S = rng.choice(p, k, replace=False)
    D = (S[None, :] - xs[:, None]) % p
    prof = chi[D]; inS = (D == 0).any(1)
    key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp; key[inS] = -1
    bc = np.bincount(key[~inS], minlength=M)
    sumN1 += int(sum(math.comb(int(b), k) for b in bc if b >= k))
    for (i, j), (u, v) in PAIRS:
        gm = mob_from((int(S[i]), int(S[j]), int(S[u])), (int(S[j]), int(S[i]), int(S[v])))
        A, B, C, Dd = gm
        disc = ((A - Dd) ** 2 + 4 * B * C) % p
        split = bool(disc != 0 and ind[disc] % 2 == 0)
        im = apply(gm, xs)
        good = (~inS) & (im >= 0) & (im != xs)
        good[good] &= ~inS[im[good]]
        sw = [i, j, u, v]
        pk = (prof[:, sw[1:]] - prof[:, sw[:1]]) % k            # partial profile on the swapped points
        pf = np.zeros(p, dtype=bool)
        pf[good] = (pk[im[good]] == pk[good]).all(1)
        pf_keys = set(np.unique(key[pf]).tolist())
        paired = np.zeros(p, dtype=bool)
        paired[good] = key[im[good]] == key[good]
        pkeys = set(np.unique(key[paired]).tolist())
        if not pkeys <= pf_keys: viol += 1
        npf_hist[len(pf_keys)] = npf_hist.get(len(pf_keys), 0) + 1
        inpf = (~inS) & np.isin(key, list(pf_keys)) if pf_keys else np.zeros(p, dtype=bool)
        pf_pts += int(inpf.sum()); pf_paired += int(paired.sum())
        m = np.bincount(key[paired], minlength=M) // 2
        pairs_by[split][0] += int(m.sum()); pairs_by[split][1] += 1
        for K in np.flatnonzero(m >= 2):
            sum22 += math.comb(int(m[K]), 2) * math.comb(int(bc[K]) - 4, k - 4)
ETp = M * lam ** k / math.factorial(k)
R22 = Ninv ** 2 * k ** 4 / p ** 2
s = sum22 / max(sumN1, 1)
print('k=%d p=%d lambda=%.3f nS=%d  N1/mu1 %.4f' % (k, p, lam, a.nS, sumN1 / a.nS / ETp))
print('  P1: partial-fixed key counts per iota %s; paired keys outside the partial-fixed set: %d of %d iota' % (
    ' '.join('%d:%d' % kv for kv in sorted(npf_hist.items())), viol, a.nS * Ninv))
print('  P2: paired fraction in partial-fixed buckets %.4f (1/k = %.4f)' % (pf_paired / max(pf_pts, 1), 1 / k))
for sp in (True, False):
    t, n = pairs_by[sp]
    if n: print('  P3: %s iota: %d, mean iota-pairs in buckets %.4f (main term p/(2k^(2k-5)) * k^(k-3) = %.4f)' % (
        'split    ' if sp else 'non-split', n, t / n, p / (2 * k ** (2 * k - 5)) * k ** (k - 3)))
print('  P4: 2+2 share s %.6f  R22 %.6f  G = s/R22 %.4f   F = G*N1/mu1 %.4f' % (s, R22, s / R22, s / R22 * sumN1 / a.nS / ETp))
