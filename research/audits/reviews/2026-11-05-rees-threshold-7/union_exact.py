"""Exact exceptional sets of union chains for kappa = 5, 7 (report Section 4.4).

Every step of a union chain has modulus kappa, so by Lemma 4.5 (restriction of a two-level
contraction) it can fail only at p in E_2(kappa).  E_2(5) and E_2(7) are known exactly, so the
exceptional set of a chain is decided by running each step at those primes only.
Steps are decided by the complete DFS of rectu.c (ALLOWDUP=1 for union targets); every FEASIBLE
witness is re-checked by adaptive_chain.check_pair (pow-based, separately written).
Interpreter: /opt/anaconda3/bin/python.
"""
import subprocess, os, sys
from adaptive_chain import check_pair, primroot

HERE = os.path.dirname(os.path.abspath(__file__))
E2 = {5: [11, 31, 41, 61, 71, 101, 131, 151, 181],
      7: [29, 43, 71, 113, 127, 197, 211, 239, 281, 337, 379, 421, 449, 463, 491, 547, 617, 631, 659,
          673, 701, 743, 757, 827, 883, 911, 953, 1009, 1051, 1093, 1163, 1289, 1303, 1373, 1471,
          1499, 1583, 1597, 1667, 1709, 1877, 2017, 2087, 2143, 2213, 2297, 2339, 2381, 2423,
          2591, 2731, 2801, 2843, 2969, 3137, 3221]}

def decide(p, D, R, K):
    env = dict(os.environ); env['ALLOWDUP'] = '0' if list(K) == [0] else '1'
    out = subprocess.run([os.path.join(HERE, 'rectu'), str(D), ','.join(map(str, R)), ','.join(map(str, K)),
                          str(p), str(p), '1', '1'], capture_output=True, text=True, env=env).stdout.split()
    if out[1] == 'INFEASIBLE': return False
    assert out[1] == 'FEASIBLE'
    g = int(out[2].split('=')[1]); assert g == primroot(p)
    bi = out.index('beta'); ai = out.index('alpha')
    beta = dict(zip(R, map(int, out[bi+1:ai]))); alpha = list(map(int, out[ai+1:ai+1+D]))
    assert check_pair(p, g, D, R, K, alpha, beta), "witness rejected"
    return True

def chain_steps(kappa, Ks):
    """Ks = [K_1, ..., K_{L-1}] (union targets); last target {0}"""
    steps, R = [], list(range(kappa))
    for K in Ks + [[0]]:
        steps.append((kappa, R, K)); R = K
    return steps

if __name__ == "__main__":
    chains = {5: [[[0, 1]], [[0, 1, 2]], [[0, 1, 3]], [[0, 1, 2], [0, 1]]],
              7: [[[0, 1, 2, 3]], [[0, 1, 2]], [[0, 1, 3]], [[0, 1, 2], [0, 1]], [[0, 1, 3], [0, 1]]]}
    cache = {}
    for kappa in [5, 7]:
        for Ks in chains[kappa]:
            steps = chain_steps(kappa, Ks)
            bad = []
            for p in E2[kappa]:
                ok = True
                for (D, R, K) in steps:
                    key = (p, D, tuple(R), tuple(K))
                    if key not in cache: cache[key] = decide(p, D, R, K)
                    if not cache[key]: ok = False; break
                if not ok: bad.append(p)
            print("kappa=%d chain Z_%d -> %s -> {0}: fails exactly at %s (all other p = 1 mod %d covered)" % (
                kappa, kappa, " -> ".join(str(set(K)) for K in Ks), bad, kappa), flush=True)
        # union over the chains listed
    print("step decisions:", sum(cache.values()), "feasible (witness re-checked),", len(cache) - sum(cache.values()), "infeasible (complete DFS)")
