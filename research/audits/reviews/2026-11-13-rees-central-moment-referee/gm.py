"""Independent implementation of TH2 Theorem 5 (G_m) and paper prop:app-s2-TA (U_kappa, T_A),
written from the statements in TH2 sec. 2 and appendix-schedule2.tex.  mpmath, 60 digits."""
import mpmath as mp
from functools import lru_cache
mp.mp.dps = 60

@lru_cache(None)
def S2(n, k):          # Stirling numbers of the second kind
    if n == 0 and k == 0: return 1
    if n == 0 or k == 0: return 0
    return k * S2(n - 1, k) + S2(n - 1, k - 1)

@lru_cache(None)
def S2ns(n, j):        # set partitions of [n] into j blocks, no singleton block
    if n == 0 and j == 0: return 1
    if n <= 0 or j <= 0: return 0
    # element n either joins one of j blocks of a no-singleton partition of [n-1],
    # or forms a 2-block with one of the n-1 others, rest no-singleton partition of n-2
    return j * S2ns(n - 1, j) + (n - 1) * S2ns(n - 2, j - 1)

def Ek(k, p, K):
    K = mp.mpf(K)
    return (k - 1 - k / K + K ** (-k)) * mp.sqrt(p) + k / K - k * K ** (-k)

def delta(k, p, K):
    if k == 0: return mp.mpf(0)
    eps = mp.mpf(K) ** k * Ek(k, p, K) / (p - k)
    if eps >= 1: return mp.inf
    return max((1 + eps) ** (K - 1) - 1, 1 - ((1 - mp.mpf(k) / p) * (1 - eps)) ** (K - 1))

def G(p, K, m):
    p = mp.mpf(p)
    lam = (p - 1) / mp.mpf(K) ** K
    A = sum(S2ns(2 * m, j) * lam ** j for j in range(1, m + 1))
    W = sum(mp.binomial(2 * m, j) * lam ** (-j) * sum(S2(j, k) * lam ** k for k in range(0, j + 1))
            for j in range(0, 2 * m + 1))
    d = max(delta(k, p, K) for k in range(0, 2 * m + 1))
    if d == mp.inf: return mp.inf
    return K * (lam ** (-2 * m) * A + W * d)

def Gmin(p, K, mmax=16):
    best = (mp.inf, None)
    for m in range(1, mmax + 1):
        if p <= 2 * m: break
        g = G(p, K, m)
        if g < best[0]: best = (g, m)
    return best

def bisect(f, lo, hi, it=200):
    # f monotone: False on lo side, True on hi side
    for _ in range(it):
        mid = mp.sqrt(lo * hi)
        if f(mid): hi = mid
        else: lo = mid
        if hi / lo - 1 < mp.mpf(10) ** -12: break
    return hi

def TC(K, mmax=16):
    kk = mp.mpf(K) ** K
    best = (mp.inf, None)
    for m in range(1, mmax + 1):
        lo, hi = mp.mpf(2 * m + 1), kk * 10 ** 8
        if not G(hi, K, m) < 1: continue
        t = bisect(lambda q: G(q, K, m) < 1, lo, hi)
        if t < best[0]: best = (t, m)
    return best

def Delta(p, K):
    return ((K - 1) * (K - 2) * mp.sqrt(p) + 2 * (K - 1)) / (p - K - 1)

def U(p, K):
    p = mp.mpf(p); D = Delta(p, K)
    if D > mp.mpf(1) / 2: return mp.inf
    u = mp.mpf(1) / 2 - D / 3 - 1 / (K * (1 - D))
    v = D / (mp.sqrt(K) * (1 - D))
    smax = mp.sqrt(K) * D
    if u > 0:
        s = min(max(v / (2 * u), 0), smax)
    else:
        s = smax
    Emax = max(-u * s * s + v * s, mp.mpf(0))
    return mp.mpf(K) ** K * p ** (K - 1) / (p - 1) ** K + mp.exp(Emax)

def TA(K):
    lo, hi = mp.mpf(K + 2), mp.mpf(K) ** (K + 1) * 4
    return bisect(lambda q: U(q, K) < mp.mpf(K) / (K - 1), lo, hi)
