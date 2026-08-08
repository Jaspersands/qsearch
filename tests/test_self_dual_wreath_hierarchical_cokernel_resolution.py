import pytest

from self_dual_wreath_hierarchical_cokernel_resolution import (
    _abstract_controls,
    conditioning_counter_record,
    run_hierarchical_cokernel_resolution,
)


def test_three_lines_direct_h0_is_resolved_by_child_span_intersection() -> None:
    control = _abstract_controls()[0]

    assert control.original_pair_relation_rank == 0
    assert control.original_pair_emergent_h0_dimension == 1
    assert control.root_kernel_dimension == 1
    assert control.hierarchical_parent_relation_dimension_sum == 1
    assert control.hierarchical_relations_exhaust_root_kernel
    assert control.exact_hierarchical_cokernel_audit


def test_pair_generated_control_has_exact_recursive_kernel_decomposition() -> None:
    control = _abstract_controls()[1]

    assert control.root_kernel_dimension == 3
    assert control.original_pair_relation_rank == 3
    assert control.original_pair_emergent_h0_dimension == 0
    assert control.hierarchical_parent_relation_dimension_sum == 3
    assert all(
        node.exact_node_cokernel_decomposition_verified
        for node in control.nodes
    )
    assert control.maximum_kernel_projector_residual < 1e-10


def test_complete_hierarchy_can_have_small_endpoint_gap() -> None:
    control = _abstract_controls()[2]
    record = conditioning_counter_record(8)

    assert control.hierarchical_relations_exhaust_root_kernel
    assert control.minimum_hierarchical_endpoint_gap == pytest.approx(1 / 9)
    assert control.maximum_hierarchical_grading_defect == pytest.approx(7 / 9)
    assert record.minimum_endpoint_gap == pytest.approx(1 / 9)
    assert record.inverse_gap_cost == pytest.approx(9)


def test_conditioning_counterfamily_gap_vanishes_with_width() -> None:
    early = conditioning_counter_record(4)
    late = conditioning_counter_record(1 << 20)

    assert early.exact_hierarchy_complete
    assert late.exact_hierarchy_complete
    assert late.minimum_endpoint_gap < 1e-6
    assert late.inverse_gap_cost == pytest.approx((1 << 20) + 1)
    assert not late.constant_endpoint_gap


def test_report_resolves_h0_but_keeps_natural_comparability_blocked() -> None:
    report = run_hierarchical_cokernel_resolution()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "hierarchical_span_relations_exhaust_full_cokernel"
    ]
    assert not report.claim_gate["augmented_h0_is_information_theoretic_no_go"]
    assert not report.claim_gate[
        "natural_child_pseudoinverse_frames_comparable"
    ]
    assert not report.claim_gate["natural_hierarchical_endpoint_gap_proved"]
    assert not report.claim_gate[
        "coherent_hierarchical_cokernel_transform_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
