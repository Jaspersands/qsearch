"""Physical matrix-source shear controls and missing-premise falsifiers.

The dense states and sparse Kraus operators are finite diagnostics, not a
scalable HSP implementation or new toy-oracle candidates.
"""
from itertools import product
from math import prod

import numpy as np
import pytest
from scipy.sparse import csr_matrix


P = 3
POINTS = list(product(range(P), repeat=2))
POINT_INDEX = {point: i for i, point in enumerate(POINTS)}
SUPPORT = {(x, 0) for x in range(P)}


def _difference(q, other):
    return tuple((x-y) % P for x, y in zip(q, other))


def _affine(y, scale, q):
    return tuple((a+scale*b) % P for a, b in zip(y, q))


def _gauges(dimension, variant):
    omega = np.exp(2j*np.pi/dimension)
    gauges = {}
    for q in POINTS:
        matrix = np.zeros((dimension, dimension), dtype=complex)
        for j in range(dimension):
            shift = (q[0]+variant*q[1]) % dimension
            phase = (q[0]*q[1]+q[0]**2+variant*q[1])*j+q[1]
            matrix[(j+shift) % dimension, j] = omega**(phase % dimension)
        gauges[q] = matrix
    return gauges


def _source(gauges, support=SUPPORT):
    d = len(gauges[POINTS[0]])
    return np.block([[gauges[q].conj().T @ gauges[other]
                      if _difference(q, other) in support else np.zeros((d, d))
                      for other in POINTS] for q in POINTS])/(len(POINTS)*d)


def _kraus(scales, outcomes, dimensions):
    """Fresh |+>, subtract s_i*q, then measure ALL old quotient registers."""
    carriers = list(product(*(range(d) for d in dimensions)))
    rows, columns = [], []
    for q_index, q in enumerate(POINTS):
        old_points = [_affine(y, s, q) for y, s in zip(outcomes, scales)]
        for t_index, t in enumerate(carriers):
            address = 0
            for old, d, coordinate in zip(old_points, dimensions, t):
                address = address*len(POINTS)*d+POINT_INDEX[old]*d+coordinate
            rows.append(q_index*len(carriers)+t_index)
            columns.append(address)
    return csr_matrix((np.full(len(rows), 1/np.sqrt(len(POINTS))), (rows, columns)),
                      shape=(len(POINTS)*prod(dimensions),
                             prod(len(POINTS)*d for d in dimensions)))


def _joint_source(gauges):
    result = np.ones((1, 1), dtype=complex)
    for gauge in gauges:
        result = np.kron(result, _source(gauge))
    return result


def _combined(gauges, scales, outcomes):
    result = {}
    for q in POINTS:
        matrix = np.ones((1, 1), dtype=complex)
        for gauge, scale, y in zip(gauges, scales, outcomes):
            matrix = np.kron(matrix, gauge[_affine(y, scale, q)])
        result[q] = matrix
    return result


@pytest.mark.parametrize("scales", [(1, 2), (1, 0), (0, 2), (0, 0)])
def test_all_outcomes_complete_and_match_matrix_kernel_for_variable_carrier_sizes(scales):
    dimensions = (2, 3)
    gauges = [_gauges(d, i+1) for i, d in enumerate(dimensions)]
    joint = _joint_source(gauges)
    completeness = csr_matrix(joint.shape, dtype=complex)
    probability = len(POINTS)**-len(scales)
    for outcomes in product(POINTS, repeat=len(scales)):
        operator = _kraus(scales, outcomes, dimensions)
        actual = operator @ joint @ operator.conj().T
        completeness += operator.conj().T @ operator
        assert np.trace(actual) == pytest.approx(probability)
        support = SUPPORT if any(scales) else set(POINTS)
        expected = _source(_combined(gauges, scales, outcomes), support)
        np.testing.assert_allclose(actual/probability, expected, atol=1e-13)
        if scales == (1, 0):
            active = {q: gauges[0][_affine(outcomes[0], scales[0], q)] for q in POINTS}
            np.testing.assert_allclose(expected, np.kron(_source(active), np.eye(3)/3), atol=1e-13)
        if not any(scales):
            uniform = np.ones((len(POINTS), len(POINTS)))/len(POINTS)
            np.testing.assert_allclose(expected, np.kron(uniform, np.eye(6)/6), atol=1e-13)
    np.testing.assert_allclose(completeness.toarray(), np.eye(len(joint)), atol=1e-13)


def test_correct_marginals_do_not_imply_independent_shear_outcomes():
    n = len(POINTS)
    joint = np.zeros((n*n, n*n), dtype=complex)
    for coset in range(P):
        vector = np.array([int(q[1] == coset)/np.sqrt(P) for q in POINTS])
        pure = np.outer(vector, vector)
        joint += np.kron(pure, pure)/P
    expected_marginal = _source({q: np.ones((1, 1)) for q in POINTS})
    tensor = joint.reshape(n, n, n, n)
    np.testing.assert_allclose(np.einsum("abcb->ac", tensor), expected_marginal, atol=1e-13)
    np.testing.assert_allclose(np.einsum("abad->bd", tensor), expected_marginal, atol=1e-13)
    probabilities = []
    for y in product(POINTS, repeat=2):
        operator = _kraus((1, 1), y, (1, 1))
        probability = np.trace(operator @ joint @ operator.conj().T).real
        expected = P/n**2 if y[0][1] == y[1][1] else 0
        assert probability == pytest.approx(expected)
        probabilities.append(probability)
    assert sum(probabilities) == pytest.approx(1)
    assert sum(value > 1e-12 for value in probabilities) == n*n//P
    assert not np.allclose(probabilities, 1/n**2)


def test_incoherent_fresh_register_keeps_outcome_rates_but_erases_the_support():
    gauges = [_gauges(2, 1), _gauges(3, 2)]
    joint = _joint_source(gauges)
    operator = _kraus((1, 2), ((0, 0), (1, 2)), (2, 3))
    coherent = operator @ joint @ operator.conj().T
    # I/|Q| instead of |+><+| is the mixture of fixed-q Kraus branches.
    quotient_indices = np.repeat(np.arange(len(POINTS)), 6)
    incoherent = coherent*(quotient_indices[:, None] == quotient_indices[None, :])
    assert np.trace(incoherent) == pytest.approx(np.trace(coherent))
    assert np.linalg.norm(coherent-incoherent) > 1e-3
    np.testing.assert_allclose(incoherent/np.trace(incoherent),
                               np.eye(len(incoherent))/len(incoherent), atol=1e-13)


def test_different_hidden_supports_intersect_despite_uniform_outcome_rates():
    first, second = _gauges(2, 1), _gauges(3, 2)
    other_support = {(0, x) for x in range(P)}
    joint = np.kron(_source(first, SUPPORT), _source(second, other_support))
    for outcomes in [((0, 0), (1, 2)), ((2, 1), (0, 2))]:
        operator = _kraus((1, 2), outcomes, (2, 3))
        branch = operator @ joint @ operator.conj().T
        assert np.trace(branch) == pytest.approx(len(POINTS)**-2)
        np.testing.assert_allclose(branch/np.trace(branch), np.eye(len(branch))/len(branch), atol=1e-13)


def test_reusing_an_old_pivot_is_not_the_fresh_register_outcome_law():
    counts = {y: 0 for y in product(POINTS, repeat=2)}
    for q0, q1 in product(POINTS, repeat=2):
        # Keep q0 as the output and shear only the other old register.
        y = ((0, 0), _difference(q1, _affine((0, 0), 2, q0)))
        counts[y] += 1
    assert {y[0] for y, count in counts.items() if count} == {(0, 0)}
    assert sum(count > 0 for count in counts.values()) == len(POINTS)
    assert set(counts.values()) == {0, len(POINTS)}


def test_physical_carrier_unitary_matches_conjugated_gauges_not_left_multiplication():
    gauges = [_gauges(2, 1), _gauges(3, 2)]
    scales, outcomes = (1, 2), ((1, 1), (0, 2))
    operator = _kraus(scales, outcomes, (2, 3))
    branch = operator @ _joint_source(gauges) @ operator.conj().T
    branch /= np.trace(branch)
    d = 6
    fourier = np.exp(2j*np.pi*np.outer(np.arange(d), np.arange(d))/d)/np.sqrt(d)
    phase = np.diag(np.exp(2j*np.pi*np.arange(d)**2/7))
    carrier = fourier @ phase
    physical = np.kron(np.eye(len(POINTS)), carrier)
    actual = physical @ branch @ physical.conj().T
    combined = _combined(gauges, scales, outcomes)
    transformed = {q: carrier @ matrix @ carrier.conj().T for q, matrix in combined.items()}
    np.testing.assert_allclose(actual, _source(transformed), atol=1e-13)
    wrong = {q: carrier @ matrix for q, matrix in combined.items()}
    np.testing.assert_allclose(_source(wrong), branch, atol=1e-13)
    assert np.linalg.norm(actual-_source(wrong)) > 0.1


def test_shear_alignment_and_spectator_measurement_compose_to_one_graph_support():
    omega = np.exp(2j*np.pi/P)
    first = {q: np.diag([omega**(q[0]*j % P) for j in range(P)]) for q in POINTS}
    second = {q: np.diag([omega**((q[0]**2+q[1])*j % P) for j in range(P)]) for q in POINTS}
    joint = _joint_source((first, second))
    fourier = np.exp(2j*np.pi*np.outer(np.arange(P), np.arange(P))/P)/np.sqrt(P)
    carrier = np.kron(fourier, np.eye(P))
    physical = np.kron(np.eye(len(POINTS)), carrier)
    retained = [(q, j) for q in POINTS for j in range(P)]
    for outcomes in [((0, 0), (0, 0)), ((1, 2), (2, 1)), ((2, 2), (1, 0))]:
        operator = _kraus((1, 2), outcomes, (P, P))
        branch = operator @ joint @ operator.conj().T
        aligned = physical @ branch @ physical.conj().T
        for spectator in range(P):
            addresses = [POINT_INDEX[q]*P*P+j*P+spectator for q, j in retained]
            measured = aligned[np.ix_(addresses, addresses)]
            probability = len(POINTS)**-2/P
            assert np.trace(measured) == pytest.approx(probability)
            phase = {}
            for q in POINTS:
                q2 = _affine(outcomes[1], 2, q)
                phase[q] = omega**(-(q2[0]**2+q2[1])*spectator % P)
            expected = np.array([
                [phase[q]*phase[other].conjugate()/len(retained)
                 if _difference(q, other) in SUPPORT and (j-k-q[0]+other[0]) % P == 0
                 else 0 for other, k in retained] for q, j in retained
            ])
            np.testing.assert_allclose(measured/probability, expected, atol=1e-13)
