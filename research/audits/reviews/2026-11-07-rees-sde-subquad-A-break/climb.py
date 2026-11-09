"""Simulated annealing / hill climbing against ALG-T.  Usage: climb.py OBJ SEED STEPS

OBJ:
  slack   minimise the least slack over the count inequalities that decide a recursion
          (rec_count = cols in target - F(rank), M_outside_bound, I1, I2-type c30_outside,
          Tmb_outside, TS, Y_ineq, load_le_c, T2b_rounds)
  load    maximise the least absorption load at stalls in case 3 (pushes to the Rado flat)
  top     reward the top phase (T_m), then minimise the top-phase slacks
Starts from several of my families at kappa in {2,3}, J in {2,3,4}, r in {10..24}.
Every evaluated bank is fully checked (leaf (F1),(F2),(S), witness); any failure is saved.
"""
import json
import os
import random
import sys
import time
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from la import Fq  # noqa
from algt import Par, Rec, run_algt, Fail  # noqa
import checker  # noqa
import families  # noqa
from harness import save_failure  # noqa

OBJ = sys.argv[1]
SEED = int(sys.argv[2])
STEPS = int(sys.argv[3]) if len(sys.argv) > 3 else 150
rng = random.Random(SEED)
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
LOG = open(os.path.join(HERE, "out", "climb_%s_%d.out" % (OBJ, SEED)), "w")

KEYS = ["rec_count", "M_outside_bound", "I1", "c30_outside", "Tmb_outside", "TS", "Y_ineq",
        "load_le_c", "T2b_rounds", "I2"]
STATS = Counter()
MINSLACK = {}
FAILS = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def evaluate(bank, p, k, J, Fd, kw):
    par = Par(J, k, **kw)
    par.least_load = OBJ == "load"
    STATS["evals"] += 1
    try:
        out, rec = run_algt(Fd, bank, par)
    except Fail as ex:
        fn = save_failure("climb_fail", bank, p, k, J, str(ex))
        FAILS.append(fn)
        log("FAIL", ex, fn)
        return -10 ** 9, None
    STATS.update(rec.branch)
    for kk, v in rec.slack.items():
        if kk not in MINSLACK or v < MINSLACK[kk]:
            MINSLACK[kk] = v
    if rec.viol:
        fn = save_failure("climb_viol", bank, p, k, J, rec.viol[:5])
        FAILS.append(fn)
        log("VIOL", rec.viol[:3], fn)
    kind, obj = out
    bl = [list(map(int, v)) for v in bank]
    if kind == "leaf":
        probs, info = checker.check_leaf(bl, p, k, J, obj, c=par.c)
    else:
        probs = checker.check_witness(bl, p, k, obj)
    if probs:
        fn = save_failure("climb_check", bank, p, k, J, probs)
        FAILS.append(fn)
        log("CHECK", probs, fn)
    # score: higher = better for the attacker
    sl = [rec.slack[x] for x in KEYS if x in rec.slack]
    ms = min(sl) if sl else 10 ** 6
    br = rec.branch
    if OBJ == "slack":
        score = -ms + 5 * br["stall"] + 3 * (br["case31_W"] + br["top_stall_rec"] + br["case30_Uplus"]
                                            + br["case33_Uplus"] + br["case2_Y"])
    elif OBJ == "load":
        score = (max(rec.least_loads) if rec.least_loads else -1) * 10 + br["stall"]
    else:
        t = br["case33_top"] + br["top_stall_rec"] * 3 + br["case33_Uplus"] + br["case33_closure"]
        tsl = [rec.slack[x] for x in ("Tmb_outside", "TS", "rec_count_Hcur") if x in rec.slack]
        score = 20 * t + br["stall"] - (min(tsl) if tsl else 50) * 0.5
    return score, rec


def mutate(bank, r, p, rng):
    b = [list(v) for v in bank]
    M = len(b)
    u = rng.random()
    i = rng.randrange(r, M)
    if u < 0.25:
        j = rng.randrange(M)
        t = rng.randrange(1, p)
        b[i] = [t * z % p for z in b[j]]
    elif u < 0.45:
        j, j2 = rng.randrange(M), rng.randrange(M)
        t, t2 = rng.randrange(1, p), rng.randrange(1, p)
        b[i] = [(t * z + t2 * w) % p for z, w in zip(b[j], b[j2])]
    elif u < 0.55:
        js = rng.sample(range(M), rng.randrange(2, 5))
        v = [0] * r
        for j in js:
            t = rng.randrange(1, p)
            v = [(x + t * y) % p for x, y in zip(v, b[j])]
        b[i] = v
    elif u < 0.65:
        b[i] = [rng.randrange(p) for _ in range(r)]
    elif u < 0.85:
        j = rng.randrange(r, M)
        b[i], b[j] = b[j], b[i]
    else:
        j = rng.randrange(r, M)
        v = b.pop(i)
        b.insert(j, v)
    if not any(b[i]):
        b[i][0] = 1
    return b


def climb(p, k, J, r, fam, steps, kw):
    Fd = Fq(p, k)
    bank = families.make(fam, random.Random(rng.randrange(10 ** 9)), p, k, J, r)
    best_s, rec = evaluate(bank, p, k, J, Fd, kw)
    cur, cur_s = bank, best_s
    T0 = 3.0
    for it in range(steps):
        cand = mutate(cur, r, p, rng)
        s, rec = evaluate(cand, p, k, J, Fd, kw)
        temp = T0 * (1 - it / steps) + 0.05
        if s >= cur_s or rng.random() < np.exp((s - cur_s) / temp):
            cur, cur_s = cand, s
            if s > best_s:
                best_s = s
    return best_s


def main():
    t0 = time.time()
    combos = [(10007, 2, 2), (10007, 2, 3), (10007, 2, 4), (100003, 3, 3), (100003, 3, 4)]
    fams = ["planted", "planted2", "twist", "adapt_rado", "adapt_top", "adapt_mix", "nested", "repeat"]
    n = 0
    while True:
        for (p, k, J) in combos:
            r = rng.choice([10, 12, 14, 16, 20, 24] if J <= 3 else [16, 20, 24])
            fam = rng.choice(fams)
            kw = dict(sigma_place="index") if fam.startswith("adapt") else {}
            b = climb(p, k, J, r, fam, STEPS, kw)
            n += 1
            log("climb", n, "p=%d k=%d J=%d r=%d fam=%s best=%s evals=%d %.0fs" %
                (p, k, J, r, fam, b, STATS["evals"], time.time() - t0))
            with open(os.path.join(HERE, "out", "climb_%s_%d.json" % (OBJ, SEED)), "w") as f:
                json.dump(dict(stats=dict(STATS), minslack=MINSLACK, fails=FAILS), f, indent=1)
            if time.time() - t0 > float(os.environ.get("CLIMB_SECONDS", "3000")):
                log("TOTAL", dict(STATS), "minslack", MINSLACK, "fails", FAILS)
                return


if __name__ == "__main__":
    main()
