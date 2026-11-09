"""EC banks (padded to F(r)) under a uniformly random scan order: does the forward pass still
produce exact rounds and source-concentrated control?  Reports only the "reach V" leaf (thm2);
banks that stall are counted and skipped (ALG-T would recurse).

Usage: ec_shuffle.py kappa J p L1,L2,.. reps passes seed [ec|copies]
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import subquad_u as SQ  # noqa
from families_u import ec_bank, ec_copies_bank  # noqa
from lookahead import Ctl  # noqa

k, J, p = map(int, sys.argv[1:4])
FAM = sys.argv[8] if len(sys.argv) > 8 else "ec"
Ls = [int(x) for x in sys.argv[4].split(",")]
reps, passes, seed = map(int, sys.argv[5:8])
rng = random.Random(seed)
Fd = SQ.Field(p, k)
Par = SQ.Params(J, k)
for L in Ls:
    r = (J - 1) * L
    for rep in range(reps):
        cols = (ec_bank if FAM == "ec" else ec_copies_bank)(rng, Fd, J, L, Par.F(r))
        order = list(range(len(cols)))
        rng.shuffle(order)
        st = SQ.init_state(Fd, cols, order)
        status = SQ.forward_fast(Fd, cols, J, rng, st, rule="first")
        if status != "ok":
            print("L=%d rep=%d status=%s (not a thm2 leaf)" % (L, rep, status), flush=True)
            continue
        rounds = st["rounds"]
        n_exact = sum(1 for R in rounds if not any(R.e))
        ctl = Ctl(Fd, cols, rounds, st["Ub"], st["B"])
        sm = ctl.summary()
        res = {}
        for mode in ("plain", "look"):
            res[mode] = sum(ctl.backward(rng, mode)[0] is not None for _ in range(passes)) / passes
        print("L=%2d r=%2d rep=%d rounds=%2d exact(e=0)=%2d rho=%3d N_lev=%2d N_src=%3d src_ctrl=%3d "
              "maxgap=%d | plain %.3f look %.3f"
              % (L, r, rep, len(rounds), n_exact, sm["rho"], sm["N_lev"], sm["N_src"], sm["src_ctrl"],
                 sm["maxgap"], res["plain"], res["look"]), flush=True)
