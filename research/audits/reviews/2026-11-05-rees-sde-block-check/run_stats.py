"""Empirical failure rates against the bounds of Theorem C / Corollary C at small p (below the
stated prime bounds), with mybrt.  Bank side: (H1) or (ND') fails; bound (M_E(a)+L*C(E,2))/(p-1).
Pass side: fraction of single backward passes that fail on banks meeting (H1) and (ND'); bound
L*C(E,2)/G_E(p) (G from the exact scan)."""
import math
import random
import sys

import mybrt as mb

G_EXACT = {(2, 257): 29, (3, 271): None, (2, 1031): None}


def run(k, p, a, E, reps, seed, G):
    rng = random.Random(seed)
    Fd = mb.Field(p, k)
    M = mb.arity(a, E)
    bank_bad = passes = pass_fail = solved = budget = wrong = 0
    cap = 50 * p  # exhaustive-equivalent cap: s is uniform, so cap >> p/|Good| or Good empty
    for _ in range(reps):
        cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
        rounds, U, top, used, status, h1 = mb.forward(Fd, cols, a, E, rng)
        if status == "budget":
            budget += 1
            bank_bad += 1
            continue
        nd = mb.nd_fails(Fd, rounds, U, top)
        good_bank = h1 and not nd
        if not good_bank:
            bank_bad += 1
        ok_any = False
        for _t in range(10):
            x, _ = mb.backward(Fd, cols, a, rounds, U, top, rng, cap)
            if good_bank:
                passes += 1
                pass_fail += x is None
            if x is not None:
                if not mb.verify(Fd, cols, x):
                    wrong += 1
                ok_any = True
        solved += ok_any
    L = math.ceil(a / (E - 1))
    bb = (M + L * math.comb(E, 2)) / (p - 1)
    pb = (L * math.comb(E, 2) / G) if G else None
    print(f"kappa={k} p={p} a={a} E={E} M={M}: banks={reps} bad-bank={bank_bad} ({bank_bad / reps:.3f}; bound {bb:.3f}) "
          f"budget={budget} pass-fail on good banks={pass_fail}/{passes} "
          f"({pass_fail / max(passes, 1):.3f}; bound {pb if pb is None else round(pb, 3)}) solved={solved} wrong={wrong}",
          flush=True)


if __name__ == "__main__":
    reps = int(sys.argv[1])
    run(2, 257, 6, 3, reps, 1, 29)
    run(2, 1031, 8, 3, reps, 2, None)
    run(3, 307, 4, 3, reps, 3, 2)
    run(3, 2713, 6, 3, reps, 4, 74)
    run(3, 241, 4, 3, reps, 5, None)      # 241 in E_cg(3,3): Good can be empty
    run(2, 101, 6, 4, reps, 6, None)      # 101 > 59, but below p_W(4,2)=2033; E_cg(4,2) max is 59
