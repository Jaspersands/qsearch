from fractions import Fraction

import pytest

from dcp_fourier_noise_decoder_bound import (
    boolean_block_collision_certificate, boolean_envelope_native_certificate, collision_decoder_certificate,
    fourier_noise_distribution, run_controls,
)
from dcp_physical_phase_noise import read


def test_collision_bound_is_exact_and_does_not_assume_efficient_decoder():
    row = collision_decoder_certificate(16, 4, [Fraction(3, 2)] * 2)
    assert read(row["mean_correct_secret_probability_squared_upper_bound"]) == Fraction(9, 64)
    assert row["unbounded_computation_or_quantum_processing_of_classical_input_allowed"]
    assert not row["decoder_receiving_coherent_noise_purification_is_bounded"]


def test_zero_information_source_has_exact_uniform_secret_guess_probability_squared_bound():
    # The collision converse is not always tight: uniform noise has optimal1/G,
    # whereas this general Cauchy bound only gives1/sqrt(G).
    row = collision_decoder_certificate(32, 8, [1] * 4)
    assert read(row["mean_correct_secret_probability_squared_upper_bound"]) == Fraction(1, 32)


def test_full_observation_information_and_excess_samples_can_make_bound_vacuous():
    assert read(collision_decoder_certificate(4, 4, [4])["mean_correct_secret_probability_squared_upper_bound"]) == 1
    row = boolean_envelope_native_certificate(2, 4, 64)
    assert row["conservative_correct_probability_dyadic_exponent"] == 0
    assert not row["general_quantum_or_native_DCP_decoder_bounded"]


def test_native_width_shortcut_fails_with_exponential_probability_bound():
    rows = [boolean_envelope_native_certificate(n, 4*n+1, n*(4*n+1)+16) for n in (8, 16, 32)]
    assert [r["conservative_correct_probability_dyadic_exponent"] for r in rows] == [48, 203, 820]
    assert all(not r["unlimited_runtime_removes_this_information_obstruction"] for r in rows)


def test_actual_envelope_noise_and_optimal_decoders_obey_scoped_bound():
    report = run_controls()
    assert len(report["complete_envelope_collision_controls"]) == 15
    assert len(report["exhaustive_optimal_classical_decoder_controls"]) == 6
    for row in report["exhaustive_optimal_classical_decoder_controls"]:
        assert row["actual_exhaustive_optimal_classical_correct_probability"] <= row["collision_correct_probability_upper_bound"] + 1e-10
    assert not report["claim_gate"]["all_quantum_subset_sum_algorithms_ruled_out"]


def test_entangled_boolean_envelopes_do_not_beat_tensor_collision_bound():
    report = run_controls()
    rows = report["entangled_Boolean_block_controls"]
    assert len(rows) == 15
    for row in rows:
        assert row["q_to_m_times_Fourier_intensity_collision"] <= row["tensor_bound"] + 1e-9
        assert abs(row["q_to_m_times_Fourier_intensity_collision"] - row["independent_coefficient_additive_energy"]) < 1e-9
        if row["amplitude_family"] == "product_balanced":
            assert abs(row["q_to_m_times_Fourier_intensity_collision"] - row["tensor_bound"]) < 1e-9
    certificate = boolean_block_collision_certificate(8, 16)
    assert read(certificate["q_to_m_times_Fourier_intensity_collision_upper_bound"]) == Fraction(3,2)**16
    assert not certificate["coordinate_noise_independence_required"]
    assert not certificate["generic_subgroup_covariant_quantum_measurement_ruled_out"]


def test_matrix_adaptive_amplitudes_allowed_but_native_subgroup_measurement_not_ruled_out():
    row = boolean_envelope_native_certificate(16, 65, 1056)
    assert row["arbitrary_entangled_amplitudes_and_correlated_Fourier_noise_allowed"]
    assert row["envelope_may_depend_on_public_matrix_A"]
    assert not row["envelope_may_depend_on_unknown_secret"]
    assert not row["A_adaptive_subgroup_covariant_measurements_are_bounded"]
    with pytest.raises(ValueError):
        boolean_block_collision_certificate(2, 16)


def test_actual_subgroup_coherent_measurement_beats_measured_noise_bound_on_rare_labels():
    rows = run_controls()["native_subgroup_measurement_scope_countercontrols"]
    assert len(rows) == 3
    for row in rows:
        assert row["actual_coherent_QFT_correct_probability_every_secret"] > 1-1e-10
        assert row["measured_full_coordinate_Fourier_noise_decoder_bound"] < 1
        assert row["IID_native_literal_label_pattern_probability_dyadic_exponent"] == row["modulus_bits"]**2
        assert not row["scalable_native_label_selector_or_quantum_algorithm_supplied"]


@pytest.mark.parametrize("arguments", [(0, 4, [1]), (4, 1, [1]), (4, 4, []), (4, 4, [0]), (4, 4, [5])])
def test_invalid_collision_certificates_rejected(arguments):
    with pytest.raises(ValueError):
        collision_decoder_certificate(*arguments)


def test_invalid_envelope_and_native_parameters_rejected():
    with pytest.raises(ValueError):
        fourier_noise_distribution(8, [1, 1])
    with pytest.raises(ValueError):
        boolean_envelope_native_certificate(1, 1, 10)
