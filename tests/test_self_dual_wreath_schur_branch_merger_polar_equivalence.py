from __future__ import annotations

import json

import pytest

from self_dual_wreath_schur_branch_merger_polar_equivalence import (
    audit_schur_branch_merger,
    run_schur_branch_merger_polar_equivalence,
    schur_branch_merger_scaling_record,
    write_schur_branch_merger_polar_equivalence_report,
)


S3_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_encoded_subspace_merger_is_the_physical_polar_in_new_coordinates() -> None:
    control = audit_schur_branch_merger(
        3,
        (2, 1),
        S3_LABELS,
        control_id="s3-polar-transport",
    )
    assert control.active_orientation_count >= 2
    assert control.total_active_multiplicity_dimension > 0
    assert (
        control.encoded_branch_companion_dimension
        > control.total_active_multiplicity_dimension
    )
    assert control.raw_frame_identity_residual < 1e-9
    assert control.encoded_output_frame_residual < 1e-9
    assert control.encoded_domain_gram_transport_residual < 1e-9
    assert control.nonzero_singular_spectrum_transport_residual < 1e-9
    assert control.physical_polar_transport_residual < 1e-9
    assert control.physical_polar_left_support_residual < 1e-9
    assert control.maximum_source_isotypic_embedding_residual < 1e-9
    assert control.maximum_invariant_bell_factorization_residual < 1e-9
    assert control.maximum_invariant_companion_interface_residual < 1e-9
    assert control.exact_schur_branch_polar_equivalence_verified


def test_encoded_joint_character_factor_preserves_kernel_and_polar() -> None:
    control = audit_schur_branch_merger(
        3,
        (2, 1),
        S3_LABELS,
        control_id="s3-kernel-transport",
        seed=17,
    )
    assert control.orientation_kernel_factor_residual < 1e-9
    assert control.encoded_orientation_kernel_transport_residual < 1e-9
    assert control.orientation_kernel_spectrum_transport_residual < 1e-9
    assert control.orientation_kernel_polar_transport_residual < 1e-9


def test_overlapping_ranges_force_which_path_environment_tags() -> None:
    control = audit_schur_branch_merger(
        3,
        (2, 1),
        S3_LABELS,
        control_id="s3-environment",
    )
    assert control.overlapping_branch_pair_count > 0
    assert control.overlap_graph_clique_lower_bound >= 2
    assert control.common_environment_isometry_defect > 1e-6
    assert control.orthogonal_environment_isometry_residual < 1e-9


def test_raw_merger_contraction_scale_is_not_a_polar_compiler() -> None:
    control = audit_schur_branch_merger(
        3,
        (2, 1),
        S3_LABELS,
        control_id="s3-contraction",
    )
    assert 0 < control.largest_contractive_raw_merger_amplitude <= 1
    assert control.largest_contractive_raw_merger_probability_scale == pytest.approx(
        control.largest_contractive_raw_merger_amplitude**2
    )
    assert control.physical_frame_maximum_eigenvalue >= 1 - 1e-9


def test_scaling_keeps_encoding_separate_from_polar_complexity() -> None:
    row = schur_branch_merger_scaling_record(512)
    assert row.information_threshold_copy_count > 10_000
    assert row.joint_schur_local_log2_dimension > 100_000
    assert row.fixed_source_schur_carrier_encoding_polynomial
    assert row.physical_invariant_to_schur_companion_interface_compiled
    assert not row.branch_encoding_changes_nonzero_singular_values
    assert not row.branch_encoding_removes_inverse_square_root
    assert not row.direct_structured_branch_polar_compiled
    assert not row.branch_character_retaining_decoder_ruled_out


def test_report_closes_only_the_free_merger_loophole() -> None:
    report = run_schur_branch_merger_polar_equivalence()
    assert report.theorem.theorem_verified
    assert report.claim_gate[
        "schur_branch_encoding_preserves_nonzero_singular_spectrum"
    ]
    assert report.claim_gate[
        "encoded_merger_polar_equals_physical_orientation_polar"
    ]
    assert report.claim_gate[
        "encoded_joint_character_polar_equals_original_polar"
    ]
    assert report.claim_gate[
        "physical_encoded_polar_compilers_interreduce_given_interface"
    ]
    assert report.claim_gate[
        "physical_encoded_polar_compilers_polynomially_interreducible"
    ]
    assert report.claim_gate[
        "physical_invariant_to_schur_companion_interface_compiled"
    ]
    assert not report.claim_gate[
        "schur_dilation_alone_compiles_cross_orientation_merger"
    ]
    assert not report.claim_gate["direct_structured_branch_polar_compiled"]
    assert not report.claim_gate["multi_round_companion_transform_ruled_out"]
    assert not report.claim_gate["branch_character_retaining_decoder_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_equivalence_artifact(tmp_path) -> None:
    path = tmp_path / "schur-branch-merger-polar-equivalence.json"
    payload = write_schur_branch_merger_polar_equivalence_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"][
        "exact_schur_branch_polar_equivalence_theorem_count"
    ] == 1
    assert loaded["headline_metrics"]["finite_control_failure_count"] == 0


def test_invalid_control_without_two_active_orientations_is_rejected() -> None:
    with pytest.raises(ValueError):
        audit_schur_branch_merger(
            3,
            (3,),
            (((3,), (2, 1)),),
            control_id="insufficient-active-branches",
        )
