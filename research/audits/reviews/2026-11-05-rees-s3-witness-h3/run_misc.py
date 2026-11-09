"""Further checks for the mu_h-digit witness sampler.

  first_moment : exhaustive existence of D-witnesses at arity a + k vs ((h+1)^M - 1)/p^a.
  biased       : columns with entries uniform on {0,1}: mean reads should miss N_0 (control).
  hyperplane   : last coordinate = first coordinate: every top-level beta vanishes; the capped
                 solver must exhaust its cap every time and never return a wrong output.
  scaled       : the J = 1 variant (scaling switches to beta = 2^k, randomized splitting) at
                 large primes, with the kappa-th root conversion at d = kappa; reads compared with
                 the exact expectation 1 + K p/(p-1) n(n+1)/2, K = bitlength(p-1).

Usage: python run_misc.py out.json
"""
import itertools
import json
import math
import random
import sys
import time
import numpy as np
from sympy.ntheory.residue_ntheory import nthroot_mod
from sympy import isprime

from wh_lib import (Chain, Stream, solve, check, Exhausted, mu, covering_time_exact,
                    expected_reads, BigStream, solve_scaled, check_big, weil_ok,
                    weil_pairs_lower, chain_sets)

rng = np.random.default_rng(777)
out = {}

# ---------------------------------------------------------------- first moment
fm = []
for h, p, a, ks, banks in [(3, 7, 2, range(0, 6), 300), (3, 7, 3, range(0, 5), 200),
                           (4, 13, 2, range(0, 5), 200), (3, 13, 2, range(0, 5), 200)]:
    D = [0] + mu(h, p)
    for k in ks:
        M = a + k
        allv = np.array(list(itertools.product(D, repeat=M)), dtype=np.int64)[1:]  # drop 0
        hits = 0
        for _ in range(banks):
            X = rng.integers(0, p, (M, a))
            hits += bool(np.any(np.all((allv @ X) % p == 0, axis=1)))
        bound = ((h + 1) ** M - 1) / p ** a
        fm.append({"h": h, "p": p, "a": a, "M": M, "freq": hits / banks, "banks": banks,
                   "first_moment_bound": bound, "consistent": hits / banks <= min(1, bound) + 3 * math.sqrt(min(1, bound) / banks) + 1e-9})
        print("fm", fm[-1], flush=True)
out["first_moment"] = fm

# ---------------------------------------------------------------- biased columns
bias = []
for h, p, n, runs in [(3, 13, 6, 60), (4, 17, 3, 60)]:
    ch = Chain(h, p)
    N = float(expected_reads(ch.J, n, covering_time_exact(p)))
    reads = []
    ok = True
    for _ in range(runs):
        st = Stream(p, n, rng, cap=50 * int(N), gen=lambda kk, n=n: rng.integers(0, 2, (kk, n)))
        try:
            I, W = solve(ch, 0, n, np.zeros(n, dtype=np.int64), st)
            ok &= check(ch, st, I, W, n, np.zeros(n, dtype=np.int64), 0)
            reads.append(st.count)
        except Exhausted:
            reads.append(st.count)
    m, se = float(np.mean(reads)), float(np.std(reads, ddof=1) / math.sqrt(runs))
    bias.append({"h": h, "p": p, "n": n, "mean": m, "se": se, "N0": N, "z": (m - N) / se, "outputs_ok": bool(ok)})
    print("bias", bias[-1], flush=True)
out["biased"] = bias

# ---------------------------------------------------------------- hyperplane bank
hyp = []
for h, p, n in [(3, 13, 3), (3, 19, 3), (4, 17, 3)]:
    ch = Chain(h, p)
    N = float(expected_reads(ch.J, n, covering_time_exact(p) if p <= 17 else 6.4))
    exh, wrong = 0, 0
    for _ in range(40):
        def gen(kk, n=n):
            A = rng.integers(0, p, (kk, n))
            A[:, n - 1] = A[:, 0]
            return A
        st = Stream(p, n, rng, cap=int(20 * N), gen=gen)
        try:
            I, W = solve(ch, 0, n, np.zeros(n, dtype=np.int64), st)
            wrong += not check(ch, st, I, W, n, np.zeros(n, dtype=np.int64), 0)
        except Exhausted:
            exh += 1
    hyp.append({"h": h, "p": p, "n": n, "trials": 40, "exhausted": exh, "wrong": wrong})
    print("hyp", hyp[-1], flush=True)
out["hyperplane"] = hyp

# ---------------------------------------------------------------- scaled J = 1 variant
sc = []
for kappa, p, ns, runs in [(4, 101, [2, 4, 6], 20), (3, 2 ** 31 - 1, [2, 4, 6, 8, 10], 10),
                           (6, 2 ** 61 - 1, [2, 4, 6, 8], 6), (8, 11689, [2, 4, 6, 8], 10),
                           (3, 13, [2, 4, 6], 20), (10, 6151, [2, 4, 6], 10)]:
    assert isprime(p) and (p - 1) % kappa == 0
    h = (p - 1) // kappa
    d1 = None
    if p < 20000:
        d1 = len(chain_sets(h, p)[1])   # |D_0 - D_0|
    for n in ns:
        reads, oks, conv_ok, t_tot = [], True, True, 0.0
        stats = {}
        for rr in range(runs):
            st = BigStream(p, n, seed=1000 * n + rr + p % 997)
            t0 = time.time()
            W = solve_scaled(n, [0] * n, st, h, kappa, random.Random(rr), 10 ** 6, stats)
            t_tot += time.time() - t0
            oks &= check_big(W, st, n, [0] * n, h, p)
            reads.append(st.count)
            # conversion at d = kappa: s_i with s_i^kappa = y_i, check sum s_i^d v_i = 0
            if rr < 2:
                tot = [0] * n
                for i, y in W.items():
                    s_i = nthroot_mod(y, kappa, p)
                    assert pow(s_i, kappa, p) == y
                    for r_ in range(n):
                        tot[r_] = (tot[r_] + pow(s_i, kappa, p) * st.cols[i][r_]) % p
                conv_ok &= not any(tot)
        K = (p - 1).bit_length()
        Nexp = 1 + K * p / (p - 1) * n * (n + 1) / 2
        sc.append({"kappa": kappa, "p": p, "h": h, "n": n, "runs": runs, "weil_ok": weil_ok(kappa, p),
                   "D0minusD0_size": d1, "mean_reads": float(np.mean(reads)), "N_exact": Nexp,
                   "outputs_ok": bool(oks), "conversion_ok": bool(conv_ok),
                   "split_trials": stats.get("split_trials", 0), "split_searches": stats.get("split_searches", 0), "zero_beta": stats.get("zero_beta", 0),
                   "sec_per_run": t_tot / runs,
                   "pairs_lower_bound_over_h": weil_pairs_lower(kappa, p) / h})
        print("scaled", sc[-1], flush=True)
out["scaled"] = sc

with open(sys.argv[1], "w") as f:
    json.dump(out, f, indent=1)
print("first moment consistent", all(x["consistent"] for x in fm),
      "| hyperplane exhausted all", all(x["exhausted"] == x["trials"] and x["wrong"] == 0 for x in hyp),
      "| scaled ok", all(x["outputs_ok"] and x["conversion_ok"] for x in sc))
