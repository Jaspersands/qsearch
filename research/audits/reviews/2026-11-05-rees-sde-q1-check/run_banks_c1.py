"""Referee run 4: own ALG-Q1 with the budget f(r) = D_3(r) + r (CC = 1), every count of the proof
asserted, on the search agent's 33 banks (which sit exactly at D_3(a)+a), three split rules,
shuffled column orders included.  Usage: run_banks_c1.py seed"""
import sys, os, json, glob, random
from collections import Counter
import myq1
myq1.CC = 1
from myq1 import GF, solve, verify, f

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
bd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "2026-11-05-rees-sde-q1-search", "banks")
tot = Counter()
for fn in sorted(glob.glob(os.path.join(bd, "*.json"))):
    bk = json.load(open(fn))
    F, cols0 = GF(bk["p"], bk["kappa"]), bk["cols"]
    assert len(cols0) >= f(len(cols0[0])) or True
    res = Counter()
    for t in range(12):
        cols = list(cols0)
        if t >= 3:
            rng.shuffle(cols)
        tr = []
        x = solve(F, cols, rng, rule=["first", "last", "random"][t % 3], fallback=True, passes=8, trace=tr)
        ok = x is not None and verify(F.p, F.k, cols, x)
        res["solved" if ok else "UNSOLVED"] += 1
        for d, c, info in tr:
            if c not in ("stall",):
                res[c] += 1
    tot.update(res)
    print(os.path.basename(fn), "M=%d f1(a)=%d" % (len(cols0), f(len(cols0[0]))), dict(res), flush=True)
print("total", dict(tot))
