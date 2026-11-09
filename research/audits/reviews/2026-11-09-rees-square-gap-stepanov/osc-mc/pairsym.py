"""Partial involution symmetry of (C1) configurations.  For uniform S (as in mc_classes.py) and every full S-bucket
X (|X| = b >= k), each involution iota of PGL_2(F_p) that swaps two disjoint pairs of S (45 of them for k = 6;
an involution is determined by two of its 2-cycles) is tested: m_S(iota) = number of iota-pairs inside S,
m_X(iota) = number of iota-pairs {x, iota(x)} inside X.  Heuristic behind the test: if S and T both contain two
iota-pairs, the 4x4 index block on those pairs is rank-1 with probability 2*6^-5 for a split iota (two fixed points
in P^1(F_p)) and never for a non-split one at even k (about half of the iota are of each kind), so 6^-5 on average
instead of 6^-9 (an enhancement 6^4 = 1296), against a probability ~45^2/p^2 for such a structure to be present; at
p ~ 1620 the product is ~1, so a large share of configurations would carry it if the remaining conditions behaved
independently (review-2026-11-10/REPORT.md corrected an earlier factor 2 here).
Prints the share of configurations (k-subsets T of X, each tested against every such iota, so the share is exact)
with at least two iota-pairs in T for some iota of S, against the same share for random b-subsets of F_p (run with --null), and by bucket size.  Also the
share with at least two 'units' in T, a unit being an iota-pair or a fixed point of iota (a fixed point in T
removes two rank-1 conditions of its column and forces c = 0).
Usage: python pairsym.py k p nS [--seed s] [--null]"""
import sys, math, itertools, argparse
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
from sym_confs_lib import mob_from, act_factory

ap = argparse.ArgumentParser()
ap.add_argument('k', type=int); ap.add_argument('p', type=int); ap.add_argument('nS', type=int)
ap.add_argument('--seed', type=int, default=5); ap.add_argument('--null', action='store_true')
a = ap.parse_args(); k, p = a.k, a.p
g0 = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
for e in range(p - 1):
    ind[x] = e; x = x * g0 % p
chi = ind % k; chi[0] = -1
xs = np.arange(p); kp = k ** np.arange(k - 1); M = k ** (k - 1); lam = p / M
act = act_factory(p)


def involutions(S):
    S = [int(s) for s in S]; out = []
    for (i, j), (u, v) in itertools.combinations(itertools.combinations(range(len(S)), 2), 2):
        if len({i, j, u, v}) < 4: continue
        out.append(mob_from((S[i], S[j], S[u]), (S[j], S[i], S[v])))
    return out


rng = np.random.default_rng(a.seed)
nconf = 0; withpair = 0; withunit = 0; byb = {}; mhist = {}
for i in range(a.nS):
    S = rng.choice(p, k, replace=False)
    D = (S[None, :] - xs[:, None]) % p
    prof = chi[D]; inS = (D == 0).any(1)
    key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp; key[inS] = -1
    bc = np.bincount(key[~inS], minlength=M)
    for Bk in np.flatnonzero(bc >= k):
        X = np.flatnonzero(key == Bk); b = len(X)
        if a.null:
            X = rng.choice(np.setdiff1d(np.arange(p), S), b, replace=False)
        Xl = [int(t) for t in X]; sX = set(Xl); c = math.comb(b, k)
        best = 0; struct = []                   # per involution: (iota-pairs inside X, iota-fixed points in X)
        for gm in involutions(S):
            im = act(gm, Xl)
            prs = {frozenset((t, u)) for t, u in zip(Xl, im) if u in sX and u != t}
            fx = {t for t, u in zip(Xl, im) if u == t}
            best = max(best, len(prs))
            if len(prs) + len(fx) >= 2: struct.append((prs, fx))
        wp = wu = 0                             # exact: k-subsets T structured for at least one iota
        if struct:
            for Tt in itertools.combinations(Xl, k):
                sT = set(Tt); ip = iu = False
                for prs, fx in struct:
                    npair = sum(1 for pr in prs if pr <= sT)
                    if npair >= 2: ip = True
                    if npair + len(fx & sT) >= 2: iu = True
                    if ip: break
                wp += ip; wu += iu or ip
        nconf += c; withpair += wp; withunit += wu
        byb.setdefault(b, [0, 0]); byb[b][0] += c; byb[b][1] += wp
        mhist[best] = mhist.get(best, 0) + c
ETp = M * lam ** k / math.factorial(k)
print('k=%d p=%d lambda=%.3f nS=%d %s configurations %d (ratio to Poisson %.2f)' % (
    k, p, lam, a.nS, 'NULL (random b-sets in place of buckets)' if a.null else '', nconf, nconf / a.nS / ETp))
print('  share of configurations with >= 2 iota-pairs in T for some involution iota swapping two pairs of S: %.3f' % (withpair / max(nconf, 1)))
print('  share with >= 2 units (iota-pairs or iota-fixed points) in T for some such iota: %.3f' % (withunit / max(nconf, 1)))
print('  configurations by max_iota m_X(iota) (pairs in the whole bucket): ' + '  '.join('%d:%.3f' % (m, v / nconf) for m, v in sorted(mhist.items())))
print('  by bucket size: ' + '  '.join('b=%d %d conf, share with 2 pairs %.3f' % (b, v[0], v[1] / v[0]) for b, v in sorted(byb.items())))
