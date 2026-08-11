import pytest

from coset_hidden_involution_multiplicity_support_obstruction import (
    audit_multiplicity_support_control,
    build_multiplicity_support_obstruction_report,
    carrier_algebra_boundary_record,
    write_multiplicity_support_obstruction_report,
)


@pytest.mark.parametrize(
    ("n", "transpositions", "copies"),
    ((3, 1, 1), (3, 1, 2), (3, 1, 3), (4, 2, 2)),
)
def test_proper_multiplicity_support_refutes_carrier_label_only_compiler(
    n, transpositions, copies
):
    row = audit_multiplicity_support_control(n, transpositions, copies)
    assert row.finite_control_verified
    assert row.proper_support_sector_count > 0
    assert row.group_algebra_only_support_compiler_refuted_finitely
    assert row.irrep_label_total_variation < row.full_helstrom_trace_distance
    assert row.isotypic_completeness_residual < 1e-9
    assert row.maximum_isotypic_idempotence_residual < 1e-8
    assert sum(sector.support_intersection_rank for sector in row.sectors) == (
        row.support_rank
    )


def test_s3_diagonal_irrep_label_has_exactly_zero_binary_signal():
    for copies in (1, 2, 3):
        row = audit_multiplicity_support_control(3, 1, copies)
        assert row.irrep_label_total_variation == pytest.approx(0.0, abs=1e-12)
        assert row.full_helstrom_trace_distance > 0.1


def test_s4_threshold_has_proper_support_in_every_irrep_sector():
    row = audit_multiplicity_support_control(4, 2, 2)
    assert row.irrep_sector_count == 5
    assert row.proper_support_sector_count == 5
    assert row.full_support_sector_count == 0
    assert row.zero_support_sector_count == 0
    assert row.irrep_label_total_variation == pytest.approx(1 / 6)
    assert row.full_helstrom_trace_distance == pytest.approx(3 / 8)


def test_scaling_boundary_does_not_promote_finite_proper_support():
    row = carrier_algebra_boundary_record(64)
    assert row.subgroup_action_on_global_multiplicity == "identity"
    assert not row.carrier_only_compiler_sufficient
    assert not row.scalable_proper_support_sector_proved
    assert not row.commutant_side_primitive_constructed


def test_report_requires_commutant_primitive_without_claiming_scaling_no_go(tmp_path):
    report = build_multiplicity_support_obstruction_report(
        finite_specs=((3, 1, 1), (3, 1, 2), (4, 2, 2)),
        scaling_n_values=(16, 32, 64),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.diagonal_group_actions_are_identity_on_multiplicity
    assert report.theorem.proper_support_requires_commutant_side_operation
    assert not report.theorem.scalable_proper_support_theorem_proved
    assert not report.theorem.commutant_support_compiler_constructed
    assert not report.claim_gate["stabilizer_subgroup_qft_alone_sufficient"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_multiplicity_support_obstruction_report(
        tmp_path / "multiplicity.json",
        finite_specs=((3, 1, 1), (3, 1, 2)),
        scaling_n_values=(16, 32),
    )
    assert payload["status"] == (
        "carrier-and-subgroup-label-only-support-route-refuted-finitely"
    )

