import pytest

from coset_hidden_involution_matrix_hecke_transfer_reduction import (
    audit_matrix_hecke_transfer,
    build_matrix_hecke_transfer_report,
    matrix_hecke_scaling_record,
    write_matrix_hecke_transfer_report,
)


@pytest.mark.parametrize("copy_count", (1, 2))
def test_direct_transfer_matches_matrix_hecke_gram(copy_count):
    control = audit_matrix_hecke_transfer(copy_count)
    assert control.finite_control_verified
    assert control.scalar_branch_hecke_dimension == 2
    assert control.vector_bundle_commutant_dimension == (
        3 * 9**copy_count + 1
    ) // 2
    assert control.matrix_valued_extension_noncommutative
    assert control.maximum_gram_formula_residual < 1e-9
    assert control.maximum_equivariance_residual < 1e-9
    assert all(
        sector.exact_matrix_hecke_transfer_verified
        for sector in control.sectors
    )


def test_one_copy_sector_dimensions_and_ranks_are_source_specific():
    control = audit_matrix_hecke_transfer(1)
    sectors = {sector.irrep_name: sector for sector in control.sectors}
    assert sectors["trivial"].source_multiplicity == 2
    assert sectors["trivial"].physical_multiplicity == 3
    assert sectors["trivial"].observed_transfer_rank == 2
    assert sectors["sign"].source_multiplicity == 1
    assert sectors["sign"].physical_multiplicity == 1
    assert sectors["sign"].observed_transfer_rank == 1
    assert sectors["standard"].source_multiplicity == 3
    assert sectors["standard"].physical_multiplicity == 1
    assert sectors["standard"].observed_transfer_rank == 1


def test_matrix_hecke_growth_dwarfs_scalar_branch_transform():
    rows = [matrix_hecke_scaling_record(k) for k in (1, 2, 8, 32, 128)]
    assert rows[0].vector_bundle_commutant_dimension_decimal == "14"
    assert all(not row.scalar_spherical_transform_sufficient for row in rows)
    assert all(not row.matrix_hecke_basis_compiled for row in rows)
    assert all(not row.structured_transfer_polar_compiled for row in rows)
    assert rows[-1].vector_to_scalar_dimension_ratio > rows[1].vector_to_scalar_dimension_ratio

    with pytest.raises(ValueError, match="positive"):
        matrix_hecke_scaling_record(0)
    with pytest.raises(ValueError, match="positive"):
        audit_matrix_hecke_transfer(0)


def test_report_isolates_matrix_operator_without_claiming_compiler(tmp_path):
    report = build_matrix_hecke_transfer_report(
        finite_copy_counts=(1, 2),
        scaling_copy_counts=(1, 2, 8, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_transfer_formula_proved
    assert report.theorem.matrix_valued_hecke_reduction_proved
    assert not report.theorem.scalar_spherical_transform_sufficient
    assert not report.theorem.uniform_matrix_hecke_basis_compiled
    assert not report.theorem.structured_multiplicity_polar_compiled
    assert not report.theorem.physical_to_source_lift_compiled
    assert report.claim_gate[
        "source_specific_physical_multiplicity_operator_isolated"
    ]
    assert not report.claim_gate["scalar_matching_association_scheme_sufficient"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_matrix_hecke_transfer_report(
        tmp_path / "matrix-hecke.json",
        finite_copy_counts=(1,),
        scaling_copy_counts=(1, 2, 8),
    )
    assert payload["status"] == (
        "matrix-hecke-transfer-formalized-structured-polar-open"
    )
    assert payload["headline_metrics"][
        "uniform_matrix_hecke_basis_compiler_count"
    ] == 0
