"""Referee scratch: same sample as pairsym.py (same seed, same rng calls, non-null mode), but for every full bucket
X computes (a) pairsym's max-over-iota count, (b) the exact number of k-subsets T of X that contain >= 2 iota-pairs
for SOME iota (union), by enumeration, (c) whether the witnessing involutions are split (fixed points in F_p),
(d) for the non-structured T, whether their bucket contains a structured T (shared bucket).
Usage: python pairsym_exact.py k p nS [--seed s]   (run from osc-mc)"""
import sys, math, itertools, argparse
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
from sym_confs_lib import mob_from, act_factory

ap = argparse.ArgumentParser()
ap.add_argument('k', type=int); ap.add_argument('p', type=int); ap.add_argument('nS', type=int)
ap.add_argument('--seed', type=int, default=5)
a = ap.parse_args(); k, p = a.k, a.p
g0 = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
for e in range(p - 1):
    ind[x] = e; x = x * g0 % p
chi = ind % k; chi[0] = -1
xs = np.arange(p); kp = k ** np.arange(k - 1); M = k ** (k - 1); lam = p / M
act = act_factory(p)
issq = np.zeros(p, dtype=bool); issq[(np.arange(1, p) ** 2) % p] = True


def involutions(S):
    S = [int(s) for s in S]; out = []
    for (i, j), (u, v) in itertools.combinations(itertools.combinations(range(len(S)), 2), 2):
        if len({i, j, u, v}) < 4: continue
        out.append(mob_from((S[i], S[j], S[u]), (S[j], S[i], S[v])))
    return out


def n_T_with_two_pairs(b, m):          # copy of pairsym.py
    tot = 0
    for j in range(2, m + 1):
        rest = k - 2 * j
        if rest < 0: break
        others = b - 2 * m; cnt = 0
        for h in range(0, rest + 1):
            if rest - h > others or h > m - j: continue
            cnt += math.comb(m - j, h) * 2 ** h * math.comb(others, rest - h)
        tot += math.comb(m, j) * cnt
    return tot


rng = np.random.default_rng(a.seed)
nconf = 0; wmax = 0; wunion = 0; wsplit_only = 0; wnonsplit_wit = 0; trace_bad = 0; ninv = 0
uns_in_strbucket = 0; uns_tot = 0; byb = {}
for i in range(a.nS):
    S = rng.choice(p, k, replace=False)
    D = (S[None, :] - xs[:, None]) % p
    prof = chi[D]; inS = (D == 0).any(1)
    key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp; key[inS] = -1
    bc = np.bincount(key[~inS], minlength=M)
    full = np.flatnonzero(bc >= k)
    if not len(full): continue
    invs = involutions(S)
    for gm in invs:
        ninv += 1
        if (gm[0] + gm[3]) % p != 0: trace_bad += 1
    for Bk in full:
        X = np.flatnonzero(key == Bk); b = len(X)
        Xl = [int(t) for t in X]; sX = set(Xl); c = math.comb(b, k)
        wp = 0; pairsets = []
        for gm in invs:
            im = act(gm, Xl)
            prs = {frozenset((t, u)) for t, u in zip(Xl, im) if u in sX and u != t}
            m = len(prs)
            if m >= 2:
                wp = max(wp, n_T_with_two_pairs(b, m))
                aa, bb, cc, dd = gm
                split = bool(issq[(aa * aa + bb * cc) % p]) and (aa * aa + bb * cc) % p != 0
                pairsets.append((prs, split))
        nu = 0; ns_wit = 0
        for Tt in itertools.combinations(Xl, k):
            sT = set(Tt)
            wit = [sp for prs, sp in pairsets if sum(1 for pr in prs if pr <= sT) >= 2]
            if wit:
                nu += 1
                if not any(wit): ns_wit += 1          # witnessed only by non-split involutions
        nconf += c; wmax += wp; wunion += nu; wnonsplit_wit += ns_wit
        uns_tot += c - nu
        if nu > 0: uns_in_strbucket += c - nu
        byb.setdefault(b, [0, 0, 0]); byb[b][0] += c; byb[b][1] += wp; byb[b][2] += nu
ETp = M * lam ** k / math.factorial(k)
print('k=%d p=%d lambda=%.3f nS=%d seed=%d configurations %d (ratio to Poisson %.2f)' % (k, p, lam, a.nS, a.seed, nconf, nconf / a.nS / ETp))
print('  share >=2 iota-pairs: pairsym max-over-iota %.3f   exact union %.3f' % (wmax / max(nconf, 1), wunion / max(nconf, 1)))
print('  structured T witnessed only by non-split involutions: %d of %d' % (wnonsplit_wit, wunion))
print('  involution matrices with nonzero trace (not involutions): %d of %d' % (trace_bad, ninv))
print('  non-structured configurations lying in a bucket that contains a structured T: %d of %d (%.3f)' % (
    uns_in_strbucket, uns_tot, uns_in_strbucket / max(uns_tot, 1)))
print('  by bucket size (max / union): ' + '  '.join('b=%d %d conf %.3f/%.3f' % (b, v[0], v[1] / v[0], v[2] / v[0]) for b, v in sorted(byb.items())))
