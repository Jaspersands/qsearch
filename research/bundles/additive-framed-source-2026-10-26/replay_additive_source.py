"""Reproduce exact source-identity controls, not a native geometric label."""

import argparse
import hashlib
import json
from pathlib import Path

from sympy import Matrix, Rational, eye, zeros

from additive_source import (
    adjoint, block_isometry, candidate_lattice, construct, fixes_inclusions,
    multiply, norm, scalar_matrix, shear, uniform_plan,
)
from kernel_output import odd_maximal_order

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def control(p, n, roots, beta, delta):
    order = odd_maximal_order(p)
    beta, delta = Matrix(beta), Matrix(delta)
    current = construct(order, beta, n, roots)
    other = construct(order, beta+n*delta, n, roots)
    z, w, identity = current["polarization"], shear(order, delta), scalar_matrix(order, eye(16))
    checks = {
        "hermitian": adjoint(order, z) == z,
        "integral": z.integral,
        "quadratic_identity": multiply(order, z, z)-z.scale(current["trace"])+identity == scalar_matrix(order, zeros(16)),
        "integral_inverse": multiply(order, z, identity.scale(current["trace"])-z) == identity,
        "integral_translation": w.integral and fixes_inclusions(order, w),
        "translation_congruence": multiply(order, multiply(order, adjoint(order, w), z), w) == other["polarization"],
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {
        "characteristic": p, "denominator": n, "roots": list(roots),
        "beta_coordinates": list(map(int, beta)), "delta_coordinates": list(map(int, delta)),
        "beta_norm": current["degree"], "trace": current["trace"],
        "beta_delta_noncommuting": order.multiply(beta, delta) != order.multiply(delta, beta),
        "checks": checks,
    }


def negative_controls():
    order = odd_maximal_order(11)
    plus = construct(order, order.unit, 3, (8, 4, 0, 0))["polarization"]
    minus = construct(order, -order.unit, 3, (8, 4, 0, 0))["polarization"]
    collisions = []
    for signs in [(-1, 1), (1, -1)]:
        small = scalar_matrix(order, Matrix.diag(*signs))
        w = block_isometry(order, small, small)
        congruence = multiply(order, multiply(order, adjoint(order, w), plus), w)
        if congruence != minus or fixes_inclusions(order, w):
            raise AssertionError("omitted-inclusion collision control")
        collisions.append({"signs": signs, "polarization_collision": True,
                           "passes_complete_frame": False})
    wrong = Matrix.diag(1, 3, 3, 3)*candidate_lattice([eye(4)[:, 0]], 27)
    if wrong[0, 0] != Rational(1, 27) or norm(order, wrong[:, 0]) != Rational(1, 729):
        raise AssertionError("index-only false positive control")
    return {
        "omitted_inclusion_collisions": collisions,
        "index_only_false_positive": {
            "input_index": 27, "candidate_index_check_passes": True,
            "nonintegral_scalar": "1/27", "nonintegral_norm": "1/729",
            "native_division_executed": False,
        },
    }


def receipt():
    paths = [
        HERE / "additive_source.py", HERE / "ADDITIVE_SOURCE.md", HERE / "SELF_AUDIT.md",
        HERE / "test_additive_source.py", HERE / "replay_additive_source.py", HERE / "COMPARISON.md",
        ROOT / "smooth-repolarization-2026-10-23/smooth_repolarization.py",
        ROOT / "prime-square-flags-2026-10-23/PRIME_SQUARE_FLAGS.md",
        ROOT / "source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md",
        ROOT / "ppav-source-2026-10-23/2026-1142.pdf",
        ROOT / "large-prime-source-audit-2026-10-25/chen-petit-accepted.pdf",
    ]
    return {
        "schema": "additive-framed-source-algebra-controls-v1",
        "status": "unreviewed proposed reduction with exact algebra controls",
        "controls": [
            control(11, 3, (8, 4, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)),
            control(19, 5, (24, 4, 4, 4), (2, -1, 3, -2), (1, 1, 0, 1)),
        ],
        "negative_controls": negative_controls(),
        "uniform_cost_example": uniform_plan(27, 25),
        "hashes": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in paths},
        "execution_scope": {
            "exact_quaternion_matrix_controls_executed": True,
            "provenance": "known arithmetic orders supplied as controls; no unknown native ring recovered",
            "native_geometric_label_executed": False,
            "native_output_integrality_verifier_executed": False,
            "coherent_source_executed": False,
            "quantum_receiver_executed": False,
            "independent_review_of_additive_proposal": False,
            "native_classical_hardness_established": False,
            "novelty_established": False,
            "speedup_established": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = receipt()
    encoded = json.dumps(result, sort_keys=True, indent=2)+"\n"
    path = HERE / "receipt.json"
    if args.write:
        path.write_text(encoded)
    if args.check and json.loads(path.read_text()) != json.loads(encoded):
        raise SystemExit("receipt mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
