import itertools
import math
import random

from semidirect_hms_transfer_boundary import (
    dcp_amplification_scaling,
    dcp_tensor_phase_control,
    dihedral_nonpermutable_subgroup_control,
    expected_uniform_subset_sum_collision_pairs,
    hms_resource_control,
    run_semidirect_hms_transfer_boundary,
    subset_sums_mod,
    unordered_collision_pair_count,
    write_semidirect_hms_transfer_boundary,
)


def test_dhsp_scalarity_does_not_meet_hms_ratio_condition():
    row = hms_resource_control(
        "dcp",
        modulus=1 << 32,
        shift_count=2,
        generator_rank=1,
        interpretation="test",
    )
    assert row.exponent_to_shift_ratio == 1 << 31
    assert row.dominant_rank_factor_log2 == 31.0
    assert not row.scalar_action_alone_certifies_efficiency
    assert not row.paper_parameter_regime_satisfied
    assert not row.asymptotic_family_certificate_supplied


def test_subset_sum_collision_expectation_is_exact_by_exhaustion():
    modulus = 5
    copy_count = 3
    collision_total = 0
    frequency_count = 0
    for frequencies in itertools.product(range(modulus), repeat=copy_count):
        collision_total += unordered_collision_pair_count(
            subset_sums_mod(frequencies, modulus)
        )
        frequency_count += 1
    empirical_exact_average = collision_total / frequency_count
    theorem_average = expected_uniform_subset_sum_collision_pairs(
        modulus, copy_count
    )
    assert math.isclose(empirical_exact_average, theorem_average, abs_tol=1e-12)


def test_tensor_phase_relabeling_is_state_level_not_oracle_level():
    row = dcp_tensor_phase_control(
        "injective",
        modulus=257,
        frequencies=(1, 2, 4, 8),
        coherent_inverse_subset_sum_map_available=True,
    )
    assert row.subset_sum_map_injective
    assert row.relabelled_hms_phase_identity_verified
    assert row.coherent_inverse_subset_sum_map_available
    assert not row.fixed_shift_set_across_fresh_samples
    assert row.direct_product_oracle_branch_rank == 4
    assert row.scalar_hms_oracle_branch_rank == 1
    assert not row.oracle_level_hms_lift_possible
    assert math.isclose(row.exact_normalized_frequency_reuse_probability, 257**-3)


def test_high_apparent_shift_count_enters_collision_regime():
    low_density = dcp_amplification_scaling(128, 64)
    high_density = dcp_amplification_scaling(128, 114)
    assert low_density.low_collision_expectation
    assert not low_density.hms_polylog_shift_count_target_met
    assert high_density.hms_polylog_shift_count_target_met
    assert not high_density.low_collision_expectation
    assert high_density.expected_collision_pairs_log2 > 90
    assert not high_density.free_hms_amplification_certified


def test_collision_expectation_matches_monte_carlo_without_becoming_a_tail_claim():
    rng = random.Random(8305321)
    modulus = 101
    copy_count = 4
    samples = 6000
    observed = 0
    for _ in range(samples):
        frequencies = [rng.randrange(modulus) for _ in range(copy_count)]
        observed += unordered_collision_pair_count(
            subset_sums_mod(frequencies, modulus)
        )
    observed_average = observed / samples
    expected = expected_uniform_subset_sum_collision_pairs(modulus, copy_count)
    assert abs(observed_average - expected) < 0.08


def test_dihedral_reflection_subgroups_fail_permutability_control():
    assert dihedral_nonpermutable_subgroup_control()


def test_report_keeps_every_breakthrough_gate_closed(tmp_path):
    report = run_semidirect_hms_transfer_boundary()
    assert report.theorem.theorem_verified
    assert report.theorem.tensor_phase_identity_proved
    assert report.theorem.collision_expectation_proved
    assert report.theorem.oracle_level_rank_obstruction_proved
    assert report.theorem.varying_set_fourier_sampling_transfer_proved
    assert not report.theorem.dcp_polynomial_algorithm_constructed
    assert report.headline_metrics["dcp_resource_controls_outside_explicit_envelope"] == 2
    assert report.headline_metrics["polylog_ratio_high_collision_scaling_count"] == 3
    assert not report.claim_gate["morales_theorem_directly_solves_dhsp"]
    assert not report.claim_gate["shift_multiplicity_candidate_passes_proof_gate"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_semidirect_hms_transfer_boundary(tmp_path / "report.json")
    assert payload["status"] == "semidirect-hms-transfer-boundary-active"
