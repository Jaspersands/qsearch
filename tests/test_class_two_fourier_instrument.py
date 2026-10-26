"""Dense finite controls for the written class-two Fourier circuit.

These compare actual Fourier/permutation/phase stages with representation
coefficients. Dense tables are diagnostics, NOT the scalable implementation.
"""
from itertools import product

import numpy as np
import pytest

from theorems.class_four_matrix_source import label_coordinates


def _points(p, width):
    return list(product(range(p), repeat=width))


def _index(point, p):
    index = 0
    for coordinate in point:
        index = p*index + coordinate
    return index


def _dot(left, right):
    return sum(a*b for a, b in zip(left, right))


def _coordinates(plan, v, p):
    values = tuple(_dot(row, v) % p for row in plan.weyl + plan.radical)
    r = plan.qudits
    return values[:r], values[r:2*r], values[2*r:]


def _form(width, i=None, j=None):
    value = [[0]*width for _ in range(width)]
    if i is not None:
        value[i][j], value[j][i] = 1, 2  # This finite diagnostic uses p=3.
    return value


def _factorized_transform(p, forms, *, omit_half_phase=False):
    """Apply the described stages to all basis columns, not the QFT formula."""
    w, z = len(forms[0]), len(forms)
    order = p**(w+z)
    omega = np.exp(2j*np.pi/p)
    columns = np.eye(order, dtype=complex).reshape((p,)*(w+z)+(order,))
    for axis in range(w, w+z):
        columns = np.fft.fft(columns, axis=axis, norm="ortho")
    columns = columns.reshape(p**w, p**z, order)
    blocks = []
    for label_index, label in enumerate(_points(p, z)):
        plan = label_coordinates(p, forms, label)
        r = plan.qudits
        block = np.empty((p**w, order), dtype=complex)
        destinations = set()
        for v_index, v in enumerate(_points(p, w)):
            a, b, t = _coordinates(plan, v, p)
            destination = _index(a+b+t, p)
            destinations.add(destination)
            block[destination] = columns[v_index, label_index]
        assert len(destinations) == p**w
        if not omit_half_phase:
            for address, value in enumerate(_points(p, w)):
                phase = -pow(2, -1, p)*_dot(value[:r], value[r:2*r]) % p
                block[address] *= omega**phase
        block = block.reshape((p,)*w+(order,))
        # Fourier transform b -> j and t -> alpha; a remains quantum.
        for axis in range(r, w):
            block = np.fft.fft(block, axis=axis, norm="ortho")
        block = block.reshape(p**w, order)
        relabeled = np.empty_like(block)
        for row, output in enumerate(_points(p, w)):
            alpha, i, j = output[:w-2*r], output[w-2*r:w-r], output[w-r:]
            a = tuple((x-y) % p for x, y in zip(i, j))
            relabeled[row] = block[_index(a+j+alpha, p)]
        blocks.append(relabeled)
    return np.concatenate(blocks)


def _representation(p, plan, label, alpha, element, *, omit_half_phase=False):
    w = len(plan.weyl)+len(plan.radical)
    a, b, t = _coordinates(plan, element[:w], p)
    phase = _dot(label, element[w:])+_dot(alpha, t)
    if not omit_half_phase:
        phase += pow(2, -1, p)*_dot(a, b)
    omega = np.exp(2j*np.pi/p)
    d = p**plan.qudits
    matrix = np.zeros((d, d), dtype=complex)
    for j_index, j in enumerate(_points(p, plan.qudits)):
        i = tuple((x+y) % p for x, y in zip(a, j))
        matrix[_index(i, p), j_index] = omega**((phase+_dot(b, j)) % p)
    return matrix


def _representation_transform(p, forms):
    w, z = len(forms[0]), len(forms)
    elements = _points(p, w+z)
    order = len(elements)
    rows, sectors = [], []
    for label in _points(p, z):
        plan = label_coordinates(p, forms, label)
        d = p**plan.qudits
        for alpha in _points(p, w-2*plan.qudits):
            sectors.append((label, alpha, plan, len(rows), d))
            matrices = np.array([_representation(p, plan, label, alpha, n) for n in elements])
            rows.extend(np.sqrt(d/order)*matrices.conjugate().transpose(1, 2, 0).reshape(d*d, order))
    return np.array(rows), sectors


def _multiply(p, forms, left, right):
    w = len(forms[0])
    v, other = left[:w], right[:w]
    bracket = [sum(v[i]*form[i][j]*other[j] for i in range(w) for j in range(w))
               for form in forms]
    return tuple((x+y) % p for x, y in zip(v, other)) + tuple(
        (x+y+pow(2, -1, p)*b) % p for x, y, b in zip(left[w:], right[w:], bracket)
    )


@pytest.mark.parametrize("forms", [
    [_form(2, 0, 1), _form(2)],
    [_form(3, 0, 1), _form(3, 0, 2)],
    [_form(4, 0, 1), _form(4, 2, 3)],
])
def test_complete_factorization_matches_all_variable_rank_representation_sectors(forms):
    p = 3
    actual = _factorized_transform(p, forms)
    expected, sectors = _representation_transform(p, forms)
    np.testing.assert_allclose(actual, expected, atol=1e-13)
    np.testing.assert_allclose(actual.conj().T @ actual, np.eye(len(actual)), atol=1e-13)
    assert sum(d*d for _, _, _, _, d in sectors) == len(actual)
    mass = {label: 0 for label in _points(p, len(forms))}
    for label, _, _, _, d in sectors:
        mass[label] += d*d/len(actual)
    assert all(value == pytest.approx(p**-len(forms)) for value in mass.values())
    if len(forms[0]) == 2:
        assert any(any(label) and d == 1 for label, _, _, _, d in sectors)
    if len(forms[0]) == 4:
        assert {d for _, _, _, _, d in sectors} == {1, 3, 9}


def test_half_phase_is_required_even_though_omitting_it_preserves_unitarity():
    p, forms, label, alpha = 3, [_form(2, 0, 1)], (1,), ()
    wrong = _factorized_transform(p, forms, omit_half_phase=True)
    right, _ = _representation_transform(p, forms)
    np.testing.assert_allclose(wrong.conj().T @ wrong, np.eye(len(wrong)), atol=1e-13)
    assert np.linalg.norm(wrong-right) > 1
    plan = label_coordinates(p, forms, label)
    x, y = (1, 0, 0), (0, 1, 0)
    xy = _multiply(p, forms, x, y)
    rho = lambda n: _representation(p, plan, label, alpha, n)
    bad = lambda n: _representation(p, plan, label, alpha, n, omit_half_phase=True)
    np.testing.assert_allclose(rho(x) @ rho(y), rho(xy), atol=1e-13)
    assert np.linalg.norm(bad(x) @ bad(y)-bad(xy)) > 1


def test_radical_character_and_weyl_coordinates_give_actual_group_representations():
    p, forms = 3, [_form(3, 0, 1), _form(3, 0, 2)]
    pairs = [((1, 2, 0, 1, 2), (2, 0, 1, 2, 1)),
             ((0, 1, 2, 2, 0), (1, 1, 1, 0, 2))]
    for label in _points(p, 2):
        plan = label_coordinates(p, forms, label)
        for alpha in _points(p, 3-2*plan.qudits):
            for x, y in pairs:
                matrices = [_representation(p, plan, label, alpha, n)
                            for n in (x, y, _multiply(p, forms, x, y))]
                np.testing.assert_allclose(matrices[0] @ matrices[1], matrices[2], atol=1e-13)


def test_factorized_instrument_on_actual_cosets_keeps_zero_rank_nonzero_labels():
    p, forms = 3, [_form(2, 0, 1), _form(2)]
    normal = _points(p, 4)
    order = len(normal)
    transform = _factorized_transform(p, forms)
    _, sectors = _representation_transform(p, forms)
    potential = lambda u: (u % p, 2*u % p, u % p, 2*u % p)
    # G=N x C_3 and H is the graph of the homomorphism potential.
    density = np.zeros((p*order, p*order), dtype=complex)
    for q, n, u in product(range(p), normal, range(p)):
        other = _multiply(p, forms, n, potential(u))
        density[q*order+_index(n, p), ((q+u) % p)*order+_index(other, p)] += 1/(p*order)
    complete = np.kron(np.eye(p), transform)
    output = complete @ density @ complete.conj().T
    mass = {label: 0.0 for label in _points(p, 2)}
    for label, alpha, plan, start, d in sectors:
        actual = np.zeros((p*d, p*d), dtype=complex)
        for i in range(d):
            addresses = [q*order+start+i*d+j for q, j in product(range(p), range(d))]
            actual += output[np.ix_(addresses, addresses)]
        probability = d*d/order
        assert np.trace(actual) == pytest.approx(probability)
        gauges = [_representation(p, plan, label, alpha, potential(q)) for q in range(p)]
        expected = np.block([[a.conj().T @ b for b in gauges] for a in gauges])/(p*d)
        np.testing.assert_allclose(actual/probability, expected, atol=1e-13)
        mass[label] += float(np.trace(actual).real)
    assert all(value == pytest.approx(1/p**2) for value in mass.values())
    assert mass[(0, 1)] > 0  # Zero Weyl rank, nonzero central label: retain it.
