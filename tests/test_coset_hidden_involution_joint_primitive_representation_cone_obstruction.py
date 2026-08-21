import sympy as sp

from coset_hidden_involution_joint_primitive_representation_cone_obstruction import (
    alternating_hook_vector,
    audit_hook_kernel,
    build_representation_cone_report,
    trivial_restriction_control,
    write_representation_cone_report,
)
from coset_hidden_involution_paired_tower_joint_primitive_projector import (
    Young_down_incidence,
    Young_primitive_projector,
)
from representation_obstruction import integer_partitions


def test_alternating_hook_vector_is_in_Young_down_kernel():
    for rank in range(2, 10):
        down = Young_down_incidence(rank)
        vector = alternating_hook_vector(rank)
        assert down * vector == sp.zeros(down.rows, 1)
        assert sum(value != 0 for value in vector) == rank


def test_top_column_has_an_exact_negative_adjacent_hook_entry():
    for rank in range(2, 10):
        partitions = list(integer_partitions(rank))
        index = {partition: i for i, partition in enumerate(partitions)}
        projector = Young_primitive_projector(rank)
        diagonal = projector[index[(rank,)], index[(rank,)]]
        negative = projector[index[(rank - 1, 1)], index[(rank,)]]
        assert diagonal > 0
        assert negative == -diagonal
        row = audit_hook_kernel(rank)
        assert row.alternating_hook_in_down_kernel
        assert row.top_cover_sum_in_up_image
        assert row.adjacent_coefficient_is_negative_diagonal
        assert not row.projector_preserves_nonnegative_cone


def test_trivial_restriction_is_an_all_rank_physical_counterexample():
    for half_degree in range(2, 9):
        row = trivial_restriction_control(half_degree)
        assert row.branching_vector_is_single_trivial_irrep
        assert row.occupied_branch_count == 1
        assert row.maximum_branching_multiplicity == 1
        assert row.repeated_branch_count == 0
        assert row.primitive_residual_nonzero
        assert row.primitive_residual_has_negative_coefficient
        assert not row.primitive_residual_is_nonnegative_integral_branching_vector
        assert row.physical_missing_copy_dimension == 0


def test_nonzero_coefficient_residual_is_not_promoted_to_source_mass():
    report = build_representation_cone_report()
    theorem = report.theorem
    assert theorem.alternating_hook_kernel_proved
    assert theorem.all_rank_negative_projector_entry_proved
    assert not theorem.joint_projector_preserves_representation_cone
    assert not theorem.nonzero_primitive_residual_implies_physical_missing_copy
    assert not theorem.primitive_coefficient_norm_is_physical_source_mass
    assert not theorem.polynomial_query_label_reflection_is_physical_measurement
    assert not theorem.within_mu_commutant_route_obstructed
    assert not theorem.full_nonequivariant_subduction_route_obstructed
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_adversarial_audit_preserves_the_open_physical_routes():
    report = build_representation_cone_report()
    assert report.claim_gate["within_mu_commutant_route_remains_open"]
    assert report.claim_gate["full_nonequivariant_subduction_route_remains_open"]
    assert not report.claim_gate["physical_joint_primitive_measurement_compiled"]
    assert not report.claim_gate["primitive_residual_is_physical_source_mass"]
    assert all(row["resolved"] for row in report.adversarial_audit)


def test_live_representation_cone_report_is_json_serializable(tmp_path):
    output = tmp_path / "representation-cone.json"
    payload = write_representation_cone_report(output)
    assert output.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["status"] == "joint-primitive-coefficient-projector-diagnostic-only"
    assert not payload["claim_gate"]["speedup_claim_allowed"]
