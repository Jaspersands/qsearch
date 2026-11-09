"""Exact Lambda_M via affine normalisation (s1=0,s2=1), own code; then the unique law on {0..k-1}
with per-bucket factorial moments Lambda_m / k^(k-1), m<k (binomial-moment inversion)."""
import sys, itertools, math
from collections import Counter
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from bf import indtab, ff
k = int(sys.argv[1])
for p in map(int, sys.argv[2:]):
    ind = indtab(p, k); tot = [0] * (k + 1); n = 0
    for tail in itertools.permutations(range(2, p), k - 2):
        S = (0, 1) + tail
        c = Counter(tuple((ind[(s - t) % p] - ind[(S[0] - t) % p]) % k for s in S[1:]) for t in range(p) if t not in S)
        for M in range(1, k + 1): tot[M] += sum(ff(b, M) for b in c.values())
        n += 1
    lam = [Fr(x, n) for x in tot]
    D = k ** (k - 1); phi = [Fr(1)] + [lam[m] / D for m in range(1, k)]
    P = [sum((-1) ** (m - j) * math.comb(m, j) * phi[m] / math.factorial(m) for m in range(j, k)) for j in range(k)]
    print(f'k={k} p={p} Lambda=' + ' '.join(f'{float(x):.6g}' for x in lam[1:]) + ' | law ' + ' '.join(f'{float(x):.4g}' for x in P)
          + (' REALIZABLE' if min(P) >= 0 else ' not realizable'), flush=True)
