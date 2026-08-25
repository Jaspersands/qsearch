from __future__ import annotations

import json
import math

import numpy as np
import pytest

from research_registry import initialize_seed_registry, load_negative_results
from self_dual_wreath_addressed_cross_map_linear_assembly_normalization_boundary import (
    audit_linear_coefficient_mixer,
    audit_orthogonal_flat_frame,
    audit_s3_linear_metric_assembly,
    coefficient_mixed_kernel,
    linear_assembly_scaling_record,
    linear_dense_assembly_normalization_lower_bound,
    run_linear_assembly_normalization_boundary,
    uniform_linear_coefficient_matrix,
    write_linear_assembly_normalization_boundary_report,
)


@pytest.mark.parametrize("branch_count", [2, 3, 4, 8, 16])
def test_equal_coefficient_mixer_has_sharp_alpha_q(branch_count: int) -> None:
    control = audit_linear_coefficient_mixer(branch_count)
    assert control.alpha_lower_bound_saturated
    assert control.contractive_signal_verified
    assert control.ordered_entry_count == branch_count**2
    assert control.optimal_dense_assembly_normalization == branch_count
    assert control.unscaled_uniform_coefficient_matrix_norm == pytest.approx(
        branch_count
    )
    assert control.optimal_coefficient_matrix_norm == pytest.approx(1.0)
    assert control.optimal_coefficient_matrix_frobenius_norm == pytest.approx(1.0)
    assert control.optimal_coefficient_matrix_rank == 1
    assert linear_dense_assembly_normalization_lower_bound(branch_count) == branch_count


def test_coefficient_mixed_kernel_places_every_block_at_one_over_q() -> None:
    blocks = (
        (np.asarray([[1.0]]), np.asarray([[2.0]])),
        (np.asarray([[3.0]]), np.asarray([[4.0]])),
    )
    coefficient = uniform_linear_coefficient_matrix(2)
    np.testing.assert_allclose(
        coefficient_mixed_kernel(blocks, coefficient),
        np.asarray([[0.5, 1.0], [1.5, 2.0]]),
        atol=1e-12,
    )


def test_s3_linear_assembly_is_exact_positive_g_over_three() -> None:
    control = audit_s3_linear_metric_assembly()
    assert control.exact_control_verified
    assert control.branch_count == 3
    assert control.dense_gram_rank == 5
    assert control.dense_gram_operator_norm == pytest.approx(3.0)
    assert control.direct_instance_normalization_lower_bound == pytest.approx(3.0)
    assert control.coefficient_only_linear_normalization == 3
    assert control.normalized_gram_minimum_eigenvalue > -1e-9
    assert control.normalized_gram_minimum_positive_eigenvalue == pytest.approx(0.5)
    assert control.normalized_gram_maximum_eigenvalue == pytest.approx(1.0)
    assert control.normalized_analysis_minimum_positive_singular_value == pytest.approx(
        1 / math.sqrt(2)
    )
    assert not control.coefficient_architecture_strictly_suboptimal_for_instance


def test_orthogonal_frame_exposes_oracle_scale_but_has_known_direct_bypass() -> None:
    control = audit_orthogonal_flat_frame(8)
    assert control.exact_control_verified
    assert control.dense_gram_operator_norm == pytest.approx(1.0)
    assert control.direct_instance_normalization_lower_bound == pytest.approx(1.0)
    assert control.coefficient_only_linear_normalization == 8
    assert control.normalized_gram_minimum_positive_eigenvalue == pytest.approx(1 / 8)
    assert control.normalized_analysis_minimum_positive_singular_value == pytest.approx(
        1 / math.sqrt(8)
    )
    assert control.coefficient_architecture_strictly_suboptimal_for_instance
    assert control.known_structure_specific_polar_bypass


def test_factorial_orientation_width_survives_table_free_preparation() -> None:
    row = linear_assembly_scaling_record(512)
    assert row.information_threshold_copy_count > 10_000
    assert row.pair_address_qubit_count == 2 * row.information_threshold_copy_count
    assert row.pair_address_hadamard_count == row.pair_address_qubit_count
    assert row.addressed_entry_query_normalization == 1.0
    assert (
        row.dense_linear_assembly_normalization_log2
        == row.information_threshold_copy_count
    )
    assert row.flat_frame_normalized_gram_eigenvalue_log2 == -row.orientation_count_log2
    assert row.coefficient_only_flat_frame_amplification_superpolynomial
    assert row.uniform_pair_prepare_gate_count_polynomial
    assert not row.orientation_pair_table_enumerated
    assert not row.natural_q_scale_retained_spectral_window_proved
    assert not row.hierarchical_or_direct_global_polar_ruled_out


def test_report_closes_only_linear_equal_coefficient_assembly() -> None:
    report = run_linear_assembly_normalization_boundary()
    assert report.theorem.theorem_verified
    assert report.claim_gate["addressed_raw_cross_map_entry_query_normalization_one"]
    assert report.claim_gate["uniform_pair_address_prepare_polynomial"]
    assert report.claim_gate["canonical_linear_global_psd_metric_assembly_compiled"]
    assert report.claim_gate["canonical_linear_global_metric_normalization_is_q"]
    assert report.claim_gate[
        "linear_equal_coefficient_dense_assembly_alpha_lower_bound_q"
    ]
    assert not report.claim_gate["orientation_pair_table_required"]
    assert not report.claim_gate[
        "linear_dense_assembly_polynomial_normalization_proved"
    ]
    assert not report.claim_gate[
        "natural_retained_spectrum_at_q_over_polynomial_scale_proved"
    ]
    assert not report.claim_gate["nonlinear_hierarchical_metric_assembly_ruled_out"]
    assert not report.claim_gate[
        "representation_specific_direct_global_polar_ruled_out"
    ]
    assert not report.claim_gate["physical_pgm_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_and_scoped_negative_result(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    payload = write_linear_assembly_normalization_boundary_report()
    artifact = json.loads(
        (
            tmp_path
            / "research/representation/"
            "self_dual_wreath_addressed_cross_map_linear_assembly_normalization_boundary.json"
        ).read_text(encoding="utf-8")
    )
    assert artifact["status"] == payload["status"]
    negatives = {row["id"]: row for row in load_negative_results()}
    negative = negatives[
        "SCHUR-COMPANION-ALPHA-ONE-ENTRY-QUERY-NO-ALPHA-ONE-DENSE-ASSEMBLY"
    ]
    assert negative["evidence"]["addressed_entry_query_normalization"] == 1.0
    assert negative["evidence"]["linear_dense_assembly_normalization"] == "q"
    assert not negative["evidence"]["natural_q_scale_retained_window_proved"]
    assert not negative["evidence"]["hierarchical_or_direct_global_polar_ruled_out"]
    assert not negative["evidence"]["speedup_claim_allowed"]
