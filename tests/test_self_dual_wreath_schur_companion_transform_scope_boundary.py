from __future__ import annotations

import json

from research_registry import initialize_seed_registry, load_negative_results
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)
from self_dual_wreath_schur_companion_transform_scope_boundary import (
    PRIMARY_LITERATURE,
    audit_schur_companion_scope,
    run_schur_companion_transform_scope_boundary,
    schur_companion_scope_scaling,
    write_schur_companion_transform_scope_boundary_report,
)


S3_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_actual_orientation_kernel_and_inverse_root_cross_branches() -> None:
    control = audit_schur_companion_scope(
        3,
        (2, 1),
        S3_LABELS,
        control_id="s3-cross-branch",
    )
    assert control.active_orientation_count == 6
    assert control.kernel_offdiagonal_frobenius_norm > 0.5
    assert control.inverse_sqrt_offdiagonal_frobenius_norm > 0.4
    assert control.maximum_kernel_branch_commutator_norm > 0.3
    assert control.maximum_inverse_sqrt_branch_commutator_norm > 0.2
    assert control.cross_branch_multiplier_required
    assert not control.known_transform_stack_compiles_polar


def test_inverse_root_reconstructs_kernel_exactly_on_support() -> None:
    control = audit_schur_companion_scope(
        4,
        (2, 1, 1),
        _w4_collision_free_labels()[0],
        control_id="s4-pseudoinverse-identity",
    )
    assert control.orientation_kernel_rank == control.active_orientation_count
    assert control.inverse_sqrt_reconstruction_residual < 1e-9
    assert control.best_branch_diagonal_inverse_sqrt_error > 0.04
    assert control.exact_scope_boundary_verified


def test_branch_workspace_composition_and_top_blocks_remain_closed() -> None:
    control = audit_schur_companion_scope(
        4,
        (3, 1),
        _w4_collision_free_labels()[1],
        control_id="s4-branch-algebra-closure",
    )
    assert control.branch_workspace_closure_residual < 1e-12
    assert control.selected_top_block_closure_residual < 1e-12
    assert control.maximum_inverse_sqrt_branch_commutator_norm > 0.03


def test_primary_sources_are_typed_without_importing_extra_capabilities() -> None:
    literature_ids = {row["id"] for row in PRIMARY_LITERATURE}
    assert "bacon-chuang-harrow-schur-2004" in literature_ids
    assert "burchardt-high-dimensional-schur-2025" in literature_ids
    assert "ikenmeyer-subramanian-kronecker-2023" in literature_ids
    assert "christandl-et-al-plethysm-sharp-bqp-2026" in literature_ids
    assert all(row["proved_primitive"] for row in PRIMARY_LITERATURE)
    assert all(row["not_supplied"] for row in PRIMARY_LITERATURE)


def test_natural_scaling_keeps_new_cross_oracle_as_the_missing_gate() -> None:
    row = schur_companion_scope_scaling(512)
    assert row.information_threshold_copy_count > 10_000
    assert row.joint_local_dimension_log2 > 100_000
    assert row.collision_free_source_probability_tends_one
    assert row.natural_high_dimensional_target_mass_tends_one
    assert row.natural_balanced_pair_cross_overlap_density_tends_one
    assert row.symmetric_group_qft_polynomial
    assert row.high_dimensional_schur_transform_polynomial
    assert row.invariant_membership_reflections_polynomial
    assert not row.known_stack_exposes_internal_kronecker_coordinates
    assert not row.known_stack_supplies_cross_branch_multiplier
    assert row.physical_interface_supplies_addressed_raw_cross_map_block_encoding
    assert row.addressed_raw_cross_map_block_encoding_normalization == 1.0
    assert row.coherent_gpe_supplies_direct_pair_polar
    assert not row.known_stack_supplies_normalization_one_orientation_polar
    assert not row.direct_non_branch_preserving_companion_circuit_ruled_out


def test_report_falsifies_only_the_known_transform_stack_hypothesis() -> None:
    report = run_schur_companion_transform_scope_boundary()
    assert report.theorem.theorem_verified
    assert "alpha=poly(n)" in report.theorem.normalization_boundary
    assert "classically" in report.theorem.classical_alternative
    assert report.claim_gate["known_schur_qft_and_projector_interfaces_typed"]
    assert report.claim_gate[
        "branch_preserving_stack_closed_under_coherent_composition"
    ]
    assert report.claim_gate[
        "actual_orientation_inverse_sqrt_requires_cross_branch_action"
    ]
    assert report.claim_gate["natural_cross_orientation_overlap_density_one_proved"]
    assert report.claim_gate["natural_high_dimensional_target_mass_proved"]
    assert not report.claim_gate["companion_only_stack_supplies_cross_branch_action"]
    assert not report.claim_gate["known_transform_stack_compiles_orientation_polar"]
    assert report.claim_gate[
        "physical_interface_supplies_addressed_raw_cross_map_block_encoding"
    ]
    assert report.claim_gate[
        "addressed_raw_cross_map_block_encoding_normalization_one"
    ]
    assert report.claim_gate["coherent_gpe_supplies_direct_pair_polar"]
    assert not report.claim_gate[
        "polynomial_normalized_global_cross_branch_whitening_oracle_compiled"
    ]
    assert not report.claim_gate[
        "full_global_cross_branch_block_encoding_normalization_charged"
    ]
    assert not report.claim_gate["global_operator_valued_metric_assembly_compiled"]
    assert not report.claim_gate["direct_structured_companion_polar_ruled_out"]
    assert not report.claim_gate["multi_round_companion_transform_ruled_out"]
    assert not report.claim_gate["physical_pgm_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_artifact_without_mutating_registry(tmp_path) -> None:
    path = tmp_path / "schur-companion-transform-scope-boundary.json"
    payload = write_schur_companion_transform_scope_boundary_report(
        path,
        write_registry=False,
    )
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"][
        "known_transform_stack_scope_theorem_count"
    ] == 1
    assert loaded["headline_metrics"]["finite_control_failure_count"] == 0


def test_writer_registers_the_precise_negative_result(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    write_schur_companion_transform_scope_boundary_report()
    negatives = {row["id"]: row for row in load_negative_results()}
    row = negatives["SCHUR-COMPANION-KNOWN-TRANSFORM-STACK-NO-POLAR"]
    assert row["evidence"]["cross_branch_inverse_sqrt_control_count"] == 3
    assert row["evidence"]["finite_control_failure_count"] == 0
    assert not row["evidence"]["speedup_claim_allowed"]
