"""Exact exceptional sets of union chains at kappa = 5, 7 (check of threshold-7 Section 4.4).

A chain Z_k -> K_1 -> ... -> K_{L-1} -> {0} has steps RC(k; R_t -> K_t) with R_1 = Z_k and
R_t = K_{t-1}.  Each step at modulus kappa is a row-restriction of a two-level contraction, so a
chain can fail only on E_2(kappa); E_2(5), E_2(7) are the sets of the paper (threshold-2 Thm 6).
Union targets depend on the coset generator: for xi' = xi^u q the condition RC_{xi'}(R -> K) is
RC_xi(uR -> uK).  So every chain is decided for each unit u (generator g^u, g the least primitive
root).  Every FEASIBLE verdict is re-checked by rc.check (pow-based).
"""
import sys
from rc import feasible, is_prime
E2 = {5: [11, 31, 41, 61, 71, 101, 131, 151, 181],
      7: [int(x) for x in """29 43 71 113 127 197 211 239 281 337 379 421 449 463 491 547 617 631 659
    673 701 743 757 827 883 911 953 1009 1051 1093 1163 1289 1303 1373 1471
    1499 1583 1597 1667 1709 1877 2017 2087 2143 2213 2297 2339 2381 2423
    2591 2731 2801 2843 2969 3137 3221""".split()]}
assert len(E2[7]) == 56 and max(E2[7]) == 3221
chains = {5: [[[0, 1]], [[0, 1, 2]], [[0, 1, 2], [0, 1]]],
          7: [[[0, 1, 2, 3]], [[0, 1, 2]], [[0, 1, 2], [0, 1]], [[0, 1, 3], [0, 1]]]}
cache = {}
def dec(p, D, R, K):
    key = (p, D, tuple(sorted(R)), tuple(sorted(K)))
    if key not in cache:
        st, a, b, n = feasible(p, D, list(key[2]), list(key[3]))
        assert st in (0, 1), key
        cache[key] = st
    return cache[key]
for kap in (5, 7):
    units = [u for u in range(1, kap)]
    for Ks in chains[kap]:
        fails = {}
        for u in units:
            bad = []
            for p in E2[kap]:
                R = list(range(kap)); ok = True
                for K in Ks + [[0]]:
                    uK = sorted({(u * k) % kap for k in K})
                    if not dec(p, kap, R, uK): ok = False; break
                    R = uK
                if not ok: bad.append(p)
            fails[u] = bad
        name = " -> ".join(["Z_%d" % kap] + [str(set(K)) for K in Ks] + ["{0}"])
        print("kappa=%d chain %s" % (kap, name))
        for u in units: print("   generator g^%d: fails at %s" % (u, fails[u]))
        allf = sorted(set.intersection(*[set(v) for v in fails.values()]))
        print("   fails for every generator: %s ; for some generator: %s" % (allf, sorted(set.union(*[set(v) for v in fails.values()]))), flush=True)
print("decisions: %d feasible (pow-checked), %d infeasible" % (sum(cache.values()), len(cache) - sum(cache.values())))
# Lemma 4.5 spot check: off E_2 every step of these chains is feasible
miss = []
for kap, top in [(5, 1200), (7, 1200)]:
    for p in range(kap + 1, top, kap):
        if not is_prime(p) or p in E2[kap]: continue
        for Ks in chains[kap]:
            R = list(range(kap))
            for K in Ks + [[0]]:
                if not dec(p, kap, R, K): miss.append((kap, p, tuple(R), tuple(K)))
                R = K
print("off-E_2 spot check (p < 1200): failing steps:", miss)
