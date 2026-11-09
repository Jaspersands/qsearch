"""Trace check (kappa_trace_check.trace_check, T1-T6 + L4) at kappa = 5 and kappa = 6,
at the first primes outside E_2(5) (p = 191) and E_2(6) (p = 229) found by the module's
own refusal test. Sampled (structured + degenerate inputs). Report Section 2.6.
AI-written, pending human review."""
import json, sys, time
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import numpy as np
from kappa_trace_check import trace_check, degenerate_inputs
from theorems.rees_coherent_sde_k2 import structured_inputs
from theorems.rees_coherent_sde_kappa import CoherentSDEKappa

out = sys.argv[1]
rng = np.random.default_rng(56)
rows = []
for (p, a, d, n) in [(191, 1, 5, 2000), (229, 1, 6, 2000), (191, 2, 5, 200), (229, 2, 6, 200)]:
    refused = []
    for q in range(7, p):
        if all(q % t for t in range(2, int(q**0.5)+1)) and q % d == 1:
            try:
                CoherentSDEKappa(q, 1, d)
                refused.append((q, False))
            except ValueError:
                refused.append((q, True))
    A = np.concatenate([structured_inputs(p, a, n, seed=p+a), degenerate_inputs(p, a, rng, n_rand=4 if a == 2 else 8)])
    r = trace_check(p, a, d, A, label=f"kappa{d} first p outside E_2({d})")
    r["smaller_primes_1_mod_d_all_refused"] = all(x for _, x in refused)
    rows.append(r)
    print(json.dumps({k: r.get(k) for k in ("label", "p", "a", "d", "kappa", "inputs", "all_pass", "K_hist",
                                            "seconds", "smaller_primes_1_mod_d_all_refused")}), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1, default=str)
