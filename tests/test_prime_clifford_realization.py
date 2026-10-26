"""Independent dense controls for a public polynomial-size Clifford plan.

Dense matrices appear only here. Large-prime/controller tests use exact
tableaux, not Hilbert-space enumeration. No hidden oracle data is supplied.
"""
from dataclasses import replace
from itertools import product
import random

import numpy as np
import pytest

from theorems.class_four_matrix_source import align_variable_jets
from theorems.prime_clifford_realization import (
    CliffordGate, compile_alignment, compile_symplectic, symplectic_action,
)
from theorems.ut5_matrix_phase_alignment import _identity, _product


def _points(p, width):
    return list(product(range(p), repeat=width))


def _index(point, p):
    value = 0
    for x in point:
        value = p*value+x
    return value


def _mv(matrix, vector, p):
    return tuple(sum(a*b for a, b in zip(row, vector)) % p for row in matrix)


def _weyl(p, vector):
    r = len(vector)//2
    x, z = vector[:r], vector[r:]
    omega = np.exp(2j*np.pi/p)
    matrix = np.zeros((p**r, p**r), dtype=complex)
    for j, t in enumerate(_points(p, r)):
        output = tuple((a+b) % p for a, b in zip(t, x))
        phase = pow(2, -1, p)*sum(a*b for a, b in zip(x, z))+sum(a*b for a, b in zip(z, t))
        matrix[_index(output, p), j] = omega**(phase % p)
    return matrix


def _gate_matrix(p, width, gate, *, wrong_phase=False):
    omega = np.exp(2j*np.pi/p)
    matrix = np.zeros((p**width, p**width), dtype=complex)
    i, value = gate.sites[0], gate.parameter
    for column, point in enumerate(_points(p, width)):
        output = list(point)
        amplitude = 1
        if gate.kind == "fourier":
            for y in range(p):
                output[i] = y
                matrix[_index(output, p), column] = omega**(value*y*point[i] % p)/np.sqrt(p)
            continue
        if gate.kind == "scale":
            output[i] = value*point[i] % p
        elif gate.kind == "add":
            j = gate.sites[1]
            output[j] = (point[j]+value*point[i]) % p
        elif gate.kind == "swap":
            j = gate.sites[1]
            output[i], output[j] = output[j], output[i]
        elif gate.kind == "phase":
            polynomial = point[i]*(point[i]-int(wrong_phase))
            amplitude = omega**(value*pow(2, -1, p)*polynomial % p)
        elif gate.kind == "cz":
            amplitude = omega**(value*point[i]*point[gate.sites[1]] % p)
        else:
            raise AssertionError("unexpected primitive")
        matrix[_index(output, p), column] = amplitude
    return matrix


def _unitary(plan):
    matrix = np.eye(plan.p**plan.width, dtype=complex)
    for gate in plan.gates:
        matrix = _gate_matrix(plan.p, plan.width, gate) @ matrix
    return matrix


@pytest.mark.parametrize("gate", [
    CliffordGate("fourier", (0,), 1), CliffordGate("fourier", (1,), -1),
    CliffordGate("scale", (0,), 2), CliffordGate("phase", (1,), 2),
    CliffordGate("add", (1, 0), 2), CliffordGate("cz", (0, 1), 2),
    CliffordGate("swap", (0, 1)),
])
def test_primitive_conventions_have_exact_not_projective_weyl_covariance(gate):
    p, width = 3, 2
    unitary = _gate_matrix(p, width, gate)
    tableau = symplectic_action(p, width, (gate,))
    np.testing.assert_allclose(unitary.conj().T @ unitary, np.eye(p**width), atol=1e-13)
    for vector in _points(p, 2*width):
        np.testing.assert_allclose(unitary @ _weyl(p, vector) @ unitary.conj().T,
                                   _weyl(p, _mv(tableau, vector, p)), atol=1e-13)


@pytest.mark.parametrize("p", [3, 5])
def test_all_one_qudit_symplectic_matrices_including_singular_a_blocks(p):
    count = 0
    for a, b, c, d in product(range(p), repeat=4):
        if (a*d-b*c) % p != 1:
            continue
        plan = compile_symplectic(p, ((a, b), (c, d)))
        assert len(plan.gates) <= plan.gate_bound
        unitary = _unitary(plan)
        for vector in _points(p, 2):
            np.testing.assert_allclose(unitary @ _weyl(p, vector) @ unitary.conj().T,
                                       _weyl(p, _mv(plan.symplectic, vector, p)), atol=1e-12)
        count += 1
    assert count == p*(p*p-1)


def test_multiqudit_elimination_on_independent_transvection_products():
    p, width = 3, 2
    for seed in range(8):
        rng = random.Random(seed)
        target = _identity(2*width)
        for _ in range(8):
            vector = [rng.randrange(p) for _ in range(2*width)]
            functional = vector[width:]+[-x % p for x in vector[:width]]
            step = [[(int(i == j)+vector[i]*functional[j]) % p
                     for j in range(2*width)] for i in range(2*width)]
            target = _product(step, target, p)
        plan = compile_symplectic(p, target)
        unitary = _unitary(plan)
        np.testing.assert_allclose(unitary.conj().T @ unitary, np.eye(p**width), atol=1e-12)
        for vector in _points(p, 2*width):
            np.testing.assert_allclose(unitary @ _weyl(p, vector) @ unitary.conj().T,
                                       _weyl(p, _mv(target, vector, p)), atol=1e-12)


def test_standard_unsymmetrized_phase_gate_has_right_tableau_but_wrong_phase():
    p, gate, vector = 5, CliffordGate("phase", (0,), 2), (1, 0)
    tableau = symplectic_action(p, 1, (gate,))
    expected = _weyl(p, _mv(tableau, vector, p))
    good = _gate_matrix(p, 1, gate)
    wrong = _gate_matrix(p, 1, gate, wrong_phase=True)
    np.testing.assert_allclose(good @ _weyl(p, vector) @ good.conj().T, expected, atol=1e-13)
    actual = wrong @ _weyl(p, vector) @ wrong.conj().T
    byproduct = np.exp(2j*np.pi*(-gate.parameter*pow(2, -1, p) % p)/p)
    np.testing.assert_allclose(actual, byproduct*expected, atol=1e-13)
    assert np.linalg.norm(actual-expected) > 1


@pytest.mark.parametrize("p", [7, 2**127-1])
def test_real_variable_radical_alignment_compiles_without_enumerating_the_carrier(p):
    forms = [[[0, 1], [p-1, 0]]]
    labels, scales = [[1], [p-1]]*3, [2, 2, 3, 3, 4, 4]
    outcomes = [[i] for i in range(6)]
    alignment = align_variable_jets(p, forms, labels, scales, outcomes)
    assert alignment.maps.mixed_padding_qudits == 0
    plan = compile_alignment(alignment)
    assert plan.width == alignment.maps.carrier_width == 6
    assert plan.symplectic == alignment.symplectic
    assert symplectic_action(p, plan.width, plan.gates) == alignment.symplectic
    assert sum(plan.primitive_counts.values()) == len(plan.gates) <= plan.gate_bound
    bad = replace(alignment, symplectic=tuple(map(tuple, _identity(12))))
    with pytest.raises(ValueError, match="alignment"):
        compile_alignment(bad)


def test_127_bit_prime_high_width_and_identity_have_bounded_plans():
    p, width = 2**127-1, 16
    vector = [pow(17, i+1, p) for i in range(2*width)]
    functional = vector[width:]+[-x % p for x in vector[:width]]
    # Independent rank-one symplectic transvection I + v*Omega(v, .).
    target = [[(int(i == j)+vector[i]*functional[j]) % p
               for j in range(2*width)] for i in range(2*width)]
    plan = compile_symplectic(p, target)
    assert symplectic_action(p, width, plan.gates) == tuple(map(tuple, target))
    assert len(plan.gates) <= plan.gate_bound
    assert not compile_symplectic(p, _identity(2*width)).gates


@pytest.mark.parametrize("p,matrix", [
    (2, [[1, 0], [0, 1]]), (9, [[1, 0], [0, 1]]), (True, [[1, 0], [0, 1]]),
    (5, []), (5, [[1]]), (5, [[1, 0], [0, 2]]),
    (5, [[1, 0], [0, 5]]), (5, [[True, 0], [0, 1]]),
])
def test_rejects_invalid_fields_and_noncanonical_or_nonsymplectic_inputs(p, matrix):
    with pytest.raises(ValueError):
        compile_symplectic(p, matrix)


@pytest.mark.parametrize("gate", [
    CliffordGate("unknown", (0,)), CliffordGate("fourier", (0,), 0),
    CliffordGate("add", (0, 0), 1), CliffordGate("scale", (0,), 0),
    CliffordGate("phase", (True,), 1), CliffordGate("cz", (0, 2), 1),
    CliffordGate("swap", (0, 1), 2), CliffordGate("phase", (0,), 3),
])
def test_replay_rejects_invalid_primitive_descriptions(gate):
    with pytest.raises(ValueError):
        symplectic_action(3, 2, (gate,))
