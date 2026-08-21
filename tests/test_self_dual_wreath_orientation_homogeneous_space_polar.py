import json
import math

from self_dual_wreath_orientation_homogeneous_space_polar import (
    _group_data,
    audit_homogeneous_incidence,
    matrix_multiplicity_scaling_record,
    native_occupied_rank_scaling_record,
    omega_multiply,
    orientation_embedding,
    partition_number,
    run_orientation_homogeneous_space_polar,
    write_orientation_homogeneous_space_polar_report,
)


def test_branch_group_conjugates_zero_diagonal_to_every_orientation() -> None:
    n = 3
    copy_count = 2
    group, _gamma, _omega, branch_subgroup, diagonal_subgroup = _group_data(
        n,
        copy_count,
    )
    for orientation, branch in enumerate(branch_subgroup):
        for element, diagonal in zip(group, diagonal_subgroup):
            conjugate = omega_multiply(omega_multiply(branch, diagonal), branch)
            assert conjugate == (
                orientation_embedding(element, copy_count, orientation),
                0,
            )


def test_homogeneous_incidence_equals_direct_orientation_synthesis() -> None:
    control = audit_homogeneous_incidence(2, 2)
    assert control.source_quotient_dimension == 64
    assert control.physical_quotient_dimension == 32
    assert control.direct_orientation_synthesis_dimension == (32, 64)
    assert control.maximum_homogeneous_incidence_residual == 0.0
    assert control.maximum_left_equivariance_residual == 0.0
    assert control.maximum_frame_moment_residual < 1e-12
    assert control.exact_homogeneous_space_polar_verified


def test_nonabelian_control_preserves_polar_supports() -> None:
    control = audit_homogeneous_incidence(3, 1)
    assert control.omega_order == 432
    assert control.source_quotient_dimension == 72
    assert control.physical_quotient_dimension == 216
    assert control.polar_initial_support_residual < 1e-12
    assert control.polar_final_support_residual < 1e-12
    assert control.exact_homogeneous_space_polar_verified


def test_partition_number_and_matrix_multiplicity_formulas() -> None:
    assert [partition_number(n) for n in range(1, 9)] == [1, 2, 3, 5, 7, 11, 15, 22]
    record = matrix_multiplicity_scaling_record(5)
    group_order = math.factorial(5)
    expected_copy_count = (group_order - 1).bit_length() + 2
    assert record.copy_count == expected_copy_count
    assert record.partition_count == 7
    assert record.maximum_fixed_multiplicity_log2_lower_bound > 30
    assert record.low_multiplicity_physical_dimension_fraction_log2_upper_bound < -24
    assert record.low_multiplicity_source_dimension_fraction_log2_upper_bound < -26
    assert record.matrix_multiplicity_typical_on_both_quotients


def test_exact_frame_moments_force_huge_native_occupied_rank() -> None:
    record = native_occupied_rank_scaling_record(5)
    assert 4.0 <= record.orientation_to_group_ratio < 8.0
    assert record.total_support_rank_fraction_lower_bound > 0.8
    assert record.occupied_rank_threshold_log2 > 15
    assert record.low_occupied_rank_native_frame_mass_log2_upper_bound < -11
    assert record.high_occupied_rank_native_frame_mass_lower_bound > 0.999
    assert record.native_regular_master_large_occupied_rank_proved
    assert not record.physical_conditioned_size_biased_transfer_proved


def test_report_keeps_subduction_compiler_and_speedup_gates_false() -> None:
    report = run_orientation_homogeneous_space_polar()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "complete_regular_master_polar_reduces_to_fixed_space_cs_blocks"
    ]
    assert not report.claim_gate["outer_semidirect_qft_scalarizes_fixed_space_overlap"]
    assert report.claim_gate[
        "occupied_overlap_high_rank_on_native_regular_master_mass"
    ]
    assert not report.claim_gate["occupied_overlap_high_rank_on_native_pgm_mass"]
    assert not report.claim_gate[
        "normalization_one_fixed_space_cs_transform_compiled"
    ]
    assert not report.claim_gate["complete_natural_orientation_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_preserves_claim_boundary(tmp_path) -> None:
    path = tmp_path / "homogeneous_polar.json"
    payload = write_orientation_homogeneous_space_polar_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["claim_gate"] == payload["claim_gate"]
    assert stored["status"] == (
        "orientation-polar-flattened-to-matrix-fixed-space-cs-transform"
    )
    assert stored["headline_metrics"]["single_homogeneous_incidence_theorem_count"] == 1
    assert stored["headline_metrics"][
        "native_regular_master_occupied_rank_theorem_count"
    ] == 1
    assert stored["headline_metrics"]["complete_orientation_polar_compiler_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
