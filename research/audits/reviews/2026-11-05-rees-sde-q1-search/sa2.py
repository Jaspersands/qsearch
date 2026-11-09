"""Simulated annealing for ORDER-ROBUST failures of sss_full (the restart step R5).
usage: sa2.py kappa p a seed iters K seedfam outfile [M]
Score = mean over K fresh RANDOM orders of
   10*[one sss_full iteration fails] + 3*[critical stall] + [stall] + 0.25*pi
(pi, stall, critical from the Theorem-2 forward pass on that order).  Seeds: chain4,
chainfull (kappa=3), codim1_front, flag_sub.  Mutations: q1lib.mutate (replace, scale by a
non-residue, project into the span of 1..a-1 other columns, put on the line of another
column, swap positions, move into a plane of two others)."""
import json
import math
import os
import random
import sys
import time
from q1lib import (Field, budget, theorem_forward, one_order, mutate, sss_full,
                   fam_codim1_front, fam_flag_subthreshold)
from critical import chain4, chainfull
import indep

k, p, a, seed, iters, K = (int(v) for v in sys.argv[1:7])
seedfam, outfile = sys.argv[7], sys.argv[8]
M = int(sys.argv[9]) if len(sys.argv) > 9 else budget(a, 3)
rng = random.Random(seed)
Fd = Field(p, k)
T0 = float(os.environ.get("SA_T0", "0.3"))


def seed_bank():
    f = seedfam if seedfam != "mix" else rng.choice(["chain4", "chainfull", "codim1", "flag"])
    if f == "chainfull" and k != 3:
        f = "chain4"
    if f == "chain4":
        return chain4(Fd, rng, a, M)
    if f == "chainfull":
        return chainfull(Fd, rng, a, M)
    if f == "codim1":
        return fam_codim1_front(rng, p, a, M, rng.randint(2, 4))
    return fam_flag_subthreshold(rng, p, a, M)


def score(cols, KK=K):
    s, fails, pis = 0.0, 0, []
    for t in range(KK):
        perm = list(range(M))
        rng.shuffle(perm)
        pc = [cols[i] for i in perm]
        tf = theorem_forward(Fd, pc, rng=rng)
        pi = tf.get("pi", 0)
        pis.append(pi)
        st = tf["status"] == "stall"
        cr = st and tf["unused"] == 0 and tf["BoutU"] == tf["q"]
        x, status, cert = one_order(Fd, cols, perm, rng, passes=6)
        f = x is None
        fails += f
        s += 10 * f + 3 * cr + st + 0.25 * pi
    return s / KK, fails, max(pis)


cur = seed_bank()
cs, cf, _ = score(cur)
best = (cs, cf, cur)
maxpi = 0
found = []
t0 = time.time()
for it in range(iters):
    T = T0 * (1 - it / iters) + 0.02
    new, op = mutate(Fd, cur, rng)
    ns, nf, npi = score(new)
    maxpi = max(maxpi, npi)
    if nf:
        # confirm: failure rate over 40 fresh orders, then sss_full itself
        _, f40, _ = score(new, 40)
        x, st = sss_full(Fd, new, 3, rng, passes=10, forwards=3)
        rec = dict(it=it, cols=new, fails_of_K=nf, fails_of_40=f40, sss_full_fail=x is None,
                   sss_full_status=st)
        if x is None:
            w, how = indep.find_solution(indep.F(p, k), new, random.Random(1))
            rec.update(indep_witness=w, indep_how=how)
        found.append(rec)
        print("ORDERFAIL it=%d K-fails=%d fails/40=%d sss_full_fail=%s" % (it, nf, f40, x is None), flush=True)
    if ns >= cs or rng.random() < math.exp((ns - cs) / T):
        cur, cs, cf = new, ns, nf
        if cs > best[0]:
            best = (cs, cf, cur)
    if it % 100 == 0:
        print("it %d cur %.2f best %.2f maxpi %d found %d %.0fs" % (it, cs, best[0], maxpi, len(found), time.time() - t0), flush=True)
_, bf40, _ = score(best[2], 40)
json.dump(dict(kappa=k, p=p, a=a, M=M, seed=seed, seedfam=seedfam, iters=iters, K=K,
               best_score=best[0], best_fail_of_40=bf40, best_bank=best[2], max_pi=maxpi,
               found=found), open(outfile, "w"))
print("DONE best %.2f best_fail/40 %d maxpi %d found %d" % (best[0], bf40, maxpi, len(found)), flush=True)
