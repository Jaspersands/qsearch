"""Composition falsifiers, not new oracle problems or a receiver simulation.

The exact finite kernels expose assumptions a symbolic phase checker cannot
verify: conditional independence, common hidden parameters, nonzero active
support and the active (rather than allocated) branch normalization.
"""
from fractions import Fraction
from itertools import product

import pytest

from theorems.class_three_monomial_jet import FullTaylorJetChart
from theorems.metabelian_induced_phase import InducedPhasePacket, merge_induced_phases


def _branch(p, kernel, scales, outcome):
    """Actual fresh-uniform-register shear/measure branch, in matrix entries."""
    return tuple(tuple(Fraction(1, p) * kernel(
        tuple((y+s*q) % p for y, s in zip(outcome, scales)),
        tuple((y+s*r) % p for y, s in zip(outcome, scales)))
        for r in range(p)) for q in range(p))


@pytest.mark.parametrize("p", [3, 5, 7])
def test_shared_randomness_with_correct_marginals_can_destroy_the_hidden_support(p):
    # Separable state (1/p) sum_l |+_l><+_l| tensor |+_l><+_l|.
    # Root-of-unity orthogonality gives this exact rational matrix.
    # Each marginal is I/p, the valid source for U=0; the joint is NOT
    # the tensor of those marginals. No entanglement is needed to fail.
    def correlated(a, b):
        return Fraction(int(sum(a) % p == sum(b) % p), p*p)

    def independent(a, b):
        return Fraction(int(a == b), p*p)

    for q, r in product(range(p), repeat=2):
        expected = Fraction(int(q == r), p)
        assert sum(correlated((q, z), (r, z)) for z in range(p)) == expected
        assert sum(correlated((z, q), (z, r)) for z in range(p)) == expected
    probability = Fraction(1, p*p)
    for outcome in product(range(p), repeat=2):
        honest = _branch(p, independent, (1, p-1), outcome)
        wrong = _branch(p, correlated, (1, p-1), outcome)
        assert sum(honest[q][q] for q in range(p)) == probability
        assert sum(wrong[q][q] for q in range(p)) == probability
        assert honest[0][1] == 0
        assert wrong[0][1] / probability == Fraction(1, p)
        # Fourier readout would output 0 with certainty instead of a
        # uniform element of U-perp. All branch probabilities still agree.
        assert sum(map(sum, wrong)) / (p*probability) == 1
        assert sum(map(sum, honest)) / (p*probability) == Fraction(1, p)


@pytest.mark.parametrize("p", [3, 5])
def test_zero_scale_discard_uses_active_normalization_not_allocated_arity(p):
    def full_tensor(a, b):
        return Fraction(int(a == b), p**3)

    def reduced(a, b):
        return sum(full_tensor(a+(z,), b+(z,)) for z in range(p))

    for a, b in product(product(range(p), repeat=2), repeat=2):
        assert reduced(a, b) == Fraction(int(a == b), p*p)
    probabilities = []
    for outcome in product(range(p), repeat=2):
        branch = _branch(p, reduced, (1, 1), outcome)
        mass = sum(branch[q][q] for q in range(p))
        assert mass == Fraction(1, p**2)
        assert mass != Fraction(1, p**3)
        probabilities.append(mass)
    assert sum(probabilities) == 1


def _packets():
    ch = FullTaylorJetChart(7, 1, 1, 2)
    q2 = (2,)+(0,)*ch.jet_width
    first = InducedPhasePacket(ch, 2, 2, {(q2, (0,)): 1})
    second = InducedPhasePacket(ch, 2, 2, {(q2, (0,)): 6})
    discarded = InducedPhasePacket(ch, 2, 2, {(q2, (4,)): 3})
    return ch, first, second, discarded


def test_actual_compiler_restricts_a_nonzero_vector_to_its_active_subtype():
    ch, first, second, discarded = _packets()
    zero = (0,)*ch.jet_width
    active_outcomes = [((1,), zero), ((2,), zero)]
    expected = merge_induced_phases([first, second], [1, 1], active_outcomes, 2)
    assert expected.weighted_degree == 1
    for y in range(ch.p):
        actual = merge_induced_phases([first, second, discarded], [1, 1, 0],
                                     active_outcomes+[((y,), (y,)*ch.jet_width)], 2)
        assert actual == expected
    with pytest.raises(ValueError, match="nonzero"):
        ch.transport_matrix((0,), 0)


def test_single_active_input_is_valid_if_its_current_top_degree_vanishes():
    ch, _, _, discarded = _packets()
    q1 = (1,)+(0,)*ch.jet_width
    active = InducedPhasePacket(ch, 2, 2, {(q1, (0,)): 1})
    zero = (0,)*ch.jet_width
    result = merge_induced_phases([active, discarded], [1, 0],
                                 [((0,), zero), ((3,), zero)], 2)
    assert result == active


def test_all_zero_witness_and_stage_zero_are_rejected_even_for_empty_phases():
    ch, first, second, _ = _packets()
    empty = InducedPhasePacket(ch, 2, 2, {})
    outcomes = [((0,), (0,)*ch.jet_width)]*2
    with pytest.raises(ArithmeticError, match="cancellation"):
        merge_induced_phases([empty, empty], [0, 0], outcomes, 1)
    with pytest.raises(ValueError, match="positive degree"):
        merge_induced_phases([first, second], [1, 1], outcomes, 0)


def test_ignoring_the_nonzero_guard_would_create_false_full_support_coherence():
    p = 5
    branch = _branch(p, lambda a, b: Fraction(int(a == b), p*p), (0, 0), (1, 2))
    mass = sum(branch[q][q] for q in range(p))
    assert mass == Fraction(1, p*p)
    assert all(value / mass == Fraction(1, p) for row in branch for value in row)


def test_matching_symbolic_schemas_do_not_certify_one_hidden_instance():
    ch, first, second, _ = _packets()
    outcomes = [((0,), (0,)*ch.jet_width)]*2
    assert not merge_induced_phases([first, second], [1, 1], outcomes, 2).terms
    theta1 = [1]+[0]*(len(first.parameter_basis)-1)
    theta2 = [2]+[0]*(len(first.parameter_basis)-1)
    point = (1,)+(0,)*ch.jet_width
    assert (first.evaluate_fixture(point, theta1)+second.evaluate_fixture(point, theta2)) % ch.p != 0
