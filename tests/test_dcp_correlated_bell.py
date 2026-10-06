from fractions import Fraction
import itertools

import pytest

from dcp_carry_packets import compile_packet, public_common_radical
from dcp_correlated_bell import (
    Z4Quadratic, compile_bell_parity, full_output_countercontrol,
    middle_parseval_controls, q4_full_bell_likelihood, quadratic_gauss, run_controls,
    tail_unit_information_certificate,
)


def read(value):
    return Fraction(value["sign"] * int(value["numerator_hex"], 16),
                    1 << value["denominator_binary_exponent"])


def test_quadratic_gauss_keeps_exact_complex_phase_and_radical_obstructions():
    assert quadratic_gauss(Z4Quadratic(0, (1,), (0,))) == (Fraction(1, 2), Fraction(1, 2))
    assert quadratic_gauss(Z4Quadratic(3, (), ())) == (Fraction(0), Fraction(-1))
    assert quadratic_gauss(Z4Quadratic(0, (2,), (0,))) == (Fraction(0), Fraction(0))
    assert quadratic_gauss(Z4Quadratic(0, (0, 0), (2, 0))) == (Fraction(1, 2), Fraction(0))
    assert quadratic_gauss(Z4Quadratic(0, (2, 2), (2, 0))) == (Fraction(-1, 2), Fraction(0))


def test_nonmatching_bell_readout_has_a_valid_likelihood_not_only_public_equations():
    left = compile_packet([[1, 1, 1]], 4)
    right = compile_packet([[1, 1, 0]], 4)
    assert public_common_radical(left, right) == ()
    tensor = compile_bell_parity(left, right, 0, 1)
    assert tensor.bias([0]) == 1
    assert tensor.bias([1]) == 0
    assert q4_full_bell_likelihood(left, right, [0], 0, 0) == Fraction(1, 4)
    assert q4_full_bell_likelihood(left, right, [1], 0, 0) == Fraction(1, 16)
    control = full_output_countercontrol()
    assert read(control["q4_nonmatching_full_readout_bayes_success"]) == Fraction(7, 8)
    assert read(control["one_coordinate_parity_bayes_success"]) == Fraction(3, 4)


def test_uniform_coordinate_marginals_cannot_be_multiplied_as_independent():
    left = compile_packet([[1, 1, 1, 1]], 4)
    right = compile_packet([[1, 1, 0, 0]], 4)
    probabilities = [q4_full_bell_likelihood(left, right, [1], 0, v) * 8 for v in range(8)]
    assert sum(probabilities) == 1
    for i in range(3):
        assert sum(p for v, p in enumerate(probabilities) if not (v >> i & 1)) == Fraction(1, 2)
    assert any(p == 0 for p in probabilities)
    assert set(probabilities) == {Fraction(0), Fraction(1, 4)}


def test_modulus_eight_cubic_carries_still_have_quadratic_parity_derivatives():
    left = compile_packet([[1, 3, 5, 7]], 8)
    right = compile_packet([[3, 1, 7, 5]], 8)
    for u, h in itertools.product(range(8), range(1, 8)):
        tensor = compile_bell_parity(left, right, u, h)
        for s in range(4):
            phase = tensor.instantiate([s])
            exact = sum((1, 1j, -1, -1j)[phase.evaluate(z)] for z in range(8)) / 8
            assert float(tensor.bias([s])) == pytest.approx(exact.real)
            assert abs(exact.imag) < 1e-12
            assert sum(tensor.likelihood([s], b) for b in (0, 1)) == Fraction(1, 8)
    with pytest.raises(ValueError, match="cubic phases"):
        q4_full_bell_likelihood(left, right, [1], 0, 0)


def test_public_middle_rank_and_quadratic_part_do_not_use_fresh_higher_bits():
    low = [[1, 1, 1, 1]]
    left, right = compile_packet(low, 8), compile_packet(low, 8)
    reference = compile_bell_parity(left, right, 3, 2)
    for bits in range(16):
        labels = [[b + 2 * (bits >> i & 1) for i, b in enumerate(low[0])]]
        changed = compile_bell_parity(compile_packet(labels, 8), right, 3, 2)
        assert changed.middle_linear_rank == reference.middle_linear_rank
        assert changed.upper_rows == reference.upper_rows


def test_wrong_hierarchy_level_or_unaccounted_outcomes_are_rejected():
    packet = compile_packet([[1, 1, 1]], 16)
    with pytest.raises(ValueError, match="four or eight"):
        compile_bell_parity(packet, packet, 0, 1)
    packet = compile_packet([[1, 1, 1]], 8)
    with pytest.raises(ValueError, match="nonzero parity"):
        compile_bell_parity(packet, packet, 0, 0)
    tensor = compile_bell_parity(packet, packet, 0, 1)
    with pytest.raises(ValueError, match="dimension"):
        tensor.bias([0, 1])
    with pytest.raises(ValueError, match="binary"):
        tensor.likelihood([0], 2)


def test_source_information_certificate_leaves_full_and_quantum_adaptive_readouts_open():
    row = tail_unit_information_certificate(128, 128**2)
    assert read(row["uniform_secret_mutual_information_bits_upper_bound"]) < Fraction(1, 10**8)
    assert row["success_below_one_over_100"]
    assert row["middle_rank_floor_outside_bad_event"] == 65
    assert row["secret_parameter_modulus_after_parity_chart"] == 4
    assert not row["full_bell_transcript_covered"]
    assert not row["coherent_memory_or_reused_packets_covered"]
    assert not row["independent_theorem_review"]
    assert read(tail_unit_information_certificate(8)["one_bit_average_squared_bias_upper_bound"]) == 1


def test_parseval_bound_is_native_middle_average_and_not_an_even_secret_bound():
    control = middle_parseval_controls()
    assert len(control["rows"]) == 48
    for row in control["rows"]:
        assert read(row["average_squared_bias"]) == Fraction(1, 1 << row["middle_linear_rank"])
    assert read(control["all_even_secret_exception_squared_bias_witness"]) == 1
    assert control["nonzero_secret_parity_precondition_required"]


def test_exact_engine_scales_past_dense_state_cap():
    phase = Z4Quadratic(0, (0,) * 128, tuple(1 << (i + 1) if i % 2 == 0 else 0 for i in range(128)))
    assert quadratic_gauss(phase) == (Fraction(1, 1 << 64), Fraction(0))
    labels = [[(i * 3 + 1) % 8 for i in range(64)]]
    packet = compile_packet(labels, 8)
    tensor = compile_bell_parity(packet, packet, 0, 1)
    assert tensor.width == 63
    assert tensor.input_phase_qubits == 128
    assert tensor.bias([0]) == 1


def test_complete_gauss_and_physical_controls_preserve_unresolved_decoder_obligations():
    report = run_controls()
    assert report["quadratic_gauss"]["complete_quadratic_phase_tables"] == 2196
    assert report["physical_bell"]["complete_derivative_polynomial_assignments"] > 0
    assert not report["claim_gate"]["unknown_secret_decoder"]
    assert not report["claim_gate"]["full_q8_likelihood_implemented"]
    assert not report["claim_gate"]["known_secret_simulation_is_dequantization"]
    assert not report["claim_gate"]["speedup_claim_allowed"]


def test_invalid_quadratic_representation_is_not_silently_coerced():
    with pytest.raises(ValueError, match="upper-triangular"):
        Z4Quadratic(0, (0,), (1,))
    with pytest.raises(ValueError, match="modulo four"):
        Z4Quadratic(4, (), ())
