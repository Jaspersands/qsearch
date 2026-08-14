import math

from self_dual_wreath_free_probability_projector_resolution_boundary import (
    audit_central_feature_resolution,
    central_class_sum_feature,
    central_feature_vector_count_upper,
    exact_central_feature_count,
    hidden_fiber_countermodel,
    projector_resolution_scaling_record,
    run_free_probability_projector_resolution_boundary,
)


def test_class_sum_features_are_integral_and_obey_range_bound() -> None:
    feature = central_class_sum_feature((4, 2), 3)
    assert all(isinstance(value, int) for value in feature)
    row = audit_central_feature_resolution(8, 3)
    assert row.distinct_feature_vector_count <= row.feature_vector_count_upper
    assert row.maximum_class_sum_integrality_residual == 0
    assert row.feature_count_bound_verified
    assert [exact_central_feature_count(s) for s in (2, 3, 4, 6)] == [1, 2, 4, 10]


def test_feature_entropy_chain_exposes_unresolved_partition_entropy() -> None:
    coarse = audit_central_feature_resolution(12, 2)
    finer = audit_central_feature_resolution(12, 3)
    assert coarse.entropy_chain_residual_bits < 1e-10
    assert finer.entropy_chain_residual_bits < 1e-10
    assert coarse.plancherel_conditional_entropy_bits >= 0
    assert finer.plancherel_conditional_entropy_bits <= (
        coarse.plancherel_conditional_entropy_bits + 1e-10
    )


def test_hidden_fiber_coupling_has_independent_features_and_large_label_mi() -> None:
    row = hidden_fiber_countermodel(4, 16)
    assert row.visible_feature_mutual_information_bits == 0.0
    assert math.isclose(row.full_label_mutual_information_bits, 4.0, abs_tol=1e-12)
    assert row.maximum_visible_joint_independence_residual < 1e-12
    assert row.exact_hidden_fiber_countermodel_verified


def test_fixed_support_feature_capacity_is_sub_sqrt_n_on_scaling_control() -> None:
    early = projector_resolution_scaling_record(100, 3)
    late = projector_resolution_scaling_record(10_000, 3)
    assert late.feature_log_capacity_over_sqrt_n < early.feature_log_capacity_over_sqrt_n
    assert late.support_is_fixed
    assert late.exact_feature_count_identity_verified
    assert late.feature_capacity_can_resolve_plancherel_entropy_proved is False
    assert central_feature_vector_count_upper(20, 3) > 1


def test_report_rejects_fixed_degree_free_probability_shortcut() -> None:
    report = run_free_probability_projector_resolution_boundary()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["fixed_support_central_feature_count_bound_proved"] is True
    assert report.claim_gate[
        "cited_fixed_degree_free_probability_results_reach_projector_resolution"
    ] is False
    assert report.claim_gate["natural_racah_mi_survives_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
