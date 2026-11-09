"""For kappa <= 12: exact number N_full of balanced e touching every row and column, T_A(kappa)
(bisection on U_kappa of appendix-schedule2.tex), and the largest mean square-root constant
m* = T_A^(kappa-1) / N_full for which the v = 2 kappa class alone stays below S0 at p = T_A.
Also (kappa-1)^(kappa+1) and the class-only ideal threshold (m N_full)^(1/(kappa-1)) for m = 0.2, 0.42.
"""
from math import comb, exp, sqrt
from mpmath import mp, mpf, findroot
mp.dps = 40


def N_full(K):
    tot = 0
    for r2 in range(K + 1):
        for c2 in range(K + 1):
            m = r2 * c2
            B = mpf(K) ** (m - 1) if m >= 1 else 1
            tot += (-1) ** (2 * K - r2 - c2) * comb(K, r2) * comb(K, c2) * B
    return tot


def U(K, p):
    p = mpf(p)
    D = ((K - 1) * (K - 2) * mp.sqrt(p) + 2 * (K - 1)) / (p - K - 1)
    u = mpf(1) / 2 - D / 3 - 1 / (K * (1 - D))
    v = D / (mp.sqrt(K) * (1 - D))
    smax = mp.sqrt(K) * D
    s = v / (2 * u) if u > 0 else smax
    s = min(max(s, 0), smax)
    E = max(-u * s * s + v * s, -u * smax ** 2 + v * smax, 0)
    return K ** K * p ** (K - 1) / (p - 1) ** K + mp.e ** E, D


def TA(K):
    lo, hi = mpf(K + 2), mpf(K) ** (K + 2)
    for _ in range(200):
        mid = (lo + hi) / 2
        Uv, D = U(K, mid)
        if D <= 0.5 and Uv < mpf(K) / (K - 1):
            hi = mid
        else:
            lo = mid
    return hi


print("kappa  N_full/kappa^(k^2-1)  T_A  T_A/((k-1)k^k)  m*  ideal(m=0.2)/T_A  ideal(m=0.42)/T_A  (k-1)^(k+1)/T_A")
for K in range(3, 13):
    N = N_full(K)
    T = TA(K)
    ms = T ** (K - 1) / N
    i1 = (0.2 * N) ** (mpf(1) / (K - 1)) / T
    i2 = (0.42 * N) ** (mpf(1) / (K - 1)) / T
    print(f"{K:3d}  {float(N / mpf(K) ** (K * K - 1)):.4f}  {float(T):.4g}  {float(T / ((K - 1) * mpf(K) ** K)):.4f}  "
          f"{float(ms):.3f}  {float(i1):.3f}  {float(i2):.3f}  {float(mpf(K - 1) ** (K + 1) / T):.3g}")
