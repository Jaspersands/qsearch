"""Hyperplane-dense banks: N_H = M - t generic columns of a hyperplane H, t outside.
Random orders only.  For each (a, t): banks x orders single sss_full iterations, counting
Theorem-2 stalls, critical stalls (unused = 0, |B \\ U_L| = q) and failures.
usage: hyper_scan.py kappa p seed banks orders a1,a2,.. [variant]
variant 'gen' = generic in H; 'chain' = chain4 bank (H = span(b_1..b_{r-1})) for reference."""
import random
import sys
from q1lib import Field, budget, theorem_forward, one_order, fam_codim1, D3
from critical import chain4

k, p, seed, NB, NO = (int(v) for v in sys.argv[1:6])
As = [int(x) for x in sys.argv[6].split(",")]
variant = sys.argv[7] if len(sys.argv) > 7 else "gen"
tlist = [int(x) for x in sys.argv[8].split(",")] if len(sys.argv) > 8 else None


def fam_paired(rng, p, a, M, t):
    """H generic with M - t columns; t outside columns c_j = mu_j w + h_j with every mu_j in
    P, so that (when -1 in P) any two outside columns get equal delta-classes in a circuit
    whose other members lie in H."""
    from q1lib import rvec, comb
    H = [rvec(rng, p, a) for _ in range(a - 1)]
    w = rvec(rng, p, a)
    cols = [comb(rng, p, H, a) for _ in range(M - t)]
    for j in range(t):
        mu = Fd.randP(rng)
        h = comb(rng, p, H, a)
        cols.append([(mu * x + y) % p for x, y in zip(w, h)])
    return cols
rng = random.Random(seed)
Fd = Field(p, k)
for a in As:
    M = budget(a, 3)
    ts = (tlist or range(2, a + 4)) if variant in ("gen", "paired") else [None]
    for t in ts:
        st = cr = fl = tot = 0
        for b in range(NB):
            cols = (fam_codim1(rng, p, a, M, t) if variant == "gen" else
                    fam_paired(rng, p, a, M, t) if variant == "paired" else chain4(Fd, rng, a, M))
            for o in range(NO):
                perm = list(range(M))
                rng.shuffle(perm)
                pc = [cols[i] for i in perm]
                tf = theorem_forward(Fd, pc, rng=rng)
                if tf["status"] == "stall":
                    st += 1
                    cr += tf["unused"] == 0 and tf["BoutU"] == tf["q"]
                x, s, c = one_order(Fd, cols, perm, rng, passes=8)
                fl += x is None
                tot += 1
        print("k=%d p=%d a=%d M=%d %s t=%s N_H=%s thrH=%d : stall %d crit %d fail %d / %d orders" % (
            k, p, a, M, variant, t, (M - t) if t else "-", D3(a - 1) + a - 1, st, cr, fl, tot), flush=True)
