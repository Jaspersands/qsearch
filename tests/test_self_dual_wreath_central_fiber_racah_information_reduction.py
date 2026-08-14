import math

from self_dual_wreath_central_fiber_racah_information_reduction import (
    audit_central_fiber_racah_information,
    cross_swapped_fiber_countermodel,
    run_central_fiber_racah_information_reduction,
)


def test_natural_racah_central_fiber_information_chain_is_exact() -> None:
    row = audit_central_fiber_racah_information(5, 2)
    assert row.exact_information_decomposition_residual_bits < 1e-9
    assert row.maximum_intermediate_plancherel_marginal_residual < 1e-9
    assert row.physical_average_fiber_resolution_debt_bits >= -1e-9
    assert row.exact_central_fiber_reduction_verified


def test_finer_central_features_reduce_resolution_debt() -> None:
    coarse = audit_central_fiber_racah_information(5, 2)
    fine = audit_central_fiber_racah_information(5, 3)
    assert fine.plancherel_hidden_entropy_bits <= coarse.plancherel_hidden_entropy_bits
    assert fine.physical_average_fiber_resolution_debt_bits <= (
        coarse.physical_average_fiber_resolution_debt_bits + 1e-9
    )


def test_cross_swapped_model_saturates_both_hidden_entropy_terms() -> None:
    row = cross_swapped_fiber_countermodel(8)
    assert math.isclose(row.full_label_mutual_information_bits, 6.0, abs_tol=1e-12)
    assert row.visible_feature_mutual_information_bits == 0.0
    assert row.joint_hidden_entropy_bits == 0.0
    assert abs(row.entropy_budget_slack_bits) < 1e-12
    assert row.exact_two_fiber_budget_saturation_verified


def test_report_keeps_both_natural_racah_obligations_open() -> None:
    report = run_central_fiber_racah_information_reduction()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["exact_information_decomposition_proved"] is True
    assert report.claim_gate["fixed_degree_free_probability_closes_rank_mi"] is False
    assert report.claim_gate["natural_racah_rank_mi_vanishes_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
