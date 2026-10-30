"""Replay exact module/descent controls, not the geometric converter."""

import hashlib
import json
from pathlib import Path

from sympy import Matrix

from effective_output import (left_order_actions, pullback_matrix,
                              scalar_base_change, source_inclusion)
from kernel_output import matrix_multiply, odd_maximal_order, odd_maximal_split, reconstruct
from twist_control import twist_control


def main():
    root, rows = Path(__file__).resolve().parent, []
    for p, ell in ((7, 3), (11, 5), (19, 7)):
        order = odd_maximal_order(p)
        output = reconstruct(order, odd_maximal_split(p, ell),
                             Matrix([[1, 0], [1, 2], [0, 1], [2, 3]]), ell)
        basis, actions = output.order_basis, left_order_actions(order, output)
        maps = [pullback_matrix(order, output, basis[:, i]) for i in range(basis.cols)]
        pairs = ((0, 1), (1, 2), (3, 7), (4, 12), (5, 10))
        checks = {
            "full_left_action_commutes": all(t*a == a*t for t in maps for a in actions),
            "opposite_multiplication": all(
                pullback_matrix(order, output, matrix_multiply(order, basis[:, i], basis[:, j]))
                == maps[j]*maps[i] for i, j in pairs),
            "noncommutativity_witness": any(maps[i]*maps[j] != maps[j]*maps[i] for i, j in pairs),
            "source_inclusion_index": abs(int(source_inclusion(order, output).det())) == ell**4,
        }
        if not all(checks.values()):
            raise AssertionError(checks)
        rows.append({"curve_characteristic": p, "kernel_prime": ell,
                     "checks": checks, "twist_control": twist_control(p),
                     "positive_scalar_normalization": scalar_base_change(p, 2, p),
                     "negative_scalar_normalization": scalar_base_change(p, 2, -p)})
    files = [root/name for name in ("effective_output.py", "twist_control.py",
                                   "test_effective_output.py", "replay_effective_output.py",
                                   "EFFECTIVE_OUTPUT_AUDIT.md", "HANDOFF.md")]
    files.extend((root.parent/"kernel-output-2026-10-23"/"kernel_output.py",
                  root.parent/"smooth-repolarization-2026-10-23"/"page-robert-soumier-2026-276.pdf"))
    record = {
        "status": "CONDITIONAL_OUTPUT_COMPOSITION_REVIEW_PENDING",
        "secret_kernel_supplied_to_postprocessor": True,
        "geometric_converter_executed": False,
        "source_oracle_executed": False,
        "quantum_receiver_executed": False,
        "speedup_admitted": False,
        "cases": rows,
        "source_sha256": {str(path.relative_to(root.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in files},
    }
    destination = root/"effective_output_receipt.json"
    destination.write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps({"receipt": str(destination), "cases": len(rows),
                      "all_exact_controls_passed": True,
                      "geometric_converter_executed": False}, indent=2))


if __name__ == "__main__":
    main()
