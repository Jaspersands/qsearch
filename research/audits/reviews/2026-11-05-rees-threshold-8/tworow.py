"""Two-row criterion (threshold-8, Theorem 2) [computed].
p in E2row(kappa)  <=>  some difference set (Q_0 u {0}) - (Q_b u {0}), b != 0, misses a nonzero element.
By Theorem 2 of the report, E2row(kappa) is contained in E_2(kappa).
Implementation: discrete-log table, then S_b = {x - y : x in Q_0^o, y in Q_b^o} as a bitset,
directly from the definition (no cyclotomic-number shortcut), so it is independent of the proof's
reformulation.  Usage: python tworow.py K PMAX   -> prints members and the count of primes tested."""
import sys
from sympy import primerange, primitive_root
def classes(p, k):
    g = primitive_root(p); ind = [None]*p; x = 1
    for e in range(p-1):
        ind[x] = e % k; x = x*g % p
    return ind
def tworow_member(p, k):
    ind = classes(p, k)
    Q = [[x for x in range(1, p) if ind[x] == m] + [0] for m in range(k)]
    full = (1 << p) - 1
    def mask(S):
        M = 0
        for s in S: M |= 1 << s
        return M
    M0 = mask(Q[0])
    for b in range(1, k):
        # S_b = union over y in Q_b^o of (Q_0^o - y)
        S = 0
        for y in Q[b]:
            S |= ((M0 >> y) | (M0 << (p - y))) & full    # {x - y mod p}
        if S | 1 != full:
            missing = next(z for z in range(1, p) if not (S >> z) & 1)
            return b, missing
    return None
k = int(sys.argv[1]); pmax = int(sys.argv[2])
mem = []; n = 0
for p in primerange(3, pmax+1):
    if p % k != 1: continue
    n += 1
    r = tworow_member(p, k)
    if r: mem.append(p); print(f"TWOROW k={k} p={p} b={r[0]} missing={r[1]}", flush=True)
print(f"DONE k={k} pmax={pmax} primes={n} tworow_members={len(mem)} max={max(mem) if mem else None}")
