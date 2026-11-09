"""Configuration rate of involution-symmetric S, and its share of N1/mu1.
Every split involution of PGL_2(F_p) is conjugate to x -> -x, so the k-sets S that are unions of k/2 swapped
pairs are, up to PGL_2, S = {+-r_1, ..., +-r_{k/2}} with r_i uniform in F_p^* (r_i != +-r_j); for odd k,
S = {0} u {+-r_1, ..., +-r_{(k-1)/2}} (one fixed point of the involution in S).  For such S the involution
permutes the S-buckets; the buckets it fixes are unions of pairs {x, -x}.
For even k this misses the S that are unions of pairs of a NON-split involution (conjugate to x -> eps/x, eps a
non-square, no fixed points in P^1(F_p)); at odd k every symmetric S needs a fixed point, so none are missed.
At k = 6 the missed S have no fixed buckets and a small rate except at some primes (0.56 and 0.89 x Poisson at 1621
and 1657, 26 +- 13 at 1531; review-2026-11-10/REPORT.md), so C_sym below is a lower estimate.
Their share of all S (in P^1) is f = [p(p+1)/2] C((p-1)/2, k/2) / C(p+1, k) for even k and
f = [p(p+1)/2] 2 C((p-1)/2, (k-1)/2) / C(p+1, k) for odd k (overlaps neglected), so their
contribution to the configurations per S, relative to the Poisson value M lambda^k/k!, is
    C_sym = f * (configurations per symmetric S) / (M lambda^k / k!),
to be compared with the measured N1/mu1 (mc_classes.py) of the same prime.  Also printed: the part of the
symmetric-S configurations that comes from involution-fixed buckets.
Usage: python sym_rate.py k nS p [p ...]"""
import sys, math
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot

k, nS = int(sys.argv[1]), int(sys.argv[2])
print('  p    lam   conf/symS   ratio_to_Poisson  from_fixed_buckets   f=share_of_S   C_sym   (k=%d, %d symmetric S per prime)' % (k, nS))
for p in [int(x) for x in sys.argv[3:]]:
    g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p - 1):
        ind[x] = e; x = x * g % p
    chi = ind % k; chi[0] = -1
    xs = np.arange(p); kp = k ** np.arange(k - 1); M = k ** (k - 1); lam = p / M
    neg = (-xs) % p
    rng = np.random.default_rng(11)
    tot = 0.0; fixed = 0.0; done = 0
    while done < nS:
        r = rng.integers(1, p, k // 2)
        S = np.concatenate([r, (-r) % p] + ([np.array([0])] if k % 2 else []))
        if len(set(S.tolist())) < k: continue
        done += 1
        D = (S[None, :] - xs[:, None]) % p
        prof = chi[D]; inS = (D == 0).any(1)
        key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp; key[inS] = -1
        bc = np.bincount(key[~inS], minlength=M)
        for Bk in np.flatnonzero(bc >= k):
            X = np.flatnonzero(key == Bk); c = math.comb(len(X), k); tot += c
            if set(X.tolist()) == set(neg[X].tolist()): fixed += c
    ETp = M * lam ** k / math.factorial(k)
    f = (p * (p + 1) / 2) * (2 if k % 2 else 1) * math.comb((p - 1) // 2, k // 2) / math.comb(p + 1, k)
    print('%6d  %5.3f  %9.5f   %9.2f          %5.3f            %.2e     %6.3f' % (
        p, lam, tot / nS, tot / nS / ETp, fixed / max(tot, 1), f, f * tot / nS / ETp))
