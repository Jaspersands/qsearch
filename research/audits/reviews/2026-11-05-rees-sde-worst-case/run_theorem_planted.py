"""Theorem-2 algorithm (sss_theorem: no recursion, no fallback) on (i) the planted family of
the two-relation report padded to D_E(a)+a, (ii) the lines family; prints one stalled bank."""
import os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-05-rees-sde-two-relation"))
import common as C
import brt_tests
sys.path.insert(0, HERE)
from sss import Field, sss_theorem, sss_full, budget
from run_adversarial import fam_lines

rng = random.Random(99)
res = {}
for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (10009, 3)]:
    Fo, Fd = C.F(p, k), Field(p, k)
    for a in (4, 6, 8):
        for t in range(4):
            cols = brt_tests.planted_top(Fo, a, 3, rng)
            if cols is None:
                continue
            while len(cols) < budget(a, 3):
                cols.append([rng.randrange(p) for _ in range(a)])
            x, st, npool = sss_theorem(Fd, cols, 3, rng, passes=20, rule="first")
            res[st] = res.get(st, 0) + 1
print("planted (padded), Theorem-2 algorithm:", res)
res, shown = {}, False
for (p, k) in [(1009, 2), (10007, 2)]:
    Fd = Field(p, k)
    for a in (3, 5, 7):
        for t in range(20):
            cols = fam_lines(rng, p, a, budget(a, 3), a + 1)
            x, st, npool = sss_theorem(Fd, cols, 3, rng, passes=20)
            res[(st, npool > 0)] = res.get((st, npool > 0), 0) + 1
            if st == "stall" and not shown and a == 3:
                shown = True
                y, st2 = sss_full(Fd, cols, 3, rng)
                print("stalled bank p=%d kappa=%d a=%d: %s ; full algorithm: %s, x=%s" % (p, k, a, cols, st2, y))
print("lines family, Theorem-2 algorithm (status, had true pool):", res)
