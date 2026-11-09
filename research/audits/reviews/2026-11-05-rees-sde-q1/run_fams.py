"""Compare: Theorem-2 algorithm alone vs ALG-Q1 mechanisms, on structured banks at the
budget D_E(a)+a.  Usage: run_fams.py seed [trials]"""
import sys
import random
from collections import Counter
from q1core import Field, D, rank, check
from q1solve import solve
import sss

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 6
rng = random.Random(seed)
E = 3
from fams import family_list

tot_thm, tot_q1, tot_q1norec, n = 0, 0, 0, 0
hows = Counter()
stalls = Counter()
for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (10009, 3)]:
    Fd = Field(p, k)
    nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
    for a in ((3, 4, 5, 6, 7) if k == 2 else (4, 5, 6)):
        M = D(a, E) + a
        for name, gen in family_list(rng, p, a, M, nr).items():
            row = Counter()
            for _ in range(trials):
                cols = gen()
                n += 1
                x0, st0, _pi = sss.sss_theorem(Fd, cols, E, rng, passes=12)
                tot_thm += x0 is not None
                log = []
                x1, how1 = solve(Fd, cols, E, rng, use_rec=False, log=log)
                tot_q1norec += x1 is not None
                for d, cl in log:
                    stalls[(cl["q"], cl["qplus"], "eps>0" if cl["eps"] else "eps0")] += 1
                if x1 is None:
                    log2 = []
                    x1, how1 = solve(Fd, cols, E, rng, use_rec=True, log=log2)
                if x1 is not None:
                    assert check(Fd, cols, x1)
                tot_q1 += x1 is not None
                key = how1.split("(")[0] if x1 is not None else how1
                row[key] += 1
                hows[key] += 1
            print(p, k, a, M, name, dict(row), flush=True)
print("banks", n, "thm2 solved", tot_thm, "Q1 no-rec solved", tot_q1norec, "Q1 solved", tot_q1)
print("mechanisms", dict(hows))
print("unresolved stalls before recursion (q,q+,eps):", dict(stalls))
