from coset_hidden_involution_matching_charge_cs_correlation import (
    audit_matching_charge_CS_correlation,
    build_matching_charge_CS_correlation_report,
    write_matching_charge_CS_correlation_report,
)


def test_exact_three_source_invariant_block_construction():
    invariant, _ = audit_matching_charge_CS_correlation()
    assert invariant.repeated_irrep_dimension == 225
    assert invariant.S9_commutant_dimension == 2
    assert invariant.S8_commutant_dimension == 7
    assert invariant.point_orbit_candidate_count == 9
    assert invariant.standard_standard_A_invariant_dimension == 6
    assert invariant.maximum_A_orthonormality_residual < 1e-9
    assert invariant.maximum_A_generator_invariance_residual < 1e-9
    assert invariant.maximum_B_projection_gram_residual < 1e-9
    assert invariant.maximum_B_K_generator_invariance_residual < 1e-9
    assert invariant.maximum_B_source_parity_residual < 1e-9
    assert invariant.construction_verified


def test_CS_block_is_full_rank_and_nonflat():
    _, control = audit_matching_charge_CS_correlation()
    assert control.occupied_CS_rank == 6
    assert control.minimum_squared_principal_cosine > 0.09
    assert control.maximum_squared_principal_cosine > 0.23
    assert control.principal_cosine_squared_range > 0.14
    assert control.principal_spectrum_nonflat


def test_matching_charge_is_nontrivial_and_correlated_with_CS():
    _, control = audit_matching_charge_CS_correlation()
    assert control.matching_charge_distinct_compressed_eigenvalue_count == 6
    assert control.matching_charge_compression_frobenius_norm > 0.1
    assert control.matching_charge_occupied_subspace_leakage_norm > 0.1
    assert control.matching_charge_CS_commutator_norm > 1e-3
    assert control.matching_charge_centered_CS_correlation > 0.2
    assert control.matching_charge_incremental_regression_R2 > 1e-3
    assert control.matching_charge_nontrivial_in_occupied_block
    assert control.matching_charge_correlates_with_CS_operator
    assert not control.matching_charge_diagonalizes_CS_operator


def test_report_preserves_finite_only_and_speedup_boundaries():
    report = build_matching_charge_CS_correlation_report()
    assert report.theorem.exact_invariant_space_construction_verified
    assert report.theorem.full_rank_nonflat_matrix_CS_block_verified
    assert report.theorem.D_adds_branch_copy_label_verified
    assert report.theorem.D_nontrivial_on_occupied_CS_space_verified
    assert report.theorem.finite_D_CS_correlation_verified
    assert not report.theorem.D_diagonalizes_finite_CS_operator
    assert not report.theorem.asymptotic_natural_CS_correlation_proved
    assert not report.theorem.source_likelihood_decoder_constructed
    assert not report.theorem.coherent_subduction_transform_compiled
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed


def test_live_report_is_json_serializable(tmp_path):
    output_path = tmp_path / "matching-charge-cs-correlation.json"
    payload = write_matching_charge_CS_correlation_report(output_path)
    assert output_path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["correlation_control"][
        "matching_charge_distinct_compressed_eigenvalue_count"
    ] == 6
