import pytest

from self_dual_wreath_internal_closure_graded_rescue import (
    audit_internal_closure,
    exact_internal_closure_formulas,
    internal_closure_scaling_record,
    run_internal_closure_graded_rescue,
)


@pytest.mark.parametrize("gamma", [1 / 5, 1 / 9])
@pytest.mark.parametrize("width", [2, 3, 4, 6, 8])
def test_complete_internal_channel_has_exact_quarter_gap_bound(
    gamma: float,
    width: int,
) -> None:
    record = audit_internal_closure(width, gamma)
    cycle, row, constant, defect, gap = exact_internal_closure_formulas(
        width,
        gamma,
    )

    assert record.observed_cycle_metric == pytest.approx(cycle)
    assert record.observed_row_metric == pytest.approx(row)
    assert record.observed_constant_metric == pytest.approx(constant)
    assert record.observed_grading_defect_norm == pytest.approx(defect)
    assert record.observed_endpoint_gap == pytest.approx(gap)
    assert record.endpoint_gap_at_least_one_quarter
    assert record.exact_audit


def test_natural_width_complete_channel_converges_to_quarter_gap() -> None:
    record = internal_closure_scaling_record(256)

    assert record.metric_floor > 1.99
    assert record.grading_defect_norm == pytest.approx(0.5)
    assert record.endpoint_gap == pytest.approx(0.25)
    assert record.endpoint_gap_at_least_one_quarter


def test_report_rescues_flat_model_but_keeps_natural_gate_closed() -> None:
    report = run_internal_closure_graded_rescue()

    assert report.claim_gate[
        "complete_internal_flat_channel_spectrum_proved"
    ]
    assert report.claim_gate[
        "complete_internal_flat_channel_endpoint_gap_at_least_quarter"
    ]
    assert not report.claim_gate[
        "crossing_only_flat_no_go_survives_complete_internal_closure"
    ]
    assert not report.claim_gate[
        "natural_global_affine_channel_closure_proved"
    ]
    assert not report.claim_gate["natural_pgm_endpoint_gap_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
