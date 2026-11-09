"""Resource counts of the generated circuits across (m, c, p). AI-checked, pending human review.

Run from the repo root:
  PYTHONPATH=. nice -n 10 /opt/anaconda3/bin/python -B research/audits/reviews/2026-11-03-rees-circuit-2/resource_table.py
Writes resource_table.json next to this file. Logical counts are module sums
with multiplicities (all witness entries 1); cx counts transpile each module
separately ({cx, u}, optimization level 1) only where TRANSPILE is set.
"""
import json, os, time
import theorems.rees_circuit_general as G
from theorems.rees_end_to_end_sim import heisenberg, filiform4, filiform5

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = [("Heis(F_3)", heisenberg(3), True), ("Heis(F_5)", heisenberg(5), True), ("Heis(F_7)", heisenberg(7), False),
         ("n4(F_5)", filiform4(5), True), ("n4(F_7)", filiform4(7), False), ("n5(F_5)", filiform5(5), False),
         ("n5(F_7)", filiform5(7), False)]
out = {}
for name, alg, tr in CASES:
    t = time.time()
    cfg = G.Config(alg)
    N = G.sources_per_grade(cfg)
    row = {"m": cfg.m, "c": cfg.c, "p": cfg.p, "dims": cfg.dims, "arity": cfg.arity, "N_d": N,
           "bits_per_coordinate": cfg.enc.nb, "label_bits": cfg.label_bits,
           "A_p_gates_per_add_scaled": G.increment_gate_cost(cfg.p),
           "bch_nodes": {d: [w for w, _, _ in cfg.nodes[d]] for d in cfg.nodes},
           "primitive_counts": G.primitive_formula(cfg),
           "bracket_bound_thm_uniform_compilation_i": G.paper_bracket_bound(cfg),
           "qubits_no_reuse": G.width_formula(cfg),
           "logical_ops_module_sum": G.module_sum_counts(cfg)}
    row["logical_gates_total"] = sum(v for k, v in row["logical_ops_module_sum"].items() if k != "measure")
    macro = {"source": G.macro_counts(G.source_circuit(cfg, None)[1])}
    for d in range(2, cfg.c+1):
        macro[f"merge_d{d}"] = G.macro_counts(G.merge_circuit(cfg, d, 1)[1])
        macro[f"instrument_d{d}"] = G.macro_counts(G.instrument_circuit(cfg, d)[1])
    row["macro_counts_per_module"] = macro
    if tr:
        cx = {"source": G.gate_profile(G.source_circuit(cfg, None)[0])["transpiled_cx_u_excluding_oracle"].get("cx", 0)}
        for d in range(2, cfg.c+1):
            cx[f"instrument_d{d}"] = G.gate_profile(G.instrument_circuit(cfg, d)[0])["transpiled_cx_u_excluding_oracle"].get("cx", 0)
            cx[f"merge_d{d}_s1"] = G.gate_profile(G.merge_circuit(cfg, d, 1)[0])["transpiled_cx_u_excluding_oracle"].get("cx", 0)
            cx[f"q_prep_d{d}"] = G.gate_profile(G.fourier_circuit(cfg, cfg.width[d-1], "x")[0])["transpiled_cx_u_excluding_oracle"].get("cx", 0)
        cx["readout"] = G.gate_profile(G.fourier_circuit(cfg, cfg.m, "x")[0])["transpiled_cx_u_excluding_oracle"].get("cx", 0)
        row["transpiled_cx_per_module"] = cx
        row["transpiled_cx_total_module_sum"] = cx["source"]*N[cfg.c]+cx["readout"]+sum(
            N[d]*(cx[f"instrument_d{d}"]+cx[f"merge_d{d}_s1"])+N[d-1]*cx[f"q_prep_d{d}"] for d in range(2, cfg.c+1))
    row["seconds"] = round(time.time()-t, 1)
    out[name] = row
    print(name, row["qubits_no_reuse"], row["logical_gates_total"], row.get("transpiled_cx_total_module_sum"), row["seconds"], flush=True)
with open(os.path.join(HERE, "resource_table.json"), "w") as fh:
    json.dump(out, fh, indent=1, default=str)
