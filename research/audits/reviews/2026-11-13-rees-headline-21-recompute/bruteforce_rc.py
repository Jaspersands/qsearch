"""Cross-check rcsearch's exhaustive verdicts against a brute force that uses only the
translation normalisation beta_0 = 0 (no scaling), classes by the power test (rc.ClassOracle)."""
import itertools, numpy as np, sys
from rc import RCSearch, ClassOracle
from plus import lift
def brute(p, D, R, K):
    O = ClassOracle(p, D); K = set(K)
    clv = np.array([-1] + [O.cl(x) for x in range(1, p)])
    xs = np.arange(p)
    Rn = [i for i in R if i]
    for bs in itertools.product(range(p), repeat=len(Rn)):
        beta = dict(zip(Rn, bs)); beta[0] = 0; ok = True
        for j in range(D):
            good = np.ones(p, bool)
            if j == 0: good &= (xs != 0) & (clv[xs] == 0)
            for i in R:
                v = (xs + beta[i]) % p
                good &= (v == 0) | np.isin((clv[v] + i + j) % D, list(K))
            if not good.any(): ok = False; break
        if ok: return True
    return False
S = RCSearch(None); n = agree = 0; dis = []
for p, rmax in [(7, 6), (13, 4), (19, 3), (31, 3), (37, 3), (73, 3), (11, 5)]:
    for D in range(2, 10):
        if (p - 1) % D: continue
        subsets = [frozenset((0,) + c) for sz in range(0, 3) for c in itertools.combinations(range(1, D), sz)]
        Rs = set()
        for Dp in [x for x in range(1, D) if D % x == 0]:
            for Kp in ([frozenset({0})] if Dp == 1 else [frozenset((0,) + c) for sz in range(0, 3) for c in itertools.combinations(range(1, Dp), sz)]):
                Rs.add(lift(Kp, Dp, D))
        Rs |= {K for K in subsets if len(K) >= 2}
        for R in Rs:
            if len(R) < 2 or len(R) > rmax: continue
            for K in subsets:
                st, _ = S.query(p, D, sorted(R), sorted(K), "e", 10**9)
                b = brute(p, D, sorted(R), sorted(K)); n += 1
                if (st == "FOUND") == b and st != "UNKNOWN": agree += 1
                else: dis.append((p, D, sorted(R), sorted(K), st, b))
print("cases", n, "agree", agree, "disagreements", dis[:10])
