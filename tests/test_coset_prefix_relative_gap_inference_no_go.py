import math

import numpy as np
import pytest

from coset_prefix_relative_gap_inference_no_go import (
    audit_prefix_gap_counterfamily,
    build_coset_prefix_relative_gap_inference_report,
    prefix_gap_counterfamily_matrices,
    prefix_gap_scaling_record,
    write_coset_prefix_relative_gap_inference_report,
)


def test_counterfamily_embedding_and_projectors_are_explicit():
    embedding, projectors, direct = prefix_gap_counterfamily_matrices(3, 0.1)
    assert embedding.shape == direct.shape == (24, 3)
    assert len(projectors) == 3
    assert np.linalg.norm(embedding.conj().T @ embedding - np.eye(3)) < 1e-10
    for projector in projectors:
        assert np.linalg.norm(projector @ projector - projector) < 1e-10
    with pytest.raises(ValueError, match="delta"):
        prefix_gap_counterfamily_matrices(2, 1.0)


def test_every_order_has_bad_relative_edge_despite_final_condition_one():
    delta = 0.01
    row = audit_prefix_gap_counterfamily(4, delta)
    assert row.control_verified
    assert row.tested_ordering_count == row.expected_ordering_count == 24
    assert row.final_metric_condition_number == pytest.approx(1.0)
    assert row.final_metric_scalar_residual < 1e-10
    assert row.determinant_telescoping_residual < 1e-10
    assert row.minimum_relative_effect_eigenvalue == pytest.approx(delta)
    assert row.maximum_relative_effect_eigenvalue == pytest.approx(1.0)
    assert row.every_order_has_delta_relative_edge


def test_bad_relative_qsvt_gap_coexists_with_trivial_direct_polar():
    row = audit_prefix_gap_counterfamily(5, 0.002)
    assert row.all_holonomies_identity
    assert row.maximum_holonomy_identity_distance < 1e-8
    assert row.direct_structured_polar_constructed
    assert row.maximum_direct_step_polar_residual < 1e-8
    assert row.final_direct_polar_residual < 1e-8


def test_scaling_keeps_both_algorithm_and_lower_bound_inferences_false():
    row = prefix_gap_scaling_record(256)
    assert row.delta == pytest.approx(math.exp(-16))
    assert row.final_condition_number == 1.0
    assert not row.inverse_polynomial_relative_gap_inferred
    assert not row.generic_qsvt_hardness_implies_circuit_hardness


def test_report_requires_natural_recoupling_structure(tmp_path):
    report = build_coset_prefix_relative_gap_inference_report()
    assert report.theorem.theorem_verified
    assert report.theorem.loewner_monotonicity_proved
    assert report.theorem.determinant_telescoping_proved
    assert not report.theorem.final_constant_condition_implies_polynomial_relative_gaps
    assert not report.theorem.adaptive_ordering_always_repairs_relative_gaps
    assert not report.theorem.small_relative_gap_implies_circuit_hardness
    assert report.theorem.exact_direct_counterfamily_polar_constructed
    assert not report.theorem.natural_coset_source_counterfamily_proved
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_coset_prefix_relative_gap_inference_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "final-spectrum-and-determinant-prefix-gap-inference-refuted"
    )
