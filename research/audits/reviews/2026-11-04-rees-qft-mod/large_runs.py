"""Float check of the full operator error for larger N (31, 49) at small t."""
import json, sys
from theorems.rees_qft_mod import operator_error
out = sys.argv[1]
res = []
for N, t, r, tp in ((31, 7, 7, 28), (31, 9, 4, 28), (49, 8, 8, 28)):
    d = operator_error(N, t, r, tp, tol=1e-11)
    res.append(d)
    print(N, t, r, tp, d["sigma_max"], d["sigma_upper"], d["bound"]["B"], d["prune_err_max"], d["seconds"], flush=True)
    json.dump(res, open(out, "w"), indent=1)
