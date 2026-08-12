from __future__ import annotations

import pytest

from self_dual_wreath_constant_arity_joint_freeness import (
    EIGHT_WAY_ENDPOINT_POSITIVE_EDGE_FLOOR,
    EIGHT_WAY_ENDPOINT_TRIM,
    colored_split_relations,
    constant_arity_leading_support_control,
    constant_arity_scaling_record,
    eight_way_endpoint_aspect_record,
    free_mp_family_coefficient_counts,
    run_constant_arity_joint_freeness,
)


def test_colored_split_relations_use_every_prefix_bit() -> None:
    relations = colored_split_relations(3, (0, 3, 5, 6))

    assert len(relations) == 6
    assert all(relations)


@pytest.mark.parametrize(
    ("bits", "word"),
    [
        (2, (0, 1)),
        (2, (0, 3, 1)),
        (2, (0, 1, 2, 3)),
        (3, (0, 4)),
        (3, (0, 3, 5)),
        (3, (0, 3, 5, 6)),
    ],
)
def test_leading_supports_are_color_respecting_noncrossing(
    bits: int,
    word: tuple[int, ...],
) -> None:
    control = constant_arity_leading_support_control(bits, word)

    assert control.leading_support_classification_verified
    assert control.extra_free_support_count == 0
    assert control.missing_predicted_support_count == 0
    assert control.predicted_counts_by_block_count == free_mp_family_coefficient_counts(word)


@pytest.mark.parametrize("gamma", [0.25, 0.3, 0.375, 0.45, 0.5])
def test_eight_way_endpoint_bulk_has_uniform_two_sided_edge(gamma: float) -> None:
    row = eight_way_endpoint_aspect_record(gamma)

    assert row.fixed_parent_window_contains_limit
    assert row.endpoint_trim_below_uniform_edge
    assert row.endpoint_two_sided_edge_lower_bound >= EIGHT_WAY_ENDPOINT_POSITIVE_EDGE_FLOOR - 1e-12
    assert EIGHT_WAY_ENDPOINT_TRIM < row.endpoint_two_sided_edge_lower_bound


def test_mixed_schedule_scaling_uses_natural_eight_way_theorem() -> None:
    row = constant_arity_scaling_record(32)

    assert row.selected_copy_count == row.information_threshold_copy_count + 2
    assert 0.25 <= row.eight_way_child_aspect < 0.5
    assert 2 <= row.eight_way_parent_aspect < 4
    assert row.natural_fixed_eight_way_joint_freeness_proved
    assert not row.operator_norm_endpoint_edge_proved
    assert not row.structured_endpoint_effect_access_proved
    assert not row.early_binary_levels_compiled


def test_invalid_colored_words_and_aspects_are_rejected() -> None:
    with pytest.raises(ValueError):
        colored_split_relations(0, (0, 1))
    with pytest.raises(ValueError):
        colored_split_relations(2, (1, 1))
    with pytest.raises(ValueError):
        eight_way_endpoint_aspect_record(0.2)


def test_report_preserves_access_and_early_level_gates() -> None:
    report = run_constant_arity_joint_freeness()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["natural_fixed_arity_joint_freeness_proved"]
    assert report.claim_gate["natural_eight_way_threshold_endpoint_bulk_gap_proved"]
    assert report.claim_gate["annealed_eight_way_native_state_loss_vanishes"]
    assert not report.claim_gate["eight_way_untrimmed_operator_edge_proved"]
    assert not report.claim_gate["structured_eight_way_endpoint_effect_access_proved"]
    assert not report.claim_gate["early_low_rank_binary_levels_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
