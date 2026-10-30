"""Replay arithmetic controls; the output is not a real-input admission."""

import argparse
import hashlib
import json
from pathlib import Path
import random

from sympy import Matrix, eye

from borel_residual import build_borel_reduction, check_exceptional_planes
from residual import (
    ROOT, analyze_local_matrix, analyze_pullback, mod, nullspace, same_space,
    select_with_original_hiding_function,
)
from residual_controls import (
    OpaqueLabels, incompatible_inert_pullback, inert_stable_fixture,
    split_frobenius_fixture,
)
from controls import frobenius_relation_fixture
from kernel_output import action, odd_maximal_split, product_actions
from pullback import reconstruct_pullbacks


def run():
    rows = []
    fixtures = [(f"split_rank_{i}", split_frobenius_fixture(i)) for i in range(3)]
    fixtures += [("inert_rank_zero", inert_stable_fixture()),
                 ("previous_ell_eleven_rank_one", frobenius_relation_fixture(1))]
    for name, source in fixtures:
        recovered = reconstruct_pullbacks(source.order, source.ell, source.characteristic,
                                          source.norms(), source.levels(), source.split,
                                          source.observe, max_auxiliary_prime=47)
        if recovered.coordinates != source.reference_pullbacks():
            raise AssertionError("weak-action CRT recovery mismatch")
        result = analyze_pullback(source.order, recovered.coordinates[0], source.ell,
                                  source.characteristic, source.split(source.ell),
                                  rng=random.Random(721))
        truth = nullspace(action(source.phi, product_actions(source.split(source.ell))), source.ell)
        row = {
            "id": name, "characteristic": source.characteristic, "ell": source.ell,
            "rank": result.image_rank, "status": result.status,
            "splitting_type": result.splitting_type,
            "compatible_lagrangians_for_this_map": result.candidate_count,
            "exact_source_relations_checked": result.exact_source_relations_checked,
            "weak_arithmetic_packets": len(source.calls),
            "auxiliary_primes": list(recovered.primes), "crt_modulus": recovered.modulus,
            "point_access_requirements_not_executions": {
                "weak_basis": recovered.weak_basis_points_required,
                "gamma_basis": recovered.target_basis_points_required,
                "source_basis_maps": recovered.source_basis_points_required},
            "geometric_point_evaluations_executed": 0,
        }
        if result.image_rank == 1:
            oracle = OpaqueLabels(truth, source.ell)
            selected = select_with_original_hiding_function(result.candidates, source.ell, oracle)
            if not same_space(truth, selected.kernel, source.ell):
                raise AssertionError("original-source selection failed")
            row.update(original_opaque_label_calls=oracle.calls, reference_kernel_recovered=True,
                       root_draws=result.root_draws, root_abort_bound=result.root_abort_bound)
        elif result.image_rank == 2:
            if not same_space(truth, result.candidates[0], source.ell):
                raise AssertionError("full-image recovery failed")
            row.update(original_opaque_label_calls=0, reference_kernel_recovered=True)
        else:
            reduction = build_borel_reduction(result.residual_operator, source.ell,
                                               source.characteristic, rng=random.Random(523))
            oracle = OpaqueLabels(truth, source.ell)
            exceptional = check_exceptional_planes(reduction, oracle)
            row.update(existing_receiver_domain=reduction.domain,
                       original_opaque_exception_checks=oracle.calls,
                       exceptional_kernel_found=exceptional.kernel is not None,
                       random_draws=reduction.random_draws, abort_bound=reduction.abort_bound,
                       imported_quantum_receiver_executed=False)
            if exceptional.kernel is not None and not same_space(truth, exceptional.kernel, source.ell):
                raise AssertionError("exceptional-plane check failed")
        rows.append(row)

    order, alpha = incompatible_inert_pullback()
    bad = analyze_pullback(order, alpha, 5, 7, odd_maximal_split(7, 5))
    if bad.status != "INCONSISTENT_WITH_INPUT_PROMISE" or bad.candidate_count:
        raise AssertionError("incompatible integral source map was admitted")
    large = []
    ell = 2**127 - 1
    a = Matrix.diag(Matrix([[0, ell * ell], [-7, 0]]),
                    ell * Matrix([[0, 1], [-7, 0]]))
    r = analyze_local_matrix(a, ell, 7, rng=random.Random(918))
    large.append({"case": "rank_one", "candidate_count": r.candidate_count,
                  "exact_global_source_verified": False, "root_draws": r.root_draws})
    for p in (7, 11):
        block = Matrix([[0, 1], [-p, 0]])
        b = build_borel_reduction(Matrix.diag(block, block), ell, p, rng=random.Random(483))
        group_element, line = Matrix([[1, 87324], [0, 1]]), Matrix([972442, 78345])
        checked = same_space(b.embed(group_element) * b.kernel_from_line(line),
                             b.kernel_from_line(group_element * line), ell)
        if not checked:
            raise AssertionError("large-prime Borel action failed")
        large.append({"case": "rank_zero", "characteristic": p, "domain": b.domain,
                      "equivariance_checked": checked, "random_draws": b.random_draws,
                      "abort_bound": b.abort_bound, "exact_global_source_verified": False})
    root = Path(__file__).resolve().parent
    files = list(root.glob("*.py"))
    files += [ROOT / directory / name for directory, name in (
        ("source-pullback-2026-10-23", "pullback.py"),
        ("source-pullback-2026-10-23", "controls.py"),
        ("kernel-output-2026-10-23", "kernel_output.py"),
        ("quadratic-cancellation-2026-10-23", "quadratic_cancellation.py"),
        ("central-rank-2026-10-23", "central_rank.py"),
        ("scalar-cancellation-2026-10-23", "scalar_cancellation.py"),
    )]
    return {
        "scope": "same-input skew-Frobenius residual reduction, arithmetic controls only",
        "new_quantum_algorithm": False, "novelty_claim": False,
        "independent_review": False, "geometry_executed": False,
        "quantum_receiver_executed": False,
        "secret_phi_used_only_in_fixture_and_correctness_comparison": True,
        "original_source_promise_verified": False,
        "finite_counts_are_not_full_input_indistinguishability": True,
        "positive_square_self_adjoint_twists_excluded": True,
        "seeded_replay_does_not_certify_uniform_randomness": True,
        "records": rows,
        "integral_relation_without_compatible_neighbor": {
            "status": bad.status, "rank": bad.image_rank,
            "exact_source_relations_checked": bad.exact_source_relations_checked,
            "compatible_kernels": bad.candidate_count},
        "large_prime_local_controls": {"ell": ell, "bits": ell.bit_length(), "records": large},
        "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in sorted(files)},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    serialized = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(serialized)
        print(f"Wrote arithmetic-only receipt: {arguments.output}")
    else:
        print(serialized, end="")
