"""Experiments for the weight-doubling solver (report section C1).

Usage: nice -n 10 /opt/anaconda3/bin/python exp_doubling.py PART OUT.json
PART in {A, B}: A = p in {3,5,7}, B = p in {11,13,17}.  Each part stays under ~20 min.

For every (p, n): R independent runs on fresh uniform columns; every output is checked
exactly (nonempty, distinct indices, weights 1, zero sum over all n coordinates).  Records the
mean and standard error of the number of columns read, the exact expectation N_0(n), and the
closed-form bound.  Also: inhomogeneous targets at levels 0 and 1 (checked exactly), and a
Monte Carlo check of the covering time s_p.
"""
import json
import math
import sys
import time

import numpy as np

from doubling import (Stream, solve, check_solution, binsis, covering_time,
                      expected_consumption, closed_form_bound, jstar_of)

PLAN = {
    "A": [(3, [8, 16, 32, 64, 96], 200), (5, [4, 8, 12, 16, 24, 32], 40),
          (7, [3, 4, 6, 8, 10, 12, 14], 25)],
    "B": [(11, [2, 3, 4, 5, 6, 7, 8], 25), (13, [2, 3, 4, 5, 6, 7, 8], 25),
          (17, [2, 3, 4, 5, 6, 7], 20)],
}


def covering_mc(p, trials, rng):
    tot = 0
    for _ in range(trials):
        R = {0}
        s = 0
        while len(R) < p:
            b = int(rng.integers(0, p))
            R |= {(r + b) % p for r in R}
            s += 1
        tot += s
    return tot / trials


def inhomogeneous_checks(p, n, level, trials, rng):
    """Random targets; level-0 and level-1 solves; exact checks."""
    js = jstar_of(p)
    ok = 0
    for _ in range(trials):
        st = Stream(p, n, rng)
        t = rng.integers(0, p, n)
        I, W = solve(level, n, t, st, p, js)
        ok += check_solution(st, I, W, n, t, p, level)
    return ok


def main():
    part, out = sys.argv[1], sys.argv[2]
    rng = np.random.default_rng(20261105 + ord(part))
    res = {"part": part, "rows": [], "covering": [], "inhomogeneous": []}
    t0 = time.time()
    for p, ns, R in PLAN[part]:
        sp = covering_time(p)
        mc = covering_mc(p, 20000, rng)
        res["covering"].append({"p": p, "s_p_exact": float(sp), "s_p_str": str(sp), "mc_20000": mc})
        for lev in ([0, 1] if jstar_of(p) > 1 else [0]):
            nn = min(ns[-1], 6)
            ok = inhomogeneous_checks(p, nn, lev, 10, rng)
            res["inhomogeneous"].append({"p": p, "n": nn, "level": lev, "ok": ok, "of": 10})
        for n in ns:
            cs = []
            tt = time.time()
            for _ in range(R):
                I, c, st = binsis(p, n, rng)
                # independent re-check of the zero sum over all n coordinates
                assert len(I) > 0 and len(set(I.tolist())) == len(I)
                assert np.all(st.buf[I, :n].astype(np.int64).sum(axis=0) % p == 0)
                cs.append(c)
            cs = np.array(cs, dtype=float)
            exact = float(expected_consumption(p, n, sp))
            row = {"p": p, "n": n, "runs": R, "all_checked": True,
                   "mean": cs.mean(), "stderr": cs.std(ddof=1) / math.sqrt(R),
                   "min": cs.min(), "max": cs.max(),
                   "exact_expectation": exact,
                   "z": (cs.mean() - exact) / (cs.std(ddof=1) / math.sqrt(R)),
                   "closed_form_bound": float(closed_form_bound(p, n, sp)),
                   "exponent_1_plus_jstar": 1 + jstar_of(p),
                   "seconds": time.time() - tt}
            res["rows"].append(row)
            print(json.dumps(row), flush=True)
            with open(out, "w") as f:
                json.dump(res, f, indent=1)
    res["total_seconds"] = time.time() - t0
    with open(out, "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
