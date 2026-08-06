import pytest

from self_dual_wreath_reciprocal_carrier_accumulation_no_go import (
    reciprocal_carrier_accumulation_control,
    run_reciprocal_carrier_accumulation_no_go,
)


@pytest.mark.parametrize("carrier_dimension", [2, 3, 4, 5])
def test_reciprocal_pair_angles_accumulate_at_quadratic_width(
    carrier_dimension: int,
) -> None:
    control = reciprocal_carrier_accumulation_control(carrier_dimension)
    width = carrier_dimension**2

    assert control.child_width == width
    assert control.exact_cross_correlation_magnitude == 1 / carrier_dimension
    assert control.maximum_cross_correlation_magnitude_residual < 1e-10
    assert control.crossing_pair_common_dimension == 0
    assert control.child_span_intersection_dimension == width
    assert control.augmented_h0_dimension == width
    assert control.exact_residual_principal_correlation > 1 - 1e-10
    assert control.absolute_weight_cross_norm == pytest.approx(carrier_dimension)
    assert control.emergent_dependency_despite_reciprocal_bound
    assert control.exact_accumulation_no_go_audit


def test_report_kills_magnitude_only_all_depth_proof() -> None:
    report = run_reciprocal_carrier_accumulation_no_go()

    assert report.headline_metrics[
        "reciprocal_carrier_accumulation_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "quadratic_width_reciprocal_bound_counterexample_count"
    ] == 4
    assert not report.claim_gate[
        "pairwise_reciprocal_magnitude_sufficient_for_pair_generation"
    ]
    assert report.claim_gate["quadratic_width_accumulation_counterfamily_verified"]
    assert report.claim_gate["signed_racah_structure_required"]
    assert not report.claim_gate[
        "natural_wreath_fourier_like_accumulation_excluded"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
