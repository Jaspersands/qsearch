"""s2b: the set of primes to which Prop app-s2-cyclotomic(i) applies, kappa = 3..16
(Remark app-s2-local-scope), computed from scratch: A(u,v) = #{w in Q_u : w-1 in Q_v},
eps = ind(-1); (i) applies iff A(u,v)=0 for some u != 0, v != eps, u != v.
Primes above the bound of (iii) need no check (proved there); we still scan a margin."""
import math, sys
import numpy as np
from sympy import primerange, primitive_root

def ind_table(p, g, k):
    t = np.full(p, -1, dtype=np.int64)
    x = 1
    for e in range(p - 1):
        t[x] = e % k
        x = x * g % p
    return t

def applies(p, k):
    g = primitive_root(p)
    ind = ind_table(p, g, k)
    w = np.arange(2, p)
    u = ind[w]; v = ind[w - 1]
    A = np.bincount(u * k + v, minlength=k * k).reshape(k, k)
    eps = int(ind[p - 1])
    assert A.sum() == p - 2
    hits = [(a, b) for a in range(k) for b in range(k) if a != 0 and b != eps and a != b and A[a, b] == 0]
    return hits, A, eps

out = []
def say(s):
    print(s); out.append(s)

nocha = {4: [5, 13], 5: [11], 6: [7, 13, 19, 31, 43], 7: [29, 71], 8: [17, 41, 73], 9: [19, 37, 73]}
E2 = {4: {5, 13, 17, 29, 37, 53}, 5: {11, 31, 41, 61, 71, 101, 131, 151, 181}}
claimed_max = {4: 29, 5: 11, 6: 223, 7: 71, 8: 761, 9: 163}
for k in range(3, 17):
    N = (k - 1) * (k - 2)
    # (iii): A >= 1 for all u,v once p-2 > N sqrt p + 3(k-1); scan up to 1.2x that bound
    s = (N + math.sqrt(N * N + 4 * (3 * (k - 1) + 2))) / 2
    bound = int(1.2 * s * s) + 10
    S = []
    viol3 = []
    for p in primerange(3, bound):
        if p % k != 1: continue
        hits, A, eps = applies(p, k)
        if hits: S.append(p)
        # check (iii)'s numerical bound |k^2 A - (p-2)| <= 3(k-1) + N sqrt p for all u,v
        dev = np.abs(k * k * A - (p - 2)).max()
        if dev > 3 * (k - 1) + N * math.sqrt(p) + 1e-9: viol3.append(p)
    small = [p for p in primerange(3, k * k - 3 * k + 4) if p % k == 1]
    msg = "kappa=%2d: |set|=%3d max=%s  15k^2=%d  (iii)-violations=%s  (ii)-primes %s all in set: %s" % (
        k, len(S), max(S) if S else None, 15 * k * k, viol3 if viol3 else "none", small,
        all(p in S for p in small))
    if k in claimed_max: msg += "  claimed max %d: %s" % (claimed_max[k], (max(S) if S else None) == claimed_max[k])
    if k in nocha: msg += "  contains no-chain primes %s: %s" % (nocha[k], all(p in S for p in nocha[k]))
    if k in E2: msg += "  subset of E_2: %s" % set(S).issubset(E2[k])
    say(msg)
    if k <= 9: say("    set: %s" % S)
# kappa = 7, (iii) threshold "p >= 940"
f = lambda p: p - 2 - (30 * math.sqrt(p) + 18)
say("kappa=7: (iii) inequality at p=939: %.4f, at p=940: %.4f" % (f(939), f(940)))
open(__file__.replace('.py', '.out'), 'w').write("\n".join(out) + "\n")
