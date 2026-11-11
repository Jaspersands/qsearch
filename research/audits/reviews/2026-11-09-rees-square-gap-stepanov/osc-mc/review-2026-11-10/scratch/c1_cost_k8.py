"""Scoping timer: the index-list form of the sequential (C1) sampler (filters shrink the candidate lists, so only the
first two updates touch all p points) and the per-configuration cost of mc_classes.py's Q = P Hc P^T at kappa = k.
Usage: nice -n 19 python -I c1_cost_k8.py k p attempts [seed]"""
import sys, math, time, itertools
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot, tables
k, p, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
for e in range(p - 1):
    ind[x] = e; x = x * g % p
chi = ind % k; chi[0] = -1
xs = np.arange(p); rng = np.random.default_rng(seed)
t0 = time.time(); W = []; confs = []; nat = 0
for a in range(n):
    s1 = int(rng.integers(p)); t1 = int(rng.integers(p - 1)); t1 += t1 >= s1
    w = float(p) * (p - 1); S = [s1]; T = [t1]
    cS = xs; cT = xs                          # candidate lists (constraints only; used points removed at pick time)
    c0 = int(chi[(s1 - t1) % p]); dead = False
    for step in range(2, 2 * k):
        if step % 2 == 0:
            cand = cS[~np.isin(cS, S + T)]
        else:
            cand = cT[~np.isin(cT, S + T)]
        c = len(cand)
        if c == 0:
            dead = True; break
        y = int(cand[rng.integers(c)]); w *= c
        if step % 2 == 0:
            S.append(y); tgt = (int(chi[(y - t1) % p]) - c0) % k
            cT = cT[((chi[(y - cT) % p] - chi[(s1 - cT) % p]) % k) == tgt]
        else:
            T.append(y); tgt = (int(chi[(s1 - y) % p]) - c0) % k
            cS = cS[((chi[(cS - y) % p] - chi[(cS - t1) % p]) % k) == tgt]
    if not dead:
        Sa, Ta = np.array(S), np.array(T)
        Mx = chi[(Sa[:, None] - Ta[None, :]) % p]
        assert (((Mx - Mx[:, :1] - Mx[:1, :] + Mx[0, 0]) % k) == 0).all()
        W.append(w); confs.append((Sa, Ta))
ts = time.time() - t0
W = np.array(W); ess = W.sum() ** 2 / (W ** 2).sum() if len(W) else 0
print('k=%d p=%d: %d attempts, %d successes, %.2f ms/attempt (index lists), ESS %.0f' % (k, p, n, len(W), 1000 * ts / n, ess), flush=True)
t1_ = time.time(); classes, R, P, orb, rb, supp, canon, base, reps = tables(k); nR, nA = P.shape
print('tables(%d): nR %d, nA %d, %.0f s' % (k, nR, nA, time.time() - t1_), flush=True)
tq = []
for S, T in confs[:5]:
    tq0 = time.time()
    mask = np.ones(p, dtype=bool); mask[S] = False; mask[T] = False; z = xs[mask]
    uref = chi[(T - S[0]) % p]; vref = chi[(S - T[0]) % p]
    U = (chi[(T[None, :] - z[:, None]) % p] - uref[None, :]) % k
    Vv = (chi[(S[None, :] - z[:, None]) % p] - vref[None, :]) % k
    U = np.vstack([U, (-uref)[None, :] % k]); Vv = np.vstack([Vv, (-vref)[None, :] % k])
    cu = np.zeros(len(U), dtype=np.int64); cv = np.zeros(len(U), dtype=np.int64)
    for v in range(k):
        cu += (U == v).sum(1) * base[v]; cv += (Vv == v).sum(1) * base[v]
    iu = canon[cu]; iv = canon[cv]
    th = time.time() - tq0
    Hc = np.bincount(iu * nA + iv, minlength=nA * nA).reshape(nA, nA).astype(float)
    Q = P @ Hc @ P.T
    tq.append((th, time.time() - tq0))
for th, tt in tq:
    print('  per configuration: histogram %.2f s, histogram + Q %.2f s' % (th, tt))
