"""Families on which recursive SSS stalled, with the F1 fallback and random orders."""
import random
from sss import Field, sss_full, budget
from run_adversarial import fam_lines, fam_subspace, fam_flag, fam_sparse

rng = random.Random(11)
E = 3
tot = {}
for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (10009, 3)]:
    Fd = Field(p, k)
    for a in ((3, 4, 5, 7, 9) if k == 2 else (4, 5, 6, 8)):
        M = budget(a, E)
        fams = {"lines_a+1": lambda: fam_lines(rng, p, a, M, a + 1),
                "lines_a+2": lambda: fam_lines(rng, p, a, M, a + 2),
                "lines_a": lambda: fam_lines(rng, p, a, M, a),
                "subsp_a-1": lambda: fam_subspace(rng, p, a, M, a - 1, 0.8),
                "flag": lambda: fam_flag(rng, p, a, M),
                "sparse": lambda: fam_sparse(rng, p, a, M)}
        for name, gen in fams.items():
            out = {}
            for t in range(10):
                x, st = sss_full(Fd, gen(), E, rng, passes=10, forwards=1)
                key = st.split("(")[0] if x is not None else st
                out[key] = out.get(key, 0) + 1
                tot[x is not None] = tot.get(x is not None, 0) + 1
            print(p, k, a, M, name, out, flush=True)
print("TOTAL solved/failed", tot)
