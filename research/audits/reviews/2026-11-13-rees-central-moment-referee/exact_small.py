"""Exact law of n = n_0(y) for small (kappa, p); test every step of the TH2 Theorem 5 chain.
Also a direct per-tuple test of the Weil count |N - (p-k)/K^k| <= E_k(p)."""
import sys, numpy as np, random, math; sys.path.insert(0, '.')
from gm import *

def coset_index(p, K):
    g = next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in {q for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, int(q**.5) + 1))}))
    ind = -np.ones(p, dtype=int); x = 1
    for e in range(p - 1): ind[x] = e % K; x = x * g % p
    return ind

def law(p, K):
    ind = coset_index(p, K)
    X = np.arange(p)
    inQ0 = (ind == 0)
    # row i: x + y_i in Q_{-i}
    def R(i):  # matrix [x, y] -> indicator
        return (ind[(X[:, None] + X[None, :]) % p] == ((-i) % K)).astype(np.float64)
    if K == 3:
        A = R(1) * inQ0[:, None]          # [x, y1]
        Nmat = A.T @ R(2)                 # [y1, y2]
        vals = np.rint(Nmat).astype(int).ravel()
    elif K == 4:
        R1, R2, R3 = R(1) * inQ0[:, None], R(2), R(3)
        vals = []
        for y1 in range(p):
            M = (R1[:, y1][:, None] * R2).T @ R3   # [y2, y3]
            vals.append(np.rint(M).astype(int).ravel())
        vals = np.concatenate(vals)
    return np.bincount(vals)

def falling(n, k):
    r = 1
    for t in range(k): r *= (n - t)
    return r

for (K, p) in ((3, 1009), (3, 3001), (4, 197), (4, 389)):
    dist = law(p, K); tot = dist.sum(); assert tot == p ** (K - 1)
    h = (p - 1) // K; Q = mp.mpf(K) ** (-(K - 1)); lam = h * Q
    P0 = mp.mpf(int(dist[0])) / tot
    print(f"kappa={K} p={p} lam={mp.nstr(lam,5)} P(n=0)={mp.nstr(P0,5)}  K*P0={mp.nstr(K*P0,4)}")
    ok = True
    for k in range(1, 7):
        Fk = mp.mpf(sum(int(c) * falling(n, k) for n, c in enumerate(dist))) / tot
        Bk = mp.mpf(falling(h, k)) * Q ** k
        eps = mp.mpf(K) ** k * Ek(k, p, K) / (p - k)
        lo = ((1 - mp.mpf(k) / p) * (1 - eps)) ** (K - 1) if eps < 1 else -mp.inf
        hi = ((1 - mp.mpf(k) / p) * (1 + eps)) ** (K - 1)
        r = Fk / Bk
        tol = mp.mpf(10) ** -40
        inb = lo * (1 - tol) <= r <= hi * (1 + tol)
        ok &= inb
        print(f"  k={k} F/B={mp.nstr(r,8)} bracket=[{mp.nstr(lo,6)},{mp.nstr(hi,6)}] {'ok' if inb else 'VIOLATION'}")
    for m in (1, 2, 3):
        Ef = mp.mpf(sum(int(c) * (1 - mp.mpf(n) / lam) ** (2 * m) for n, c in enumerate(dist))) / tot
        # exact binomial central moment
        cm = sum(mp.binomial(h, b) * Q ** b * (1 - Q) ** (h - b) * (b - lam) ** (2 * m) for b in range(h + 1))
        A = sum(S2ns(2 * m, j) * lam ** j for j in range(1, m + 1))
        g = G(p, K, m)
        print(f"  m={m} P0<=Ef: {P0 <= Ef}  Ef={mp.nstr(Ef,5)}  G_m/K={mp.nstr(g/K,5)}  Ef<=G/K: {Ef <= g/K}  E(B-lam)^2m={mp.nstr(cm,5)} <= A={mp.nstr(A,5)}: {cm <= A}")
    print("  brackets all ok:", ok)

print("== per-tuple Weil count test")
rng = random.Random(1)
worst = 0
for (K, p) in ((3, 1009), (4, 1009), (5, 1021), (6, 1009), (7, 1009), (3, 10009), (4, 10009)):
    if (p - 1) % K: continue
    ind = coset_index(p, K)
    for trial in range(300):
        k = rng.randint(2, min(6, K + 3))
        a = rng.sample(range(p), k); c = [rng.randrange(K) for _ in range(k)]
        ys = np.arange(p)
        mask = np.ones(p, bool)
        for al, cl in zip(a, c): mask &= (ind[(ys + al) % p] == cl)
        N = int(mask.sum())
        err = abs(N - (p - k) / K ** k)
        bound = float(Ek(k, p, K))
        worst = max(worst, err / bound)
        if err > bound + 1e-9: print("VIOLATION", K, p, k, a, c, N, err, bound)
print("max |N-(p-k)/K^k| / E_k over trials:", round(worst, 4))
