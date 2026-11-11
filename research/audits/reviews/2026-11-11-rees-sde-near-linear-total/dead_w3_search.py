"""Local search for dead banks of 2d+1 = 7 columns in F_p^3 (kappa = 3), and 9 in F_p^4.

A dead bank of 2d+1 columns would show N(kappa, d, p) > 2d+1. Search only falsifies:
not finding one proves nothing. Control: p = 7 (P = {+-1}), where dead 7-sets in F_7^3
exist (a dead 5-set in a plane plus a dead pair).
Objective: number of projective P0-solutions; moves: re-draw one column (random class),
or (structured restarts) seed with dead pairs. Accept if not worse; restart after a stall.
Run: nice -n 19 /opt/anaconda3/bin/python -I dead_w3_search.py
"""
import argparse
import random
import sys
import time

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdecore import coset_table, rank_mod, solutions_count_p0  # noqa: E402


def score(cols, p, cos, d, kap=3):
    if rank_mod(cols, p) < d:
        return 10 ** 9
    return solutions_count_p0(cols, p, kap)


def rand_col(rng, p, d):
    while True:
        c = [rng.randrange(p) for _ in range(d)]
        if any(c):
            return c


def _has_prop(cols, p, idx):
    a = cols[idx]
    for j, b in enumerate(cols):
        if j == idx:
            continue
        dep, ratio = True, None
        for x, y in zip(a, b):
            if (x == 0) != (y == 0):
                dep = False
                break
            if x != 0:
                r = (y * pow(x, p - 2, p)) % p
                if ratio is None:
                    ratio = r
                elif ratio != r:
                    dep = False
                    break
        if dep:
            return True
    return False


def rand_ssc_col(rng, cols, idx, p, d):
    while True:
        cols[idx] = rand_col(rng, p, d)
        if not _has_prop(cols, p, idx):
            return


def search(p, kap, d, n, budget_s, rng, ssc=False):
    g, cos = coset_table(p, kap)
    nonP = (-g) % p  # pair (e, c e) with -c = g not in P is dead
    t0, evals, best_overall = time.time(), 0, None
    restarts = 0
    while time.time() - t0 < budget_s:
        restarts += 1
        if ssc:
            cols = []
            for _ in range(n):
                cols.append(rand_col(rng, p, d))
                rand_ssc_col(rng, cols, len(cols) - 1, p, d)
        elif restarts % 2:
            cols = [rand_col(rng, p, d) for _ in range(n)]
        else:  # structured seed: floor(n/2) - 1 dead pairs on random independent directions
            cols = []
            for _ in range(n // 2 - 1):
                v = rand_col(rng, p, d)
                cols += [v, [nonP * x % p for x in v]]
            while len(cols) < n:
                cols.append(rand_col(rng, p, d))
        s = score(cols, p, cos, d, kap=kap)
        stall = 0
        while stall < 400 and time.time() - t0 < budget_s:
            i = rng.randrange(n)
            old = cols[i]
            if ssc:
                rand_ssc_col(rng, cols, i, p, d)
            else:
                cols[i] = rand_col(rng, p, d)
            s2 = score(cols, p, cos, d, kap=kap)
            evals += 1
            if s2 <= s:
                stall = 0 if s2 < s else stall + 1
                s = s2
            else:
                cols[i] = old
                stall += 1
            if s == 0:
                return True, cols, evals, restarts, time.time() - t0
        if best_overall is None or s < best_overall:
            best_overall = s
    return False, best_overall, evals, restarts, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--item5", action="store_true", help="Run kappa=3, d=3..5, p in {19, 31, 37}")
    ap.add_argument("--ssc", action="store_true", help="Maintain no-proportional-pair s.s.c. seeds/moves")
    ap.add_argument("--budget", type=int, default=600)
    args = ap.parse_args()
    rng = random.Random(1111)
    print("kappa p d n found evals restarts seconds  [dead bank or least #proj solutions]")
    if args.item5:
        jobs = [(3, p, d, 2 * d + 1, args.budget) for d in (3, 4, 5) for p in (19, 31, 37)]
    else:
        jobs = [(3, 7, 3, 7, 120), (3, 13, 3, 7, 600), (3, 19, 3, 7, 600),
                (3, 13, 4, 9, 600), (4, 29, 3, 7, 300)]
    for (kap, p, d, n, bud) in jobs:
        found, info, ev, rs, sec = search(p, kap, d, n, bud, rng, ssc=args.ssc)
        print(kap, p, d, n, found, ev, rs, f"{sec:.0f}", info, flush=True)


if __name__ == "__main__":
    main()
