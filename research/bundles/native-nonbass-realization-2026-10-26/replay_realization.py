"""Replay the wrong-maximal-order control, not an IsERP solver."""

import argparse
import hashlib
import json
from pathlib import Path

from sympy import eye

from native_realization import fixture, opposite_queries, rebase_order
from additive_source import candidate_lattice, input_index, norm
from kernel_output import integer_matrix

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def control(q):
    f = fixture(q)
    d, r, target = f["index"], f["r_basis"], f["target_basis"]
    cases = []
    for name, basis in (("wrong_abstract_center", eye(4)), ("supplied_actual_neighbor", target)):
        generators = integer_matrix(d*r.inv()*basis)
        result = candidate_lattice([generators[:, i] for i in range(4)], d)
        ambient = r*result
        algebra = rebase_order(f["source"], ambient)
        maximal = input_index(algebra, 11) == 1
        integral_norms = all(norm(algebra, eye(4)[:, i]).is_Integer for i in range(4))
        contained = all(x.q == 1 for x in target.inv()*ambient)
        if not maximal or not integral_norms or contained != (name == "supplied_actual_neighbor"):
            raise AssertionError("wrong-order falsifier changed")
        cases.append({"candidate": name, "algebraic_maximality_checks_pass": True,
                      "contained_in_supplied_target_order": contained})
    positive, negative = opposite_queries(f)
    for query in (positive, negative):
        if not query["construction"]["polarization"].integral:
            raise AssertionError("source arithmetic left the supplied suborder")
    return {"prime": q, "input_index": d, "output_controls": cases,
            "source_constructed_in_suborder_coordinates": True,
            "all_ambient_orders_supplied": True}


def receipt():
    paths = [HERE / name for name in (
        "REALIZATION.md", "native_realization.py", "test_realization.py", "replay_realization.py",
    )]
    paths += [ROOT / name for name in (
        "kernel-output-2026-10-23/kernel_output.py",
        "additive-framed-source-2026-10-26/additive_source.py",
        "additive-framed-source-2026-10-26/receipt.json",
        "local-order-scope-2026-10-26/receipt.json",
        "ppav-source-2026-10-23/2026-1142.pdf",
    )]
    return {
        "schema": "native-nonbass-realization-controls-v1",
        "status": "proposed native reduction plus verified supplied-order false positives",
        "controls": [control(q) for q in (3, 5, 17)],
        "execution_scope": {
            "exact_supplied_order_and_suborder_source_arithmetic": True,
            "native_phi_or_dual_construction": False,
            "native_output_division": False,
            "native_geometric_hiding_labels": False,
            "unknown_native_ring_recovery": False,
            "native_hardness_or_quantum_advantage": False,
            "independent_review": False,
        },
        "hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in paths},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = receipt()
    path = HERE / "receipt.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    if args.check and json.loads(path.read_text()) != result:
        raise SystemExit("receipt mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
