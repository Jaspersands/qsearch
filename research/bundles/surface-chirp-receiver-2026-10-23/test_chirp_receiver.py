from itertools import product
from random import Random

import numpy as np
import pytest
from qiskit.quantum_info import DensityMatrix, Operator
from sympy import Matrix, eye

from chirp_receiver import ChirpPacket, pair_equation, pair_root, recover
from classical_siegel import uniform_symplectic
from quantum_controls import (NativeFiberControl, inverse_fourier, pair_circuit,
                              paired_state, reference_chirp, width)
from test_classical_siegel import hidden_plane_oracle, subspace_key


@pytest.mark.parametrize("p", [3, 5, 7, 11])
def test_exact_shift_and_cancellation_polynomials(p):
    for b, c, off, r in product(range(p), range(p), range(p), range(1, p)):
        shift = off*pow(2*r, -1, p) % p
        constant = (c*r*shift*shift-(2*b*r+c*off)*shift) % p
        for t in (0, 1, p-1):
            assert (c*r*(t-shift)**2+(2*b*r+c*off)*(t-shift)
                    -r*(c*t*t+2*b*t)-constant) % p == 0
    for first, second in product(range(1, p), repeat=2):
        gamma = pair_root(first, second, p)
        if gamma is None:
            continue
        for b, c, s, t in product((0, 1, p-1), repeat=4):
            old = first*(c*t*t+2*b*t)+second*(c*(gamma*t+s)**2+2*b*(gamma*t+s))
            frequency = 2*((first+second*gamma)*b+second*gamma*s*c) % p
            assert (old-frequency*t-second*(c*s*s+2*b*s)) % p == 0
            slope, value = pair_equation(first, second, gamma, s, frequency, p)
            assert (b+slope*c-value) % p == 0


def test_all_three_field_chirp_pairs_by_quantum_interference():
    p, d = 3, 1 << width(3)
    for b, c, first, second in product(range(p), range(p), range(1, p), range(1, p)):
        gamma = pair_root(first, second, p)
        if gamma is None:
            continue
        state = paired_state(reference_chirp(b, c, first, p), reference_chirp(b, c, second, p), gamma, p)
        expected = np.zeros(d*d)
        for s in range(p):
            frequency = 2*((first+second*gamma)*b+second*gamma*s*c) % p
            expected[frequency+d*s] = 1/p
        assert np.allclose(state.probabilities(), expected, atol=1e-12)


@pytest.mark.parametrize("p", [5, 7, 11, 13])
def test_paired_circuit_is_public_unitary_and_has_correct_support(p):
    first, second, b, c = 1, p-1, p-2, 2
    gamma, d = pair_root(first, second, p), 1 << width(p)
    assert gamma == p-1
    matrix = Operator(pair_circuit(p, gamma)).data
    assert np.allclose(matrix.conj().T@matrix, np.eye(d*d), atol=1e-12)
    assert inverse_fourier(p).is_unitary()
    state = paired_state(reference_chirp(b, c, first, p), reference_chirp(b, c, second, p), gamma, p)
    expected = np.zeros(d*d)
    for s in range(p):
        frequency = 2*((first+second*gamma)*b+second*gamma*s*c) % p
        expected[frequency+d*s] = 1/p
    assert np.allclose(state.probabilities(), expected, atol=1e-12)


@pytest.mark.parametrize("p,seed", [(3, 0), (3, 7), (5, 1), (5, 9)])
def test_native_oracle_fibers_recover_without_secret_coefficients(p, seed):
    k = uniform_symplectic(p, Random(seed+200))[:, [0, 2]]
    oracle, calls = hidden_plane_oracle(k, p, seed+700)
    backend = NativeFiberControl(oracle, p, seed)
    result = recover(backend.prepare, backend.measure_pair, oracle, p, block_pairs=48)
    assert result["status"] == "RECOVERED_UNDER_ORACLE_AND_STATE_PROMISES"
    assert subspace_key(result["basis"], p) == subspace_key(k, p)
    assert result["source_copies"] == backend.prepared_copies <= result["source_copy_bound"]
    assert result["verification_queries"] <= 9
    assert len(calls) == backend.reference_table_queries+result["verification_queries"]
    assert backend.reference_table_queries == p**4*len(backend.tables)


def test_bad_constant_chart_aborts_then_another_chart_recovers():
    k, p = eye(4)[:, [0, 2]], 3
    oracle, _ = hidden_plane_oracle(k, p, 52)
    backend = NativeFiberControl(oracle, p, 42)
    result = recover(backend.prepare, backend.measure_pair, oracle, p, block_pairs=24)
    assert result["charts"][0]["status"] == "ABORT"
    assert result["status"] == "RECOVERED_UNDER_ORACLE_AND_STATE_PROMISES"
    assert subspace_key(result["basis"], p) == subspace_key(k, p)


def test_fabricated_row_outputs_cannot_bypass_original_oracle_certificate():
    p, k = 5, Matrix([[1, 1], [1, 0], [1, 2], [0, 1]])
    oracle, _ = hidden_plane_oracle(k, p, 3)
    prepared, measured = 0, 0
    def fake_prepare(chart, direction):
        nonlocal prepared
        prepared += 1
        return ChirpPacket(1 if prepared % 2 else p-1, None)
    def fake_measure(*args):
        nonlocal measured
        measured += 1
        return measured % 2, 0
    result = recover(fake_prepare, fake_measure, oracle, p, block_pairs=2)
    assert result["status"] == "ABORT"
    assert all(c["status"] == "CERTIFICATE_REJECTED" for c in result["charts"])


def test_exhaustion_and_parameter_failures_are_explicit():
    result = recover(lambda *args: None, lambda *args: (0, 0), lambda _: 0, 3, block_pairs=1)
    assert result["status"] == "ABORT"
    assert result["source_copies"] == 8
    with pytest.raises(ValueError):
        pair_equation(1, 2, 1, 0, 0, 3)
    with pytest.raises(ValueError):
        recover(None, None, None, 2)
    with pytest.raises(ValueError, match="limited"):
        NativeFiberControl(None, 7)


def test_dephasing_removes_the_linear_equation_signal():
    p, d, b, c, first, second = 3, 4, 1, 2, 1, 2
    gamma = pair_root(first, second, p)
    first_state, second_state = reference_chirp(b, c, first, p), reference_chirp(b, c, second, p)
    vector = np.kron(second_state.data, first_state.data)
    dephased = DensityMatrix(np.diag(np.abs(vector)**2)).evolve(pair_circuit(p, gamma))
    probability = sum(dephased.probabilities()[
        (2*((first+second*gamma)*b+second*gamma*s*c) % p)+d*s] for s in range(p))
    assert np.isclose(probability, 1/p, atol=1e-12)


def test_public_postprocessing_at_a_127_bit_prime():
    p = 2**127-1
    first, second = p-4, 1
    gamma = pair_root(first, second, p)
    assert (first+second*gamma*gamma) % p == 0
    b, c = p//3, 12345678901234567890
    equations = []
    for s in (7, 11):
        frequency = 2*((first+second*gamma)*b+second*gamma*s*c) % p
        equations.append(pair_equation(first, second, gamma, s, frequency, p))
    (s1, v1), (s2, v2) = equations
    recovered_c = (v2-v1)*pow(s2-s1, -1, p) % p
    assert recovered_c == c
    assert (v1-s1*recovered_c) % p == b
