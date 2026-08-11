import math

import pytest

from coset_hyperoctahedral_branching_polar_boundary import (
    branch_coherence_control,
    build_coset_hyperoctahedral_branching_polar_report,
    canonical_fixed_point_free_involution,
    hyperoctahedral_elements,
    hyperoctahedral_scaling_record,
    restriction_parity_control,
    wreath_irrep_dimension,
    wreath_irrep_parity_control,
    write_coset_hyperoctahedral_branching_polar_report,
)


def test_wreath_bipartition_dimensions_and_central_parity_balance():
    assert wreath_irrep_dimension(3, (2,), (1,)) == 3
    assert wreath_irrep_dimension(3, (), (2, 1)) == 2
    with pytest.raises(ValueError, match="total size"):
        wreath_irrep_dimension(3, (1,), (1,))

    for half_degree in range(1, 9):
        row = wreath_irrep_parity_control(half_degree)
        assert row.dimension_identity_verified
        assert row.central_parity_balance_verified
        assert row.sum_irrep_dimension_squares == (
            2**half_degree * math.factorial(half_degree)
        )


def test_explicit_wreath_elements_are_the_full_involution_centralizer():
    for half_degree in (1, 2, 3):
        elements = hyperoctahedral_elements(half_degree)
        permutations = {element[0] for element in elements}
        assert len(permutations) == 2**half_degree * math.factorial(half_degree)
        hidden = canonical_fixed_point_free_involution(half_degree)
        assert hidden in permutations


def test_restricted_symmetric_irreps_obey_even_beta_parity_projector():
    for half_degree, partition in (
        (2, (4,)),
        (2, (3, 1)),
        (2, (2, 2)),
        (3, (5, 1)),
        (3, (4, 2)),
        (3, (3, 2, 1)),
    ):
        row = restriction_parity_control(half_degree, partition)
        assert row.centralizer_generation_verified
        assert row.canonical_involution_central_in_subgroup
        assert row.plus_projector_rank_residual == 0
        assert row.maximum_subgroup_commutator_residual < 1e-8
        assert row.one_dimensional_multiplicities_integral_nonnegative
        assert row.parity_projector_is_subgroup_invariant


def test_exact_s6_polar_output_requires_cross_branch_coherence():
    row = branch_coherence_control()
    assert row.control_verified
    assert row.hom_space_multiplicity == 1
    assert row.restriction_map_rank == 1
    assert row.positive_gram_eigenvalues == pytest.approx((7 / 30,))
    assert row.nonzero_target_wreath_sector_count == 2
    assert sorted(row.target_wreath_sector_weights) == pytest.approx([2 / 7, 5 / 7])
    assert row.branch_dephased_output_purity == pytest.approx(29 / 49)
    assert row.coherence_destroyed_by_branch_measurement == pytest.approx(20 / 49)
    assert row.singular_value_basis_change_residual < 1e-10
    assert not row.branch_measurement_preserves_polar_output
    assert not row.unitary_basis_change_alters_singular_values


def test_scaling_separates_wreath_qft_from_large_subgroup_index():
    row = hyperoctahedral_scaling_record(10)
    assert row.hyperoctahedral_qft_polynomial
    assert not row.coherent_isotypic_sampling_requires_multiplicity_table
    assert not row.direct_symmetric_to_hyperoctahedral_tower_index_polynomial
    assert not row.clean_subduction_multiplicity_basis_compiled
    assert not row.normalization_free_fused_polar_compiled


def test_report_removes_isotypic_access_not_polar_obligation(tmp_path):
    report = build_coset_hyperoctahedral_branching_polar_report()
    assert report.theorem.theorem_verified
    assert report.theorem.hyperoctahedral_qft_efficiency_applied
    assert report.theorem.coherent_wreath_isotypic_sampling_constructed
    assert report.theorem.source_projector_as_wreath_parity_filter_proved
    assert not report.theorem.classical_plethysm_table_required_for_isotypic_access
    assert not report.theorem.branch_label_measurement_sufficient_for_polar
    assert not report.theorem.unitary_branching_basis_change_removes_small_singular_scale
    assert not report.theorem.clean_subduction_multiplicity_basis_constructed
    assert not report.theorem.normalization_free_fused_polar_constructed
    assert not report.theorem.general_quantum_circuit_lower_bound_proved
    assert not report.claim_gate["speedup_claim_allowed"]

    hardness = next(
        row
        for row in report.literature_links
        if row["paper_id"] == "arxiv:2002.00788"
    )
    assert "not treated" in hardness["use"]

    payload = write_coset_hyperoctahedral_branching_polar_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "wreath-isotypic-access-closed-coherent-subduction-polar-open"
    )
