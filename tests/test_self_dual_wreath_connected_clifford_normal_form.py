import json

from self_dual_wreath_connected_clifford_normal_form import (
    audit_clifford_fixed_space_normal_form,
    clifford_normal_form_scaling_record,
    run_connected_clifford_normal_form,
    write_connected_clifford_normal_form_report,
)


def test_single_pair_clifford_cross_gram_retains_half_normalization() -> None:
    control = audit_clifford_fixed_space_normal_form(
        "S3-PAIR",
        (2, 1),
        (((3,), (2, 1)),),
    )
    assert control.orientation_count == 2
    assert control.branch_fixed_dimension == control.base_carrier_dimension
    assert control.diagonal_fixed_dimension == 1
    assert control.frame_rank == 1
    assert abs(control.minimum_positive_cross_gram_eigenvalue - 0.5) < 1e-12
    assert not control.normalized_overlap_already_partial_isometry
    assert control.exact_clifford_fixed_space_normal_form_verified


def test_multibranch_clifford_cross_gram_is_matrix_valued() -> None:
    control = audit_clifford_fixed_space_normal_form(
        "S3-MULTI",
        (2, 1),
        (
            ((3,), (2, 1)),
            ((2, 1), (1, 1, 1)),
        ),
    )
    assert control.orientation_count == 4
    assert control.diagonal_fixed_dimension == 5
    assert control.frame_rank == 5
    assert control.distinct_positive_cross_gram_eigenvalue_count == 3
    assert abs(control.minimum_positive_cross_gram_eigenvalue - 0.125) < 1e-12
    assert abs(control.maximum_positive_cross_gram_eigenvalue - 0.375) < 1e-12
    assert not control.normalized_overlap_already_partial_isometry


def test_clifford_fixed_space_polar_is_exact_orientation_analysis_polar() -> None:
    control = audit_clifford_fixed_space_normal_form(
        "S4-POLAR",
        (3, 1),
        (
            ((4,), (3, 1)),
            ((2, 2), (2, 1, 1)),
        ),
    )
    assert control.cross_gram_identity_residual < 1e-12
    assert control.polar_orientation_analysis_residual < 1e-12
    assert control.maximum_diagonal_projector_residual < 1e-12
    assert control.exact_clifford_fixed_space_normal_form_verified


def test_scaling_keeps_self_conjugate_and_cs_gates_open() -> None:
    record = clifford_normal_form_scaling_record(8)
    assert record.orientation_count_log2 == record.copy_count
    assert record.inertia_sign_code_dimension == record.copy_count + 1
    assert record.branch_orbit_dimension_log2 == record.copy_count
    assert record.induced_branch_basis_polynomial
    assert record.ordinary_clifford_orbit_transform_polynomial_if_a_qft_available
    assert not record.self_conjugate_tuple_absence_proved
    assert record.normalized_flat_overlap_singular_amplitude_log2 < -7
    assert not record.ordinary_clifford_labels_compile_cs_polar


def test_report_records_qft_no_free_lunch_without_claiming_hardness() -> None:
    report = run_connected_clifford_normal_form()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["nontrivial_normalized_overlap_control_count"] == 3
    assert report.claim_gate["generic_nonsplit_connected_clifford_normal_form_proved"]
    assert report.claim_gate[
        "clifford_fixed_space_cross_gram_equals_normalized_orientation_frame"
    ]
    assert report.claim_gate[
        "clifford_fixed_space_cross_polar_equals_orientation_polar"
    ]
    assert not report.claim_gate[
        "ordinary_connected_group_qft_labels_compile_cs_polar"
    ]
    assert not report.claim_gate["self_conjugate_split_sectors_resolved"]
    assert not report.claim_gate["direct_matrix_cs_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_has_no_fake_clifford_or_direct_cs_compiler() -> None:
    report = run_connected_clifford_normal_form()
    assert report.headline_metrics["ordinary_clifford_transform_cs_compiler_count"] == 0
    assert report.headline_metrics["direct_matrix_cs_polar_compiler_count"] == 0
    assert report.headline_metrics["complete_orientation_polar_compiler_count"] == 0
    assert report.status == (
        "connected-clifford-normal-form-reconstructs-orientation-cs-polar-open"
    )


def test_report_writer_records_clifford_boundary(tmp_path) -> None:
    path = tmp_path / "clifford_normal_form.json"
    payload = write_connected_clifford_normal_form_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["headline_metrics"]["finite_control_count"] == 3
    assert stored["headline_metrics"][
        "clifford_cross_polar_orientation_polar_identity_count"
    ] == 1
    assert stored["headline_metrics"]["direct_matrix_cs_polar_compiler_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
