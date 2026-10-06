from fractions import Fraction

import pytest

from dcp_carry_packets import compile_packet
from dcp_physical_phase_noise import (
    IndependentPhysicalZ, SparsePhysicalZ, _correlated_cancellation_control,
    _correlation_control, _full_physical_source_control,
    _systematic_low_controls, fixed_chart_physical_collision, native_physical_source_mean,
    physical_error_pushforward, physical_transcript_information_bound, read,
)


def test_iid_physical_errors_do_not_become_iid_logical_errors():
    row = _correlation_control()
    assert read(row["joint_two_bit_error"]) != read(row["product_of_bit_error_marginals"])
    assert sum(read(p) for p in row["logical_error_distribution"]) == 1


def test_exact_full_probability_source_matches_correlated_physical_convolution():
    row = _full_physical_source_control()
    assert row["complete_higher_label_tables"] == 256
    assert not row["certificate"]["logical_errors_assumed_independent"]
    assert not row["certificate"]["error_lineage_independence_programmatically_verified"]


def test_systematic_formula_checks_full_low_source_and_correct_candidate_completeness():
    rows = _systematic_low_controls()
    assert len(rows) == 4
    assert read(rows[-1]["source_mean_relative_collision"]) == 1
    assert read(rows[-1]["known_residue_all_zero_acceptance"]) == Fraction(1, 4)


def test_constant_physical_dephasing_can_close_the_declared_full_bell_protocol_only():
    row = physical_transcript_information_bound(256, 256, Fraction(1, 16), 256**2)
    assert row["orbit_success_below_one_over_100"]
    assert row["all_noisy_full_output_bits_retained"]
    assert not row["quantum_memory_encoding_or_other_measurements_covered"]
    assert row["independent_input_Z_errors_not_a_verified_reduction_promise"]


def test_vanishing_phase_noise_is_not_rejected_by_a_constant_noise_bound():
    row = native_physical_source_mean(64, Fraction(1, 64**2))
    assert not row["exponential_uniformization_regime"]
    assert read(row["single_packet_known_correct_residue_all_zero_mean_acceptance"]) > Fraction(9, 10)
    noisy = native_physical_source_mean(128, Fraction(1, 16))
    assert read(noisy["single_packet_known_correct_residue_all_zero_mean_acceptance"]) < Fraction(1, 10**10)
    assert noisy["correct_residue_all_zero_verifier_noiseless_completeness_no_longer_valid"]


def test_fourier_transport_scales_without_dense_physical_error_distribution():
    packet = compile_packet([[1] * 65], 128)
    noise = IndependentPhysicalZ.iid(packet, packet, Fraction(1, 16))
    assert noise.fourier(packet, packet, 1) == Fraction(7, 8)**4
    with pytest.raises(ValueError, match="exponential"):
        physical_error_pushforward(packet, packet, noise)
    with pytest.raises(ValueError, match="exponential"):
        fixed_chart_physical_collision(packet, packet, noise)


def test_nonuniform_physical_rates_keep_exact_correlated_fourier_law():
    left, right = compile_packet([[1, 1, 1]], 8), compile_packet([[1, 1, 0]], 8)
    noise = IndependentPhysicalZ((0, Fraction(1, 8), Fraction(1, 2)), (Fraction(1, 4), 0, Fraction(1, 16)))
    law = physical_error_pushforward(left, right, noise)
    assert sum(law) == 1
    assert noise.fourier(left, right, 2) == 0


def test_wrong_source_dimensions_and_invalid_rates_are_rejected():
    packet = compile_packet([[1, 1, 1]], 8)
    for rate in (Fraction(-1, 8), Fraction(3, 4)):
        with pytest.raises(ValueError):
            IndependentPhysicalZ.iid(packet, packet, rate)
    with pytest.raises(ValueError, match="width"):
        IndependentPhysicalZ((0,), (0,)).fourier(packet, packet, 1)
    with pytest.raises(ValueError):
        native_physical_source_mean(0, 0)


def test_shared_correlated_errors_can_cancel_despite_large_physical_marginals():
    row = _correlated_cancellation_control()
    assert row["shared_correlated_Z_errors_cancel_in_bell_readout"]
    assert not row["correlated_certificate"]["physical_mask_bits_independent"]
    assert row["native_iid_source_uniformization_formula_does_not_apply"]
    packet = compile_packet([[1] * 65], 128)
    law = SparsePhysicalZ(((0, 0, Fraction(1, 2)), (1, 1, Fraction(1, 2))))
    assert law.logical_distribution(packet, packet) == {0: 1}
    assert law.fourier(packet, packet, 2**63) == 1


def test_sparse_noise_law_normalization_and_mask_range_are_checked():
    with pytest.raises(ValueError):
        SparsePhysicalZ(((0, 0, Fraction(1, 2)),))
    packet = compile_packet([[1, 1, 1]], 8)
    with pytest.raises(ValueError):
        SparsePhysicalZ(((8, 0, Fraction(1)),)).validate(packet, packet)
