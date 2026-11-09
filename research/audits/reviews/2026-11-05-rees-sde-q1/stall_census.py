"""Census of Theorem-2 forward-pass stalls (no snapshots, no repairs) on structured banks
at the budget D_3(a)+a, classified by (q, q+, eps, |X|), then ALG-Q1 on each stalled bank.
Also a hill climb that maximises the stall codimension q (target: q>=3 with q+<=1).
Usage: stall_census.py seed trials climb_steps"""
import sys
import random
from collections import Counter
from q1core import Field, D, forward, init_state, check
from q1solve import solve, classify
from fams import family_list

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 4
steps = int(sys.argv[3]) if len(sys.argv) > 3 else 200
rng = random.Random(seed)
E = 3


def stall_of(Fd, cols):
    if any(not any(c) for c in cols):
        return None
    st = init_state(Fd, cols)
    s = forward(Fd, cols, E, random.Random(0), st, rule="first")
    if s != "stall":
        return None
    return classify(Fd, cols, st)


def score(cl):
    if cl is None:
        return -1
    return 10 * cl["q"] - 3 * cl["qplus"] + min(cl["eps"], 3)


census = Counter()
alg = Counter()
hard = []
for (p, k) in [(1009, 2), (1009, 3)]:
    Fd = Field(p, k)
    nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
    for a in (5, 6, 7):
        M = D(a, E) + a
        for name, gen in family_list(rng, p, a, M, nr).items():
            for _ in range(trials):
                cols = gen()
                cl = stall_of(Fd, cols)
                if cl is None:
                    continue
                census[(cl["q"], cl["qplus"], cl["eps"] > 0)] += 1
                x, how = solve(Fd, cols, E, rng)
                alg[how.split("(")[0] if x is not None else how] += 1
                if x is not None:
                    assert check(Fd, cols, x)
                # hill climb from stalled banks of this family
                best, bs = cols, score(cl)
                for _ in range(steps):
                    c2 = [list(v) for v in best]
                    i = rng.randrange(M)
                    mode = rng.random()
                    if mode < 0.4:
                        j = rng.randrange(M)
                        t = rng.randrange(1, p)
                        c2[i] = [t * z % p for z in best[j]]
                    elif mode < 0.7:
                        j, j2 = rng.randrange(M), rng.randrange(M)
                        t, t2 = rng.randrange(1, p), rng.randrange(1, p)
                        c2[i] = [(t * z + t2 * w) % p for z, w in zip(best[j], best[j2])]
                    else:
                        c2[i] = [rng.randrange(p) for _ in range(a)]
                    rng.shuffle(c2)
                    cl2 = stall_of(Fd, c2)
                    s2 = score(cl2)
                    if s2 >= bs:
                        best, bs = c2, s2
                        if cl2 and cl2["q"] >= 3 and cl2["qplus"] <= 1:
                            hard.append((p, k, a, cl2, best))
                            break
print("stall census (q, q+, eps>0):", dict(sorted(census.items())))
print("ALG-Q1 on stalled banks:", dict(alg))
print("hill-climb hits with q>=3 and q+<=1:", len(hard))
res = Counter()
for p, k, a, cl, cols in hard[:60]:
    Fd = Field(p, k)
    x, how = solve(Fd, cols, E, rng)
    if x is not None:
        assert check(Fd, cols, x)
    res[how.split("(")[0] if x is not None else how] += 1
print("ALG-Q1 on those:", dict(res))
if hard:
    p, k, a, cl, cols = hard[-1]
    print("example", p, k, a, cl)
    print(cols)
