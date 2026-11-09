"""Are spike primes driven by symmetric (C1) configurations?  For uniform S (as in mc_classes.py), every full
S-bucket X (|X| = b >= k, giving C(b, k) configurations) is tested for a nontrivial common PGL_2(F_p)
stabiliser: g with g(S) = S and g(X) = X.  Mechanism: if an involution g fixes S, it permutes the S-buckets
(it acts on profiles by an affine map, independent of x mod the diagonal), and a g-invariant bucket is a union
of g-orbits, so its size is ~2 Poisson(lambda/2), far more often >= k than Poisson(lambda) when lambda is small.
Configurations (S, T) themselves are rarely symmetric (a 6-subset T of a symmetric 10-point bucket usually is
not g-invariant), so the bucket, not T, is tested.
Every g is found by sending (s_1, s_2, s_3) to an ordered triple of distinct points of S (k(k-1)(k-2)
candidates) and checking g(S) = S, g(X) = X, so the stabilisers are exact.
Prints: configurations per S against Poisson, the share of configurations whose (S, bucket) has a nontrivial
stabiliser (by bucket size and by stabiliser order), the share with |Stab(S)| > 1, and examples.
Usage: python sym_confs.py k p nS [--seed s]"""
import sys, math, itertools, argparse
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot

ap = argparse.ArgumentParser()
ap.add_argument('k', type=int); ap.add_argument('p', type=int); ap.add_argument('nS', type=int)
ap.add_argument('--seed', type=int, default=1)
a = ap.parse_args(); k, p = a.k, a.p
g0 = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
for e in range(p - 1):
    ind[x] = e; x = x * g0 % p
chi = ind % k; chi[0] = -1
xs = np.arange(p); kp = k ** np.arange(k - 1); M = k ** (k - 1); lam = p / M
INF = p
inv = [0] + [pow(i, p - 2, p) for i in range(1, p)]


def mob_from(z, w):
    """Matrix of the Moebius map sending z1, z2, z3 -> w1, w2, w3 (all finite, distinct)."""
    def h(z1, z2, z3):     # sends z1 -> 0, z2 -> inf, z3 -> 1
        return ((z3 - z2) % p, (-z1 * (z3 - z2)) % p, (z3 - z1) % p, (-z2 * (z3 - z1)) % p)
    A = h(*z); B = h(*w)
    a_, b_, c_, d_ = B; Bi = (d_, (-b_) % p, (-c_) % p, a_)          # inverse up to scalar
    m = lambda X, Y: ((X[0] * Y[0] + X[1] * Y[2]) % p, (X[0] * Y[1] + X[1] * Y[3]) % p,
                      (X[2] * Y[0] + X[3] * Y[2]) % p, (X[2] * Y[1] + X[3] * Y[3]) % p)
    return m(Bi, A)


def act(gm, pts):
    a_, b_, c_, d_ = gm; out = []
    for x in pts:
        if x == INF:
            out.append(INF if c_ == 0 else a_ * inv[c_] % p)
        else:
            den = (c_ * x + d_) % p
            out.append(INF if den == 0 else (a_ * x + b_) * inv[den] % p)
    return out


def stab(S, T):
    S = [int(s) for s in S]; T = [int(t) for t in T]; sS, sT = set(S), set(T)
    nST = nS_ = 0
    for w in itertools.permutations(S, 3):
        gm = mob_from(tuple(S[:3]), w)
        if set(act(gm, S)) == sS:
            nS_ += 1
            if set(act(gm, T)) == sT:
                nST += 1
    return nST, nS_


rng = np.random.default_rng(a.seed)
nconf = 0; byb = {}; byord = {}; nsymS = 0; ex = []
for i in range(a.nS):
    S = rng.choice(p, k, replace=False)
    D = (S[None, :] - xs[:, None]) % p
    prof = chi[D]; inS = (D == 0).any(1)
    key = ((prof[:, 1:] - prof[:, :1]) % k) @ kp; key[inS] = -1
    bc = np.bincount(key[~inS], minlength=M)
    for Bk in np.flatnonzero(bc >= k):
        X = np.flatnonzero(key == Bk); b = len(X); c = math.comb(b, k)
        hSX, hS = stab(S, X)
        nconf += c
        byb.setdefault(b, [0, 0, 0]); byb[b][0] += c; byb[b][2] += 1
        if hS > 1: nsymS += c
        if hSX > 1:
            byb[b][1] += c; byord[hSX] = byord.get(hSX, 0) + c
            if len(ex) < 6 or b > ex[-1][0]:
                ex.append((b, hSX, hS, sorted(int(s) for s in S), sorted(int(t) for t in X))); ex.sort(key=lambda e: -e[0]); ex = ex[:6]
nsym = sum(v[1] for v in byb.values())
ETp = M * lam ** k / math.factorial(k)
print('k=%d p=%d lambda=%.3f nS=%d configurations %d (%.5f per S, Poisson %.5f, ratio %.2f)' % (
    k, p, lam, a.nS, nconf, nconf / a.nS, ETp, nconf / a.nS / ETp))
print('  (S, bucket) with |Stab| > 1: %.3f of configurations; by stabiliser order: %s;  |Stab(S)| > 1: %.3f' % (
    nsym / max(nconf, 1), ' '.join('%d:%d' % kv for kv in sorted(byord.items())), nsymS / max(nconf, 1)))
print('  by bucket size b: ' + '  '.join('b=%d %d buckets %d conf (%.3f symmetric)' % (b, v[2], v[0], v[1] / v[0]) for b, v in sorted(byb.items())))
print('  non-symmetric configurations per S %.5f (ratio to Poisson %.2f); symmetric per S %.5f (ratio %.2f)' % (
    (nconf - nsym) / a.nS, (nconf - nsym) / a.nS / ETp, nsym / a.nS, nsym / a.nS / ETp))
for e in ex:
    print('    b=%d |Stab(S,X)|=%d |Stab(S)|=%d S=%s X=%s' % e)
