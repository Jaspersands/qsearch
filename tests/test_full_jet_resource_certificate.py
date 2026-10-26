"""Exact clocks and falsifiers for the adaptive full-jet resource theorem."""
from fractions import Fraction
from itertools import product
import json
from math import ceil, log2, prod

import numpy as np
import pytest

from theorems.full_jet_resource_certificate import (
    certificate_report, full_jet_resource_certificate, sde_arity, tree_schedule,
    weighted_slice_count,
)
from theorems.nil3_complete_budget import ceil_log


def budget(**changes):
    parameters = dict(p=7, ambient_class=4, quotient_width=1,
                      a_width=1, b_width=0, c_width=1)
    parameters.update(changes)
    return full_jet_resource_certificate(**parameters)


@pytest.mark.parametrize("p,c,m,r,s,z", [
    (7, 4, 1, 1, 0, 1), (19, 6, 6, 9, 2, 4),
    (2**127 - 1, 6, 6, 9, 2, 4), (17, 7, 1, 2, 1, 2),
])
def test_exact_schedule_and_error_budget(p, c, m, r, s, z):
    cert = budget(p=p, ambient_class=c, quotient_width=m, a_width=r, b_width=s, c_width=z)
    cert.validate()
    assert cert.trial_failure_bound < Fraction(1, 2)
    assert cert.queries == cert.leaves * cert.leaf_retry_cap * cert.batch
    assert cert.field_draws == cert.queries * cert.scale_draw_cap
    assert cert.instruments * cert.instrument_tolerance == cert.epsilon / 8
    assert sum(cert.failures.values()) <= 3 * cert.epsilon / 4
    assert [st.degree for st in cert.stages if st.kind == "ordinary"] == list(range(c-2, 0, -1))
    assert cert.curve_readouts == cert.roots * prod(st.arity for st in cert.stages if st.kind == "ordinary")
    for i, stage in enumerate(cert.stages):
        assert stage.nodes == cert.roots * prod(st.arity for st in cert.stages[i+1:])
    data = certificate_report(cert)
    json.dumps(data)  # even the 127-bit case must not hit huge-decimal limits
    assert int(data["counts"]["queries"]["hex"], 16) == cert.queries


def test_near_integer_logarithm_does_not_undercap_annihilator_samples():
    # The previous floating-point clock rounds this strictly larger ratio down.
    p, k = 7, 30
    epsilon = Fraction(4, p**k + 1)
    rounded = ceil((2 + log2(epsilon.denominator) - log2(epsilon.numerator)) / log2(p))
    assert rounded == k
    cert = budget(epsilon=epsilon)
    assert cert.roots == 1 + k + 1
    assert p**(cert.roots - cert.m - 1) < 4 / epsilon <= p**(cert.roots - cert.m)


def test_clock_minimality_and_tree_direction():
    cert = budget()
    for base, ratio, clock in (
        (cert.p, 8 * cert.batch, cert.scale_draw_cap),
        (2, 4 * cert.leaves / cert.epsilon, cert.leaf_retry_cap),
        (2, 8 * cert.field_draws / cert.epsilon, cert.binary_rejection_cap),
    ):
        assert base**(clock-1) < ratio <= base**clock
    stages, leaves = tree_schedule((("weighted", 2, 1, 2), ("ordinary", 1, 2, 3)), 5)
    assert [st.nodes for st in stages] == [15, 5]
    assert leaves == 30
    assert sum(st.nodes*(st.arity-1) for st in stages) == leaves - 5


@pytest.mark.parametrize("changes", [
    {"epsilon": 0.125}, {"epsilon": Fraction(0)}, {"epsilon": Fraction(1)},
    {"quotient_width": 1.0}, {"a_width": 0}, {"b_width": -1},
    {"ambient_class": 3}, {"p": 5},
])
def test_invalid_envelopes_rejected(changes):
    with pytest.raises(ValueError):
        budget(**changes)


def test_published_sde_arity_and_exact_collision_depth():
    assert sde_arity(1, 4) == 5
    assert sde_arity(2, 3) == 1024
    for degree in range(2, 33):
        layers = ceil_log(2, degree + 1)
        expected = (degree**(degree*(degree-1)//2) * 3**degree)**layers
        assert sde_arity(degree, 2) == expected


@pytest.mark.parametrize("m,multiplicities", [(1, (2, 1)), (2, (1, 1))])
def test_structured_weighted_counts_match_independent_monomial_enumeration(m, multiplicities):
    weights = [k for k, number in enumerate(multiplicities, 1) for _ in range(number)]
    for weight in range(7):
        for q_bound, t_bound in ((2, 2), (4, 1), (3, 0)):
            expected = 0
            for q in product(range(q_bound+1), repeat=m):
                if sum(q) > q_bound:
                    continue
                for t in product(range(t_bound+1), repeat=len(weights)):
                    if sum(t) <= t_bound and sum(q)+sum(x*w for x, w in zip(t, weights)) == weight:
                        expected += 1
            assert weighted_slice_count(m, multiplicities, weight, q_bound, t_bound) == expected


def test_source_structure_strictly_reduces_every_stage_envelope():
    structured = budget()
    generic = budget(support_model="generic")
    assert structured.leaves < generic.leaves
    assert structured.queries < generic.queries
    for small, large in zip(structured.stages, generic.stages):
        assert small.kind == large.kind and small.degree == large.degree
        assert small.equations < large.equations
        assert small.arity < large.arity


def test_rank_witness_polynomials_on_nonzero_scale_domain():
    # D=2,m=1: after dividing by s, the full feature row is (1,Y,s).
    p = 5
    points = tuple(product(range(p), range(1, p)))
    maximum = Fraction(0)
    for coefficients in product(range(p), repeat=3):
        if not any(coefficients):
            continue
        zeros = sum((coefficients[0] + coefficients[1]*y + coefficients[2]*s) % p == 0
                    for y, s in points)
        maximum = max(maximum, Fraction(zeros, len(points)))
    assert maximum == Fraction(1, p-1)
    ell, degree = 3, 2
    batch = (ell+1) * p.bit_length() + 2
    rank_union = (p**ell-1) * Fraction(degree-1, p-1)**batch
    assert rank_union <= Fraction(1, 4*p)


def test_adaptive_retry_bound_needs_conditional_not_marginal_hazards():
    # Histories have non-IID transition laws but every conditional failure <=1/2.
    histories = {(): Fraction(1)}
    failed = Fraction(0)
    for retry in range(6):
        new = {}
        for history, mass in histories.items():
            hazard = Fraction(1, 2) if sum(history) % 2 else Fraction(1, 3)
            for label in (0, 1):
                new[history + (label,)] = mass * hazard / 2
        histories = new
        failed = sum(histories.values())
        assert failed <= Fraction(1, 2**(retry+1))
    # Reuse a single latent bad seed: each marginal failure is 1/2, but retries do not help.
    correlated_all_fail = Fraction(1, 2)
    assert correlated_all_fail > Fraction(1, 2**6) >= failed


def trace_distance(left, right):
    return np.linalg.svd(left-right, compute_uv=False).sum() / 2


def test_forgetting_shared_record_breaks_product_state_premise():
    retained = np.diag([0.5, 0, 0, 0.5])
    product_of_marginals = np.eye(4) / 4
    assert trace_distance(retained, product_of_marginals) == pytest.approx(0.5)


def test_rare_branch_normalization_can_amplify_global_error():
    probability = 2**-20
    ideal = np.diag([1-probability, 0, probability, 0])
    approximate = np.diag([1-probability, 0, 0, probability])
    assert trace_distance(ideal, approximate) == pytest.approx(probability, abs=1e-15)
    assert trace_distance(ideal[2:, 2:]/probability, approximate[2:, 2:]/probability) == 1


def test_frontend_uses_exact_certificate_for_large_prime():
    from theorems.class_three_ambient_frontend import class_three_full_jet_resource_budget
    data = class_three_full_jet_resource_budget(
        p=2**127-1, ambient_class=4, quotient_width=1, a_width=1, b_width=0, c_width=1)
    assert data["adaptive_resource_certificate"]["schema"] == "full_jet_adaptive_resource_certificate_v1"
    assert data["matrix_batch_rank_failure_bound"] == str(Fraction(1, 4*(2**127-1)))
