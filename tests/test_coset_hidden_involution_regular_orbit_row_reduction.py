import pytest

from coset_hidden_involution_regular_orbit_row_reduction import (
    audit_regular_orbit_row_reduction,
    build_regular_orbit_row_report,
    regular_orbit_row_scaling_record,
    write_regular_orbit_row_report,
)


def test_s3_free_source_becomes_regular_orbit_rows():
    control = audit_regular_orbit_row_reduction(2)
    assert control.exact_regular_orbit_row_reduction_verified
    assert control.group_order == 6
    assert control.stabilizer_order == 2
    assert control.free_fiber_tuple_count == 8
    assert control.free_fiber_orbit_count == 4
    assert control.regular_source_dimension == 24
    assert control.synthesis_rank == 20
    assert control.source_kernel_dimension == 4
    assert control.maximum_column_norm_residual < 1e-9
    assert control.maximum_covariance_residual < 1e-9
    assert control.maximum_group_convolution_residual < 1e-9
    assert control.nonzero_cross_orbit_block_count > 0
    assert control.maximum_cross_orbit_overlap == pytest.approx(0.25)
    assert not control.canonicalization_alone_is_polar


def test_regular_row_reduction_keeps_physical_polar_open():
    rows = [
        regular_orbit_row_scaling_record(m)
        for m in (3, 4, 8, 16, 32, 64, 128)
    ]
    assert all(row.induced_regular_source_normal_form_available for row in rows)
    assert all(row.symmetric_group_qft_available for row in rows)
    assert all(not row.hyperoctahedral_cg_required_on_trimmed_source for row in rows)
    assert all(row.orbit_representative_row_frame_formalized for row in rows)
    assert all(not row.orbit_representative_row_polar_compiled for row in rows)
    assert all(not row.physical_label_erasure_compiled for row in rows)
    assert rows[-1].trimmed_alternative_success_lower_bound == 1.0


def test_report_removes_wreath_fusion_not_row_polar(tmp_path):
    report = build_regular_orbit_row_report(
        scaling_half_degrees=(3, 4, 8, 16, 32)
    )
    assert report.theorem.theorem_verified
    assert report.theorem.induced_regular_identity_proved
    assert report.theorem.regular_source_basis_compiled_on_trimmed_mass
    assert not report.theorem.hyperoctahedral_cg_required_on_trimmed_mass
    assert report.theorem.matrix_group_convolution_reduction_proved
    assert not report.theorem.orbit_representative_row_polar_compiled
    assert not report.theorem.physical_label_erasure_compiled
    assert not report.theorem.hidden_involution_algorithm_constructed
    assert not report.claim_gate[
        "generic_hyperoctahedral_cg_required_on_trimmed_source"
    ]
    assert not report.claim_gate["orbit_representative_row_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_regular_orbit_row_report(
        tmp_path / "regular-row.json",
        scaling_half_degrees=(3, 4, 8),
    )
    assert payload["status"] == (
        "regular-orbit-row-frame-reduced-physical-row-polar-open"
    )
    assert payload["headline_metrics"][
        "orbit_representative_row_polar_compiler_count"
    ] == 0
