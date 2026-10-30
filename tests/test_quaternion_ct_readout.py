"""Finite algebra controls for CT readout; no oracle search or receiver backend.

The native fixture uses a skew basis of the Lipschitz quaternion order and
a rational norm-one right rotation. Finite coefficient enumeration checks
unique packet inversion, not the asymptotic Gaussian sampling theorem.
"""

from itertools import product
from math import cos, exp, floor, pi, sin, sqrt

import numpy as np
import sympy as sp


def _mixture_scores(first, second):
    rows = []
    for left, right in zip(first, second, strict=True):
        denominator = sp.simplify(abs(left) ** 2 + abs(right) ** 2)
        if denominator == 0:
            continue
        probability = denominator / 2
        score = sp.simplify(2 * sp.conjugate(left) * right / denominator)
        rows.append((probability, score))
    return rows


def test_bounded_mixture_estimator_keeps_phases_and_disjoint_support():
    pairs = [
        ([sp.Rational(3, 5), sp.Rational(4, 5), 0],
         [0, sp.Rational(5, 13), 12 * sp.I / 13]),
        ([sp.Rational(3, 5), sp.Rational(4, 5), 0],
         [sp.Rational(3, 5), 4 * sp.I / 5, 0]),
        ([1, 0, 0], [0, 1, 0]),
    ]
    for first, second in pairs:
        rows = _mixture_scores(first, second)
        assert sp.simplify(sum(probability for probability, _ in rows)) == 1
        assert all(sp.simplify(abs(score) ** 2) <= 1 for _, score in rows)
        overlap = sum(sp.conjugate(x) * y for x, y in zip(first, second, strict=True))
        mean = sum(probability * score for probability, score in rows)
        assert sp.simplify(mean - overlap) == 0
        # A fresh randomized bit has the same Hadamard-test mean.
        plus = sum(probability * (1 + sp.re(score)) / 2 for probability, score in rows)
        assert sp.simplify(plus - (1 + sp.re(overlap)) / 2) == 0
        # Independent scores also give an unbiased SWAP-test probability.
        square_mean = sum(
            p * q * sp.re(x * sp.conjugate(y))
            for p, x in rows for q, y in rows
        )
        assert sp.simplify(square_mean - abs(overlap) ** 2) == 0


def _packet(center, spacing):
    choices = []
    for coordinate in center:
        scaled = coordinate / spacing
        lower = floor(scaled)
        fraction = scaled - lower
        choices.append(((lower, cos(pi * float(fraction) / 2)),
                        (lower + 1, sin(pi * float(fraction) / 2))))
    for entries in product(*choices):
        amplitude = np.prod([entry[1] for entry in entries])
        if amplitude != 0:
            yield tuple(entry[0] for entry in entries), float(amplitude)


def test_native_skew_order_packets_have_unique_evaluable_coefficients():
    basis = sp.Matrix([[1, 2, 0, 1], [0, 1, 1, 0],
                       [0, 0, 1, 1], [0, 0, 0, 1]])
    rotation = sp.Matrix([[3, -4, 0, 0], [4, 3, 0, 0],
                          [0, 0, 3, 4], [0, 0, -4, 3]]) / 5
    assert basis.det() == 1
    assert rotation.T * rotation == sp.eye(4)
    spacing = sp.Rational(1, 256)
    coefficients = tuple(product(range(-1, 2), repeat=4))
    weights = {
        z: exp(-pi * float((basis * sp.Matrix(z)).dot(basis * sp.Matrix(z))) / 64)
        for z in coefficients
    }
    normalizer = sqrt(sum(weight ** 2 for weight in weights.values()))
    for transform in (sp.eye(4), rotation):
        matrix = transform * basis
        inverse = matrix.inv()
        assert float(2 * spacing * sp.sqrt(4) * inverse.norm()) < 0.125
        amplitudes, owners = {}, {}
        for z in coefficients:
            center = matrix * sp.Matrix(z)
            packet_norm = 0.0
            for cell, packet_amplitude in _packet(center, spacing):
                assert cell not in owners  # Coefficient erasure is injective here.
                owners[cell] = z
                amplitudes[cell] = weights[z] * packet_amplitude / normalizer
                packet_norm += packet_amplitude ** 2
            assert abs(packet_norm - 1) < 1e-12
        assert abs(sum(value ** 2 for value in amplitudes.values()) - 1) < 1e-12
        for cell, expected in amplitudes.items():
            approximate_coefficients = inverse * (spacing * sp.Matrix(cell))
            recovered = tuple(floor(value + sp.Rational(1, 2)) for value in approximate_coefficients)
            assert recovered == owners[cell]
            # Membership must be checked after rounding; rounding alone is not support.
            packet = dict(_packet(matrix * sp.Matrix(recovered), spacing))
            evaluated = weights[recovered] * packet.get(cell, 0.0) / normalizer
            assert abs(evaluated - expected) < 1e-14
        outside = tuple(100000 + j for j in range(4))
        candidate = tuple(floor(value + sp.Rational(1, 2))
                          for value in inverse * (spacing * sp.Matrix(outside)))
        assert candidate not in weights


def test_clifford_output_parities_are_monomial_observables():
    h = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    phase = sp.diag(1, sp.I)
    cnot = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0],
                      [0, 0, 0, 1], [0, 0, 1, 0]])
    circuit = sp.kronecker_product(h, sp.eye(2)) * cnot * sp.kronecker_product(phase, h)
    state = sp.Matrix([sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(2, 3), 0])
    output = circuit * state
    for mask in range(4):
        signs = [(-1) ** ((mask & bitstring).bit_count()) for bitstring in range(4)]
        observable = sp.simplify(circuit.H * sp.diag(*signs) * circuit)
        assert all(sum(observable[row, col] != 0 for col in range(4)) == 1
                   for row in range(4))
        transformed = observable * state
        estimated = sum(p * score for p, score in _mixture_scores(state, transformed))
        actual = sum(sign * abs(value) ** 2 for sign, value in zip(signs, output, strict=True))
        assert sp.simplify(estimated - actual) == 0


def test_shadow_score_amplifies_exponentially_small_amplitude_error():
    for qubits in (8, 32, 80):
        dimension = sp.Integer(2) ** qubits
        amplitude = 1 / sp.sqrt(dimension)
        perturbed = amplitude * sp.Rational(101, 100)
        amplitude_error = perturbed - amplitude
        score_error = (dimension + 1) * (perturbed ** 2 - amplitude ** 2)
        assert score_error > sp.Rational(2, 100)
        assert amplitude_error == 1 / (100 * sp.sqrt(dimension))
    # This is an error-propagation countercontrol, not an estimator lower bound.


def test_efficient_boolean_postprocessing_need_not_have_small_fourier_l1():
    # One quadratic phase factor has four Walsh coefficients of magnitude 1/2.
    table = {(x, y): (-1) ** (x * y) for x, y in product((0, 1), repeat=2)}
    spectrum = {
        (a, b): sum(value * (-1) ** (a * x + b * y)
                    for (x, y), value in table.items()) / sp.Integer(4)
        for a, b in product((0, 1), repeat=2)
    }
    assert sum(abs(value) for value in spectrum.values()) == 2
    for pairs in (1, 4, 16):
        # Tensoring factors costs linear Boolean work but multiplies the l1 norm.
        assert sum(abs(value) for value in spectrum.values()) ** pairs == 2 ** pairs
