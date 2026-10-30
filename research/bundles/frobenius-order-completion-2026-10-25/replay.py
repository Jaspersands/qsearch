"""Deterministic exact receipts; no geometric weak isogeny is supplied here."""

from collections import Counter
import hashlib
import json
from pathlib import Path

from sympy import Matrix, diag, eye, zeros

from completion import (curve_control, integral_completion, lagrangians,
                        local_completion, recover_frobenius_polynomial,
                        spectral_gate, weak_completion_actions)
from product_corners import (gaussian_fixture, matrix_multiply, matrix_star,
                             mod, reference_gram)
from kernel_output import odd_maximal_split, product_actions


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    parent = root.parent
    frozen_path = parent/"product-corner-attack-2026-10-23"/"product_corner_receipt.json"
    frozen = json.loads(frozen_path.read_text())
    for relative, expected in frozen["source_sha256"].items():
        if digest(parent/relative) != expected:
            raise AssertionError(f"frozen predecessor changed: {relative}")

    local_gamma = diag(Matrix([[0, 1], [1, 2]]), Matrix([[0, 1], [1, 1]]))
    census = [(plane, local_completion(plane, local_gamma, 3)) for plane in lagrangians(3)]
    profiles = Counter(tuple(result["cyclic_space_ranks"]) for _, result in census)
    if profiles != {(2, 4, 4): 24, (2, 3, 4): 16}:
        raise AssertionError("all-Lagrangian profile changed")
    for _, result in census:
        if result["literal_matrix_span_ranks"] != [r*r for r in result["cyclic_space_ranks"]]:
            raise AssertionError("tensor-span identity failed")
    strict_plane, strict_result = next((plane, result) for plane, result in census
                                     if result["cyclic_space_ranks"][1] == 3)

    native_curve = curve_control()
    polynomial = native_curve["characteristic_polynomial"]
    curve_gates = [spectral_gate(polynomial, 5, ell) for ell in (3, 31, 43, 47, 2**127-1)]
    if [row["all_lagrangians_cyclic_sufficient"] for row in curve_gates] != [True]*3+[False]*2:
        raise AssertionError("fixed-input spectral controls changed")

    integer_gamma = Matrix([[0, 0, 0, -5], [0, 0, 1, 0], [1, 0, 0, 0], [0, 5, 0, 0]])
    acquired = recover_frobenius_polynomial(5, [(r, integer_gamma) for r in (7, 11)])
    if acquired["coefficients"] != polynomial:
        raise AssertionError("auxiliary CRT and actual point counts disagree")

    completed_orders = []
    for p, parameters in ((7, (3, 1, 1)), (11, (3, 3, 1))):
        order, phi = gaussian_fixture(p, *parameters)
        gamma = Matrix.vstack(Matrix([3, 2, 0, 0]), zeros(4, 1), zeros(4, 1), Matrix([2, 3, 0, 0]))
        unit = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
        if matrix_multiply(order, matrix_star(order, gamma), gamma) != 13*unit:
            raise AssertionError("integral polarized-map identity failed")
        completed = integral_completion(order, phi, gamma)
        scalar = integral_completion(order, phi, unit)
        ell = sum(x*x for x in parameters)
        determinant = int((completed.T*reference_gram(order)*completed).det())
        if completed != eye(16) or determinant != p**8 or abs(scalar.det()) != ell**16:
            raise AssertionError("integral lattice/fullness control failed")
        completed_orders.append({"characteristic": p, "ell": ell, "map_multiplier": 13,
                                 "completed_index": 1, "gram_determinant": determinant,
                                 "scalar_completion_index": int(abs(scalar.det())),
                                 "reference_coordinates_used": True,
                                 "map_is_geometric_frobenius": False})

    order, phi = gaussian_fixture(7, 3, 1, 1)
    gamma = Matrix.vstack(Matrix([3, 2, 0, 0]), zeros(4, 1), zeros(4, 1), Matrix([2, 3, 0, 0]))
    actions = product_actions(odd_maximal_split(7, 17))
    evaluate = lambda vector: mod(sum((vector[i]*actions[i] for i in range(16)), zeros(4)), 17)
    w, gamma_action = evaluate(phi), evaluate(gamma)
    weak = weak_completion_actions(actions, w, gamma_action, 11, 17, 13)
    masked = weak_completion_actions(actions, 7*w, gamma_action, 11, 17, 13)
    independent = weak_completion_actions(actions, w*diag(1, 2, 3, 4), gamma_action, 11, 17, 13)
    if weak != masked or weak == independent:
        raise AssertionError("weak-mask contract control failed")
    unit = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    powers = [unit, gamma, matrix_multiply(order, gamma, gamma)]
    direct = []
    for a in range(16):
        transported = matrix_multiply(order, matrix_multiply(order, phi, eye(16)[:, a]), matrix_star(order, phi))
        for left in powers:
            for right in powers:
                direct.append(evaluate(matrix_multiply(order, matrix_multiply(order, left, transported),
                                                      matrix_star(order, right))))
    if tuple(direct) != weak or len(weak) != 144:
        raise AssertionError("auxiliary maps disagree with genuine integral controls")

    c = Matrix([[0, 2], [1, 0]])
    repeated = local_completion(eye(2).col_join(eye(2)+c), diag(c, c), 3)
    a = Matrix([[0, 6], [1, 0]])
    permutation = eye(4)[:, [0, 2, 1, 3]]
    paired_gamma = permutation.T*diag(a, mod(5*a.inv_mod(7).T, 7))*permutation
    paired = local_completion(eye(4)[:, [0, 2]], paired_gamma, 7)
    scalar = local_completion(eye(4)[:, [0, 2]], integer_gamma**4, 3)
    a = Matrix([[0, 2], [1, 0]])
    self_adjoint_gamma = permutation.T*diag(a, a.T)*permutation
    self_adjoint = local_completion(eye(4)[:, [0, 2]], self_adjoint_gamma, 3)
    if any(result["full_after_two_powers"] for result in (repeated, paired, scalar, self_adjoint)):
        raise AssertionError("a negative invariant-plane control was promoted")

    source_names = ("completion.py", "test_completion.py", "replay.py",
                    "FROBENIUS_COMPLETION.md", "HANDOFF.md")
    dependency_names = ("product-corner-attack-2026-10-23/product_corners.py",
                        "product-corner-attack-2026-10-23/PRODUCT_CORNER_ATTACK.md",
                        "product-corner-attack-2026-10-23/product_corner_receipt.json",
                        "kernel-output-2026-10-23/kernel_output.py",
                        "kernel-output-2026-10-23/KERNEL_TO_OUTPUT.md")
    record = {
        "status": "PROPOSED_CONDITIONAL_CLASSICAL_ATTACK_REVIEW_PENDING",
        "supplied_weak_isogeny_constructed": False,
        "geometric_endomorphism_lattice_extracted": False,
        "native_kernel_recovered": False,
        "general_source_dequantized": False,
        "quantum_speedup_admitted": False,
        "geometry_and_field_costs_are_promises_not_matrix_certificates": True,
        "curve_control": native_curve,
        "curve_spectral_gates": curve_gates,
        "public_auxiliary_polynomial_reconstruction": acquired,
        "insufficient_auxiliary_CRT": recover_frobenius_polynomial(5, [(7, integer_gamma)]),
        "local_census": {
            "ell": 3, "total_lagrangians": len(census), "two_power_successes": 40,
            "one_power_failures": 16,
            "profiles": [{"cyclic_space_ranks": list(key), "count": count}
                         for key, count in sorted(profiles.items())],
            "strict_extension_plane": [[int(x) for x in row] for row in strict_plane.tolist()],
            "strict_extension_result": strict_result,
            "geometric_source_distribution": "NOT_ESTABLISHED"},
        "integral_order_controls": completed_orders,
        "public_weak_actions": {"auxiliary_prime": 17, "ell": 11, "actions_checked": len(weak),
                                "common_mask_invariant": True, "independent_masks_change_actions": True,
                                "reference_maps_match": True, "curve_points_used": False},
        "negative_local_controls": {"repeated_factor": repeated, "distinct_reciprocal_pair": paired,
                                    "extension_field_scalar_frobenius": scalar,
                                    "self_adjoint_quadratic_map": self_adjoint},
        "large_prime_non_frobenius_integral_control": spectral_gate([169, -130, 50, -10, 1], 13, 2**127-1),
        "source_sha256": {name: digest(root/name) for name in source_names},
        "dependency_sha256": {name: digest(parent/name) for name in dependency_names},
        "frozen_predecessor_source_hashes_checked": len(frozen["source_sha256"]),
    }
    destination = root/"receipt.json"
    destination.write_text(json.dumps(record, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"receipt": str(destination), "sha256": digest(destination),
                      "local_planes": len(census), "strict_extensions": 16,
                      "integral_order_controls": len(completed_orders),
                      "geometric_attack_executed": False}, indent=2))


if __name__ == "__main__":
    main()
