"""Central-moment certificate (Theorem 5 of 2026-11-02-rees-threshold-2.md).

n = n_0(y) as in 2026-11-02-rees-weil-threshold.md: y_0 = 0, y_1..y_{K-1}
uniform, n = #{x in Q_0 : x + y_i in Q_{-i}, i >= 1}.  h = (p-1)/K,
Q = K^-(K-1), lam = hQ = (p-1)/K^K.

For f(n) = (1 - n/lam)^(2m) (f(0) = 1, f >= 0) we have P(n=0) <= E f(n), and
    E f(n) <= lam^-2m A_2m(lam) + W_m(lam) * max_{k<=2m} delta_k(p) =: G_m(p)/K,
with
    A_2m(lam) = sum_{j=1}^m S2(2m, j) lam^j,      S2 = partitions with no singleton block,
    W_m(lam)  = sum_{j=0}^{2m} C(2m,j) lam^-j T_j(lam),  T_j = Touchard (sum_k S(j,k) lam^k),
    eps_k     = K^k E_k(p)/(p-k),  E_k = (k-1-k/K+K^-k) sqrt p + k/K - k K^-k  (SPA §2),
    delta_k   = max((1+eps_k)^(K-1) - 1, 1 - ((1-k/p)(1-eps_k))^(K-1)).
Every piece is non-increasing in p, so G_m(p) < 1 at p0 implies it for all p >= p0.

Modes:
  table K0 K1 [mmax]   T_C(K) = min over m of inf{p : G_m(p) < 1}, against T_A.
  check K pmax         exact brute force (all y) at small p: P(n=0) <= E f(n)
                       for the exact moments, and exact E f(n) <= G_m(p)/K.
"""
import sys
from functools import lru_cache
from math import comb

import mpmath as mp

mp.mp.dps = 50


@lru_cache(None)
def stirling2(n, k):
    if n == k:
        return 1
    if k == 0 or k > n:
        return 0
    return k * stirling2(n - 1, k) + stirling2(n - 1, k - 1)


@lru_cache(None)
def assoc_stirling2(n, k):
    """Partitions of an n-set into k blocks, each of size >= 2."""
    if n == 0 and k == 0:
        return 1
    if n <= 0 or k <= 0:
        return 0
    # element n joins an existing block (k ways) of a valid partition of n-1,
    # or forms a pair with one of the other n-1 elements that was a singleton:
    return k * assoc_stirling2(n - 1, k) + (n - 1) * assoc_stirling2(n - 2, k - 1)


def A2m(lam, m):
    return sum(assoc_stirling2(2 * m, j) * lam ** j for j in range(1, m + 1))


def touchard(j, lam):
    return sum(stirling2(j, k) * lam ** k for k in range(0, j + 1))


def Wm(lam, m):
    return sum(comb(2 * m, j) * lam ** (-j) * touchard(j, lam) for j in range(0, 2 * m + 1))


def Ek(p, K, k):
    return (k - 1 - mp.mpf(k) / K + mp.mpf(K) ** (-k)) * mp.sqrt(p) + mp.mpf(k) / K - k * mp.mpf(K) ** (-k)


def delta(p, K, k):
    eps = mp.mpf(K) ** k * Ek(p, K, k) / (p - k)
    if eps >= 1:
        return mp.inf
    return max((1 + eps) ** (K - 1) - 1, 1 - ((1 - mp.mpf(k) / p) * (1 - eps)) ** (K - 1))


def G(p, K, m):
    p = mp.mpf(p)
    lam = (p - 1) / mp.mpf(K) ** K
    if p <= 2 * m + 1 or lam <= 0:
        return mp.inf
    dmax = max(delta(p, K, k) for k in range(1, 2 * m + 1))
    return K * (lam ** (-2 * m) * A2m(lam, m) + Wm(lam, m) * dmax)


def threshold(K, m):
    hi = mp.mpf(K) ** (K + 3)
    if not G(hi, K, m) < 1:
        return None
    lo = mp.mpf(K) ** (K - 2)
    if G(lo, K, m) < 1:
        return lo
    for _ in range(300):
        mid = mp.sqrt(lo * hi)
        if G(mid, K, m) < 1:
            hi = mid
        else:
            lo = mid
        if hi / lo < 1 + mp.mpf(10) ** -8:
            break
    return hi


def table(K0, K1, mmax=20):
    print("kappa | T_C(kappa) | best m | T_C/kappa^kappa | (kappa-1)kappa^kappa | T_A_approx/T_C | log_kappa T_C - kappa")
    for K in range(K0, K1 + 1):
        best = None
        for m in range(1, mmax + 1):
            t = threshold(K, m)
            if t is not None and (best is None or t < best[0]):
                best = (t, m)
        ta = (K - 1) * mp.mpf(K) ** K
        if best is None:
            print(f"{K} | none | - | - | {mp.nstr(ta, 5)} | - | -")
            continue
        t, m = best
        print(f"{K} | {mp.nstr(t, 6)} | {m} | {mp.nstr(t / mp.mpf(K) ** K, 5)} | {mp.nstr(ta, 5)} | "
              f"{mp.nstr(ta / t, 4)} | {mp.nstr(mp.log(t) / mp.log(K) - K, 4)}", flush=True)


def check(K, pmax, mmax=3):
    """Brute force: exact E f(n) and P(n=0) vs the bound G_m(p)/K."""
    from itertools import product
    sys.path.insert(0, ".")
    from bonferroni import coset_index, primes_upto
    for p in primes_upto(pmax):
        if p < 3 or (p - 1) % K:
            continue
        idx = coset_index(p, K)
        Q0 = [x for x in range(1, p) if idx[x] == 0]
        dist = {}
        for y in product(range(p), repeat=K - 1):
            n = 0
            for x in Q0:
                for i in range(1, K):
                    v = (x + y[i - 1]) % p
                    if v == 0 or idx[v] != (-i) % K:
                        break
                else:
                    n += 1
            dist[n] = dist.get(n, 0) + 1
        tot = sum(dist.values())
        lam = mp.mpf(p - 1) / mp.mpf(K) ** K
        p0 = mp.mpf(dist.get(0, 0)) / tot
        line = [f"K={K} p={p} lam={mp.nstr(lam, 4)} P(n=0)={mp.nstr(p0, 5)}"]
        for m in range(1, mmax + 1):
            Ef = sum(c * (1 - mp.mpf(n) / lam) ** (2 * m) for n, c in dist.items()) / tot
            g = G(p, K, m) / K
            ok = (p0 <= Ef + 1e-30) and (Ef <= g)
            line.append(f"m={m}: Ef={mp.nstr(Ef, 4)} G/K={mp.nstr(g, 4)} {'ok' if ok else 'FAIL'}")
        print(" | ".join(line), flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "table":
        table(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 20)
    elif sys.argv[1] == "check":
        check(int(sys.argv[2]), int(sys.argv[3]))
