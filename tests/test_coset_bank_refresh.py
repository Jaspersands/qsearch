"""Independent finite channel audit; no black-box HSP solver is implemented.

This file deliberately has no theorem-module imports: some of their transitive
dependencies are cloud-offloaded. These tests do not validate that integration.
"""
from itertools import product

import numpy as np
import pytest


D8 = tuple(product(range(4), range(2)))
INDEX = {g: i for i, g in enumerate(D8)}
H = ((0, 0), (0, 1))  # Nonnormal, so left/right mistakes are observable.


def _mul(a, b):
    return ((a[0] + (-1)**a[1]*b[0]) % 4, (a[1] + b[1]) % 2)


def _inv(a):
    return ((-(-1)**a[1]*a[0]) % 4, a[1])


LEFT = np.array([[INDEX[_mul(g, x)] for x in D8] for g in D8])
RIGHT = np.array([[INDEX[_mul(x, _inv(g))] for x in D8] for g in D8])


def _pure(ket):
    return np.outer(ket, np.conjugate(ket))


def _coset(a):
    ket = np.zeros(8)
    for h in H:
        ket[INDEX[_mul(a, h)]] = 1/np.sqrt(len(H))
    return _pure(ket)


RHO = sum(_coset((r, 0)) for r in range(4))/4


def _local_twirl(rho, actions, dimensions, slot):
    order = np.arange(np.prod(dimensions)).reshape(dimensions)
    out = np.zeros_like(rho, dtype=complex)
    for action in actions:
        pullback = np.take(order, np.argsort(action), axis=slot).ravel()
        out += rho[np.ix_(pullback, pullback)]/len(actions)
    return out


def _control_trace(rho, actions):
    # Kraus operator K_z[q,x] = [actions[q,x]=z]/sqrt(number of addresses).
    inverse = np.argsort(actions, axis=1)
    out = np.zeros((len(actions), len(actions)), dtype=complex)
    for z in range(len(rho)):
        indices = inverse[:, z]
        out += rho[np.ix_(indices, indices)]/len(actions)
    return out


def _distance(a, b):
    return np.sum(np.abs(np.linalg.eigvalsh(a-b)))/2


def test_public_controlled_discard_equals_left_twirl_on_every_matrix_unit():
    for i, j in product(range(8), repeat=2):
        unit = np.zeros((8, 8), dtype=complex)
        unit[i, j] = 1j
        np.testing.assert_allclose(_control_trace(unit, RIGHT),
                                   _local_twirl(unit, LEFT, (8,), 0), atol=1e-14)


def test_unknown_fixed_coset_refresh_is_not_right_translation_twirling():
    assert _mul(_mul((1, 0), H[1]), _inv((1, 0))) not in H
    for a in D8:
        np.testing.assert_allclose(_local_twirl(_coset(a), LEFT, (8,), 0),
                                   RHO, atol=1e-14)
    wrong = _local_twirl(_coset((0, 0)), RIGHT, (8,), 0)
    np.testing.assert_allclose(_distance(wrong, RHO), 0.25, atol=1e-14)


def test_correlated_coset_bank_decouples_even_from_quantum_side_information():
    environment = [np.array([1, 0]), np.array([0, 1]),
                   np.array([1, 1])/np.sqrt(2), np.array([1, 1j])/np.sqrt(2)]
    bank = np.zeros((128, 128), dtype=complex)
    env = np.zeros((2, 2), dtype=complex)
    for r, weight in enumerate((0.1, 0.2, 0.3, 0.4)):
        e = _pure(environment[r])
        bank += weight*np.kron(np.kron(_coset((r, 0)), _coset((r ^ 1, 0))), e)
        env += weight*e
    expected = np.kron(np.kron(RHO, RHO), env)
    assert _distance(bank, expected) > 0.5
    out = _local_twirl(bank, LEFT, (8, 8, 2), 0)
    out = _local_twirl(out, LEFT, (8, 8, 2), 1)
    np.testing.assert_allclose(out, expected, atol=1e-14)
    np.testing.assert_allclose(np.trace(out), 1, atol=1e-14)


def test_existing_joint_right_action_lift_already_ignores_classical_coset_centers():
    bank = sum(np.kron(_coset((r, 0)), _coset((r ^ 1, 0))) for r in range(4))/4
    controls = np.array([[8*permutation[a]+permutation[b]
                          for a, b in product(range(8), repeat=2)]
                         for permutation in RIGHT])
    np.testing.assert_allclose(_control_trace(bank, controls), RHO, atol=1e-14)


def test_reusing_one_random_translation_does_not_make_independent_samples():
    bank = sum(np.kron(_coset((r, 0)), _coset((r, 0))) for r in range(4))/4
    shared = np.array([[8*permutation[a]+permutation[b]
                       for a, b in product(range(8), repeat=2)]
                      for permutation in LEFT])
    out = _local_twirl(bank, shared, (64,), 0)
    np.testing.assert_allclose(out, bank, atol=1e-14)
    assert _distance(out, np.kron(RHO, RHO)) > 0.7


def test_refresh_randomness_must_be_ignored_not_conditioned_on():
    record_and_output = np.zeros((64, 64), dtype=complex)
    for i, g in enumerate(D8):
        record = np.zeros(8)
        record[i] = 1
        record_and_output += np.kron(_pure(record), _coset(g))/8
    expected_independence = np.kron(np.eye(8)/8, RHO)
    np.testing.assert_allclose(_distance(record_and_output, expected_independence),
                               0.75, atol=1e-14)
    reduced = np.trace(record_and_output.reshape(8, 8, 8, 8), axis1=0, axis2=2)
    np.testing.assert_allclose(reduced, RHO, atol=1e-14)


def _opposite_charge_bank(p):
    bank = np.zeros((p*p, p*p), dtype=complex)
    for k in range(p):
        second = -k*pow(2, -1, p) % p
        first_ket = np.exp(2j*np.pi*k*np.arange(p)/p)/np.sqrt(p)
        second_ket = np.exp(2j*np.pi*second*np.arange(p)/p)/np.sqrt(p)
        bank += np.kron(_pure(first_ket), _pure(second_ket))/p
    left = np.array([[(x+g) % p for x in range(p)] for g in range(p)])
    controls = np.array([[p*((a-q) % p)+(b-2*q) % p
                          for a, b in product(range(p), repeat=2)] for q in range(p)])
    return bank, left, controls


@pytest.mark.parametrize("p", (3, 5))
def test_separable_correct_marginals_can_survive_refresh_and_falsify_the_lift(p):
    # Explicit convex mixture of PRODUCT character states, not an entangled bank.
    bank, left, controls = _opposite_charge_bank(p)
    for axes in ((0, 2), (1, 3)):
        marginal = np.trace(bank.reshape(p, p, p, p), axis1=axes[0], axis2=axes[1])
        np.testing.assert_allclose(marginal, np.eye(p)/p, atol=1e-14)
    refreshed = _local_twirl(_local_twirl(bank, left, (p, p), 0), left, (p, p), 1)
    np.testing.assert_allclose(refreshed, bank, atol=1e-14)
    actual = _control_trace(refreshed, controls)
    np.testing.assert_allclose(actual, np.ones((p, p))/p, atol=1e-14)
    ideal = _control_trace(np.eye(p*p)/(p*p), controls)
    np.testing.assert_allclose(ideal, np.eye(p)/p, atol=1e-14)
    np.testing.assert_allclose(_distance(actual, ideal), 1-1/p, atol=1e-14)


def test_joint_error_remains_charged_even_when_marginal_error_is_zero():
    p, delta = 3, 0.125
    bad, left, controls = _opposite_charge_bank(p)
    good = np.eye(p*p)/(p*p)
    bank = (1-delta)*good+delta*bad
    refreshed = _local_twirl(_local_twirl(bank, left, (p, p), 0), left, (p, p), 1)
    actual, ideal = _control_trace(refreshed, controls), np.eye(p)/p
    np.testing.assert_allclose(_distance(actual, ideal), delta*(1-1/p), atol=1e-14)
    assert _distance(actual, ideal) <= _distance(bank, good)+1e-14
