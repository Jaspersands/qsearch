"""Run alg_thm.solve_thm on structured families at the budget f(a) = D_3(a)+3a, and a hill
climb maximising the absorption load.  Usage: run_thm.py seed trials climb"""
import sys
import random
from collections import Counter
from q1core import Field, check
from alg_thm import solve_thm, f
from fams import family_list

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 3
climb = int(sys.argv[3]) if len(sys.argv) > 3 else 0
rng = random.Random(seed)
cases, fails, n, maxload = Counter(), 0, 0, 0
stalls = Counter()
toppair = []


def run(Fd, cols):
    tr = []
    x = solve_thm(Fd, cols, rng, trace=tr)
    if x is not None:
        assert check(Fd, cols, x)
    load = max([d["load"] for _, c, d in tr if c == "absorb"] + [0])
    return x, tr, load


for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (10009, 3)]:
    Fd = Field(p, k)
    nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
    for a in ((3, 4, 5, 6, 7) if k == 2 else (3, 4, 5, 6)):
        M = f(a)
        for name, gen in family_list(rng, p, a, M, nr).items():
            for _ in range(trials):
                cols = gen()
                n += 1
                x, tr, load = run(Fd, cols)
                maxload = max(maxload, load)
                fails += x is None
                for d, c, info in tr:
                    cases[c] += 1
                    if c == "stall":
                        stalls[(info["q"], info["qplus"])] += 1
                    if c == "top-pair":
                        toppair.append(info)
                if x is None:
                    print("FAIL", p, k, a, name, tr, flush=True)
                # hill climb on the absorption load / stall codimension
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
                    n += 1
                    fails += x2 is None
                    for d, c, info in tr2:
                        cases[c] += 1
                        if c == "stall":
                            stalls[(info["q"], info["qplus"])] += 1
                    s2 = (l2, max([i["q"] for _, c, i in tr2 if c == "stall"] + [0]))
                    maxload = max(maxload, l2)
                    if s2 >= bs:
                        best, bs = c2, s2
        print(p, k, "done", dict(cases), "maxload", maxload, flush=True)
print("banks", n, "failures", fails, "max absorption load", maxload)
print("cases", dict(cases))
print("stalls (q,q+)", dict(sorted(stalls.items())))
if toppair:
    print("top-pair: n range", min(t["n"] for t in toppair), max(t["n"] for t in toppair),
          "max bad", max(t["bad"] for t in toppair), "max bad/rho",
          max(t["bad"] / max(1, t["rho"]) for t in toppair), "count", len(toppair))
