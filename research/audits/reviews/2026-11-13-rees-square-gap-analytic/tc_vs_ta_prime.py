"""Independent re-implementation (written from the statements, not from TH2's code) of
  - T_A(k): inf{p : Delta(p) <= 1/2, U_k(p) < k/(k-1)}  (appendix-schedule2.tex, prop:app-s2-TA)
  - T_C(k): min_m inf{p : G_m(p) < 1}                     (TH2 Theorem 5)
for prime k, by bisection on real p (both functions are decreasing in p).
"""
import sys
from math import comb
from functools import lru_cache
import mpmath as mp
mp.mp.dps = 60

def E(k, K, p):  # E_K(k,p), closed form of lem:app-s2-weil-count
    k = mp.mpf(k); K = mp.mpf(K)
    return (k - 1 - k / K + K ** (-k)) * mp.sqrt(p) + k / K - k * K ** (-k)

def UA(K, p):
    Delta = ((K - 1) * (K - 2) * mp.sqrt(p) + 2 * (K - 1)) / (p - K - 1)
    if Delta > mp.mpf(1) / 2:
        return mp.inf
    u = mp.mpf(1) / 2 - Delta / 3 - 1 / (K * (1 - Delta))
    v = Delta / (mp.sqrt(K) * (1 - Delta))
    smax = mp.sqrt(K) * Delta
    if u > 0:
        s = min(max(v / (2 * u), 0), smax)
    else:
        s = smax
    Em = max(-u * s * s + v * s, -u * smax * smax + v * smax, 0)
    return mp.mpf(K) ** K * p ** (K - 1) / (p - 1) ** K + mp.e ** Em

@lru_cache(None)
def S2(n, k):  # Stirling 2nd kind
    if n == k: return 1
    if k == 0 or k > n: return 0
    return k * S2(n - 1, k) + S2(n - 1, k - 1)

@lru_cache(None)
def S2ns(n, k):  # partitions into k blocks of size >= 2
    if n == 0 and k == 0: return 1
    if n <= 0 or k <= 0: return 0
    return k * S2ns(n - 1, k) + (n - 1) * S2ns(n - 2, k - 1)

def G(K, m, p):
    lam = (p - 1) / mp.mpf(K) ** K
    A = sum(S2ns(2 * m, j) * lam ** j for j in range(1, m + 1))
    W = sum(comb(2 * m, j) * lam ** (-j) * sum(S2(j, k) * lam ** k for k in range(0, j + 1))
            for j in range(0, 2 * m + 1))
    dmax = mp.mpf(0)
    for k in range(1, 2 * m + 1):
        eps = mp.mpf(K) ** k * E(k, K, p) / (p - k)
        if eps >= 1: return mp.inf
        d = max((1 + eps) ** (K - 1) - 1, 1 - ((1 - mp.mpf(k) / p) * (1 - eps)) ** (K - 1))
        dmax = max(dmax, d)
    return K * (lam ** (-2 * m) * A + W * dmax)

def bisect(f, lo, hi, it=200):
    # smallest p with f(p) true, f monotone (false then true)
    for _ in range(it):
        mid = mp.sqrt(lo * hi)
        if f(mid): hi = mid
        else: lo = mid
    return hi

def main(Ks):
    print("k | T_A(k) | T_A/k^k | T_C(k) | best m | T_C/k^k | T_A/T_C")
    for K in Ks:
        KK = mp.mpf(K) ** K
        TA = bisect(lambda p: UA(K, p) < mp.mpf(K) / (K - 1), KK / 10, KK * K * 10)
        best = None
        for m in range(1, 9):
            hi = KK * mp.mpf(10) ** 8
            if not G(K, m, hi) < 1: continue
            T = bisect(lambda p: G(K, m, p) < 1, mp.mpf(K) ** 4, hi)
            if best is None or T < best[0]: best = (T, m)
        if best is None:
            print(f"{K} | {mp.nstr(TA,6)} | {mp.nstr(TA/KK,5)} | none | - | - | -")
        else:
            T, m = best
            print(f"{K} | {mp.nstr(TA,6)} | {mp.nstr(TA/KK,5)} | {mp.nstr(T,6)} | {m} | "
                  f"{mp.nstr(T/KK,5)} | {mp.nstr(TA/T,4)}")
        sys.stdout.flush()

if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]])
