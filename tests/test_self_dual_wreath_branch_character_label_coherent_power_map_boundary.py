import math

from self_dual_wreath_branch_character_label_coherent_power_map_boundary import (
    audit_cyclic_label_retention,
    audit_plancherel_normalization,
    audit_symmetric_coset_label_superselection,
    label_coherence_scaling_record,
    plancherel_inverse_normalization_mean,
    run_label_coherent_power_map_boundary,
)


def test_coset_state_has_exact_irrep_label_superselection():
    control = audit_symmetric_coset_label_superselection(3)
    assert control.exact_irrep_label_block_diagonality_verified
    assert control.maximum_cross_irrep_block_norm < 1e-9
    assert control.coset_state_trace_residual < 1e-10


def test_cyclic_one_pair_matching_block_keeps_inverse_normalization():
    control = audit_cyclic_label_retention(3, (2,))
    assert control.exact_label_retention_identity_verified
    assert control.nonzero_output_blocks_per_input == 3
    assert math.isclose(control.expected_nonzero_block_mass, 1 / 3)
    assert math.isclose(control.mean_matching_physical_block_mass, 1 / 9)
    assert math.isclose(
        control.mean_matching_physical_block_mass,
        control.inverse_normalization_squared,
    )


def test_cyclic_two_pair_full_direct_sum_is_norm_one_but_matching_mass_is_tiny():
    control = audit_cyclic_label_retention(5, (2, 1))
    assert control.exact_label_retention_identity_verified
    assert control.nonzero_output_blocks_per_input == 5**3
    assert math.isclose(control.expected_nonzero_block_mass, 5**-3)
    assert math.isclose(control.mean_matching_physical_block_mass, 5**-4)


def test_plancherel_inverse_normalization_formula_for_cyclic_group():
    assert math.isclose(
        plancherel_inverse_normalization_mean((1, 1, 1, 1, 1), 2),
        5**-4,
    )


def test_nonabelian_plancherel_formula_matches_brute_force():
    control = audit_plancherel_normalization("S3", (1, 1, 2), 2)
    assert control.upper_bound_verified
    assert control.exact_formula_residual < 1e-12
    assert control.exact_inverse_normalization_mean <= control.universal_upper_bound


def test_natural_scaling_rejects_label_coherence_cancellation():
    row = label_coherence_scaling_record(16)
    assert row.copy_count == math.ceil(3 * math.log2(math.factorial(16))) + 2
    assert row.log2_inverse_normalization_mean_upper_bound < 0
    assert row.label_coherence_cancellation_superpolynomially_rejected


def test_report_keeps_whole_sum_and_speedup_claims_closed():
    report = run_label_coherent_power_map_boundary()
    assert report.theorem.theorem_verified
    assert report.claim_gate["label_coherence_escape_rejected"]
    assert not report.claim_gate["whole_quadrant_sum_factorized"]
    assert not report.claim_gate["direct_equivariant_multiplier_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
