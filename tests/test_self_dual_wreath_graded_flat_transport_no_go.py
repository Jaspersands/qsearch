import pytest

from self_dual_wreath_graded_flat_transport_no_go import (
    audit_flat_transport_grading,
    exact_flat_transport_formulas,
    flat_transport_scaling_record,
    run_graded_flat_transport_no_go,
)


@pytest.mark.parametrize("width", [2, 3, 4, 6, 8, 12])
def test_flat_groupoid_has_constant_metric_but_closing_graded_gap(
    width: int,
) -> None:
    gamma = 1 / 5
    record = audit_flat_transport_grading(width, gamma)
    metric, defect, gap = exact_flat_transport_formulas(width, gamma)

    assert record.observed_metric_minimum_eigenvalue == pytest.approx(metric)
    assert record.observed_grading_defect_norm == pytest.approx(defect)
    assert record.observed_endpoint_gap == pytest.approx(gap)
    assert metric == pytest.approx(8 / 5)
    assert record.flat_vertex_groupoid_verified
    assert record.exact_audit


def test_natural_width_model_is_far_below_inverse_polynomial_gap() -> None:
    record = flat_transport_scaling_record(48)

    assert record.metric_floor > 1.9
    assert record.log2_endpoint_gap < -190
    assert not record.endpoint_gap_inverse_polynomial


def test_report_rejects_metric_to_grading_inference() -> None:
    report = run_graded_flat_transport_no_go()

    assert report.claim_gate["flat_transport_spectrum_proved"]
    assert not report.claim_gate[
        "constant_metric_floor_sufficient_for_endpoint_gap"
    ]
    assert not report.claim_gate[
        "flat_vertex_groupoid_sufficient_for_endpoint_gap"
    ]
    assert not report.claim_gate[
        "natural_width_unquotiented_endpoint_gap_inverse_polynomial"
    ]
    assert not report.claim_gate[
        "internal_cech_row_column_mode_elimination_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
