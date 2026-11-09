"""kappa = 7: primes of E_2(7) at which no two-step union chain Z_7 -> K -> {0} with |K| in {2,3}
(or K = {0,1,2,3} and its unit multiples, i.e. |K| = 4) works.  All K containing 0 of these sizes
are tried, so the answer does not depend on the coset generator.  Steps decided by rcdfs.c."""
import itertools
from rc import feasible
from e2lists import E2
Ks = {s: [[0] + list(c) for c in itertools.combinations(range(1, 7), s - 1)] for s in (2, 3, 4)}
for sizes in [(2, 3), (2, 3, 4)]:
    bad = []
    for p in E2[7]:
        ok = False
        for s in sizes:
            for K in Ks[s]:
                if feasible(p, 7, K, [0])[0] == 1 and feasible(p, 7, list(range(7)), K)[0] == 1: ok = True; break
            if ok: break
        if not ok: bad.append(p)
    print("|K| in %s: no two-step union chain at %s" % (sizes, bad), flush=True)
