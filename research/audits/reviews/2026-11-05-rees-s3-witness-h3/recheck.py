"""Re-run the one solver row with |z| > 3 (h=3, p=19, n=11) with a fresh seed and more runs."""
import json, math, sys
import numpy as np
from wh_lib import Chain, Stream, solve, check, covering_time_mc, expected_reads
h, p, n, runs = 3, 19, 11, int(sys.argv[2])
ch = Chain(h, p)
s, se_s = covering_time_mc(p, 400000, seed=99)
N = expected_reads(ch.J, n, s)
rng = np.random.default_rng(424242)
reads, ok = [], True
for _ in range(runs):
    st = Stream(p, n, rng)
    I, W = solve(ch, 0, n, np.zeros(n, dtype=np.int64), st)
    ok &= check(ch, st, I, W, n, np.zeros(n, dtype=np.int64), 0)
    reads.append(st.count)
m, se = float(np.mean(reads)), float(np.std(reads, ddof=1) / math.sqrt(runs))
res = {"h": h, "p": p, "n": n, "runs": runs, "s_p_mc": s, "s_p_se": se_s, "N0": N, "mean": m, "se": se,
       "z": (m - N) / se, "all_ok": bool(ok)}
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(res)
