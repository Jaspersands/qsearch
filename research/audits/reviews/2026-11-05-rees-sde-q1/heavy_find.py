"""Hill climb (as in run_thm.py) with the current alg_thm, saving every bank on which a heavy
stall (balanced absorption load >= 3) occurs, with its stall data, to heavy_found_<seed>.jsonl.
Usage: heavy_find.py seed climb"""
import sys
import json
import random
from collections import Counter
from q1core import Field, check
from alg_thm import solve_thm, f
from fams import family_list

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
climb = int(sys.argv[2]) if len(sys.argv) > 2 else 60
rng = random.Random(seed)
outf = open("heavy_found_%d.jsonl" % seed, "w")
cases, n, fails = Counter(), 0, 0
heavy_end = Counter()


def run(Fd, cols):
    tr = []
    x = solve_thm(Fd, cols, rng, trace=tr)
    if x is not None:
        assert check(Fd, cols, x)
    load = max([d["load"] for _, c, d in tr if c in ("absorb", "heavy")] + [0])
    return x, tr, load


def record(p, k, a, cols, x, tr):
    global n, fails
    n += 1
    fails += x is None
    for d, c, info in tr:
        cases[c] += 1
    for t, (d, c, info) in enumerate(tr):
        if c == "heavy":
            nxt = tr[t + 1][1] if t + 1 < len(tr) else None
            heavy_end[nxt] += 1
            outf.write(json.dumps(dict(p=p, k=k, a=a, info=info, next=nxt, solved=x is not None,
                                       cols=cols)) + "\n")
            outf.flush()
    if x is None:
        print("FAIL", p, k, a, tr, cols, flush=True)


for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (10009, 3)]:
    Fd = Field(p, k)
    nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
    for a in ((3, 4, 5, 6, 7) if k == 2 else (3, 4, 5, 6)):
        M = f(a)
        for name, gen in family_list(rng, p, a, M, nr).items():
            cols = gen()
            x, tr, load = run(Fd, cols)
            record(p, k, a, cols, x, tr)
            best, bs = cols, (load, max([i["q"] for _, c, i in tr if c == "stall"] + [0]))
            for _ in range(climb):
                c2 = [list(v) for v in best]
                i = rng.randrange(M)
                u = rng.random()
                if u < 0.4:
                    j = rng.randrange(M)
                    t = rng.randrange(1, p)
                    c2[i] = [t * z % p for z in best[j]]
                elif u < 0.7:
                    j, j2 = rng.randrange(M), rng.randrange(M)
                    t, t2 = rng.randrange(1, p), rng.randrange(1, p)
                    c2[i] = [(t * z + t2 * w) % p for z, w in zip(best[j], best[j2])]
                else:
                    c2[i] = [rng.randrange(p) for _ in range(a)]
                rng.shuffle(c2)
                x2, tr2, l2 = run(Fd, c2)
                record(p, k, a, c2, x2, tr2)
                s2 = (l2, max([i["q"] for _, c, i in tr2 if c == "stall"] + [0]))
                if s2 >= bs:
                    best, bs = c2, s2
        print(p, k, "done", n, dict(cases), "heavy ->", dict(heavy_end), flush=True)
print("banks", n, "failures", fails)
print("cases", dict(cases))
print("heavy stalls, next step", dict(heavy_end))
