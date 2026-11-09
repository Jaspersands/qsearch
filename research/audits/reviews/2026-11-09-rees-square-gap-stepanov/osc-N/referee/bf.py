"""Independent brute force (referee C).
(1) first (C1) prime in the infinity chart: S' = kappa-1 finite points (affine-normalised 0,1,...),
    T = kappa points of F_p minus S' with identical raw profile (ind(s_j - t))_j  (no diag quotient).
(2) exact Lambda_M (finite chart, profile mod diag, t in F_p minus S) by enumerating ALL ordered S
    for small p (no affine normalisation) to cross-check the normalised enumeration of bucket_cert.py.
"""
import sys, itertools
from collections import Counter
from math import prod

def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n**.5) + 1))

def indtab(p, k):
    # discrete log mod k via brute-force generator search
    for g in range(2, p):
        x, seen = 1, set()
        for e in range(p - 1):
            seen.add(x); x = x * g % p
        if len(seen) == p - 1: break
    ind = [None] * p; x = 1
    for e in range(p - 1):
        ind[x] = e % k; x = x * g % p
    return ind

def ff(x, n):
    return prod(x - i for i in range(n))

def maxbucket_inf(p, k):
    ind = indtab(p, k); best = 0
    rest = [x for x in range(2, p)]
    for tail in itertools.combinations(rest, k - 3) if k >= 3 else [()]:
        S = (0, 1) + tail
        c = Counter(tuple(ind[(s - t) % p] for s in S) for t in range(p) if t not in S)
        best = max(best, max(c.values()))
        if best >= k: return best
    return best

def lam_exact_full(p, k):
    ind = indtab(p, k); tot = [0.0] * (k + 1); n = 0
    for S in itertools.permutations(range(p), k):
        c = Counter(tuple((ind[(s - t) % p] - ind[(S[0] - t) % p]) % k for s in S[1:]) for t in range(p) if t not in S)
        for M in range(1, k + 1):
            tot[M] += sum(ff(b, M) for b in c.values())
        n += 1
    return [x / n for x in tot]

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'first':
        k = int(sys.argv[2]); pmax = int(sys.argv[3])
        for p in range(k + 1, pmax + 1):
            if p % k == 1 and isprime(p):
                mb = maxbucket_inf(p, k)
                print(f'k={k} p={p} max-bucket(inf chart)>={mb} {"C1" if mb >= k else "none"}', flush=True)
    else:
        k = int(sys.argv[2])
        for p in map(int, sys.argv[3:]):
            L = lam_exact_full(p, k)
            print(f'k={k} p={p} Lambda_1..k (full ordered S) = ' + ' '.join(f'{x:.6g}' for x in L[1:]), flush=True)
