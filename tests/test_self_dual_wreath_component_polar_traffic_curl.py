from fractions import Fraction

from self_dual_wreath_component_commutator_haar_benchmark import (
    haar_normalized_commutator_trace,
)
from self_dual_wreath_component_polar_traffic_curl import (
    _random_synthesis,
    audit_polar_ridge_stability,
    natural_polar_curl_limit,
    polar_traffic_curl_theorem,
    run_component_polar_traffic_curl,
    sparse_polar_limit_record,
)


def test_polar_ridge_tail_identity_and_curl_stability() -> None:
    synthesis = _random_synthesis(8, 16, seed=14001)
    coarse = audit_polar_ridge_stability("COARSE", synthesis, 4, 1e-1)
    fine = audit_polar_ridge_stability("FINE", synthesis, 4, 1e-3)

    assert coarse.exact_tail_identity_verified
    assert fine.exact_tail_identity_verified
    assert coarse.curl_stability_verified
    assert fine.curl_stability_verified
    assert fine.support_ridge_error_squared < coarse.support_ridge_error_squared
    assert fine.normalized_curl_difference < coarse.normalized_curl_difference


def test_sparse_polar_limit_matches_haar_asymptotic_formula() -> None:
    for alpha in (2.0, 2.5, 3.0, 4.0):
        gamma = 1.0 / alpha
        assert abs(natural_polar_curl_limit(alpha) - gamma**2 * (1 - gamma)) < 1e-15
        row = sparse_polar_limit_record(alpha)
        assert row.positive_limit
        assert row.sparse_haar_polar_curl_limit >= 3 / 64 - 1e-12


def test_exact_haar_formula_converges_to_sparse_limit() -> None:
    errors = []
    for scale in (1, 2, 4, 8):
        ambient = 100 * scale
        fiber = 50 * scale
        block = 1
        exact = float(haar_normalized_commutator_trace(ambient, fiber, block))
        errors.append(abs(exact - Fraction(1, 8)))

    assert errors[-1] < errors[0]
    assert errors[-1] < 2e-3


def test_theorem_proves_signal_but_not_algorithm_or_speedup() -> None:
    theorem = polar_traffic_curl_theorem()
    report = run_component_polar_traffic_curl()

    assert theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["polar_functional_calculus_transfer_proved"]
    assert report.claim_gate["natural_exact_dependency_component_M4_positive"]
    assert report.claim_gate["global_distinct_positive_component_M4"]
    assert not report.claim_gate["coherent_component_measurement_compiled"]
    assert not report.claim_gate["decoder_information_gain_proved"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
