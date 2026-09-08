from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_affine_node_frame_response_boundary import (
    _finite_controls,
    affine_node_average_frame,
    affine_node_circuit_record,
    affine_node_masks,
    audit_affine_node_frame_formula,
    audit_equal_width_response_scale_cancellation,
    natural_response_window_record,
    representation_lcu_affine_node_average,
    run_affine_node_frame_response_boundary,
    write_affine_node_frame_response_boundary_report,
)


REPEATED_STANDARD = (((3,), (2, 1)),) * 3


def test_affine_node_masks_are_table_free_coset() -> None:
    masks = affine_node_masks(5, 16, (1, 2, 12))

    assert len(masks) == 8
    assert len(set(masks)) == 8
    assert all(mask & 16 for mask in masks)


@pytest.mark.parametrize(
    ("bit_count", "offset", "generators"),
    [
        (3, 0, (1, 1)),
        (3, 0, (0, 2)),
        (3, 8, (1, 2)),
    ],
)
def test_affine_node_masks_reject_invalid_data(
    bit_count: int,
    offset: int,
    generators: tuple[int, ...],
) -> None:
    with pytest.raises(ValueError):
        affine_node_masks(bit_count, offset, generators)


def test_representation_lcu_formula_matches_physical_node_average() -> None:
    direct = affine_node_average_frame((3,), REPEATED_STANDARD, 0, (1, 2))
    formula = representation_lcu_affine_node_average(
        (3,),
        REPEATED_STANDARD,
        0,
        (1, 2),
    )

    assert np.linalg.norm(direct - formula, ord=2) < 1e-12
    assert np.linalg.eigvalsh(direct)[0] > -1e-12
    assert np.linalg.eigvalsh(direct)[-1] <= 1 + 1e-12


def test_affine_node_frame_control_records_normalization_one() -> None:
    row = audit_affine_node_frame_formula(
        "left",
        (3,),
        REPEATED_STANDARD,
        0,
        (1, 2),
    )

    assert row.exact_affine_node_representation_average_verified
    assert row.node_width == 4
    assert row.representation_summand_count == 24
    assert row.lcu_block_encoding_normalization == 1
    assert row.unnormalized_frame_lcu_normalization == 4
    assert row.affine_mask_table_entry_count == 0
    assert row.maximum_representation_formula_residual < 1e-12


def test_balanced_response_width_scale_cancels_but_inverse_remains() -> None:
    row = audit_equal_width_response_scale_cancellation(
        "root",
        (3,),
        REPEATED_STANDARD,
        0,
        4,
        (1, 2),
    )

    assert row.exact_response_scale_boundary_verified
    assert row.child_width == 4
    assert row.common_span_dimension == 5
    assert row.equal_width_scale_cancels_exactly
    assert row.separate_normalized_frame_inverse_still_required
    assert row.maximum_response_width_scaling_residual < 1e-12
    assert row.endpoint_effect_scale_cancellation_residual < 1e-12
    assert row.endpoint_effect_minimum_eigenvalue > 0.2
    assert row.endpoint_effect_maximum_eigenvalue < 0.8


def test_finite_control_bundle_is_fully_representation_based() -> None:
    frames, responses = _finite_controls()

    assert len(frames) == 3
    assert len(responses) == 1
    assert all(row.exact_affine_node_representation_average_verified for row in frames)
    assert all(row.exact_response_scale_boundary_verified for row in responses)


def test_affine_node_circuit_is_polynomial_but_does_not_compile_response() -> None:
    row = affine_node_circuit_record(32, 120, 119)

    assert row.affine_coordinate_hadamard_count == 119
    assert row.affine_mask_cnot_upper_bound == 120 * 119
    assert row.controlled_irrep_action_count_per_select == 121
    assert row.average_frame_block_encoding_normalization == 1
    assert row.leaf_metric_table_entries == 0
    assert row.polynomial_given_controlled_sn_action
    assert not row.response_pseudoinverse_compiled


@pytest.mark.parametrize("n", [32, 40, 48])
def test_natural_polynomial_response_window_fails_full_sibling_mass(n: int) -> None:
    row = natural_response_window_record(n)

    assert row.conditional_good_event_probability_lower_bound > 0.99
    assert row.globally_distinct_full_sibling_native_retained_mass_upper_bound < 0.01
    assert row.globally_distinct_full_sibling_native_retained_mass_upper_bound < (
        row.required_retained_mass_benchmark
    )
    assert row.finite_full_sibling_mass_requirement_falsified
    assert row.asymptotic_inverse_polynomial_window_mass_vanishes
    assert row.asymptotic_common_spectral_trim_relative_dimension_vanishes
    assert not row.polynomial_separate_qsvt_inverse_is_uniform_common_fiber_compiler
    assert not row.parent_common_fiber_native_density_bound_proved
    assert not row.parent_conditional_native_loss_recurrence_proved
    assert not row.direct_joint_scale_free_naimark_ruled_out


@pytest.mark.parametrize("n", [40, 48])
def test_common_qsvt_spectral_trim_has_vanishing_dimension_proxy(n: int) -> None:
    row = natural_response_window_record(n)

    assert row.common_span_relative_rank_asymptotic_lower_bound == pytest.approx(
        19 / 128
    )
    assert row.common_span_event_mass_asymptotic_lower_bound == pytest.approx(1 / 9)
    assert row.common_spectral_trim_relative_dimension_upper_bound_proxy < 1e-6


def test_report_advances_actual_kernel_and_closes_only_separate_qsvt_route() -> None:
    report = run_affine_node_frame_response_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "actual_affine_node_frame_formula_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "normalization_one_affine_node_frame_block_encoding_count"
    ] == 1
    assert report.headline_metrics[
        "equal_width_endpoint_scale_cancellation_theorem_count"
    ] == 1
    assert report.headline_metrics["imported_natural_sibling_mass_theorem_count"] == 1
    assert report.headline_metrics[
        "imported_positive_mass_common_span_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "separate_qsvt_full_sibling_mass_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "separate_qsvt_common_fiber_dimension_no_go_theorem_count"
    ] == 1
    assert report.claim_gate[
        "actual_affine_node_frame_low_description_formula_proved"
    ]
    assert report.claim_gate[
        "actual_affine_node_frame_block_encoding_normalization_one"
    ]
    assert report.claim_gate["balanced_response_width_scale_cancellation_proved"]
    assert not report.claim_gate["normalized_frame_access_equals_response_access"]
    assert not report.claim_gate[
        "separate_polynomial_qsvt_response_preserves_full_sibling_native_mass"
    ]
    assert not report.claim_gate[
        "separate_qsvt_is_uniform_common_fiber_response_compiler"
    ]
    assert not report.claim_gate[
        "parent_conditional_native_loss_o_one_over_depth_proved"
    ]
    assert not report.claim_gate["joint_scale_free_generalized_eigenvalue_compiler_proved"]
    assert not report.claim_gate["direct_local_schur_racah_naimark_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_round_trip(tmp_path) -> None:
    path = tmp_path / "affine-node-frame-response.json"
    payload = write_affine_node_frame_response_boundary_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["status"] == (
        "affine-node-frame-lcu-proved-separate-qsvt-uniform-common-fiber-falsified-native-density-open"
    )
    assert payload["primary_literature"][0]["url"].startswith("https://")
