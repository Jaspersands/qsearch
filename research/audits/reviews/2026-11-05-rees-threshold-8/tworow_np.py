"""Complete two-row exceptional sets E2row(kappa) via cyclotomic numbers [computed, exact].
Theorem 2 of the report: p in E2row(kappa) iff A(u,v) = 0 for some (u,v) with u != 0, v != eps,
u != v, where A(u,v) = #{w in Q_u : w-1 in Q_v} and eps = ind(-1).  E2row is contained in E_2.
Completeness: |k^2 A(u,v) - (p-2)| <= (k-1)(k-2) sqrt(p) + 3(k-1) (Jacobi sums), so E2row is
empty for p > W2(k); we scan every prime p = 1 mod k up to W2(k).
Discrete logs are computed with numpy from a primitive root g (sympy), classes ind = e mod k.
Usage: python tworow_np.py KMIN KMAX [--check-against tworow_k4-9.out]"""
import sys, math
import numpy as np
from sympy import primerange, primitive_root
def W2(k):
    a = (k-1)*(k-2); c = 3*(k-1) + 2
    s = (a + math.sqrt(a*a + 4*c))/2       # p - a sqrt p - c > 0 for sqrt p > s
    return int(s*s) + 1
def ind_table(p, k):
    g = primitive_root(p); m = int(math.isqrt(p)) + 1
    small = np.empty(m, dtype=np.int64); x = 1
    for r in range(m):
        small[r] = x; x = x*g % p
    gm = x                                  # g^m
    nblk = (p - 1 + m - 1)//m
    big = np.empty(nblk, dtype=np.int64); y = 1
    for b in range(nblk):
        big[b] = y; y = y*gm % p
    pw = (big[:, None]*small[None, :] % p).ravel()[:p-1]   # pw[e] = g^e
    ind = np.full(p, -1, dtype=np.int64)
    ind[pw] = np.arange(p-1, dtype=np.int64) % k
    assert (ind[1:] >= 0).all() and ind[1] == 0
    return ind
def tworow(p, k):
    ind = ind_table(p, k)
    w = np.arange(2, p, dtype=np.int64)
    A = np.bincount(ind[w]*k + ind[w-1], minlength=k*k).reshape(k, k)
    eps = int(ind[p-1])
    bad = [(u, v) for u in range(1, k) for v in range(k) if v != eps and u != v and A[u, v] == 0]
    return bad, int(A.sum())
kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
for k in range(kmin, kmax+1):
    W = W2(k); mem = []; n = 0
    for p in primerange(3, W+1):
        if p % k != 1: continue
        n += 1
        bad, tot = tworow(p, k)
        assert tot == p-2
        if bad: mem.append(p)
    print(f"E2ROW k={k} W2={W} primes_scanned={n} members={len(mem)} max={max(mem) if mem else None} "
          f"max/k^2={max(mem)/k**2 if mem else 0:.2f} list={','.join(map(str,mem))}", flush=True)
