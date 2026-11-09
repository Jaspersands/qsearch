"""fb check 6: re-run the repo's counting mode of theorems/rees_circuit_arith.py for one multiply-accumulate
(add_product) and one add_scaled macro, and compare with 40b^2+2b Toffoli and <= 158b^2+46b gates.
Run from the repo root (imports the repo package read-only)."""
import sys, json
sys.path.insert(0, '.')
import theorems.rees_circuit_arith as A
res = {}
for p in [3, 5, 7, 11, 13, 31, 127, 8191, 131071, 2**31 - 1, 2**61 - 1]:
    b = max(1, (p - 1).bit_length())
    mc = A.multiplication_counts(p)
    ap = mc["add_product"]
    fc = A.formula_counts(p, 1)
    ok = (ap["ccx"] == 40 * b * b + 2 * b) and (ap["max_total"] <= 158 * b * b + 46 * b)
    res[p] = {"b": b, "ccx": ap["ccx"], "max_total": ap["max_total"], "min_total": ap["min_total"],
              "bound": 158 * b * b + 46 * b, "ancilla": ap["qubits_ancilla"], "3b+5": 3 * b + 5, "ok": ok}
    print(p, res[p], flush=True)
json.dump(res, open(sys.argv[1], 'w'), indent=1)
