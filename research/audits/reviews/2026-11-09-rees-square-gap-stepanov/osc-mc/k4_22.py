"""kappa = 4: the 2+2 family in closed form, checked exactly.

Claims checked (derivation in the topic note, section 12.13):
  (a) each of the three involutions iota of PGL_2(F_p) that preserve S = {s1..s4} (the Klein group V4 of S) maps
      buckets to buckets, and a bucket K contains iota-pairs only if its key is sigma_iota-fixed; then every point of
      K is paired (up to <= 3 exceptional points: fixed points of iota, the pole -d/c and iota(inf));
  (b) sigma_iota has 8 fixed keys if iota is split (two fixed points in P^1(F_p)) and 0 if not;
  (c) #split = 1 + 2*[eta(r) = eta(1-r) = 1], r the cross-ratio of S, eta the quadratic character (p = 1 mod 4);
  (d) the 2+2 count of S (4-subsets T of one bucket that are two iota-pairs for some iota) equals
      sum_iota sum_K C(m_{iota,K}, 2) - 2 * #(free V4-orbits inside one bucket), m = iota-pairs in K.
Then G = s / R22 with s = sum_S #2+2(S) / sum_S N1(S), R22 = N_inv^2 k^4 / p^2 = 2304 / p^2, against the main-term
prediction G -> (2/3) E[#split] = 1 as p -> infinity (Weil, fixed kappa).
Usage: python k4_22.py p [nS]   (nS omitted: all S = {0, 1, x, y}, which is uniform over 4-sets of F_p)
       add --brute n to brute-force (d) on the first n S with every bucket of size <= 14."""
import sys, math, itertools, argparse
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
from sym_confs_lib import mob_from

ap = argparse.ArgumentParser()
ap.add_argument('p', type=int); ap.add_argument('nS', type=int, nargs='?', default=0)
ap.add_argument('--seed', type=int, default=7); ap.add_argument('--brute', type=int, default=0)
a = ap.parse_args(); p, k = a.p, 4
assert p % 4 == 1
g0 = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
for e in range(p - 1):
    ind[x] = e; x = x * g0 % p
chi = ind % 4; chi[0] = -1
eta = lambda v: 1 if ind[v % p] % 2 == 0 else -1
xs = np.arange(p); kp = 4 ** np.arange(3); M = 64; lam = p / M
inv = np.zeros(p, dtype=np.int64); inv[1:] = [pow(i, p - 2, p) for i in range(1, p)]
mob_from.p = p
PAIRINGS = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]


def apply(gm, t):
    A, B, C, D = gm
    den = (C * t + D) % p
    out = np.full(t.shape, -1, dtype=np.int64); ok = den != 0
    out[ok] = (A * t[ok] + B) % p * inv[den[ok]] % p
    return out                                   # -1 marks infinity


def S_iter():
    if a.nS == 0:
        for u in range(2, p):
            for v in range(u + 1, p):
                yield np.array([0, 1, u, v])
    else:
        rng = np.random.default_rng(a.seed)
        for _ in range(a.nS):
            yield rng.choice(p, 4, replace=False)


nS = 0; sumN1 = 0; sum22 = 0; sumfree = 0; sumsplit = 0; bad_a = bad_b = bad_c = 0; nfull = 0
brute_done = brute_bad = 0; pole_used = 0; hist_split = {}; sumN1_by = {1: 0, 3: 0}; sum22_by = {1: 0, 3: 0}; nS_by = {1: 0, 3: 0}
for S in S_iter():
    nS += 1
    D = (S[None, :] - xs[:, None]) % p
    prof = chi[D]; inS = (D == 0).any(1)
    key = ((prof[:, 1:] - prof[:, :1]) % 4) @ kp; key[inS] = -1
    bc = np.bincount(key[~inS], minlength=M)
    N1 = int(sum(math.comb(int(b), 4) for b in bc if b >= 4))
    nonempty = np.flatnonzero(bc > 0)
    imgs = []; nsplit = 0; c22 = 0
    for (i, j), (u, v) in PAIRINGS:
        gm = mob_from((int(S[i]), int(S[j]), int(S[u])), (int(S[j]), int(S[i]), int(S[v])))
        A, B, C, Dd = gm
        disc = ((A - Dd) ** 2 + 4 * B * C) % p   # fixed-point discriminant of the involution
        split = disc != 0 and eta(disc) == 1
        nsplit += split
        im = apply(gm, xs); imgs.append(im)
        good = (~inS) & (im >= 0) & (im != xs)
        paired = np.zeros(p, dtype=bool)
        paired[good] = key[im[good]] == key[good]
        npair = np.bincount(key[paired], minlength=M)
        # (a): a bucket is wholly paired or wholly unpaired, up to 3 exceptional points
        frac_keys = [K for K in nonempty if npair[K] > 0]
        for K in nonempty:
            if npair[K] > 0 and bc[K] - npair[K] > 3: bad_a += 1
        # (b): sigma_iota-fixed keys (keys of t with key(iota t) = key(t), fixed points of iota included): 0 if
        # non-split, at most 8, exactly 8 when all 64 buckets are nonempty; paired keys are among them
        fin = (~inS) & (im >= 0)
        fx = np.zeros(p, dtype=bool); fx[fin] = key[im[fin]] == key[fin]
        fkeys = set(np.unique(key[fx]).tolist())
        # Counter only (referee round 4i): adds key(t0) when 7 keys are witnessed, WITHOUT checking that it is fixed.
        # It is right only when all 64 buckets are nonempty; no reported number depends on it.
        if split and C % p:
            t0 = (-Dd * pow(int(C), p - 2, p)) % p
            if key[t0] >= 0 and len(fkeys) == 7: fkeys.add(int(key[t0])); pole_used += 1
        if (not split and fkeys) or len(fkeys) > 8 or not set(frac_keys) <= fkeys: bad_b += 1
        if split and len(nonempty) == M and len(fkeys) != 8: bad_b += 1
        m = npair // 2
        c22 += int(sum(math.comb(int(mm), 2) for mm in m))
    if len(nonempty) == M: nfull += 1
    # free V4-orbits inside one bucket: t, i1 t, i2 t, i3 t distinct, finite, all of one key
    ok = (~inS).copy()
    for im in imgs: ok &= im >= 0
    I1, I2, I3 = [np.where(im >= 0, im, 0) for im in imgs]
    orb = ok & (I1 != xs) & (I2 != xs) & (I3 != xs) & (I1 != I2) & (I1 != I3) & (I2 != I3)
    orb &= (key[I1] == key) & (key[I2] == key) & (key[I3] == key) & (key >= 0)
    nfree = int(orb.sum()) // 4
    n22 = c22 - 2 * nfree
    # (c)
    s1, s2, s3, s4 = [int(z) for z in S]
    r = (s3 - s1) * (s4 - s2) % p * pow((s3 - s2) * (s4 - s1) % p, p - 2, p) % p
    pred = 1 + 2 * (eta(r) == 1 and eta(1 - r) == 1)
    if pred != nsplit: bad_c += 1
    hist_split[nsplit] = hist_split.get(nsplit, 0) + 1
    # (d) brute force on small buckets
    if brute_done < a.brute and bc.max() <= 14:
        brute_done += 1; cnt = 0
        for K in np.flatnonzero(bc >= 4):
            X = [int(t) for t in np.flatnonzero(key == K)]
            for T in itertools.combinations(X, 4):
                sT = set(T); hit = False
                for im in imgs:
                    prs = {frozenset((t, int(im[t]))) for t in T if int(im[t]) in sT and int(im[t]) != t}
                    if len(prs) >= 2: hit = True; break
                cnt += hit
        if cnt != n22: brute_bad += 1
    sumN1 += N1; sum22 += n22; sumfree += nfree; sumsplit += nsplit
    if nsplit in sumN1_by:
        sumN1_by[nsplit] += N1; sum22_by[nsplit] += n22; nS_by[nsplit] += 1

ETp = M * lam ** 4 / 24
R22 = 9 * 256 / p ** 2
s = sum22 / sumN1
print('k=4 p=%d lambda=%.3f  S %s: %d  (all 64 buckets nonempty in %d)' % (p, lam, 'all {0,1,x,y}' if a.nS == 0 else 'random', nS, nfull))
print('  checks: (a) partially paired buckets %d   (b) fixed-key-count violations %d   (c) #split formula failures %d   (d) brute-force mismatches %d of %d' % (
    bad_a, bad_b, bad_c, brute_bad, brute_done) + '   (8th key witnessed only by the pole in %d iota)' % pole_used)
print('  #split distribution: ' + '  '.join('%d: %.4f' % (q, v / nS) for q, v in sorted(hist_split.items())) + '   mean %.4f' % (sumsplit / nS))
print('  N1/mu1 %.4f   2+2 share s %.5f   R22 %.5f   G = s/R22 %.4f   (main-term prediction (2/3) E[#split] = %.4f)' % (
    sumN1 / nS / ETp, s, R22, s / R22, 2 / 3 * sumsplit / nS))
mu22 = (sumsplit / nS) * lam ** 2               # main term of #2+2 per S: 8 fixed keys per split iota, C(lam/2, 2) each
print('  N22/mu22 %.4f (mu22 = E[#split] lam^2 per S); identity G = (2/3) E[#split] (N22/mu22) / (N1/mu1)' % (sum22 / nS / mu22))
print('  free V4-orbits per S %.4f (overlap correction %.4f of the 2+2 count)' % (sumfree / nS, 2 * sumfree / max(sum22 + 2 * sumfree, 1)))
for q in (1, 3):
    if nS_by[q]:
        print('  S with %d split: share %.4f of S; their G = %.4f (main-term %.4f); their N1/mu1 %.4f' % (
            q, nS_by[q] / nS, sum22_by[q] / max(sumN1_by[q], 1) / R22, 2 * q / 3, sumN1_by[q] / nS_by[q] / ETp))
