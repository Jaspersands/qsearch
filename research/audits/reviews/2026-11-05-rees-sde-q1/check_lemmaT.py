"""Exact check of Lemma T (codimension 1) on every codimension-1 snapshot of forward
passes: with beta = first free column outside U, the number of pairs {a,b} in X-{beta}
whose top round leaves a vanishing steering functional is at most the number of lower
cross-class pairs (at most one bad pair per lower pair).  Also runs the backward pass on a
good pair.  Usage: check_lemmaT.py seed trials"""
import sys
import random
from itertools import combinations
from collections import Counter
from q1core import (Field, D, forward, init_state, free_cols, in_span, rebuild, mk_round,
                    steer_bad, solve_in_span, run_backward, check)
from fams import family_list

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 2
rng = random.Random(seed)
E = 3
PK = [tuple(map(int, s.split(","))) for s in (sys.argv[3].split(";") if len(sys.argv) > 3 else ["1009,2", "10007,2", "1009,3", "10009,3"])]
tally = Counter()
worst = 0.0


def snap_check(Fd, cols, r):
    def snap(st):
        global worst
        p = Fd.p
        rounds, Ub = st["rounds"], st["Ub"]
        if r - len(Ub) != 1:
            return None
        Fr = free_cols(len(cols), rounds)
        X = [i for i in Fr if not in_span(Ub, cols[i], p)]
        if len(X) < 3:
            tally["small X"] += 1
            return None
        rho = sum(1 for R in rounds for b in range(len(R.blocks))
                  for b2 in range(b + 1, len(R.blocks)) if R.bclass[b] != R.bclass[b2])
        nbad, good = 0, None
        for a1, a2 in combinations(X[1:], 2):
            co = solve_in_span(Ub + [cols[a2]], cols[a1], p)
            delta = {a1: 1, a2: (-co[-1]) % p}
            rr = rounds + [mk_round(Fd, cols, [a1, a2], delta, [[a1], [a2]])]
            Ub2 = rebuild(Fd, rr)
            src = [i for i in Fr if i not in (a1, a2)]
            if steer_bad(Fd, cols, rr, Ub2, src):
                nbad += 1
            elif good is None:
                good = (rr, Ub2, src)
        assert nbad <= rho, ("Lemma T violated", nbad, rho)
        tally["snapshots"] += 1
        tally["bad pairs"] += nbad
        if rho:
            worst = max(worst, nbad / rho)
        if good is not None:
            x = run_backward(Fd, cols, *good, rng, 12)
            tally["solved" if x is not None and check(Fd, cols, x) else "unsolved"] += 1
        return None
    return snap


for (p, k) in PK:
    Fd = Field(p, k)
    nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
    for a in (4, 5, 6, 7):
        M = D(a, E) + a
        for name, gen in family_list(rng, p, a, M, nr).items():
            for _ in range(trials):
                cols = gen()
                if any(not any(c) for c in cols):
                    continue
                st = init_state(Fd, cols)
                forward(Fd, cols, E, rng, st, snap=snap_check(Fd, cols, len(st["B"])))
print(dict(tally), "max bad/rho", worst)
