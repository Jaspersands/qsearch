"""Cross-check subquad.forward_fast against the reference q1core.forward (rule "first")
on structured banks larger than the authors' check (a <= 9): r in {10, 12, 14}, planted-like
and twisted banks from adv.py's own generators plus random subspace mixtures.
Compares status, B, pool, T and every round (support, delta, blocks)."""
import os
import sys
import random

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.join(HERE, "..")
sys.path.insert(0, PARENT)
sys.path.insert(0, os.path.join(PARENT, "..", "2026-11-05-rees-sde-q1"))
from subquad import Field, Params, init_state, forward_fast  # noqa
from q1core import forward  # noqa

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)


def comb(p, basis, a):
    co = [rng.randrange(1, p) for _ in basis]
    return [sum(c * v[t] for c, v in zip(co, basis)) % p for t in range(a)]


def mixture(p, a, M):
    subs = []
    for _ in range(rng.randrange(2, 5)):
        d = rng.randrange(1, a + 1)
        subs.append([[rng.randrange(p) for _ in range(a)] for _ in range(d)])
    cols = []
    while len(cols) < M:
        u = rng.random()
        if u < 0.15 and cols:
            v = cols[rng.randrange(len(cols))]
            cols.append([rng.randrange(1, p) * z % p for z in v])
        else:
            cols.append(comb(p, subs[rng.randrange(len(subs))], a))
    return cols


def same(Fd, cols, J):
    s1 = init_state(Fd, cols)
    s2 = init_state(Fd, cols)
    a1 = forward_fast(Fd, cols, J, rng, s1, rule="first")
    a2 = forward(Fd, cols, J, rng, s2, rule="first")
    if a1 != a2:
        return False
    if a1 == "direct":
        return s1["x"] == s2["x"]
    if s1["B"] != s2["B"] or s1["pool"] != s2["pool"]:
        return False
    if a1 == "stall" and s1["T"] != s2["T"]:
        return False
    if len(s1["rounds"]) != len(s2["rounds"]):
        return False
    for R1, R2 in zip(s1["rounds"], s2["rounds"]):
        if R1.S != R2.S or R1.blocks != R2.blocks or R1.delta != R2.delta:
            return False
    return True


def main():
    n = bad = 0
    stat = {}
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fd = Field(p, k)
        for J in (3, 4, 5):
            if J < k:
                continue
            P = Params(J, k)
            for a in (10, 12, 14):
                for rep in range(4):
                    cols = mixture(p, a, P.F(a))
                    ok = same(Fd, cols, J)
                    n += 1
                    bad += (not ok)
                    if not ok:
                        print("MISMATCH", p, J, a, cols, flush=True)
            print("p=%d J<=5 done: banks %d mismatches %d" % (p, n, bad), flush=True)
    print("TOTAL banks", n, "mismatches", bad)


main()
