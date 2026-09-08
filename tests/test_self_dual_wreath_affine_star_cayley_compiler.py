from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_affine_star_cayley_compiler import (
    audit_extracted_physical_stars,
    audit_operator_affine_star,
    audit_scalar_affine_star_compiler,
    merged_center_counterexample,
    operator_affine_star_data,
    run_affine_star_cayley_compiler,
    scalar_affine_star_cayley_values,
    scalar_affine_star_naimark,
    scalar_affine_star_signal_block_encoding,
    spectrum_only_degree_boundary,
    walsh_matrix,
    write_affine_star_cayley_compiler_report,
)


def test_walsh_and_scalar_compiler_reject_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        walsh_matrix(3)
    with pytest.raises(ValueError):
        scalar_affine_star_cayley_values(1, 0.2)
    with pytest.raises(ValueError):
        scalar_affine_star_cayley_values(4, 0.0)
    with pytest.raises(ValueError):
        scalar_affine_star_cayley_values(4, 0.6)


@pytest.mark.parametrize("width", [2, 4, 8, 16])
@pytest.mark.parametrize("gamma", [1 / 5, 1 / 9, 1 / 10])
def test_scalar_affine_star_has_exact_normalization_one_compiler(
    width: int,
    gamma: float,
) -> None:
    row = audit_scalar_affine_star_compiler(width, gamma)

    assert row.exact_label_resolved_compiler_verified
    assert row.block_encoding_normalization == 1.0
    assert row.endpoint_gap > 0.25
    assert row.signal_block_encoding_residual < 1e-12
    assert row.signal_unitarity_residual < 1e-12
    assert row.naimark_isometry_residual < 2e-12
    assert row.left_branch_effect_residual < 2e-12
    assert row.right_branch_effect_residual < 2e-12


def test_signal_and_naimark_dimensions_encode_no_width_normalization() -> None:
    signal = scalar_affine_star_signal_block_encoding(8, 1 / 9)
    naimark = scalar_affine_star_naimark(8, 1 / 9)

    assert signal.shape == (16, 16)
    assert naimark.shape == (16, 8)
    assert np.linalg.norm(signal.conj().T @ signal - np.eye(16), ord=2) < 1e-12
    assert np.linalg.norm(naimark.conj().T @ naimark - np.eye(8), ord=2) < 1e-12


def test_commuting_operator_star_reduces_to_two_address_sectors() -> None:
    angle = 0.37
    rotation = np.asarray(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    gamma = rotation @ np.diag((0.07, 0.29)) @ rotation.T
    row = audit_operator_affine_star(8, gamma)

    assert row.operator_functional_reduction_verified
    assert row.functional_cayley_residual < 1e-12
    assert row.address_sector_commutator_residual < 1e-12
    assert row.naimark_isometry_residual < 2e-12
    assert row.endpoint_gap > 0.25
    assert row.normalized_gamma_block_encoding_assumed
    assert not row.coherent_gamma_eigenlabel_supplied
    assert not row.uniform_polylogarithmic_qsvt_degree_proved


def test_operator_star_rejects_nonpositive_or_too_large_gamma() -> None:
    with pytest.raises(ValueError):
        operator_affine_star_data(4, np.diag((-0.01, 0.2)))
    with pytest.raises(ValueError):
        operator_affine_star_data(4, np.diag((0.1, 0.51)))
    with pytest.raises(ValueError):
        operator_affine_star_data(4, np.ones((2, 3)))


def test_spectrum_only_qsvt_degree_is_exponential_in_address_bits() -> None:
    rows = [spectrum_only_degree_boundary(1 << bits) for bits in (4, 8, 12, 16, 20)]

    assert rows[-1].markov_degree_lower_bound > rows[0].markov_degree_lower_bound
    assert rows[-1].markov_degree_lower_bound >= 200
    assert min(row.target_jump for row in rows) > 0.2
    assert all(not row.polynomial_in_address_bits for row in rows)
    assert all(row.exact_carrier_label_bypasses_uniform_polynomial for row in rows)


def test_degree_boundary_rejects_vacuous_error() -> None:
    with pytest.raises(ValueError):
        spectrum_only_degree_boundary(16, 0.0)
    with pytest.raises(ValueError):
        spectrum_only_degree_boundary(16, 0.1)


def test_all_current_physical_global_channels_are_covered_scalar_stars() -> None:
    row = audit_extracted_physical_stars()

    assert row.physical_control_count == 7
    assert row.extracted_channel_count == 8
    assert row.affine_star_channel_count == 8
    assert row.every_extracted_channel_is_label_resolved_scalar_star
    assert row.finite_physical_compiler_coverage_verified
    assert row.maximum_predicted_defect_residual < 1e-12


def test_merged_centers_falsify_one_predicate_star_compiler() -> None:
    row = merged_center_counterexample()

    assert row.counterexample_verified
    assert row.crossing_edge_count == 4
    assert row.distinct_cayley_eigenvalue_count > 2
    assert row.best_uniform_vs_orthogonal_fit_residual > 0.1
    assert row.uniform_address_projector_commutator_norm < 1e-12
    assert not row.one_predicate_affine_star_compiler_applies


def test_report_keeps_natural_and_matrix_claim_gates_closed() -> None:
    report = run_affine_star_cayley_compiler()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["physical_w6_compiler_covered_channel_count"] == 8
    assert report.claim_gate[
        "label_resolved_scalar_affine_star_cayley_compiled_at_normalization_one"
    ]
    assert report.claim_gate[
        "label_resolved_scalar_affine_star_naimark_compiled_directly"
    ]
    assert not report.claim_gate[
        "opaque_operator_gamma_has_uniform_polylog_qsvt_compiler"
    ]
    assert not report.claim_gate["natural_all_depth_channels_classified"]
    assert not report.claim_gate["noncommuting_matrix_valued_channels_compiled"]
    assert not report.claim_gate["physical_pgm_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_round_trip_without_registry(tmp_path) -> None:
    path = tmp_path / "affine-star-cayley.json"
    payload = write_affine_star_cayley_compiler_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["headline_metrics"][
        "normalization_one_scalar_star_cayley_compiler_count"
    ] == 1
    assert payload["status"] == (
        "label-resolved-affine-star-normalized-cayley-compiler-proved-"
        "natural-matrix-channel-boundary-open"
    )
