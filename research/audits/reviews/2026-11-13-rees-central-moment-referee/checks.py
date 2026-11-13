import sys, math; sys.path.insert(0, '.')
from gm import *

def m_of(K): return math.ceil(math.log(4 * K))

# (1) Condition (C) of Corollary 5': K^(K/2) >= 49 m 4^m K^(2m+2), exact integer test (squared)
print("== (C) exact integer test, K = 3..3000; log test with margin 3000..20000")
fails = []
for K in range(3, 3001):
    m = m_of(K)
    if not (K ** K >= (49 * m) ** 2 * 16 ** m * K ** (4 * m + 4)): fails.append(K)
for K in range(3001, 20001):
    m = m_of(K)
    lhs = (K / 2 - 2 * m - 2) * math.log(K); rhs = math.log(49 * m) + m * math.log(4)
    if not lhs > rhs + 1: fails.append(K)
print("fails:", fails[-8:], "max fail", max(fails))
# m_of check (math.log vs mpmath) for jumps
bad = [K for K in range(3, 20001) if m_of(K) != int(mp.ceil(mp.log(4 * K)))]
print("m_of float/mp disagreements:", bad)
# tail K >= 20000: m <= ln(4K)+1 <= 2 ln K ; f(K) = (K/2 - 4 lnK - 2) lnK - ln(98 lnK) - 2 lnK ln4
f = lambda K: (K / 2 - 4 * math.log(K) - 2) * math.log(K) - math.log(98 * math.log(K)) - 2 * math.log(K) * math.log(4)
print("tail f(20000) =", f(20000), "(f increasing for K>=20000 since df/dK >= lnK/2 - O(lnK/K) > 0)")
# also the LHS/RHS derivative sanity: f increasing on [20000, 1e9] sample
print("f increasing on samples:", all(f(a) < f(b) for a, b in zip([2e4 * 2 ** i for i in range(15)], [2e4 * 2 ** (i + 1) for i in range(15)])))

# (2) direct G_m(p*) at p* = lam* K^K + 1, lam* = 4e m^2
print("== Cor 5' direct: G_m(p*) with m = ceil(ln 4K)")
worst = 0
for K in list(range(32, 81)) + [100, 150, 200, 300, 500, 1000]:
    m = m_of(K); lam = 4 * mp.e * m * m
    g = G(mp.mpf(K) ** K * lam + 1, K, m)
    worst = max(worst, g)
    if K in (32, 33, 37, 38, 45, 60, 80, 100, 500, 1000): print(K, m, mp.nstr(g, 5))
print("worst G over list:", mp.nstr(worst, 5))
# also the crude bound components at K=32 to see the slack in each step
K = 32; m = m_of(K); lam = 4 * mp.e * m * m; p = mp.mpf(K) ** K * lam + 1
main = K * sum(S2ns(2*m, j) * lam ** (j - 2*m) for j in range(1, m+1))
print("K=32 main term K*lam^-2m A =", mp.nstr(main, 5), " bound 1/4")

# (3) kappa >= 15 improvement on T_A: show min_m G_m((K-1)K^K) < 1 (T_A > (K-1)K^K proved)
print("== T_C < (K-1)K^K < T_A: direct test at p0 = (K-1)K^K for 15 <= K <= K1")
# K1: least K >= 250 with 4e(ln 4K + 1)^2 + 1 < K - 1 ; beyond K1, Cor 5' gives T_C <= lam*K^K+1 < (K-1)K^K
K1 = next(K for K in range(250, 10**6) if 4 * math.e * (math.log(4 * K) + 1) ** 2 + 1 < K - 1)
print("K1 =", K1, "; need also K>=32 for Cor 5' (holds)")
# exact (ceil) version: least K with 4e ceil(ln4K)^2 + K^-K < K-1 for all K >= it up to 1e5
ok_from = None
for K in range(32, 100001):
    good = 4 * math.e * m_of(K) ** 2 + 1e-30 < K - 1
    if good and ok_from is None: ok_from = K
    if not good: ok_from = None
print("4e ceil(ln4K)^2 < K-1 for all K in [", ok_from, ", 1e5]")
failK = []
maxg = 0
for K in range(15, K1 + 1):
    p0 = (K - 1) * mp.mpf(K) ** K
    g, m = Gmin(p0, K, mmax=10)
    maxg = max(maxg, g)
    if not g < 1: failK.append(K)
    if K in (15, 16, 20, 30, 50, 100, 200, 400, K1): print(K, "min_m G(p0) =", mp.nstr(g, 5), "m =", m, flush=True)
print("failures:", failK, " max G(p0) over [15, K1] =", mp.nstr(maxg, 5))
for K in (13, 14):
    p0 = (K - 1) * mp.mpf(K) ** K
    print("K =", K, "min_m G((K-1)K^K) =", mp.nstr(Gmin(p0, K)[0], 5), "; T_C > T_A? ", TC(K)[0] > TA(K))

# (4) TH9 Corollary 3 range (C): G_2 at lam = sqrt(8K)
print("== TH9 range (C): G_2 at p = sqrt(8K) K^K + 1")
for K in (729, 1000, 1677, 10**4, 10**5, 10**6):
    lam = mp.sqrt(8 * K); p = mp.mpf(K) ** K * lam + 1
    g = G(p, K, 2)
    main = K * (3 / lam ** 2 + 1 / lam ** 3)
    epsstar = 8 * mp.mpf(K) ** 4 / mp.sqrt(p)
    print(K, "G_2 =", mp.nstr(g, 8), "main =", mp.nstr(main, 8), "excess =", mp.nstr(g - main, 4),
          "(K-1)eps* =", mp.nstr((K - 1) * epsstar, 4))

# (5) data consistency: known E_2 members must have G_m >= 1 for all m
print("== data: min_m G_m at known E_2 members (must be >= 1 or inf)")
E27 = [int(x) for x in open('../2026-11-02-rees-threshold-2/E2_k7.txt').read().split() if x.isdigit()]
print("E_2(7) list length", len(E27), "max", max(E27))
print("kappa=7 min over list of min_m G:", mp.nstr(min(Gmin(q, 7)[0] for q in E27), 5))
for K, q in ((5, 181), (8, 14281), (9, 24967), (4, 53), (6, 859)):
    print("kappa", K, "p", q, "min_m G =", mp.nstr(Gmin(q, K)[0], 5), " p/T_C =", mp.nstr(q / TC(K)[0], 4))
