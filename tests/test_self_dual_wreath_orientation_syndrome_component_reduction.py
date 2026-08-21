import json

from self_dual_wreath_orientation_homogeneous_space_polar import (
    _group_data,
    omega_multiply,
)
from self_dual_wreath_orientation_syndrome_component_reduction import (
    audit_syndrome_component_reduction,
    omega_syndrome,
    run_syndrome_component_reduction,
    syndrome_component_scaling_record,
    syndrome_representative,
    write_syndrome_component_reduction_report,
)


def test_syndrome_is_a_homomorphism_and_ignores_branch_swaps() -> None:
    _group, _gamma, omega, _branch, _diagonal = _group_data(2, 2)
    for left in omega:
        for right in omega:
            assert omega_syndrome(omega_multiply(left, right)) == (
                omega_syndrome(left) ^ omega_syndrome(right)
            )


def test_explicit_representatives_canonicalize_every_syndrome() -> None:
    n = 3
    copy_count = 3
    for syndrome in range(1 << copy_count):
        representative = syndrome_representative(n, copy_count, syndrome)
        assert omega_syndrome(representative) == syndrome


def test_generated_subgroup_equals_kernel_and_components_match_for_two_pairs() -> None:
    control = audit_syndrome_component_reduction(2, 2)
    assert control.generated_subgroup_order == 32
    assert control.syndrome_kernel_order == 32
    assert control.generated_subgroup_equals_syndrome_kernel
    assert control.component_count == 4
    assert control.physical_component_dimension == 8
    assert control.source_component_dimension == 16
    assert control.maximum_off_syndrome_incidence == 0.0
    assert control.maximum_component_singular_spectrum_residual == 0.0
    assert control.exact_syndrome_component_reduction_verified


def test_nonabelian_component_control_is_not_already_a_polar() -> None:
    control = audit_syndrome_component_reduction(3, 1)
    assert control.component_count == 2
    assert control.maximum_component_singular_spectrum_residual < 1e-12
    assert control.minimum_normalized_component_positive_singular_value < 0.51
    assert control.maximum_normalized_component_positive_singular_value > 0.99
    assert control.minimum_unitary_only_distance_to_component_polar >= 0.49
    assert control.exact_syndrome_component_reduction_verified


def test_scaling_canonicalizes_replication_but_keeps_matrix_polar_open() -> None:
    record = syndrome_component_scaling_record(8)
    assert record.component_count_log2 == record.copy_count
    assert 4.0 <= record.source_to_physical_component_dimension_ratio < 8.0
    assert record.total_support_rank_fraction_lower_bound > 0.8
    assert record.flat_benchmark_normalized_singular_amplitude_log2 < -7
    assert record.syndrome_computation_polynomial
    assert record.zero_component_canonicalization_polynomial
    assert not record.syndrome_only_polar_compiler_proved


def test_report_keeps_syndrome_signal_and_polar_claims_false() -> None:
    report = run_syndrome_component_reduction()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "branch_diagonal_generated_group_equals_syndrome_kernel"
    ]
    assert report.claim_gate[
        "complete_polar_is_repeated_zero_syndrome_component_polar"
    ]
    assert report.claim_gate["syndrome_computation_and_canonicalization_compiled"]
    assert not report.claim_gate["syndrome_is_hidden_label_signal"]
    assert not report.claim_gate["syndrome_only_unitaries_compile_connected_polar"]
    assert not report.claim_gate["connected_component_matrix_cs_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_records_component_reduction(tmp_path) -> None:
    path = tmp_path / "syndrome_components.json"
    payload = write_syndrome_component_reduction_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["status"] == (
        "orientation-polar-reduced-to-one-syndrome-connected-component"
    )
    assert stored["headline_metrics"]["finite_control_count"] == 3
    assert stored["headline_metrics"]["connected_component_matrix_cs_polar_compiler_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
