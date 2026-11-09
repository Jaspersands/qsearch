"""Target parameters from the statement of lem:qft-mod only: general call <= eta,
zero-input call <= 3 pi 2^-tau <= eta/(b+3); n * delta <= 0.1. Writes lemma_level.json.
AI-checked, pending human review."""
import json, math, os, sys
sys.path.insert(0, os.getcwd())
import theorems.rees_circuit_general as G
import theorems.rees_circuit_qft_wire as W
import theorems.rees_qft_mod as Q
from theorems.rees_end_to_end_sim import filiform4, heisenberg
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for name, alg, n in (("heis_f3", heisenberg(3), 7), ("n4_f5", filiform4(5), 8)):
    cfg = G.Config(alg)
    b = cfg.enc.nb
    calls = W.qft_call_inputs(*W.terminal_sample_circuit(cfg))
    nz = sum(1 for c in calls if c[2]); ng = len(calls)-nz
    eta = 0.1/(n*(nz/(b+3)+ng))
    t, r, tp = Q.params_for_eta(cfg.p, eta)
    r = min(r, t)
    delta_lemma = nz*3*math.pi/2**tp+ng*eta
    bd = Q.error_bound(cfg.p, t, r, tp)
    assert bd["B_simple"] <= eta and 3*math.pi/2**tp <= eta/(b+3)
    c = W.terminal_counts(cfg, "explicit", params=(t, r, tp))
    out[name] = {"n_samples": n, "zero_calls": nz, "general_calls": ng, "eta": eta, "params": (t, r, tp),
                 "delta_lemma_level": delta_lemma, "run_failure_lemma_level": n*delta_lemma,
                 "delta_exact_formula": W.hybrid_budget(calls, cfg.p, t, r, tp)["proved_total"], "counts": c}
    print(name, json.dumps(out[name], default=float))
json.dump(out, open(os.path.join(HERE, "lemma_level.json"), "w"), indent=1, default=float)
