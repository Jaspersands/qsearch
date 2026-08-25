from __future__ import annotations

import json

import numpy as np
import pytest

from research_registry import initialize_seed_registry, load_negative_results
from self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary import (
    audit_addressed_cross_map_oracle,
    audit_pair_polar_global_gram_boundary,
    cross_map_oracle_scaling,
    phase_only_pair_polar_kernel,
    projector_lcu_unitary,
    run_addressed_cross_map_pair_polar_gram_boundary,
    s3_pair_data,
    tensor_phase_only_boundary_record,
    write_addressed_cross_map_pair_polar_gram_boundary_report,
)


def test_projector_reflection_lcu_has_alpha_one_signal_block() -> None:
    reflections, projectors, _ = s3_pair_data()
    for reflection, projector in zip(reflections, projectors):
        lcu = projector_lcu_unitary(reflection)
        dimension = len(reflection)
        np.testing.assert_allclose(
            lcu.conj().T @ lcu,
            np.eye(2 * dimension),
            atol=1e-10,
        )
        np.testing.assert_allclose(
            lcu[:dimension, :dimension],
            projector,
            atol=1e-10,
        )


def test_physical_interface_sandwich_is_exact_addressed_cross_map() -> None:
    control = audit_addressed_cross_map_oracle()
    assert control.exact_addressed_cross_map_oracle_verified
    assert control.ordered_pair_query_count == 9
    assert control.addressed_cross_map_block_encoding_normalization == 1.0
    assert control.maximum_projector_lcu_unitarity_residual < 1e-9
    assert control.maximum_projector_signal_block_residual < 1e-9
    assert control.maximum_decoded_cross_map_residual < 1e-9
    assert control.maximum_pair_polar_unitarity_residual < 1e-9


def test_phase_only_pair_polar_kernel_is_indefinite_on_s3_holonomy() -> None:
    control = audit_pair_polar_global_gram_boundary()
    assert control.exact_metric_retention_boundary_verified
    assert control.physical_gram_rank == 5
    assert control.physical_gram_minimum_eigenvalue > -1e-9
    assert control.physical_gram_minimum_positive_eigenvalue == pytest.approx(1.5)
    assert control.phase_only_kernel_minimum_eigenvalue == pytest.approx(-1.0)
    assert control.phase_only_kernel_negative_eigenvalue_count == 2
    assert control.phase_only_kernel_zero_eigenvalue_count == 2
    assert not control.phase_only_kernel_positive_semidefinite
    assert control.minimum_nontrivial_pair_correlation == pytest.approx(0.5)
    assert control.maximum_nontrivial_pair_correlation == pytest.approx(0.5)


def test_phase_only_kernel_has_the_exact_holonomy_spectrum() -> None:
    reflections, _, bases = s3_pair_data()
    kernel = phase_only_pair_polar_kernel(reflections, bases)
    values = np.linalg.eigvalsh((kernel + kernel.conj().T) / 2.0)
    np.testing.assert_allclose(
        values,
        [-1, -1, 0, 0, 2, 2, 2, 2, 3],
        atol=1e-9,
    )


def test_uniform_pair_query_uses_masks_not_exponential_table() -> None:
    row = cross_map_oracle_scaling(512)
    assert row.information_threshold_copy_count > 10_000
    assert row.orientation_pair_count_expression.startswith("2^")
    assert row.source_factor_mask_controls == 2 * row.information_threshold_copy_count
    assert row.addressed_raw_cross_map_normalization == 1.0
    assert not row.orientation_pair_table_enumerated
    assert row.uniform_coherent_pair_query_polynomial
    assert row.direct_gpe_pair_polar_polynomial
    assert not row.full_address_transition_gram_normalization_one_proved
    assert not row.complete_orientation_polar_polynomial


def test_tensor_phase_only_negativity_is_extensive_but_not_natural_mass() -> None:
    row = tensor_phase_only_boundary_record(64)
    total = int(row.phase_only_kernel_dimension_decimal)
    negative = int(row.phase_only_negative_eigenvalue_count_decimal)
    assert row.fixed_point_free_embedding
    assert row.phase_only_minimum_eigenvalue == -1.0
    assert negative / total == pytest.approx(row.phase_only_negative_eigenvalue_fraction)
    assert 0.16 < row.phase_only_negative_eigenvalue_fraction < 0.17
    assert not row.positive_natural_plancherel_mass_proved


def test_report_corrects_raw_access_and_kills_only_phase_only_global_gram() -> None:
    report = run_addressed_cross_map_pair_polar_gram_boundary()
    assert report.theorem.theorem_verified
    assert report.claim_gate[
        "physical_schur_interface_supplies_addressed_raw_cross_map_block_encoding"
    ]
    assert report.claim_gate[
        "addressed_raw_cross_map_block_encoding_normalization_one"
    ]
    assert report.claim_gate["direct_gpe_pair_polar_compiled"]
    assert report.claim_gate["phase_only_pair_polar_global_gram_ansatz_refuted"]
    assert report.claim_gate["operator_valued_cross_metric_retention_required"]
    assert not report.claim_gate[
        "phase_only_pair_polar_block_kernel_positive_semidefinite"
    ]
    assert not report.claim_gate[
        "global_address_transition_kernel_polynomial_normalization_proved"
    ]
    assert not report.claim_gate["positive_natural_mass_holonomy_metric_event_proved"]
    assert not report.claim_gate["physical_pgm_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_and_precise_negative_result(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    payload = write_addressed_cross_map_pair_polar_gram_boundary_report()
    artifact = json.loads(
        (
            tmp_path
            / "research/representation/"
            "self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary.json"
        ).read_text(encoding="utf-8")
    )
    assert artifact["status"] == payload["status"]
    negatives = {row["id"]: row for row in load_negative_results()}
    negative = negatives[
        "SCHUR-COMPANION-PHASE-ONLY-PAIR-POLAR-GRAM-NO-GLOBAL-POLAR"
    ]
    assert negative["evidence"]["addressed_raw_cross_map_normalization"] == 1.0
    assert negative["evidence"]["finite_phase_only_negative_eigenvalue_count"] == 2
    assert not negative["evidence"]["speedup_claim_allowed"]
