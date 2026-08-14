import math

import pytest

from self_dual_wreath_compressed_orientation_racah_cumulant_probe import (
    compile_orientation_racah_channel,
)
from self_dual_wreath_orientation_fixed_support_control_variate import (
    audit_fixed_support_control_variate,
    fixed_support_permutations,
    moved_point_count,
    run_orientation_fixed_support_control_variate,
)


def test_support_two_ball_is_identity_plus_transpositions_without_group_scan() -> None:
    for n in range(3, 9):
        ball = fixed_support_permutations(n, 2)
        assert len(ball) == 1 + math.comb(n, 2)
        assert max(map(moved_point_count, ball)) == 2
        assert len(set(ball)) == len(ball)


def test_support_two_walsh_sum_has_exact_product_null_aggregate() -> None:
    control = compile_orientation_racah_channel(
        "S6-SUPPORT-TWO-TEST", ((3, 1, 1, 1),) * 6
    )
    row = audit_fixed_support_control_variate(control, 2)
    assert row.aggregate_support_two_identity_residual == 0.0
    assert row.partial_aggregate_likelihood_ratio == 1.0
    assert row.fixed_radius_enumeration_polynomial
    assert row.enumerated_word_triple_count == (1 + math.comb(6, 2)) ** 3


def test_s7_channel_has_close_polynomial_support_two_surrogate() -> None:
    control = compile_orientation_racah_channel(
        "S7-SUPPORT-TWO-TEST", ((3, 2, 1, 1),) * 6
    )
    row = audit_fixed_support_control_variate(control, 2)
    assert row.partial_channel_is_nonnegative
    assert row.partial_to_full_total_variation == pytest.approx(
        0.006206281135, abs=1e-10
    )
    assert row.partial_irreducible_cmi_bits == pytest.approx(
        7.0677026468e-05, rel=1e-8
    )
    assert row.low_support_channel_within_one_percent_tv
    assert row.full_channel_dequantized is False


def test_s6_spike_is_not_explained_by_same_fixed_support_surrogate() -> None:
    control = compile_orientation_racah_channel(
        "S6-SUPPORT-TWO-FALSIFIER", ((3, 1, 1, 1),) * 6
    )
    row = audit_fixed_support_control_variate(control, 2)
    assert row.partial_irreducible_cmi_bits < 0.002
    assert row.full_irreducible_cmi_bits > 0.99
    assert row.low_support_channel_within_one_percent_tv is False
    assert row.full_residual_outside_support_ball_bounded is False


def test_report_demotes_s7_without_claiming_all_n_dequantization() -> None:
    report = run_orientation_fixed_support_control_variate()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["S7_finite_channel_has_close_polynomial_low_support_surrogate"] is True
    assert report.claim_gate["S6_one_bit_spike_explained_by_support_two"] is False
    assert report.claim_gate["full_residual_tail_bounded"] is False
    assert report.claim_gate["all_n_orientation_channel_dequantized"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
