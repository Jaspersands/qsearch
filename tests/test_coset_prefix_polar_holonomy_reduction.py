import math

import numpy as np
import pytest

from coset_prefix_polar_holonomy_reduction import (
    audit_partial_polar_chain_step,
    audit_polar_chain_step,
    build_coset_prefix_polar_holonomy_report,
    fixed_point_free_prefix_control,
    fixed_point_free_rank_loss_control,
    prefix_polar_scaling_record,
    write_coset_prefix_polar_holonomy_report,
)


def test_full_rank_chain_step_rejects_lost_support():
    previous = np.eye(2)
    rank_deficient = np.diag([1.0, 0.0])
    with pytest.raises(ValueError, match="positive definite"):
        audit_polar_chain_step(2, previous, rank_deficient)

    with pytest.raises(ValueError, match="nonempty support"):
        audit_partial_polar_chain_step(previous, np.zeros((2, 2)))


def test_fixed_point_free_s6_prefix_spectra_are_exact_controls():
    control = fixed_point_free_prefix_control()
    assert control.control_verified
    assert control.degree == 6
    assert control.source_partitions == ((5, 1), (5, 1), (5, 1))
    assert control.target_partition == (4, 2)
    assert control.multiplicity_dimension == 3
    assert control.prefix_metric_eigenvalues[0] == pytest.approx((2 / 5,) * 3)
    assert control.prefix_metric_eigenvalues[1] == pytest.approx(
        (1 / 10, 1 / 10, 7 / 30)
    )
    assert control.prefix_metric_eigenvalues[2] == pytest.approx(
        (1 / 30, 1 / 30, 11 / 60)
    )
    assert control.final_global_minimum_singular_value == pytest.approx(
        math.sqrt(1 / 30)
    )


def test_commuting_first_step_and_noncommuting_second_step_need_different_holonomy():
    control = fixed_point_free_prefix_control()
    first, second = control.chain_steps
    assert first.exact_chain_rule_verified
    assert first.prefix_metrics_commute
    assert first.holonomy_is_identity
    assert first.holonomy_identity_distance < 1e-8

    assert second.exact_chain_rule_verified
    assert not second.prefix_metrics_commute
    assert not second.holonomy_is_identity
    assert second.prefix_metric_commutator_norm > 0.007
    assert second.holonomy_identity_distance > 0.06
    assert second.relative_polar_to_global_polar_distance == pytest.approx(
        second.holonomy_identity_distance
    )
    assert second.holonomy_unitarity_residual < 1e-8
    assert second.holonomy_formula_residual < 1e-8


def test_relative_effects_can_be_constant_gap_while_global_metric_shrinks():
    control = fixed_point_free_prefix_control()
    assert control.finite_constant_relative_gap_found
    assert min(
        row.relative_effect_minimum_eigenvalue for row in control.chain_steps
    ) > 0.2
    final_step = control.chain_steps[-1]
    assert final_step.relative_effect_minimum_eigenvalue == pytest.approx(11 / 42)
    assert final_step.relative_effect_maximum_eigenvalue == pytest.approx(1.0)
    assert control.naive_sequential_conditioning_falsified


def test_partial_ulhmann_transport_handles_exact_s6_rank_loss():
    control = fixed_point_free_rank_loss_control()
    assert control.exact_partial_support_chain_rule_verified
    assert control.target_partition == (4, 1, 1)
    assert control.multiplicity_dimension == 3
    assert control.previous_prefix_rank == 3
    assert control.next_prefix_rank == 1
    assert control.relative_effect_rank == 1
    assert control.lost_multiplicity_dimension == 2
    assert control.positive_relative_effect_eigenvalues == pytest.approx((5 / 14,))
    assert control.next_support_outside_previous_support_residual < 1e-8
    assert control.relative_polar_partial_isometry_residual < 1e-8
    assert control.global_polar_partial_isometry_residual < 1e-8
    assert control.holonomy_initial_support_residual < 1e-8
    assert control.holonomy_final_support_residual < 1e-8
    assert control.holonomy_formula_residual < 1e-8
    assert control.partial_chain_rule_residual < 1e-8


def test_scaling_records_only_a_constructive_criterion():
    row = prefix_polar_scaling_record(32)
    assert row.prefix_depth == row.information_threshold_copy_count
    assert not row.all_prefix_relative_gap_theorem_proved
    assert not row.uniform_holonomy_compiler_constructed
    assert not row.rank_loss_compiler_constructed
    assert not row.global_polar_constructed
    with pytest.raises(ValueError, match="even"):
        prefix_polar_scaling_record(9)


def test_report_keeps_asymptotic_holonomy_and_rank_loss_gates_false(tmp_path):
    report = build_coset_prefix_polar_holonomy_report()
    assert report.theorem.theorem_verified
    assert report.theorem.exact_full_rank_chain_rule_proved
    assert report.theorem.holonomy_unitarity_proved
    assert report.theorem.identity_if_and_only_if_commuting_proved
    assert not report.theorem.naive_sequential_conditioning_universally_valid
    assert report.theorem.finite_fixed_point_free_noncommuting_control_verified
    assert not report.theorem.all_n_relative_gap_proved
    assert not report.theorem.uniform_holonomy_compiler_constructed
    assert report.theorem.rank_loss_extension_proved
    assert not report.theorem.polynomial_fused_polar_constructed
    assert report.claim_gate["exact_partial_support_chain_rule_proved"]
    assert report.claim_gate["rank_loss_chain_rule_proved"]
    assert not report.claim_gate["rank_loss_compiler_constructed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_coset_prefix_polar_holonomy_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "prefix-polar-chain-rule-proved-holonomy-and-gaps-open"
    )
