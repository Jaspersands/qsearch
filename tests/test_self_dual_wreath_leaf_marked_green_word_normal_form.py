from functools import lru_cache

from representation_obstruction import integer_partitions
from self_dual_wreath_leaf_marked_green_word_normal_form import (
    independent_leaf_marked_word_moment,
    leaf_marked_word_map_strata,
    partially_pinned_two_color_count,
    run_leaf_marked_green_word_normal_form,
    uncompressed_pair_formula_control,
)
from self_dual_wreath_sibling_word_map_normal_form import (
    independent_sibling_word_moment,
)


@lru_cache(maxsize=1)
def _report():
    return run_leaf_marked_green_word_normal_form()


def test_partially_pinned_count_distinguishes_equal_and_different_coordinates():
    identity = (0, 1, 2)
    transposition = (1, 0, 2)
    sequence = (transposition, transposition, identity, identity)
    same = partially_pinned_two_color_count(
        sequence,
        "EEFF",
        differing_coordinate=False,
    )
    different = partially_pinned_two_color_count(
        sequence,
        "EEFF",
        differing_coordinate=True,
    )
    assert same == 1
    assert different == 1


def test_unmarked_sibling_word_is_recovered_exactly():
    for target in integer_partitions(3):
        marked = independent_leaf_marked_word_moment(
            3,
            2,
            1,
            target,
            "AABB",
        )
        sibling = independent_sibling_word_moment(3, 2, target, "AABB")
        assert marked == sibling


def test_all_left_leaf_words_are_exactly_target_independent():
    noncrossing = {
        independent_leaf_marked_word_moment(3, 2, 1, target, "EEFF")
        for target in integer_partitions(3)
    }
    crossing = {
        independent_leaf_marked_word_moment(3, 2, 1, target, "EFEF")
        for target in integer_partitions(3)
    }
    assert len(noncrossing) == 1
    assert len(crossing) == 1


def test_uncompressed_pair_formula_is_recovered_at_multiple_distances():
    controls = (
        uncompressed_pair_formula_control(3, 2, 1),
        uncompressed_pair_formula_control(4, 3, 1),
        uncompressed_pair_formula_control(4, 3, 2),
    )
    assert all(
        row.exact_target_independent_pair_formula_verified for row in controls
    )
    assert all(row.maximum_target_residual == "0" for row in controls)


def test_marked_strata_are_collapsed_before_target_evaluation():
    strata = leaf_marked_word_map_strata(3, "EAFB")
    assert strata
    assert all(same >= 0 and different >= 0 and count > 0 for same, different, _, count in strata)
    assert sum(count for *_, count in strata) == 6**2


def test_physical_controls_verify_word_formula_and_green_algebra_membership():
    report = _report()
    assert all(row.exact_direct_validation for row in report.direct_moment_controls)
    assert all(
        row.sibling_frame_algebra_contains_green_kernel
        for row in report.green_algebra_controls
    )
    assert report.headline_metrics["direct_moment_control_failure_count"] == 0
    assert report.headline_metrics["green_algebra_control_failure_count"] == 0


def test_claim_gate_keeps_the_actual_green_gap_open():
    report = _report()
    assert report.claim_gate[
        "exact_leaf_marked_independent_word_normal_form_proved"
    ]
    assert report.claim_gate[
        "exact_common_green_is_sibling_frame_algebra_function"
    ]
    assert not report.claim_gate["growing_marked_word_rigidity_proved"]
    assert not report.claim_gate[
        "natural_typical_hamming_green_pair_gap_positive"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.literature_links
    assert not any(
        row["covers_required_regime"] for row in report.literature_links
    )
