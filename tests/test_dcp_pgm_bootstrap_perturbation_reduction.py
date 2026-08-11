import pytest

from dcp_pgm_bootstrap_perturbation_reduction import (
    amplification_query_upper_bound,
    audit_hybrid_telescoping_bound,
    perturbation_scaling_record,
    pgm_bootstrap_perturbation_theorem,
    run_pgm_bootstrap_perturbation_reduction,
    sufficient_dilation_error,
)


def test_amplification_query_and_precision_contracts() -> None:
    queries = amplification_query_upper_bound(1 / 64, 1e-4)
    returned_queries, delta = sufficient_dilation_error(1 / 64, 1e-4)
    assert returned_queries == queries
    assert delta == pytest.approx(1e-4 / (8 * (queries + 1)))
    with pytest.raises(ValueError, match="success"):
        amplification_query_upper_bound(0, 1e-4)
    with pytest.raises(ValueError, match="target"):
        amplification_query_upper_bound(0.5, 1.0)


def test_hybrid_telescoping_bound_holds_for_unitary_products() -> None:
    for dimension, queries in ((3, 2), (4, 5), (5, 12)):
        control = audit_hybrid_telescoping_bound(
            dimension,
            queries,
            perturbation_scale=1e-3,
            seed=dimension * 100 + queries,
        )
        assert control.exact_product_unitarity_residual < 1e-10
        assert control.approximate_product_unitarity_residual < 1e-10
        assert control.product_operator_error <= control.hybrid_error_upper_bound + 1e-10
        assert control.hybrid_bound_verified


def test_inverse_polynomial_precision_preserves_canonicalization() -> None:
    row = perturbation_scaling_record(
        n_bits=512,
        pgm_success_power=12,
        target_error_power=16,
    )
    assert row.polynomial_query_complexity
    assert row.inverse_polynomial_precision_sufficient
    assert row.canonicalization_error_upper_bound < (
        row.target_canonicalization_error / 2
    )
    assert row.status == "operator-norm-approximate-pgm-bootstrap-polynomial"


def test_theorem_does_not_promote_outcome_only_closeness() -> None:
    theorem = pgm_bootstrap_perturbation_theorem()
    assert theorem.operator_norm_approximate_accessible_pgm_reduced
    assert not theorem.classical_outcome_distribution_closeness_reduced
    assert not theorem.average_state_error_reduced
    assert not theorem.inaccessible_environment_recovered
    assert not theorem.arbitrary_collective_povm_reduced


def test_report_keeps_weaker_approximation_contracts_open() -> None:
    report = run_pgm_bootstrap_perturbation_reduction()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["polynomial_resource_scaling_row_count"] == report.headline_metrics[
        "scaling_row_count"
    ]
    assert report.claim_gate[
        "operator_norm_approximate_accessible_pgm_route_is_solver_equivalent"
    ]
    assert not report.claim_gate["finite_precision_standard_circuit_loophole_alive"]
    assert not report.claim_gate["outcome_distribution_only_approximation_route_closed"]
    assert not report.claim_gate["non_pgm_collective_measurement_route_closed"]
    assert not report.claim_gate["speedup_claim_allowed"]
