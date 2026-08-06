import pytest

from self_dual_wreath_pair_transport_degree_obstruction import (
    pair_transport_degree_control,
    pair_transport_degree_scaling_record,
    polar_sign_degree_lower_bound,
    run_pair_transport_degree_obstruction,
)


def test_polar_sign_degree_bound_scales_inverse_with_correlation() -> None:
    error = 0.01
    assert polar_sign_degree_lower_bound(0.5, error) == pytest.approx(
        (1 - error) * 3**0.5
    )
    assert polar_sign_degree_lower_bound(0.01, error) > 98
    assert polar_sign_degree_lower_bound(0.001, error) > 989


def test_wreath_specialization_is_linear_in_carrier_dimension() -> None:
    record = pair_transport_degree_control("carrier", 1_000_000)

    assert record.exact_analytic_control
    assert record.principal_correlation == 1e-6
    assert record.bernstein_degree_lower_bound > 989_999
    assert record.lower_bound_to_dimension_ratio == pytest.approx(0.99)


def test_worst_available_carrier_bound_becomes_superpolynomial() -> None:
    small = pair_transport_degree_scaling_record(16)
    large = pair_transport_degree_scaling_record(512)

    assert large.log2_maximum_irrep_dimension_lower_bound > (
        small.log2_maximum_irrep_dimension_lower_bound
    )
    assert large.worst_available_transport_degree_superpolynomial
    assert large.log2_worst_available_pair_transport_degree_lower_bound > (
        large.polynomial_degree_benchmark_log2
    )
    assert not large.candidate_fiber_uses_worst_carrier_proved
    assert not large.explicit_recoupling_bypass_ruled_out


def test_report_preserves_access_model_scope() -> None:
    report = run_pair_transport_degree_obstruction()

    assert report.claim_gate[
        "pair_overlap_polar_qsvt_degree_lower_bound_proved"
    ]
    assert report.claim_gate["superpolynomial_dimension_carriers_exist"]
    assert not report.claim_gate[
        "candidate_fiber_uses_high_dimension_carriers_proved"
    ]
    assert not report.claim_gate["explicit_recoupling_bypass_ruled_out"]
    assert not report.claim_gate[
        "general_pair_transport_circuit_lower_bound_proved"
    ]
    assert not report.claim_gate["hierarchical_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
