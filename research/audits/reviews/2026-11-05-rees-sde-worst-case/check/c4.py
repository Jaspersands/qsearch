import os, sys, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "2026-11-05-rees-sde-two-relation"))
import common as C, brt_tests
sys.path.insert(0, os.path.join(HERE, ".."))
from sss import rank, budget, Field, forward_swap, solve_in_span
rng = random.Random(1)
for (p, k) in [(1009, 2), (1009, 3)]:
    Fo = C.F(p, k); Fd = Field(p, k)
    for a in (4, 6):
        for t in range(3):
            cols = brt_tests.planted_top(Fo, a, 3, rng)
            if cols is None: continue
            n0 = len(cols)
            r = rank(cols, p)[0]
            dep = sum(1 for S in itertools.combinations(range(n0), r) if rank([cols[i] for i in S], p)[0] < r)
            print(p, k, a, "planted M=%d rank=%d dependent r-subsets among planted part: %d" % (n0, r, dep))
