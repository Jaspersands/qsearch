from fractions import Fraction
from functools import lru_cache

import pytest

from coset_kronecker_marginal_conservation import (
    audit_existing_two_copy_law_marginal,
    audit_fusion_marginal,
    audit_regular_column_support,
    canonical_involution,
    fused_target_probability_from_projector_sum,
    kronecker_marginal_conservation_theorem,
    run_kronecker_marginal_conservation,
)
from coset_same_hidden_target_law import source_label_probability
from representation_obstruction import integer_partitions


@lru_cache(maxsize=1)
def _report():
    return run_kronecker_marginal_conservation()


def test_canonical_involution_has_requested_disjoint_transpositions():
    assert canonical_involution(6, 1) == (1, 0, 2, 3, 4, 5)
    assert canonical_involution(6, 3) == (1, 0, 3, 2, 5, 4)


@pytest.mark.parametrize(
    ("n", "transpositions"),
    ((3, 1), (4, 1), (4, 2), (5, 2)),
)
def test_source_character_sum_has_exact_two_point_support(n, transpositions):
    control = audit_regular_column_support(n, transpositions)
    assert control.supported_group_element_count == 2
    assert control.maximum_exact_column_residual == 0
    assert control.exact_two_point_support_verified


@pytest.mark.parametrize("copies", (1, 2, 3, 4, 7))
@pytest.mark.parametrize(
    ("n", "transpositions"),
    ((3, 1), (4, 1), (4, 2)),
)
def test_fused_target_marginal_equals_one_copy_weak_fourier_law(
    n,
    transpositions,
    copies,
):
    for target in integer_partitions(n):
        assert fused_target_probability_from_projector_sum(
            n,
            transpositions,
            copies,
            target,
        ) == source_label_probability(n, transpositions, target)
    control = audit_fusion_marginal(n, transpositions, copies)
    assert Fraction(control.exact_probability_sum) == 1
    assert Fraction(control.maximum_exact_one_copy_residual) == 0
    assert control.one_copy_weak_fourier_marginal_conserved
    assert control.pointwise_two_plancherel_domination_verified


@pytest.mark.parametrize(
    ("n", "transpositions"),
    ((3, 1), (4, 1), (4, 2), (5, 2)),
)
def test_existing_two_copy_joint_law_sums_to_conserved_marginal(n, transpositions):
    control = audit_existing_two_copy_law_marginal(n, transpositions)
    assert Fraction(control.exact_joint_probability_sum) == 1
    assert Fraction(control.maximum_exact_target_marginal_residual) == 0
    assert control.existing_conditional_law_matches_conservation_theorem


def test_theorem_does_not_discard_joint_or_multiplicity_frontier():
    theorem = kronecker_marginal_conservation_theorem()
    assert theorem.arbitrary_copy_count
    assert theorem.arbitrary_finite_group
    assert theorem.theorem_verified
    assert not theorem.target_label_amplification_possible
    assert not theorem.full_joint_information_collapses_to_one_copy


def test_report_closes_only_final_target_label_amplification():
    report = _report()
    assert report.headline_metrics[
        "all_copy_marginal_conservation_theorem_count"
    ] == 1
    assert report.headline_metrics["regular_column_control_failure_count"] == 0
    assert report.headline_metrics["fusion_marginal_control_failure_count"] == 0
    assert report.headline_metrics[
        "existing_two_copy_law_marginal_failure_count"
    ] == 0
    assert not report.claim_gate[
        "ordinary_kronecker_target_label_amplifies_signal"
    ]
    assert not report.claim_gate["postfusion_central_commutator_filter_viable"]
    assert not report.claim_gate["source_target_correlations_are_uninformative"]
    assert not report.claim_gate["multiplicity_space_collective_gain_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
