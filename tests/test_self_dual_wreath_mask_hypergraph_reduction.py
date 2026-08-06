from fractions import Fraction

from self_dual_wreath_character_moments import unequal_pair_descriptor
from self_dual_wreath_mask_hypergraph_reduction import (
    column_weights,
    exact_joint_character_product,
    gauge_fixed_triangle_character_product,
    has_private_column,
    private_column_count,
    run_mask_hypergraph_reduction,
)


def test_mask_incidence_private_columns() -> None:
    masks = (0b0011, 0b1100, 0b1010)
    assert column_weights(masks) == (1, 2, 1, 2)
    assert private_column_count(masks) == 2
    assert has_private_column(masks)
    assert not has_private_column((0b011, 0b101, 0b110))


def test_private_column_joint_character_product_vanishes() -> None:
    descriptors = (
        unequal_pair_descriptor((3,), (2, 1)),
        unequal_pair_descriptor((3,), (1, 1, 1)),
        unequal_pair_descriptor((2, 1), (1, 1, 1)),
    )
    value = exact_joint_character_product(
        3,
        (0b0011, 0b1100, 0b1010),
        descriptors,
    )
    assert value == 0


def test_collision_free_triangle_can_have_nonzero_exact_correlation() -> None:
    descriptors = (
        unequal_pair_descriptor((5,), (4, 1)),
        unequal_pair_descriptor((3, 2), (2, 2, 1)),
        unequal_pair_descriptor((2, 1, 1, 1), (1, 1, 1, 1, 1)),
    )
    value = gauge_fixed_triangle_character_product(5, descriptors)
    assert value == Fraction(1, 1600)


def test_report_reduces_to_two_core_without_closing_tail() -> None:
    report = run_mask_hypergraph_reduction()
    assert report.claim_gate["private_column_joint_vanishing_proved"]
    assert report.claim_gate["mask_hypergraph_two_core_reduction_proved"]
    assert report.claim_gate[
        "collision_free_two_core_correlations_can_be_nonzero"
    ]
    assert not report.claim_gate["joint_two_core_anticoncentration_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
