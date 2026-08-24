from __future__ import annotations

import json

from self_dual_wreath_schur_dilated_multiplicity_access import (
    audit_schur_dilation,
    kronecker_branching_dimension,
    common_isometry_gram_invariance_residual,
    run_schur_dilated_multiplicity_access,
    schur_dilation_scaling,
    weyl_module_dimension,
    write_schur_dilated_multiplicity_access_report,
)


def test_hook_content_dimensions_are_exact() -> None:
    assert weyl_module_dimension((3,), 2) == 4
    assert weyl_module_dimension((2, 1), 2) == 2
    assert weyl_module_dimension((2, 1), 3) == 8
    assert weyl_module_dimension((1, 1, 1), 2) == 0


def test_exact_gl_branching_identity_matches_kronecker_sum() -> None:
    for target, left_dimension, right_dimension in (
        ((2, 1), 2, 2),
        ((2, 2), 2, 3),
        ((3, 1, 1), 3, 3),
    ):
        joint = weyl_module_dimension(
            target,
            left_dimension * right_dimension,
        )
        assert kronecker_branching_dimension(
            target,
            left_dimension,
            right_dimension,
        ) == joint


def test_direct_diagonal_projector_has_kronecker_rank() -> None:
    control = audit_schur_dilation(
        (2, 2),
        (3, 1),
        (3, 1),
        2,
        3,
        control_id="rank-control",
    )
    assert control.projector_rank_residual == 0
    assert control.projector_idempotence_residual < 1e-9
    assert control.projector_hermiticity_residual < 1e-9
    assert control.exact_schur_dilation_control_verified


def test_genuine_multiplicity_two_is_encoded_not_discarded() -> None:
    control = audit_schur_dilation(
        (3, 2),
        (3, 1, 1),
        (3, 1, 1),
        3,
        3,
        control_id="multiplicity-two",
    )
    assert control.kronecker_multiplicity == 2
    assert control.fixed_companion_encoded_multiplicity_dimension == 2
    assert control.direct_isotypic_projector_rank == 12
    assert control.full_branch_companion_dimension > 2
    assert control.target_joint_branch_sector_count > 1
    assert control.exact_schur_dilation_control_verified


def test_common_isometric_coordinate_change_preserves_orientation_gram() -> None:
    assert common_isometry_gram_invariance_residual() < 1e-9


def test_information_threshold_dilation_is_polynomial_but_not_a_polar() -> None:
    row = schur_dilation_scaling(512)
    assert row.information_threshold_copy_count > 10_000
    assert row.log2_joint_local_dimension > 100_000
    assert row.global_k_copy_isotypic_router_polynomial
    assert row.encoded_multiplicity_carrier_available
    assert not row.standard_multiplicity_coordinates_exposed
    assert not row.racah_associator_compiled
    assert not row.orientation_gram_conditioning_improved
    assert not row.direct_orientation_polar_compiled


def test_report_corrects_blanket_no_access_claim_without_overclaiming() -> None:
    report = run_schur_dilated_multiplicity_access()
    literature_ids = {item["id"] for item in report.literature_scope}
    assert report.theorem.theorem_verified
    assert "christandl-et-al-plethysm-sharp-bqp-2026" in literature_ids
    assert report.claim_gate["global_k_copy_isotypic_router_polynomial_proved"]
    assert report.claim_gate["encoded_kronecker_multiplicity_carrier_proved"]
    assert not report.claim_gate["bare_internal_kronecker_basis_transform_compiled"]
    assert not report.claim_gate["k_copy_racah_associator_compiled"]
    assert report.claim_gate["common_coordinate_isometry_preserves_orientation_gram"]
    assert not report.claim_gate["controlled_source_schur_router_realizes_orientation_gram"]
    assert not report.claim_gate["cross_orientation_branch_intertwiner_compiled"]
    assert not report.claim_gate["direct_orientation_kernel_polar_compiled"]
    assert not report.claim_gate["actual_physical_pgm_rejected"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_schur_dilation_artifact(tmp_path) -> None:
    path = tmp_path / "schur-dilated-multiplicity-access.json"
    payload = write_schur_dilated_multiplicity_access_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"]["polynomial_dilated_router_count"] == 1
    assert loaded["headline_metrics"][
        "genuine_multiplicity_greater_than_one_control_count"
    ] == 1
