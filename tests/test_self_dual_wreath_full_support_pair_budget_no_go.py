from functools import lru_cache

from self_dual_wreath_full_support_pair_budget_no_go import (
    _generic_transverse_frame,
    _orthogonal_pvm,
    audit_full_support_pair_budget,
    full_support_pair_budget_theorem,
    natural_full_support_pair_budget_scaling_record,
    run_full_support_pair_budget_no_go,
)
from self_dual_wreath_leaf_whitening_commutator_no_go import (
    construct_commuting_whitening_counterfamily,
)


@lru_cache(maxsize=1)
def _report():
    return run_full_support_pair_budget_no_go()


def test_commuting_full_support_frame_obeys_pair_budget_bound():
    _, _, leaves, _ = construct_commuting_whitening_counterfamily(3, 5, 2)
    row = audit_full_support_pair_budget("commuting", leaves)
    assert row.full_support
    assert row.canonical_effects_commute
    assert row.exact_pair_common_budget >= row.total_leaf_rank_excess
    assert row.pair_budget_bound_residual >= 0
    assert row.exact_full_support_pair_budget_theorem_verified


def test_transverse_rank_excess_forces_noncommutativity():
    row = audit_full_support_pair_budget(
        "transverse",
        _generic_transverse_frame(2309),
    )
    assert row.full_support
    assert row.total_leaf_rank_excess > 0
    assert row.exact_pair_common_budget == 0
    assert row.pair_budget_obstruction_detects_noncommutativity
    assert not row.canonical_effects_commute
    assert row.exact_full_support_pair_budget_theorem_verified


def test_orthogonal_pvm_is_sharp_zero_excess_boundary():
    row = audit_full_support_pair_budget("pvm", _orthogonal_pvm(9))
    assert row.total_leaf_rank_excess == 0
    assert row.exact_pair_common_budget == 0
    assert row.canonical_effects_commute
    assert row.exact_full_support_pair_budget_theorem_verified


def test_natural_probability_bound_uses_rank_gap_and_pair_budget():
    small = natural_full_support_pair_budget_scaling_record(24)
    large = natural_full_support_pair_budget_scaling_record(48)
    assert small.commuting_pair_budget_relative_lower_bound >= 31 / 32
    assert large.commuting_pair_budget_relative_lower_bound >= 31 / 32
    assert large.expected_all_orientation_pair_budget_relative_upper_bound < (
        small.expected_all_orientation_pair_budget_relative_upper_bound
    )
    assert large.conditioned_commuting_full_support_probability_upper_bound < (
        small.conditioned_commuting_full_support_probability_upper_bound
    )
    assert large.asymptotic_probability_vanishes
    assert not large.natural_child_full_support_proved
    assert not large.quantitative_component_M4_proved


def test_theorem_is_full_support_conditional_and_keeps_M4_gate_false():
    theorem = full_support_pair_budget_theorem()
    assert theorem.all_finite_dimensions
    assert theorem.arbitrary_projection_ranks
    assert theorem.natural_full_support_branch_noncommutative_with_high_probability
    assert theorem.theorem_verified
    assert not theorem.natural_full_support_proved
    assert not theorem.natural_component_M4_positive


def test_report_eliminates_only_full_support_commuting_branch():
    report = _report()
    assert report.headline_metrics[
        "full_support_pair_budget_inequality_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "natural_full_support_commuting_branch_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["natural_full_support_commuting_branch_eliminated"]
    assert not report.claim_gate["natural_final_child_full_support_proved"]
    assert not report.claim_gate["proper_common_span_commuting_branch_eliminated"]
    assert not report.claim_gate["quantitative_natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
