"""Independent re-implementation (Python/numpy, no class tables) of the w2 search.

Cone C(B) = {sum x_i lambda_i : x in P0^n} is stored as a p x p boolean array of
vectors (not classes).  B + lambda is dead iff (-P lambda) misses C(B) (all |P|
vectors are tested, P-stability is not assumed).  C(B + lambda) = U_{s in P0} (C(B) + s lambda)
via np.roll.  The search tree is dead_w2.py's: base e1, e2; candidates = dead_w2's
classes2 list; multisets in index order.  Prints m1 (by brute force over P0^n),
m2 and #max_ext, to be compared with deadcone.c (w2 mode) and dead_w2_rerun.out.
Run: nice -n 19 /opt/anaconda3/bin/python -I indep_cone.py p kappa
"""
import itertools
import sys
import time

import numpy as np

OLD = "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-11-rees-sde-near-linear-total"
sys.path.insert(0, OLD)
from sdecore import primroot  # noqa: E402  (only the primitive root)
from dead_w2 import classes2  # noqa: E402  (reference class list and order)


def main():
    p, kap = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.time()
    g = primroot(p)
    P = sorted({pow(x, kap, p) for x in range(1, p)})
    P0 = [0] + P
    # m1 by brute force: multisets of 1-dim classes g^e, dead iff no nonzero x in P0^n with sum x_i c_i = 0
    reps1 = [pow(g, e, p) for e in range(kap)]

    def dead1(ms):
        for x in itertools.product(P0, repeat=len(ms)):
            if any(x) and sum(a * c for a, c in zip(x, ms)) % p == 0:
                return False
        return True
    m1 = 0
    for n in range(1, kap + 2):
        if any(dead1([reps1[i] for i in ms]) for ms in itertools.combinations_with_replacement(range(kap), n)):
            m1 = n
        else:
            break
    cl = classes2(p, g, kap)
    negidx = np.array([[((-s * u) % p) * p + ((-s * v) % p) for s in P] for (u, v) in cl])
    shifts = [[((s * u) % p, (s * v) % p) for s in P] for (u, v) in cl]

    def add(C, j):
        out = C.copy()
        for (a, b) in shifts[j]:
            out |= np.roll(C, (a, b), axis=(0, 1))
        return out
    C = np.zeros((p, p), dtype=bool)
    C[0, 0] = True
    base = [cl.index([1, 0]), cl.index([0, 1])]
    for j in base:
        assert not C.flat[negidx[j]].any()
        C = add(C, j)
    cand = [j for j in range(len(cl)) if not C.flat[negidx[j]].any()]
    candarr = np.array(cand)
    best, nbest, nodes = 2, 0, 0
    sys.setrecursionlimit(100)

    def rec(C, start, size):
        nonlocal best, nbest, nodes
        nodes += 1
        if size > best:
            best, nbest = size, 1
        elif size == best:
            nbest += 1
        ok = ~C.flat[negidx[candarr[start:]]].any(axis=1)
        for off in np.nonzero(ok)[0]:
            jj = start + int(off)
            rec(add(C, cand[jj]), jj, size + 1)
    rec(C, 0, 2)
    print(f"indep kappa={kap} p={p} m1={m1} m2={best} nmax_ext={nbest} ncand3={len(cand)} nodes={nodes} "
          f"sec={time.time() - t0:.1f}", flush=True)


if __name__ == "__main__":
    main()
