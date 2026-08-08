import math

import numpy as np

from self_dual_wreath_pair_transport_native_mass_boundary import (
    _orthonormal_span,
    fourth_power_carrier_distribution,
    native_pair_transport_scaling_record,
    run_pair_transport_native_mass_boundary,
)


def test_two_projection_active_channel_has_trace_two_even_when_common():
    for correlation in (0.2, 0.5, 1.0):
        left_vector = np.array([[1.0], [0.0]])
        right_vector = np.array(
            [[correlation], [math.sqrt(max(0.0, 1 - correlation**2))]]
        )
        left = left_vector @ left_vector.T
        right = right_vector @ right_vector.T
        active_span = _orthonormal_span(
            np.concatenate((left_vector, right_vector), axis=1),
            1e-10,
        )
        trace = np.trace(active_span.T @ (left + right) @ active_span).real
        assert abs(trace - 2.0) < 1e-10


def test_fourth_power_distribution_is_exactly_normalized_by_z4():
    rows = fourth_power_carrier_distribution(8)
    total = sum(weight for _, weight in rows)
    assert total > 0
    assert abs(sum(weight / total for _, weight in rows) - 1.0) < 1e-12


def test_native_trace_controls_match_pair_angle_multiplicities():
    report = run_pair_transport_native_mass_boundary()
    assert report.finite_controls
    assert all(
        row.exact_native_trace_multiplicity_bridge_verified
        for row in report.finite_controls
    )
    assert all(
        abs(
            row.observed_active_pair_frame_trace
            - row.predicted_active_pair_frame_trace
        )
        < 1e-8
        for row in report.finite_controls
    )


def test_natural_mass_makes_cheap_cross_transport_negligible():
    early = native_pair_transport_scaling_record(12)
    late = native_pair_transport_scaling_record(48)
    assert late.quadratic_dimension_mass < early.quadratic_dimension_mass
    assert late.mass_at_or_below_theorem_threshold <= 0.5 + 1e-12
    assert (
        late.branchwise_expected_bernstein_degree_lower_bound_log2
        > late.polynomial_degree_benchmark_log2
    )
    assert late.branchwise_average_degree_superpolynomial_signal


def test_claims_remain_scoped_to_normalized_active_pair_transport():
    report = run_pair_transport_native_mass_boundary()
    gate = report.claim_gate
    assert gate["conditional_active_pair_native_mass_bridge_proved"]
    assert gate["natural_q4_law_is_conditional_native_pair_mass_proved"]
    assert gate["stacked_pair_polar_sampler_remains_polynomial"]
    assert not gate["direct_representation_specific_transport_ruled_out"]
    assert not gate["complete_many_orientation_pgm_mass_transfer_proved"]
    assert not gate["arbitrary_quantum_circuit_lower_bound_proved"]
    assert not gate["speedup_claim_allowed"]
