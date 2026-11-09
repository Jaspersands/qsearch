"""SSS on the planted non-steerable family of the two-relation report (Section 6.2)
and on random columns.  Budget: D_E(a) + a columns (D_E = worst greedy forward cost)."""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-05-rees-sde-two-relation"))
import common as C  # noqa: E402
import brt_tests  # noqa: E402

sys.path.insert(0, HERE)
from sss import Field, sss, worst_forward_cost  # noqa: E402


def budget(a, E):
    return worst_forward_cost(a, E) + a


def main():
    rng = random.Random(20261105)
    print("== planted family of brt_tests.planted_top (M = M_E(a)), padded to budget D_E(a)+a ==")
    tot = ok = 0
    for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (10009, 3)]:
        Fd_old = C.F(p, k)
        Fd = Field(p, k)
        for E in (3, 4):
            if E < k:
                continue
            for a in (4, 6, 8):
                for trial in range(4):
                    cols = brt_tests.planted_top(Fd_old, a, E, rng)
                    if cols is None:
                        continue
                    n0 = len(cols)
                    # pad with fresh random columns up to the SSS budget
                    while len(cols) < budget(a, E):
                        cols.append([rng.randrange(p) for _ in range(a)])
                    x, st = sss(Fd, cols, E, rng, passes=20, rule="first")
                    tot += 1
                    ok += x is not None
                    print(p, k, E, a, "planted M=%d padded=%d" % (n0, len(cols)), st)
    print("planted total", tot, "solved", ok)
    print("== planted family, no padding (exactly M_E(a) columns; SSS reserves a basis) ==")
    tot = ok = 0
    for (p, k) in [(1009, 2), (1009, 3)]:
        Fd_old = C.F(p, k)
        Fd = Field(p, k)
        for E in (3,):
            for a in (6, 8, 10):
                for trial in range(4):
                    cols = brt_tests.planted_top(Fd_old, a, E, rng)
                    if cols is None:
                        continue
                    x, st = sss(Fd, cols, E, rng, passes=20, rule="first", forwards=5)
                    tot += 1
                    ok += x is not None
                    print(p, k, E, a, "M=%d" % len(cols), st)
    print("unpadded total", tot, "solved", ok)
    print("== random columns at budget ==")
    for (p, k) in [(1009, 2), (1009, 3), (10007, 2), (10009, 3)]:
        Fd = Field(p, k)
        for E in (3, 4):
            if E < k:
                continue
            res = {}
            for a in (3, 5, 8, 12):
                for trial in range(5):
                    cols = [[rng.randrange(p) for _ in range(a)] for _ in range(budget(a, E))]
                    x, st = sss(Fd, cols, E, rng, passes=20)
                    res[st] = res.get(st, 0) + 1
            print(p, k, E, res)


if __name__ == "__main__":
    main()
