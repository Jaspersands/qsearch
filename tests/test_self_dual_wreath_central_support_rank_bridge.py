from fractions import Fraction

from self_dual_wreath_central_support_rank_bridge import (
    audit_global_covariance_multiplicity,
    collision_free_s4_rank_bridge_control,
    polynomial_rank_bridge_scaling_record,
    relative_rank_bridge_control,
    run_central_support_rank_bridge,
)


def test_relative_rank_bridge_is_exact() -> None:
    control = relative_rank_bridge_control(
        "synthetic",
        Fraction(1, 4),
        Fraction(1, 20),
        Fraction(1, 10),
    )
    assert control.rank_bridge_probability_upper_bound == "1/2"
    assert control.bridge_slack == "1/4"
    assert control.exact_rank_bridge_inequality_verified


def test_collision_free_s4_control_obeys_rank_bridge() -> None:
    control = collision_free_s4_rank_bridge_control()
    assert control.bad_block_probability == "54/89"
    assert control.scalar_bad_spectral_mass == "10/267"
    assert control.minimum_nonzero_bad_projection_relative_rank == "1/18"
    assert control.rank_bridge_probability_upper_bound == "60/89"
    assert control.bridge_slack == "6/89"
    assert control.exact_rank_bridge_inequality_verified


def test_polynomial_rank_floor_reduces_degree_to_log_group_scale() -> None:
    record = polynomial_rank_bridge_scaling_record(48, 1)
    assert record.selected_copy_count == 205
    assert record.upper_edge_minimum_degree == 167
    assert record.lower_edge_minimum_degree == 921
    assert record.degree_is_order_log_group
    assert not record.natural_relative_rank_bound_proved


def test_global_covariance_does_not_force_relative_rank_floor() -> None:
    control = audit_global_covariance_multiplicity()
    assert control.carrier_dimension == 54
    assert control.globally_distinct_source_partitions
    assert control.maximum_global_diagonal_commutator_norm < 1e-12
    assert control.trivial_isotypic_multiplicity == 2
    assert control.sign_isotypic_multiplicity == 2
    assert control.rank_one_commutant_projection_relative_rank == "1/54"
    assert control.inverse_group_order == "1/24"
    assert not control.global_covariance_forces_inverse_group_relative_rank
    assert control.exact_global_covariance_verified


def test_report_keeps_natural_rank_and_edge_gates_closed() -> None:
    report = run_central_support_rank_bridge()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["relative_rank_central_support_bridge_proved"]
    assert not report.claim_gate[
        "natural_bad_projection_polynomial_relative_rank_proved"
    ]
    assert not report.claim_gate["center_valued_local_law_proved"]
    assert not report.claim_gate["natural_all_depth_frame_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
