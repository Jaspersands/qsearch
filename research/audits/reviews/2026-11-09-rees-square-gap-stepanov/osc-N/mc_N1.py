"""Monte Carlo estimate of N1/mu1 for open (C1) configurations (proposed test of OSC (N) at lambda < 1).

Sample S = (s_1..s_k) uniformly (ordered, distinct), bucket every t notin S by its profile
(ind(s_j - t))_j mod the diagonal, Y(S) = sum_c (b_c)_k.  E[Y] = N1_lab / (p)_k exactly.
Reported ratio (same normalisation as the last column of ../types/sep_types.py):
    R = E[Y] k^((k-1)^2) / (p-k)_k  = (#open C1) / (#open configs) * k^((k-1)^2),
compared with the 4-cycle heuristic exp(-(k-1) C(k,2)^2 / (p-2)).
Usage: python mc_N1.py k p nsamples [seed]
Validated at k = 4 against exact values (sep_k4.out).  The intended run is k = 7,
p ~ 1.2e4 .. 3.6e4 (lambda = (p-k)/k^(k-1) ~ 0.1 .. 0.3), which is NOT run here (machine load).
"""
import sys, math
import numpy as np


def primroot(p):
    n = p - 1; fac = []; d = 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac): return g


def main(k, p, ns, seed=1):
    rng = np.random.default_rng(seed)
    g = primroot(p)
    ind = np.full(p, -1, dtype=np.int64)
    x = 1
    for e in range(p - 1):
        ind[x] = e % k; x = x * g % p
    D = k ** (k - 1)
    xs = np.arange(p)
    w = k ** np.arange(k - 1)
    Ys = np.empty(ns)
    hits = 0
    for n in range(ns):
        S = rng.choice(p, size=k, replace=False)
        ic = ind[(S[None, :] - xs[:, None]) % p]  # (p, k)
        ok = (ic >= 0).all(axis=1)
        rel = (ic[ok, 1:] - ic[ok, :1]) % k
        cl = (rel * w).sum(axis=1)
        b = np.bincount(cl, minlength=D).astype(np.float64)
        f = np.ones_like(b)
        for i in range(k):
            f *= (b - i)
        Ys[n] = f.sum()
        hits += Ys[n] > 0
    ffpk = 1.0
    for i in range(k):
        ffpk *= (p - k - i)
    R = Ys.mean() * k ** ((k - 1) ** 2) / ffpk
    se = Ys.std(ddof=1) / math.sqrt(ns) * k ** ((k - 1) ** 2) / ffpk
    lam = (p - k) / D
    pred = math.exp(-(k - 1) * math.comb(k, 2) ** 2 / (p - 2))
    print(f'k={k} p={p} lambda={lam:.4f} samples={ns} S-with-a-full-bucket={hits}  R={R:.4f} +- {se:.4f}  '
          f'4-cycle heuristic={pred:.4f}', flush=True)


if __name__ == '__main__':
    k, p, ns = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    main(k, p, ns, int(sys.argv[4]) if len(sys.argv) > 4 else 1)
