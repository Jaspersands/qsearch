import itertools
from fractions import Fraction

from self_dual_wreath_sibling_frame_all_fixed_mp import (
    _binary_vectors,
    _set_partitions,
    all_fixed_mp_theorem,
    audit_marginal_support_expansion,
    exact_support_row_tuple_count,
    is_noncrossing_partition,
    leading_support_classification_control,
    narayana_number,
    partition_from_support,
    partition_support,
    run_sibling_frame_all_fixed_mp,
    support_incidence_rank,
    symmetrized_row_support,
)


def test_exact_support_sequence_count_matches_brute_force() -> None:
    support = ((0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 1))
    for source_pairs in range(1, 5):
        brute = sum(
            symmetrized_row_support(rows, 3) == support
            for rows in itertools.product(
                _binary_vectors(3),
                repeat=source_pairs,
            )
        )
        assert exact_support_row_tuple_count(support, source_pairs) == brute


def test_cube_section_rank_equality_recovers_partition_supports() -> None:
    partition = ((0, 3), (1, 2), (4,))
    support = partition_support(partition, 5)

    assert len(support) == 8
    assert support_incidence_rank(support) == 3
    assert partition_from_support(support) == partition

    nonpartition_support = (
        (0, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 0, 1, 0),
        (0, 1, 0, 0),
        (1, 0, 1, 1),
        (1, 1, 0, 1),
        (1, 1, 1, 0),
        (1, 1, 1, 1),
    )
    assert support_incidence_rank(nonpartition_support) == 4
    assert partition_from_support(nonpartition_support) is None


def test_power_two_free_supports_are_exactly_noncrossing_through_order_four() -> None:
    controls = [leading_support_classification_control(order) for order in range(1, 5)]

    assert all(row.cube_section_classification_verified for row in controls)
    assert all(row.noncrossing_free_classification_verified for row in controls)
    assert all(row.extra_free_support_count == 0 for row in controls)
    assert all(row.missing_noncrossing_support_count == 0 for row in controls)


def test_narayana_counts_match_direct_noncrossing_partition_counts() -> None:
    for order in range(1, 8):
        counts = {
            blocks: sum(
                len(partition) == blocks and is_noncrossing_partition(partition)
                for partition in _set_partitions(order)
            )
            for blocks in range(1, order + 1)
        }
        assert counts == {
            blocks: narayana_number(order, blocks)
            for blocks in range(1, order + 1)
        }


def test_support_expansion_is_exact_double_count() -> None:
    controls = [
        audit_marginal_support_expansion(2, 2, order)
        for order in (1, 2, 3, 4)
    ] + [audit_marginal_support_expansion(3, 1, 3)]

    assert all(row.exact_double_count_verified for row in controls)
    assert Fraction(controls[1].child_aspect) == Fraction(2, 1)


def test_theorem_closes_all_fixed_premise_but_not_rate_or_curl() -> None:
    theorem = all_fixed_mp_theorem()
    report = run_sibling_frame_all_fixed_mp()

    assert theorem.every_fixed_independent_marginal_moment_proved
    assert not theorem.growing_order_local_law_proved
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["all_fixed_independent_child_frame_moments_proved"]
    assert report.claim_gate["independent_child_frame_weak_mp_law_proved"]
    assert report.claim_gate["global_distinct_support_ridge_tail_small"]
    assert not report.claim_gate["inverse_polynomial_small_eigenvalue_rate_proved"]
    assert not report.claim_gate["natural_physical_ridge_curl_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
