"""Exhaustive / massive search at tiny parameters.  Usage: exhaust.py MODE SEED

MODE ex2   : every multiset (in sorted order) of F(2) columns of F_p^2 up to P-scaling,
             (p, kappa, J) in {(3,2,2), (3,2,3), (5,2,2), (5,2,3), (7,3,3), (7,2,2)} (7,3,3 sampled
             if too many); the deterministic part of Theorem A is claimed at every prime.
MODE rnd   : random banks at a in {3,4,5,6}, small p, palette of short-support vectors,
             random orders, M = F(a) (and F(a)+1, +2), J in {2,3,4}.
Every leaf checked (F1),(F2),(S); every witness verified; violations saved.
"""
import itertools
import json
import os
import random
import sys
import time
from collections import Counter
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from la import Fq  # noqa
from algt import Par, Rec, run_algt, Fail  # noqa
import checker  # noqa
from harness import save_failure  # noqa

MODE = sys.argv[1]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
rng = random.Random(SEED)
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
LOG = open(os.path.join(HERE, "out", "exhaust_%s_%d.out" % (MODE, SEED)), "w")


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def reps(p, k, a):
    P = sorted({pow(y, k, p) for y in range(1, p)})
    seen, out = set(), []
    for v in itertools.product(range(p), repeat=a):
        if not any(v) or v in seen:
            continue
        orb = [tuple(t * x % p for x in v) for t in P]
        seen.update(orb)
        out.append(min(orb))
    return sorted(out)


def run(bank, p, k, J, Fd, tot, tag):
    par = Par(J, k)
    try:
        out, rec = run_algt(Fd, bank, par)
    except Fail as ex:
        tot["FAIL"] += 1
        log("FAIL", tag, ex, save_failure("ex_fail", bank, p, k, J, str(ex)))
        return
    tot.update({"br_" + x: v for x, v in rec.branch.items()})
    if rec.viol:
        tot["VIOL"] += 1
        log("VIOL", tag, rec.viol[:3], save_failure("ex_viol", bank, p, k, J, rec.viol[:3]))
    kind, obj = out
    bl = [list(v) for v in bank]
    if kind == "leaf":
        probs, info = checker.check_leaf(bl, p, k, J, obj, c=par.c)
        tot["leaf_" + obj["kind"]] += 1
    else:
        probs = checker.check_witness(bl, p, k, obj)
        tot["solution"] += 1
    if probs:
        tot["BAD"] += 1
        log("BAD", tag, probs, save_failure("ex_bad", bank, p, k, J, probs))
    for kk, v in rec.slack.items():
        key = "minslack_" + kk
        if key not in tot or v < tot[key]:
            tot[key] = v


def ex2():
    for (p, k, J) in [(3, 2, 2), (3, 2, 3), (5, 2, 2), (5, 2, 3), (7, 2, 2), (7, 3, 3), (7, 2, 3)]:
        Fd = Fq(p, k)
        R = reps(p, k, 2)
        M = Par(J, k).F(2)
        n = comb(len(R) + M - 1, M)
        tot = Counter()
        t0 = time.time()
        if n <= 400000:
            it = itertools.combinations_with_replacement(R, M)
            mode = "exhaustive"
        else:
            it = (sorted(rng.choice(R) for _ in range(M)) for _ in range(150000))
            mode = "sampled"
        for ms in it:
            tot["banks"] += 1
            run([list(v) for v in ms], p, k, J, Fd, tot, "ex2_p%d_J%d" % (p, J))
        log("ex2", mode, "p=%d k=%d J=%d M=%d reps=%d multisets=%d %.0fs" % (p, k, J, M, len(R), n,
                                                                            time.time() - t0),
            json.dumps(dict(tot)))


def rnd():
    t0 = time.time()
    budget = float(os.environ.get("EX_SECONDS", "2400"))
    tot = Counter()
    combos = [(3, 2), (5, 2), (7, 2), (11, 2), (13, 2), (7, 3), (13, 3), (19, 3)]
    Fds = {(p, k): Fq(p, k) for p, k in combos}
    while time.time() - t0 < budget:
        p, k = rng.choice(combos)
        J = rng.choice([j for j in (2, 3, 4) if j >= k])
        a = rng.choice([3, 4, 4, 5, 5, 6])
        par = Par(J, k)
        M = par.F(a) + rng.choice([0, 0, 0, 1, 2])
        supp = rng.choice([1, 2, 2, 3, a])
        pal = []
        for _ in range(rng.randrange(a + 1, 3 * a + 3)):
            v = [0] * a
            for j in rng.sample(range(a), min(a, rng.randrange(1, supp + 1))):
                v[j] = rng.randrange(1, p)
            pal.append(v)
        bank = []
        basis_first = rng.random() < 0.5
        if basis_first:
            for i in range(a):
                v = [0] * a
                v[i] = rng.randrange(1, p)
                bank.append(v)
        while len(bank) < M:
            v = rng.choice(pal)
            t = rng.randrange(1, p)
            bank.append([t * x % p for x in v])
        if not basis_first:
            rng.shuffle(bank)
        tot["banks"] += 1
        tot["J%d" % J] += 1
        run(bank, p, k, J, Fds[(p, k)], tot, "rnd_p%d_k%d_J%d_a%d" % (p, k, J, a))
        if tot["banks"] % 2000 == 0:
            log("progress", "%.0fs" % (time.time() - t0), json.dumps(dict(tot)))
    log("rnd TOTAL %.0fs" % (time.time() - t0), json.dumps(dict(tot)))


if __name__ == "__main__":
    {"ex2": ex2, "rnd": rnd}[MODE]()
