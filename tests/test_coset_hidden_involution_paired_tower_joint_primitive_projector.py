import sympy as sp

from coset_hidden_involution_colour_resolved_paired_tower_boundary import (
    joint_primitive_dimension,
)
from coset_hidden_involution_paired_tower_joint_primitive_projector import (
    Young_down_incidence,
    Young_primitive_projector,
    audit_Young_primitive_projector,
    build_joint_primitive_projector_report,
    joint_primitive_projector_control,
    joint_primitive_scaling_record,
    partition_difference,
    partition_number,
    write_joint_primitive_projector_report,
)
from representation_obstruction import integer_partitions


def test_fast_partition_numbers_match_exact_partition_enumeration():
    for rank in range(21):
        assert partition_number(rank) == len(integer_partitions(rank))
        assert partition_difference(rank) == (
            len(integer_partitions(rank))
            - (len(integer_partitions(rank - 1)) if rank else 0)
        )


def test_Young_down_laplacian_has_exact_differential_poset_spectrum():
    for rank in range(1, 9):
        row = audit_Young_primitive_projector(rank)
        assert row.observed_laplacian_spectrum == (
            row.expected_laplacian_spectrum
        )
        assert row.primitive_kernel_dimension == (
            row.expected_primitive_kernel_dimension
        )
        assert row.minimum_positive_laplacian_eigenvalue >= 1
        assert row.maximum_laplacian_eigenvalue == rank
        assert row.normalized_zero_gap >= 1.0 / rank
        assert row.exact_spectrum_verified


def test_projector_polynomial_is_exactly_the_down_kernel_projector():
    for rank in range(1, 9):
        down = Young_down_incidence(rank)
        projector = Young_primitive_projector(rank)
        row = audit_Young_primitive_projector(rank)
        assert projector * projector == projector
        assert down * projector == sp.zeros(down.rows, projector.cols)
        assert projector.rank() == row.primitive_kernel_dimension
        assert row.exact_projector_idempotence_verified
        assert row.exact_projector_image_equals_down_kernel


def test_joint_primitive_rank_is_tensor_sum_of_Young_kernels():
    for half_degree in range(2, 13):
        row = joint_primitive_projector_control(half_degree)
        assert row.joint_primitive_dimension_from_projectors == (
            joint_primitive_dimension(half_degree)
        )
        assert row.minimum_sector_normalized_zero_gap >= (
            1.0 / half_degree
        )
        assert row.exact_direct_sum_tensor_projector_rank_verified
        assert row.polynomial_query_projector_specified


def test_scaling_preserves_inverse_polynomial_gap_and_exponential_label_space():
    rows = [
        joint_primitive_scaling_record(half_degree)
        for half_degree in (8, 16, 32, 64, 128)
    ]
    assert all(
        row.normalized_laplacian_gap_lower_bound == 1.0 / row.half_degree
        for row in rows
    )
    assert all(
        row.sparse_query_reflection_order == row.half_degree for row in rows
    )
    assert all(row.label_space_projector_polynomial_query for row in rows)
    assert all(
        not row.reversible_partition_oracle_gate_compiled for row in rows
    )
    assert all(not row.ambient_branching_copy_isometry_compiled for row in rows)
    assert all(
        right.joint_primitive_label_bits > left.joint_primitive_label_bits
        for left, right in zip(rows, rows[1:])
    )


def test_report_keeps_coefficient_projector_separate_from_physical_lift():
    report = build_joint_primitive_projector_report()
    assert report.theorem.exact_all_rank_Young_spectrum_proved
    assert report.theorem.exact_primitive_projector_polynomial_proved
    assert report.theorem.exact_joint_primitive_projector_proved
    assert report.theorem.polynomial_query_label_reflection_proved
    assert not report.theorem.reversible_partition_oracle_gate_compiled
    assert not report.theorem.ambient_branching_copy_isometry_compiled
    assert not report.theorem.source_aware_normalized_subduction_transform_compiled
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
    assert report.theorem.theorem_verified
    assert report.status == (
        "paired-tower-joint-primitive-coefficient-projector-diagnostic-only"
    )
    assert not report.claim_gate[
        "branching_multiplicity_vector_is_physical_label_state"
    ]
    assert not report.claim_gate["physical_joint_primitive_reflection_compiled"]


def test_live_joint_primitive_report_is_json_serializable(tmp_path):
    output = tmp_path / "joint-primitive-projector.json"
    payload = write_joint_primitive_projector_report(output)
    assert output.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["claim_gate"][
        "polynomial_query_joint_primitive_reflection_proved"
    ]
    assert not payload["claim_gate"][
        "ambient_branching_copy_isometry_compiled"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
