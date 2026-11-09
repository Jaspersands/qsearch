"""Exact Good-set structure at small p.

Good(beta, c) = {s in F_p : beta_b + s in Q_{-c_b} u {0} for all b}, beta_0 = 0, offsets pairwise
distinct (e = E distinct offsets), classes c in Z_kappa^E arbitrary.
G*_E(p) = min |Good| over all such data (as in Q1 section 1).  Also: the fraction of (beta, c)
with Good empty, the fraction for c with >= 2 classes, and the pigeonhole identity
sum_c |Good(beta,c)| = p + E(kappa-1) (checked on every beta).

Usage: good_small.py kappa Emax p1,p2,...
"""
import itertools
import sys

import numpy as np

k, Emax = int(sys.argv[1]), int(sys.argv[2])
primes = [int(x) for x in sys.argv[3].split(",")]
LIMIT = float(sys.argv[4]) if len(sys.argv) > 4 else 3e8


def cls_table(p, k):
    g = next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1
                                           for q in range(2, p) if (p - 1) % q == 0 and
                                           all(q % d for d in range(2, q))))
    t = -np.ones(p, dtype=np.int64)
    y = 1
    for e in range(p - 1):
        t[y] = e % k
        y = y * g % p
    return t


for p in primes:
    if (p - 1) % k:
        continue
    ct = cls_table(p, k)
    s = np.arange(p)
    for E in range(2, Emax + 1):
        if k ** E * p ** (E - 1) > LIMIT:
            print("p=%d E=%d skipped (size)" % (p, E))
            continue
        alloffs = np.array([o for o in itertools.product(range(1, p), repeat=E - 1)
                            if len(set(o)) == E - 1], dtype=np.int64)    # beta_1..beta_{E-1}
        Gmin, Gmin2, empty, empty2, tot, tot2 = 10 ** 9, 10 ** 9, 0, 0, 0, 0
        CH = max(1, 4 * 10 ** 7 // (E * p))                              # memory-safe chunks
        for c0 in range(0, len(alloffs), CH):
          offs = alloffs[c0:c0 + CH]
          betas = np.concatenate([np.zeros((len(offs), 1), dtype=np.int64), offs], axis=1)
          pat = ct[(betas[:, :, None] + s[None, None, :]) % p].astype(np.int8)  # N x E x p
          sumc = np.zeros(len(offs), dtype=np.int64)
          for c in itertools.product(range(k), repeat=E):
            need = ((-np.array(c)) % k).astype(np.int8)
            okm = (pat == need[None, :, None]) | (pat < 0)
            G = okm.all(axis=1).sum(axis=1)                            # N
            sumc += G
            gm = int(G.min())
            Gmin = min(Gmin, gm)
            empty += int((G == 0).sum())
            tot += len(G)
            if len(set(c)) > 1:
                Gmin2 = min(Gmin2, gm)
                empty2 += int((G == 0).sum())
                tot2 += len(G)
          assert (sumc == p + E * (k - 1)).all(), "pigeonhole identity"
        print("kappa=%d p=%3d E=%d  G*_E=%d  (>=2 classes: %d)  empty fraction %.4f (>=2 classes %.4f)"
              "  mean |Good| = %.3f = (p+E(k-1))/k^E"
              % (k, p, E, Gmin, Gmin2 if tot2 else -1, empty / tot, empty2 / max(tot2, 1),
                 (p + E * (k - 1)) / k ** E), flush=True)
