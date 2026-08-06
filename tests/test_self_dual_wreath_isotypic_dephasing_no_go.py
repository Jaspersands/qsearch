import numpy as np

from self_dual_wreath_isotypic_dephasing_no_go import (
    audit_partial_trace_domination,
    partial_trace_first,
    run_isotypic_dephasing_no_go,
    symmetric_group_dephasing_record,
)


def test_partial_trace_uses_first_tensor_factor() -> None:
    left = np.diag([0.25, 0.75])
    right = np.diag([0.4, 0.6])
    operator = np.kron(left, right)
    assert np.allclose(partial_trace_first(operator, 2), right)


def test_positive_operator_is_dominated_by_scaled_partial_trace() -> None:
    control = audit_partial_trace_domination(
        4,
        5,
        9,
        control_id="DOMINATION",
        seed=20260806,
    )
    assert control.partial_trace_domination_verified
    assert control.domination_residual < 1e-10


def test_symmetric_group_bound_is_largest_plancherel_atom() -> None:
    record = symmetric_group_dephasing_record(20)
    assert record.exact_dimension_square_sum_verified
    assert record.exact_identification_success_upper_bound == (
        record.maximum_plancherel_atom
    )
    assert record.exact_identification_success_upper_bound < 1 / 16


def test_report_closes_classical_sector_decoders_only() -> None:
    report = run_isotypic_dephasing_no_go()
    assert report.headline_metrics["operator_control_failure_count"] == 0
    assert report.headline_metrics["dimension_square_sum_failure_count"] == 0
    assert report.claim_gate["isotypic_dephasing_identification_no_go_proved"]
    assert report.claim_gate[
        "cross_sector_coherence_required_for_constant_identification"
    ]
    assert not report.claim_gate["coherent_isotypic_transform_ruled_out"]
    assert not report.claim_gate["coherent_cross_sector_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
