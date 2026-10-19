"""Independent native equations and physical receiver tests, not speedup claims."""

from itertools import product
from fractions import Fraction
import json

import numpy as np
import pytest

from theorems import outer_coded_chirp_probe as module
from theorems.prime_character_opi import ring, root_at_infinity


@pytest.mark.parametrize("p,r", [(5, 1), (7, 2), (11, 2)])
def test_every_native_target_in_small_fields_has_a_verified_nontrivial_witness(p, r):
    for target in product(range(p), repeat=r):
        row = module.complete_moment_squares(p, target)
        x = row["native_square_roots_x"]
        direct = [sum(pow(a, k, p) * z * z for a, z in enumerate(x, start=1)) % p for k in range(r)]
        assert direct == list(target)
        assert any(x)
        R = row["root_polynomial_coefficients"]
        assert R[0] == 0
        assert all(sum(c * pow(a, j, p) for j, c in enumerate(R)) % p == z
                   for a, z in enumerate(x, start=1))
        assert not row["coefficient_or_field_relaxation"]
        assert not row["sparse_punctured_or_folded_norm_problem_solved"]


def test_formal_square_preserves_exact_high_coefficients_and_no_power_sum_alias():
    row = module.complete_moment_squares(31, list(range(14)))
    C = ring(31)
    square = C(row["root_polynomial_coefficients"]) ** 2
    assert int(square[0]) == 0
    assert row["root_degree"] == 16
    for k, b in enumerate(row["ORIGINAL_target"]):
        assert int(square[30 - k]) == -b % 31
    assert square.degree() + row["rank_r"] - 1 < 2 * row["variables_N"]


def test_every_dense_small_support_and_target_is_solved_without_changing_support():
    from itertools import combinations
    for points in combinations(range(1, 7), 5):
        for target in product(range(7), repeat=1):
            row = module.complete_moment_squares(7, target, points=tuple(reversed(points)))
            assert row["ORIGINAL_support_points"] == list(reversed(points))
            x = row["native_square_roots_x"]
            assert sum(z * z for z in x) % 7 == target[0]
            R = ring(7)(row["root_polynomial_coefficients"])
            assert all(int(R(a)) == 0 for a in row["missing_points_forced_zero"])
            assert row["square_cancellation_degree_upper"] < row["lowest_prescribed_square_coefficient"]
            assert row["dense_unweighted_prime_field_puncturing_covered"]


def test_sparse_support_is_refused_before_any_field_sized_expansion():
    with pytest.raises(ValueError, match="strict rank boundary"):
        module.complete_moment_squares((1 << 61) - 1, [1], points=range(1, 128))
    for points in ((1, 1, 2), (0, 1, 2), (True, 2, 3)):
        with pytest.raises(ValueError, match="ORIGINAL"):
            module.complete_moment_squares(7, [0], points=points)


def test_strict_rank_boundary_is_real_for_this_construction_not_an_unsatisfiability_claim():
    # At the excluded r=N/2 boundary, removing the constant can destroy a
    # prescribed coefficient. This is an algorithm-scope countercontrol.
    p, N, d = 7, 6, 4
    C = ring(p)
    F = C.gen() ** (N + 2) - C.gen() ** (N - 2)
    R, _ = root_at_infinity(p, F, 2, d)
    R -= int(R[0])
    x = [int(R(a)) for a in range(1, p)]
    assert module.native_moments(p, x, 3) != [0, 0, 1]
    with pytest.raises(ValueError, match="strict rank boundary"):
        module.complete_moment_squares(p, [0, 0, 1])


@pytest.mark.parametrize("p", [5, 7, 11, 13])
def test_actual_local_unitary_receiver_has_derived_success_for_every_label(p):
    row = module.local_chirp_receiver(p)
    matrix = np.array(row["probabilities_by_outcome_and_label"])
    assert row["unitarity_max_error"] < 2e-14
    assert row["normalized_output_max_error"] < 2e-14
    assert row["actual_diagonal_probability_max_error"] < 2e-14
    assert np.allclose(matrix.sum(axis=0), 1)
    assert np.allclose(np.diag(matrix), row["correct_probability"])
    assert not row["postselection_or_additional_chirp_copy_used"]
    if p % 4 == 3:
        assert np.allclose(matrix[~np.eye(p, dtype=bool)], (1 - row["correct_probability"]) / (p - 1))
    else:
        assert np.ptp(matrix[~np.eye(p, dtype=bool)]) > 1e-3


def test_chirp_phase_cannot_be_discarded_as_an_irrelevant_global_phase():
    p = 7
    row = module.local_chirp_receiver(p)
    correct = row["correct_probability"]
    # Removing all phases makes every label give the SAME output column;
    # its average identification probability is1/p for ANY fixed receiver.
    assert correct > 0.5 > 1 / p
    assert abs(row["wrong_phase_erasure_average_identification_probability"] - 1 / p) < 2e-14
    assert row["wrong_phase_erasure_max_label_dependence"] < 2e-14
    assert row["qary_symmetric_only_when_p_is_3_mod_4"]


def test_validation_rejects_wrong_domains_and_out_of_scope_targets():
    for p, target in ((2, [0]), (5, []), (7, [True]), (7, [-1]), (7, [7]), (9, [0])):
        with pytest.raises((ValueError, TypeError)):
            module.complete_moment_squares(p, target)
    with pytest.raises(ValueError, match="ORIGINAL"):
        module.native_moments(7, [0] * 5, 1)


def test_live_report_preserves_provenance_and_original_moment_witnesses():
    if not module.REPORT.exists():
        pytest.skip("live workflow has not been emitted")
    report = json.loads(module.REPORT.read_text())
    assert report["source_sha256"] == module.sha256(module.__file__)
    for name, digest in report["dependency_sha256"].items():
        assert module.sha256(module.ROOT / "theorems" / name) == digest
    assert [r["variables_N"] for r in report["classical_native_controls"]] == [30, 126, 1020, 1020, 100, 800]
    assert report["no_central_candidate_negative_or_proof_promotion"]
    for row in report["classical_native_controls"]:
        assert module.native_moments(row["prime"], row["native_square_roots_x"], row["rank_r"],
                                     points=row["ORIGINAL_support_points"]) == row["ORIGINAL_target"]
        assert row["source_rerolls"] == 0
        assert not row["accepted_speedup_candidate"]
        assert not row["sparse_punctured_or_folded_norm_problem_solved"]


@pytest.fixture(scope="module")
def small_coherent_model():
    return module.coherent_chirp_model(7, (1, 2, 3), 1)


def test_full_instrument_retains_flags_and_checks_original_targets(small_coherent_model):
    model = small_coherent_model
    table = model["decoded"].copy()
    rows = [module.coherent_chirp_target(model, [b]) for b in range(7)]
    counts = [sum(sum(x * x for x in xs) % 7 == b
                  for xs in product(range(7), repeat=3)) for b in range(7)]
    for row, count in zip(rows, counts):
        assert row["native_solution_count"] == count
        assert row["native_ideal_identity_max_error"] < 2e-12
        assert row["full_instrument_squared_norm"] == pytest.approx(1)
        assert row["zero_residual_label_probability"] == pytest.approx(model["success"])
        assert row["nonzero_residual_label_probability"] > 0
        assert row["paid_zero_flag_AND_original_equations_probability"] <= model["success"] + 1e-12
    assert np.array_equal(model["decoded"], table)
    mean = np.mean([r["full_flagged_squared_vector_error_to_UNNORMALIZED_ideal"] for r in rows])
    assert mean == pytest.approx(2 * (1 - model["success"]), abs=2e-12)
    assert any(r["full_flagged_squared_vector_error_to_UNNORMALIZED_ideal"] > mean + 1e-10
               for r in rows)


def test_infeasible_targets_are_neither_normalized_nor_removed():
    row = module.full_coherent_control(3, (1, 2), 2)
    assert row["all_targets_retained"] == 9
    assert row["infeasible_targets_retained"] == 5
    for target in row["targets"]:
        if not target["native_solution_count"]:
            assert target["infeasible_target_was_not_normalized_or_dropped"]
            assert target["full_flagged_fidelity_to_normalized_ideal"] is None
            assert target["paid_zero_flag_AND_original_equations_probability"] == 0


def test_exact_histogram_certificate_matches_physical_decoder(small_coherent_model):
    model = small_coherent_model
    interval = model["error_interval"]
    lo, hi = (Fraction(interval[k]) for k in ("epsilon_lower_exact", "epsilon_upper_exact"))
    assert lo <= hi
    assert float(lo) == pytest.approx(1 - model["success"], abs=2e-13)
    assert hi - lo < Fraction(1, 1 << 70)
    assert sum(interval["correct_label_counts_by_Hamming_error_weight"]) == 7 ** 3
    assert "NOT_A_SCALABLE" in interval["scope"]
    with pytest.raises(ValueError, match="p3mod4"):
        module.decoder_error_interval(5, 2, 5, [5, 10, 10])


def test_wrong_inverse_survives_norm_checks_but_fails_native_fidelity(small_coherent_model):
    correct = module.coherent_chirp_target(small_coherent_model, [1])
    wrong = module.coherent_chirp_target(small_coherent_model, [1], wrong_transpose_inverse=True)
    assert correct["zero_residual_label_probability"] == pytest.approx(wrong["zero_residual_label_probability"])
    assert wrong["full_instrument_squared_norm"] == pytest.approx(1)
    assert correct["full_flagged_fidelity_to_normalized_ideal"] > 0.4
    assert wrong["full_flagged_fidelity_to_normalized_ideal"] < 0.001
    assert wrong["paid_zero_flag_AND_original_equations_probability"] < 0.08


@pytest.mark.parametrize("p", [7, 11])
def test_rank_one_calibration_has_a_separate_native_classical_solution(p):
    for b in range(p):
        row = module.single_moment_classical(p, b, 3)
        assert row["status"] == "CLASSICAL_NATIVE_TWO_SQUARE_WITNESS"
        assert len(row["values"]) == 3
        assert sum(x * x for x in row["values"]) % p == b
        assert row["seeded_transcript_is_not_a_confidence_theorem"]


def test_generic_counterexample_is_actual_unitary_not_an_rs_no_go():
    row = module.generic_coherence_counterexample(17, dense_check=True)
    assert row["actual_unitarity_max_error"] < 2e-14
    assert row["actual_zero_target_full_flagged_fidelity"] == pytest.approx(1 / 289)
    assert row["actual_zero_target_conditional_fidelity"] == pytest.approx(1 / 227)
    assert row["generic_pointwise_inference_falsified_not_native_RS_no_go"]
    large = module.generic_coherence_counterexample(1 << 20)
    assert Fraction(large["basis_label_error_exact"]) < Fraction(4, 10 ** 6)
    assert Fraction(large["zero_target_conditional_fidelity_exact"]) < Fraction(1, 10 ** 12)
    assert not large["dense_check_executed"]


def test_physical_model_refuses_oversize_and_invalid_targets(small_coherent_model):
    with pytest.raises(ValueError, match="bounded physical"):
        module.coherent_chirp_model((1 << 61) - 1, (1, 2, 3), 1)
    with pytest.raises(ValueError, match="bounded physical"):
        module.coherent_chirp_model(5, (1, 2), 1)
    for target in ([True], [-1], [7], [], [0, 1]):
        with pytest.raises(ValueError, match="ORIGINAL target"):
            module.coherent_chirp_target(small_coherent_model, target)


def test_live_coherence_report_preserves_all_targets_and_scope():
    report = json.loads(module.REPORT.read_text())
    assert report["schema_version"] == "outer-coded-chirp-probe-v2"
    controls = report["full_flagged_coherent_controls"]
    assert sum(c["all_targets_retained"] for c in controls) == 69
    assert sum(c["infeasible_targets_retained"] for c in controls) == 5
    for row in controls:
        assert row["mean_error_identity_residual"] < 2e-11
        assert row["naive_pointwise_use_of_mean_squared_error_is_falsified"]
        assert row["costs"]["dense_simulation_and_ML_decoder_are_EXPONENTIAL_calibrations"]
        assert not row["accepted_speedup_or_general_no_go_claim"]
        lower = Fraction(row["exact_decoder_error_interval"]["mean_paid_native_validity_lower_exact"])
        assert row["mean_paid_original_validity"] >= float(lower) - 2e-12
