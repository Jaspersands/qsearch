"""Falsification check of WeilLower K kappa for K = F_p:
for all eps, eta != 0:  p - (kappa-1)^2 sqrt(p) <= N(u^kappa + eps v^kappa = eta).
N depends only on the cosets of eps, eta modulo the d-th powers, d = gcd(kappa, p-1),
so one representative per coset pair is enough. Also records min margin in the
regime used by the paper (kappa even, p >= 4 kappa^4)."""
import math, sys
import numpy as np
from sympy import primerange, primitive_root

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
worst = {}
viol = []
for p in primerange(3, PMAX):
    g = primitive_root(p)
    for kappa in range(1, 10):
        d = math.gcd(kappa, p - 1)
        m = np.zeros(p, dtype=np.int64)          # m[y] = #{x : x^kappa = y}
        xs = np.arange(p, dtype=object)
        for x in range(p):
            m[pow(x, kappa, p)] += 1
        reps = [pow(g, i, p) for i in range(d)]   # coset representatives of F_p^x / P_d
        bound = p - (kappa - 1) ** 2 * math.sqrt(p)
        ys = np.arange(p)
        for eps in reps:
            inv = pow(eps, p - 2, p)
            for eta in reps:
                # N = sum_y m[y] * m[(eta - y)/eps]
                idx = ((eta - ys) % p) * inv % p
                N = int((m * m[idx]).sum())
                margin = N - bound
                if margin < 0:
                    viol.append((p, kappa, eps, eta, N, bound))
                if kappa % 2 == 0 and p >= 4 * kappa ** 4:
                    key = kappa
                    if key not in worst or margin < worst[key][0]:
                        worst[key] = (margin, p, eps, eta, N)
print("PMAX", PMAX)
print("violations", len(viol), viol[:5])
for k in sorted(worst):
    print("kappa", k, "min margin in used regime (margin,p,eps,eta,N):", worst[k])
