"""Exact-reduction falsifiers, not an implemented Luks or HSP solver.

Colors denote already canonical nonzero coefficient classes modulo p-th
roots of unity. This fixture does not perform that input normalization.
"""
from itertools import product

import numpy as np
import pytest


def identity(d):
    return tuple(tuple(int(i == j) for j in range(d)) for i in range(d))


def multiply(a, b, p):
    return tuple(tuple(sum(x*y for x, y in zip(row, col)) % p
                       for col in zip(*b)) for row in a)


def action(matrix, vector, p):
    return tuple(sum(x*y for x, y in zip(row, vector)) % p for row in matrix)


def phase_embedding(matrix, phase_row, colors):
    d = len(matrix)
    rows = [list(row)+(colors+1)*[0] for row in matrix]
    rows.append(list(phase_row)+[1]+colors*[0])
    for i in range(colors):
        rows.append((d+1)*[0]+[int(i == j) for j in range(colors)])
    return tuple(map(tuple, rows))


def encoded_set(terms, colors):
    assert len({v for v, _, _ in terms}) == len(terms)
    return {tuple(v)+(phase,)+tuple(int(i == color) for i in range(colors))
            for v, phase, color in terms}


def weyl(p, x, z):
    omega, half = np.exp(2j*np.pi/p), pow(2, -1, p)
    out = np.zeros((p, p), dtype=complex)
    for t in range(p):
        out[(t+x) % p, t] = omega**((half*x*z+z*t) % p)
    return out


@pytest.mark.parametrize('p', [3, 5, 7])
def test_phase_colored_set_matches_actual_clifford_conjugation(p):
    terms = (((1, 0), 1, 0), ((p-1, 0), p-1, 0),
             ((0, 1), 0, 1), ((0, p-1), 0, 1))
    amplitudes = (2, 3)
    original = encoded_set(terms, 2)
    omega, half = np.exp(2j*np.pi/p), pow(2, -1, p)
    operator = sum(amplitudes[color]*omega**phase*weyl(p, *v)
                   for v, phase, color in terms)
    assert np.allclose(operator, operator.conj().T)
    outcomes = set()
    for a, b, c in product(range(p), repeat=3):
        # U=D(b,c) P^a. The symmetric-Weyl phase is linear in v,
        # including the -a*b term from the order of composition.
        matrix = ((1, 0), (a, 1))
        phase_row = ((c-a*b) % p, -b % p)
        lifted = phase_embedding(matrix, phase_row, 2)
        moved = {action(lifted, v, p) for v in original}
        unitary = weyl(p, b, c)@np.diag([omega**((half*a*t*t) % p) for t in range(p)])
        actual = unitary@operator@unitary.conj().T
        expected = sum(amplitudes[v[3:].index(1)]*omega**v[2]*weyl(p, *v[:2])
                       for v in moved)
        assert np.allclose(actual, expected)
        fixes = np.allclose(actual, operator)
        assert fixes == (moved == original)
        outcomes.add(fixes)
    assert outcomes == {False, True}


def test_embedding_composition_retains_the_phase_cocycle():
    p = 11
    a, b = ((1, 0), (3, 1)), ((1, 2), (0, 1))
    ell, m = (2, 4), (6, 1)
    ab = multiply(a, b, p)
    combined = tuple((m[j]+sum(ell[k]*b[k][j] for k in range(2))) % p
                     for j in range(2))
    assert multiply(phase_embedding(a, ell, 3), phase_embedding(b, m, 3), p) == \
        phase_embedding(ab, combined, 3)
    assert combined != tuple((x+y) % p for x, y in zip(ell, m))


def test_ignoring_phases_or_colors_admits_false_symmetries():
    p = 5
    terms = (((1, 0), 0, 0), ((p-1, 0), 0, 0))
    source = encoded_set(terms, 1)
    moved = {action(phase_embedding(identity(2), (1, 0), 1), v, p) for v in source}
    assert {v[:2] for v in moved} == {v[:2] for v in source}
    assert moved != source
    operator = weyl(p, 1, 0)+weyl(p, p-1, 0)
    z = weyl(p, 0, 1)
    assert not np.allclose(z@operator@z.conj().T, operator)
    # -I swaps two opposite labels, but not their unequal coefficients.
    colored = encoded_set((((1, 0), 0, 0), ((p-1, 0), 0, 1)), 2)
    negation = phase_embedding(((p-1, 0), (0, p-1)), (0, 0), 2)
    moved = {action(negation, v, p) for v in colored}
    assert {v[:3] for v in moved} == {v[:3] for v in colored}
    assert moved != colored


def test_real_class_four_tableaux_do_not_require_hilbert_space_expansion():
    p = 2**127-1
    generators = []
    for i in range(4):
        a = [list(row) for row in identity(5)]
        inverse_transpose = [list(row) for row in identity(5)]
        a[i][i+1], inverse_transpose[i+1][i] = 1, p-1
        matrix = tuple(tuple(row+[0]*5) for row in a)
        matrix += tuple(tuple([0]*5+row) for row in inverse_transpose)
        generators.append(phase_embedding(matrix, (0,)*10, 1))
    # These are faithful UT5 transvections, hence genuinely class four
    # with nonabelian derived group. Only 12-dimensional field matrices.
    def inverse_transvection(g):
        result = tuple(tuple((2*int(i == j)-g[i][j]) % p for j in range(12))
                       for i in range(12))
        assert multiply(g, result, p) == identity(12)
        return result
    def commutator(g, h):
        return multiply(multiply(multiply(inverse_transvection(g),
                                          inverse_transvection(h), p), g, p), h, p)
    x12 = commutator(generators[0], generators[1])
    x34 = commutator(generators[2], generators[3])
    assert commutator(x12, x34) != identity(12)
    x123 = commutator(x12, generators[2])
    x1234 = commutator(x123, generators[3])
    assert x1234 != identity(12)
    assert all(commutator(x1234, g) == identity(12) for g in generators)
    term = encoded_set((((0, 0, 0, 0, 1, 0, 0, 0, 0, 0), p-1, 0),), 1)
    assert len({action(generators[3], v, p) for v in term}) == 1


def test_clifford_actions_do_not_imply_a_clifford_controlled_algorithm():
    p, half = 5, pow(2, -1, 5)
    # Controlled P^a has diagonal phase a*t^2/2. Conjugating target X
    # gives phase a*t+a/2, not the affine phase of a Pauli operator.
    phase = lambda a, t: half*a*t*t % p
    derivative = lambda a, t: (phase(a, t+1)-phase(a, t)) % p
    mixed_difference = (derivative(1, 1)-derivative(1, 0)
                        -derivative(0, 1)+derivative(0, 0)) % p
    assert mixed_difference == 1
    # Density conjugation symmetry also does not imply Bose symmetry.
    psi = np.eye(p)[:, 1]
    z = weyl(p, 0, 1)
    rho = np.outer(psi, psi)
    assert np.allclose(z@rho@z.conj().T, rho)
    assert not np.allclose(z@psi, psi)
