"""Empirical check of the second-moment bound of Proposition 4.1 (union steps).

For a step RC(kappa; R -> K), draw beta_0 = 0 and beta_i (i in R \\ 0) uniform, and test whether
every X_j = {x : x + beta_i in A_ij for all i in R} is nonempty, where A_ij = U_{k in K} Q_{k-i-j}
(nonzero cells only) for (i,j) != (0,0) and A_00 = Q_0.  The proof gives
   Pr[some X_j empty] <= LHS(p)            (union_threshold.lhs_union).
We print the empirical failure rate next to LHS(p) at primes just above T_U.
Interpreter: /opt/anaconda3/bin/python.
"""
import sys, random
import numpy as np
from union_threshold import lhs_union, T_U
from barrier import cls_table, primes_1mod

def fail_rate(p, kappa, R, K, draws, rng):
    g, cl = cls_table(p, kappa)
    xs = np.arange(p)
    fails = 0
    for _ in range(draws):
        beta = {0: 0}
        for i in R:
            if i: beta[i] = rng.randrange(p)
        ok = True
        for j in range(kappa):
            good = np.ones(p, dtype=bool)
            for i in R:
                c = cl[(xs + beta[i]) % p]
                if i == 0 and j == 0: allowed = {0}
                else: allowed = set((k - i - j) % kappa for k in K)
                good &= np.isin(c, list(allowed))
                if not good.any(): break
            if not good.any(): ok = False; break
        fails += (not ok)
    return fails / draws

if __name__ == "__main__":
    rng = random.Random(11)
    cases = [(5, list(range(5)), [0, 1, 2]), (7, list(range(7)), [0, 1, 2]), (7, [0, 1, 2], [0, 1]),
             (5, [0, 1, 2], [0, 1]), (7, [0, 1], [0])]
    draws = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    for kappa, R, K in cases:
        t = float(T_U(kappa, len(R), K))
        ps = [p for p in primes_1mod(kappa, int(t)+1, int(1.6*t)+50)][:4]
        for p in ps:
            L = float(lhs_union(kappa, len(R), K, p))
            fr = fail_rate(p, kappa, R, K, draws, rng)
            print("kappa=%d R=%s K=%s T_U=%.1f p=%d: empirical Pr[some X_j empty] = %.3f <= LHS(p) = %.3f : %s" % (
                kappa, R, K, t, p, fr, L, fr <= L), flush=True)
