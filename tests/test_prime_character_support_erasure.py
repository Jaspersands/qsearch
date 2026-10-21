"""Costed source-specific erasure, including a false general-decoder control."""

from fractions import Fraction
from itertools import combinations
import math

import numpy as np
import pytest

from theorems.prime_character_interleaved_probe import decode_burst
from theorems.prime_character_opi import instance
from theorems.prime_character_phase_feedback import (
    anchored_control, phase_erasure_certificate, reflection_product, support_erasure_control, support_transform,
)


@pytest.mark.parametrize("p", [7, 11])
@pytest.mark.parametrize("zero", [True, False])
def test_both_directions_run_on_native_complex_sources_without_losing_labels(p, zero):
    row = support_erasure_control(p, include_zero=zero)
    assert row["extraction_complex_amplitude_residual"] < 1e-12
    assert row["erasure_complex_amplitude_residual"] < 1e-12
    assert row["explicit_adjoint_replay_residual"] < 1e-12
    assert row["converse_clean_phase_residual"] < 1e-12
    assert row["uncontrolled_phase_vacuum_controlization_residual"] < 1e-12
    assert row["vacuum_reference_clean_with_unknown_global_phase_verified"]
    assert row["leaked_support_probability"] < 1e-25
    assert row["erase_success_probability"] == pytest.approx(1, abs=1e-12)
    coefficients = [complex(*v) for v in row["support_coefficients_real_imag"]]
    probabilities = row["extracted_support_probabilities"]
    for S, value in zip([0, 1, 2, 4, 8], coefficients):
        assert probabilities[S] == pytest.approx(abs(value) ** 2, abs=1e-12)
    assert sum(probabilities) == pytest.approx(1, abs=1e-12)
    assert row["controlled_singleton_phase_calls_per_forward_or_inverse"] == 4
    assert row["native_reflection_calls_per_forward_or_inverse"] == 4
    assert row["dense_state_amplitudes_charged"] == 16 * p * p
    assert row["dense_singleton_operator_entries_charged"] == 4 * p ** 4
    assert not row["efficient_large_gate_compiler_demonstrated"]


def test_every_basis_label_and_support_has_the_correct_coherent_xor_action():
    N, D = 3, 9
    masks = [sum(1 << i for i in S) for j in range(3) for S in combinations(range(N), j)]
    rng = np.random.default_rng(4310)
    frame, _ = np.linalg.qr(rng.normal(size=(D, len(masks))) + 1j * rng.normal(size=(D, len(masks))))
    phases = [reflection_product(frame, masks, 1 << i)[0] for i in range(N)]
    for label in range(1 << N):
        for column, S in enumerate(masks):
            source = np.zeros((1 << N, D), complex)
            source[label] = frame[:, column]
            expected = np.zeros_like(source)
            expected[label ^ S] = frame[:, column]
            assert np.linalg.norm(support_transform(source, phases) - expected) < 1e-12
            assert np.linalg.norm(support_transform(source, phases, adjoint=True) - expected) < 1e-12


@pytest.mark.parametrize("p", [7, 11])
def test_source_erasure_does_not_imply_an_arbitrary_syndrome_basis_decoder(p):
    result = decode_burst(p, 4, 2, 1, [[1, 1]])
    assert result["status"] == "VERIFIED_UNIQUE_BURST"
    assert result["support"] == [0]
    control = support_erasure_control(p)["individual_syndrome_control"]
    assert control["ordinary_basis_decoder_correct_support_probability"] == pytest.approx(1 / (p - 1), abs=1e-12)
    assert control["all_label_outcome_probabilities"][0] == pytest.approx(1 - 1 / (p - 1), abs=1e-12)
    assert control["ordinary_basis_decoder_correct_support_probability"] < 0.2
    assert not control["ordinary_classical_decoder_implied"]


def test_nonorthogonal_approximate_phases_require_explicit_inverse_order():
    G = np.array([[1, .08, .03j], [.08, 1, -.05], [-.03j, -.05, 1]], complex)
    values, vectors = np.linalg.eigh(G)
    frame = (vectors * np.sqrt(values)) @ vectors.conj().T
    gamma = np.linalg.norm(frame - np.eye(3), ord=2)
    phases = [reflection_product(frame, [0, 1, 2], 1 << i)[0] for i in range(2)]
    assert np.linalg.norm(phases[0] @ phases[1] - phases[1] @ phases[0]) > 0.01
    b = np.array([1, 2j, -3], complex) / math.sqrt(14)
    labeled = np.zeros((4, 3), complex)
    for i, S in enumerate([0, 1, 2]):
        labeled[S] = b[i] * frame[:, i]
    erased = support_transform(labeled, phases, adjoint=True)
    assert np.linalg.norm(support_transform(erased, phases) - labeled) < 1e-12
    assert np.linalg.norm(support_transform(labeled, phases) - erased) > 0.01
    target = np.zeros_like(labeled)
    target[0] = frame @ b / np.linalg.norm(frame @ b)
    bound = gamma + 4 * gamma + 2 * gamma / (1 - gamma)
    assert 0 < np.linalg.norm(erased - target) <= bound
    assert np.sum(abs(erased[1:]) ** 2) > 1e-6


def test_known_vacuum_reference_resolves_uncontrolled_global_phase_ambiguity():
    frame = np.eye(2)
    phases = [reflection_product(frame, [0, 1], 1 << i)[0] for i in range(2)]
    source = np.zeros((4, 2), complex)
    source[0, 0] = 1
    extracted = support_transform(source, phases)
    wrong = support_transform(source, [-U for U in phases])
    # U and -U have the same uncontrolled physical channel, but their
    # controlled versions move the Hadamard label by different bit strings.
    assert abs(extracted[0, 0]) == pytest.approx(1)
    assert abs(wrong[3, 0]) == pytest.approx(1)
    assert abs(wrong[0, 0]) < 1e-12
    # But the KNOWN vacuum removes this obstacle with a real swap circuit.
    # The arbitrary global phase is never learned or used as a gate input.
    control_main = np.array([[1, 1j], [-1j, 2]], complex) / math.sqrt(7)
    anchor = frame[:, 0]
    U = phases[0]
    expected = np.array([control_main[0], U @ control_main[1]])[:, :, None] * anchor[None, None, :]
    for phase in (1, -1, np.exp(.531j)):
        actual = anchored_control(control_main, phase * U, anchor)
        assert np.linalg.norm(actual - phase * expected) < 1e-12


def test_anchor_reference_must_be_provided_normalized_and_invariant():
    X = np.array([[0, 1], [1, 0]])
    with pytest.raises(ValueError, match="eigenstate"):
        anchored_control(np.eye(2), X, [1, 0])
    with pytest.raises(ValueError, match="unit-norm"):
        anchored_control(np.eye(2), X, [1, 1])


def test_large_costed_reduction_has_no_free_phase_or_extra_rank_source():
    row = phase_erasure_certificate(instance(2 ** 61 - 1, 127, 39, 2, 29), 32)
    assert row["status"] == "COSTED_SOURCE_SUPPORT_ERASURE_EQUIVALENCE_NOT_AN_EFFICIENT_COMPILER"
    assert row["forward_known_controlled_singleton_phase_calls"] == 127
    assert row["reverse_clean_erasure_or_adjoint_calls_per_phase"] == 2
    assert int(row["native_reflections_total_decimal"]) > 5 * 10 ** 31
    assert int(row["native_state_preparation_or_inverse_calls_total_decimal"]) == 2 * int(row["native_reflections_total_decimal"])
    assert Fraction(row["erased_vs_normalized_native_single_copy_distance_upper_exact"]) < Fraction(6, 10 ** 37)
    assert row["no_auxiliary_polynomial_or_rank_herald_required_by_this_abstract_circuit"]
    assert row["source_family_specific_not_arbitrary_syndrome_basis"]
    assert not row["general_classical_syndrome_decoder_reduction_proved"]
    assert row["uncontrolled_phase_plus_known_vacuum_anchor_suffices"]
    assert not row["direct_controlled_phase_circuits_are_necessary"]
    assert not row["uncontrolled_phase_alone_is_assumed_controllable"]
    assert row["anchor_reference_qubits"] == 39 * 61
    assert row["anchor_assisted_total_controlled_bit_swaps"] == 2 * 127 * 39 * 61
    assert not row["unknown_eigenphase_estimation_or_correction_used"]
    assert not row["polynomial_phase_or_erasure_compiler_supplied"]
    assert not row["new_algorithm_speedup_or_novelty_claimed"]


def test_invalid_operators_and_weak_frame_bounds_are_rejected():
    with pytest.raises(ValueError, match="unitary"):
        support_transform(np.ones((2, 2)), [np.ones((2, 2))])
    with pytest.raises(ValueError, match="bounded"):
        support_transform(np.ones((3, 2)), [np.eye(2)])
    with pytest.raises(ValueError, match="finite"):
        support_transform(np.full((2, 2), np.nan), [np.eye(2)])
    with pytest.raises(ValueError, match="capped"):
        support_erasure_control(19)
    row = phase_erasure_certificate(instance(7, 6, 3, 2, 29), 2)
    assert row["status"] == "UNKNOWN_POLAR_NORMALIZATION_BOUND_TOO_WEAK"
