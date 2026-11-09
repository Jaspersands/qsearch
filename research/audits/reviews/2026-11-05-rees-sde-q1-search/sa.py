"""Simulated annealing over banks to break Conjecture 5.
usage: sa.py kappa p a M seed iters K [start_family] [outfile]
Score(bank) averages over K column orders (identity + K-1 random):
   10 * [one sss_full iteration fails]  +  3 * [critical stall]  +  [stall]  +  0.25 * pi
where pi, stall and 'critical' (q = r - dim U_L, no unused column, |B \\ U_L| = q) come from
the exact Theorem-2 forward pass (sss_theorem's forward) on that order.  Every bank whose
score has a failing order is re-tested with sss_full (forwards=3) and, if it fails,
recorded with its stall certificate."""
import json
import math
import random
import sys
import time
from q1lib import (Field, budget, theorem_forward, one_order, mutate, sss_full, check,
                   fam_lines, fam_codim1_front, fam_flag_subthreshold, fam_random, fam_pairs,
                   fam_basis_dense, fam_lines_planes, fam_planes)

k, p, a, M, seed, iters, K = (int(v) for v in sys.argv[1:8])
start = sys.argv[8] if len(sys.argv) > 8 else "mix"
outfile = sys.argv[9] if len(sys.argv) > 9 else None
rng = random.Random(seed)
Fd = Field(p, k)


def start_bank():
    fam = start if start != "mix" else rng.choice(
        ["lines", "codim1", "flag", "random", "pairs", "basisdense", "linesplanes", "planes"])
    if fam == "lines":
        return fam_lines(rng, p, a, M, rng.randint(a, a + 3))
    if fam == "codim1":
        return fam_codim1_front(rng, p, a, M, rng.randint(2, 4))
    if fam == "flag":
        return fam_flag_subthreshold(rng, p, a, M)
    if fam == "pairs":
        return fam_pairs(rng, p, a, M)
    if fam == "basisdense":
        return fam_basis_dense(rng, p, a, M, rng.randint(1, a - 1))
    if fam == "linesplanes":
        return fam_lines_planes(rng, p, a, M, rng.randint(1, a), rng.randint(1, a))
    if fam == "planes":
        return fam_planes(rng, p, a, M, rng.randint(2, a + 1))
    return fam_random(rng, p, a, M)


def score(cols):
    s, maxpi, fails, crit = 0.0, 0, 0, 0
    for t in range(K):
        perm = list(range(M))
        if t:
            rng.shuffle(perm)
        pc = [cols[i] for i in perm]
        tf = theorem_forward(Fd, pc, rng=rng)
        pi = tf.get("pi", 0)
        maxpi = max(maxpi, pi)
        st = tf["status"] == "stall"
        cr = st and tf["unused"] == 0 and tf["BoutU"] == tf["q"]
        crit += cr
        x, status, cert = one_order(Fd, cols, perm, rng, passes=6)
        f = x is None
        fails += f
        s += 10 * f + 3 * cr + st + 0.25 * pi
    return s / K, maxpi, fails, crit


cur = start_bank()
cs, cpi, cf, cc = score(cur)
best = (cs, cur)
T0 = float(__import__("os").environ.get("SA_T0", "0.5"))
found = []
maxpi_seen = cpi
t0 = time.time()
for it in range(iters):
    T = T0 * (1 - it / iters) + 0.05
    if it and it % 400 == 0 and cs < 1.0:
        cur = start_bank()           # restart from a fresh family member
        cs, cpi, cf, cc = score(cur)
    new, op = mutate(Fd, cur, rng)
    ns, npi, nf, nc = score(new)
    maxpi_seen = max(maxpi_seen, npi)
    if nf:
        x, st = sss_full(Fd, new, 3, rng, passes=10, forwards=3)
        if x is None:
            found.append(dict(cols=new, status=st, score=ns, order_fails=nf, K=K))
            print("FAIL sss_full", it, st, json.dumps(new), flush=True)
    if ns >= cs or rng.random() < math.exp((ns - cs) / T):
        cur, cs = new, ns
        if cs > best[0]:
            best = (cs, cur)
    if it % 200 == 0:
        print("it", it, "cur %.2f best %.2f maxpi %d fails_found %d  %.0fs" % (
            cs, best[0], maxpi_seen, len(found), time.time() - t0), flush=True)
res = dict(kappa=k, p=p, a=a, M=M, seed=seed, iters=iters, K=K, best_score=best[0],
           best_bank=best[1], max_pi=maxpi_seen, failures=found)
print("DONE", json.dumps(dict(kappa=k, p=p, a=a, M=M, best=best[0], maxpi=maxpi_seen,
                              nfail=len(found))), flush=True)
if outfile:
    json.dump(res, open(outfile, "w"))
