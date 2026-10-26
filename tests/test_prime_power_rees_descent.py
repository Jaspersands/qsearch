"""Exact arithmetic/source countercontrols, not generated HSP candidates."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import gcd

import numpy as np
import pytest

from theorems.prime_power_rees_descent import (
    batch_success_probability, lift_batch_witness, plan_batch, retry_tree_budget,
)


@lru_cache(maxsize=None)
def _finite_witness(labels, p, d):
    # Bounded test oracle only. The production module contains no enumeration.
    delta = gcd(d, p-1)
    for witness in product(range(p), repeat=len(labels)):
        if any(witness) and sum(a*pow(x, delta, p) for a, x in zip(labels, witness)) % p == 0:
            return witness
    raise AssertionError("finite scalar diagonal witness missing")


def _get_witness(labels, p, e, d):
    plan = plan_batch(labels, prime=p, exponent=e, degree=d)
    if plan.action == "zero":
        return plan.zero_witness
    if plan.action == "hensel":
        return lift_batch_witness(labels, _finite_witness(plan.field_labels, p, d),
                                  prime=p, exponent=e, degree=d)
    return None


@pytest.mark.parametrize("p,e,d", [(3, 2, 2), (3, 3, 2), (5, 2, 3)])
def test_every_small_central_label_batch_and_all_hidden_intersections(p, e, d):
    modulus = p**e
    arity = gcd(d, p-1) + 1
    for b in range(e+1):
        labels_allowed = tuple(range(0, modulus, p**b))
        actions = Counter()
        for labels in product(labels_allowed, repeat=arity):
            plan = plan_batch(labels, prime=p, exponent=e, degree=d)
            actions[plan.action] += 1
            witness = _get_witness(labels, p, e, d)
            if witness is not None:
                assert any(witness)
                assert all(s == 0 or gcd(s, modulus) == 1 for s in witness)
                assert sum(a*pow(s, d, modulus) for a, s in zip(labels, witness)) % modulus == 0
        actual = Fraction(actions["zero"] + actions["hensel"], len(labels_allowed)**arity)
        assert actual == batch_success_probability(prime=p, exponent=e, degree=d,
                                                   intersection_exponent=b)
        assert actual >= Fraction(1, 4)


@pytest.mark.parametrize("p,e,d", [(3, 8, 2), (5, 9, 3), (2**127-1, 32, 6)])
def test_large_modulus_hensel_lift_has_no_field_or_ring_enumeration(p, e, d):
    arity = gcd(d, p-1) + 1
    modulus = p**e
    for valuation in (0, e//2, e-1):
        unit_modulus = p**(e-valuation)
        normalized = [1, (-1 + p) % unit_modulus] + [1]*(arity-2)
        labels = tuple(p**valuation*a for a in normalized)
        field_witness = (1, 1) + (0,)*(arity-2)
        witness = lift_batch_witness(labels, field_witness, prime=p, exponent=e, degree=d)
        assert witness[2:] == (0,)*(arity-2)
        assert witness[0] % p == witness[1] % p == 1
        assert sum(a*pow(s, d, modulus) for a, s in zip(labels, witness)) % modulus == 0


def test_distinct_valuations_need_retry_and_have_no_unit_or_zero_witness():
    labels = (1, 3, 9)
    assert plan_batch(labels, prime=3, exponent=3, degree=2).action == "retry"
    permitted = (0,) + tuple(x for x in range(27) if x % 3)
    assert not any(any(s) and sum(a*x*x for a, x in zip(labels, s)) % 27 == 0
                   for s in product(permitted, repeat=3))
    # A nonzero nonunit gives a spurious phase zero, not a legal dilation.
    assert 1 * 9**2 % 27 == 0


def test_reducing_divisible_labels_mod_p_without_normalizing_is_wrong():
    labels = (3, 6, 3)
    assert tuple(x % 3 for x in labels) == (0, 0, 0)
    assert sum(a*s*s for a, s in zip(labels, (1, 0, 0))) % 9 != 0
    plan = plan_batch(labels, prime=3, exponent=2, degree=2)
    assert plan.field_labels == (1, 2, 1)
    assert _get_witness(labels, 3, 2, 2) is not None


def _conditional_states(modulus, central_step):
    points = tuple(product(range(modulus), repeat=2))
    index = {x: i for i, x in enumerate(points)}
    def action(g):
        return np.array([index[((x-g[0]) % modulus, (y-g[1]) % modulus)] for x, y in points])
    eye = np.eye(len(points))
    h = tuple(product(range(0, modulus, 3), range(0, modulus, central_step)))
    rho = sum(eye[:, action(g)] for g in h)/len(points)
    states = {}
    for label in range(modulus):
        projector = sum(np.exp(-2j*np.pi*label*z/modulus)*eye[:, action((0, z))]
                        for z in range(modulus))/modulus
        branch = projector @ rho
        mass = np.trace(branch).real
        if mass > 1e-12:
            states[label] = branch/mass
        else:
            np.testing.assert_allclose(branch, 0, atol=1e-12)
    def correlation(label, g):
        # R_g sends |x> to |x-g>; sum rho[x,x-g] is Tr(rho R_g).
        return np.sum(states[label][np.arange(len(points)), action(g)])
    return states, correlation


def _instrument(modulus, labels, scales, degree, correlation):
    result = np.zeros((modulus, modulus), complex)
    for q, r in product(range(modulus), repeat=2):
        value = 1
        for label, scale in zip(labels, scales):
            if scale:
                # Nonlinear section sigma(q)=(q,q^2) makes cancellation visible.
                g = (scale*(q-r) % modulus, pow(scale, degree, modulus)*(q*q-r*r) % modulus)
                value *= correlation(label, g)
        result[q, r] = value/modulus
    return result


@pytest.mark.parametrize("central_step,labels", [(9, (1, 1, 1)), (9, (0, 1, 3)),
                                                 (3, (3, 3, 3)), (1, (0, 0, 0))])
def test_full_central_density_contraction_with_all_intersection_types(central_step, labels):
    states, correlation = _conditional_states(9, central_step)
    assert all(label in states for label in labels)
    scales = _get_witness(labels, 3, 2, 2)
    output = _instrument(9, labels, scales, 2, correlation)
    expected = np.array([[float((q-r) % 3 == 0)/9 for r in range(9)] for q in range(9)])
    np.testing.assert_allclose(output, expected, atol=2e-14)


def test_nonunit_phase_zero_produces_false_whole_quotient_signal():
    _, correlation = _conditional_states(9, 9)
    labels, wrong_scales = (1, 1, 1), (3, 0, 0)
    assert sum(a*s*s for a, s in zip(labels, wrong_scales)) % 9 == 0
    output = _instrument(9, labels, wrong_scales, 2, correlation)
    expected = np.array([[float((q-r) % 3 == 0)/9 for r in range(9)] for q in range(9)])
    np.testing.assert_allclose(output, np.ones((9, 9))/9, atol=2e-14)
    np.testing.assert_allclose(np.abs(np.linalg.eigvalsh(output-expected)).sum()/2,
                               2/3, atol=2e-14)


def test_mixed_torsion_rees_interpolation_without_free_module_assumption():
    # L=(Z/9)^3, [x,y]=3z, gamma_2=<3z> has order3, not order9.
    # h=<x+z,3y> is a nonnormal Lie subring with h intersect gamma_2=0.
    def in_h(v):
        x, y, z = v
        return y % 3 == 0 and (z-x) % 9 == 0
    def evaluate(a, s):
        x, y, z, w = a
        return (s*x % 9, s*y % 9, (s*z + 3*s*s*w) % 9)
    for x, y, z in product(range(9), repeat=3):
        for w in range(3):
            a = (x, y, z, w)
            hidden = in_h((x, y, z)) and w == 0
            assert all(in_h(evaluate(a, s)) for s in (1, 2)) == hidden
            for unit in (1, 2, 4, 5, 7, 8):
                dilated = (unit*x % 9, unit*y % 9, unit*z % 9, unit*unit*w % 3)
                assert (in_h(dilated[:3]) and dilated[3] == 0) == hidden
    # Distinct ring elements need distinct residues modulo p for Vandermonde.
    bad = (0, 0, 6, 1)
    assert evaluate(bad, 1) == evaluate(bad, 4) == (0, 0, 0)
    assert evaluate(bad, 2) != (0, 0, 0)


def test_cyclic_rank_does_not_bound_lie_ring_class():
    # Over Z/5^4, [x,y]=5y: rank([L,L])=1 but class=4.
    p, exponent = 5, 4
    modulus = p**exponent
    def bracket(x, y):
        return (0, p*(x[0]*y[1] - x[1]*y[0]) % modulus)
    word = (0, 1)
    for step in range(1, exponent):
        word = bracket((1, 0), word)
        assert word == (0, p**step)
    assert bracket((1, 0), word) == (0, 0)


def test_retry_clock_counts_failed_batches_not_just_successful_tree():
    budget = retry_tree_budget(prime=5, nilpotency_class=3,
                               higher_grade_cyclic_ranks=(2, 1), terminal_samples=7)
    assert budget["expected_lifted_leaves_upper"] == 7*12**2*8
    assert budget["expected_original_inputs_upper"] == 3*7*12**2*8
    assert budget["hard_original_input_cap"] == 16*budget["expected_original_inputs_upper"]
    assert budget["full_instrument_cap"] == 2*budget["hard_lifted_leaf_cap"]+7
    assert budget["clock_failure_upper"] == "1/16"


@pytest.mark.parametrize("labels,p,e,d", [((1, 1, 1), 3, 0, 2), ((1, 1), 3, 2, 3),
                                        ((1, 1), 3, 2, 2), ((-1, 1, 1), 3, 2, 2),
                                        ((True, 1, 1), 3, 2, 2)])
def test_invalid_batch_contracts(labels, p, e, d):
    with pytest.raises(ValueError):
        plan_batch(labels, prime=p, exponent=e, degree=d)


def test_false_witness_and_retry_batch_are_not_lifted():
    for labels, witness in [((1, 1, 1), (0, 0, 0)), ((1, 1, 1), (1, 0, 0)),
                            ((1, 3, 9), (1, 1, 1))]:
        with pytest.raises(ValueError):
            lift_batch_witness(labels, witness, prime=3, exponent=3, degree=2)


def test_source_probability_is_not_valid_for_an_arbitrary_fixed_label_bank():
    labels = (1, 3, 9)
    assert plan_batch(labels, prime=3, exponent=3, degree=2).action == "retry"
    # Replaying this bank fails forever. The ideal probability is not a
    # guarantee about arbitrary/adversarial labels or a source certificate.
    assert batch_success_probability(prime=3, exponent=3, degree=2,
                                     intersection_exponent=0) > Fraction(1, 4)


@pytest.mark.parametrize("p,c,ranks,samples", [(5, 3, (1, 2), 7), (5, 3, (2,), 7),
                                               (3, 3, (1, 1), 7), (5, 3, (2, 1), True)])
def test_invalid_retry_profiles(p, c, ranks, samples):
    with pytest.raises(ValueError):
        retry_tree_budget(prime=p, nilpotency_class=c,
                          higher_grade_cyclic_ranks=ranks, terminal_samples=samples)
