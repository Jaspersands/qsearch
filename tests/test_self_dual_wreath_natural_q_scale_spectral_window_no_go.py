from __future__ import annotations

import json
import math

import numpy as np
import pytest

from research_registry import (
    initialize_seed_registry,
    load_experiments,
    load_negative_results,
)
from self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary import (
    s3_pair_data,
)
from self_dual_wreath_natural_q_scale_spectral_window_no_go import (
    audit_q_scale_spectral_mass,
    identical_rank_one_projectors,
    natural_q_scale_window_scaling_record,
    orthogonal_rank_one_projectors,
    run_natural_q_scale_spectral_window_no_go,
    write_natural_q_scale_spectral_window_no_go_report,
)


def test_regular_s3_frame_has_only_one_third_native_mass_at_q_scale() -> None:
    _, projectors, _ = s3_pair_data()
    control = audit_q_scale_spectral_mass(
        projectors,
        1,
        control_id="regular-s3",
    )
    assert control.q_scale_mass_bound_verified
    assert control.branch_count == 3
    assert control.ambient_dimension == 6
    assert control.leaf_rank == 3
    assert control.frame_trace == pytest.approx(9.0)
    assert control.frame_second_moment == pytest.approx(18.0)
    assert control.average_normalized_ordered_pair_overlap == pytest.approx(0.5)
    assert control.exact_native_high_spectral_mass == pytest.approx(1 / 3)
    assert control.second_moment_high_mass_upper_bound == pytest.approx(2 / 3)
    assert control.frame_gram_nonzero_spectrum_residual < 1e-9


def test_orthogonal_and_identical_frames_saturate_opposite_coherence_limits() -> None:
    orthogonal = audit_q_scale_spectral_mass(
        orthogonal_rank_one_projectors(8),
        2,
        control_id="orthogonal",
    )
    identical = audit_q_scale_spectral_mass(
        identical_rank_one_projectors(8),
        1,
        control_id="identical",
    )
    assert orthogonal.q_scale_mass_bound_verified
    assert orthogonal.average_normalized_ordered_pair_overlap == 0.0
    assert orthogonal.exact_native_high_spectral_mass == 0.0
    assert orthogonal.second_moment_high_mass_upper_bound == pytest.approx(0.25)
    assert identical.q_scale_mass_bound_verified
    assert identical.average_normalized_ordered_pair_overlap == pytest.approx(1.0)
    assert identical.exact_native_high_spectral_mass == pytest.approx(1.0)
    assert identical.second_moment_high_mass_upper_bound == pytest.approx(1.0)


def test_pair_overlap_identity_and_mass_bound_hold_for_rotated_rank_two_frame() -> None:
    first = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
    theta = 0.37
    rotation = np.asarray(
        [
            [math.cos(theta), 0.0, -math.sin(theta), 0.0],
            [0.0, math.cos(theta), 0.0, -math.sin(theta)],
            [math.sin(theta), 0.0, math.cos(theta), 0.0],
            [0.0, math.sin(theta), 0.0, math.cos(theta)],
        ],
        dtype=complex,
    )
    second = rotation @ first @ rotation.conj().T
    control = audit_q_scale_spectral_mass(
        (first, second),
        2,
        control_id="rotated-rank-two",
    )
    assert control.q_scale_mass_bound_verified
    assert control.leaf_rank == 2
    assert control.pair_overlap_identity_residual < 1e-9
    assert control.exact_native_high_spectral_mass <= (
        control.second_moment_high_mass_upper_bound + 1e-12
    )


def test_natural_record_charges_targets_conditioning_and_rank_failure() -> None:
    row = natural_q_scale_window_scaling_record(
        16,
        polynomial_window_degree=2,
        confidence_degree=2,
    )
    assert row.partition_count == 231
    assert row.selected_copy_count == math.ceil(row.log2_group_order) + 2
    assert row.child_orientation_count_log2 == row.selected_copy_count - 1
    assert row.markov_failure_probability == pytest.approx(1 / 16**2)
    assert row.conditioned_good_event_probability_lower_bound > 0.99
    assert row.factorial_domination_margin_log2 > 0
    assert row.asymptotic_q_scale_native_mass_vanishes
    assert not row.normalized_gram_inverse_polynomial_window_retains_positive_mass
    assert not row.normalized_analysis_inverse_polynomial_window_retains_positive_mass
    assert not row.hierarchical_or_direct_global_polar_ruled_out


def test_fixed_copy_multiplier_three_has_same_factorial_q_scale_bound() -> None:
    row = natural_q_scale_window_scaling_record(
        20,
        copy_multiplier=3,
        polynomial_window_degree=2,
        confidence_degree=2,
    )
    assert row.selected_copy_count == math.ceil(3 * row.log2_group_order) + 2
    assert row.child_aspect_ratio > math.factorial(20)
    assert row.asymptotic_q_scale_native_mass_vanishes
    assert not row.hierarchical_or_direct_global_polar_ruled_out


def test_report_falsifies_only_canonical_polynomial_window() -> None:
    report = run_natural_q_scale_spectral_window_no_go()
    assert report.theorem.theorem_verified
    assert report.theorem_contract["verdict"] == "falsified"
    assert report.claim_gate["deterministic_q_scale_native_mass_bound_proved"]
    assert report.claim_gate["exact_equal_rank_pair_overlap_identity_proved"]
    assert report.claim_gate["global_distinct_positive_markov_transfer_proved"]
    assert report.claim_gate[
        "canonical_g_over_q_natural_polynomial_window_falsified"
    ]
    assert not report.claim_gate[
        "canonical_g_over_q_natural_inverse_polynomial_eigenvalue_window_has_positive_mass"
    ]
    assert not report.claim_gate["trace_weighted_absolute_frame_cutoff_falsified"]
    assert not report.claim_gate["nonlinear_hierarchical_metric_assembly_ruled_out"]
    assert not report.claim_gate[
        "representation_specific_direct_global_polar_ruled_out"
    ]
    assert not report.claim_gate["physical_pgm_impossibility_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_experiment_and_scoped_negative_result(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    payload = write_natural_q_scale_spectral_window_no_go_report()
    artifact_path = (
        tmp_path
        / "research/representation/"
        "self_dual_wreath_natural_q_scale_spectral_window_no_go.json"
    )
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert artifact["status"] == payload["status"]

    experiments = {row["id"]: row for row in load_experiments()}
    experiment = experiments[
        "EXP-CODE-SELF-DUAL-WREATH-NATURAL-Q-SCALE-SPECTRAL-WINDOW-NO-GO"
    ]
    assert experiment["status"] == "completed-negative-theorem"
    assert "hierarchical" in experiment["next_actions"][0]

    negatives = {row["id"]: row for row in load_negative_results()}
    negative = negatives[
        "SCHUR-COMPANION-CANONICAL-G-OVER-Q-NO-NATURAL-POLYNOMIAL-WINDOW"
    ]
    assert negative["evidence"][
        "natural_uniform_target_q_scale_no_go_proved"
    ]
    assert not negative["evidence"][
        "trace_weighted_absolute_frame_cutoff_falsified"
    ]
    assert not negative["evidence"][
        "hierarchical_or_direct_global_polar_ruled_out"
    ]
    assert not negative["evidence"]["speedup_claim_allowed"]
