"""Finite controls for the universal source proof, not algorithm candidates.

The first control builds ordinary group cosets and an entire normal QFT.
The second prevents mistaking a fixed-sector identity for QFT completeness.
"""
from itertools import product

import numpy as np
import pytest


def test_actual_nonabelian_normal_cosets_match_traced_matrix_source():
    p = 3
    half, omega = pow(2, -1, p), np.exp(2j*np.pi/p)
    normal = list(product(range(p), repeat=3))
    index = {n: i for i, n in enumerate(normal)}
    quotient = list(product(range(p), repeat=2))
    quotient_index = {q: i for i, q in enumerate(quotient)}
    order, width = len(normal), len(quotient)
    def multiply(a, b):
        x, z, c = a
        y, w, d = b
        return ((x+y) % p, (z+w) % p, (c+d+half*(z*y-x*w)) % p)
    def potential(q):
        return (q % p, 2*q % p, q % p)
    def representation(label, n):
        x, z, c = n
        lam, xi, eta = label
        if not lam:
            return np.array([[omega**((xi*x+eta*z) % p)]])
        result = np.zeros((p, p), dtype=complex)
        for j in range(p):
            result[(j+x) % p, j] = omega**((lam*(c+half*x*z+z*j)) % p)
        return result
    labels = [(0, x, z) for x, z in product(range(p), repeat=2)]+[(lam, 0, 0) for lam in (1, 2)]
    sectors, rows = [], []
    for label in labels:
        d = len(representation(label, (0, 0, 0)))
        start = len(rows)
        rows.extend([[np.sqrt(d/order)*representation(label, n)[i, j].conjugate()
                      for n in normal] for i, j in product(range(d), repeat=2)])
        sectors.append((label, start, d))
    transform = np.array(rows)
    np.testing.assert_allclose(transform.conj().T @ transform, np.eye(order), atol=1e-13)
    assert len(rows) == order

    # G=N x C_p^2, H={(potential(u),(u,0))}; U is a PROPER line.
    # Construct actual right cosets, not a promised phase-kernel fixture.
    density, wrong_side = [np.zeros((width*order, width*order), dtype=complex) for _ in range(2)]
    for q, n in product(quotient, normal):
        a = quotient_index[q]*order+index[n]
        for u in range(p):
            assert multiply(potential(q[0]), potential(u)) == potential(q[0]+u)
            other = quotient_index[((q[0]+u) % p, q[1])]
            b = other*order+index[multiply(n, potential(u))]
            density[a, b] += 1/(width*order)
            incorrect = other*order+index[multiply(potential(u), n)]
            wrong_side[a, incorrect] += 1/(width*order)
    assert np.trace(density) == pytest.approx(1)
    assert np.linalg.eigvalsh(density).min() > -1e-13
    complete = np.kron(np.eye(width), transform)
    output = complete @ density @ complete.conj().T
    wrong_output = complete @ wrong_side @ complete.conj().T
    pure = np.zeros(width*order, dtype=complex)
    for u in range(p):
        pure[quotient_index[(u, 0)]*order+index[potential(u)]] = 1/np.sqrt(p)
    pure_output = complete @ np.outer(pure, pure.conj()) @ complete.conj().T
    total_probability, saw_wrong_side = 0, False
    for label, start, d in sectors:
        actual = np.zeros((width*d, width*d), dtype=complex)
        incorrect = actual.copy()
        conditioned = actual.copy()
        for i in range(d):
            addresses = [q*order+start+i*d+j for q, j in product(range(width), range(d))]
            actual += output[np.ix_(addresses, addresses)]
            incorrect += wrong_output[np.ix_(addresses, addresses)]
            conditioned += pure_output[np.ix_(addresses, addresses)]
        probability = d*d/order
        assert np.trace(actual) == pytest.approx(probability)
        gauges = [representation(label, potential(q[0])) for q in quotient]
        expected = np.block([[a.conj().T @ b if q[1] == r[1] else np.zeros((d, d))
                              for r, b in zip(quotient, gauges)]
                             for q, a in zip(quotient, gauges)])/(width*d)
        np.testing.assert_allclose(actual/probability, expected, atol=1e-13)
        # Conditioning on a single hiding-output label keeps a proper
        # affine quotient coset; it is not the uniform mixed-source premise.
        assert np.trace(conditioned) == pytest.approx(probability)
        outside = [i*d+j for i, q in enumerate(quotient) if q[1] != 0 for j in range(d)]
        np.testing.assert_allclose(np.diag(conditioned)[outside], 0, atol=1e-13)
        assert np.linalg.norm(conditioned/probability-expected) > 0.1
        if d > 1:
            saw_wrong_side |= np.linalg.norm(incorrect/probability-expected) > 0.1
        total_probability += probability
    assert total_probability == pytest.approx(1)
    assert saw_wrong_side


def test_unitary_representation_alone_does_not_certify_a_fourier_measurement():
    order, dimension = 3, 2
    # Two copies of the trivial representation are unitary but reducible.
    matrices = [np.eye(dimension) for _ in range(order)]
    for a, b in product(range(order), repeat=2):
        np.testing.assert_array_equal(matrices[a] @ matrices[b], matrices[(a+b) % order])
        np.testing.assert_array_equal(matrices[a].conj().T @ matrices[a], np.eye(dimension))
    sector = np.array([[np.sqrt(dimension/order)*matrix[i, j] for matrix in matrices]
                       for i, j in product(range(dimension), repeat=2)])
    sector_trace = np.trace(sector @ (np.eye(order)/order) @ sector.conj().T)
    assert sector_trace == pytest.approx(dimension**2/order)
    assert sector_trace > 1
    assert np.linalg.eigvalsh(sector.conj().T @ sector).max() > 1
    # The fixed-sector trace formula holds, but this cannot be a Kraus
    # branch of any trace-preserving measurement with the stated scaling.
