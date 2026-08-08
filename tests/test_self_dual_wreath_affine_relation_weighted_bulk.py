import itertools
import math
from fractions import Fraction

from representation_obstruction import hook_length_dimension, integer_partitions
from self_dual_wreath_affine_relation_weighted_bulk import (
    audit_orientation_signature_counts,
    exact_signature_support_star_hs_expectation,
    expected_node_centered_frobenius_burden,
    predicted_signature_support_star_hs_expectation,
    run_affine_relation_weighted_bulk,
    valid_signature_supports,
    weighted_relation_bulk_scaling_record,
)
from self_dual_wreath_pair_core_carrier_factorization import (
    exact_star_overlap_spectrum,
)


def test_all_valid_signature_supports_match_closed_form_through_s7() -> None:
    for n in range(3, 8):
        targets = (
            (n,),
            max(integer_partitions(n), key=hook_length_dimension),
        )
        for target in targets:
            for support in valid_signature_supports():
                assert exact_signature_support_star_hs_expectation(
                    n, target, support
                ) == predicted_signature_support_star_hs_expectation(
                    n, target, support
                )


def test_closed_form_matches_exact_star_spectrum_plancherel_average() -> None:
    n = 5
    order = math.factorial(n)
    partitions = integer_partitions(n)
    support = frozenset(("10", "01"))
    for target in ((5,), (3, 1, 1)):
        observed = Fraction()
        for draws in itertools.product(partitions, repeat=4):
            labels = ((draws[0], draws[1]), (draws[2], draws[3]))
            probability = Fraction(
                math.prod(hook_length_dimension(item) ** 2 for item in draws),
                order**4,
            )
            ambient = hook_length_dimension(target) * math.prod(
                hook_length_dimension(item) for item in draws
            )
            rows = exact_star_overlap_spectrum(target, labels, 0, 1, 2)
            squared_overlap = sum(
                Fraction(
                    row.multiplicity * row.correlation_numerator**2,
                    row.correlation_denominator**2,
                )
                for row in rows
            )
            observed += probability * squared_overlap / ambient
        assert observed == exact_signature_support_star_hs_expectation(
            n, target, support
        )


def test_nonrich_two_signature_exception_is_exact_and_target_gated() -> None:
    support = frozenset(("10", "01"))
    order = math.factorial(5)
    assert exact_signature_support_star_hs_expectation(
        5, (5,), support
    ) == Fraction(2, order**4)
    assert exact_signature_support_star_hs_expectation(
        5, (3, 1, 1), support
    ) == 0


def test_orientation_signature_counts_match_exhaustive_cube_enumeration() -> None:
    for copy_count in range(2, 9):
        control = audit_orientation_signature_counts(copy_count)
        orientation_count = 1 << copy_count
        assert control.exact_signature_count_verified
        assert (
            control.predicted_two_signature_ordered_pair_count
            == 3 * (orientation_count - 2)
        )
        assert (
            control.predicted_three_or_four_signature_ordered_pair_count
            == orientation_count**2 - 6 * orientation_count + 8
        )
        assert (
            control.predicted_total_ordered_pair_count
            == (orientation_count - 1) * (orientation_count - 2)
        )


def test_exact_node_burden_includes_the_one_dimensional_exception() -> None:
    n = 5
    copy_count = 8
    order = math.factorial(n)
    orientation_count = 1 << copy_count
    high_dimensional = expected_node_centered_frobenius_burden(
        n, copy_count, (3, 1, 1)
    )
    one_dimensional = expected_node_centered_frobenius_burden(
        n, copy_count, (5,)
    )
    assert high_dimensional == Fraction(
        4 * (orientation_count**2 - 6 * orientation_count + 8),
        order**5,
    )
    assert one_dimensional - high_dimensional == Fraction(
        6 * (orientation_count - 2),
        order**4,
    )


def test_collision_free_weighted_bulk_bound_becomes_strong() -> None:
    row32 = weighted_relation_bulk_scaling_record(32)
    row48 = weighted_relation_bulk_scaling_record(48)
    assert row32.finite_collision_free_bulk_edge_certified
    assert row48.finite_collision_free_bulk_edge_certified
    assert row48.log2_conditioned_burden_to_capacity_ratio < -150
    assert row48.conditional_markov_failure_upper_bound < 1e-20
    assert row48.conditional_spectral_outlier_rank_fraction_upper_bound < 1e-19
    assert (
        row48.log2_conditioned_burden_to_capacity_ratio
        < row32.log2_conditioned_burden_to_capacity_ratio
    )


def test_report_keeps_pgm_and_speedup_claims_closed() -> None:
    report = run_affine_relation_weighted_bulk()
    assert report.headline_metrics[
        "exact_signature_support_star_burden_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "global_coefficient_bulk_edge_theorem_count"
    ] == 1
    assert report.claim_gate[
        "collision_free_global_coefficient_bulk_edge_proved"
    ]
    assert not report.claim_gate["untrimmed_relation_minimum_edge_proved"]
    assert report.claim_gate["relation_trim_zero_ideal_pgm_state_loss_proved"]
    assert not report.claim_gate[
        "retained_relations_exhaust_synthesis_cokernel_proved"
    ]
    assert not report.claim_gate["coherent_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
