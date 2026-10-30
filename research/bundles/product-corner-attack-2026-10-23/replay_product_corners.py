"""Record exact reference-lattice controls; no curve attack is executed."""

import hashlib
import json
from pathlib import Path

from sympy import Matrix, eye, zeros

from product_corners import (complete_by_corners, complete_with_known_map,
                             gaussian_fixture, odd_maximal_order, reference_gram)


def main():
    root, rows = Path(__file__).resolve().parent, []
    for p in (7, 11, 19):
        gram = reference_gram(odd_maximal_order(p))
        for parameters in ((1, 0, 2), (3, 2, 2), (6, 3, 4)):
            order, phi = gaussian_fixture(p, *parameters)
            completed = complete_by_corners(order, phi)
            if completed != eye(16) or (completed.T*gram*completed).det() != p**8:
                raise AssertionError("transverse completion failed")
            rows.append({"characteristic": p, "ell": sum(x*x for x in parameters),
                         "fixture": "transverse_gaussian_matrix_in_full_quaternion_order",
                         "completed_index": int(abs(completed.det())),
                         "gram_determinant": int((completed.T*gram*completed).det()),
                         "fullness_certificate_passed": True})
        order, phi = gaussian_fixture(p)
        gamma = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), -order.unit)
        mixed = complete_with_known_map(order, phi, gamma)
        if mixed != eye(16):
            raise AssertionError("mixing involution completion failed")
        a = Matrix([6, 5, 0, 0])
        split = Matrix.vstack(a, zeros(4, 1), zeros(4, 1), order.star(a))
        deficient = complete_by_corners(order, split)
        if abs(deficient.det()) != 61**16:
            raise AssertionError("deficient-order control changed")
        rows.append({"characteristic": p, "ell": 61,
                     "fixture": "split_dual_kernel_negative_control",
                     "completed_index": int(abs(deficient.det())),
                     "gram_determinant": int((deficient.T*gram*deficient).det()),
                     "fullness_certificate_passed": False,
                     "result": "UNKNOWN_NOT_HARDNESS"})
    files = [root/name for name in ("product_corners.py", "test_product_corners.py",
                                   "replay_product_corners.py", "PRODUCT_CORNER_ATTACK.md", "HANDOFF.md")]
    files.append(root.parent/"kernel-output-2026-10-23"/"kernel_output.py")
    record = {
        "status": "PROPOSED_CLASSICAL_SUBFAMILY_FALSIFIER_REVIEW_PENDING",
        "geometric_input_required": "explicit product projections or a paid integral mixing endomorphism",
        "reference_target_coordinates_used_in_controls": True,
        "geometric_source_executed": False,
        "geometric_ring_extraction_executed": False,
        "general_target_dequantized": False,
        "quantum_speedup_admitted": False,
        "cases": rows,
        "mixing_involution_checks": 3,
        "source_sha256": {str(path.relative_to(root.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in files},
    }
    destination = root/"product_corner_receipt.json"
    destination.write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps({"receipt": str(destination), "positive_lattice_cases": 9,
                      "rejected_deficient_lattices": 3, "mixing_involution_checks": 3,
                      "geometric_ring_extraction_executed": False}, indent=2))


if __name__ == "__main__":
    main()
