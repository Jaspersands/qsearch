from collections import Counter
from itertools import product

import numpy as np
import pytest

from quotient_bridge_controls import (
    FreeClassThreeControl, clean_compiler_error, in_place_householder_falsifier,
    reduction_control, span_rows,
)


@pytest.mark.parametrize("conjugation", [0, 1, 3, 6])
def test_full_reduction_learns_intersections_and_pulls_back_answer(conjugation):
    result = reduction_control(conjugation)
    group, p = result["group"], result["group"].p
    q = (0, conjugation, 0, 0, 0)
    reference = [group.conjugate(q, g) for g in
                 [(1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0)]]
    assert span_rows(result["answer"], 5, p) == span_rows(reference, 5, p)
    assert result["action_result"].action_order == p**2
    assert result["action_result"].stabilizer_order == p
    for probability in (result["first_probability"], result["second_probability"]):
        assert np.isclose(probability.sum(), 1)
        positive = probability[probability > 1e-12]
        assert len(positive) == p
        assert np.allclose(positive, 1/p, atol=1e-14)


def test_actual_noncentral_intersection_is_not_normal_in_ambient_group():
    result = reduction_control(0)
    group = result["group"]
    x, y, z = (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0)
    assert group.conjugate(x, z) != z
    assert result["oracle"](group.conjugate(y, z)) != result["oracle"](group.zero)
    assert result["oracle"](group.conjugate(x, z)) == result["oracle"](group.zero)


@pytest.mark.parametrize("conjugation", [0, 1, 3])
def test_every_quotient_pair_has_correct_original_oracle_fiber(conjugation):
    result = reduction_control(conjugation)
    group, section, project = result["group"], result["section"], result["project"]
    oracle, p = result["oracle"], group.p
    addresses = list(product(range(p), repeat=2))
    nonhomomorphic = False
    for a, b in product(addresses, repeat=2):
        total = tuple((x+y) % p for x, y in zip(a, b))
        multiplied = group.multiply(section(a), section(b))
        assert project(multiplied) == total
        nonhomomorphic |= multiplied != section(total)
        difference = group.multiply(group.inverse(section(a)), section(b))
        assert (oracle(section(a)) == oracle(section(b))) == (oracle(difference) == oracle(group.zero))
    assert nonhomomorphic


def test_bch_control_associativity_and_public_action_without_secret():
    group, rng = FreeClassThreeControl(), np.random.default_rng(120)
    for _ in range(200):
        x, y, z = [tuple(map(int, rng.integers(0, 7, size=5))) for _ in range(3)]
        assert group.multiply(group.multiply(x, y), z) == group.multiply(x, group.multiply(y, z))
        assert group.multiply(x, group.inverse(x)) == group.zero
        lifted = group.lift_action(group.action(x))
        assert group.action(lifted) == group.action(x)


def test_fixture_oracle_hides_the_full_group_cosets_not_just_the_quotient():
    group = FreeClassThreeControl()
    oracle, q = group.oracle(3), (0, 3, 0, 0, 0)
    generators = [group.conjugate(q, h) for h in
                  [(1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0)]]
    fibers = Counter()
    for g in product(range(7), repeat=5):
        label = oracle(g)
        fibers[label] += 1
        for h in generators:
            assert oracle(group.multiply(g, h)) == label
    assert len(fibers) == 7**2
    assert set(fibers.values()) == {7**3}


@pytest.mark.parametrize("delta", [0, 1e-8, .01, .25])
def test_clean_compiler_with_variable_phases_and_garbage(delta):
    rng = np.random.default_rng(14)
    unitaries, answers = [], [0, 1, 1, 0]
    for x, answer in enumerate(answers):
        actual_delta = delta * (x+1)/4
        desired = np.zeros(4, dtype=complex)
        desired[answer] = np.sqrt(1-actual_delta) * np.exp(1j*(x+.2))
        desired[2+1-answer] = np.sqrt(actual_delta) * np.exp(1j*(2*x+.1))
        raw = rng.normal(size=(4, 4)) + 1j*rng.normal(size=(4, 4))
        raw[:, 0] = desired
        unitary, _ = np.linalg.qr(raw)
        unitaries.append(unitary)
    error, failure = clean_compiler_error(unitaries, answers)
    assert failure <= delta + 1e-14
    assert error <= np.sqrt(2*delta) + 1e-13
    assert np.isclose(error**2, 2*failure, atol=1e-13)
    arbitrary_error, arbitrary_failure = clean_compiler_error(
        unitaries, answers, arbitrary_target=True)
    assert np.isclose(arbitrary_failure, failure)
    assert arbitrary_error <= 2*np.sqrt(delta) + 1e-13


@pytest.mark.parametrize("delta", [1e-8, .01, .25])
def test_arbitrary_quantum_target_needs_the_larger_error_bound(delta):
    unitary = np.array([[np.sqrt(1-delta), -np.sqrt(delta)],
                        [np.sqrt(delta), np.sqrt(1-delta)]])
    fresh, _ = clean_compiler_error([unitary], [0])
    arbitrary, failure = clean_compiler_error([unitary], [0], arbitrary_target=True)
    assert np.isclose(fresh**2, 2*failure, atol=1e-14)
    assert np.isclose(arbitrary**2, 4*failure, atol=1e-14)


@pytest.mark.parametrize("dimension", [4, 16, 64])
def test_in_place_basis_accuracy_does_not_bound_coherent_error(dimension):
    h = np.eye(dimension) - 2*np.ones((dimension, dimension))/dimension
    initial = np.ones(dimension)/np.sqrt(dimension)
    actual = h @ np.diag(h @ initial)
    ideal = np.diag(initial)
    expected = in_place_householder_falsifier(dimension)
    assert np.isclose(np.linalg.norm(actual-ideal), expected["uniform_input_error"])
    assert np.isclose(1-h[0, 0]**2, float(expected["basis_failure_probability"]))
    overlap = np.vdot(actual, ideal)
    assert np.isclose(2*np.sqrt(max(0, 1-abs(overlap)**2)),
                      expected["uniform_input_trace_distance"])
    orthogonal = np.zeros(dimension)
    orthogonal[0], orthogonal[1] = 1/np.sqrt(2), -1/np.sqrt(2)
    balanced = (initial + orthogonal)/np.sqrt(2)
    actual_balanced, ideal_balanced = h @ np.diag(h @ balanced), np.diag(balanced)
    # Uniform input alone differs mostly by global phase; this witness does not.
    assert abs(np.vdot(actual_balanced, ideal_balanced)) < 1e-14
    assert expected["balanced_witness_trace_distance"] == 2
    if dimension > 4:
        assert expected["uniform_input_error"] > 2*expected["basis_column_error"]


def test_large_householder_family_is_a_symbolic_falsifier_not_a_dense_run():
    result = in_place_householder_falsifier(2**40)
    assert result["basis_failure_probability"] < 2**-37
    assert result["uniform_input_error_squared"] > 3
    assert result["uniform_input_trace_distance"] < 1e-5
    assert result["balanced_witness_overlap"] == 0
    assert result["balanced_witness_trace_distance"] == 2


def test_invalid_clean_compiler_unitary_is_rejected():
    with pytest.raises(ValueError, match="workspace unitary"):
        clean_compiler_error([np.ones((2, 2))], [0])


@pytest.mark.parametrize("unitaries,answers", [([np.eye(2)], []), ([np.eye(2)], [2])])
def test_invalid_clean_compiler_answers_are_rejected(unitaries, answers):
    with pytest.raises(ValueError):
        clean_compiler_error(unitaries, answers)
