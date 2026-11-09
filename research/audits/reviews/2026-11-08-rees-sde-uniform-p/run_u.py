"""ALG-T (copy subquad_u.py, strict mode) on uniform, break-folder adversarial (families.make) and
EC banks, at primes below Theorem A's range.  Every leaf: control fan-in (N_lev, N_src), rho,
and single-pass success rates of plain (Lemma 2) and lookahead back substitution over
EVAL passes; the end-to-end run uses lookahead with 30 passes.

Usage: run_u.py kappa J primes(comma) ranks(comma) reps eval seed [fams(comma)]
"""
import json
import os
import random
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import subquad_u as SQ  # noqa
sys.path.insert(1, os.path.join(HERE, "..", "2026-11-07-rees-sde-subquad-A-break"))
import families  # noqa  (break folder generators)
from families_u import ec_bank, uniform_bank  # noqa

k, J = int(sys.argv[1]), int(sys.argv[2])
primes = [int(x) for x in sys.argv[3].split(",")]
ranks = [int(x) for x in sys.argv[4].split(",")]
reps, EV, seed = int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
fams = sys.argv[8].split(",") if len(sys.argv) > 8 else ["uniform", "EC", "planted", "twist",
                                                          "adapt_rado", "adapt_mix", "design_mix"]
rng = random.Random(seed)
SQ.EVAL_PASSES[0] = EV
SQ.LEAF_MODE[0] = "look"
Par = SQ.Params(J, k)

for p in primes:
    Fd = SQ.Field(p, k)
    agg = defaultdict(lambda: Counter())
    for r in ranks:
        for fam in fams:
            for rep in range(reps):
                s = rng.randrange(10 ** 9)
                rr = random.Random(s)
                try:
                    if fam == "EC":
                        if r % (J - 1):
                            continue
                        cols = ec_bank(rr, Fd, J, r // (J - 1), Par.F(r))
                    elif fam == "uniform":
                        cols = uniform_bank(rr, Fd, r, Par.F(r))
                    else:
                        cols = families.make(fam, rr, p, k, J, r)
                except Exception as ex:          # generator refused these parameters
                    print("GENFAIL", fam, p, r, repr(ex)[:80], flush=True)
                    continue
                SQ.LEAVES.clear()
                st = SQ.new_stats()
                x = SQ.solve_T(Fd, [list(map(int, c)) for c in cols], Par, random.Random(s + 1), st)
                A = agg[(fam, r)]
                A["banks"] += 1
                A["solved"] += x is not None
                A["direct"] += st["direct"] + st["zero"]
                for lf in SQ.LEAVES:
                    A["leaves"] += 1
                    A["sum_plain"] += lf["plain"]
                    A["sum_look"] += lf["look"]
                    A["max_rho"] = max(A["max_rho"], lf["rho"])
                    A["max_Nlev"] = max(A["max_Nlev"], lf["N_lev"])
                    A["max_Nsrc"] = max(A["max_Nsrc"], lf["N_src"])
                    A["max_gap"] = max(A["max_gap"], lf["maxgap"])
                    A["emptyGood_look"] += lf["ev_look"].get("emptyGood", 0)
                    A["fanin_exh_look"] += lf["ev_look"].get("fanin_exhausted", 0) + \
                        lf["ev_look"].get("src_fanin_exhausted", 0)
                    A["maxblocks"] = max(A["maxblocks"], st["maxblocks"])
                if x is None:
                    print("UNSOLVED(30 look passes)", fam, p, r, s, json.dumps(SQ.LEAVES)[:300], flush=True)
            A = agg[(fam, r)]
            if A["banks"]:
                nl = max(A["leaves"], 1)
                print("k=%d J=%d p=%-9d r=%2d %-10s banks=%2d solved=%2d direct=%2d leaves=%2d "
                      "plain=%.3f look=%.3f rho<=%3d Nlev<=%2d Nsrc<=%3d gap<=%2d blocks<=%d "
                      "lookEmptyGood=%d lookFaninExh=%d"
                      % (k, J, p, r, fam, A["banks"], A["solved"], A["direct"], A["leaves"],
                         A["sum_plain"] / nl, A["sum_look"] / nl, A["max_rho"], A["max_Nlev"],
                         A["max_Nsrc"], A["max_gap"], A["maxblocks"], A["emptyGood_look"],
                         A["fanin_exh_look"]), flush=True)
