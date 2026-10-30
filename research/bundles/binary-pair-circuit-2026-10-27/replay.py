"""Reproduce bounded circuit controls and symbolic resource artifacts."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np

from pair_circuit import expected_pair, input_state, inverse, pair_circuit, precision_budget, resources, simulate
from transfer_control import repetition_transfer
from sampling_bounds import sampling_bound


ROOT = Path(__file__).resolve().parent


def make_receipt():
    controls = []
    for q in (2, 3, 4, 5, 7, 8, 9, 13, 17):
        plan = pair_circuit(q)
        for c in range(q):
            start = input_state(plan, c)
            out = simulate(plan.gates, start)
            error = np.linalg.norm(out - expected_pair(plan, c))
            back_error = np.linalg.norm(simulate(inverse(plan.gates), out) - start)
            if max(error, back_error) >= 1e-12:
                raise ArithmeticError("forward/inverse circuit control failed")
        controls.append({"q": q, "labels_checked": q,
                         "forward_and_inverse_l2_error_below": 1e-12,
                         "padded_data_and_all_work_checked": True})
    transfers = [repetition_transfer(m, s) for m in (2, 3, 4) for s in range(3)]
    for row in transfers:
        for key, value in row.items():
            if isinstance(value, float):
                row[key] = round(value, 12)
    own = ("pair_circuit.py", "transfer_control.py", "sampling_bounds.py", "test_pair_circuit.py", "replay.py", "RESULT.md")
    provenance = ("usd-review-resolution-2026-10-26/RESOLUTION.md",
                  "affine-resampling-audit-2026-10-27/RESULT.md")
    files = [ROOT / x for x in own] + [ROOT.parent / x for x in provenance]
    for relative in ("pair-circuit-review-2026-10-27/REVIEW.md", "usd-novelty-review-2026-10-27/REVIEW.md",
                     "usd-novelty-review-2026-10-27/source_manifest.json"):
        path = ROOT.parent / relative
        if path.is_file():
            files.append(path)
    return {
        "scope": "binary logical construction; bounded simulations; no quantum execution",
        "hashes": {str(p.relative_to(ROOT.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        "pair_controls": controls,
        "actual_binary_inverse_transfer_controls": transfers,
        "symbolic_resources_not_simulations": [resources(pair_circuit(q)) for q in (1019, 65537, 2**127-1, 2**256+1)],
        "example_precision_allocation_not_a_success_certificate": precision_budget(1019, 176, Fraction(9, 10)),
        "example_sampling_bound_not_a_source_certificate": sampling_bound(1-Fraction(1, 10**20), 1+Fraction(1, 10**100), Fraction(1, 10**15), failure_bits=60),
        "whole_decoder_compiled": False,
        "finite_gate_synthesis_performed": False,
        "classical_hardness_or_advantage_established": False,
    }


def json_default(value):
    if isinstance(value, Fraction):
        return str(value)
    raise TypeError(type(value).__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = make_receipt()
    encoded = json.dumps(result, default=json_default, indent=2, sort_keys=True) + "\n"
    path = ROOT / "receipt.json"
    if args.write:
        path.write_text(encoded)
    elif path.read_text() != encoded:
        raise SystemExit("receipt mismatch: inspect changes, do not silently refresh")
    print(json.dumps({"status": "PASS", "mode": "write" if args.write else "check",
                      "pair_labels": sum(row["labels_checked"] for row in result["pair_controls"]),
                      "transfer_cases": len(result["actual_binary_inverse_transfer_controls"]),
                      "receipt_sha256": hashlib.sha256(encoded.encode()).hexdigest()}))
