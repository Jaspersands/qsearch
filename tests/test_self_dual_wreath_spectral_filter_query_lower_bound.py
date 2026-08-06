import math

import numpy as np

from self_dual_wreath_spectral_filter_query_lower_bound import (
    audit_search_projector_encoding,
    query_lower_bound_scaling_record,
    run_spectral_filter_query_lower_bound,
    search_projectors,
)


def test_search_projectors_have_equal_rank_and_exact_average() -> None:
    bits = (0, 1, 0, 0, 1, 0, 0, 0)
    projectors = search_projectors(bits)
    assert all(round(float(np.trace(projector))) == 1 for projector in projectors)
    frame = sum(projectors) / len(projectors)
    assert np.allclose(frame, np.diag([0.75, 0.25]))


def test_reflection_oracle_is_exact_phase_search_oracle() -> None:
    control = audit_search_projector_encoding(64, 8)
    assert control.equal_rank_search_reduction_verified
    assert control.maximum_reflection_phase_oracle_residual == 0
    assert control.marked_fraction_eigenvalue == 1 / 8
    assert control.marked_fraction_eigenvalue >= control.rejection_threshold


def test_factorial_query_lower_bound_dominates_every_fixed_polynomial() -> None:
    record = query_lower_bound_scaling_record(512, polynomial_degree=100)
    assert record.quantum_query_lower_bound_log2_without_constant > 1900
    assert record.black_box_lower_bound_superpolynomial
    assert math.isclose(
        record.quantum_query_lower_bound_log2_without_constant,
        0.5 * (record.log2_hidden_label_count - 3),
    )


def test_report_closes_only_generic_oracle_implementation() -> None:
    report = run_spectral_filter_query_lower_bound()
    assert report.claim_gate[
        "generic_indexed_projector_filter_requires_superpolynomial_queries"
    ]
    assert not report.claim_gate["representation_structured_filter_ruled_out"]
    assert not report.claim_gate["general_wreath_circuit_lower_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
