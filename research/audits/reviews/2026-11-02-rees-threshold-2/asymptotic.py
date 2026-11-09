"""Theorem 5(b): explicit range.  m = ceil(ln 4K), lam* = 4e m^2.
Condition (C): K^(K/2) >= 49 m 4^m K^(2m+2).  Prints the least K0 such that (C)
holds for every K in [K0, 20000], and checks G_m(p*) < 1 directly (exact form
from central_moment.G) at p* = K^K lam* + 1 for K in [K0, K0+40] and a few larger K."""
import math, sys
sys.path.insert(0, '.')
import mpmath as mp
from central_moment import G
def m_of(K): return math.ceil(math.log(4 * K))
def cond(K):
    m = m_of(K)
    return (K / 2 - 2 * m - 2) * math.log(K) >= math.log(49 * m) + m * math.log(4)
bad = [K for K in range(3, 20001) if not cond(K)]
K0 = max(bad) + 1
print("K0 =", K0, "; (C) fails at", bad[-5:])
for K in list(range(K0, K0 + 41)) + [100, 200, 500]:
    m = m_of(K)
    lam = 4 * math.e * m * m
    p = mp.mpf(K) ** K * lam + 1
    g = G(p, K, m)
    print(K, "m=%d" % m, "lam*=%.1f" % lam, "G_m(p*)=%s" % mp.nstr(g, 4), "ok" if g < 1 else "FAIL",
          "exponent excess log_K(lam*)=%.4f" % (math.log(lam) / math.log(K)))
