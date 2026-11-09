"""Randomised search for failures of the full algorithm (sss_full) on highly structured
banks: columns with entries in a small set {0, +-1, +-2} (many exact coincidences),
mixed with repeated/scaled columns.  Budget D_3(a) + a >= kappa*a + 1, so all solvable."""
import random
import sys
from sss import Field, sss_full, budget

def gen(rng, p, a, M, mode):
    if mode == "small":
        return [[rng.choice([0, 0, 1, p - 1, 2, p - 2]) for _ in range(a)] for _ in range(M)]
    if mode == "small01":
        cols = []
        while len(cols) < M:
            v = [rng.choice([0, 1]) for _ in range(a)]
            if any(v):
                cols.append(v)
        return cols
    if mode == "scaled":
        pal = [[rng.choice([0, 1, p - 1]) for _ in range(a)] for _ in range(a + 1)]
        pal = [v for v in pal if any(v)] or [[1] * a]
        return [[rng.randrange(1, p) * t % p for t in rng.choice(pal)] for _ in range(M)]
    raise ValueError

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
E = 3
fails, tot, stats = [], 0, {}
for (p, k, As) in [(257, 2, (3, 4, 5, 6)), (1009, 2, (3, 5, 7)), (2791, 3, (4, 5, 6)), (3001, 3, (4, 6))]:
    Fd = Field(p, k)
    for a in As:
        M = budget(a, E)
        for mode in ("small", "small01", "scaled"):
            for t in range(40):
                cols = gen(rng, p, a, M, mode)
                x, st = sss_full(Fd, cols, E, rng, passes=10, forwards=2)
                tot += 1
                key = st.split("(")[0].split("[")[0] if x is not None else st
                stats[key] = stats.get(key, 0) + 1
                if x is None:
                    fails.append((p, k, a, mode, st, cols))
                    print("FAIL", p, k, a, mode, st, cols, flush=True)
        print(p, k, a, "done", stats, flush=True)
print("TOTAL", tot, "fails", len(fails), stats)
