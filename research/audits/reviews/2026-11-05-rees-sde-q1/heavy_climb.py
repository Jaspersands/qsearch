"""Hill climb maximising the absorption load of alg_thm.solve_thm (Theorem Q1 algorithm) at
the budget f(a) = D_3(a)+3a.  Saves the best bank per setting to heavy_banks.json.
Usage: heavy_climb.py seed starts steps"""
import sys
import json
import random
from q1core import Field, check
from alg_thm import solve_thm, f
from fams import family_list

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
starts = int(sys.argv[2]) if len(sys.argv) > 2 else 4
steps = int(sys.argv[3]) if len(sys.argv) > 3 else 150
rng = random.Random(seed)
out = {}


def evaluate(Fd, cols):
    tr = []
    x = solve_thm(Fd, cols, rng, trace=tr)
    ok = x is not None and check(Fd, cols, x)
    load = max([d["load"] for _, c, d in tr if c == "absorb"] + [0])
    q = max([d["q"] for _, c, d in tr if c == "stall"] + [0])
    return ok, load, q, tr


for (p, k) in [(10007, 2), (10009, 3)]:
    Fd = Field(p, k)
    nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
    for a in (5, 6, 7, 8):
        M = f(a)
        fams = family_list(rng, p, a, M, nr)
        names = list(fams)
        best_all = None
        for s in range(starts):
            cols = fams[names[s % len(names)]]()
            ok, load, q, tr = evaluate(Fd, cols)
            best, bs = cols, (load, q)
            for _ in range(steps):
                c2 = [list(v) for v in best]
                for _m in range(rng.choice([1, 1, 2, 3])):
                    i = rng.randrange(M)
                    u = rng.random()
                    if u < 0.35:
                        j = rng.randrange(M)
                        t = rng.randrange(1, p)
                        c2[i] = [t * z % p for z in c2[j]]
                    elif u < 0.75:
                        js = rng.sample(range(M), rng.choice([2, 3]))
                        ts = [rng.randrange(1, p) for _ in js]
                        c2[i] = [sum(t * c2[j][z] for t, j in zip(ts, js)) % p for z in range(a)]
                    else:
                        c2[i] = [rng.randrange(p) for _ in range(a)]
                if rng.random() < 0.5:
                    rng.shuffle(c2)
                ok2, l2, q2, tr2 = evaluate(Fd, c2)
                if not ok2:
                    print("FAILURE", p, k, a, tr2, c2, flush=True)
                if (l2, q2) >= bs:
                    best, bs, tr = c2, (l2, q2), tr2
            if best_all is None or bs > best_all[0]:
                best_all = (bs, best, tr)
        bs, best, tr = best_all
        out["%d,%d,%d" % (p, k, a)] = dict(load=bs[0], q=bs[1], trace=[[d, c, i] for d, c, i in tr], cols=best)
        print(p, k, a, "best load", bs[0], "max stall q", bs[1], [c for _, c, _ in tr], flush=True)
json.dump(out, open("heavy_banks_%d.json" % seed, "w"))
