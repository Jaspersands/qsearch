# Prop 6: with beta_i = xi^{-i}-1 (i in R), alpha_0 = 1, every X_j (j != 0) nonempty for p >= ((r-1)k^r+2)^2.
import itertools
from sympy import primerange, primitive_root
from common import setup
def ok(p, k, R):
    ind, g = setup(p, k)
    beta = {i: (pow(g, (-i) % (p-1), p) - 1) % p for i in R}
    assert len(set(beta.values())) == len(R)
    for i in R: assert ind[(1 + beta[i]) % p] == (-i) % k
    for j in range(1, k):
        if not any(all(((x + beta[i]) % p) and ind[(x + beta[i]) % p] == (-(i + j)) % k for i in R) for x in range(p)):
            return False
    return True
for k, r, lo, hi in [(3, 2, 2, 400), (4, 2, 2, 800), (5, 2, 2, 1200), (3, 3, 2, 4000), (4, 3, 2, 20000)]:
    B = ((r-1)*k**r + 2)**2
    fails = []
    for p in primerange(lo, hi):
        if (p - 1) % k: continue
        for R in itertools.combinations(range(k), r):
            if not ok(p, k, R): fails.append(p); break
    above = [p for p in fails if p >= B]
    print(f"k={k} r={r} bound={B} largest failing p={max(fails) if fails else None} failures>=bound={above}")
