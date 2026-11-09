"""Theorem 2 check: plain SSS (no recursion, no fallback) on banks in general position,
at the budget D_3(a) + a, including kappa = 3 cases below the Chevalley-Warning bound."""
import itertools
import random
import sys
from sss import Field, sss_theorem, rank, budget


def is_gp(cols, p):
    r = rank(cols, p)[0]
    for S in itertools.combinations(range(len(cols)), r):
        if rank([cols[i] for i in S], p)[0] < r:
            return False
    return True


def run(p, k, a, trials, rng, check_gp=True):
    Fd = Field(p, k)
    M = budget(a, 3)
    out = {}
    pools = 0
    for t in range(trials):
        while True:
            cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
            if not check_gp or is_gp(cols, p):
                break
        x, st, npool = sss_theorem(Fd, cols, 3, rng, passes=10)
        pools += npool
        out[st] = out.get(st, 0) + 1
    print("p=%d kappa=%d a=%d M=%d (CW %d) trials=%d" % (p, k, a, M, k * a + 1, trials), out,
          "true-pool events:", pools, flush=True)


rng = random.Random(5)
# GP is checked exhaustively where a random bank is GP with reasonable probability;
# elsewhere the bank is random (not necessarily GP) and the true-pool count is reported.
for (p, k, As) in [(257, 2, (2, 3, 4)), (10007, 2, (5,)), (1000003, 2, (6,)), (2791, 3, (2, 3, 4)), (307, 3, (2, 3)),
                   (10009, 3, (5,))]:
    for a in As:
        run(p, k, a, 60 if a <= 4 else 15, rng, check_gp=True)
