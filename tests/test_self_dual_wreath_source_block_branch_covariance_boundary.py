import json

from self_dual_wreath_source_block_branch_covariance_boundary import (
    audit_source_block_covariance,
    orientation_leaf_rank,
    run_source_block_branch_covariance_boundary,
    source_block_covariance_scaling_record,
    swap_source_labels,
    write_source_block_branch_covariance_boundary_report,
)


S6_LABELS = (
    ((6,), (4, 2)),
    ((5, 1), (2, 2, 2)),
    ((3, 3), (2, 1, 1, 1, 1)),
    ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
)


def test_source_label_swap_is_an_involution() -> None:
    labels = (((4,), (3, 1)), ((2, 2), (2, 1, 1)))
    swapped = swap_source_labels(labels, 3)
    assert swapped != labels
    assert swap_source_labels(swapped, 3) == labels


def test_cross_block_covariance_preserves_every_leaf_rank() -> None:
    control = audit_source_block_covariance(
        "S4-COVARIANCE",
        (2, 2),
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        3,
        (0, 1),
    )
    assert control.cross_block_covariance_rank_mismatch_count == 0
    assert not control.source_block_stabilized_by_translation
    assert control.within_fixed_block_rank_mismatch_count == 1
    assert not control.fixed_block_internal_branch_unitary_possible
    assert control.exact_cross_block_covariance_scope_verified


def test_s6_fixed_block_has_the_physical_leaf_rank_mismatch() -> None:
    control = audit_source_block_covariance(
        "S6-PARTIAL-SUPPORT",
        (6,),
        S6_LABELS,
        9,
        (2, 5),
    )
    ranks = dict(control.original_leaf_ranks)
    assert (ranks[2], ranks[5]) == (225, 125)
    assert (ranks[11], ranks[12]) == (225, 2025)
    assert control.left_child_leaf_coefficient_dimension == 350
    assert control.right_child_leaf_coefficient_dimension == 2250
    assert control.maximum_within_block_leaf_rank_difference == 1900


def test_leaf_rank_formula_tracks_selected_multiplicity_and_companion_dimension() -> None:
    assert orientation_leaf_rank((6,), S6_LABELS, 2) == 225
    assert orientation_leaf_rank((6,), S6_LABELS, 5) == 125
    swapped = swap_source_labels(S6_LABELS, 9)
    assert orientation_leaf_rank((6,), swapped, 2 ^ 9) == 225
    assert orientation_leaf_rank((6,), swapped, 5 ^ 9) == 125


def test_scaling_distinguishes_annealed_symmetry_from_blockwise_compilation() -> None:
    record = source_block_covariance_scaling_record(16)
    assert record.unequal_source_tuple_branch_stabilizer_trivial
    assert record.cross_source_block_branch_covariance_exact
    assert record.independent_plancherel_law_branch_invariant
    assert not record.annealed_symmetry_implies_fixed_block_metric_equality
    assert not record.fixed_block_hadamard_endpoint_mixer_proved
    assert not record.matrix_recursive_child_compiler_proved


def test_report_rejects_only_the_fixed_block_shortcut() -> None:
    report = run_source_block_branch_covariance_boundary()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_count"] == 4
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["cross_block_covariance_rank_mismatch_count"] == 0
    assert report.headline_metrics["fixed_block_rank_mismatch_control_count"] == 4
    assert report.claim_gate["cross_source_block_branch_covariance_proved"]
    assert report.claim_gate["independent_plancherel_source_law_branch_invariant"]
    assert not report.claim_gate[
        "annealed_branch_symmetry_implies_fixed_block_sibling_conjugacy"
    ]
    assert not report.claim_gate["fixed_block_hadamard_endpoint_mixer_compiled"]
    assert not report.claim_gate["direct_rectangular_cs_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_records_covariance_scope_boundary(tmp_path) -> None:
    path = tmp_path / "source_block_covariance.json"
    payload = write_source_block_branch_covariance_boundary_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["status"] == (
        "branch-covariance-crosses-source-block-fixed-block-shortcut-rejected"
    )
    assert stored["headline_metrics"]["source_block_covariance_scope_theorem_count"] == 1
    assert stored["headline_metrics"]["fixed_block_hadamard_endpoint_compiler_count"] == 0
    assert stored["headline_metrics"]["new_quantum_algorithm_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
