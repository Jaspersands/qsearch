"""Exact public-controller tests and bounded physical source checks only."""
from fractions import Fraction
from itertools import product
from math import comb
import random

import numpy as np
import pytest

from theorems.affine_phase_erasure import PhasePacket, merge_branch
from theorems.polynomial_phase_copy_learning import (
    LearningFrame, copy_envelope, erase_line_degree, report,
)


def _poly(frame, coefficients, point):
    return sum(c*np.prod([pow(x, a, frame.p) for x, a in zip(point, alpha)], dtype=object)
               for c, alpha in zip(coefficients, frame.indices)) % frame.p


def _coefficients(frame, eta):
    return tuple((x+sum(a*v[j] for a, v in zip(eta, frame.basis))) % frame.p
                 for j, x in enumerate(frame.known))


def _state(packet, eta):
    return {(x,): np.exp(2j*np.pi*int(packet.evaluate_fixture((x,), eta))/packet.p)
                   /np.sqrt(packet.p) for x in range(packet.p)}


def test_random_measured_line_has_correct_phase_without_chosen_line_access():
    frame = LearningFrame.initial(5, 2, 3)
    eta = tuple(range(5))+(1, 2, 3, 4)
    # Exercise nonzero known correction after a legitimate parameter equation.
    relation = (1, 2)+(0,)*7
    frame = frame.learn_relation(relation, (eta[0]+2*eta[1]) % 5)
    eta = eta[1:]
    coefficients = _coefficients(frame, eta)
    axis = frame.next_axis()
    for y in range(5):
        correction, packet = frame.restrict(axis, (y,))
        actual = []
        for t in range(5):
            point = (t, y) if axis == 0 else (y, t)
            actual.append(np.exp(2j*np.pi*int(_poly(frame, coefficients, point))/5)/5)
        assert sum(abs(x)**2 for x in actual) == pytest.approx(1/5)
        corrected = np.array([a*np.exp(-2j*np.pi*sum(c*pow(t, r, 5)
                               for r, c in enumerate(correction))/5)
                              for t, a in enumerate(actual)])*np.sqrt(5)
        expected = np.array(list(_state(packet, eta).values()))
        assert abs(np.vdot(expected, corrected)) == pytest.approx(1)


def test_line_rejection_bound_is_tight_and_keeps_rejected_copies_charged():
    initial = LearningFrame.initial(5, 2, 3)
    # x0*(x1-1)*(x1-2): coordinate slices y=1,2 carry no unknown coefficient.
    coefficients = {(1, 2): 1, (1, 1): 2, (1, 0): 2}
    row = tuple(coefficients.get(alpha, 0) for alpha in initial.indices)
    frame = LearningFrame(5, 2, 3, initial.known, (row,))
    assert frame.next_axis() == 0
    accepted = sum(frame.restrict(0, (y,))[1].degree > 0 for y in range(5))
    assert Fraction(accepted, 5) == copy_envelope(5, 2, 3)["line_acceptance_lower_bound"]


def test_parameter_substitution_preserves_every_polynomial_coefficient():
    rng = random.Random(915)
    frame = LearningFrame.initial(101, 3, 3)
    original = eta = tuple(rng.randrange(101) for _ in frame.basis)
    while eta:
        relation = tuple(rng.randrange(1, 101) for _ in eta)
        value = sum(a*b for a, b in zip(relation, eta)) % 101
        frame = frame.learn_relation(relation, value)
        eta = eta[1:]
        assert _coefficients(frame, eta) == original
    assert frame.known == original
    with pytest.raises(ValueError, match="no unknown"):
        frame.next_axis()


def test_cubic_instrument_all_records_and_failure_mass():
    packet = PhasePacket(5, 1, 1, {(3,): (1,)})
    state = _state(packet, (2,))
    accepted = 0
    total_mass = 0
    for values in product(range(5), repeat=2):
        outcomes = tuple((v,) for v in values)
        reduced = erase_line_degree([packet, packet], [1, 4], outcomes)
        physical, mass = merge_branch(5, [state, state], [1, 4], outcomes)
        total_mass += mass
        assert mass == pytest.approx(1/25)
        expected = _state(reduced, (2,))
        assert abs(sum(np.conj(expected[x])*physical[x] for x in expected)) == pytest.approx(1)
        accepted += bool(reduced.degree)
    assert total_mass == pytest.approx(1)
    assert Fraction(accepted, 25) == Fraction(4, 5)


def test_two_actual_instruments_then_fourier_relation_without_hidden_feedback():
    cubic = PhasePacket(5, 1, 1, {(3,): (1,)})
    original = _state(cubic, (2,))
    ys = ((0,), (1,))
    quadratic = erase_line_degree([cubic, cubic], [1, 4], ys)
    actual_q, first_mass = merge_branch(5, [original, original], [1, 4], ys)
    linear = erase_line_degree([quadratic, quadratic], [1, 2], ys)
    actual_l, second_mass = merge_branch(5, [actual_q, actual_q], [1, 2], ys)
    assert linear.degree == 1
    # Two independently prepared first branches, not copying one quantum state.
    assert first_mass**2*second_mass == pytest.approx(Fraction(1, 5**6))
    probabilities = abs(np.fft.fft(np.array([actual_l[(x,)] for x in range(5)]))/np.sqrt(5))**2
    public_relation = linear.coefficients[(1,)][0]
    assert public_relation != 0
    assert probabilities[2*public_relation % 5] == pytest.approx(1)
    frame = LearningFrame(5, 1, 3, (0, 0, 0), ((0, 0, 1),))
    learned = frame.learn_relation((public_relation,), int(np.argmax(probabilities)))
    assert learned.known == (0, 0, 2)


def test_nonidentical_public_maps_do_not_need_uniform_or_repeated_labels():
    packets = [PhasePacket(5, 1, 2, {(3,): top, (2,): low, (1,): (1, 3)})
               for top, low in (((1, 0), (2, 1)), ((0, 1), (4, 0)), ((1, 1), (0, 3)))]
    states = [_state(packet, (2, 3)) for packet in packets]
    top_nonzero = 0
    for values in product(range(5), repeat=3):
        outcomes = tuple((v,) for v in values)
        reduced = erase_line_degree(packets, [1, 1, 4], outcomes)
        physical, mass = merge_branch(5, states, [1, 1, 4], outcomes)
        assert mass == Fraction(1, 125)
        expected = _state(reduced, (2, 3))
        assert abs(sum(np.conj(expected[x])*physical[x] for x in expected)) == pytest.approx(1)
        top_nonzero += reduced.degree == 2
    assert Fraction(top_nonzero, 125) >= Fraction(4, 5)


@pytest.mark.parametrize("p,width,degree", [(5, 2, 3), (101, 8, 3), (2**127-1, 8, 3)])
def test_budget_has_no_field_enumeration_and_pays_local_retries(p, width, degree):
    budget = copy_envelope(p, width, degree)
    assert budget["unknown_coefficients_mod_constant"] == comb(width+degree, degree)-1
    expected = budget["expected_original_copies_upper_bound"]
    assert expected/budget["original_copy_abort_cap"] <= Fraction(1, 6)
    assert budget["line_acceptance_lower_bound"] >= Fraction(2, degree+1)
    assert budget["merge_acceptance_lower_bound"] >= Fraction(degree, degree+1)
    if p > 101:
        assert expected < copy_envelope(101, width, degree)["expected_original_copies_upper_bound"]


def test_invalid_promises_and_fake_progress_are_rejected():
    for p, n, d in ((9, 1, 3), (5, 1, 5), (5, 0, 3), (5, 1, 0)):
        with pytest.raises(ValueError):
            LearningFrame.initial(p, n, d)
    with pytest.raises(ValueError, match="independent"):
        LearningFrame(5, 1, 2, (0, 0), ((1, 0), (1, 0)))
    with pytest.raises(ValueError, match="zero relation"):
        LearningFrame.initial(5, 1, 2).learn_relation((0, 0), 0)
    packet = PhasePacket(5, 1, 1, {(3,): (1,)})
    for scales in ([0, 0], [1, 1]):
        with pytest.raises(ValueError):
            erase_line_degree([packet, packet], scales, ((0,), (0,)))
    with pytest.raises(ValueError, match="strictly below"):
        erase_line_degree([PhasePacket(3, 1, 1, {(3,): (1,)})]*2, [1, 2], ((0,), (0,)))
    with pytest.raises(ValueError):
        copy_envelope(5, 2, 3, Fraction(0))


def test_report_is_not_a_dequantization_or_implemented_quantum_algorithm():
    artifact = report()
    for flag in ("classical_dequantization", "novelty_established", "quantum_learner_implemented",
                 "general_sde_backend_implemented", "asymptotic_theorem_independently_verified",
                 "global_constant_recoverable"):
        assert artifact[flag] is False
