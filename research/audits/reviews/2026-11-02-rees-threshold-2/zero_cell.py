"""Zero-cell (matching) sub-family of two-level contractions.

If -1 is a kappa-th power (h even) and s != 0, put beta_i = -alpha_{i-s}.  Then cell
(i, i-s) is 0 and cell (i, j) = alpha_j - alpha_{i-s}, so the contraction conditions
become: alpha_j - alpha_k in Q_{-(j+k+s)} for all j != k (a 'coloured clique' in
the Cayley colouring of F_p by cosets of differences), with cell (0,0) = alpha_0 - alpha_{-s} != 0.
This script searches the sub-family by DFS at small (p, kappa), re-checks every
kappa^2 cell of the resulting (alpha, beta) against A_{-(i+j)}, and reports the
first prime from which the sub-family is always nonempty in the tested range.
Usage: zero_cell.py K pmax"""
import sys
sys.path.insert(0, '.')
from bonferroni import coset_index, primes_upto
K, pmax = int(sys.argv[1]), int(sys.argv[2])
def search(p, idx, s):
    # alpha_0 = 0 by translation; DFS over alpha_1..alpha_{K-1}
    a = [0]
    def ok(x, k):
        for j, aj in enumerate(a):
            d = (x - aj) % p
            if d == 0 or idx[d] != (-(j + k + s)) % K:
                return False
        return True
    def dfs(k):
        if k == K:
            return True
        for x in range(1, p):
            if ok(x, k):
                a.append(x)
                if dfs(k + 1):
                    return True
                a.pop()
        return False
    return a if dfs(1) else None
for p in primes_upto(pmax):
    if p < 3 or (p - 1) % K or ((p - 1) // K) % 2:
        continue
    idx = coset_index(p, K)
    res = None
    for s in range(1, K):
        a = search(p, idx, s)
        if a:
            res = (s, a); break
    if res is None:
        print(f"p={p}: no zero-cell solution"); continue
    s, a = res
    beta = [(-a[(i - s) % K]) % p for i in range(K)]
    good = all(((a[j] + beta[i]) % p == 0 and (i, j) != (0, 0)) or ((a[j] + beta[i]) % p != 0 and idx[(a[j] + beta[i]) % p] == (-(i + j)) % K)
               for i in range(K) for j in range(K))
    print(f"p={p}: s={s} alpha={a} beta={beta} contraction_check={'ok' if good else 'FAIL'}")
