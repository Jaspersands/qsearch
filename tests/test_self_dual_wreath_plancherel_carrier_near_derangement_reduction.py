from fractions import Fraction

from representation_obstruction import integer_partitions
from self_dual_wreath_plancherel_carrier_near_derangement_reduction import (
    audit_support_invariance_exponential_bound,
    near_derangement_finite_control,
    perfect_matching_commuting_control,
    run_plancherel_carrier_near_derangement_reduction,
    support_invariance_exponential_bound,
    write_plancherel_carrier_near_derangement_reduction_report,
)
from self_dual_wreath_plancherel_carrier_nonidentity_tail import (
    class_pair_commuting_probability,
)


def test_support_invariance_exponential_bound_is_exactly_audited() -> None:
    for n in range(2, 11):
        audit = audit_support_invariance_exponential_bound(n)
        assert audit.exponential_support_invariance_bound_verified is True
        assert audit.maximum_exponential_bound_violation <= 1e-15


def test_every_small_class_pair_obeys_both_support_bounds() -> None:
    for n in range(2, 9):
        partitions = tuple(integer_partitions(n))
        for left in partitions:
            left_support = n - left.count(1)
            for right in partitions:
                right_support = n - right.count(1)
                probability = float(class_pair_commuting_probability(left, right))
                assert probability <= support_invariance_exponential_bound(
                    left, right_support
                ) + 1e-15
                assert probability <= support_invariance_exponential_bound(
                    right, left_support
                ) + 1e-15


def test_perfect_matching_formula_matches_cycle_index_and_decays() -> None:
    controls = [perfect_matching_commuting_control(n) for n in range(4, 26, 2)]
    assert all(row.exact_cycle_index_formula_verified for row in controls)
    assert all(row.analytic_decay_bound_verified for row in controls)
    assert all(
        right.self_commuting_probability < left.self_commuting_probability
        for left, right in zip(controls[1:], controls[2:])
    )
    assert controls[-1].self_commuting_probability < 2e-5


def test_finite_tail_partition_is_exact_and_extremality_stays_finite() -> None:
    for n in (6, 8, 10, 12):
        control = near_derangement_finite_control(n)
        total = Fraction(control.exact_nonidentity_conditional_commuting_probability)
        partitioned = sum(
            (
                Fraction(control.exact_low_support_commuting_contribution),
                Fraction(control.exact_balanced_support_commuting_contribution),
                Fraction(control.exact_near_derangement_commuting_contribution),
            ),
            Fraction(0),
        )
        assert total == partitioned
        assert control.exact_partition_verified is True
        assert control.fixed_point_free_involution_is_finite_maximizer is True
        assert control.finite_extremality_only is True


def test_report_closes_support_ranges_without_promoting_residual_corner() -> None:
    report = run_plancherel_carrier_near_derangement_reduction(
        exact_degrees=(10, 12)
    )
    assert report.theorem.support_invariance_bound_proved is True
    assert report.theorem.low_and_balanced_support_contributions_vanish_proved is True
    assert report.theorem.logarithmic_fixed_point_reduction_proved is True
    assert report.theorem.perfect_matching_self_kernel_vanishes_proved is True
    assert (
        report.theorem.perfect_matching_extremal_for_all_near_derangements_proved
        is False
    )
    assert report.theorem.weighted_commuting_probability_vanishes_proved is False
    assert report.claim_gate[
        "carrier_tail_reduced_to_logarithmic_fixed_point_classes"
    ] is True
    assert report.claim_gate[
        "logarithmic_fixed_point_commuting_tail_vanishes_proved"
    ] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_proof_gated_near_derangement_artifact(tmp_path) -> None:
    payload = write_plancherel_carrier_near_derangement_reduction_report(
        path=tmp_path / "near-derangement.json",
        write_registry=False,
        exact_degrees=(10, 12),
    )
    assert payload["headline_metrics"][
        "support_invariance_exponential_bound_theorem_count"
    ] == 1
    assert payload["headline_metrics"][
        "largest_exact_near_derangement_degree"
    ] == 12
    assert payload["headline_metrics"][
        "near_derangement_all_n_extremality_theorem_count"
    ] == 0
    assert len(payload["falsifiers_triggered"]) >= 5
