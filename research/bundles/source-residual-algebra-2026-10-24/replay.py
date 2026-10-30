"""Recorded arithmetic replay; no target geometry or quantum oracle is run."""

import argparse
import hashlib
import json
from pathlib import Path
import random

from sympy import Matrix, eye

from residual_algebra import analyze_rank_one, analyze_source_pullbacks
from algebra_controls import local_action, quartic_fixture
from pullback import column_basis, extract_kernel, reconstruct_pullbacks
from residual import nullspace, same_space, select_with_original_hiding_function
from residual_controls import OpaqueLabels, lagrangians, space_key
from controls import unit
from kernel_output import (
    action, integral_matrix_test, matrix_multiply,
    matrix_on_column, product_actions, reconstruct,
)


def matrix_rows(matrix):
    return [[int(x) for x in matrix.row(i)] for i in range(matrix.rows)]


def run():
    records = []
    for kind, expected in (("two", 2), ("one", 1), ("scalar", 12)):
        source = quartic_fixture(kind)
        recovered = reconstruct_pullbacks(
            source.order, 11, 7, source.norms(), source.levels(), source.split,
            source.observe, max_auxiliary_prime=47)
        assert recovered.coordinates == source.reference_pullbacks()
        old = extract_kernel(source.order, 11, source.split(11), recovered.coordinates)
        assert old.rank_history == (1, 1)
        output = analyze_source_pullbacks(source.order, recovered.coordinates, 11,
                                          source.split(11), rng=random.Random(24))
        assert output.candidate_count == expected
        alpha = recovered.coordinates[0]
        left = Matrix.hstack(*(matrix_on_column(source.order, alpha, eye(8)[:, i])
                               for i in range(8)))
        completions, admitted = 0, []
        for kernel in lagrangians(11):
            if column_basis(kernel.row_join(output.image_basis), 11).cols != 2:
                continue
            completions += 1
            module = reconstruct(source.order, source.split(11), kernel, 11).module_numerator
            if integral_matrix_test(module.inv() * left * module / 11):
                admitted.append(kernel)
        assert completions == 12 and len(admitted) == expected
        truth = nullspace(action(source.phi, product_actions(source.split(11))), 11)
        assert any(same_space(truth, k, 11) for k in admitted)
        if expected <= 2:
            assert {space_key(k, 11) for k in output.candidates} == {space_key(k, 11) for k in admitted}
        label_queries, recovered_kernel = 0, expected == 1
        if expected == 2:
            labels = OpaqueLabels(truth, 11)
            selected = select_with_original_hiding_function(output.candidates, 11, labels)
            assert same_space(selected.kernel, truth, 11)
            label_queries, recovered_kernel = labels.calls, True
        powers = [unit(source.order)]
        for _ in range(3):
            powers.append(matrix_multiply(source.order, powers[-1], source.gammas[0]))
        independent_powers = Matrix.hstack(*powers).rank()
        if expected <= 2:
            assert independent_powers == 4
        records.append({
            "id": f"general_target_map_{kind}", "ell": 11, "characteristic": 7,
            "fixture_phi_not_extractor_input": [int(x) for x in source.phi],
            "target_map": [int(x) for x in source.gammas[0]],
            "reconstructed_pullback": [int(x) for x in alpha],
            "target_map_independent_powers_through_degree_three": independent_powers,
            "auxiliary_primes": list(recovered.primes), "crt_modulus": recovered.modulus,
            "weak_residue_packets": len(source.calls), "additional_weak_queries_for_refinement": 0,
            "old_image_ranks": list(old.rank_history),
            "old_image_only_completions": completions,
            "residual_operators": [matrix_rows(b) for b in output.operators],
            "new_candidate_count": output.candidate_count,
            "candidate_columns": [matrix_rows(k) for k in output.candidates],
            "independent_module_admitted_count": len(admitted),
            "status": output.status, "reference_kernel_recovered_in_control": recovered_kernel,
            "opaque_original_source_calls_in_control": label_queries,
            "actual_geometric_source_calls": 0,
            "exact_source_products_checked": output.exact_source_products_checked,
            "geometric_input_verified_by_extractor": output.geometric_input_verified,
            "root_draws": output.root_draws, "root_abort_bound": output.root_abort_bound,
        })
    ell = 2**127 - 1
    large = analyze_rank_one([local_action(Matrix([[1, 0], [0, 2]]), ell)], ell,
                            rng=random.Random(7))
    scalar = analyze_rank_one([local_action(eye(2), ell)], ell)
    assert large.candidate_count == 2 and scalar.candidate_count == ell + 1
    here = Path(__file__).resolve().parent
    paths = [here / name for name in ("residual_algebra.py", "algebra_controls.py",
             "test_residual_algebra.py", "replay.py", "RESIDUAL_ALGEBRA.md", "HANDOFF.md")]
    paths += [here.parent / name for name in (
        "source-pullback-2026-10-23/pullback.py", "source-pullback-2026-10-23/controls.py",
        "frobenius-residual-2026-10-23/residual.py",
        "frobenius-residual-2026-10-23/residual_controls.py",
        "kernel-output-2026-10-23/kernel_output.py",
        "scalar-cancellation-2026-10-23/scalar_cancellation.py")]
    return {
        "scope": "complete rank-one integrality refinement for the existing weak-isogeny source",
        "independent_review": False, "novelty_claim": False,
        "natural_geometric_instance_executed": False, "quantum_execution": False,
        "records": records,
        "large_prime_local_only_control": {"ell": ell, "candidates": large.candidate_count,
                                           "scalar_symbolic_count": scalar.candidate_count,
                                           "full_field_enumeration": False},
        "sha256": {str(p.relative_to(here.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in paths},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
        print(json.dumps({"output": str(args.output.resolve()),
                          "candidate_counts": [r["new_candidate_count"] for r in result["records"]],
                          "hashes": len(result["sha256"])}))
    else:
        print(encoded, end="")
