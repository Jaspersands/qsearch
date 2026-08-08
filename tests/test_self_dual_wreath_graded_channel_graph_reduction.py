import itertools

import pytest

from self_dual_wreath_graded_channel_graph_reduction import (
    audit_graded_channel_graph,
    run_graded_channel_graph_reduction,
)


@pytest.mark.parametrize(
    "gamma,expected",
    [(1 / 9, 1 / 17), (1 / 5, 1 / 9)],
)
def test_affine_w6_star_reproduces_exact_dense_defect(
    gamma: float,
    expected: float,
) -> None:
    record = audit_graded_channel_graph(
        "W6-STAR",
        (2, 5, 11, 12),
        ((2, 12), (5, 12), (11, 12)),
        (2, 5),
        gamma,
        expected_defect=expected,
    )

    assert record.grading_defect_norm == pytest.approx(expected)
    assert record.exact_graph_reduction_verified
    assert record.direct_to_resolvent_metric_residual < 1e-12
    assert record.direct_to_resolvent_grading_residual < 1e-12


def test_complete_and_crossing_only_controls_recover_both_boundaries() -> None:
    vertices = tuple(range(8))
    left = tuple(range(4))
    right = tuple(range(4, 8))
    complete = tuple(itertools.combinations(vertices, 2))
    crossing = tuple((x, y) for x in left for y in right)

    rescued = audit_graded_channel_graph(
        "COMPLETE",
        vertices,
        complete,
        left,
        1 / 5,
        expected_defect=1 / 4,
    )
    obstructed = audit_graded_channel_graph(
        "CROSSING",
        vertices,
        crossing,
        left,
        1 / 5,
        expected_defect=1 / 3,
    )

    assert rescued.endpoint_gap == pytest.approx(3 / 8)
    assert obstructed.endpoint_gap == pytest.approx(1 / 3)
    assert rescued.exact_graph_reduction_verified
    assert obstructed.exact_graph_reduction_verified


def test_report_sets_resolvent_target_without_overclaiming_natural_case() -> None:
    report = run_graded_channel_graph_reduction()

    assert report.claim_gate[
        "flat_channel_graph_resolvent_reduction_proved"
    ]
    assert report.claim_gate[
        "endpoint_effect_comparability_is_exact_target"
    ]
    assert report.claim_gate["w6_affine_star_defects_explained"]
    assert not report.claim_gate[
        "affine_vertex_support_implies_complete_channel_closure"
    ]
    assert not report.claim_gate[
        "natural_channel_resolvent_comparability_proved"
    ]
    assert not report.claim_gate["matrix_valued_channel_extension_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
