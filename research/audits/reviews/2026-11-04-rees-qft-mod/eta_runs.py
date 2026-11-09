"""Float check: full operator error at the Corollary 8 parameters (B <= eta proved)."""
import json, sys
from theorems.rees_qft_mod import params_for_eta, operator_error
out = sys.argv[1]
res = []
for N, eta in ((3, 0.25), (3, 0.1), (5, 0.25), (5, 0.1), (7, 0.25), (9, 0.25), (11, 0.25), (13, 0.25), (3, 0.05)):
    t, r, tp = params_for_eta(N, eta)
    d = operator_error(N, t, r, tp, tol=1e-11)
    d["eta"] = eta
    res.append(d)
    print(N, eta, t, r, tp, d["sigma_max"], d["sigma_upper"], d["bound"]["B"], d["bound"]["B_simple"], d["seconds"], flush=True)
    json.dump(res, open(out, "w"), indent=1)
