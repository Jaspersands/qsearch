"""Check: zero cells (i,j) of a contraction satisfy (i-j)-(i'-j') = eps for every
ordered pair of distinct zero cells, where eps = ind(-1). Hence z<=2 if eps!=0 and
all zero cells on one diagonal i-j=const if eps=0."""
import sys
from collections import Counter
from stepanov_check import is_prime, prim_root, contractions
for k, pmax in [(2,80),(3,80),(4,120),(5,200)]:
    for p in range(k+1, pmax+1):
        if not is_prime(p) or (p-1) % k: continue
        g = prim_root(p); cons, cls = contractions(p, k, g)
        if not cons: continue
        eps = cls(p-1)
        zc = Counter()
        for a, b in cons:
            Z = [(i,j) for i in range(k) for j in range(k) if (a[j]+b[i]) % p == 0]
            for (i,j) in Z:
                for (i2,j2) in Z:
                    if (i,j)!=(i2,j2): assert ((i-j)-(i2-j2)) % k == eps, (p,k,Z)
            if eps: assert len(Z) <= 2
            zc[len(Z)] += 1
        print(f"kappa={k} p={p} h={(p-1)//k} eps={eps} z-dist={dict(sorted(zc.items()))} OK")
