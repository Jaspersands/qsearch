import pytest

from coset_hyperoctahedral_free_orbit_canonicalization_boundary import (
    audit_free_orbits,
    build_free_orbit_canonicalization_report,
    canonical_plus_cosets,
    free_orbit_scaling_record,
    write_free_orbit_canonicalization_report,
)


def test_plus_coset_basis_has_half_the_regular_dimension():
    assert len(canonical_plus_cosets(2)) == 12
    assert len(canonical_plus_cosets(3)) == 360
    with pytest.raises(ValueError, match="positive"):
        canonical_plus_cosets(0)


@pytest.mark.parametrize(
    ("half_degree", "copy_count"),
    ((2, 1), (2, 2), (2, 3), (3, 1), (3, 2)),
)
def test_exact_free_tuple_counts_obey_fixed_point_union_bound(
    half_degree, copy_count
):
    control = audit_free_orbits(half_degree, copy_count)
    assert control.exact_permutation_module_control_verified
    assert control.free_tuple_count_divisible_by_group_order
    assert control.free_orbit_count * control.hyperoctahedral_order == (
        control.free_tuple_count
    )
    assert control.exact_nonfree_tuple_fraction <= (
        control.exact_fixed_point_union_upper_bound + 1e-12
    )
    assert control.exact_fixed_point_union_upper_bound <= (
        control.maximum_character_union_upper_bound + 1e-12
    )


def test_free_source_and_alternative_mass_tend_to_one():
    rows = [
        free_orbit_scaling_record(m) for m in (3, 4, 8, 16, 32, 64, 128)
    ]
    assert all(row.asymptotically_free_source_module for row in rows)
    assert all(row.regular_orbit_qft_after_canonicalization_available for row in rows)
    assert all(not row.coherent_orbit_canonicalizer_constructed for row in rows)
    assert all(not row.matrix_hecke_polar_compiled for row in rows)
    assert rows[-1].nonfree_source_fraction_upper_bound < 1e-100
    assert rows[-1].nonfree_alternative_contribution_upper_bound < 1e-50

    with pytest.raises(ValueError, match="at least three"):
        free_orbit_scaling_record(2)


def test_report_exposes_canonicalization_without_claiming_gi_hardness(tmp_path):
    report = build_free_orbit_canonicalization_report(
        finite_specs=((2, 1), (2, 2), (3, 1)),
        scaling_half_degrees=(3, 4, 8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_permutation_module_identity_proved
    assert report.theorem.asymptotically_free_source_proved
    assert report.theorem.free_regular_module_decomposition_proved
    assert report.theorem.alternative_free_mass_proved
    assert not report.theorem.coherent_orbit_canonicalizer_constructed
    assert not report.theorem.matrix_hecke_polar_compiled
    assert not report.theorem.graph_isomorphism_hardness_proved
    assert report.claim_gate["free_source_module_regular_by_orbit"]
    assert not report.claim_gate["average_case_canonicalizer_polynomial"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_free_orbit_canonicalization_report(
        tmp_path / "free-orbit.json",
        finite_specs=((2, 1), (3, 1)),
        scaling_half_degrees=(3, 4, 8),
    )
    assert payload["status"] == (
        "free-regular-source-proved-coherent-canonicalizer-open"
    )
    assert payload["headline_metrics"]["coherent_orbit_canonicalizer_count"] == 0
