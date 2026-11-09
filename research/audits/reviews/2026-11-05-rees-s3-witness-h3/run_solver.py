"""Measurements of the mu_h-digit weight-doubling solver (table variant).

For each (h, p): exact depth J, exact or Monte Carlo covering time s_p, exact expected reads
N_0(n); runs on fresh uniform columns; every output (and every inhomogeneous level-j output) is
checked exactly: nonempty, distinct indices, nonzero weights in D_level, correct weighted sum.

Usage: python run_solver.py out.json [quick]
"""
import json
import math
import sys
import time
import numpy as np

from wh_lib import (Chain, Stream, solve, check, covering_time_exact, covering_time_mc,
                    expected_reads)

quick = len(sys.argv) > 2
rng = np.random.default_rng(20261105)
CASES = [(3, 7), (3, 13), (3, 19), (3, 31), (4, 5), (4, 13), (4, 17)]
BUDGET = 25000 if quick else 120000     # target total reads per row (runs * N_0)

out = {"cases": {}}
for h, p in CASES:
    t0 = time.time()
    ch = Chain(h, p)
    J = ch.J
    if p <= 17:
        s = covering_time_exact(p)
        s_f, s_err, s_kind = float(s), 0.0, "exact"
    else:
        s_f, s_err = covering_time_mc(p, 200000, seed=p)
        s, s_kind = s_f, "monte carlo (200000 draws)"
    rows = []
    # choose n values
    ns = []
    for n in range(1, 40):
        N = float(expected_reads(J, n, s))
        if N * 8 > BUDGET:
            break
        ns.append(n)
    if len(ns) > 6:
        ns = sorted({ns[round(i * (len(ns) - 1) / 5)] for i in range(6)})
    for n in ns:
        N = float(expected_reads(J, n, s))
        runs = int(min(400, max(8, BUDGET // max(N, 1))))
        reads = []
        allok = True
        for _ in range(runs):
            st = Stream(p, n, rng)
            I, W = solve(ch, 0, n, np.zeros(n, dtype=np.int64), st)
            allok &= check(ch, st, I, W, n, np.zeros(n, dtype=np.int64), 0)
            reads.append(st.count)
        m = float(np.mean(reads))
        se = float(np.std(reads, ddof=1) / math.sqrt(runs)) if runs > 1 else float("nan")
        rows.append({"n": n, "runs": runs, "mean": m, "se": se, "N0": N,
                     "z": (m - N) / se if se > 0 else 0.0, "all_checked_ok": bool(allok),
                     "max_reads": int(max(reads))})
    # inhomogeneous targets at every level j < J, small n
    inh = {}
    for lev in range(J):
        ok, tot = 0, 0
        for n in range(1, 5):
            for _ in range(5):
                tgt = rng.integers(0, p, n)
                st = Stream(p, n, rng, cap=10 ** 6)
                I, W = solve(ch, lev, n, tgt, st)
                ok += check(ch, st, I, W, n, tgt, lev)
                tot += 1
        inh[lev] = [ok, tot]
    # exact slopes of log N_0 between n and 2n
    slopes = {}
    for n in (32, 64, 128):
        a, b = float(expected_reads(J, n, s_f)), float(expected_reads(J, 2 * n, s_f))
        slopes[n] = math.log(b / a) / math.log(2)
    out["cases"][f"h={h},p={p}"] = {"kappa": (p - 1) // h, "J": J, "sizes": [len(D) for D in ch.D],
                                    "s_p": s_f, "s_p_se": s_err, "s_kind": s_kind,
                                    "s_p_exact": str(s) if s_kind == "exact" else None,
                                    "rows": rows, "inhomogeneous": inh, "slopes": slopes,
                                    "degree": 1 + J, "seconds": time.time() - t0}
    print(h, p, "J", J, "s", round(s_f, 4), [(r["n"], round(r["z"], 2), r["all_checked_ok"]) for r in rows],
          inh, {k: round(v, 3) for k, v in slopes.items()}, round(time.time() - t0, 1), flush=True)

zs = [r["z"] for c in out["cases"].values() for r in c["rows"]]
out["max_abs_z"] = max(abs(z) for z in zs)
out["all_outputs_ok"] = all(r["all_checked_ok"] for c in out["cases"].values() for r in c["rows"])
out["all_inhomogeneous_ok"] = all(v[0] == v[1] for c in out["cases"].values() for v in c["inhomogeneous"].values())
with open(sys.argv[1], "w") as f:
    json.dump(out, f, indent=1)
print("max|z|", out["max_abs_z"], "outputs ok", out["all_outputs_ok"], "inhom ok", out["all_inhomogeneous_ok"])
