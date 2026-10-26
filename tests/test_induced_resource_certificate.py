"""Support-envelope and exact-schedule falsifiers, not algorithm benchmarks."""
from dataclasses import replace
from fractions import Fraction
from itertools import combinations_with_replacement, product
import json
from math import comb, prod

import pytest

from theorems.class_three_monomial_jet import FullTaylorJetChart
from theorems.induced_resource_certificate import (
    exact_ceil_log, induced_equation_bounds, induced_resource_certificate,
    jet_monomial_table, mixed_slice_count, report,
)
from theorems.metabelian_induced_phase import (
    InducedPhasePacket, align_induced_jet, compile_induced_phase,
    induced_leading_columns, merge_induced_phases, pullback_induced_phase,
)
from theorems.nil3_complete_budget import ceil_log
from tests.test_metabelian_induced_phase import design, filiform_chart


def budget(**changes):
    values = dict(p=43, ambient_class=9, normal_class=4,
                  quotient_width=2, a_width=7, ideal_width=10)
    values.update(changes)
    return induced_resource_certificate(**values)


def test_exact_logarithm_including_large_near_boundaries():
    for base in range(2, 12):
        for numerator, denominator in product(range(1, 40), repeat=2):
            if numerator >= denominator:
                value = Fraction(numerator, denominator)
                assert exact_ceil_log(base, value) == ceil_log(base, value)
    for base in (2, 43, 2**127-1):
        for exponent in (1, 5, 37):
            exact = base**exponent
            assert exact_ceil_log(base, exact) == exponent
            assert exact_ceil_log(base, Fraction(exact*11+1, 11)) == exponent+1
    assert exact_ceil_log(2, 2**100_000+1) == 100_001
    with pytest.raises(ValueError):
        exact_ceil_log(2, 1.0)


@pytest.mark.parametrize("multiplicities", [(2, 0, 1), (1, 1), (0, 0)])
def test_general_jet_counter_against_independent_enumeration(multiplicities):
    weights = tuple(w for w, count in enumerate(multiplicities, 1) for _ in range(count))
    maximum, max_weight = 4, 12
    table = jet_monomial_table(multiplicities, maximum, max_weight)
    expected = [[0]*(max_weight+1) for _ in range(maximum+1)]
    for exponents in product(range(maximum+1), repeat=len(weights)):
        d, w = sum(exponents), sum(e*v for e, v in zip(exponents, weights))
        if d <= maximum and w <= max_weight:
            expected[d][w] += 1
    assert table == tuple(map(tuple, expected))
    for m, q_bound, t_bound, weight in product((1, 2), (0, 2, 5), range(5), range(9)):
        count = 0
        for q in product(range(q_bound+1), repeat=m):
            if sum(q) > q_bound:
                continue
            for exponents in product(range(t_bound+1), repeat=len(weights)):
                if sum(exponents) <= t_bound and sum(q)+sum(e*w for e, w in zip(exponents, weights)) == weight:
                    count += 1
        assert mixed_slice_count(m, table, weight, q_bound, t_bound) == count


def test_parameter_lift_and_full_pair_counts_by_enumeration():
    m, r, b, d, k = 1, 1, 1, 2, 3
    h_a, h_i = r*comb(m+d, m), b*comb(m+d, m)
    chart = FullTaylorJetChart(11, m, r, d)
    counts, _ = induced_equation_bounds(m, r, b, d, k)
    explicit = dict.fromkeys(counts, 0)
    supported_parameters = 0
    for h in range(1, k+1):
        for parameters in combinations_with_replacement(range(h_a+h_i), h):
            ideals = sum(i >= h_a for i in parameters)
            if ideals > 1 or (not ideals and h == k):
                continue
            supported_parameters += 1
            for q_degree in range(h*d+1):
                for beta in product(range(k-h+1), repeat=chart.jet_width):
                    if sum(beta) > k-h:
                        continue
                    weight = chart.weighted_degree((q_degree,)+beta)
                    if weight:
                        explicit[weight] += 1
    assert explicit == counts
    assert supported_parameters == (1+h_i)*comb(h_a+k-1, k-1)-1


@pytest.mark.parametrize("carrier_width", [1, 2])
def test_actual_compiler_and_pullbacks_fit_every_stage_bound(carrier_width):
    st = replace(filiform_chart(17, 4), a_width=carrier_width)
    ch = FullTaylorJetChart(17, 1, carrier_width, 2)
    a = align_induced_jet(ch, st, *design(ch, st))
    spectator = tuple(range(1, carrier_width+1))
    initial = compile_induced_phase(a, spectator)
    pulled = pullback_induced_phase(initial, (3,), (1,)*ch.jet_width, 2)
    opposite = replace(initial, terms={key: -c % 17 for key, c in initial.terms.items()})
    merged = merge_induced_phases([initial, opposite], (1, 1),
                                  [((0,), (0,)*ch.jet_width), ((3,), (1,)*ch.jet_width)], initial.weighted_degree)
    bounds, _ = induced_equation_bounds(1, carrier_width, st.ideal_width, 2, 4)
    for packet in (initial, pulled, merged):
        packet.validate()
        for j, upper in bounds.items():
            assert sum(ch.weighted_degree(alpha) == j for alpha, _ in packet.terms) <= upper
        for j in range(packet.weighted_degree, 9):
            _, keys = induced_leading_columns([packet], j)
            assert len(keys) <= bounds[j]


def test_old_weight_bound_does_not_imply_separated_source_support():
    ch = FullTaylorJetChart(17, 1, 2, 2)
    t2 = next(i for i, weight in enumerate(ch.weights[1:]) if weight == 2)
    alpha = (6,)+tuple(int(i == t2) for i in range(ch.jet_width))
    packet = InducedPhasePacket(ch, 5, 4, {(alpha, (0, 0, 0)): 1})
    assert packet.weighted_degree == 8
    # t_weight2 <- t_weight2+q obeys generic triangular weight constraints,
    # but is NOT the actual block-separated Taylor transport.
    leaked = (7,)+(0,)*ch.jet_width
    assert ch.weighted_degree(leaked) < packet.weighted_degree
    with pytest.raises(ValueError, match="separated"):
        replace(packet, terms={**packet.terms, (leaked, (0, 0, 0)): 1})
    with pytest.raises(ValueError, match="separated"):
        replace(packet, terms={((3,)+(0,)*ch.jet_width, (0,)): 1})
    with pytest.raises(ValueError, match="separated"):
        replace(packet, terms={((1,)+(0,)*ch.jet_width, ()): 1})


@pytest.mark.parametrize("p", [43, 2**127-1])
def test_new_scope_exact_schedule_and_joint_error(p):
    cert = budget(p=p)
    cert.validate()
    assert [s.degree for s in cert.stages if s.kind == "weighted"] == list(range(36, 0, -1))
    assert [s.degree for s in cert.stages if s.kind == "ordinary"] == list(range(9, 0, -1))
    assert cert.queries == cert.leaves*cert.leaf_retry_cap*cert.batch
    assert cert.trial_failure_bound < Fraction(1, 2)
    assert sum(cert.failures.values()) <= 3*cert.epsilon/4
    for index, stage in enumerate(cert.stages):
        assert stage.nodes == cert.roots*prod(s.arity for s in cert.stages[index+1:])
    data = report(cert)
    json.dumps(data)
    for name, exponent in data["counts_upper_power_of_two_exponents"].items():
        actual = getattr(cert, name)
        assert 2**(exponent-1) < actual <= 2**exponent
    assert not data["speedup_claim_allowed"]
    with pytest.raises(AssertionError):
        replace(cert, leaf_retry_cap=cert.leaf_retry_cap-1).validate()
    with pytest.raises(AssertionError):
        replace(cert, stages=(replace(cert.stages[0], equations=1),)+cert.stages[1:]).validate()


def test_new_support_reduces_every_weighted_stage_without_changing_the_claim():
    small, generic = budget(), budget(support_model="generic")
    assert small.queries < generic.queries
    for s, g in zip(small.stages, generic.stages):
        if s.kind == "weighted":
            assert s.equations < g.equations and s.arity < g.arity
        else:
            assert s.equations == g.equations and s.arity == g.arity
    from theorems.full_jet_resource_certificate import full_jet_resource_certificate
    with pytest.raises(ValueError):
        # There is no correct way to request a normal-class-four induced
        # source by pretending that the old B/C dimensions are its fibers.
        full_jet_resource_certificate(p=43, ambient_class=9, quotient_width=2,
                                       a_width=7, b_width=10, c_width=0)


@pytest.mark.parametrize("changes", [{"normal_class": 5}, {"normal_class": 1}, {"p": 31},
    {"quotient_width": 0}, {"ideal_width": 0}, {"epsilon": 0.125}, {"support_model": "quadratic"}])
def test_invalid_resource_promises_are_rejected(changes):
    with pytest.raises(ValueError):
        budget(**changes)
