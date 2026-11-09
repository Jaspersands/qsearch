"""Theorem O2 (the (kappa-1)-wise obstruction): exact checks.

Part A (exchangeable law, exact rationals).  For kappa in [2, 20] and q on a rational
grid, the unique signed law on W in {0..kappa} with E(W)_k = (kappa)_k q^k (k < kappa)
and P(W = kappa) = 0 is
    w'_z = C(kappa,z) q^z [ (1-q)^(kappa-z) - (-q)^(kappa-z) ].
Check: (i) total mass 1 and factorial moments k <= kappa-1 equal those of Bin(kappa,q);
(ii) w' >= 0 iff q <= 1/2; (iii) for q > 1/2 the minimum of P(W = kappa) over all
nonnegative laws with those moments is q^kappa - q^(kappa-d)(1-q)^d, d = largest even
number <= kappa.  (iii) is checked by the one-parameter description of the fibre.

Part B (general laws, LP in floating point).  For kappa <= 6, minimise P(all ones) over
ALL laws on {0,1}^kappa whose marginals on every set of <= kappa-1 coordinates are those
of iid Bernoulli(q); compare with the formula in (iii) (0 for q <= 1/2).

Part C (thresholds).  q_bin(p) = 1 - (1 - kappa^-(kappa-1))^((p-1)/kappa); the largest
real p with q_bin <= 1/2, and the rigorous bound kappa^kappa/2 (true q <= E n < p/kappa^kappa).
Usage: obstruction_law.py
"""
from fractions import Fraction as F
from math import comb, log, log1p

import numpy as np
from scipy.optimize import linprog
from itertools import combinations, product


def ff(z, k):
    r = 1
    for t in range(k):
        r *= (z - t)
    return r


def law(K, q):
    return [comb(K, z) * q ** z * ((1 - q) ** (K - z) - (-q) ** (K - z)) for z in range(K + 1)]


def minall_formula(K, q):
    if q <= F(1, 2):
        return F(0)
    d = K if K % 2 == 0 else K - 1
    return q ** K - q ** (K - d) * (1 - q) ** d


def partA():
    bad = 0
    grid = [F(a, 40) for a in range(1, 40)]
    for K in range(2, 21):
        for q in grid:
            w = law(K, q)
            ok_mass = sum(w) == 1
            ok_mom = all(sum(ff(z, k) * w[z] for z in range(K + 1)) == ff(K, k) * q ** k for k in range(K))
            nonneg = all(x >= 0 for x in w)
            if not (ok_mass and ok_mom and w[K] == 0 and nonneg == (q <= F(1, 2))):
                bad += 1
                print("FAIL A", K, q, ok_mass, ok_mom, nonneg)
            # (iii): fibre = Bin + t * delta, delta_z = (-1)^(K-z) C(K,z); P(W=K) = q^K + t
            binw = [comb(K, z) * q ** z * (1 - q) ** (K - z) for z in range(K + 1)]
            lo = max(-binw[z] / comb(K, z) for z in range(K + 1) if (K - z) % 2 == 0)
            hi = min(binw[z] / comb(K, z) for z in range(K + 1) if (K - z) % 2 == 1)
            assert lo <= hi
            if q ** K + lo != minall_formula(K, q):
                bad += 1
                print("FAIL iii", K, q)
    print(f"Part A: kappa 2..20, q in (1/40..39/40): failures = {bad}")


def partB():
    worst = 0.0
    for K in range(2, 7):
        pts = list(product((0, 1), repeat=K))
        for qn in range(1, 20):
            q = qn / 20
            A, b = [], []
            for r in range(K):           # all subsets S with |S| <= K-1, all assignments
                for S in combinations(range(K), r):
                    for a in product((0, 1), repeat=r):
                        A.append([1.0 if all(x[s] == a[i] for i, s in enumerate(S)) else 0.0 for x in pts])
                        b.append(np.prod([q if ai else 1 - q for ai in a]))
            c = [1.0 if all(x) else 0.0 for x in pts]
            res = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method="highs")
            f = float(minall_formula(K, F(qn, 20)))
            worst = max(worst, abs(res.fun - f))
            if abs(res.fun - f) > 1e-9:
                print("FAIL B", K, q, res.fun, f)
    print(f"Part B: kappa 2..6, q = 0.05..0.95: max |LP min - formula| = {worst:.2e}")


def partC():
    print("kappa | p with q_bin = 1/2 | /kappa^kappa | kappa^kappa/2 | (kappa-1)kappa^kappa (< T_A)")
    for K in range(3, 21):
        Q = float(K) ** (1 - K)
        p_half = 1 + K * log(2) / (-log1p(-Q))
        print(f"{K} | {p_half:.6g} | {p_half / K ** K:.6f} | {K ** K / 2:.6g} | {(K - 1) * K ** K:.6g}")


partA()
partB()
partC()
