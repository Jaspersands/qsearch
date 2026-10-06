import itertools

import numpy as np
import pytest

from dcp_carry_packets import (
    calibration_bell_probabilities,
    calibration_packet_state,
    calibration_physical_chart,
    compile_packet,
    exhaustive_conductor_controls,
    expanded_carry_coefficients,
    greedy_common_isotropic,
    isotropic_readout_rows,
    isotropic_source_controls,
    matched_bell_equations,
    partial_bell_equation,
    public_common_radical,
    quadratic_data,
    run_controls,
    single_packet_conductor_radical,
    single_packet_source_bound,
)


def test_public_clifford_chart_retains_all_free_qubits_and_all_syndromes():
    labels = [[1, 0, 3, 2, 1], [0, 1, 1, 3, 0]]
    packet = compile_packet(labels, 4)
    assert packet.retained_qubits == 3
    assert len(packet.pivots) == 2
    assert not packet.resource_record()["output_is_independent_phase_qubits"]
    physical = calibration_physical_chart(packet, [3, 2])
    assert np.allclose(np.sum(abs(physical)**2, axis=1), 1 / 4)
    for y in range(4):
        conditioned = compile_packet(labels, 4, y)
        state = calibration_packet_state(conditioned, [3, 2])
        assert abs(np.vdot(state, physical[y] * 2)) == pytest.approx(1)


def test_correlated_carry_cannot_be_promoted_to_two_product_phase_states():
    packet = compile_packet([[1, 1, 1]], 4)
    coefficients = expanded_carry_coefficients(packet)
    assert coefficients[3] == (1,)
    matrix = calibration_packet_state(packet, [1]).reshape(2, 2)
    reduced = matrix @ matrix.conj().T
    assert np.trace(reduced @ reduced).real == pytest.approx(1 / 2)


def test_modulus_eight_has_a_cubic_term_and_rejects_quadratic_readout():
    packet = compile_packet([[1, 1, 1, 1]], 8)
    assert expanded_carry_coefficients(packet)[7] == (2,)
    with pytest.raises(ValueError, match="modulus four"):
        quadratic_data(packet)


def test_matched_bell_outcomes_are_uniform_xor_plus_linear_secret_equations():
    p1 = compile_packet([[1, 0, 1, 1], [0, 1, 1, 0]], 4, 1)
    p2 = compile_packet([[3, 2, 1, 3], [2, 1, 3, 2]], 4, 2)
    assert quadratic_data(p1)[1] == quadratic_data(p2)[1]
    for secret in itertools.product(range(4), repeat=2):
        probabilities = calibration_bell_probabilities(calibration_packet_state(p1, secret),
                                                       calibration_packet_state(p2, secret))
        s = sum((value & 1) << i for i, value in enumerate(secret))
        for u in range(4):
            rows = matched_bell_equations(p1, p2, u)
            v = sum(((row & s).bit_count() & 1) << j for j, row in enumerate(rows))
            assert probabilities[u, v] == pytest.approx(1 / 4)
            assert probabilities[u].sum() == pytest.approx(probabilities[u, v])


def test_mismatch_is_not_a_deterministic_equation_with_small_independent_noise():
    left = compile_packet([[1, 1, 1]], 4)
    right = compile_packet([[1, 1, 0]], 4)
    with pytest.raises(ValueError, match="tensors mismatch"):
        matched_bell_equations(left, right, 0)
    probs = calibration_bell_probabilities(calibration_packet_state(left, [1]),
                                          calibration_packet_state(right, [1]))
    assert np.allclose(probs, 1 / 16)
    assert public_common_radical(left, right) == ()


def test_partial_radical_readout_does_not_require_full_quadratic_matching():
    left = compile_packet([[1, 1, 1, 1]], 4)
    right = compile_packet([[1, 1, 0, 0]], 4)
    assert quadratic_data(left)[1] != quadratic_data(right)[1]
    radical = public_common_radical(left, right)
    assert radical == (7,)
    for secret in range(4):
        probs = calibration_bell_probabilities(calibration_packet_state(left, [secret]),
                                              calibration_packet_state(right, [secret]))
        for u in range(8):
            equation = partial_bell_equation(left, right, u, radical[0])
            assert equation == 1
            allowed = [v for v in range(8) if (v & 7).bit_count() % 2 == secret % 2]
            assert probs[u, allowed].sum() == pytest.approx(1 / 8)
    with pytest.raises(ValueError, match="outside"):
        partial_bell_equation(left, right, 0, 1)


def test_single_packet_radical_is_exactly_the_public_code_conductor():
    assert exhaustive_conductor_controls() == 264
    packet = compile_packet([[1, 1, 1, 1]], 4)
    assert single_packet_conductor_radical(packet) == (7,)
    assert single_packet_conductor_radical(compile_packet([[1, 1, 1]], 4)) == ()


def test_native_single_packet_bound_is_scoped_and_not_a_quantum_no_go():
    from fractions import Fraction

    for n in (8, 16, 32, 64):
        row = single_packet_source_bound(n)
        bound = row["public_guaranteed_single_packet_equation_probability_upper_bound"]
        assert 0 < Fraction(int(bound["numerator_hex"], 16), 1 << bound["denominator_binary_exponent"]) <= 1
        assert row["all_kernel_basis_charts_included"]
        assert not row["all_clifford_or_quantum_measurements_excluded"]
    bound = single_packet_source_bound(64)["public_guaranteed_single_packet_equation_probability_upper_bound"]
    assert Fraction(int(bound["numerator_hex"], 16), 1 << bound["denominator_binary_exponent"]) < Fraction(1, 10**15)


def test_common_isotropic_readout_escapes_radical_gate_by_measuring_complement():
    packet = compile_packet([[1, 1, 1]], 4)
    assert single_packet_conductor_radical(packet) == ()
    directions = greedy_common_isotropic(packet)
    assert len(directions) == 1
    assert len(isotropic_readout_rows(packet, directions, 1)) == 1
    with pytest.raises(ValueError, match="not common"):
        isotropic_readout_rows(packet, (1, 2))


def test_isotropic_output_labels_are_jointly_uniform_not_only_marginally():
    controls = isotropic_source_controls()
    assert controls["affine_phase_identity_checks"] > 0
    assert all(s["joint_output_labels_uniform_and_independent"]
               for s in controls["uniform_high_bit_source_strata"])


def test_public_carry_evaluator_scales_without_dense_polynomial_or_state_tables():
    labels = [[(3 * i + 2 * l + (i >> l)) % 256 for i in range(128)] for l in range(8)]
    packet = compile_packet(labels, 256)
    assert packet.retained_qubits >= 120
    value = packet.residual((1 << packet.retained_qubits) - 1)
    assert len(value) == 8
    assert packet.cnots <= 8 * packet.retained_qubits
    with pytest.raises(ValueError, match="calibration-only"):
        expanded_carry_coefficients(packet)
    with pytest.raises(ValueError, match="bounded calibration"):
        calibration_packet_state(packet, [0] * 8)


def test_complete_controls_keep_matching_and_decoder_as_unproved_obligations():
    report = run_controls()
    assert report["controls"]["physical_chart_branches"] > 0
    assert report["controls"]["fault_shift_rows"] > 0
    assert report["countercontrols"]["modulus_eight_cubic_carry_retained"]
    assert not report["claim_gate"]["native_iid_quadratic_tensor_matcher"]
    assert not report["claim_gate"]["matched_test_batches_are_unconditional_source_samples"]
    assert not report["claim_gate"]["speedup_claim_allowed"]


def test_empty_or_invalid_source_records_are_rejected():
    for labels, modulus in (([], 4), ([[]], 4), ([[1], [1, 2]], 4), ([[1]], 6)):
        with pytest.raises(ValueError):
            compile_packet(labels, modulus)
    with pytest.raises(ValueError, match="syndrome"):
        compile_packet([[1, 1]], 4, 2)
