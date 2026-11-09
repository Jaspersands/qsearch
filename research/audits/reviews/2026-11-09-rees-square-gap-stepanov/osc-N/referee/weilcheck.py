import sys, itertools, math
from collections import Counter
sys.path.insert(0, '.')
from bf import indtab, isprime
from cert import Edev
# max over affine-normalised U=(0,1,u3..um) of max_d |n_d(U) - (p-m)/k^(m-1)| vs referee/their bound
for k, m, ps in [(3, 3, [31, 61, 103]), (4, 3, [41, 97, 197]), (5, 3, [41, 101, 211]), (3, 4, [31, 61]), (4, 4, [41, 61])]:
    for p in ps:
        ind = indtab(p, k); D = k ** (m - 1); nb = (p - m) / D; worst = 0
        for tail in itertools.permutations(range(2, p), m - 2):
            U = (0, 1) + tail
            c = Counter(tuple((ind[(s - u) % p] - ind[(s - U[0]) % p]) % k for u in U[1:]) for s in range(p) if s not in U)
            dev = max(max(abs(v - nb) for v in c.values()), nb if len(c) < D else 0)
            worst = max(worst, dev)
        print(f'k={k} m={m} p={p}: max dev={worst:.3f}  ref bound={Edev(k,p,m,"ref"):.3f}  their bound={float(Edev(k,p,m,"theirs")):.3f}', flush=True)
