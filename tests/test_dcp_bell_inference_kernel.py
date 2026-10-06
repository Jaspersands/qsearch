from fractions import Fraction

import pytest

from dcp_carry_packets import compile_packet
from dcp_bell_inference_kernel import (
    _noisy_physical_source_control, _weighted_systematic_control, character_kernel_controls,
    detector_repetition_countercontrol,
    fixed_chart_order_two_alias_control,
    cross_secret_kernel, noisy_transcript_certificate, statistical_query_certificate,
    systematic_noisy_source_mean,
)
from dcp_full_bell_source_moments import systematic_source_mean


def read(v):
    return Fraction(v["sign"] * int(v["numerator_hex"], 16), int(v["denominator_hex"], 16))


def test_cross_secret_kernels_cover_all_small_vectors_not_only_independent_parities():
    controls = character_kernel_controls()
    assert len(controls["records"]) == 912
    assert all(read(r["mean_relative_cross_collision"]) >= 1 for r in controls["records"])
    assert any(r["modulus"] == 128 and r["secret_s"] == (1, 0) and r["secret_t"] == (3, 0)
               and read(r["mean_relative_cross_collision"]) == 1 for r in controls["records"])


def test_negation_is_the_exact_kernel_alias_and_order_two_is_not_odd_case():
    packets = [compile_packet([[1, 1, 1]], 8), compile_packet([[1, 1, 0]], 8)]
    diagonal = cross_secret_kernel(*packets, [1], [1])
    negative = cross_secret_kernel(*packets, [1], [3])
    assert diagonal["source_mean_relative_cross_collision"] == negative["source_mean_relative_cross_collision"]
    assert read(cross_secret_kernel(*packets, [0], [2])["centered_likelihood_inner_product"]) == 0
    assert cross_secret_kernel(*packets, [2], [2])["evaluation_cost_class"] == "polynomial_binary_rank"


def test_different_orbits_need_no_exponential_mask_enumeration():
    packet = compile_packet([[1] * 65], 128)
    row = cross_secret_kernel(packet, packet, [1], [3])
    assert read(row["source_mean_relative_cross_collision"]) == 1
    assert row["public_masks_enumerated"] == 0
    with pytest.raises(ValueError, match="exponential"):
        cross_secret_kernel(packet, packet, [1], [1])


def test_noise_kernel_is_checked_against_complete_physical_higher_source():
    control = _noisy_physical_source_control()
    assert control["complete_higher_label_tables"] == 256
    assert len(control["records"]) == 16
    assert read(control["records"][5]["mean_relative_cross_collision"]) == Fraction(41, 32)


def test_weighted_native_formula_matches_complete_small_low_source_and_clean_limit():
    _weighted_systematic_control()
    for n in (1, 4, 16):
        clean = systematic_source_mean(n)["conditional_mean_relative_full_collision"]
        old = Fraction(clean["sign"] * int(clean["numerator_hex"], 16), 1 << clean["denominator_binary_exponent"])
        assert read(systematic_noisy_source_mean(n)["conditional_mean_relative_full_collision"]) == old
        assert read(systematic_noisy_source_mean(n, Fraction(1, 2))["conditional_mean_relative_full_collision"]) == 1


def test_sq_gate_does_not_claim_raw_sample_or_quantum_hardness():
    row = statistical_query_certificate(32, 32, 32**2, Fraction(1, 32**2))
    assert read(row["adversarial_valid_sq_oracle_uniform_orbit_success_upper_bound"]) < Fraction(1, 10**20)
    assert not row["raw_sample_algorithms_covered"]
    assert not row["joint_multisample_queries_covered"]
    assert not row["classical_hardness_or_quantum_speedup_claim"]


def test_full_noisy_transcript_gate_charges_native_rejection_and_even_secret_exception():
    row = noisy_transcript_certificate(256, 256, Fraction(1, 8), 256**2)
    assert row["orbit_success_below_one_over_100"]
    assert row["original_phase_states_consumed"] == 6 * 256**3
    assert read(row["uniform_prior_order_at_most_two_exception_mass"]) == Fraction(1, 64**256)
    assert not row["arbitrary_decoders_or_other_measurements_closed"]
    assert not row["source"]["correlated_native_phase_errors_covered"]
    clean = noisy_transcript_certificate(16, 16, 0, 16**2)
    assert not clean["orbit_success_below_one_over_100"]


def test_invalid_model_parameters_are_not_silently_reinterpreted():
    for epsilon in (Fraction(-1, 8), Fraction(3, 4)):
        with pytest.raises(ValueError):
            systematic_noisy_source_mean(4, epsilon)
    with pytest.raises(ValueError):
        statistical_query_certificate(4, 8, 1, 0)
    with pytest.raises(ValueError):
        noisy_transcript_certificate(4, 6, 0, 1)


def test_detector_only_repetition_kills_a_false_general_noise_obstruction():
    row = detector_repetition_countercontrol(Fraction(1, 8), 7, 256)
    assert read(row["majority_vote_effective_flip_probability"]) < Fraction(1, 100)
    assert not row["remains_in_uniformization_regime"]
    assert not row["repairs_pre_hadamard_phase_errors"]
    assert row["additional_cnot_gates"] == 1536
    assert row["measured_bits"] == 1792
    for repetitions in (0, 2):
        with pytest.raises(ValueError):
            detector_repetition_countercontrol(Fraction(1, 8), repetitions, 256)


def test_zero_centered_norm_even_secrets_can_alias_outside_negation_on_a_fixed_chart():
    row = fixed_chart_order_two_alias_control()
    assert row["not_same_negation_orbit"]
    assert row["both_combined_binary_quadratic_ranks"] == [2, 2]
    assert read(row["both_centered_likelihood_squared_norms"]) == 0
    assert row["bounded_physical_full_law_checks"] == 32
    assert row["full_rank_quadratic_derivation_not_exhaustive_high_source"]
