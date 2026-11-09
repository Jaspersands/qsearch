"""Drift control: rees_circuit_arith.py was modified (2026-11-04 22:15) after
exhaustive_p5_a2.json (13:57). Re-run the CURRENT CoherentSDEK2(5,2,2) gate list
on two index ranges of 2^20 inputs and 16384 structured inputs."""
import json, sys, time
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
import theorems.rees_coherent_sde_k2 as K
t0 = time.time()
circ = K.CoherentSDEK2(5, 2, 2)
gates = circ.flatten()
keys = ("output_equals_canonical", "inputs_restored", "workspace_clean", "witness_nonzero", "equation_holds", "canonical_padding_free")
rows = []
for name, A in (("range_0_2^20", K.input_range(5, 2, 0, 1 << 20)),
                ("range_123456789_+2^20", K.input_range(5, 2, 123456789, 123456789 + (1 << 20))),
                ("structured_16384", K.structured_inputs(5, 2, 16384, seed=20261105))):
    r = K.check_circuit(circ, A, gates)
    rows.append({"set": name, "inputs": r["inputs"], "gates": r["gates"], **{k: r[k] for k in keys}})
print(json.dumps({"rows": rows, "seconds": round(time.time()-t0, 1)}, indent=1))
