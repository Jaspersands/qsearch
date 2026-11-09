"""Poisson-orbit model with NO fitted constant [conjecture/float].
Pr[p in E_2(k)] = exp(-mu_G(p)/(2k^2)), mu_G = p^(2k-2) q^(k^2-1), q = (h+1)/p (TH6 Conj 6.4).
2k^2 = size of the recentring x transpose group acting on normalised solutions (dfs2b PRUNE 2).
Predicted largest member p*: the largest p with  sum_{p' >= p} Pr[p' in E_2] >= 1/2.
Prints p*/k^((k+1)/2) and the expected number of members above k^((k+1)/2)."""
import math
from sympy import primerange
def logmu(p, k):
    h = (p-1)//k
    return (2*k-2)*math.log(p) + (k*k-1)*math.log((h+1)/p)
for k in (4, 5, 6, 7, 8, 9, 10, 12, 16, 20):
    X = k**((k+1)/2)
    hi = int(6*X); lo = int(0.2*X)
    if k <= 10:
        ps = [p for p in primerange(lo, hi) if p % k == 1]
    else:   # density approximation on a log grid: primes = 1 mod k have density 1/(phi(k) ln p)
        from sympy import totient
        ph = int(totient(k)); ps = None
    acc = 0.0; pstar = None; above = 0.0
    if ps is not None:
        for p in reversed(ps):
            pr = math.exp(-math.exp(logmu(p, k))/(2*k*k)) if logmu(p, k) < 700 else 0.0
            acc += pr
            if p >= X: above += pr
            if pstar is None and acc >= 0.5: pstar = p
    else:
        N = 200000; t1, t0 = math.log(hi), math.log(lo)
        for s in range(N, 0, -1):
            t = t0 + (t1-t0)*s/N; p = math.exp(t); dp = p*(t1-t0)/N
            lm = (2*k-2)*math.log(p) + (k*k-1)*math.log(1/k + 1/p)
            pr = math.exp(-math.exp(lm)/(2*k*k)) if lm < 700 else 0.0
            w = pr*dp/(ph*math.log(p)); acc += w
            if p >= X: above += w
            if pstar is None and acc >= 0.5: pstar = p
    print(f"k={k}: predicted max E_2 ~ {pstar:.4g} = {pstar/X:.3f} k^((k+1)/2); expected members above k^((k+1)/2): {above:.1f}")
