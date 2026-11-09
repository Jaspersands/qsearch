"""Planted non-steerable instances (generator from the report's brt_tests.py) against mybrt.
At kappa = 3, a = 8, E = 3 the budget M_3(8) = 25 = 3a + 1, so Chevalley-Warning makes every
instance solvable; at kappa = 2, a = 6, M_3(6) = 16 >= 2a + 1 = 13."""
import random
import sys

sys.path.insert(0, "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-05-rees-sde-two-relation")
import brt_tests  # noqa: E402  (report code: used only to generate the adversarial columns)
from common import F  # noqa: E402

import mybrt as mb  # noqa: E402

rng = random.Random(4242)
for (p, k, a, E) in [(1009, 3, 8, 3), (2767, 3, 8, 3), (1009, 3, 10, 3), (1009, 2, 6, 3), (1009, 3, 6, 3)]:
    Fd_r = F(p, k)
    Fd = mb.Field(p, k)
    res = dict(inst=0, nd_fail=0, solved=0, solved_first=0, three_classes=0)
    for _ in range(8):
        cols = brt_tests.planted_top(Fd_r, a, E, rng)
        if cols is None:
            continue
        res["inst"] += 1
        # my solver, deterministic and random splits
        rounds, U, top, used, status, h1 = mb.forward(Fd, cols, a, E, random.Random(1), mode="first")
        lv = [R for R in rounds if R["kind"] == "level"]
        if lv and len(set(lv[0]["bcls"])) == 3:
            res["three_classes"] += 1
        if status != "budget" and mb.nd_fails(Fd, rounds, U, top):
            res["nd_fail"] += 1
        x, info = mb.solve(Fd, cols, E, random.Random(2), passes=40, mode="first", reduce=False)
        res["solved_first"] += x is not None
        x2, info2 = mb.solve(Fd, cols, E, random.Random(3), passes=40, mode="random", reduce=False)
        res["solved"] += x2 is not None
        for xx in (x, x2):
            if xx is not None:
                assert mb.verify(Fd, cols, xx)
    print(f"p={p} kappa={k} a={a} E={E} M={mb.arity(a, E)} (kappa*a+1={k * a + 1}): {res}", flush=True)
