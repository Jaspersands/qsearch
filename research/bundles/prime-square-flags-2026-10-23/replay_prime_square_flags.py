"""Replay exact flags and lattice pairings; never emit a speedup verdict."""

import hashlib
import json
from pathlib import Path
import sys

from sympy import Matrix, eye, zeros

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent/"smooth-repolarization-2026-10-23"
sys.path.insert(0, str(SOURCE))
from smooth_repolarization import certificate, evaluate
from prime_square_flags import (
    mod, refine, residual_quotient, scalar_torsion_extension,
    stable_under, symplectic_form,
)


def main():
    h = ((1, 0, 1, -2), (0, 1, 2, 1), (1, 2, 6, 0), (-2, 1, 0, 6))
    f = Matrix(evaluate(certificate(7, 30)["E"], h))
    cases = []
    for r in (2, 3, 5):
        flag = refine(f, r)
        quotient = residual_quotient(flag)
        q, j1, residual = (quotient[key] for key in
                           ("quotient_matrix", "pairing", "residual_kernel"))
        checks = {
            "first_quotient_multiplier": q.T*j1*q == r*symplectic_form(16),
            "quotient_pairing_unimodular": abs(int(j1.det())) == 1,
            "residual_kernel_dimension": residual.cols == 16,
            "residual_kernel_isotropic": mod(residual.T*j1*residual, r) == zeros(16),
            "scalar_frobenius_preserves_first_kernel": stable_under(flag.first_kernel, -103*eye(32), r),
        }
        if not all(checks.values()):
            raise AssertionError(checks)
        row = flag.receipt()
        row.update({"checks": checks,
                    "scalar_frobenius_control": -103,
                    "scalar_torsion_extension_degree": scalar_torsion_extension(-103, r),
                    "geometric_field_contract_verified": False})
        cases.append(row)
    frobenius = Matrix([[0, -1], [1, 0]])
    lines = [Matrix([1, a]) for a in range(3)]+[Matrix([0, 1])]
    negative = {
        "rG_shortcut_is_not_lagrangian_for_X_r": refine(3*eye(2), 3).multiplied_kernel.cols == 0,
        "nonscalar_local_control_has_no_stable_line": all(not stable_under(line, frobenius, 3) for line in lines),
    }
    if not all(negative.values()):
        raise AssertionError(negative)
    sources = [ROOT/name for name in (
        "prime_square_flags.py", "test_prime_square_flags.py",
        "replay_prime_square_flags.py", "PRIME_SQUARE_FLAGS.md", "HANDOFF.md")]
    sources.append(SOURCE/"smooth_repolarization.py")
    receipt = {
        "status": "CONDITIONAL_SOURCE_REFINEMENT_INDEPENDENT_REVIEW_PENDING",
        "schema": "isolated-exact-algebra-receipt-v1",
        "geometric_quotients_executed": False,
        "kernel_recovery_executed": False,
        "quantum_algorithm_executed": False,
        "speedup_admitted": False,
        "cases": cases,
        "negative_controls": negative,
        "source_sha256": {str(path.relative_to(ROOT.parent)):
                          hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
    }
    destination = ROOT/"prime_square_flags_receipt.json"
    destination.write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({"receipt": str(destination), "cases": len(cases),
                      "negative_controls": len(negative), "all_passed": True,
                      "speedup_admitted": False}, indent=2))


if __name__ == "__main__":
    main()
