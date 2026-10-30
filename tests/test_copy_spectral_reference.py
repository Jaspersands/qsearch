"""Finite channel falsifiers, not a proof of spectral-projection access."""

import numpy as np
import pytest

from theorems.copy_spectral_reference import (
    MAX_DATA_DIM,
    MAX_REFERENCE_DIM,
    MAX_STEPS,
    controlled_partial_swap,
    controlled_partial_swap_unitary,
    ideal_controlled_evolution,
    simulate_controlled_density_exponentiation,
)


def projector(vector):
    vector = np.asarray(vector, dtype=complex)
    vector = vector / np.linalg.norm(vector)
    return np.outer(vector, vector.conj())


def trace_norm(matrix):
    return np.linalg.svd(matrix, compute_uv=False).sum()


def assert_density(matrix):
    np.testing.assert_allclose(matrix, matrix.conj().T, atol=2e-12)
    assert np.trace(matrix) == pytest.approx(1, abs=2e-12)
    assert np.linalg.eigvalsh(matrix).min() >= -2e-12


def program(d, rank):
    rng = np.random.default_rng(400 + d + rank)
    vectors, _ = np.linalg.qr(rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d)))
    weights = np.zeros(d)
    weights[:rank] = np.arange(1, rank + 1)
    weights /= weights.sum()
    return (vectors * weights) @ vectors.conj().T


def coherent_input(d, r):
    if r == 1:
        data_reference = projector(np.arange(1, d + 1) + 1j)
    else:
        data_reference = projector(np.eye(d, r).reshape(-1))
    return np.kron(projector([1, 1j]), data_reference)


@pytest.mark.parametrize("d,r", [(1, 1), (2, 1), (2, 2), (3, 3), (3, 6)])
@pytest.mark.parametrize("theta", [-0.31, 0, 0.31])
def test_unitary_matches_basis_action_and_is_unitary(d, r, theta):
    unitary = controlled_partial_swap_unitary(d, theta, reference_dim=r)
    expected = np.zeros_like(unitary)
    def index(c, a, b, p):
        return ((c * d + a) * r + b) * d + p
    for c in range(2):
        for a in range(d):
            for b in range(r):
                for p in range(d):
                    j = index(c, a, b, p)
                    expected[j, j] += 1 if c == 0 else np.cos(theta)
                    if c == 1:
                        expected[index(c, p, b, a), j] -= 1j * np.sin(theta)
    np.testing.assert_allclose(unitary, expected, atol=1e-14)
    np.testing.assert_allclose(unitary.conj().T @ unitary, np.eye(len(unitary)), atol=1e-14)


@pytest.mark.parametrize("d,rank", [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3)])
@pytest.mark.parametrize("theta", [-0.37, 0.37])
def test_single_step_matches_independent_control_block_formulas(d, rank, theta):
    r = d
    rho = program(d, rank)
    rng = np.random.default_rng(d + rank)
    size = 2 * d * r
    amplitudes = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    state = amplitudes @ amplitudes.conj().T
    state /= np.trace(state)
    blocks = state.reshape(2, d * r, 2, d * r)
    expected = np.empty_like(blocks)
    c, s = np.cos(theta), np.sin(theta)
    rho_ref = np.kron(rho, np.eye(r))
    active = blocks[1, :, 1, :]
    reference = np.trace(active.reshape(d, r, d, r), axis1=0, axis2=2)
    expected[0, :, 0, :] = blocks[0, :, 0, :]
    expected[0, :, 1, :] = blocks[0, :, 1, :] @ (c * np.eye(d * r) + 1j * s * rho_ref)
    expected[1, :, 0, :] = (c * np.eye(d * r) - 1j * s * rho_ref) @ blocks[1, :, 0, :]
    expected[1, :, 1, :] = (
        c**2 * active + s**2 * np.kron(rho, reference)
        - 1j * c * s * (rho_ref @ active - active @ rho_ref)
    )
    actual = controlled_partial_swap(state, rho, theta, reference_dim=r)
    np.testing.assert_allclose(actual, expected.reshape(size, size), atol=2e-14)
    assert_density(actual)


@pytest.mark.parametrize("d,rank", [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3)])
@pytest.mark.parametrize("with_reference", [False, True])
@pytest.mark.parametrize("t", [-0.8, 0.8])
def test_composition_preserves_coherence_within_trace_norm_allowance(d, rank, with_reference, t):
    r = d if with_reference else 1
    rho = program(d, rank)
    state = coherent_input(d, r)
    ideal = ideal_controlled_evolution(state, rho, t, reference_dim=r)
    assert_density(ideal)
    errors = []
    for n in [1, 8, 64, 256]:
        result = simulate_controlled_density_exponentiation(state, rho, t, n, reference_dim=r)
        assert result.program_copies == n
        assert result.half_diamond_bound == pytest.approx(min(1, 2 * t**2 / n))
        error = trace_norm(result.state - ideal)
        assert error <= 2 * result.half_diamond_bound + 2e-12
        assert_density(result.state)
        # Check cross branches explicitly, not just conditional data states.
        width = d * r
        assert np.linalg.norm(result.state[:width, width:] - ideal[:width, width:]) <= error + 1e-12
        errors.append(error)
    if d > 1:
        assert errors[-1] < errors[0] / 50


def test_reference_can_be_entangled_with_entire_control_data_system():
    d, r = 2, 4
    state = projector(np.eye(2 * d).reshape(-1))
    rho = program(d, 2)
    for t in [-0.6, 0.6]:
        ideal = ideal_controlled_evolution(state, rho, t, reference_dim=r)
        result = simulate_controlled_density_exponentiation(state, rho, t, 64, reference_dim=r)
        assert trace_norm(result.state - ideal) <= 2 * result.half_diamond_bound
        reference = np.trace(result.state.reshape(2 * d, r, 2 * d, r), axis1=0, axis2=2)
        np.testing.assert_allclose(reference, np.eye(r) / r, atol=2e-13)


def test_uncontrolled_channel_and_dephasing_miss_cross_branch_phase():
    rho = np.diag([0.8, 0.2])
    data = projector([1, 0])
    control = projector([1, 1])
    state = np.kron(control, data)
    t, n = 1.0, 256
    ideal = ideal_controlled_evolution(state, rho, t)
    correct = simulate_controlled_density_exponentiation(state, rho, t, n)
    # An actual uncontrolled partial-SWAP data channel, applied n times.
    output_data = data.copy()
    c, s = np.cos(t / n), np.sin(t / n)
    for _ in range(n):
        output_data = (c**2 * output_data + s**2 * rho
                       - 1j * c * s * (rho @ output_data - output_data @ rho))
    uncontrolled = np.kron(control, output_data)
    # Even exact uncontrolled evolution has exactly right diagonal blocks here.
    uncontrolled_ideal = state.copy()
    dephased = ideal.copy()
    dephased[:2, 2:] = 0
    dephased[2:, :2] = 0
    for incorrect in [uncontrolled, uncontrolled_ideal, dephased]:
        assert_density(incorrect)
        for branch in [slice(0, 2), slice(2, 4)]:
            np.testing.assert_allclose(incorrect[branch, branch], ideal[branch, branch], atol=1e-3)
        assert trace_norm(incorrect - ideal) > 0.7
    assert trace_norm(correct.state - ideal) < 0.01
    assert np.linalg.norm(dephased[:2, 2:]) == 0


def test_fresh_negative_time_is_not_an_exact_inverse_but_converges():
    rho = np.diag([0.7, 0.3])
    state = coherent_input(2, 2)
    t = 0.9
    ideal_forward = ideal_controlled_evolution(state, rho, t, reference_dim=2)
    ideal_back = ideal_controlled_evolution(ideal_forward, rho, -t, reference_dim=2)
    np.testing.assert_allclose(ideal_back, state, atol=1e-14)
    errors = []
    for n in [4, 32, 256]:
        forward = simulate_controlled_density_exponentiation(state, rho, t, n, reference_dim=2)
        backward = simulate_controlled_density_exponentiation(forward.state, rho, -t, n, reference_dim=2)
        backward_ideal = ideal_controlled_evolution(forward.state, rho, -t, reference_dim=2)
        assert forward.program_copies + backward.program_copies == 2 * n
        assert trace_norm(forward.state - ideal_forward) <= 2 * forward.half_diamond_bound
        assert trace_norm(backward.state - backward_ideal) <= 2 * backward.half_diamond_bound
        error = trace_norm(backward.state - state)
        assert 1e-5 < error <= 4 * forward.half_diamond_bound
        assert np.trace(backward.state @ backward.state).real < 1 - 1e-5
        errors.append(error)
    assert errors[2] < errors[1] < errors[0]


def test_zero_time_and_repeated_steps_and_no_input_mutation():
    rho = program(2, 2)
    state = coherent_input(2, 2)
    original_state, original_rho = state.copy(), rho.copy()
    result = simulate_controlled_density_exponentiation(state, rho, 0, np.int64(3), reference_dim=2)
    np.testing.assert_allclose(result.state, state, atol=1e-14)
    assert result.program_copies == 3
    assert result.half_diamond_bound == 0
    repeated = state
    for _ in range(3):
        repeated = controlled_partial_swap(repeated, rho, -0.2, reference_dim=2)
    composed = simulate_controlled_density_exponentiation(state, rho, -0.6, 3, reference_dim=2)
    np.testing.assert_allclose(composed.state, repeated, atol=1e-14)
    np.testing.assert_array_equal(state, original_state)
    np.testing.assert_array_equal(rho, original_rho)


@pytest.mark.parametrize("n", [0, -1, True, False, np.bool_(True), 1.5, 2.0, "2", MAX_STEPS + 1])
def test_invalid_step_counts(n):
    with pytest.raises(ValueError, match="n must"):
        simulate_controlled_density_exponentiation(np.eye(4) / 4, np.eye(2) / 2, 1, n)


@pytest.mark.parametrize("entry", [controlled_partial_swap, ideal_controlled_evolution,
                                    simulate_controlled_density_exponentiation])
@pytest.mark.parametrize("target", ["state", "rho"])
@pytest.mark.parametrize("bad", ["shape", "trace", "negative", "nonhermitian", "nan", "inf"])
def test_all_channel_entries_validate_density_matrices(entry, target, bad):
    state, rho = np.eye(4) / 4, np.eye(2) / 2
    matrix = (state if target == "state" else rho).copy().astype(complex)
    if bad == "shape":
        matrix = matrix[:, :-1]
    elif bad == "trace":
        matrix *= 2
    elif bad == "negative":
        matrix[0, 0], matrix[1, 1] = -0.1, matrix[1, 1] + matrix[0, 0] + 0.1
    elif bad == "nonhermitian":
        matrix[0, 1] = 0.2j
    else:
        matrix[0, 0] = float(bad)
    args = [matrix if target == "state" else state, matrix if target == "rho" else rho, 0.2]
    if entry is simulate_controlled_density_exponentiation:
        args.append(4)
    with pytest.raises(ValueError):
        entry(*args)


@pytest.mark.parametrize("r", [0, -1, True, np.bool_(False), 1.0, MAX_REFERENCE_DIM + 1])
def test_reference_dimension_validation(r):
    with pytest.raises(ValueError):
        controlled_partial_swap(np.eye(4) / 4, np.eye(2) / 2, 0.2, reference_dim=r)


def test_dimension_caps_and_reference_mismatch():
    with pytest.raises(ValueError):
        controlled_partial_swap(np.eye(4) / 4, np.eye(2) / 2, 0.2, reference_dim=2)
    with pytest.raises(ValueError):
        controlled_partial_swap(np.eye(8) / 8, np.eye(4) / 4, 0.2)
    for d in [0, True, 2.0, MAX_DATA_DIM + 1]:
        with pytest.raises(ValueError):
            controlled_partial_swap_unitary(d, 0.2)


@pytest.mark.parametrize("t", [True, np.bool_(True), np.nan, np.inf, -np.inf, 1j, "1"])
def test_time_validation(t):
    for entry in [controlled_partial_swap, ideal_controlled_evolution,
                  simulate_controlled_density_exponentiation]:
        args = [np.eye(4) / 4, np.eye(2) / 2, t]
        if entry is simulate_controlled_density_exponentiation:
            args.append(4)
        with pytest.raises(ValueError, match="finite real"):
            entry(*args)
