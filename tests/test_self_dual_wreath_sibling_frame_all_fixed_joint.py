import itertools

from self_dual_wreath_sibling_frame_all_fixed_joint import (
    _free_mp_coefficient_counts,
    all_fixed_joint_theorem,
    audit_mixed_support_sequence_count,
    exact_mixed_support_row_tuple_count,
    mixed_leading_support_control,
    run_sibling_frame_all_fixed_joint,
    symmetrized_mixed_row_support,
)
from self_dual_wreath_sibling_frame_all_fixed_mp import _binary_vectors
from self_dual_wreath_sibling_word_map_normal_form import canonical_binary_words


def test_mixed_support_sequence_formula_matches_brute_force() -> None:
    supports = (
        ((0, 0), (1, 1)),
        ((0, 1), (1, 0)),
        ((0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 1)),
    )
    for support, source_pairs in zip(supports, (3, 4, 4)):
        control = audit_mixed_support_sequence_count(support, source_pairs)
        assert control.exact_support_sequence_formula_verified


def test_mixed_support_count_requires_every_complement_pair() -> None:
    support = ((0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 1))
    expected = exact_mixed_support_row_tuple_count(support, 3)
    brute = sum(
        symmetrized_mixed_row_support(rows, 3) == support
        for rows in itertools.product(_binary_vectors(3), repeat=3)
    )
    assert expected == brute


def test_leading_supports_match_colored_noncrossing_partitions_through_four() -> None:
    controls = [
        mixed_leading_support_control(word)
        for order in range(2, 5)
        for word in canonical_binary_words(order)
    ]

    assert all(row.leading_support_classification_verified for row in controls)
    assert all(row.free_mp_polynomial_match_verified for row in controls)
    assert all(row.extra_free_support_count == 0 for row in controls)
    assert all(row.missing_predicted_support_count == 0 for row in controls)


def test_crossing_word_has_fewer_leading_supports_than_noncrossing_word() -> None:
    noncrossing = mixed_leading_support_control("AABB")
    crossing = mixed_leading_support_control("ABAB")

    assert noncrossing.predicted_counts_by_block_count == {
        "2": 1,
        "3": 2,
        "4": 1,
    }
    assert crossing.predicted_counts_by_block_count == {"3": 2, "4": 1}
    assert crossing.predicted_leading_support_count < (
        noncrossing.predicted_leading_support_count
    )
    assert _free_mp_coefficient_counts("ABAB") == {"3": 2, "4": 1}


def test_theorem_closes_joint_fixed_words_but_not_marked_curl() -> None:
    theorem = all_fixed_joint_theorem()
    report = run_sibling_frame_all_fixed_joint()

    assert theorem.every_fixed_joint_moment_proved
    assert theorem.uniform_in_target_irrep
    assert not theorem.growing_order_control_proved
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["all_fixed_independent_joint_freeness_proved"]
    assert report.claim_gate["final_root_common_codimension_subextensive"]
    assert not report.claim_gate["low_rank_common_compression_curl_transfer_proved"]
    assert not report.claim_gate["natural_full_support_whitened_leaf_curl_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
