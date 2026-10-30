from fractions import Fraction as F
from itertools import product
import math

import numpy as np
import pytest
from scipy.linalg import expm

import linear_pullback as l
from test_defect_observables import build_model, pauli_matrix


def physical_density(model, decoder):
    pilot_model = build_model(model.pilot.m, model.pilot.edges, tuple(map(float, model.pilot.couplings)))
    pilot = expm(-float(model.pilot.beta)*pilot_model.h/2)[:, 0]
    pilot /= np.linalg.norm(pilot)
    dimension = 1 << model.n
    sectors = {}
    for y, amplitude in enumerate(pilot):
        residue = y ^ decoder(model.label(y))
        sectors.setdefault(residue, np.zeros((dimension, dimension), dtype=complex))
        sectors[residue] += amplitude*pauli_matrix(model.n, *model.ordered(y))/math.sqrt(dimension)
    density = sum(matrix @ matrix.conj().T for matrix in sectors.values())
    return pilot, density


@pytest.mark.parametrize("paulis", [((1, 0, 0), (0, 1, 0), (1, 1, 1)),
                                     ((1, 0, 2), (0, 1, 0), (1, 0, 0)),
                                     ((1, 1, 3), (0, 1, 0), (0, 0, 2)),
                                     ((0, 1, 0), (0, 0, 0))])
def test_all_physical_observables_and_phases_match_density(paulis):
    model = l.d.Physical.create(1, paulis, [F((-1)**i, i+1) for i in range(len(paulis))], F(1, 16))
    decoder = l.linear.build_linear_decoder(model)
    pilot, density = physical_density(model, decoder)
    assert abs(np.trace(density)-1) < 2e-14
    for x, z, sign in product(range(2), repeat=3):
        observable = (x, z, (x & z)+2*sign)
        pulled = l.pullback(model, decoder, observable)
        actual = np.trace(density @ pauli_matrix(1, *observable))
        result = 0 if pulled is None else pilot @ pauli_matrix(model.pilot.m, *pulled) @ pilot
        assert abs(result-actual) < 3e-14
        if pulled is not None:
            h, w, p = pulled
            for y in range(1 << model.pilot.m):
                phase = l.d.multiply(l.d.dagger(model.ordered(y ^ h)),
                                    l.d.multiply(observable, model.ordered(y)))
                assert phase == (0, 0, (p+2*(w & y).bit_count()) % 4)


def test_bad_gibbs_decoder_is_not_repaired_or_called_gibbs():
    model = l.d.Physical.create(1, [(0, 1, 0), (0, 0, 0)], [1, 1], F(1, 2))
    decoder = l.linear.LinearDecoder.create(model, (0, 3))
    pilot, density = physical_density(model, decoder)
    pulled = l.pullback(model, decoder, (0, 1, 0))
    value = pilot @ pauli_matrix(2, *pulled) @ pilot
    assert abs(value-math.tanh(0.5)**2) < 2e-14
    assert abs(value+math.tanh(0.5)) > 0.5
    assert abs(value-np.trace(density @ pauli_matrix(1, 0, 1))) < 2e-14


def test_all_linear_sections_of_a_redundant_noncommuting_input():
    model = l.d.Physical.create(1, [(1, 0, 0), (0, 1, 0), (1, 1, 3)],
                                [1, F(-1, 2), F(3, 4)], F(1, 16))
    sections = 0
    for columns in product(range(8), repeat=2):
        try:
            decoder = l.linear.LinearDecoder.create(model, columns)
        except ValueError:
            continue
        sections += 1
        pilot, density = physical_density(model, decoder)
        for x, z in product(range(2), repeat=2):
            observable = x, z, x & z
            pulled = l.pullback(model, decoder, observable)
            assert pulled is not None
            exact = np.trace(density @ pauli_matrix(1, *observable))
            approx = pilot @ pauli_matrix(3, *pulled) @ pilot
            assert abs(exact-approx) < 3e-14
    assert sections == 4


def test_nonlinear_unverified_dimension_and_nonsection_rejected():
    model = l.d.Physical.create(1, [(1, 0, 0), (0, 1, 0)], [1, 1], F(1, 16))
    with pytest.raises(ValueError, match="explicit linear"):
        l.pullback(model, lambda s: s, (1, 0, 0))
    with pytest.raises(ValueError, match="BDB"):
        l.pullback(model, l.linear.LinearDecoder(1, 2, (0, 0)), (1, 0, 0))
    with pytest.raises(ValueError, match="dimensions"):
        l.pullback(model, l.linear.LinearDecoder(2, 2, (0,)*4), (1, 0, 0))


def test_large_noncommuting_pullback_does_not_enumerate_states():
    n = 128
    paulis = [(1 << i, (1 << (i-1)) if i else 0, 0) for i in range(n)]
    model = l.d.Physical.create(n, paulis, [1]*n, F(1, 32))
    decoder = l.linear.build_linear_decoder(model)
    assert model.pilot.edges
    assert l.pullback(model, decoder, paulis[64]) is not None
    assert model.pilot.m == 128
