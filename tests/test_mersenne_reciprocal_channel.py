"""Finite, conditional Fourier-channel controls for the tagged new relation.

These 48 cases exhaust only N=3, K=1 over F_8 or F_32. They check the
unnormalized radius-mask identity from research/EXACT_PREDICATE_CHANNEL.md
assuming clean full-list coalescence with fixed public padding. This is not
a physical circuit, decoder implementation, source-access construction,
asymptotic proof, or evidence of classical hardness or quantum advantage.

The reference uses direct field equations and exact integer Fourier sums,
not the production predicate, root sampler, or legacy channel workbench.
"""

from fractions import Fraction
from itertools import product
from math import comb

import numpy as np
import pytest

from theorems import mersenne_reciprocal_curve as mersenne
from theorems.explicit_quadratic_opi import element


@pytest.fixture(scope="module", params=((3, 2), (5, 2), (5, 3)))
def finite_field_data(request):
    bits, s = request.param
    q = 1 << bits
    assert q <= 32
    elements = [element(bits, word) for word in range(q)]
    characters = np.array([
        [1-2*int((a*b).trace()) for b in elements] for a in elements
    ], dtype=np.int64)
    predicate = np.array([
        int((x**(-((1 << s)-1))).trace()) if word else 0
        for word, x in enumerate(elements)
    ], dtype=np.int64)
    assert np.count_nonzero(predicate == 0) == q//2
    assert np.count_nonzero(predicate == 1) == q//2
    return bits, s, characters, predicate, np.indices((q, q, q))


@pytest.mark.parametrize("targets", tuple(product((0, 1), repeat=3)))
@pytest.mark.parametrize("radius", (1, 2))
def test_finite_conditional_native_channel(finite_field_data, targets, radius):
    bits, s, characters, predicate, coordinates = finite_field_data
    q, length, message_count = 1 << bits, 3, 1 << bits
    native = (coordinates[0] ^ coordinates[1] ^ coordinates[2]) == 0
    weight = (coordinates != 0).sum(axis=0)
    valid = native.copy()
    for axis, target in enumerate(targets):
        valid &= predicate[coordinates[axis]] == target
    fiber_size = int(valid.sum())
    relative_fiber_size = Fraction(message_count*2**length*fiber_size, q**length)

    root_sums = [characters[:, predicate == target].sum(axis=1)
                 for target in targets]
    source = (root_sums[0][:, None, None]*root_sums[1][None, :, None]
              *root_sums[2][None, None, :])
    masked = source*(weight <= radius)

    # For K=1, D is exactly {(d,d,d)}; encoded field addition is XOR.
    coalesced = sum(
        masked[coordinates[0] ^ d, coordinates[1] ^ d, coordinates[2] ^ d]
        for d in range(q)
    )
    transformed = np.einsum("ia,abc->ibc", characters, coalesced)
    transformed = np.einsum("jb,ibc->ijc", characters, transformed)
    transformed = np.einsum("kc,ijc->ijk", characters, transformed)
    assert np.all(transformed[~native] == 0)

    instance = mersenne.make_instance(bits, s, [0, 1, 2], list(targets), 1)
    budget = mersenne.ideal_budget(instance, radius)
    tau = Fraction(sum(comb(length, j) for j in range(radius+1)), 2**length)
    padding = budget["padding"]
    assert budget["tau"] == tau

    # Classical list-sum rejection samples the coalesced state BEFORE Fourier.
    # Exact integer weights retain interference; sampling the error alone does not.
    intensity = sum(
        masked[coordinates[0] ^ d, coordinates[1] ^ d, coordinates[2] ^ d]**2
        for d in range(q)
    )
    squared = coalesced**2
    assert np.all(squared <= padding*intensity)
    source_norm = sum(map(int, masked.reshape(-1)**2))
    proposal_norm = q*source_norm
    born_norm = sum(map(int, squared.reshape(-1)))
    assert sum(map(int, intensity.reshape(-1))) == proposal_norm
    acceptance_rate = Fraction(born_norm, padding*proposal_norm)
    assert 0 <= acceptance_rate <= 1
    if born_norm:
        # proposal(z) * accept(z), normalized by its total, is exactly B(z)^2/Z.
        for r_weight, b_weight in set(zip(map(int, intensity.reshape(-1)),
                                          map(int, squared.reshape(-1)))):
            if r_weight:
                proposal = Fraction(r_weight, proposal_norm)
                accept = Fraction(b_weight, padding*r_weight)
                assert proposal*accept/acceptance_rate == Fraction(b_weight, born_norm)
            else:
                assert b_weight == 0
        z_over_tau = Fraction(born_norm, proposal_norm)
        assert 1-budget["eta"] <= z_over_tau <= 1+budget["eta"]

    # Restore source, message, padding, and inverse-Fourier normalization.
    # int64 sums are safe at q<=32; squaring uses unbounded Python integers.
    native_integers = tuple(map(int, transformed[valid]))
    observed = Fraction(
        2**length*sum(value**2 for value in native_integers),
        q**(3*length)*message_count*padding,
    )
    assert observed == relative_fiber_size*tau**2/padding
    assert observed >= budget["native_success_per_attempt_lower"]
    assert abs(relative_fiber_size-1) <= budget["eta"]

    if fiber_size:
        expected_integer = message_count*q**length*tau
        assert expected_integer.denominator == 1
        assert set(native_integers) == {expected_integer.numerator}
        point_probability = Fraction(
            2**length*native_integers[0]**2,
            q**(3*length)*message_count*padding,
        )
        assert point_probability/observed == Fraction(1, fiber_size)
    else:
        assert not native_integers
        assert observed == 0  # Empty fibers cannot be conditioned into success.
