import math

import pytest

from coset_hidden_involution_rigid_gi_bridge import (
    audit_rigid_gi_wreath_bridge,
    build_rigid_gi_hidden_involution_bridge_report,
    rigid_gi_bridge_scaling_record,
    structured_gi_involution,
    write_rigid_gi_hidden_involution_bridge_report,
)


@pytest.mark.parametrize("graph_size", (2, 3))
def test_structured_gi_involutions_and_wreath_lift_are_exact(graph_size):
    row = audit_rigid_gi_wreath_bridge(graph_size)
    assert row.exact_wreath_to_symmetric_coset_lift_verified
    assert row.wreath_subgroup_order == 2 * math.factorial(graph_size) ** 2
    assert row.structured_involution_count == math.factorial(graph_size)
    assert row.all_structured_elements_are_involutions
    assert row.all_structured_elements_are_fixed_point_free
    assert row.all_structured_elements_swap_blocks
    assert row.structured_elements_are_distinct
    assert row.structured_class_closed_under_young_conjugation
    assert row.hidden_state_lift_residual < 1e-8
    assert row.null_state_lift_residual < 1e-8


def test_structured_involution_encodes_alpha_and_inverse():
    alpha = (2, 0, 1)
    hidden = structured_gi_involution(alpha)
    assert hidden == (5, 3, 4, 1, 2, 0)
    assert all(hidden[hidden[index]] == index for index in range(6))
    with pytest.raises(ValueError, match="permutation"):
        structured_gi_involution((0, 0, 1))


def test_scaling_keeps_rigid_and_nonrigid_scope_separate():
    rows = [rigid_gi_bridge_scaling_record(n) for n in (2, 3, 4, 8, 16, 32)]
    assert all(row.random_full_conjugation_symmetrizes_structured_hidden for row in rows)
    assert all(row.polynomial_full_class_binary_detector_implies_rigid_gi for row in rows)
    assert all(row.polynomial_full_class_identifier_implies_rigid_gi_search for row in rows)
    assert all(not row.nonrigid_gi_covered for row in rows)
    assert rows[-1].structured_fraction_log2 < -20
    with pytest.raises(ValueError, match="at least two"):
        rigid_gi_bridge_scaling_record(1)


def test_report_links_natural_problem_without_claiming_algorithm(tmp_path):
    report = build_rigid_gi_hidden_involution_bridge_report(
        finite_graph_sizes=(2,),
        scaling_graph_sizes=(2, 3, 4, 8),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.wreath_to_full_symmetric_state_lift_proved
    assert report.theorem.full_class_detector_to_rigid_gi_reduction_proved
    assert report.theorem.full_class_identifier_to_rigid_gi_search_reduction_proved
    assert not report.theorem.efficient_full_class_binary_detector_constructed
    assert not report.theorem.rigid_gi_quantum_algorithm_constructed
    assert not report.theorem.general_gi_quantum_algorithm_constructed
    assert not report.claim_gate["bridge_new_to_literature"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_rigid_gi_hidden_involution_bridge_report(
        tmp_path / "rigid-gi-bridge.json",
        finite_graph_sizes=(2,),
        scaling_graph_sizes=(2, 3, 4),
    )
    assert payload["status"] == (
        "rigid-gi-natural-bridge-proved-binary-detector-open"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0


def test_dense_finite_control_rejects_large_instance():
    with pytest.raises(ValueError, match="supports graph size"):
        audit_rigid_gi_wreath_bridge(4)
