import json

from self_dual_wreath_connected_quotient_heisenberg_reduction import (
    audit_parity_quotient,
    connected_quotient_scaling_record,
    parity_quotient_commutator,
    parity_quotient_elements,
    parity_quotient_inverse,
    parity_quotient_multiply,
    run_connected_quotient_heisenberg_reduction,
    write_connected_quotient_heisenberg_reduction_report,
)


def test_parity_quotient_multiplication_is_associative_with_exact_inverses() -> None:
    elements = parity_quotient_elements(2)
    identity = (0, 0, 0)
    for element in elements:
        inverse = parity_quotient_inverse(element)
        assert parity_quotient_multiply(element, inverse) == identity
        assert parity_quotient_multiply(inverse, element) == identity
    for left in elements:
        for middle in elements:
            for right in elements:
                assert parity_quotient_multiply(
                    parity_quotient_multiply(left, middle), right
                ) == parity_quotient_multiply(
                    left, parity_quotient_multiply(middle, right)
                )


def test_orientation_sign_and_branch_commutators_generate_central_pair_bits() -> None:
    copy_count = 4
    orientation_sign = (1, 0, 0)
    for pair_index in range(copy_count):
        branch = (0, 0, 1 << pair_index)
        assert parity_quotient_commutator(orientation_sign, branch) == (
            0,
            1 << pair_index,
            0,
        )


def test_single_pair_quotient_has_dihedral_irrep_profile() -> None:
    control = audit_parity_quotient(1)
    assert control.group_order == 8
    assert control.center_order == 2
    assert control.derived_subgroup_order == 2
    assert control.one_dimensional_irrep_count == 4
    assert control.two_dimensional_irrep_count == 1
    assert control.conjugacy_class_count == 5
    assert control.irrep_dimension_square_sum == 8
    assert control.exact_parity_quotient_classification_verified


def test_four_pair_quotient_has_only_one_and_two_dimensional_irreps() -> None:
    control = audit_parity_quotient(4)
    assert control.group_order == 512
    assert control.center_order == 16
    assert control.derived_subgroup_order == 16
    assert control.one_dimensional_irrep_count == 32
    assert control.two_dimensional_irrep_count == 120
    assert control.conjugacy_class_count == 152
    assert control.maximum_irrep_dimension == 2
    assert control.irrep_dimension_square_sum == 512
    assert control.exact_parity_quotient_classification_verified


def test_scaling_separates_easy_quotient_from_huge_occupied_rank() -> None:
    record = connected_quotient_scaling_record(8)
    assert record.parity_quotient_order_log2 == 2 * record.copy_count + 1
    assert record.maximum_parity_quotient_irrep_dimension == 2
    assert record.native_occupied_cs_rank_threshold_log2 > 60
    assert record.quotient_irrep_to_occupied_rank_log2_ratio < -59
    assert record.parity_quotient_qft_polynomial
    assert record.alternating_product_qft_polynomial
    assert not record.full_connected_group_clifford_transform_compiled
    assert not record.matrix_cs_polar_compiled


def test_report_keeps_alternating_recoupling_and_speedup_gates_false() -> None:
    report = run_connected_quotient_heisenberg_reduction()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["connected_group_parity_quotient_classified"]
    assert report.claim_gate["parity_quotient_qft_polynomial"]
    assert report.claim_gate["all_parity_quotient_irreps_dimension_at_most_two"]
    assert not report.claim_gate[
        "high_rank_cs_multiplicity_can_live_only_in_parity_quotient"
    ]
    assert not report.claim_gate["full_connected_group_clifford_transform_compiled"]
    assert not report.claim_gate[
        "alternating_group_many_way_subduction_polar_compiled"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_records_connected_quotient_boundary(tmp_path) -> None:
    path = tmp_path / "connected_quotient.json"
    payload = write_connected_quotient_heisenberg_reduction_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["status"] == (
        "connected-parity-quotient-solved-alternating-recoupling-open"
    )
    assert stored["headline_metrics"]["finite_control_count"] == 4
    assert stored["headline_metrics"]["parity_quotient_qft_compiler_count"] == 1
    assert stored["headline_metrics"]["alternating_subduction_polar_compiler_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
