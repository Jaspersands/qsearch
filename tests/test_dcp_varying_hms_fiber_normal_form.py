import math

import pytest

from dcp_varying_hms_fiber_normal_form import (
    fiber_compression_control,
    hms_phase_state,
    run_dcp_varying_hms_fiber_normal_form,
    varying_hms_fourier_control,
    write_dcp_varying_hms_fiber_normal_form,
)


def test_hms_phase_state_rejects_duplicate_support():
    with pytest.raises(ValueError, match="distinct"):
        hms_phase_state(11, (0, 1, 1), 3)


def test_varying_known_supports_preserve_samplewise_fourier_success():
    row = varying_hms_fourier_control(
        "varying",
        17,
        supports=((0, 1), (0, 3, 5, 8, 12), (2, 4, 9)),
        phase_targets=(1, 7, 14),
    )
    assert not row.supports_identical
    assert row.varying_support_extension_verified
    assert row.observed_target_probabilities == pytest.approx(
        [2 / 17, 5 / 17, 3 / 17]
    )
    assert row.observed_joint_all_correct_probability == pytest.approx(
        (2 * 5 * 3) / 17**3
    )


def test_injective_subset_sum_control_matches_hms_and_pgm_formulas():
    row = fiber_compression_control(
        "injective",
        17,
        labels=(1, 2, 4),
        phase_target=6,
        structured_polylog_fiber_compression_known=True,
    )
    assert row.collision_pair_count == 0
    assert row.occupied_residue_count == 8
    assert row.observed_compressed_qft_success == pytest.approx(8 / 17)
    assert row.covariant_pgm_success_probability == pytest.approx(8 / 17)
    assert row.forward_compute_with_preimage_garbage_success == pytest.approx(1 / 17)
    assert row.coherent_interference_gain == pytest.approx(8.0)
    assert row.normal_form_verified


def test_uniform_collisions_can_give_perfect_information():
    row = fiber_compression_control(
        "uniform-two-to-one",
        8,
        labels=(1, 2, 4, 0),
        phase_target=5,
        structured_polylog_fiber_compression_known=True,
    )
    assert row.collision_pair_count == 8
    assert row.minimum_positive_multiplicity == 2
    assert row.maximum_multiplicity == 2
    assert row.multiplicities_uniform_on_support
    assert row.observed_compressed_qft_success == pytest.approx(1.0)
    assert row.forward_compute_with_preimage_garbage_success == pytest.approx(1 / 8)
    assert row.coherent_interference_gain == pytest.approx(8.0)


def test_nonuniform_collisions_still_match_exact_pgm_formula():
    row = fiber_compression_control(
        "nonuniform",
        17,
        labels=(1, 2, 3, 6),
        phase_target=7,
    )
    assert row.collision_pair_count > 0
    assert not row.multiplicities_uniform_on_support
    assert row.pgm_formula_residual < 1e-12
    assert row.forward_garbage_formula_residual < 1e-12
    assert row.observed_compressed_qft_success > 1 / 17
    assert not row.generic_random_instance_circuit_constructed


def test_forward_garbage_probability_is_label_independent():
    controls = [
        fiber_compression_control("a", 13, (0, 0, 0), phase_target=2),
        fiber_compression_control("b", 13, (1, 2, 4), phase_target=2),
        fiber_compression_control("c", 13, (1, 1, 2, 3), phase_target=2),
    ]
    for row in controls:
        assert row.forward_compute_with_preimage_garbage_success == pytest.approx(1 / 13)
        assert row.forward_garbage_formula_residual < 1e-12


def test_report_corrects_false_fixed_set_blocker_without_claiming_algorithm(tmp_path):
    report = run_dcp_varying_hms_fiber_normal_form()
    assert report.theorem.theorem_verified
    assert report.theorem.varying_support_extension_proved
    assert report.theorem.weighted_multiplier_normal_form_proved
    assert report.theorem.pgm_success_identity_proved
    assert report.theorem.retained_preimage_no_interference_proved
    assert not report.theorem.collisions_are_information_no_go
    assert not report.theorem.generic_fiber_compression_constructed
    assert not report.theorem.dcp_polynomial_algorithm_constructed
    assert report.headline_metrics["perfect_information_collision_control_count"] == 1
    assert not report.claim_gate["shift_multiplicity_candidate_passes_proof_gate"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_dcp_varying_hms_fiber_normal_form(tmp_path / "report.json")
    assert payload["status"] == "varying-hms-dcp-fiber-normal-form-active"
