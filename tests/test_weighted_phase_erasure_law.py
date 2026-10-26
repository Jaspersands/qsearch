"""Bridge the universal filtered-polynomial law to the full-jet compiler."""

import random

import pytest

from theorems.class_three_monomial_jet import FullTaylorJetChart
from theorems.nonlinear_jet_erasure import (
    pullback_phase, verify_weighted_witness, weighted_degree, weighted_merge,
)
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket


def _phase(chart, terms):
    return SymbolicScalarPacket(chart.p, chart.quotient_width, chart.jet_width,
                                ((0, (1, 0)), (0, (0, 1))), terms)


def _terms_at_weight(chart, degree, rng):
    terms = {}
    lifts = [(), (0,), (1,), (0, 0), (0, 1), (1, 1)]
    # Include each jet weight and mixed terms; fill the remaining weight
    # with quotient variables, whose weight is one.
    for i, weight in enumerate(chart.weights):
        alpha = [0]*chart.width
        alpha[i] += 1
        alpha[0] += degree-weight
        for lift in lifts:
            terms[(tuple(alpha), lift)] = rng.randrange(1, chart.p)
    for _ in range(12):
        alpha, remaining = [0]*chart.width, degree
        while remaining:
            possible = [i for i, w in enumerate(chart.weights) if w <= remaining]
            i = rng.choice(possible)
            alpha[i] += 1
            remaining -= chart.weights[i]
        terms[(tuple(alpha), rng.choice(lifts))] = rng.randrange(1, chart.p)
    return terms


@pytest.mark.parametrize("p", [17, 2**127-1])
@pytest.mark.parametrize("D", [2, 3])
def test_full_jet_leading_law_with_every_parameter_lift_and_zero_scale_discard(p, D, monkeypatch):
    chart, rng = FullTaylorJetChart(p, 2, 1, D), random.Random(407+D)
    degree = 3*D
    leading = _terms_at_weight(chart, degree, rng)
    first = dict(leading)
    first.update(_terms_at_weight(chart, degree-1, rng))
    multiplier = -pow(pow(2, degree, p), -1, p) % p
    second = {key: value*multiplier % p for key, value in leading.items()}
    second.update(_terms_at_weight(chart, degree-2, rng))
    packets = [_phase(chart, first), _phase(chart, second), _phase(chart, leading)]
    scales = [1, 2, 0]
    def forbidden(*args):
        raise AssertionError("hidden parameter evaluation is not an erasure certificate")
    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", forbidden)
    verify_weighted_witness(chart, packets, scales, degree)
    for _ in range(4):
        outcomes = [(tuple(rng.randrange(p) for _ in range(2)),
                     tuple(rng.randrange(p) for _ in chart.indices)) for _ in range(2)]
        # Invalid dimensions are intentional: a zero-scale input is discarded,
        # not submitted to an invertible transport or reused as a source.
        outcomes.append(((), ()))
        for packet, scale, (y, z) in zip(packets[:2], scales[:2], outcomes[:2]):
            _, matrix = chart.affine_map(y, z, scale)
            for i, row in enumerate(matrix):
                assert row[i] == pow(scale, chart.weights[i], p)
                assert all(value == 0 for j, value in enumerate(row)
                           if j != i and chart.weights[j] >= chart.weights[i])
            pulled = pullback_phase(chart, packet, y, z, scale)
            actual = {key: value for key, value in pulled.terms.items()
                      if chart.weighted_degree(key[0]) == degree}
            expected = {key: value*pow(scale, degree, p) % p for key, value in packet.terms.items()
                        if chart.weighted_degree(key[0]) == degree}
            assert actual == expected
            assert all(len(parameters) <= 2 for _, parameters in pulled.terms)
        result = weighted_merge(chart, packets, scales, outcomes, degree)
        assert weighted_degree(chart, result) < degree
        without_discard = weighted_merge(chart, packets[:2], scales[:2], outcomes[:2], degree)
        assert result.terms == without_discard.terms


@pytest.mark.parametrize("p", [11, 2**127-1])
def test_same_weight_outcome_dependent_mixing_defeats_diagonal_cancellation(p):
    class InvalidTransport(FullTaylorJetChart):
        def affine_map(self, y, z, scale):
            offset, matrix = super().affine_map(y, z, scale)
            rows = [list(row) for row in matrix]
            rows[0][1] = y[0]  # Forbidden equal-weight q_1 into q_0 mixing.
            return offset, tuple(map(tuple, rows))
    chart = InvalidTransport(p, 2, 1, 2)
    alpha = (3,)+(0,)*(chart.width-1)
    packets = [_phase(chart, {(alpha, (0, 1)): coefficient}) for coefficient in (1, p-1)]
    verify_weighted_witness(chart, packets, [1, 1], 3)
    outcomes = [((0, 0), (0,)*chart.jet_width), ((1, 0), (0,)*chart.jet_width)]
    with pytest.raises(ArithmeticError, match="weighted degree did not decrease"):
        weighted_merge(chart, packets, [1, 1], outcomes, 3)
