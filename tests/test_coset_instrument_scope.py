"""Independent, finite regular-S_3 controls for invariant measurement scope.

These tests do not import the production MI calculation or propose an algorithm.
The candidate-copy bound is exact arithmetic for the existing public test, not a
large-group state simulation, speedup claim, or result on the hard GI ensemble.
"""

from fractions import Fraction
from itertools import combinations, permutations
from math import comb, log2

import numpy as np
import pytest


GROUP = tuple(permutations(range(3)))
INDEX = {g: i for i, g in enumerate(GROUP)}
IDENTITY = (0, 1, 2)
EYE = np.eye(len(GROUP), dtype=complex)
ATOL = 1e-12


def _multiply(a, b):
    return tuple(a[b[i]] for i in range(3))


def _inverse(g):
    return tuple(g.index(i) for i in range(3))


def _conjugate(x, g):
    return _multiply(_multiply(x, g), _inverse(x))


def _transposition(pair):
    g = list(IDENTITY)
    i, j = pair
    g[i], g[j] = g[j], g[i]
    return tuple(g)


TRANSPOSITIONS = tuple(_transposition(pair) for pair in combinations(range(3), 2))
PUBLIC = TRANSPOSITIONS[0]


def _action_matrix(action):
    matrix = np.zeros_like(EYE)
    for g, column in INDEX.items():
        matrix[INDEX[action(g)], column] = 1
    return matrix


def _right(g):
    """R_g |a> = |a g^-1>, with a homomorphic regular-action convention."""
    return _action_matrix(lambda a: _multiply(a, _inverse(g)))


def _left(g):
    return _action_matrix(lambda a: _multiply(g, a))


def _conjugation(x):
    return _action_matrix(lambda g: _conjugate(x, g))


def _native_coset_state(hidden):
    rho = np.zeros_like(EYE)
    for g in GROUP:
        ket = np.zeros(len(GROUP), dtype=complex)
        ket[INDEX[g]] = ket[INDEX[_multiply(g, hidden)]] = 1 / np.sqrt(2)
        rho += np.outer(ket, ket.conj()) / len(GROUP)
    return rho


def _weak_irrep_projectors():
    signs = np.array([
        (-1) ** sum(g[i] > g[j] for i in range(3) for j in range(i + 1, 3))
        for g in GROUP
    ])
    trivial = np.ones_like(EYE) / len(GROUP)
    sign = np.outer(signs, signs) / len(GROUP)
    return trivial, sign, EYE - trivial - sign


def _public_effects():
    return (EYE + _right(PUBLIC)) / 2, (EYE - _right(PUBLIC)) / 2


def _final_effects():
    return tuple(P @ F @ P for P in _weak_irrep_projectors() for F in _public_effects())


def _assert_close(actual, expected):
    np.testing.assert_allclose(actual, expected, atol=ATOL, rtol=0)


def _assert_positive(operator):
    assert np.isfinite(operator).all()
    _assert_close(operator, operator.conj().T)
    assert np.linalg.eigvalsh(operator).min() >= -ATOL


def _real_trace(operator):
    trace = np.trace(operator)
    assert abs(trace.imag) <= ATOL
    return float(trace.real)


def _assert_density(rho):
    _assert_positive(rho)
    assert _real_trace(rho) == pytest.approx(1, abs=ATOL, rel=0)


def _probabilities(states, effects):
    for effect in effects:
        _assert_positive(effect)
    _assert_close(sum(effects), EYE)
    for rho in states:
        _assert_density(rho)
    probabilities = np.array([
        [_real_trace(effect @ rho) for effect in effects] for rho in states
    ])
    assert np.isfinite(probabilities).all()
    assert probabilities.min() >= -ATOL
    assert probabilities.max() <= 1 + ATOL
    _assert_close(probabilities.sum(axis=1), np.ones(len(states)))
    # Clip only roundoff after checking physicality, bounds, and normalization.
    return np.clip(probabilities, 0, 1)


def _mutual_information(probabilities):
    """Shannon MI for a uniform hidden-transposition prior, including zero cells."""
    assert np.isfinite(probabilities).all()
    assert (probabilities >= 0).all()
    assert (probabilities <= 1).all()
    _assert_close(probabilities.sum(axis=1), np.ones(len(probabilities)))
    marginal = np.broadcast_to(probabilities.mean(axis=0), probabilities.shape)
    positive = probabilities > 0
    return float(np.sum(
        probabilities[positive] * np.log2(probabilities[positive] / marginal[positive])
    ) / len(probabilities))


def _binary_entropy(p):
    return -p * log2(p) - (1 - p) * log2(1 - p)


@pytest.mark.parametrize("hidden", TRANSPOSITIONS)
def test_native_coset_state_is_normalized_psd_and_conjugation_covariant(hidden):
    rho = _native_coset_state(hidden)
    _assert_density(rho)
    _assert_close(rho, (EYE + _right(hidden)) / len(GROUP))
    _assert_close(np.diag(rho), np.full(len(GROUP), 1 / len(GROUP)))
    _assert_close(np.linalg.eigvalsh(rho), [0, 0, 0, 1 / 3, 1 / 3, 1 / 3])
    for x in GROUP:
        C = _conjugation(x)
        _assert_close(C.conj().T @ C, EYE)
        _assert_close(C, _left(x) @ _right(x))
        _assert_close(C @ rho @ C.conj().T, _native_coset_state(_conjugate(x, hidden)))


def test_old_fixed_subgroup_incoherent_mixture_is_not_native_or_covariant():
    def old_mixture(label):
        rho = np.zeros_like(EYE)
        for g in (IDENTITY, PUBLIC):
            index = INDEX[_multiply(g, label)]
            rho[index, index] += 1 / 2
        return rho

    x = (1, 2, 0)
    C = _conjugation(x)
    old = old_mixture(PUBLIC)
    old_conjugate_label = old_mixture(_conjugate(x, PUBLIC))
    _assert_density(old)
    _assert_density(old_conjugate_label)
    assert not np.allclose(old, _native_coset_state(PUBLIC), atol=ATOL, rtol=0)
    residual = C @ old @ C.conj().T - old_conjugate_label
    assert np.max(np.abs(residual)) == pytest.approx(1 / 2, abs=ATOL, rel=0)


def test_weak_irrep_luders_labels_are_blind_but_native_states_are_preserved():
    projectors = _weak_irrep_projectors()
    _assert_close([_real_trace(P) for P in projectors], [1, 1, 4])
    for i, P in enumerate(projectors):
        for j, Q in enumerate(projectors):
            _assert_close(P @ Q, P if i == j else np.zeros_like(EYE))
    states = tuple(_native_coset_state(hidden) for hidden in TRANSPOSITIONS)
    probabilities = _probabilities(states, projectors)
    _assert_close(probabilities, np.tile([1 / 3, 0, 2 / 3], (3, 1)))
    assert abs(_mutual_information(probabilities)) <= ATOL
    for rho in states:
        branches = tuple(P @ rho @ P for P in projectors)
        for branch in branches:
            _assert_positive(branch)
        _assert_close(sum(branches), rho)


def test_post_carrier_readout_is_informative_after_blind_irrep_labels():
    states = tuple(_native_coset_state(hidden) for hidden in TRANSPOSITIONS)
    direct = _probabilities(states, _public_effects())
    _assert_close(direct, [[1, 0], [1 / 2, 1 / 2], [1 / 2, 1 / 2]])
    joint = _probabilities(states, _final_effects())
    _assert_close(joint, [
        [1 / 3, 0, 0, 0, 2 / 3, 0],
        [1 / 3, 0, 0, 0, 1 / 6, 1 / 2],
        [1 / 3, 0, 0, 0, 1 / 6, 1 / 2],
    ])
    branches = np.array([
        [_real_trace(F @ (P @ rho @ P))
         for P in _weak_irrep_projectors() for F in _public_effects()]
        for rho in states
    ])
    _assert_close(joint, branches)
    _assert_close(joint.reshape(3, 3, 2).sum(axis=1), direct)
    _assert_close(joint.reshape(3, 3, 2).sum(axis=2), np.tile([1 / 3, 0, 2 / 3], (3, 1)))
    direct_information = _mutual_information(direct)
    joint_information = _mutual_information(joint)
    assert direct_information == pytest.approx(_binary_entropy(2 / 3) - 2 / 3, abs=ATOL, rel=0)
    assert joint_information == pytest.approx(
        (2 / 3) * (1 - (2 / 3) * _binary_entropy(1 / 4)), abs=ATOL, rel=0
    )
    assert joint_information > direct_information > 0


def test_final_effects_are_left_invariant_but_not_conjugation_invariant():
    effects = _public_effects() + _final_effects()
    for x in GROUP:
        L, C = _left(x), _conjugation(x)
        for effect in effects:
            _assert_close(L @ effect, effect @ L)
        for P in _weak_irrep_projectors():
            _assert_close(C @ P, P @ C)
    x = (1, 2, 0)
    C = _conjugation(x)
    public_plus = _public_effects()[0]
    _assert_close(
        C @ public_plus @ C.conj().T,
        (EYE + _right(_conjugate(x, PUBLIC))) / 2,
    )
    standard_plus = _final_effects()[4]
    for effect in (public_plus, standard_plus):
        assert np.max(np.abs(C @ effect - effect @ C)) > 0.1


def test_covariant_luders_instrument_is_not_conjugation_twirling():
    projectors = _weak_irrep_projectors()
    conjugations = tuple(_conjugation(x) for x in GROUP)
    # Matrix units span every input operator, not just the three coset states.
    for row in range(len(GROUP)):
        for column in range(len(GROUP)):
            A = np.zeros_like(EYE)
            A[row, column] = 1
            for C in conjugations:
                for P in projectors:
                    _assert_close(
                        P @ (C @ A @ C.conj().T) @ P,
                        C @ (P @ A @ P) @ C.conj().T,
                    )
    states = tuple(_native_coset_state(hidden) for hidden in TRANSPOSITIONS)
    orbit_average = sum(states) / len(states)
    twirled = tuple(
        sum(C @ rho @ C.conj().T for C in conjugations) / len(GROUP)
        for rho in states
    )
    for rho, twirl in zip(states, twirled):
        _assert_density(twirl)
        _assert_close(twirl, orbit_average)
        _assert_close(sum(P @ rho @ P for P in projectors), rho)
        assert np.max(np.abs(twirl - rho)) > 0.1
    probabilities = _probabilities(twirled, _public_effects())
    _assert_close(probabilities, np.tile([2 / 3, 1 / 3], (3, 1)))
    assert abs(_mutual_information(probabilities)) <= ATOL
    assert abs(_mutual_information(_probabilities(twirled, _final_effects()))) <= ATOL


def _candidate_copy_bound(n, failure_probability):
    """Exact ceiling-log bound for fresh, disjoint candidate-test copies."""
    candidates = comb(n, 2)
    repeats = 0
    while Fraction(candidates - 1, 2 ** repeats) > failure_probability:
        repeats += 1
    return candidates, repeats, candidates * repeats


@pytest.mark.parametrize("n", (3, 4, 16, 64))
@pytest.mark.parametrize("failure_probability", (Fraction(1, 3), Fraction(2, 5), Fraction(1, 1024)))
def test_exact_polynomial_copy_union_bound_for_existing_public_test(n, failure_probability):
    candidates, repeats, copies = _candidate_copy_bound(n, failure_probability)
    false_survival = Fraction(1, 2) ** repeats
    assert Fraction(1) ** repeats == 1
    assert (candidates - 1) * false_survival <= failure_probability
    assert repeats > 0
    assert Fraction(candidates - 1, 2 ** (repeats - 1)) > failure_probability
    assert copies == comb(n, 2) * repeats
    # n^2 * denominator bounds (M-1)/delta, without floating-point logarithms.
    log_bound = 2 * (n - 1).bit_length() + (failure_probability.denominator - 1).bit_length()
    assert repeats <= log_bound
    assert copies <= comb(n, 2) * log_bound
    if n <= 4:
        exact_error = 1 - (1 - false_survival) ** (candidates - 1)
        assert exact_error <= (candidates - 1) * false_survival
