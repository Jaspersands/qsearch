from fractions import Fraction

from self_dual_wreath_short_word_profile import (
    mask_collision_scaling_record,
    run_short_word_profile,
    short_transposition_length_probability,
    unsigned_stirling_first_kind_row,
    validate_fixed_even_mask_uniformity,
)


def test_unsigned_stirling_row_counts_permutations() -> None:
    for n in range(1, 9):
        row = unsigned_stirling_first_kind_row(n)
        total = sum(row)
        expected = 1
        for value in range(2, n + 1):
            expected *= value
        assert total == expected


def test_short_length_probability_is_exact() -> None:
    assert short_transposition_length_probability(3, 0) == Fraction(1, 6)
    assert short_transposition_length_probability(3, 1) == Fraction(2, 3)
    assert short_transposition_length_probability(3, 2) == 1


def test_fixed_even_mask_has_uniform_base_marginals() -> None:
    for parameters in (
        (2, 3, 0b101),
        (3, 3, 0b101),
        (3, 4, 0b1111),
    ):
        record = validate_fixed_even_mask_uniformity(*parameters)
        assert record.exact_uniform_marginals_verified
        assert record.maximum_left_multiplicity_deviation == 0
        assert record.maximum_right_multiplicity_deviation == 0


def test_target_order_mask_collision_is_negligible() -> None:
    record = mask_collision_scaling_record(
        n=64,
        copy_count=296,
        moment_order=175526,
    )
    assert record.pairwise_mask_distinct_with_overwhelming_probability
    assert record.log2_pairwise_mask_collision_union_bound < -175000
    assert not record.non_diagonal_shared_generator_correlation_proved_small


def test_report_keeps_joint_word_tail_open() -> None:
    report = run_short_word_profile()
    assert report.claim_gate["fixed_even_mask_uniform_marginal_proved"]
    assert report.claim_gate[
        "pairwise_mask_collisions_negligible_at_target_order"
    ]
    assert not report.claim_gate[
        "non_diagonal_shared_generator_correlation_bound_proved"
    ]
    assert not report.claim_gate[
        "joint_short_word_anticoncentration_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
