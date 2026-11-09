"""Banks built to reach the top-pair step of Theorem Q1: a small flat Y (dim b) holding a
basis part and many pool columns, a hyperplane H > Y realized by generic columns of H, and
the rest of the reserved basis outside H.  Checks Lemma T (bad pairs <= lower cross pairs)
and the success of the step.  Usage: run_top.py seed reps"""
import sys
import random
from collections import Counter
from q1core import Field, D, check
from alg_thm import solve_thm, f

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
reps = int(sys.argv[2]) if len(sys.argv) > 2 else 5
rng = random.Random(seed)
E = 3


def comb(basis, a, p):
    co = [rng.randrange(1, p) for _ in basis]
    return [sum(c * v[t] for c, v in zip(co, basis)) % p for t in range(a)]


def bank(p, a, b, extraH):
    M = f(a)
    G = [[rng.randrange(p) for _ in range(a)] for _ in range(a)]   # random basis of V
    Y, H = G[:b], G[:a - 1]
    cols = [comb(Y, a, p) for _ in range(b)]                        # B cap Y
    cols += [[rng.randrange(p) for _ in range(a)] for _ in range(a - b)]  # rest of B, generic
    NH = D(a - 1, E) - D(b, E) + extraH
    NY = M - len(cols) - NH
    cols += [comb(Y, a, p) for _ in range(NY)]
    cols += [comb(H, a, p) for _ in range(NH)]
    return cols


cases = Counter()
stats = []
for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (10009, 3)]:
    Fd = Field(p, k)
    for a in (6, 8, 10, 12):
        for b in (1, 2, 3):
            for extraH in (0, 1, 2, 4):
                for _ in range(reps):
                    cols = bank(p, a, b, extraH)
                    tr = []
                    x = solve_thm(Fd, cols, rng, trace=tr)
                    ok = x is not None and check(Fd, cols, x)
                    key = "/".join(c for _, c, _ in tr)
                    cases[(ok, key)] += 1
                    for _, c, info in tr:
                        if c == "top-pair":
                            stats.append((p, k, a, b, info))
for kk, v in sorted(cases.items(), key=lambda t: -t[1]):
    print(v, kk)
print("top-pair steps:", len(stats))
if stats:
    print("max bad pairs", max(s[4]["bad"] for s in stats),
          "max bad/rho", max(s[4]["bad"] / max(1, s[4]["rho"]) for s in stats),
          "min pairs", min(s[4]["pairs"] for s in stats))
