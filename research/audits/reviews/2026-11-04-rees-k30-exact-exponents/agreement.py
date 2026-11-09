"""K30: exact vs float instrument exponents, entry by entry, on every grade.
Run from the repo root: PYTHONPATH=. python -B research/audits/reviews/2026-11-04-rees-k30-exact-exponents/agreement.py OUT.json"""
import json
import sys
import time

import theorems.rees_circuit_general as G
from theorems.rees_circuit_arith import arith_backend, reduced_instrument_circuit
from theorems.rees_end_to_end_sim import filiform4, filiform5, heisenberg


out, t0 = {"rows": []}, time.time()
for backend in ("original", "arith"):
    for name, alg in (("heis_f3", heisenberg(3)), ("n4_f5", filiform4(5)), ("n4_f7", filiform4(7)),
                      ("n5_f5", filiform5(5)), ("n5_f7", filiform5(7))):
        ts = time.time()
        if backend == "arith":
            with arith_backend():                 # as instrument_semantics_arith does
                saved, G.instrument_circuit = G.instrument_circuit, reduced_instrument_circuit
                try:
                    cfg = G.Config(alg)
                    r = G.instrument_exponent_agreement(cfg)
                finally:
                    G.instrument_circuit = saved
        else:
            cfg = G.Config(alg)
            r = G.instrument_exponent_agreement(cfg)
        r.update(backend=backend, job=name, seconds=round(time.time()-ts, 2),
                 max_float_round_err=max(g["float_info"]["round_err"] for g in r["grades"].values()))
        out["rows"].append(r)
        print(backend, name, "gates", {d: g["gates"] for d, g in r["grades"].items()}, "entries", r["entries"],
              "mismatches", r["mismatches"], "max float round err", r["max_float_round_err"], r["seconds"], "s",
              flush=True)
out["total_entries"] = sum(r["entries"] for r in out["rows"])
out["total_mismatches"] = sum(r["mismatches"] for r in out["rows"])
out["seconds"] = round(time.time()-t0, 1)
print("total entries", out["total_entries"], "mismatches", out["total_mismatches"])
with open(sys.argv[1], "w") as fh:
    fh.write(json.dumps(out, indent=1, default=str)+"\n")
