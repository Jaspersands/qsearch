import math
from functools import lru_cache

import pytest

from self_dual_wreath_exceptional_block_graph_core_pressure import (
    audit_exceptional_block_graph,
    exceptional_block_graph_code,
    reverse_ordered_blocks,
    run_exceptional_block_graph_core_pressure,
)


@lru_cache(maxsize=1)
def _report():
    return run_exceptional_block_graph_core_pressure()


@pytest.mark.parametrize(
    "block_sizes",
    ((1, 1), (1, 1, 1), (2, 1, 3), (1, 3, 2, 1)),
)
def test_reverse_block_code_is_nonpeelable_and_every_row_cancels(block_sizes):
    blocks = reverse_ordered_blocks(block_sizes)
    code = exceptional_block_graph_code(block_sizes)
    assert len(code) == 2 ** len(block_sizes)
    assert all(
        max(later) < min(earlier)
        for earlier, later in zip(blocks, blocks[1:])
    )
    control = audit_exceptional_block_graph(block_sizes)
    assert control.minimum_code_distance >= 2
    assert control.support_difference_peeling_stalls_on_full_core
    assert control.every_codeword_relation_cancels_after_singleton_substitution
    assert control.exact_control_verified


def test_exact_factorization_is_free_checks_times_fixed_genus_two_surface():
    for control in _report().representative_controls:
        assert control.remaining_generator_count == control.check_width + 5
        assert len(control.residual_relations) == 1
        assert control.residual_orientable_surface_genus == 2
        assert control.exact_free_surface_factorization_verified
        assert control.exact_solution_exponent_upper_bound == control.check_width + 4
        expected = 1 + 0.5 * math.log2(
            2**control.information_width
            / (2**control.information_width - 1)
        )
        assert control.true_pressure_margin == pytest.approx(expected)
        assert control.true_pressure_margin > 1


def test_report_rejects_the_unique_all_face_cancellation_mechanism():
    report = _report()
    assert report.headline_metrics[
        "all_depth_exceptional_block_graph_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.claim_gate[
        "globally_exceptional_block_graph_family_classified"
    ]
    assert not report.claim_gate[
        "all_face_cancellation_preserves_actual_pressure"
    ]
    assert report.claim_gate["exceptional_block_graph_uniformly_subleading"]
    assert not report.claim_gate["all_high_codimension_local_words_controlled"]
    assert not report.claim_gate["all_nonlinear_stopping_cores_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
