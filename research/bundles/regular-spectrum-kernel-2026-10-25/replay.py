"""Exact arithmetic receipts, explicitly not an executed geometric attack."""

import hashlib
import json
from pathlib import Path
import random

from sympy import Matrix, eye

from regular_kernel import from_source_pullback, regular_candidates, select_original
from regular_controls import POLYNOMIAL, acquire_polynomial, arithmetic_source, previous_unknown_control
from pullback import reconstruct_pullbacks
from residual import nullspace, same_space
from residual_controls import OpaqueLabels
from kernel_output import (action, integral_matrix_test, matrix_on_column,
                           product_actions, reconstruct)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_manifest(base, manifest):
    for relative, expected in manifest.items():
        if digest(base/relative) != expected:
            raise AssertionError(f"frozen dependency changed: {relative}")
    return len(manifest)


def main():
    root = Path(__file__).resolve().parent
    parent = root.parent
    completion_path = parent/"frobenius-order-completion-2026-10-25"/"receipt.json"
    completion = json.loads(completion_path.read_text())
    frozen = {
        "completion_source": checked_manifest(completion_path.parent, completion["source_sha256"]),
        "completion_dependencies": checked_manifest(parent, completion["dependency_sha256"]),
    }
    residual_path = parent/"source-residual-algebra-2026-10-24"/"receipt.json"
    frozen["residual_sources_and_dependencies"] = checked_manifest(
        parent, json.loads(residual_path.read_text())["sha256"])
    product_path = parent/"product-corner-attack-2026-10-23"/"product_corner_receipt.json"
    frozen["product_corner_sources"] = checked_manifest(
        parent, json.loads(product_path.read_text())["source_sha256"])

    arithmetic = []
    for rank in (0, 1, 2):
        source = arithmetic_source(rank)
        public = acquire_polynomial(source)
        if tuple(public["coefficients"]) != POLYNOMIAL:
            raise AssertionError("auxiliary characteristic polynomial changed")
        got = reconstruct_pullbacks(source.order, source.ell, source.characteristic,
                                   source.norms(), source.levels(), source.split, source.observe,
                                   max_auxiliary_prime=47)
        if got.coordinates != source.reference_pullbacks():
            raise AssertionError("exact source CRT reconstruction failed")
        result = from_source_pullback(source.order, got.coordinates[0], public["coefficients"],
                                      source.ell, source.split(source.ell), rng=random.Random(25))
        truth = nullspace(action(source.phi, product_actions(source.split(source.ell))), source.ell)
        labels = OpaqueLabels(truth, source.ell)
        chosen = select_original(result.candidates, source.ell, labels)
        left = Matrix.hstack(*(matrix_on_column(source.order, got.coordinates[0], eye(8)[:, j])
                               for j in range(8)))
        for kernel in result.candidates:
            module = reconstruct(source.order, source.split(source.ell), kernel, source.ell).module_numerator
            if not integral_matrix_test(module.inv()*left*module/source.ell):
                raise AssertionError("independent Hom-module integrality check failed")
        if (result.image_ranks != (rank, rank) or len(result.candidates) != (4, 2, 1)[rank]
                or not same_space(chosen["kernel"], truth, source.ell)
                or chosen["original_source_calls"] != (9, 5, 0)[rank]):
            raise AssertionError("fixed arithmetic branch changed")
        arithmetic.append({
            "characteristic": source.characteristic, "ell": source.ell,
            "public_polynomial_acquisition": public,
            "pullback_auxiliary_primes": list(got.primes),
            "pullback_modulus": int(got.modulus),
            "word_image_ranks": list(result.image_ranks), "status": result.status,
            "candidate_count": len(result.candidates),
            "residual_polynomial": list(result.residual_polynomial),
            "root_abort_bound": result.root_abort_bound,
            "exact_source_products_checked": result.exact_source_products_checked,
            "independent_hom_integrality_checks": len(result.candidates),
            "original_source_interface_calls": chosen["original_source_calls"],
            "selected_reference_kernel": True, "label_backend": "FINITE_OPAQUE_CONTROL_ONLY",
            "target_map_is_geometric_frobenius": False,
            "geometric_input_verified": result.geometric_input_verified,
            "global_source_fibers_verified": chosen["source_fibers_verified"],
        })

    previous_unknown = []
    for ell in (47, 2**127-1):
        alpha, truth, old = previous_unknown_control(ell)
        result = regular_candidates(alpha, [25, 0, 0, 0, 1], ell, rng=random.Random(25))
        selected = select_original(result.candidates, ell, OpaqueLabels(truth, ell))
        if (old["status"] != "UNKNOWN" or len(result.candidates) != 2
                or selected["original_source_calls"] != 5
                or not same_space(truth, selected["kernel"], ell)):
            raise AssertionError("unchanged-prime extension failed")
        previous_unknown.append({"ell": ell, "prior_gate": old["status"],
                                 "new_gate": result.status, "candidate_count": 2,
                                 "original_source_interface_calls": 5,
                                 "selected_reference_kernel": True,
                                 "control_scope": "LOCAL_LATTICE_NOT_INCOMING_ISOGENY"})

    repeated = regular_candidates(7*eye(4), [1, -4, 6, -4, 1], 7)
    common_field = regular_candidates(47*eye(4), [25, 0, 10, 0, 1], 47)
    if any(r.status != "NOT_REGULAR_USE_EXISTING_GENERAL_GATES" for r in (repeated, common_field)):
        raise AssertionError("repeated spectrum was promoted")
    sources = ("regular_kernel.py", "regular_controls.py", "test_regular_kernel.py",
               "replay.py", "REGULAR_SPECTRUM.md", "HANDOFF.md")
    dependencies = {str(completion_path.relative_to(parent)), str(residual_path.relative_to(parent)),
                    str(product_path.relative_to(parent))}
    dependencies.update(str(completion_path.parent.relative_to(parent)/name)
                        for name in completion["source_sha256"])
    dependencies.update(completion["dependency_sha256"])
    dependencies.update(json.loads(residual_path.read_text())["sha256"])
    record = {
        "status": "PROPOSED_CONDITIONAL_CLASSICAL_ATTACK_REVIEW_PENDING",
        "candidate_bound": 6, "classical_original_source_call_bound": 13,
        "original_source_implementation_is_still_required_for_nonunique_lists": True,
        "geometric_attack_executed": False, "general_weak_isogeny_solver": False,
        "quantum_speedup_admitted": False, "independent_review_completed": False,
        "arithmetic_controls": arithmetic, "unchanged_previous_unknown_controls": previous_unknown,
        "negative_controls": {"repeated_spectrum": repeated.status,
                              "common_field_product_frobenius": common_field.status},
        "frozen_predecessor_hashes_checked": frozen,
        "source_sha256": {name: digest(root/name) for name in sources},
        "dependency_sha256": {name: digest(parent/name) for name in sorted(dependencies)},
    }
    destination = root/"receipt.json"
    destination.write_text(json.dumps(record, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"receipt": str(destination), "sha256": digest(destination),
                      "arithmetic_candidate_counts": [row["candidate_count"] for row in arithmetic],
                      "previous_unknown_counts": [2, 2], "geometric_attack_executed": False}, indent=2))


if __name__ == "__main__":
    main()
