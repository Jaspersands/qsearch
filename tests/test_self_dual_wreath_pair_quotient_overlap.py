import math

from self_dual_wreath_pair_quotient_overlap import (
    _controls,
    audit_s6_pair_quotient_portfolio,
    run_pair_quotient_overlap,
)


def test_pair_quotient_recovers_w3_emergent_boundaries() -> None:
    distinct, repeated, _, _ = _controls()

    assert distinct.crossing_pair_core_span_dimension == 0
    assert distinct.emergent_cross_dependency_dimension == 2
    assert distinct.exact_residual_principal_correlation > 1 - 1e-10
    assert not distinct.exact_pair_quotient_certifies_pair_generation
    assert repeated.emergent_cross_dependency_dimension == 1
    assert repeated.exact_residual_principal_correlation > 1 - 1e-10
    assert distinct.exact_pair_quotient_overlap_audit
    assert repeated.exact_pair_quotient_overlap_audit


def test_pair_rich_w5_node_has_positive_exact_quotient_gap() -> None:
    control = _controls()[2]

    assert control.crossing_pair_core_span_dimension == 5
    assert control.child_intersection_dimension == 5
    assert control.emergent_cross_dependency_dimension == 0
    assert control.exact_pair_quotient_gap_below_one > 0.65
    assert control.residual_sign_blind_bound_certifies_pair_generation
    assert control.exact_pair_quotient_certifies_pair_generation


def test_phase_sensitive_quotient_succeeds_when_scalar_bound_is_infinite() -> None:
    control = _controls()[3]

    assert control.emergent_cross_dependency_dimension == 0
    assert control.exact_pair_quotient_gap_below_one > 0.59
    assert math.isinf(control.residual_weighted_span_correlation_bound)
    assert not control.residual_sign_blind_bound_certifies_pair_generation
    assert control.exact_pair_quotient_certifies_pair_generation
    assert control.exact_pair_quotient_overlap_audit


def test_report_keeps_uniform_quotient_gap_and_circuit_open() -> None:
    report = run_pair_quotient_overlap()

    assert report.headline_metrics["finite_pair_quotient_audit_failure_count"] == 0
    assert report.headline_metrics["finite_phase_only_certificate_count"] == 1
    assert report.claim_gate[
        "exact_pair_core_quotient_overlap_criterion_verified"
    ]
    assert report.claim_gate["finite_phase_only_residual_certificate_exists"]
    assert not report.claim_gate[
        "residual_sign_blind_bound_universally_sufficient"
    ]
    assert not report.claim_gate["uniform_all_n_pair_quotient_gap_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_s6_low_carrier_portfolio_has_positive_exact_residual_gap() -> None:
    screen = audit_s6_pair_quotient_portfolio()

    assert screen.active_target_count == 9
    assert screen.affine_merge_audit_count == 693
    assert screen.emergent_cross_dependency_merge_count == 0
    assert screen.phase_only_certificate_count == 12
    assert screen.minimum_exact_pair_quotient_gap > 0.737
    assert screen.minimum_pair_rich_exact_quotient_gap > 0.79
    assert screen.exact_pair_quotient_audit_failure_count == 0
