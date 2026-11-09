"""Nested paired-hyperplane banks: a flag V = H_0 > H_1 > ... > H_L, with t_j columns in
H_{j-1} \\ H_j ('paired': c = mu w_j + h, mu in P, h in H_j) and the rest generic in H_L.
Aim: the top level stalls critically with U_L = H_1 (then R3 recurses into H_1, where
there is no finishing pass), and the depth-1 pass stalls too.
usage: nested.py kappa p seed banks orders a t1,t2,...
Random orders only; counts sss_full single-iteration failures and Theorem-2 stalls."""
import collections
import random
import sys
from q1lib import Field, budget, theorem_forward, one_order, rvec, comb, sss_full

k, p, seed, NB, NO, a = (int(v) for v in sys.argv[1:7])
ts = [int(x) for x in sys.argv[7].split(",")]
rng = random.Random(seed)
Fd = Field(p, k)
M = budget(a, 3)


def bank():
    base = [rvec(rng, p, a) for _ in range(a)]   # H_j = span(base[:a-j])
    cols = []
    for j, t in enumerate(ts):
        Hj = base[:a - j - 1]
        w = base[a - j - 1]
        for _ in range(t):
            mu = Fd.randP(rng)
            h = comb(rng, p, Hj, a)
            cols.append([(mu * x + y) % p for x, y in zip(w, h)])
    HL = base[:a - len(ts)]
    while len(cols) < M:
        cols.append(comb(rng, p, HL, a))
    return cols


tot = fails = stalls = crits = 0
C = collections.Counter()
for b in range(NB):
    cols = bank()
    for o in range(NO):
        perm = list(range(M))
        rng.shuffle(perm)
        tf = theorem_forward(Fd, [cols[i] for i in perm], rng=rng)
        if tf["status"] == "stall":
            stalls += 1
            crits += tf["unused"] == 0 and tf["BoutU"] == tf["q"]
        x, st, cert = one_order(Fd, cols, perm, rng, passes=8)
        tot += 1
        if x is None:
            fails += 1
            C[st] += 1
    xf, stf = sss_full(Fd, cols, 3, rng, passes=10, forwards=3)
    if xf is None:
        print("SSS_FULL FAIL", cols, flush=True)
print("k=%d p=%d a=%d M=%d t=%s : stall %d crit %d fail %d / %d orders %s" % (
    k, p, a, M, ts, stalls, crits, fails, tot, dict(C)), flush=True)
