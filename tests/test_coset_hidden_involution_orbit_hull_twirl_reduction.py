import math

import pytest

from coset_hidden_involution_orbit_hull_twirl_reduction import (
    audit_orbit_hull_control,
    build_hidden_involution_orbit_hull_report,
    perfect_matching_orbit_hull_scaling_record,
    write_hidden_involution_orbit_hull_report,
)


@pytest.mark.parametrize(
    ("n", "transpositions", "copies"),
    ((3, 1, 1), (3, 1, 2), (4, 2, 1)),
)
def test_orbit_average_equals_twirl_and_support_equals_explicit_hull(
    n, transpositions, copies
):
    row = audit_orbit_hull_control(n, transpositions, copies)
    assert row.finite_control_verified
    assert row.orbit_average_full_twirl_residual < 1e-9
    assert row.maximum_twirl_commutator_residual < 1e-9
    assert row.maximum_stabilizer_projector_commutator_residual < 1e-9
    assert row.support_projector_orbit_hull_residual < 1e-8
    assert row.support_rank == row.explicit_orbit_hull_rank
    assert row.orbit_stabilizer_quotient == row.conjugacy_class_size
    assert row.carrier_invariant_support_verified


def test_fixed_point_free_orbit_stabilizer_is_hyperoctahedral():
    row = perfect_matching_orbit_hull_scaling_record(16)
    assert row.symmetric_group_order == math.factorial(16)
    assert row.hyperoctahedral_stabilizer_order == 2**8 * math.factorial(8)
    assert (
        row.symmetric_group_order
        == row.matching_count * row.hyperoctahedral_stabilizer_order
    )
    assert row.orbit_stabilizer_identity_verified
    assert row.diagonal_conjugation_irrep_label_accessible
    assert not row.individual_hidden_orientation_required
    assert not row.uniform_multiplicity_support_projector_known


def test_report_eliminates_carrier_but_not_multiplicity_obligation(tmp_path):
    report = build_hidden_involution_orbit_hull_report(
        finite_specs=((3, 1, 1), (3, 1, 2), (4, 2, 1)),
        scaling_n_values=(16, 32, 64),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.orbit_hull_identity_proved
    assert report.theorem.schur_support_reduction_proved
    assert report.theorem.carrier_orientation_eliminated_for_binary_support
    assert not report.theorem.multiplicity_support_projector_constructed
    assert not report.claim_gate["individual_hidden_orientation_required_for_binary_support"]
    assert not report.claim_gate["uniform_multiplicity_support_projector_constructed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_hidden_involution_orbit_hull_report(
        tmp_path / "orbit.json",
        finite_specs=((3, 1, 1), (3, 1, 2)),
        scaling_n_values=(16, 32),
    )
    assert payload["status"] == (
        "binary-support-reduced-to-canonical-multiplicity-support"
    )

