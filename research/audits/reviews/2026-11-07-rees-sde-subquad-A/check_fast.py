"""Cross-check forward_fast (subquad.py) against q1core.forward (reference) on random and
structured banks: identical rounds (supports, relations, blocks), B, pool, T and status."""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-05-rees-sde-q1"))
from subquad import Field, forward_fast, init_state, Params  # noqa
from q1core import forward  # noqa
from fams import family_list  # noqa
rng = random.Random(5)
n = bad = 0
for (p, k) in [(1009, 2), (10007, 2), (1009, 3), (100003, 3)]:
    Fd = Field(p, k)
    nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
    for J in (3, 4, 5):
        if J < k:
            continue
        for a in (3, 5, 7, 9):
            M = Params(J, k).F(a)
            for name, gen in family_list(rng, p, a, M, nr).items():
                cols = gen()
                if not all(any(v) for v in cols):
                    continue
                s1, s2 = init_state(Fd, cols), init_state(Fd, cols)
                r1 = forward(Fd, cols, J, rng, s1, rule="first")
                r2 = forward_fast(Fd, cols, J, rng, s2, rule="first")
                same = (r1 == r2 and s1["B"] == s2["B"] and s1["pool"] == s2["pool"] and
                        s1.get("T") == s2.get("T") and len(s1["rounds"]) == len(s2["rounds"]) and
                        all(R1.S == R2.S and R1.delta == R2.delta and R1.blocks == R2.blocks
                            for R1, R2 in zip(s1["rounds"], s2["rounds"])) and s1.get("x") == s2.get("x"))
                n += 1
                bad += not same
                if not same:
                    print("MISMATCH", p, k, J, a, name)
print("banks", n, "mismatches", bad)
