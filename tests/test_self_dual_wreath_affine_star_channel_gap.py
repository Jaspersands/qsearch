import pytest

from self_dual_wreath_affine_star_channel_gap import (
    affine_star_scaling_record,
    audit_affine_star_gap,
    exact_affine_star_defects,
    run_affine_star_channel_gap,
)


@pytest.mark.parametrize("gamma", [1 / 5, 1 / 9, 1 / 10])
@pytest.mark.parametrize("width", [2, 3, 4, 8, 16, 32])
def test_affine_star_exact_formula_and_uniform_gap(
    gamma: float,
    width: int,
) -> None:
    record = audit_affine_star_gap(width, gamma)
    _orthogonal, _constant, defect, gap = exact_affine_star_defects(
        width,
        gamma,
    )

    assert record.observed_grading_defect_norm == pytest.approx(defect)
    assert record.observed_endpoint_gap == pytest.approx(gap)
    assert record.uniform_bound_respected
    assert record.uniform_endpoint_gap_lower_bound > 0.25
    assert record.exact_audit


def test_w6_plane_star_defects_are_exact() -> None:
    assert audit_affine_star_gap(2, 1 / 9).observed_grading_defect_norm == pytest.approx(
        1 / 17
    )
    assert audit_affine_star_gap(2, 1 / 5).observed_grading_defect_norm == pytest.approx(
        1 / 9
    )
    assert audit_affine_star_gap(2, 1 / 10).observed_grading_defect_norm == pytest.approx(
        1 / 19
    )


def test_natural_width_affine_star_stays_above_quarter() -> None:
    record = affine_star_scaling_record(256)

    assert record.endpoint_gap > 0.25
    assert record.endpoint_gap >= record.uniform_endpoint_gap_lower_bound
    assert record.endpoint_gap_above_quarter


def test_report_keeps_channel_classification_gate_open() -> None:
    report = run_affine_star_channel_gap()

    assert report.claim_gate["affine_star_exact_defect_formula_proved"]
    assert report.claim_gate[
        "affine_star_endpoint_gap_uniformly_above_quarter"
    ]
    assert report.claim_gate["extracted_w6_star_defects_explained"]
    assert not report.claim_gate["all_affine_channel_graphs_safe"]
    assert not report.claim_gate[
        "natural_residual_channels_classified_as_affine_stars"
    ]
    assert not report.claim_gate["natural_pgm_endpoint_gap_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
